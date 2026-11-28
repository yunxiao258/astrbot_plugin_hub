# -*- coding: utf-8 -*-
"""AstrBot 插件生态中枢与端口管理面板主入口（astrbot_plugin_hub）。"""

from __future__ import annotations

import importlib
import json
import os
import re
import sys
from typing import Any

from astrbot.api import AstrBotConfig, logger
from astrbot.api.all import MessageChain
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.message_components import Plain
from astrbot.api.star import Context, Star, register

try:
    from astrbot.core.utils.astrbot_path import get_astrbot_data_path
except Exception:  # pragma: no cover
    get_astrbot_data_path = None

from . import web_server as _web_server_mod
from . import web_ui as _web_ui_mod
from .bus import HUB_BUS_KEY, HubEventBus
from .registry import PluginRegistry

try:
    importlib.reload(_web_ui_mod)
    importlib.reload(_web_server_mod)
except Exception:  # pragma: no cover
    pass

HubWebServer = _web_server_mod.HubWebServer

PLUGIN_NAME = "astrbot_plugin_hub"
PLUGIN_AUTHOR = "云晓"
PLUGIN_DESC = (
    "AstrBot 全插件联动中枢与 Web 管理面板：提供跨插件事件总线、13 条开箱即用自动化联动管线、"
    "生态统一积分榜、在线配置编辑器与端口可视化管理台（默认 127.0.0.1:8686）"
)
PLUGIN_VERSION = "1.3.0"
PLUGIN_REPO = "https://github.com/yunxiao258/astrbot_plugin_hub"

_CMD_RE = re.compile(r"^[\\/／]?\s*(?:中枢|hub|面板|联动)\b\s*(.*)$", re.IGNORECASE | re.S)


def _split_csv(raw: str) -> set[str]:
    return {x.strip() for x in (raw or "").split(",") if x.strip()}


