# -*- coding: utf-8 -*-
"""AstrBot 全生态插件发现注册表、统一动作调用、跨插件数据聚合与在线配置编辑器引擎。"""

from __future__ import annotations

import inspect
import os
import re
from typing import Any

import yaml

from .bus import atomic_write_json, safe_read_json

SECRET_FIELD_RE = re.compile(
    r"(password|passwd|token|secret|api_key|apikey|auth_code|cookie|private_key|credential)",
    re.IGNORECASE,
)
SECRET_MASK = "******"
_SAFE_PLUGIN_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")


def validate_plugin_name(plugin_name: str) -> str:
    """严格校验插件目录名，防止路径穿越（../、斜杠、空名等）。"""
    name = (plugin_name or "").strip()
    if not name or ".." in name or "/" in name or "\\" in name or not _SAFE_PLUGIN_NAME_RE.match(name):
        raise ValueError(f"非法插件名：{plugin_name!r}")
    return name

# 全部 21 个生态插件的分类与元数据映射
ECOSYSTEM_META: dict[str, dict[str, str]] = {
    "astrbot_plugin_hub": {"label": "生态中枢与面板", "category": "hub", "icon": "🎛️"},
    "astrbot_plugin_chat_digest": {"label": "群聊记忆摘要", "category": "efficiency", "icon": "📝"},
    "astrbot_plugin_memo": {"label": "备忘与定时提醒", "category": "efficiency", "icon": "⏰"},
    "astrbot_plugin_group_stats": {"label": "群统计报表", "category": "efficiency", "icon": "📊"},
    "astrbot_plugin_daily_news": {"label": "每日新闻播报", "category": "efficiency", "icon": "📰"},
    "astrbot_plugin_weather": {"label": "天气查询播报", "category": "efficiency", "icon": "🌤️"},
    "astrbot_plugin_translator": {"label": "多语种翻译", "category": "efficiency", "icon": "🌐"},
    "astrbot_plugin_qa": {"label": "自定义问答", "category": "efficiency", "icon": "💬"},
    "astrbot_plugin_command_guide": {"label": "指令大全", "category": "efficiency", "icon": "📖"},
    "astrbot_plugin_anti_flood": {"label": "防刷屏过滤", "category": "guard", "icon": "🛡️"},
    "astrbot_plugin_ignore_at": {"label": "忽略他人互@", "category": "guard", "icon": "🙈"},
    "astrbot_plugin_smart_silence": {"label": "智能静默", "category": "guard", "icon": "🤫"},
    "astrbot_plugin_context_analyzer": {"label": "上下文与审计", "category": "ops", "icon": "🔍"},
    "astrbot_plugin_remote_task": {"label": "远程任务助手", "category": "ops", "icon": "🚀"},
    "astrbot_plugin_status_sync": {"label": "多机状态同步", "category": "ops", "icon": "🖥️"},
    "astrbot_plugin_github_monitor": {"label": "GitHub 监控", "category": "ops", "icon": "🐙"},
    "astrbot_plugin_sendmail": {"label": "邮件发送助手", "category": "ops", "icon": "📧"},
    "astrbot_plugin_group_games": {"label": "群聊小游戏", "category": "fun", "icon": "🎮"},
    "astrbot_plugin_fortune": {"label": "每日运势占卜", "category": "fun", "icon": "🔮"},
    "astrbot_plugin_music_custom": {"label": "多源点歌", "category": "fun", "icon": "🎵"},
    "astrbot_plugin_gay": {"label": "浓度检测娱乐", "category": "fun", "icon": "🌈"},
}


def is_secret_key(key: str) -> bool:
    return bool(SECRET_FIELD_RE.search(key or ""))


