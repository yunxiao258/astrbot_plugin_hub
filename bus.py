# -*- coding: utf-8 -*-
"""AstrBot 插件生态中枢事件总线、10 条内置自动化联动管线、自定义规则与生态统一积分账本。"""

from __future__ import annotations

import asyncio
import json
import os
import tempfile
import time
import uuid
from datetime import datetime
from typing import Any

HUB_BUS_KEY = "_astrbot_plugin_hub_bus"


def atomic_write_json(path: str, data: Any, do_fsync: bool = False) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".hub_tmp_", suffix=".json", dir=parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            if do_fsync:
                f.flush()
                os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except OSError:
            pass
        raise


def safe_read_json(path: str, default: Any) -> Any:
    if not os.path.isfile(path):
        return json.loads(json.dumps(default))
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            val = json.load(f)
        if type(val) is not type(default):
            return json.loads(json.dumps(default))
        return val
    except Exception:
        return json.loads(json.dumps(default))


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


BUILTIN_RULES: list[dict[str, Any]] = [
    {
        "id": "digest_todo_to_memo",
        "name": "摘要待办自动同步备忘录",
        "category": "efficiency",
        "sources": ["astrbot_plugin_chat_digest"],
        "targets": ["astrbot_plugin_memo"],
        "events": ["digest.todo_added"],
        "description": "在群聊记忆助手中新增待办时，自动同步写入同会话的备忘录（memo）",
        "default_enabled": True,
    },
    {
        "id": "digest_email_copy",
        "name": "群聊摘要自动抄送邮件",
        "category": "efficiency",
        "sources": ["astrbot_plugin_chat_digest"],
        "targets": ["astrbot_plugin_sendmail"],
        "events": ["digest.created"],
        "description": "生成群聊摘要后，若中枢已配置 digest_copy_email 则自动通过 sendmail 抄送邮箱",
        "default_enabled": True,
    },
    {
        "id": "antiflood_share_bots",
        "name": "防刷屏 Bot 名单全生态共享",
        "category": "guard",
        "sources": ["astrbot_plugin_anti_flood"],
        "targets": ["astrbot_plugin_group_stats", "astrbot_plugin_smart_silence", "astrbot_plugin_ignore_at"],
        "events": ["antiflood.bot_detected"],
        "description": "anti_flood 探测或标记新 Bot 后，自动同步至群统计（排除刷屏）、智能静默与忽略互@",
        "default_enabled": True,
    },
    {
        "id": "antispam_to_context",
        "name": "防扰拦截事件归档上下文审计",
        "category": "guard",
        "sources": ["astrbot_plugin_anti_flood", "astrbot_plugin_ignore_at", "astrbot_plugin_smart_silence"],
        "targets": ["astrbot_plugin_context_analyzer"],
        "events": ["antiflood.flood_blocked", "ignore_at.blocked", "smart_silence.silenced"],
        "description": "将防刷屏、忽略互@与智能静默拦截事件统一上报至 context_analyzer 事件审计日志",
        "default_enabled": True,
    },
    {
        "id": "ops_alerts_to_digest",
        "name": "运维关键事件自动归档群记忆",
        "category": "ops",
        "sources": ["astrbot_plugin_remote_task", "astrbot_plugin_status_sync", "astrbot_plugin_github_monitor"],
        "targets": ["astrbot_plugin_chat_digest"],
        "events": [
            "remote_task.completed",
            "remote_task.failed",
            "status_sync.machine_offline",
            "status_sync.status_changed",
            "github_monitor.release_found",
            "github_monitor.star_alert",
        ],
        "description": "远程任务完成/失败、机器离线/切换、GitHub 新 Release 与 Star 异动自动记入群记忆精华",
        "default_enabled": True,
    },
    {
        "id": "ops_alerts_to_mail",
        "name": "运维告警自动发送邮件通知",
        "category": "ops",
        "sources": ["astrbot_plugin_remote_task", "astrbot_plugin_status_sync", "astrbot_plugin_github_monitor"],
        "targets": ["astrbot_plugin_sendmail"],
        "events": ["remote_task.failed", "status_sync.machine_offline", "github_monitor.release_found", "github_monitor.star_alert"],
        "description": "触发运维高优先级告警时，若已配置 ops_alert_email 则自动通过 sendmail 发送邮件提醒",
        "default_enabled": True,
    },
    {
        "id": "points_economy_bridge",
        "name": "全生态统一积分账本互通",
        "category": "fun",
        "sources": ["astrbot_plugin_group_games", "astrbot_plugin_group_stats", "astrbot_plugin_fortune", "astrbot_plugin_gay"],
        "targets": ["astrbot_plugin_group_stats", "astrbot_plugin_hub"],
        "events": ["group_games.points_awarded", "group_stats.points_changed", "fortune.drawn", "gay.tested"],
        "description": "汇总小游戏胜利、群活跃发言、每日运势与互动积分至中枢统一生态积分榜，并同步至群统计",
        "default_enabled": True,
    },
    {
        "id": "lucky_fortune_music_bonus",
        "name": "大吉运势自动赠送点歌配额",
        "category": "fun",
        "sources": ["astrbot_plugin_fortune"],
        "targets": ["astrbot_plugin_music_custom"],
        "events": ["fortune.drawn"],
        "description": "群友抽到高分大吉运势（默认 >= 85 分）时，自动向点歌插件赠送额外当日点歌额度",
        "default_enabled": True,
    },
    {
        "id": "news_weather_to_digest",
        "name": "新闻与天气预警自动归档摘要",
        "category": "efficiency",
        "sources": ["astrbot_plugin_daily_news", "astrbot_plugin_weather"],
        "targets": ["astrbot_plugin_chat_digest"],
        "events": ["daily_news.pushed", "weather.pushed", "weather.alert"],
        "description": "每日新闻与天气预警推送后自动沉淀到会话记忆精华，便于后续全文检索回顾",
        "default_enabled": True,
    },
    {
        "id": "qa_translator_to_digest",
        "name": "问答与长文翻译知识沉淀",
        "category": "efficiency",
        "sources": ["astrbot_plugin_qa", "astrbot_plugin_translator"],
        "targets": ["astrbot_plugin_chat_digest"],
        "events": ["qa.added", "translator.translated"],
        "description": "新增自定义问答或长文翻译（>= 60 字）自动归档为群记忆精华条目",
        "default_enabled": True,
    },
]