@register(PLUGIN_NAME, PLUGIN_AUTHOR, PLUGIN_DESC, PLUGIN_VERSION, repo=PLUGIN_REPO)
class PluginHubStar(Star):
    """AstrBot 全插件联动中枢与 Web 可视化管理台。"""

    HUB_PROTOCOL_VERSION = 1

    def __init__(
        self,
        context: Context,
        config: AstrBotConfig | None = None,
        data_dir: str | None = None,
        plugins_dir: str | None = None,
    ) -> None:
        super().__init__(context)
        self.config: dict[str, Any] = config if isinstance(config, dict) else {}
        base_data = get_astrbot_data_path() if callable(get_astrbot_data_path) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.astrbot_data_dir = os.path.abspath(base_data)
        self.data_dir = os.path.abspath(data_dir) if data_dir else os.path.join(self.astrbot_data_dir, "plugin_data", PLUGIN_NAME)
        os.makedirs(self.data_dir, exist_ok=True)
        self.plugins_dir = os.path.abspath(plugins_dir) if plugins_dir else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.registry = PluginRegistry(self.context, self.plugins_dir, self.astrbot_data_dir)
        self.registry.register_local_instance(PLUGIN_NAME, self)
        self.bus = HubEventBus(
            data_dir=self.data_dir,
            registry=self.registry,
            config_getter=lambda: self.config,
            max_history=self.cfg_int("max_event_history", 500, min_val=50),
        )
        self.web_server: HubWebServer | None = None
        logger.info(f"【{PLUGIN_NAME}】生态中枢初始化完成，数据目录: {self.data_dir}")

    # ==================== 配置读取辅助 ====================

    def cfg_bool(self, key: str, default: bool) -> bool:
        if key not in self.config or self.config.get(key) is None:
            return default
        val = self.config.get(key)
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return bool(val)
        s = str(val).strip().lower()
        if s in ("true", "1", "yes", "on"):
            return True
        if s in ("false", "0", "no", "off", ""):
            return False
        return default

    def cfg_int(self, key: str, default: int, min_val: int | None = None) -> int:
        raw = self.config.get(key, default)
        if raw is None or isinstance(raw, bool):
            val = default
        else:
            try:
                val = int(raw)
            except (TypeError, ValueError):
                val = default
        if min_val is not None and val < min_val:
            return min_val
        return val

    def cfg_str(self, key: str, default: str = "") -> str:
        raw = self.config.get(key)
        if raw is None:
            return default
        return str(raw).strip()

    # ==================== 异步生命周期 ====================

    async def initialize(self) -> None:
        """挂载全局事件总线并按配置启动端口 Web 管理面板。"""
        sys.modules[HUB_BUS_KEY] = self.bus  # type: ignore[assignment]
        if self.cfg_bool("web_enabled", True):
            host = self.cfg_str("web_host", "127.0.0.1") or "127.0.0.1"
            port = self.cfg_int("web_port", 8686, min_val=0)
            token = self.cfg_str("web_token", "")
            req_local = self.cfg_bool("require_auth_on_localhost", False)
            self.web_server = HubWebServer(
                hub=self,
                host=host,
                port=port,
                token=token,
                require_auth_on_localhost=req_local,
                token_file=os.path.join(self.data_dir, "hub_token.txt"),
            )
            try:
                bound = await self.web_server.start()
                auth_tip = "本机免登" if (self.web_server.is_loopback_bind() and not req_local) else "Token 鉴权已启用"
                logger.info(f"【{PLUGIN_NAME}】Web 管理面板已启动：http://{host}:{bound}（{auth_tip}）")
            except Exception as exc:
                logger.error(f"【{PLUGIN_NAME}】Web 管理面板启动失败 ({host}:{port}): {exc}")
                self.web_server = None

    async def terminate(self) -> None:
        """卸载清理：关闭 Web 服务、排空事件总线、移除全局总线注册并落盘。"""
        if self.web_server is not None:
            await self.web_server.stop()
            self.web_server = None
        await self.bus.drain()
        self.bus.save_all()
        if sys.modules.get(HUB_BUS_KEY) is self.bus:
            sys.modules.pop(HUB_BUS_KEY, None)
        logger.info(f"【{PLUGIN_NAME}】生态中枢已停止并保存数据")

    # ==================== 标准协议自述 ====================

    def hub_status(self) -> dict[str, Any]:
        rules = self.bus.list_rules()
        return {
            "version": PLUGIN_VERSION,
            "status": "online",
            "metrics": {
                "规则启用": f"{sum(1 for r in rules if r['enabled'])}/{len(rules)}",
                "事件数": len(self.bus._events),
                "生态积分人": self.bus.count_eco_users(),
                "面板端口": self.web_server.bound_port if self.web_server else "关闭",
            },
            "actions": ["get_leaderboard", "list_rules", "toggle_rule", "emit_event"],
        }

    async def hub_action(self, action: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        p = params or {}
        if action == "get_leaderboard":
            return {"ok": True, "data": self.bus.get_eco_leaderboard(scope=p.get("scope"), limit=int(p.get("limit", 20)))}
        if action == "list_rules":
            return {"ok": True, "data": self.bus.list_rules()}
        if action == "toggle_rule":
            res = self.bus.toggle_rule(str(p.get("rule_id", "")), bool(p.get("enabled", True)))
            return {"ok": res is not None, "data": res, "error": "" if res else "未找到规则"}
        if action == "emit_event":
            rec = await self.bus.emit_async(str(p.get("source", PLUGIN_NAME)), str(p.get("event_type", "")), p.get("payload") or {})
            return {"ok": True, "data": rec}
        return {"ok": False, "error": f"不支持的动作：{action}"}

    # ==================== 权限与回复辅助 ====================

    def _is_admin(self, event: Any) -> bool:
        try:
            if callable(getattr(event, "is_admin", None)) and event.is_admin():
                return True
        except Exception:
            pass
        umo = str(getattr(event, "unified_msg_origin", "") or "")
        uid = ""
        try:
            uid = str(event.get_sender_id() or "")
        except Exception:
            pass
        if umo and umo in _split_csv(self.cfg_str("admin_umos", "")):
            return True
        if uid and uid in _split_csv(self.cfg_str("admin_user_ids", "")):
            return True
        return False

    @staticmethod
    def _reply(event: Any, text: str) -> Any:
        if hasattr(event, "plain_result"):
            return event.plain_result(text)
        return MessageChain([Plain(text)])

    # ==================== 统一指令入口：/中枢（别名 /hub、/面板、/联动） ====================

    @filter.command("中枢", alias={"hub", "面板", "联动"}, priority=200)
    async def hub_command(self, event: AstrMessageEvent) -> Any:
        raw = str(getattr(event, "message_str", "") or "").strip()
        m = _CMD_RE.match(raw)
        rest = (m.group(1) if m else raw).strip()
        if not rest:
            return self._reply(event, self._status_text())

        parts = rest.split(None, 1)
        sub = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if sub in ("帮助", "help", "-h", "--help"):
            return self._reply(event, self._help_text())
        if sub in ("状态", "status"):
            return self._reply(event, self._status_text())
        if sub in ("面板", "panel", "web"):
            return self._reply(event, self._panel_text(event))
        if sub in ("联动", "规则", "rules"):
            return self._reply(event, self._handle_rules_cmd(event, arg))
        if sub in ("事件", "events", "log"):
            limit = int(arg) if arg.isdigit() else 10
            return self._reply(event, self._events_text(max(1, min(30, limit))))
        if sub in ("积分", "排行", "points", "rank"):
            return self._reply(event, self._points_text())
        if sub in ("触发", "action", "call"):
            return self._reply(event, await self._handle_trigger_cmd(event, arg))
        return self._reply(event, f"❌ 未知子指令「{parts[0]}」，发送 `/中枢 帮助` 查看用法。")

    def _status_text(self) -> str:
        plugins = self.registry.list_plugins(include_third_party=False)
        online = sum(1 for p in plugins if p["online"])
        linked = sum(1 for p in plugins if p["protocol_version"] >= 1)
        rules = self.bus.list_rules()
        enabled_rules = sum(1 for r in rules if r["enabled"])
        panel_url = self.web_server.url if self.web_server else "未启动"
        return (
            f"🎛️ AstrBot 插件生态中枢 v{PLUGIN_VERSION}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🧩 生态插件：在线 {online} / 已发现 {len(plugins)}（标准协议接入 {linked}）\n"
            f"⚡ 联动管线：启用 {enabled_rules} / 总计 {len(rules)}（总开关：{'开' if self.cfg_bool('auto_linkage_enabled', True) else '关'}）\n"
            f"📡 事件总线：累计 {len(self.bus._events)} 条事件\n"
            f"🏆 统一积分：{self.bus.count_eco_users()} 位活跃用户\n"
            f"🌐 管理面板：{panel_url}"
        )

    def _panel_text(self, event: Any) -> str:
        if self.web_server is None:
            return "⏸️ Web 管理面板当前未启动（请在配置中开启 `web_enabled=true` 后重载）。"
        req = not self.web_server.is_loopback_bind() or self.web_server.require_auth_on_localhost
        lines = [
            "🌐 AstrBot 插件生态 Web 管理面板",
            f"地址：{self.web_server.url}",
            f"监听：{self.web_server.host}:{self.web_server.bound_port}",
            f"鉴权：{'🔐 Token 强制登录' if req else '🔓 本机免登（外网暴露自动切换强制 Token）'}",
        ]
        if req and self._is_admin(event):
            is_private = "FriendMessage" in str(getattr(event, "unified_msg_origin", ""))
            if is_private:
                lines.append(f"管理员 Token：`{self.web_server.token}`")
            else:
                lines.append("💡 为防群聊泄露令牌，请私聊机器人发送 `/中枢 面板` 或查看 `data/hub_token.txt` 获取 Token。")
        return "\n".join(lines)

    def _handle_rules_cmd(self, event: Any, arg: str) -> str:
        if not arg or arg.lower() in ("列表", "list"):
            rules = self.bus.list_rules()
            lines = [f"⚡ 自动化联动管线（共 {len(rules)} 条）："]
            for r in rules:
                st = "✅" if r["enabled"] else "⏸️"
                lines.append(f"{st} `{r['id']}` — {r['name']}（已触发 {r['triggered_count']} 次）")
            lines.append("\n管理员可用 `/中枢 联动 开启|关闭 <规则ID>` 切换。")
            return "\n".join(lines)
        parts = arg.split(None, 1)
        act = parts[0].lower()
        rid = parts[1].strip() if len(parts) > 1 else ""
        if act in ("开启", "开", "on", "enable", "关闭", "关", "off", "disable"):
            if not self._is_admin(event):
                return "⛔ 切换联动规则开关仅限管理员操作。"
            if not rid:
                return "❌ 用法：`/中枢 联动 开启|关闭 <规则ID>`"
            en = act in ("开启", "开", "on", "enable")
            res = self.bus.toggle_rule(rid, en)
            if not res:
                return f"❌ 未找到规则 ID：{rid}"
            return f"{'✅ 已开启' if en else '⏸️ 已关闭'}联动规则：{res['name']} (`{rid}`)"
        return "❌ 用法：`/中枢 联动 [列表 | 开启 <规则ID> | 关闭 <规则ID>]`"

    def _events_text(self, limit: int) -> str:
        evs = self.bus.recent_events(limit=limit)
        if not evs:
            return "📡 暂无跨插件联动事件记录。"
        lines = [f"📡 最近 {len(evs)} 条跨插件联动事件："]
        for e in evs:
            dispatched = len(e.get("dispatched") or [])
            ok_cnt = sum(1 for d in (e.get("dispatched") or []) if d.get("ok"))
            src = str(e.get("source", "")).replace("astrbot_plugin_", "")
            lines.append(f"• [{str(e.get('ts',''))[5:16]}] {src} → `{e.get('event_type')}` (联动 {ok_cnt}/{dispatched})")
        return "\n".join(lines)

    def _points_text(self) -> str:
        lb = self.bus.get_eco_leaderboard(limit=10)
        if not lb:
            return "🏆 生态统一积分榜暂无记录（参与群聊小游戏、发言统计、每日运势或娱乐互动即可自动累计）。"
        lines = ["🏆 AstrBot 全生态统一积分榜 Top 10："]
        for i, u in enumerate(lb, 1):
            src_brief = ", ".join(f"{k.replace('astrbot_plugin_','')}:{v}" for k, v in (u.get("sources") or {}).items())
            lines.append(f"{i}. {u.get('nickname', u.get('user_id'))} — {u.get('total', 0)} 分（{src_brief}）")
        return "\n".join(lines)

    async def _handle_trigger_cmd(self, event: Any, arg: str) -> str:
        if not self._is_admin(event):
            return "⛔ 手动触发跨插件动作仅限管理员操作。"
        parts = arg.split(None, 2)
        if len(parts) < 2:
            return "❌ 用法：`/中枢 触发 <插件名> <动作> [JSON参数]`"
        plugin, action = parts[0], parts[1]
        if not plugin.startswith("astrbot_plugin_"):
            plugin = f"astrbot_plugin_{plugin}"
        params: dict[str, Any] = {}
        if len(parts) == 3:
            try:
                params = json.loads(parts[2])
            except Exception as exc:
                return f"❌ JSON 参数解析失败：{exc}"
        res = await self.registry.call_action(plugin, action, params)
        if res.get("ok"):
            return f"✅ 已执行 `{plugin}.{action}`：\n{json.dumps(res.get('data'), ensure_ascii=False)[:600]}"
        return f"❌ 执行失败：{res.get('error', '未知错误')}"

    @staticmethod
    def _help_text() -> str:
        return (
            f"📖 AstrBot 插件生态中枢 v{PLUGIN_VERSION}（别名 /hub、/面板、/联动）\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "• `/中枢` 或 `/中枢 状态`：查看生态插件在线数、联动规则与面板状态\n"
            "• `/中枢 面板`：查看端口 Web 管理面板地址与鉴权说明\n"
            "• `/中枢 联动 [列表 | 开启 <ID> | 关闭 <ID>]`：管理 10 条内置与自定义自动联动规则\n"
            "• `/中枢 事件 [N]`：查看最近跨插件联动事件流\n"
            "• `/中枢 积分`：查看跨游戏/统计/运势/互动的统一生态积分榜\n"
            "• `/中枢 触发 <插件> <动作> [JSON]`：手动调用任意生态插件动作（管理员）"
        )
