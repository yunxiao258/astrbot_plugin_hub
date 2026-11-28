"""AstrBot 插件生态中枢异步 Web 管理面板服务器（aiohttp.web）。"""

from __future__ import annotations

import hmac
import importlib
import os
import secrets
import time
from typing import Any

from aiohttp import web

from . import web_ui as _web_ui

LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
COOKIE_NAME = "astrbot_hub_token"
_WEB_UI_MTIME: float = 0.0


def _load_dashboard_html() -> str:
    """按文件修改时间热读取最新面板 HTML，避免 AstrBot 热重载子模块缓存滞后。"""
    global _WEB_UI_MTIME
    ui_file = getattr(_web_ui, "__file__", "") or ""
    if ui_file and os.path.isfile(ui_file):
        try:
            mt = os.path.getmtime(ui_file)
            if _WEB_UI_MTIME and mt != _WEB_UI_MTIME:
                importlib.reload(_web_ui)
            _WEB_UI_MTIME = mt
        except Exception:
            pass
    return _web_ui.DASHBOARD_HTML


class HubWebServer:
    """内置端口 Web 管理服务：本机 127.0.0.1 默认免登，外网/0.0.0.0 绑定强制 Token 鉴权。"""

    def __init__(
        self,
        hub: Any,
        host: str = "127.0.0.1",
        port: int = 8686,
        token: str = "",
        require_auth_on_localhost: bool = False,
        token_file: str = "",
    ) -> None:
        self.hub = hub
        self.host = (host or "127.0.0.1").strip()
        self.port = max(0, min(65535, int(port)))
        self.require_auth_on_localhost = bool(require_auth_on_localhost)
        self.token = self._resolve_token(token, token_file)
        self.started_at = time.monotonic()

        self._app: web.Application | None = None
        self._runner: web.AppRunner | None = None
        self._site: web.TCPSite | None = None
        self.bound_port: int = self.port

    @staticmethod
    def _resolve_token(configured: str, token_file: str) -> str:
        c = (configured or "").strip()
        if c:
            return c
        if token_file and os.path.isfile(token_file):
            try:
                saved = open(token_file, "r", encoding="utf-8").read().strip()
                if saved:
                    return saved
            except OSError:
                pass
        generated = secrets.token_urlsafe(24)
        if token_file:
            try:
                os.makedirs(os.path.dirname(os.path.abspath(token_file)), exist_ok=True)
                with open(token_file, "w", encoding="utf-8", newline="\n") as f:
                    f.write(generated + "\n")
            except OSError:
                pass
        return generated

    def is_loopback_bind(self) -> bool:
        return self.host.lower() in LOOPBACK_HOSTS

    def auth_required_for_request(self, request: web.Request) -> bool:
        if self.require_auth_on_localhost or not self.is_loopback_bind():
            return True
        peer = (request.remote or "").strip().lower()
        # 本机监听且确实来自回环客户端时免登；经反向代理或非回环来源仍校验 Token
        if peer and peer not in ("127.0.0.1", "::1", "localhost"):
            return True
        if request.headers.get("X-Forwarded-For"):
            return True
        return False

    def _is_authenticated(self, request: web.Request) -> bool:
        if not self.auth_required_for_request(request):
            return True
        auth_hdr = request.headers.get("Authorization", "")
        cand = ""
        if auth_hdr.lower().startswith("bearer "):
            cand = auth_hdr[7:].strip()
        if not cand:
            cand = (request.cookies.get(COOKIE_NAME) or "").strip()
        if not cand:
            cand = (request.query.get("token") or "").strip()
        return bool(cand) and hmac.compare_digest(cand, self.token)

    def build_app(self) -> web.Application:
        @web.middleware
        async def auth_middleware(request: web.Request, handler):
            path = request.path
            public_paths = {"/", "/api/health", "/api/login", "/api/logout"}
            if path.startswith("/api/") and path not in public_paths:
                if not self._is_authenticated(request):
                    return web.json_response(
                        {"ok": False, "error": "需要管理员 Token 登录"}, status=401
                    )
            resp = await handler(request)
            resp.headers["X-Content-Type-Options"] = "nosniff"
            resp.headers["X-Frame-Options"] = "SAMEORIGIN"
            return resp

        app = web.Application(middlewares=[auth_middleware])
        app.router.add_get("/", self._handle_index)
        app.router.add_get("/api/health", self._handle_health)
        app.router.add_post("/api/login", self._handle_login)
        app.router.add_post("/api/logout", self._handle_logout)
        app.router.add_get("/api/overview", self._handle_overview)
        app.router.add_get("/api/plugins", self._handle_plugins)
        app.router.add_get("/api/plugins/{name}/config", self._handle_get_config)
        app.router.add_post("/api/plugins/{name}/config", self._handle_save_config)
        app.router.add_post("/api/plugins/{name}/action", self._handle_plugin_action)
        app.router.add_get("/api/rules", self._handle_list_rules)
        app.router.add_post("/api/rules/{rule_id}/toggle", self._handle_toggle_rule)
        app.router.add_post("/api/rules/custom", self._handle_add_custom_rule)
        app.router.add_delete(
            "/api/rules/custom/{rule_id}", self._handle_delete_custom_rule
        )
        app.router.add_get("/api/events", self._handle_events)
        app.router.add_post("/api/events/emit", self._handle_emit_event)
        app.router.add_get("/api/data/{panel}", self._handle_data_panel)
        app.router.add_post("/api/points/adjust", self._handle_adjust_points)
        return app

    async def start(self) -> int:
        if self._runner is not None:
            return self.bound_port
        self._app = self.build_app()
        self._runner = web.AppRunner(self._app, access_log=None)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, self.host, self.port)
        await self._site.start()
        # 获取实际绑定端口（支持测试中传 port=0 随机分配）
        try:
            sock = self._site._server.sockets[0]
            self.bound_port = int(sock.getsockname()[1])
        except Exception:
            self.bound_port = self.port
        self.started_at = time.monotonic()
        return self.bound_port

    async def stop(self) -> None:
        if self._runner is not None:
            try:
                await self._runner.cleanup()
            except Exception:
                pass
        self._runner = None
        self._site = None
        self._app = None

    @property
    def url(self) -> str:
        display_host = "127.0.0.1" if self.host == "0.0.0.0" else self.host
        return f"http://{display_host}:{self.bound_port}"

    # ==================== HTTP 路由处理 ====================

    @staticmethod
    async def _read_json_dict(request: web.Request) -> dict[str, Any] | None:
        try:
            body = await request.json()
        except Exception:
            return None
        return body if isinstance(body, dict) else None

    async def _handle_index(self, request: web.Request) -> web.Response:
        return web.Response(
            text=_load_dashboard_html(),
            content_type="text/html",
            charset="utf-8",
            headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
        )

    async def _handle_health(self, request: web.Request) -> web.Response:
        return web.json_response(
            {
                "ok": True,
                "plugin": "astrbot_plugin_hub",
                "host": self.host,
                "port": self.bound_port,
                "auth_required": self.auth_required_for_request(request),
                "uptime_seconds": int(time.monotonic() - self.started_at),
            }
        )

    async def _handle_login(self, request: web.Request) -> web.Response:
        body = await self._read_json_dict(request)
        if body is None:
            return web.json_response(
                {"ok": False, "error": "无效 JSON 对象"}, status=400
            )
        tok = str(body.get("token", "") or "").strip()
        if not tok or not hmac.compare_digest(tok, self.token):
            return web.json_response({"ok": False, "error": "Token 不正确"}, status=401)
        resp = web.json_response({"ok": True})
        resp.set_cookie(COOKIE_NAME, tok, httponly=True, samesite="Lax", path="/")
        return resp

    async def _handle_logout(self, request: web.Request) -> web.Response:
        resp = web.json_response({"ok": True})
        resp.del_cookie(COOKIE_NAME, path="/")
        return resp

    async def _handle_overview(self, request: web.Request) -> web.Response:
        plugins = self.hub.registry.list_plugins(include_third_party=True)
        rules = self.hub.bus.list_rules()
        return web.json_response(
            {
                "ok": True,
                "server": {
                    "host": self.host,
                    "port": self.bound_port,
                    "url": self.url,
                    "uptime_seconds": int(time.monotonic() - self.started_at),
                },
                "auth": {
                    "required": self.auth_required_for_request(request),
                    "loopback_bind": self.is_loopback_bind(),
                },
                "auto_linkage_enabled": bool(
                    self.hub.cfg_bool("auto_linkage_enabled", True)
                ),
                "event_count": len(self.hub.bus._events),
                "total_rule_triggers": sum(
                    int(r.get("triggered_count", 0)) for r in rules
                ),
                "eco_users": self.hub.bus.count_eco_users(),
                "plugins": plugins,
            }
        )

    async def _handle_plugins(self, request: web.Request) -> web.Response:
        eco_only = request.query.get("eco_only", "").lower() in ("1", "true", "yes")
        return web.json_response(
            {
                "ok": True,
                "plugins": self.hub.registry.list_plugins(
                    include_third_party=not eco_only
                ),
            }
        )

    async def _handle_get_config(self, request: web.Request) -> web.Response:
        name = request.match_info["name"]
        try:
            return web.json_response(
                {"ok": True, **self.hub.registry.get_plugin_config(name)}
            )
        except ValueError as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=400)

    async def _handle_save_config(self, request: web.Request) -> web.Response:
        name = request.match_info["name"]
        body = await self._read_json_dict(request)
        if body is None:
            return web.json_response(
                {"ok": False, "error": "无效 JSON 对象"}, status=400
            )
        try:
            res = self.hub.registry.save_plugin_config(name, body)
            return web.json_response(res)
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=400)

    async def _handle_plugin_action(self, request: web.Request) -> web.Response:
        name = request.match_info["name"]
        body = await self._read_json_dict(request)
        if body is None:
            return web.json_response(
                {"ok": False, "error": "无效 JSON 对象"}, status=400
            )
        action = str(body.get("action", "") or "").strip()
        raw_params = body.get("params")
        if raw_params is not None and not isinstance(raw_params, dict):
            return web.json_response(
                {"ok": False, "error": "params 必须为 JSON 对象"}, status=400
            )
        params = raw_params or {}
        if not action:
            return web.json_response(
                {"ok": False, "error": "缺少 action 参数"}, status=400
            )
        res = await self.hub.registry.call_action(name, action, params)
        return web.json_response(res, status=200 if res.get("ok") else 400)

    async def _handle_list_rules(self, request: web.Request) -> web.Response:
        return web.json_response({"ok": True, "rules": self.hub.bus.list_rules()})

    async def _handle_toggle_rule(self, request: web.Request) -> web.Response:
        rule_id = request.match_info["rule_id"]
        body = await self._read_json_dict(request)
        if body is None:
            return web.json_response(
                {"ok": False, "error": "无效 JSON 对象"}, status=400
            )
        res = self.hub.bus.toggle_rule(rule_id, bool(body.get("enabled", True)))
        if res is None:
            return web.json_response(
                {"ok": False, "error": f"未找到规则 {rule_id}"}, status=404
            )
        return web.json_response({"ok": True, "rule": res})

    async def _handle_add_custom_rule(self, request: web.Request) -> web.Response:
        body = await self._read_json_dict(request)
        if body is None:
            return web.json_response(
                {"ok": False, "error": "无效 JSON 对象"}, status=400
            )
        try:
            ev = str(body.get("event_type", "") or "").strip()
            tp = str(body.get("target_plugin", "") or "").strip()
            ta = str(body.get("target_action", "") or "").strip()
            raw_tpl = body.get("payload_template")
            if raw_tpl is not None and not isinstance(raw_tpl, dict):
                return web.json_response(
                    {"ok": False, "error": "payload_template 必须为 JSON 对象"},
                    status=400,
                )
            if not (ev and tp and ta):
                return web.json_response(
                    {
                        "ok": False,
                        "error": "event_type / target_plugin / target_action 不能为空",
                    },
                    status=400,
                )
            rule = self.hub.bus.add_custom_rule(
                name=str(body.get("name", "") or ""),
                source=str(body.get("source", "*") or "*"),
                event_type=ev,
                target_plugin=tp,
                target_action=ta,
                payload_template=raw_tpl or {},
                description=str(body.get("description", "") or ""),
            )
            return web.json_response({"ok": True, "rule": rule})
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=400)

    async def _handle_delete_custom_rule(self, request: web.Request) -> web.Response:
        rule_id = request.match_info["rule_id"]
        ok = self.hub.bus.delete_custom_rule(rule_id)
        return web.json_response({"ok": ok}, status=200 if ok else 404)

    async def _handle_events(self, request: web.Request) -> web.Response:
        try:
            limit = max(1, min(200, int(request.query.get("limit", "50"))))
        except ValueError:
            limit = 50
        ev_type = request.query.get("event_type", "")
        src = request.query.get("source", "")
        return web.json_response(
            {
                "ok": True,
                "events": self.hub.bus.recent_events(
                    limit=limit, event_type=ev_type, source=src
                ),
            }
        )

    async def _handle_emit_event(self, request: web.Request) -> web.Response:
        body = await self._read_json_dict(request)
        if body is None:
            return web.json_response(
                {"ok": False, "error": "无效 JSON 对象"}, status=400
            )
        source = str(
            body.get("source", "astrbot_plugin_hub") or "astrbot_plugin_hub"
        ).strip()
        event_type = str(body.get("event_type", "") or "").strip()
        raw_payload = body.get("payload")
        if raw_payload is not None and not isinstance(raw_payload, dict):
            return web.json_response(
                {"ok": False, "error": "payload 必须为 JSON 对象"}, status=400
            )
        payload = raw_payload or {}
        if not event_type:
            return web.json_response(
                {"ok": False, "error": "缺少 event_type"}, status=400
            )
        rec = await self.hub.bus.emit_async(
            source=source, event_type=event_type, payload=payload
        )
        return web.json_response({"ok": True, "event": rec})

    async def _handle_data_panel(self, request: web.Request) -> web.Response:
        panel = request.match_info["panel"]
        data = await self.hub.registry.get_aggregated_data(panel, bus=self.hub.bus)
        return web.json_response({"ok": "error" not in data, **data})

    async def _handle_adjust_points(self, request: web.Request) -> web.Response:
        body = await self._read_json_dict(request)
        if body is None:
            return web.json_response(
                {"ok": False, "error": "无效 JSON 对象"}, status=400
            )
        try:
            uid = str(body.get("user_id", "") or "").strip()
            delta = int(body.get("delta", 0))
            if not uid or delta == 0:
                return web.json_response(
                    {"ok": False, "error": "user_id 与非零 delta 必填"}, status=400
                )
            rec = self.hub.bus.add_eco_points(
                scope=str(body.get("scope", "global") or "global"),
                user_id=uid,
                nickname=str(body.get("nickname", uid) or uid),
                delta=delta,
                source="astrbot_plugin_hub",
                reason=str(body.get("reason", "面板手动调整") or "面板手动调整"),
            )
            return web.json_response({"ok": True, "record": rec})
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=400)