class HubEventBus:
    """跨插件事件总线与自动化联动调度引擎。"""

    def __init__(
        self,
        data_dir: str,
        registry: Any,
        config_getter: Any,
        max_history: int = 500,
    ) -> None:
        self.data_dir = os.path.abspath(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        self.registry = registry
        self.config_getter = config_getter
        self.max_history = max(50, int(max_history))

        self.events_path = os.path.join(self.data_dir, "events.json")
        self.rules_path = os.path.join(self.data_dir, "rules.json")
        self.points_path = os.path.join(self.data_dir, "eco_points.json")

        self._events: list[dict[str, Any]] = []
        self._rule_state: dict[str, Any] = {"overrides": {}, "custom": [], "stats": {}}
        self._eco_points: dict[str, dict[str, dict[str, Any]]] = {}
        self._pending_tasks: set[asyncio.Task] = set()
        self._dispatch_depth = 0
        self._events_dirty = False
        self._last_events_flush = 0.0
        self._points_dirty = False
        self._last_points_flush = 0.0
        self.reload()

    def _flush_events(self, force: bool = False) -> None:
        now = time.monotonic()
        if not force and not self._events_dirty:
            return
        if force or (now - self._last_events_flush >= 5.0):
            atomic_write_json(self.events_path, self._events[-self.max_history :])
            self._events_dirty = False
            self._last_events_flush = now

    def _flush_points(self, force: bool = False) -> None:
        now = time.monotonic()
        if not force and not self._points_dirty:
            return
        if force or (now - self._last_points_flush >= 3.0):
            atomic_write_json(self.points_path, self._eco_points)
            self._points_dirty = False
            self._last_points_flush = now

    def reload(self) -> None:
        self._events = safe_read_json(self.events_path, [])
        rs = safe_read_json(self.rules_path, {"overrides": {}, "custom": [], "stats": {}})
        rs.setdefault("overrides", {})
        rs.setdefault("custom", [])
        rs.setdefault("stats", {})
        self._rule_state = rs
        self._eco_points = safe_read_json(self.points_path, {})

    def save_all(self) -> None:
        atomic_write_json(self.events_path, self._events[-self.max_history :], do_fsync=True)
        atomic_write_json(self.rules_path, self._rule_state, do_fsync=True)
        atomic_write_json(self.points_path, self._eco_points, do_fsync=True)
        self._events_dirty = False
        self._points_dirty = False

    # ==================== 规则管理 ====================

    def is_rule_enabled(self, rule_id: str) -> bool:
        cfg = self.config_getter() or {}
        if not self._bool(cfg.get("auto_linkage_enabled", True), True):
            return False
        overrides = self._rule_state.get("overrides", {})
        if rule_id in overrides:
            return bool(overrides[rule_id])
        for r in BUILTIN_RULES:
            if r["id"] == rule_id:
                return bool(r.get("default_enabled", True))
        for cr in self._rule_state.get("custom", []):
            if cr.get("id") == rule_id:
                return bool(cr.get("enabled", True))
        return False

    def list_rules(self) -> list[dict[str, Any]]:
        stats = self._rule_state.get("stats", {})
        overrides = self._rule_state.get("overrides", {})
        out: list[dict[str, Any]] = []
        for r in BUILTIN_RULES:
            rid = r["id"]
            enabled = bool(overrides[rid]) if rid in overrides else bool(r.get("default_enabled", True))
            st = stats.get(rid, {})
            out.append({
                **r,
                "builtin": True,
                "enabled": enabled,
                "triggered_count": int(st.get("count", 0)),
                "last_triggered": str(st.get("last_at", "")),
                "last_status": str(st.get("last_status", "")),
            })
        for cr in self._rule_state.get("custom", []):
            rid = str(cr.get("id", ""))
            st = stats.get(rid, {})
            out.append({
                **cr,
                "builtin": False,
                "enabled": bool(cr.get("enabled", True)),
                "triggered_count": int(st.get("count", 0)),
                "last_triggered": str(st.get("last_at", "")),
                "last_status": str(st.get("last_status", "")),
            })
        return out

    def toggle_rule(self, rule_id: str, enabled: bool) -> dict[str, Any] | None:
        for r in BUILTIN_RULES:
            if r["id"] == rule_id:
                self._rule_state.setdefault("overrides", {})[rule_id] = bool(enabled)
                atomic_write_json(self.rules_path, self._rule_state)
                return {**r, "builtin": True, "enabled": bool(enabled)}
        for cr in self._rule_state.get("custom", []):
            if cr.get("id") == rule_id:
                cr["enabled"] = bool(enabled)
                atomic_write_json(self.rules_path, self._rule_state)
                return {**cr, "builtin": False}
        return None

    def add_custom_rule(
        self,
        name: str,
        source: str,
        event_type: str,
        target_plugin: str,
        target_action: str,
        payload_template: dict[str, Any] | None = None,
        description: str = "",
    ) -> dict[str, Any]:
        rule = {
            "id": f"custom_{uuid.uuid4().hex[:8]}",
            "name": (name or f"{source} -> {target_plugin}").strip()[:80],
            "category": "custom",
            "sources": [source.strip()],
            "targets": [target_plugin.strip()],
            "events": [event_type.strip()],
            "target_plugin": target_plugin.strip(),
            "target_action": target_action.strip(),
            "payload_template": dict(payload_template or {}),
            "description": (description or f"监听 {event_type} 自动触发 {target_plugin}.{target_action}").strip()[:200],
            "enabled": True,
            "created_at": _now_iso(),
        }
        self._rule_state.setdefault("custom", []).append(rule)
        atomic_write_json(self.rules_path, self._rule_state)
        return rule

    def delete_custom_rule(self, rule_id: str) -> bool:
        lst = self._rule_state.get("custom", [])
        before = len(lst)
        self._rule_state["custom"] = [x for x in lst if x.get("id") != rule_id]
        if len(self._rule_state["custom"]) != before:
            atomic_write_json(self.rules_path, self._rule_state)
            return True
        return False

    def _record_rule_hit(self, rule_id: str, ok: bool) -> None:
        stats = self._rule_state.setdefault("stats", {})
        entry = stats.setdefault(rule_id, {"count": 0, "last_at": "", "last_status": ""})
        entry["count"] = int(entry.get("count", 0)) + 1
        entry["last_at"] = _now_iso()
        entry["last_status"] = "ok" if ok else "error"
        atomic_write_json(self.rules_path, self._rule_state)

    # ==================== 统一生态积分账本 ====================

    def add_eco_points(
        self,
        scope: str,
        user_id: str,
        nickname: str,
        delta: int,
        source: str,
        reason: str = "",
    ) -> dict[str, Any]:
        sc = str(scope or "global")
        uid = str(user_id or "").strip()
        if not uid or delta == 0:
            return {}
        bucket = self._eco_points.setdefault(sc, {})
        rec = bucket.setdefault(
            uid,
            {"user_id": uid, "nickname": nickname or uid, "total": 0, "sources": {}, "updated_at": ""},
        )
        if nickname:
            rec["nickname"] = str(nickname)[:40]
        rec["total"] = int(rec.get("total", 0)) + int(delta)
        srcs = rec.setdefault("sources", {})
        srcs[source] = int(srcs.get(source, 0)) + int(delta)
        rec["updated_at"] = _now_iso()
        if reason:
            rec["last_reason"] = str(reason)[:80]
        self._points_dirty = True
        self._flush_points(force=False)
        return dict(rec)

    def get_eco_leaderboard(self, scope: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        if scope and scope in self._eco_points:
            items = list(self._eco_points[scope].values())
        else:
            merged: dict[str, dict[str, Any]] = {}
            for sc_data in self._eco_points.values():
                if not isinstance(sc_data, dict):
                    continue
                for uid, rec in sc_data.items():
                    m = merged.setdefault(
                        uid,
                        {
                            "user_id": uid,
                            "nickname": rec.get("nickname", uid),
                            "total": 0,
                            "sources": {},
                            "updated_at": rec.get("updated_at", ""),
                        },
                    )
                    m["total"] += int(rec.get("total", 0))
                    if rec.get("nickname"):
                        m["nickname"] = rec["nickname"]
                    for sk, sv in (rec.get("sources") or {}).items():
                        m["sources"][sk] = int(m["sources"].get(sk, 0)) + int(sv)
            items = list(merged.values())
        items.sort(key=lambda x: (-int(x.get("total", 0)), str(x.get("user_id", ""))))
        return items[: max(1, limit)]

    def count_eco_users(self) -> int:
        users: set[str] = set()
        for sc_data in self._eco_points.values():
            if isinstance(sc_data, dict):
                users.update(sc_data.keys())
        return len(users)

    # ==================== 事件上报与联动调度 ====================

    def emit(
        self,
        source: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """同步安全入口：记录事件；若存在运行中的事件循环则异步调度联动规则。"""
        data = dict(payload or {})
        if data.get("_hub_origin") or self._dispatch_depth >= 2:
            # 防止联动二次重入造成循环风暴
            return {"skipped": True, "reason": "reentrant"}

        record = {
            "id": uuid.uuid4().hex[:10],
            "ts": _now_iso(),
            "source": str(source),
            "event_type": str(event_type),
            "payload": data,
            "dispatched": [],
        }
        self._events.append(record)
        if len(self._events) > self.max_history:
            self._events = self._events[-self.max_history :]
        self._events_dirty = True
        self._flush_events(force=False)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return record

        task = loop.create_task(self._dispatch_record(record))
        self._pending_tasks.add(task)
        task.add_done_callback(self._pending_tasks.discard)
        return record

    async def emit_async(
        self,
        source: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """异步等待入口：记录事件并同步等待全部匹配联动规则执行完成。"""
        data = dict(payload or {})
        if data.get("_hub_origin") or self._dispatch_depth >= 2:
            return {"skipped": True, "reason": "reentrant"}

        record = {
            "id": uuid.uuid4().hex[:10],
            "ts": _now_iso(),
            "source": str(source),
            "event_type": str(event_type),
            "payload": data,
            "dispatched": [],
        }
        self._events.append(record)
        if len(self._events) > self.max_history:
            self._events = self._events[-self.max_history :]
        self._events_dirty = True
        await self._dispatch_record(record)
        return record

    async def drain(self) -> None:
        if self._pending_tasks:
            await asyncio.gather(*list(self._pending_tasks), return_exceptions=True)
        self._flush_events(force=True)
        self._flush_points(force=True)

    def recent_events(self, limit: int = 50, event_type: str = "", source: str = "") -> list[dict[str, Any]]:
        items = list(self._events)
        if event_type:
            items = [e for e in items if event_type.lower() in str(e.get("event_type", "")).lower()]
        if source:
            items = [e for e in items if source.lower() in str(e.get("source", "")).lower()]
        return list(reversed(items[-max(1, limit) :]))

    async def _call_target(
        self,
        record: dict[str, Any],
        rule_id: str,
        plugin: str,
        action: str,
        params: dict[str, Any],
    ) -> bool:
        t0 = time.monotonic()
        safe_params = dict(params)
        safe_params["_hub_origin"] = record["id"]
        res = await self.registry.call_action(plugin, action, safe_params)
        ms = int((time.monotonic() - t0) * 1000)
        ok = bool(res.get("ok"))
        record["dispatched"].append({
            "rule": rule_id,
            "target": plugin,
            "action": action,
            "ok": ok,
            "ms": ms,
            "error": str(res.get("error", ""))[:160] if not ok else "",
        })
        self._record_rule_hit(rule_id, ok)
        return ok

    @staticmethod
    def _bool(val: Any, default: bool) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return bool(val)
        s = str(val or "").strip().lower()
        if s in ("true", "1", "yes", "on"):
            return True
        if s in ("false", "0", "no", "off", ""):
            return False
        return default

    @staticmethod
    def _int(val: Any, default: int) -> int:
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    async def _dispatch_record(self, record: dict[str, Any]) -> None:
        cfg = self.config_getter() or {}
        if not self._bool(cfg.get("auto_linkage_enabled", True), True):
            return

        self._dispatch_depth += 1
        try:
            ev = record["event_type"]
            src = record["source"]
            p = record["payload"]

            # 1. chat_digest 待办 -> memo 备忘录
            if ev == "digest.todo_added" and self.is_rule_enabled("digest_todo_to_memo"):
                umo = str(p.get("umo", ""))
                title = str(p.get("title", "")).strip()
                assignee = str(p.get("assignee", "")).strip()
                if umo and title and self.registry.has_live_plugin("astrbot_plugin_memo"):
                    content = f"[群待办] {title}" + (f" (@{assignee})" if assignee else "")
                    await self._call_target(record, "digest_todo_to_memo", "astrbot_plugin_memo", "add_memo", {"umo": umo, "content": content})

            # 2. chat_digest 摘要生成 -> sendmail 邮件抄送（仅配置邮箱时触发）
            if ev == "digest.created" and self.is_rule_enabled("digest_email_copy"):
                email_to = str(cfg.get("digest_copy_email", "") or "").strip()
                if email_to and self.registry.has_live_plugin("astrbot_plugin_sendmail"):
                    subject = f"[AstrBot 群聊摘要] {p.get('date', '')} ({p.get('message_count', 0)} 条消息)"
                    body = str(p.get("text") or p.get("summary") or "")
                    if body:
                        await self._call_target(
                            record,
                            "digest_email_copy",
                            "astrbot_plugin_sendmail",
                            "send_mail",
                            {"to": email_to, "subject": subject, "body": body},
                        )

            # 3. anti_flood 新识别/标记 Bot -> 同步至 group_stats / smart_silence / ignore_at
            if ev == "antiflood.bot_detected" and self.is_rule_enabled("antiflood_share_bots"):
                bot_id = str(p.get("bot_id", "")).strip()
                if bot_id:
                    for target_plug, act in (
                        ("astrbot_plugin_group_stats", "add_ignored_bot"),
                        ("astrbot_plugin_smart_silence", "sync_bot_ids"),
                        ("astrbot_plugin_ignore_at", "sync_bot_ids"),
                    ):
                        if self.registry.has_live_plugin(target_plug):
                            await self._call_target(
                                record,
                                "antiflood_share_bots",
                                target_plug,
                                act,
                                {"bot_ids": [bot_id], "bot_id": bot_id},
                            )

            # 4. 防扰拦截事件 -> context_analyzer 审计事件日志
            if ev in ("antiflood.flood_blocked", "ignore_at.blocked", "smart_silence.silenced") and self.is_rule_enabled("antispam_to_context"):
                if self.registry.has_live_plugin("astrbot_plugin_context_analyzer"):
                    await self._call_target(
                        record,
                        "antispam_to_context",
                        "astrbot_plugin_context_analyzer",
                        "record_external_event",
                        {"event_type": ev, "plugin": src, "details": p},
                    )

            # 5. 运维事件 -> chat_digest 精华归档
            if ev in (
                "remote_task.completed",
                "remote_task.failed",
                "status_sync.machine_offline",
                "status_sync.status_changed",
                "github_monitor.release_found",
                "github_monitor.star_alert",
            ) and self.is_rule_enabled("ops_alerts_to_digest"):
                target_umo = str(cfg.get("ops_archive_umo", "") or p.get("umo", "")).strip()
                summary = str(p.get("summary") or p.get("title") or ev).strip()
                if target_umo and summary and self.registry.has_live_plugin("astrbot_plugin_chat_digest"):
                    await self._call_target(
                        record,
                        "ops_alerts_to_digest",
                        "astrbot_plugin_chat_digest",
                        "add_highlight",
                        {"umo": target_umo, "text": f"[运维/{ev}] {summary}", "added_by": src, "tags": ["运维联动"]},
                    )

            # 6. 运维高优告警 -> sendmail 邮件告警
            if ev in ("remote_task.failed", "status_sync.machine_offline", "github_monitor.release_found", "github_monitor.star_alert") and self.is_rule_enabled("ops_alerts_to_mail"):
                alert_to = str(cfg.get("ops_alert_email", "") or "").strip()
                if alert_to and self.registry.has_live_plugin("astrbot_plugin_sendmail"):
                    summary = str(p.get("summary") or p.get("title") or ev)
                    await self._call_target(
                        record,
                        "ops_alerts_to_mail",
                        "astrbot_plugin_sendmail",
                        "send_mail",
                        {"to": alert_to, "subject": f"[AstrBot 运维告警] {ev}", "body": summary},
                    )

            # 7. 跨插件统一生态积分互通
            if ev in ("group_games.points_awarded", "group_stats.points_changed", "fortune.drawn", "gay.tested") and self.is_rule_enabled("points_economy_bridge"):
                uid = str(p.get("user_id", "")).strip()
                nick = str(p.get("nickname", "") or uid)
                scope = str(p.get("group_id") or p.get("umo") or "global")
                delta = 0
                reason = ev
                if ev == "group_games.points_awarded":
                    delta = self._int(p.get("delta", 0), 0)
                    reason = f"小游戏:{p.get('game', '')}"
                elif ev == "group_stats.points_changed":
                    delta = self._int(p.get("delta", 0), 0)
                    reason = "群活跃发言"
                elif ev == "fortune.drawn":
                    score = self._int(p.get("score", 0), 0)
                    delta = 5 if score >= 85 else (2 if score >= 60 else 1)
                    reason = f"每日运势({score}分)"
                elif ev == "gay.tested":
                    delta = 1
                    reason = "群聊互动"

                if uid and delta > 0:
                    self.add_eco_points(scope, uid, nick, delta, src, reason)
                    record["dispatched"].append({"rule": "points_economy_bridge", "target": "astrbot_plugin_hub", "action": "add_eco_points", "ok": True, "ms": 0, "error": ""})
                    self._record_rule_hit("points_economy_bridge", True)
                    # 来自游戏/运势/互动的加分同步反哺到 group_stats 积分榜
                    if src != "astrbot_plugin_group_stats" and p.get("group_id") and self.registry.has_live_plugin("astrbot_plugin_group_stats"):
                        await self._call_target(
                            record,
                            "points_economy_bridge",
                            "astrbot_plugin_group_stats",
                            "add_points",
                            {"group_id": str(p["group_id"]), "user_id": uid, "nickname": nick, "delta": delta},
                        )

            # 8. 大吉运势 -> music_custom 赠送点歌配额
            if ev == "fortune.drawn" and self.is_rule_enabled("lucky_fortune_music_bonus"):
                score = self._int(p.get("score", 0), 0)
                threshold = self._int(cfg.get("fortune_bonus_threshold", 85), 85)
                bonus = max(1, self._int(cfg.get("fortune_bonus_quota", 2), 2))
                uid = str(p.get("user_id", "")).strip()
                if uid and score >= threshold and self.registry.has_live_plugin("astrbot_plugin_music_custom"):
                    await self._call_target(
                        record,
                        "lucky_fortune_music_bonus",
                        "astrbot_plugin_music_custom",
                        "grant_bonus_quota",
                        {"user_id": uid, "bonus": bonus, "reason": f"大吉运势({score}分)"},
                    )

            # 9. 新闻 / 天气预警 -> chat_digest 精华归档
            if ev in ("daily_news.pushed", "weather.pushed", "weather.alert") and self.is_rule_enabled("news_weather_to_digest"):
                umo = str(p.get("umo", "")).strip()
                summary = str(p.get("summary", "")).strip()
                if umo and summary and self.registry.has_live_plugin("astrbot_plugin_chat_digest"):
                    tag = "每日新闻" if ev == "daily_news.pushed" else "天气播报"
                    await self._call_target(
                        record,
                        "news_weather_to_digest",
                        "astrbot_plugin_chat_digest",
                        "add_highlight",
                        {"umo": umo, "text": f"[{tag}] {summary[:260]}", "added_by": src, "tags": [tag]},
                    )

            # 10. 问答 / 长文翻译 -> chat_digest 知识沉淀
            if ev in ("qa.added", "translator.translated") and self.is_rule_enabled("qa_translator_to_digest"):
                umo = str(p.get("umo", "")).strip()
                if umo and self.registry.has_live_plugin("astrbot_plugin_chat_digest"):
                    if ev == "qa.added":
                        q = str(p.get("question", "")).strip()
                        a = str(p.get("answer", "")).strip()
                        if q and a:
                            await self._call_target(
                                record,
                                "qa_translator_to_digest",
                                "astrbot_plugin_chat_digest",
                                "add_highlight",
                                {"umo": umo, "text": f"[问答] Q: {q} → A: {a[:180]}", "added_by": src, "tags": ["问答库"]},
                            )
                    elif ev == "translator.translated":
                        out_txt = str(p.get("translated", "")).strip()
                        if len(out_txt) >= 60:
                            await self._call_target(
                                record,
                                "qa_translator_to_digest",
                                "astrbot_plugin_chat_digest",
                                "add_highlight",
                                {"umo": umo, "text": f"[翻译摘录] {out_txt[:220]}", "added_by": src, "tags": ["翻译"]},
                            )

            # 11. 自定义联动规则匹配
            for cr in list(self._rule_state.get("custom", [])):
                rid = str(cr.get("id", ""))
                if not cr.get("enabled", True):
                    continue
                ev_match = ev in (cr.get("events") or []) or "*" in (cr.get("events") or [])
                src_match = src in (cr.get("sources") or []) or "*" in (cr.get("sources") or [])
                if not (ev_match and src_match):
                    continue
                t_plug = str(cr.get("target_plugin", ""))
                t_act = str(cr.get("target_action", ""))
                if t_plug and t_act and self.registry.has_live_plugin(t_plug):
                    merged_params = dict(p)
                    merged_params.update(cr.get("payload_template") or {})
                    await self._call_target(record, rid, t_plug, t_act, merged_params)
        finally:
            self._dispatch_depth = max(0, self._dispatch_depth - 1)
            self._events_dirty = True
            self._flush_events(force=False)
