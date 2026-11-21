# -*- coding: utf-8 -*-
"""astrbot_plugin_hub 单元测试：事件总线、10 条联动管线、配置脱敏热更新、端口 Web 面板与鉴权。"""

import asyncio
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

import aiohttp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from astrbot_plugin_hub.bus import HUB_BUS_KEY  # noqa: E402
from astrbot_plugin_hub.main import PluginHubStar  # noqa: E402


class _MockPartner:
    HUB_PROTOCOL_VERSION = 1

    def __init__(self, name: str, actions: list[str]) -> None:
        self.name = name
        self._actions = actions
        self.calls: list[tuple[str, dict]] = []
        self.config: dict = {"enabled": True, "api_token": "real_secret_xyz", "limit": 10}

    def hub_status(self) -> dict:
        return {"version": "1.2.0", "status": "online", "metrics": {"调用数": len(self.calls)}, "actions": list(self._actions)}

    async def hub_action(self, action: str, params: dict | None = None) -> dict:
        self.calls.append((action, dict(params or {})))
        if action == "get_bot_ids":
            return {"ok": True, "data": {"bot_ids": ["888001"]}}
        return {"ok": True, "data": {"handled": action, "params": params or {}}}


class _FakeEvent:
    def __init__(self, text: str, umo: str = "onebot:GroupMessage:1001", uid: str = "100", admin: bool = False) -> None:
        self.message_str = text
        self.unified_msg_origin = umo
        self._uid = uid
        self._admin = admin

    def get_sender_id(self) -> str:
        return self._uid

    def is_admin(self) -> bool:
        return self._admin

    def plain_result(self, text: str) -> str:
        return text


class _FakeContext:
    def get_all_stars(self):
        return []