class PluginRegistry:
    """统一发现并管理 AstrBot 中已加载与本地安装的插件实例与配置。"""

    def __init__(
        self,
        context: Any,
        plugins_dir: str,
        astrbot_data_dir: str,
    ) -> None:
        self.context = context
        self.plugins_dir = os.path.abspath(plugins_dir)
        self.astrbot_data_dir = os.path.abspath(astrbot_data_dir)
        self._local_instances: dict[str, Any] = {}

    def register_local_instance(self, name: str, instance: Any) -> None:
        """显式注册本地插件实例（供 Hub 自身与单元测试注入使用）。"""
        self._local_instances[name] = instance

    def _discover_live_stars(self) -> dict[str, dict[str, Any]]:
        live: dict[str, dict[str, Any]] = {}
        if self.context is not None and hasattr(self.context, "get_all_stars"):
            try:
                stars = self.context.get_all_stars() or []
            except Exception:
                stars = []
            for st in stars:
                name = str(getattr(st, "name", "") or getattr(st, "root_dir_name", "") or "")
                if not name:
                    continue
                inst = getattr(st, "star_cls", None)
                live[name] = {
                    "name": name,
                    "display_name": getattr(st, "display_name", "") or name,
                    "version": str(getattr(st, "version", "") or ""),
                    "author": str(getattr(st, "author", "") or ""),
                    "desc": str(getattr(st, "desc", "") or ""),
                    "activated": bool(getattr(st, "activated", True)),
                    "instance": inst,
                    "star_config": getattr(st, "config", None),
                }
        for name, inst in self._local_instances.items():
            entry = live.setdefault(
                name,
                {
                    "name": name,
                    "display_name": ECOSYSTEM_META.get(name, {}).get("label", name),
                    "version": "",
                    "author": "云晓",
                    "desc": "",
                    "activated": True,
                    "instance": inst,
                    "star_config": None,
                },
            )
            entry["instance"] = inst
            entry["activated"] = True
        return live

    def _safe_child_path(self, base_dir: str, *parts: str) -> str:
        base_abs = os.path.abspath(base_dir)
        target = os.path.abspath(os.path.join(base_abs, *parts))
        if os.path.commonpath([base_abs, target]) != base_abs:
            raise ValueError(f"路径越界被拒绝：{parts}")
        return target

    def _read_disk_metadata(self, plugin_name: str) -> dict[str, Any]:
        name = validate_plugin_name(plugin_name)
        meta_path = self._safe_child_path(self.plugins_dir, name, "metadata.yaml")
        if not os.path.isfile(meta_path):
            return {}
        try:
            with open(meta_path, "r", encoding="utf-8-sig") as f:
                data = yaml.safe_load(f) or {}
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _read_schema(self, plugin_name: str) -> dict[str, Any]:
        name = validate_plugin_name(plugin_name)
        schema_path = self._safe_child_path(self.plugins_dir, name, "_conf_schema.json")
        return safe_read_json(schema_path, {})

    def _config_file_path(self, plugin_name: str) -> str:
        name = validate_plugin_name(plugin_name)
        cfg_root = os.path.join(self.astrbot_data_dir, "config")
        return self._safe_child_path(cfg_root, f"{name}_config.json")

    def get_live_instance(self, plugin_name: str) -> Any:
        live = self._discover_live_stars()
        entry = live.get(plugin_name)
        return entry["instance"] if entry else None

    def has_live_plugin(self, plugin_name: str) -> bool:
        return self.get_live_instance(plugin_name) is not None

    def list_plugins(self, include_third_party: bool = True) -> list[dict[str, Any]]:
        live = self._discover_live_stars()
        names: set[str] = set(live.keys())
        # 同时扫描本地 plugins 目录中已安装但未激活的生态插件
        if os.path.isdir(self.plugins_dir):
            for entry in os.listdir(self.plugins_dir):
                full = os.path.join(self.plugins_dir, entry)
                if os.path.isdir(full) and os.path.isfile(os.path.join(full, "metadata.yaml")):
                    if include_third_party or entry in ECOSYSTEM_META:
                        names.add(entry)

        result: list[dict[str, Any]] = []
        for name in sorted(names, key=lambda n: (0 if n in ECOSYSTEM_META else 1, n)):
            eco = ECOSYSTEM_META.get(name)
            if not include_third_party and eco is None:
                continue
            disk_meta = self._read_disk_metadata(name)
            live_entry = live.get(name)
            inst = live_entry["instance"] if live_entry else None
            schema = self._read_schema(name)

            hub_info: dict[str, Any] = {}
            protocol_ver = 0
            if inst is not None:
                protocol_ver = int(getattr(inst, "HUB_PROTOCOL_VERSION", 0) or 0)
                if hasattr(inst, "hub_status") and callable(inst.hub_status):
                    try:
                        st = inst.hub_status()
                        if isinstance(st, dict):
                            hub_info = st
                    except Exception as exc:
                        hub_info = {"error": str(exc)}

            result.append({
                "name": name,
                "display_name": (eco or {}).get("label") or disk_meta.get("display_name") or (live_entry or {}).get("display_name") or name,
                "icon": (eco or {}).get("icon", "🧩"),
                "category": (eco or {}).get("category", "other"),
                "ecosystem": eco is not None,
                "version": str(disk_meta.get("version") or (live_entry or {}).get("version") or hub_info.get("version") or "unknown"),
                "author": str(disk_meta.get("author") or (live_entry or {}).get("author") or ""),
                "desc": str(disk_meta.get("desc") or (live_entry or {}).get("desc") or ""),
                "online": inst is not None and bool((live_entry or {}).get("activated", True)),
                "protocol_version": protocol_ver,
                "has_schema": bool(schema),
                "schema_count": len(schema),
                "metrics": hub_info.get("metrics", {}) if isinstance(hub_info.get("metrics"), dict) else {},
                "actions": list(hub_info.get("actions", [])) if isinstance(hub_info.get("actions"), list) else [],
                "status_text": str(hub_info.get("status", "online" if inst is not None else "offline")),
            })
        return result

    async def call_action(
        self,
        plugin_name: str,
        action: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        inst = self.get_live_instance(plugin_name)
        if inst is None:
            return {"ok": False, "plugin": plugin_name, "action": action, "error": f"插件 {plugin_name} 未加载或已停用"}
        fn = getattr(inst, "hub_action", None)
        if not callable(fn):
            return {"ok": False, "plugin": plugin_name, "action": action, "error": f"插件 {plugin_name} 未实现 hub_action 接口"}
        try:
            res = fn(action, dict(params or {}))
            if inspect.isawaitable(res):
                res = await res
            if isinstance(res, dict) and "ok" in res:
                return {"plugin": plugin_name, "action": action, **res}
            return {"ok": True, "plugin": plugin_name, "action": action, "data": res}
        except Exception as exc:
            return {"ok": False, "plugin": plugin_name, "action": action, "error": f"{type(exc).__name__}: {exc}"}

    # ==================== 在线配置读写与安全脱敏 ====================

    def _get_live_cfg_dict(self, plugin_name: str) -> Any:
        live = self._discover_live_stars()
        entry = live.get(plugin_name)
        if not entry:
            return None
        if entry.get("star_config") is not None:
            return entry["star_config"]
        inst = entry.get("instance")
        if inst is None:
            return None
        for attr in ("config", "cfg"):
            obj = getattr(inst, attr, None)
            if isinstance(obj, dict):
                return obj
        return None

    def get_plugin_config(self, plugin_name: str) -> dict[str, Any]:
        schema = self._read_schema(plugin_name)
        disk_path = self._config_file_path(plugin_name)
        disk_cfg = safe_read_json(disk_path, {})
        live_cfg = self._get_live_cfg_dict(plugin_name)

        merged: dict[str, Any] = {}
        for k, spec in schema.items():
            if isinstance(spec, dict) and "default" in spec:
                merged[k] = spec["default"]
        if isinstance(disk_cfg, dict):
            merged.update(disk_cfg)
        if isinstance(live_cfg, dict):
            merged.update(dict(live_cfg))

        fields: list[dict[str, Any]] = []
        for k, spec in schema.items():
            if not isinstance(spec, dict):
                continue
            val = merged.get(k, spec.get("default"))
            secret = is_secret_key(k)
            has_value = bool(val) if isinstance(val, str) else val is not None
            display_val = SECRET_MASK if (secret and isinstance(val, str) and val.strip()) else val
            fields.append({
                "key": k,
                "type": spec.get("type", "string"),
                "description": spec.get("description", k),
                "hint": spec.get("hint", ""),
                "default": spec.get("default"),
                "value": display_val,
                "is_secret": secret,
                "has_value": has_value,
            })

        return {
            "plugin": plugin_name,
            "config_path": disk_path,
            "live": live_cfg is not None,
            "fields": fields,
        }

    def save_plugin_config(self, plugin_name: str, incoming: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(incoming, dict):
            raise ValueError("配置参数必须是 JSON 对象")
        schema = self._read_schema(plugin_name)
        if not schema:
            raise ValueError(f"插件 {plugin_name} 不存在 _conf_schema.json")

        disk_path = self._config_file_path(plugin_name)
        current = safe_read_json(disk_path, {})
        live_cfg = self._get_live_cfg_dict(plugin_name)
        if isinstance(live_cfg, dict):
            merged_current = dict(current)
            merged_current.update(dict(live_cfg))
        else:
            merged_current = dict(current)

        updated: dict[str, Any] = dict(merged_current)
        changed_keys: list[str] = []

        for k, spec in schema.items():
            if not isinstance(spec, dict) or k not in incoming:
                continue
            raw = incoming[k]
            # 脱敏占位符原样提交时保留原密文不覆盖
            if is_secret_key(k) and raw == SECRET_MASK:
                continue
            t = str(spec.get("type", "string")).lower()
            if t == "bool":
                if isinstance(raw, bool):
                    coerced: Any = raw
                elif str(raw).strip().lower() in ("true", "1", "yes", "on"):
                    coerced = True
                elif str(raw).strip().lower() in ("false", "0", "no", "off", ""):
                    coerced = False
                else:
                    raise ValueError(f"配置项 {k} 需要布尔值")
            elif t == "int":
                try:
                    coerced = int(raw)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"配置项 {k} 需要整数") from exc
            elif t == "float":
                try:
                    coerced = float(raw)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"配置项 {k} 需要浮点数") from exc
            elif t == "list":
                if isinstance(raw, list):
                    coerced = raw
                elif isinstance(raw, str):
                    coerced = [x.strip() for x in raw.split(",") if x.strip()]
                else:
                    raise ValueError(f"配置项 {k} 需要列表")
            else:
                coerced = "" if raw is None else str(raw)

            if updated.get(k) != coerced:
                changed_keys.append(k)
            updated[k] = coerced

        # 原子写入 AstrBot 插件配置文件
        atomic_write_json(disk_path, updated)

        # 热更新内存配置对象（支持 AstrBotConfig.save_config()）
        if isinstance(live_cfg, dict):
            live_cfg.update(updated)
            save_fn = getattr(live_cfg, "save_config", None)
            if callable(save_fn):
                try:
                    save_fn()
                except Exception:
                    pass

        return {"ok": True, "plugin": plugin_name, "changed_keys": changed_keys, "config_path": disk_path}

    # ==================== 跨插件聚合数据视图 ====================

    async def get_aggregated_data(self, panel: str, bus: Any = None) -> dict[str, Any]:
        p = (panel or "overview").lower()
        if p == "antispam":
            out = {}
            for name in ("astrbot_plugin_anti_flood", "astrbot_plugin_ignore_at", "astrbot_plugin_smart_silence"):
                inst = self.get_live_instance(name)
                out[name] = inst.hub_status() if (inst and hasattr(inst, "hub_status")) else {"status": "offline"}
            bots = await self.call_action("astrbot_plugin_anti_flood", "get_bot_ids", {})
            return {"panel": "antispam", "plugins": out, "bot_ids": (bots.get("data") or {}).get("bot_ids", []) if bots.get("ok") else []}

        if p == "digest":
            ov = await self.call_action("astrbot_plugin_chat_digest", "get_overview", {})
            return {"panel": "digest", "data": ov.get("data", {}) if ov.get("ok") else {}, "online": ov.get("ok", False)}

        if p == "memo":
            ov = await self.call_action("astrbot_plugin_memo", "list_data", {})
            return {"panel": "memo", "data": ov.get("data", {}) if ov.get("ok") else {}, "online": ov.get("ok", False)}

        if p == "points":
            eco = bus.get_eco_leaderboard(limit=25) if bus else []
            games = await self.call_action("astrbot_plugin_group_games", "get_leaderboard", {})
            stats = await self.call_action("astrbot_plugin_group_stats", "get_daily_summary", {})
            fortune = await self.call_action("astrbot_plugin_fortune", "get_ranking", {})
            return {
                "panel": "points",
                "eco_leaderboard": eco,
                "group_games": games.get("data", {}) if games.get("ok") else {},
                "group_stats": stats.get("data", {}) if stats.get("ok") else {},
                "fortune": fortune.get("data", {}) if fortune.get("ok") else {},
            }

        if p == "ops":
            rt = await self.call_action("astrbot_plugin_remote_task", "list_tasks", {"limit": 10})
            ss = await self.call_action("astrbot_plugin_status_sync", "get_machines_status", {})
            gh = await self.call_action("astrbot_plugin_github_monitor", "list_repos", {})
            sm = await self.call_action("astrbot_plugin_sendmail", "get_history", {"limit": 10})
            ca = await self.call_action("astrbot_plugin_context_analyzer", "get_health_summary", {})
            return {
                "panel": "ops",
                "remote_task": rt.get("data", {}) if rt.get("ok") else {},
                "status_sync": ss.get("data", {}) if ss.get("ok") else {},
                "github_monitor": gh.get("data", {}) if gh.get("ok") else {},
                "sendmail": sm.get("data", {}) if sm.get("ok") else {},
                "context_analyzer": ca.get("data", {}) if ca.get("ok") else {},
            }

        if p == "tools":
            qa = await self.call_action("astrbot_plugin_qa", "list_qa", {})
            tr = await self.call_action("astrbot_plugin_translator", "get_stats", {})
            mc = await self.call_action("astrbot_plugin_music_custom", "get_stats", {})
            gy = await self.call_action("astrbot_plugin_gay", "get_ranking", {})
            cg = await self.call_action("astrbot_plugin_command_guide", "list_all_commands", {})
            return {
                "panel": "tools",
                "qa": qa.get("data", {}) if qa.get("ok") else {},
                "translator": tr.get("data", {}) if tr.get("ok") else {},
                "music_custom": mc.get("data", {}) if mc.get("ok") else {},
                "gay": gy.get("data", {}) if gy.get("ok") else {},
                "commands": cg.get("data", {}) if cg.get("ok") else {},
            }

        return {"panel": p, "error": "未知数据视图"}