class TestPluginHub(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp(prefix="hub_test_")
        self.plugins_dir = os.path.join(self.tmp, "plugins")
        self.astrbot_data = os.path.join(self.tmp, "astrbot_data")
        os.makedirs(self.plugins_dir, exist_ok=True)
        os.makedirs(self.astrbot_data, exist_ok=True)
        # 构造一个带 schema 的模拟插件目录供在线配置编辑器测试
        sample_dir = os.path.join(self.plugins_dir, "astrbot_plugin_memo")
        os.makedirs(sample_dir, exist_ok=True)
        with open(os.path.join(sample_dir, "metadata.yaml"), "w", encoding="utf-8") as f:
            f.write("name: astrbot_plugin_memo\nversion: 1.2.0\nauthor: 云晓\ndesc: 备忘测试\n")
        with open(os.path.join(sample_dir, "_conf_schema.json"), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "enabled": {"type": "bool", "default": True, "description": "开关"},
                    "limit": {"type": "int", "default": 10, "description": "上限"},
                    "api_token": {"type": "string", "default": "", "description": "令牌"},
                },
                f,
                ensure_ascii=False,
            )

        self.hub = PluginHubStar(
            _FakeContext(),
            config={
                "web_enabled": True,
                "web_host": "127.0.0.1",
                "web_port": 0,  # 随机可用端口
                "require_auth_on_localhost": False,
                "auto_linkage_enabled": True,
                "digest_copy_email": "ops@example.com",
                "ops_alert_email": "alert@example.com",
                "ops_archive_umo": "onebot:GroupMessage:9999",
                "fortune_bonus_threshold": 85,
                "fortune_bonus_quota": 2,
                "admin_user_ids": "999",
            },
            data_dir=os.path.join(self.tmp, "hub_data"),
            plugins_dir=self.plugins_dir,
        )
        self.hub.astrbot_data_dir = self.astrbot_data
        self.hub.registry.astrbot_data_dir = self.astrbot_data

        # 注入各模拟合作插件
        self.partners = {
            "astrbot_plugin_chat_digest": _MockPartner("astrbot_plugin_chat_digest", ["add_highlight", "add_todo", "get_overview"]),
            "astrbot_plugin_memo": _MockPartner("astrbot_plugin_memo", ["add_memo", "list_data"]),
            "astrbot_plugin_sendmail": _MockPartner("astrbot_plugin_sendmail", ["send_mail", "get_history"]),
            "astrbot_plugin_anti_flood": _MockPartner("astrbot_plugin_anti_flood", ["get_bot_ids", "mark_bot"]),
            "astrbot_plugin_group_stats": _MockPartner("astrbot_plugin_group_stats", ["add_ignored_bot", "add_points", "get_daily_summary"]),
            "astrbot_plugin_smart_silence": _MockPartner("astrbot_plugin_smart_silence", ["sync_bot_ids", "get_stats"]),
            "astrbot_plugin_ignore_at": _MockPartner("astrbot_plugin_ignore_at", ["sync_bot_ids", "get_stats"]),
            "astrbot_plugin_context_analyzer": _MockPartner("astrbot_plugin_context_analyzer", ["record_external_event", "get_health_summary"]),
            "astrbot_plugin_music_custom": _MockPartner("astrbot_plugin_music_custom", ["grant_bonus_quota", "get_stats"]),
        }
        for name, inst in self.partners.items():
            self.hub.registry.register_local_instance(name, inst)

    def tearDown(self) -> None:
        asyncio.run(self.hub.terminate())
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_schema_covers_all_config_keys(self) -> None:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(plugin_dir, "_conf_schema.json"), encoding="utf-8-sig") as f:
            schema = json.load(f)
        with open(os.path.join(plugin_dir, "main.py"), encoding="utf-8-sig") as f:
            main_src = f.read()
        with open(os.path.join(plugin_dir, "bus.py"), encoding="utf-8-sig") as f:
            bus_src = f.read()
        used = set(re.findall(r'cfg_(?:bool|int|str)\("([^"]+)"', main_src))
        used |= set(re.findall(r'cfg\.get\("([^"]+)"', bus_src))
        self.assertEqual(used - set(schema.keys()), set())
        self.assertEqual(set(schema.keys()) - used, set())

    def test_all_10_builtin_linkage_pipelines_and_custom_rule(self) -> None:
        async def _run():
            # 1. digest_todo_to_memo
            await self.hub.bus.emit_async("astrbot_plugin_chat_digest", "digest.todo_added", {"umo": "g:1", "title": "提交代码", "assignee": "云晓"})
            self.assertEqual(self.partners["astrbot_plugin_memo"].calls[-1][0], "add_memo")

            # 2. digest_email_copy
            await self.hub.bus.emit_async("astrbot_plugin_chat_digest", "digest.created", {"umo": "g:1", "date": "2026-11-21", "summary": "日报", "message_count": 12})
            self.assertEqual(self.partners["astrbot_plugin_sendmail"].calls[-1][0], "send_mail")

            # 3. antiflood_share_bots
            await self.hub.bus.emit_async("astrbot_plugin_anti_flood", "antiflood.bot_detected", {"bot_id": "999888"})
            self.assertEqual(self.partners["astrbot_plugin_group_stats"].calls[-1][0], "add_ignored_bot")
            self.assertEqual(self.partners["astrbot_plugin_smart_silence"].calls[-1][0], "sync_bot_ids")
            self.assertEqual(self.partners["astrbot_plugin_ignore_at"].calls[-1][0], "sync_bot_ids")

            # 4. antispam_to_context
            await self.hub.bus.emit_async("astrbot_plugin_ignore_at", "ignore_at.blocked", {"group_id": "1001", "user_id": "2"})
            self.assertEqual(self.partners["astrbot_plugin_context_analyzer"].calls[-1][0], "record_external_event")

            # 5 & 6. ops_alerts_to_digest + ops_alerts_to_mail
            await self.hub.bus.emit_async("astrbot_plugin_github_monitor", "github_monitor.release_found", {"repo": "yunxiao258/demo", "summary": "发布 v2.0.0"})
            self.assertEqual(self.partners["astrbot_plugin_chat_digest"].calls[-1][0], "add_highlight")
            self.assertEqual(self.partners["astrbot_plugin_sendmail"].calls[-1][0], "send_mail")

            # 7 & 8. points_economy_bridge + lucky_fortune_music_bonus
            await self.hub.bus.emit_async("astrbot_plugin_fortune", "fortune.drawn", {"user_id": "u77", "nickname": "欧皇", "score": 95, "group_id": "1001"})
            self.assertEqual(self.partners["astrbot_plugin_music_custom"].calls[-1][0], "grant_bonus_quota")
            self.assertEqual(self.partners["astrbot_plugin_group_stats"].calls[-1][0], "add_points")
            lb = self.hub.bus.get_eco_leaderboard()
            self.assertEqual(lb[0]["user_id"], "u77")
            self.assertEqual(lb[0]["total"], 5)

            # 9. news_weather_to_digest
            await self.hub.bus.emit_async("astrbot_plugin_daily_news", "daily_news.pushed", {"umo": "g:1", "summary": "今日科技头条"})
            self.assertIn("[每日新闻]", self.partners["astrbot_plugin_chat_digest"].calls[-1][1]["text"])

            # 10. qa_translator_to_digest
            await self.hub.bus.emit_async("astrbot_plugin_qa", "qa.added", {"umo": "g:1", "question": "端口", "answer": "8686"})
            self.assertIn("[问答]", self.partners["astrbot_plugin_chat_digest"].calls[-1][1]["text"])

            # 11. 自定义规则
            cr = self.hub.bus.add_custom_rule("自定义转发", "astrbot_plugin_gay", "gay.tested", "astrbot_plugin_memo", "add_memo", {"umo": "g:1", "content": "记录一次测试"})
            await self.hub.bus.emit_async("astrbot_plugin_gay", "gay.tested", {"user_id": "u1"})
            self.assertEqual(self.partners["astrbot_plugin_memo"].calls[-1][1]["content"], "记录一次测试")
            self.assertTrue(self.hub.bus.delete_custom_rule(cr["id"]))

            # 12. 防循环重入保护
            sk = await self.hub.bus.emit_async("astrbot_plugin_memo", "memo.added", {"_hub_origin": "orig1"})
            self.assertTrue(sk.get("skipped"))

        asyncio.run(_run())

    def test_online_config_masking_and_hot_reload(self) -> None:
        cfg_view = self.hub.registry.get_plugin_config("astrbot_plugin_memo")
        fields = {f["key"]: f for f in cfg_view["fields"]}
        self.assertTrue(fields["api_token"]["is_secret"])
        self.assertEqual(fields["api_token"]["value"], "******")

        # 保存时脱敏占位符不覆盖原密文，且普通字段热更新内存+落盘
        res = self.hub.registry.save_plugin_config(
            "astrbot_plugin_memo",
            {"enabled": False, "limit": 25, "api_token": "******"},
        )
        self.assertTrue(res["ok"])
        self.assertEqual(self.partners["astrbot_plugin_memo"].config["limit"], 25)
        self.assertFalse(self.partners["astrbot_plugin_memo"].config["enabled"])
        self.assertEqual(self.partners["astrbot_plugin_memo"].config["api_token"], "real_secret_xyz")
        self.assertTrue(os.path.isfile(res["config_path"]))

    def test_web_server_localhost_no_auth_and_forced_auth(self) -> None:
        async def _run():
            await self.hub.initialize()
            self.assertIs(sys.modules.get(HUB_BUS_KEY), self.hub.bus)
            base = self.hub.web_server.url

            async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as cli:
                # 1. 本机免登访问首页与核心 API
                async with cli.get(f"{base}/") as r:
                    self.assertEqual(r.status, 200)
                    html = await r.text()
                    self.assertIn("AstrBot 插件生态中枢", html)

                async with cli.get(f"{base}/api/overview") as r:
                    self.assertEqual(r.status, 200)
                    ov = await r.json()
                    self.assertTrue(ov["ok"])
                    self.assertFalse(ov["auth"]["required"])

                async with cli.post(f"{base}/api/rules/digest_todo_to_memo/toggle", json={"enabled": False}) as r:
                    self.assertEqual(r.status, 200)
                    self.assertFalse((await r.json())["rule"]["enabled"])

                async with cli.post(
                    f"{base}/api/plugins/astrbot_plugin_memo/action",
                    json={"action": "add_memo", "params": {"umo": "g:1", "content": "来自面板"}},
                ) as r:
                    self.assertEqual(r.status, 200)
                    self.assertTrue((await r.json())["ok"])

                # 2. 开启强制鉴权（模拟外网暴露或 require_auth_on_localhost=True）
                self.hub.web_server.require_auth_on_localhost = True
                async with cli.get(f"{base}/api/overview") as r:
                    self.assertEqual(r.status, 401)
                async with cli.post(f"{base}/api/login", json={"token": "wrong_tok"}) as r:
                    self.assertEqual(r.status, 401)
                async with cli.post(f"{base}/api/login", json={"token": self.hub.web_server.token}) as r:
                    self.assertEqual(r.status, 200)
                async with cli.get(f"{base}/api/overview") as r:
                    self.assertEqual(r.status, 200)
                async with cli.post(f"{base}/api/logout") as r:
                    self.assertEqual(r.status, 200)
                async with cli.get(f"{base}/api/overview") as r:
                    self.assertEqual(r.status, 401)

            await self.hub.terminate()
            self.assertIsNone(sys.modules.get(HUB_BUS_KEY))

        asyncio.run(_run())

    def test_chat_commands_and_permissions(self) -> None:
        async def _run():
            await self.hub.initialize()
            st = await self.hub.hub_command(_FakeEvent("/中枢"))
            self.assertIn("插件生态中枢", st)
            hp = await self.hub.hub_command(_FakeEvent("/hub 帮助"))
            self.assertIn("/中枢 面板", hp)

            # 群聊不泄露 Token，私聊管理员可见（强制鉴权模式下）
            self.hub.web_server.require_auth_on_localhost = True
            p_grp = await self.hub.hub_command(_FakeEvent("/面板 面板", umo="onebot:GroupMessage:1", uid="999"))
            self.assertNotIn(self.hub.web_server.token, p_grp)
            p_priv = await self.hub.hub_command(_FakeEvent("/中枢 面板", umo="onebot:FriendMessage:999", uid="999"))
            self.assertIn(self.hub.web_server.token, p_priv)

            # 非管理员不能开关联动或触发动作
            deny = await self.hub.hub_command(_FakeEvent("/中枢 联动 关闭 digest_todo_to_memo", admin=False))
            self.assertIn("仅限管理员", deny)
            ok = await self.hub.hub_command(_FakeEvent("/中枢 联动 关闭 digest_todo_to_memo", admin=True))
            self.assertIn("已关闭", ok)

            trig = await self.hub.hub_command(_FakeEvent('/中枢 触发 memo add_memo {"umo":"g:1","content":"hi"}', admin=True))
            self.assertIn("已执行", trig)

        asyncio.run(_run())


if __name__ == "__main__":
    unittest.main(verbosity=1)
