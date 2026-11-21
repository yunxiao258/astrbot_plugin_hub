# -*- coding: utf-8 -*-
"""AstrBot 插件生态中枢单页 Web 管理面板（纯静态无外部 CDN，国内离线可用）。"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AstrBot 插件生态中枢 · 管理面板</title>
<style>
:root {
  --bg: #0b1120;
  --panel: #111827;
  --card: #1e293b;
  --card-hover: #263449;
  --border: #334155;
  --text: #f1f5f9;
  --muted: #94a3b8;
  --accent: #38bdf8;
  --accent-bg: rgba(56,189,248,0.14);
  --green: #22c55e;
  --green-bg: rgba(34,197,94,0.15);
  --amber: #f59e0b;
  --amber-bg: rgba(245,158,11,0.15);
  --red: #ef4444;
  --red-bg: rgba(239,68,68,0.15);
  --purple: #a78bfa;
  --radius: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  line-height: 1.5;
}
.topbar {
  position: sticky; top: 0; z-index: 40;
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
  padding: 14px 24px;
  background: rgba(17, 24, 39, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand-logo {
  width: 36px; height: 36px; border-radius: 10px;
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  display: flex; align-items: center; justify-content: center; font-size: 20px;
}
.brand h1 { font-size: 17px; font-weight: 700; letter-spacing: .3px; }
.brand small { color: var(--muted); font-size: 12px; display: block; }
.nav-tabs { display: flex; gap: 6px; flex-wrap: wrap; }
.tab-btn {
  padding: 8px 14px; border-radius: 8px; border: 1px solid transparent;
  background: transparent; color: var(--muted); cursor: pointer; font-size: 14px; font-weight: 500;
  transition: all .15s;
}
.tab-btn:hover { color: var(--text); background: var(--card); }
.tab-btn.active { color: var(--accent); background: var(--accent-bg); border-color: rgba(56,189,248,0.35); }
.top-actions { display: flex; align-items: center; gap: 10px; }
.pill {
  font-size: 12px; padding: 4px 10px; border-radius: 999px;
  background: var(--green-bg); color: var(--green); border: 1px solid rgba(34,197,94,0.3);
}
.pill.warn { background: var(--amber-bg); color: var(--amber); border-color: rgba(245,158,11,0.3); }
.btn {
  padding: 7px 14px; border-radius: 8px; border: 1px solid var(--border);
  background: var(--card); color: var(--text); cursor: pointer; font-size: 13px; transition: all .15s;
}
.btn:hover { background: var(--card-hover); border-color: var(--accent); }
.btn-primary { background: #2563eb; border-color: #3b82f6; color: #fff; }
.btn-primary:hover { background: #1d4ed8; }
.btn-danger { background: rgba(239,68,68,0.18); border-color: rgba(239,68,68,0.4); color: #fca5a5; }
.btn-sm { padding: 4px 10px; font-size: 12px; }
.container { max-width: 1420px; margin: 0 auto; padding: 20px 24px 60px; }
.section { display: none; }
.section.active { display: block; }
.kpi-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 14px; margin-bottom: 20px;
}
.kpi {
  background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 18px;
}
.kpi .label { color: var(--muted); font-size: 12px; margin-bottom: 6px; }
.kpi .val { font-size: 28px; font-weight: 700; color: var(--text); }
.kpi .sub { font-size: 12px; color: var(--accent); margin-top: 4px; }
.panel-box {
  background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 18px 20px; margin-bottom: 20px;
}
.panel-head {
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;
  margin-bottom: 14px;
}
.panel-head h2 { font-size: 16px; font-weight: 600; }
.filter-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
input[type="text"], input[type="password"], input[type="number"], select, textarea {
  background: var(--bg); color: var(--text); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 11px; font-size: 13px; outline: none;
}
input:focus, select:focus, textarea:focus { border-color: var(--accent); }
.plugin-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 14px;
}
.p-card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px 16px; display: flex; flex-direction: column; gap: 8px; transition: border-color .15s;
}
.p-card:hover { border-color: rgba(56,189,248,0.5); }
.p-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.p-title { font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 6px; }
.badge { font-size: 11px; padding: 2px 8px; border-radius: 999px; font-weight: 600; }
.badge.on { background: var(--green-bg); color: var(--green); }
.badge.off { background: var(--red-bg); color: var(--red); }
.badge.proto { background: var(--accent-bg); color: var(--accent); }
.p-desc { font-size: 12px; color: var(--muted); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.metrics { display: flex; flex-wrap: wrap; gap: 6px; }
.metric-chip { font-size: 11px; padding: 2px 7px; border-radius: 6px; background: rgba(15,23,42,0.8); color: #cbd5e1; border: 1px solid #283548; }
.p-foot { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 6px; border-top: 1px solid rgba(51,65,85,0.6); }
.topo-wrap { width: 100%; overflow-x: auto; }
svg.topo { width: 100%; min-width: 760px; height: 340px; display: block; }
.rule-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 12px; }
.rule-card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px 16px; display: flex; flex-direction: column; gap: 8px;
}
.switch { position: relative; display: inline-block; width: 42px; height: 22px; flex-shrink: 0; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; inset: 0; background: #475569; border-radius: 22px; transition: .2s;
}
.slider:before {
  content: ""; position: absolute; height: 16px; width: 16px; left: 3px; bottom: 3px;
  background: #fff; border-radius: 50%; transition: .2s;
}
input:checked + .slider { background: #22c55e; }
input:checked + .slider:before { transform: translateX(20px); }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid rgba(51,65,85,0.65); vertical-align: top; }
th { color: var(--muted); font-weight: 600; font-size: 12px; }
.split-layout { display: grid; grid-template-columns: 260px 1fr; gap: 18px; }
@media (max-width: 860px) { .split-layout { grid-template-columns: 1fr; } }
.side-list { display: flex; flex-direction: column; gap: 4px; max-height: 70vh; overflow-y: auto; }
.side-item {
  padding: 9px 12px; border-radius: 8px; cursor: pointer; font-size: 13px;
  display: flex; justify-content: space-between; align-items: center; color: var(--muted);
  border: 1px solid transparent;
}
.side-item:hover { background: var(--card); color: var(--text); }
.side-item.active { background: var(--accent-bg); color: var(--accent); border-color: rgba(56,189,248,0.35); }
.form-row {
  display: grid; grid-template-columns: 240px 1fr; gap: 12px; align-items: start;
  padding: 12px 0; border-bottom: 1px solid rgba(51,65,85,0.5);
}
@media (max-width: 720px) { .form-row { grid-template-columns: 1fr; } }
.form-label strong { font-size: 13px; display: block; color: var(--text); }
.form-label span { font-size: 12px; color: var(--muted); display: block; margin-top: 2px; }
.sub-tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 14px; }
pre.json-box {
  background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
  padding: 12px; overflow: auto; max-height: 360px; font-size: 12px; color: #cbd5e1;
  font-family: Consolas, Monaco, monospace;
}
.toast {
  position: fixed; right: 20px; bottom: 20px; z-index: 90;
  background: #1e293b; border: 1px solid var(--accent); color: var(--text);
  padding: 11px 16px; border-radius: 10px; font-size: 13px; display: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.45);
}
.modal-bg {
  position: fixed; inset: 0; z-index: 80; background: rgba(2,6,23,0.78);
  display: none; align-items: center; justify-content: center; padding: 20px;
}
.modal-card {
  background: var(--panel); border: 1px solid var(--border); border-radius: 14px;
  padding: 24px; width: 100%; max-width: 400px;
}
.modal-card h3 { margin-bottom: 8px; font-size: 18px; }
.modal-card p { font-size: 13px; color: var(--muted); margin-bottom: 14px; }
.code-inline { font-family: Consolas, monospace; background: var(--bg); padding: 2px 6px; border-radius: 5px; font-size: 12px; color: var(--accent); }
</style>
</head>
<body>
<header class="topbar">
  <div class="brand">
    <div class="brand-logo">🎛️</div>
    <div>
      <h1>AstrBot 插件生态中枢</h1>
      <small id="subInfo">加载中...</small>
    </div>
  </div>
  <nav class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('dashboard', this)">全景仪表盘</button>
    <button class="tab-btn" onclick="switchTab('rules', this)">联动规则与事件流</button>
    <button class="tab-btn" onclick="switchTab('data', this)">跨插件数据与操作</button>
    <button class="tab-btn" onclick="switchTab('config', this)">在线配置编辑器</button>
  </nav>
  <div class="top-actions">
    <span class="pill" id="authBadge">检测中</span>
    <button class="btn btn-sm" onclick="refreshAll()">刷新</button>
    <button class="btn btn-sm btn-danger" id="logoutBtn" style="display:none" onclick="doLogout()">退出登录</button>
  </div>
</header>

<main class="container">
  <!-- TAB 1: 全景仪表盘 -->
  <section id="tab-dashboard" class="section active">
    <div class="kpi-grid" id="kpiGrid"></div>

    <div class="panel-box">
      <div class="panel-head">
        <h2>🕸️ 全生态插件联动拓扑图</h2>
        <span style="font-size:12px;color:var(--muted)">蓝色：效率记忆 ｜ 绿色：防扰安全 ｜ 琥珀：运维监控 ｜ 紫色：娱乐积分</span>
      </div>
      <div class="topo-wrap">
        <svg class="topo" id="topoSvg" viewBox="0 0 1100 340"></svg>
      </div>
    </div>

    <div class="panel-box">
      <div class="panel-head">
        <h2>🧩 插件运行全景</h2>
        <div class="filter-row">
          <select id="catFilter" onchange="renderPlugins()">
            <option value="all">全部分类</option>
            <option value="hub">中枢管理</option>
            <option value="efficiency">效率与记忆</option>
            <option value="guard">防扰与安全</option>
            <option value="ops">运维与监控</option>
            <option value="fun">娱乐与积分</option>
            <option value="other">其他第三方</option>
          </select>
          <input type="text" id="pluginSearch" placeholder="搜索插件名 / 说明..." oninput="renderPlugins()">
        </div>
      </div>
      <div class="plugin-grid" id="pluginGrid"></div>
    </div>
  </section>

  <!-- TAB 2: 联动规则与事件流 -->
  <section id="tab-rules" class="section">
    <div class="panel-box">
      <div class="panel-head">
        <h2>⚡ 自动化联动管线（内置 10 条 + 自定义规则）</h2>
        <div class="filter-row">
          <button class="btn btn-primary btn-sm" onclick="toggleCustomForm()">+ 新建自定义规则</button>
        </div>
      </div>
      <div id="customRuleForm" style="display:none;background:var(--card);padding:14px;border-radius:10px;margin-bottom:14px;border:1px solid var(--border);">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:10px;">
          <input type="text" id="crName" placeholder="规则名称（如 运势通知备忘）">
          <input type="text" id="crSource" placeholder="源插件（如 astrbot_plugin_fortune 或 *）">
          <input type="text" id="crEvent" placeholder="事件类型（如 fortune.drawn 或 *）">
          <input type="text" id="crTarget" placeholder="目标插件（如 astrbot_plugin_chat_digest）">
          <input type="text" id="crAction" placeholder="目标动作（如 add_highlight）">
        </div>
        <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
          <input type="text" id="crPayload" style="flex:1;min-width:260px" placeholder='附加参数 JSON（可选，如 {"tags":["自定义"]}）'>
          <button class="btn btn-primary btn-sm" onclick="createCustomRule()">保存规则</button>
        </div>
      </div>
      <div class="rule-grid" id="ruleGrid"></div>
    </div>

    <div class="panel-box">
      <div class="panel-head">
        <h2>📡 实时跨插件事件流</h2>
        <div class="filter-row">
          <input type="text" id="evFilter" placeholder="按事件类型过滤..." oninput="renderEvents()">
          <button class="btn btn-sm" onclick="emitTestEvent()">发送测试联动事件</button>
        </div>
      </div>
      <div style="overflow-x:auto">
        <table>
          <thead><tr><th>时间</th><th>源插件</th><th>事件类型</th><th>载荷摘要</th><th>联动执行结果</th></tr></thead>
          <tbody id="eventBody"></tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- TAB 3: 跨插件数据与操作台 -->
  <section id="tab-data" class="section">
    <div class="panel-box">
      <div class="panel-head">
        <h2>🗂️ 跨插件聚合数据视图</h2>
        <div class="sub-tabs">
          <button class="btn btn-sm btn-primary" onclick="loadDataPanel('digest', this)">📝 群聊记忆</button>
          <button class="btn btn-sm" onclick="loadDataPanel('memo', this)">⏰ 备忘提醒</button>
          <button class="btn btn-sm" onclick="loadDataPanel('antispam', this)">🛡️ 防扰安全</button>
          <button class="btn btn-sm" onclick="loadDataPanel('points', this)">🏆 生态积分榜</button>
          <button class="btn btn-sm" onclick="loadDataPanel('ops', this)">🚀 运维监控</button>
          <button class="btn btn-sm" onclick="loadDataPanel('tools', this)">🧰 工具与指令</button>
        </div>
      </div>
      <div id="dataPanelContent"></div>
    </div>

    <div class="panel-box">
      <div class="panel-head"><h2>🎛️ 快捷跨插件动作触发器（hub_action）</h2></div>
      <div style="display:grid;grid-template-columns:240px 200px 1fr auto;gap:10px;align-items:center;margin-bottom:10px;">
        <select id="actPlugin" onchange="fillPluginActions()"></select>
        <select id="actName"></select>
        <input type="text" id="actParams" placeholder='JSON 参数，例如 {"umo":"default:GroupMessage:1001","content":"测试备忘"}' value="{}">
        <button class="btn btn-primary" onclick="runQuickAction()">立即执行</button>
      </div>
      <pre class="json-box" id="actResult">等待执行...</pre>
    </div>
  </section>

  <!-- TAB 4: 在线配置编辑器 -->
  <section id="tab-config" class="section">
    <div class="panel-box">
      <div class="panel-head">
        <h2>⚙️ 全插件在线配置编辑器（自动读取 _conf_schema.json，敏感字段自动脱敏）</h2>
      </div>
      <div class="split-layout">
        <div class="side-list" id="cfgPluginList"></div>
        <div>
          <div class="panel-head">
            <h2 id="cfgTitle">请选择左侧插件</h2>
            <button class="btn btn-primary btn-sm" id="cfgSaveBtn" style="display:none" onclick="saveCurrentConfig()">保存并热更新</button>
          </div>
          <div id="cfgFormWrap" style="color:var(--muted);font-size:13px;">点击左侧插件查看并编辑其配置项。</div>
        </div>
      </div>
    </div>
  </section>
</main>

<div class="modal-bg" id="loginModal">
  <div class="modal-card">
    <h3>🔐 管理员身份验证</h3>
    <p>当前面板已启用 Token 访问控制。请输入在配置中设置的 <span class="code-inline">web_token</span> 或自动生成的管理员令牌（可在群里发送 <span class="code-inline">/中枢 面板</span> 查看）。</p>
    <input type="password" id="loginToken" style="width:100%;margin-bottom:12px" placeholder="请输入管理员 Token">
    <button class="btn btn-primary" style="width:100%" onclick="doLogin()">登录管理面板</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let STATE = { overview: null, plugins: [], rules: [], events: [], currentCfgPlugin: null, currentCfgFields: [] };

function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.style.display = 'block';
  clearTimeout(window._tTimer);
  window._tTimer = setTimeout(() => { el.style.display = 'none'; }, 3000);
}

async function api(path, opts = {}) {
  const res = await fetch(path, {
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
    ...opts,
  });
  if (res.status === 401) {
    document.getElementById('loginModal').style.display = 'flex';
    throw new Error('需要登录鉴权');
  }
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || ('HTTP ' + res.status));
  return data;
}

function switchTab(id, btn) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  if (btn) btn.classList.add('active');
  if (id === 'data' && !document.getElementById('dataPanelContent').innerHTML) {
    loadDataPanel('digest');
  }
}

async function doLogin() {
  const tok = document.getElementById('loginToken').value.trim();
  if (!tok) return toast('请输入 Token');
  try {
    await api('/api/login', { method: 'POST', body: JSON.stringify({ token: tok }) });
    document.getElementById('loginModal').style.display = 'none';
    document.getElementById('logoutBtn').style.display = 'inline-block';
    toast('登录成功');
    await refreshAll();
  } catch (e) { toast('登录失败：' + e.message); }
}

async function doLogout() {
  await api('/api/logout', { method: 'POST' });
  document.getElementById('loginModal').style.display = 'flex';
}

async function refreshAll() {
  try {
    const [ov, rulesRes, evRes] = await Promise.all([
      api('/api/overview'),
      api('/api/rules'),
      api('/api/events?limit=60'),
    ]);
    STATE.overview = ov;
    STATE.plugins = ov.plugins || [];
    STATE.rules = rulesRes.rules || [];
    STATE.events = evRes.events || [];

    const auth = ov.auth || {};
    const badge = document.getElementById('authBadge');
    badge.textContent = auth.required ? '🔐 Token 鉴权已启用' : '🔓 本机免登模式';
    badge.className = 'pill' + (auth.required ? '' : ' warn');
    document.getElementById('logoutBtn').style.display = auth.required ? 'inline-block' : 'none';
    document.getElementById('subInfo').textContent = `监听 ${ov.server.host}:${ov.server.port} · 运行 ${ov.server.uptime_seconds}s · 生态协议 v1`;

    renderKPIs(ov);
    renderTopology(ov);
    renderPlugins();
    renderRules();
    renderEvents();
    renderConfigSidebar();
    populateActionPlugins();
  } catch (e) {
    if (e.message !== '需要登录鉴权') toast('刷新失败：' + e.message);
  }
}

function renderKPIs(ov) {
  const eco = STATE.plugins.filter(p => p.ecosystem);
  const onlineEco = eco.filter(p => p.online).length;
  const activeRules = STATE.rules.filter(r => r.enabled).length;
  const kpis = [
    { label: '自研生态插件', val: `${onlineEco} / ${eco.length}`, sub: `总发现插件 ${STATE.plugins.length} 个` },
    { label: '协议联动接入', val: STATE.plugins.filter(p => p.protocol_version >= 1).length, sub: '支持 hub_status + hub_action' },
    { label: '活跃联动管线', val: `${activeRules} / ${STATE.rules.length}`, sub: ov.auto_linkage_enabled ? '自动联动已开启' : '自动联动已暂停' },
    { label: '累计跨插件事件', val: ov.event_count, sub: `总触发联动 ${ov.total_rule_triggers} 次` },
    { label: '生态统一积分人数', val: ov.eco_users, sub: '跨游戏/群统计/运势/互动' },
  ];
  document.getElementById('kpiGrid').innerHTML = kpis.map(k =>
    `<div class="kpi"><div class="label">${k.label}</div><div class="val">${k.val}</div><div class="sub">${k.sub}</div></div>`
  ).join('');
}

function renderTopology(ov) {
  const svg = document.getElementById('topoSvg');
  const cols = {
    efficiency: { x: 140, color: '#38bdf8', items: [] },
    guard:      { x: 400, color: '#22c55e', items: [] },
    hub:        { x: 550, color: '#3b82f6', items: [] },
    ops:        { x: 740, color: '#f59e0b', items: [] },
    fun:        { x: 960, color: '#a78bfa', items: [] },
  };
  STATE.plugins.filter(p => p.ecosystem).forEach(p => {
    const c = cols[p.category] || cols.efficiency;
    c.items.push(p);
  });

  const pos = {};
  let nodesHtml = '';
  Object.entries(cols).forEach(([cat, col]) => {
    const n = col.items.length;
    col.items.forEach((p, idx) => {
      const y = cat === 'hub' ? 170 : (40 + idx * (270 / Math.max(1, n - 1 || 1)));
      pos[p.name] = { x: col.x, y, color: col.color };
      const r = cat === 'hub' ? 30 : 14;
      const opacity = p.online ? 1 : 0.4;
      nodesHtml += `<g style="cursor:pointer;opacity:${opacity}" onclick="openPluginConfig('${p.name}')">
        <circle cx="${col.x}" cy="${y}" r="${r}" fill="${col.color}" fill-opacity="0.22" stroke="${col.color}" stroke-width="${cat==='hub'?3:1.8}"/>
        <text x="${col.x}" y="${y+5}" text-anchor="middle" font-size="${cat==='hub'?18:12}" fill="#fff">${p.icon}</text>
        <text x="${col.x}" y="${y+(cat==='hub'?46:26)}" text-anchor="middle" font-size="11" fill="#cbd5e1">${p.display_name}</text>
      </g>`;
    });
  });

  let edgesHtml = '';
  STATE.rules.filter(r => r.enabled).forEach(r => {
    (r.sources || []).forEach(s => {
      (r.targets || []).forEach(t => {
        if (pos[s] && pos[t] && s !== t) {
          const a = pos[s], b = pos[t];
          const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2 - 18;
          edgesHtml += `<path d="M ${a.x} ${a.y} Q ${mx} ${my} ${b.x} ${b.y}" fill="none" stroke="${a.color}" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="4 3"/>`;
        }
      });
    });
  });
  svg.innerHTML = edgesHtml + nodesHtml;
}

function renderPlugins() {
  const cat = document.getElementById('catFilter').value;
  const kw = document.getElementById('pluginSearch').value.trim().toLowerCase();
  const list = STATE.plugins.filter(p => {
    if (cat !== 'all' && p.category !== cat) return false;
    if (kw && !(p.name.toLowerCase().includes(kw) || p.display_name.toLowerCase().includes(kw) || p.desc.toLowerCase().includes(kw))) return false;
    return true;
  });
  document.getElementById('pluginGrid').innerHTML = list.map(p => {
    const mChips = Object.entries(p.metrics || {}).slice(0, 5).map(([k, v]) => `<span class="metric-chip">${k}: ${v}</span>`).join('');
    return `<div class="p-card">
      <div class="p-head">
        <div class="p-title">${p.icon} ${p.display_name}</div>
        <div style="display:flex;gap:5px">
          ${p.protocol_version ? '<span class="badge proto">联动 v'+p.protocol_version+'</span>' : ''}
          <span class="badge ${p.online?'on':'off'}">${p.online?'在线':'离线'}</span>
        </div>
      </div>
      <div style="font-size:11px;color:var(--muted)">${p.name} · v${p.version}</div>
      <div class="p-desc">${p.desc || '暂无描述'}</div>
      <div class="metrics">${mChips || '<span class="metric-chip">无运行指标</span>'}</div>
      <div class="p-foot">
        <span style="font-size:11px;color:var(--muted)">动作 ${p.actions.length} · 配置项 ${p.schema_count}</span>
        <div style="display:flex;gap:6px">
          ${p.has_schema ? `<button class="btn btn-sm" onclick="openPluginConfig('${p.name}')">配置</button>` : ''}
          ${p.actions.length ? `<button class="btn btn-sm btn-primary" onclick="jumpToAction('${p.name}')">操作</button>` : ''}
        </div>
      </div>
    </div>`;
  }).join('');
}

function renderRules() {
  document.getElementById('ruleGrid').innerHTML = STATE.rules.map(r => `
    <div class="rule-card">
      <div class="p-head">
        <div>
          <strong style="font-size:14px">${r.name}</strong>
          <div style="font-size:11px;color:var(--muted)">ID: ${r.id} · ${r.builtin ? '内置管线' : '自定义规则'}</div>
        </div>
        <label class="switch">
          <input type="checkbox" ${r.enabled ? 'checked' : ''} onchange="toggleRule('${r.id}', this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div style="font-size:12px;color:var(--muted)">${r.description || ''}</div>
      <div style="font-size:11px;color:#cbd5e1">
        事件：<span class="code-inline">${(r.events||[]).join(', ')}</span>
      </div>
      <div class="p-foot">
        <span style="font-size:11px;color:var(--muted)">触发 ${r.triggered_count || 0} 次 ${r.last_triggered ? '· ' + r.last_triggered.slice(5) : ''}</span>
        ${r.builtin ? '' : `<button class="btn btn-sm btn-danger" onclick="deleteCustomRule('${r.id}')">删除</button>`}
      </div>
    </div>
  `).join('');
}

async function toggleRule(id, enabled) {
  try {
    await api('/api/rules/' + encodeURIComponent(id) + '/toggle', { method: 'POST', body: JSON.stringify({ enabled }) });
    toast(`规则 ${id} 已${enabled ? '开启' : '关闭'}`);
    await refreshAll();
  } catch (e) { toast('切换失败：' + e.message); }
}

function toggleCustomForm() {
  const f = document.getElementById('customRuleForm');
  f.style.display = f.style.display === 'none' ? 'block' : 'none';
}

async function createCustomRule() {
  try {
    const payload = document.getElementById('crPayload').value.trim();
    const body = {
      name: document.getElementById('crName').value.trim(),
      source: document.getElementById('crSource').value.trim() || '*',
      event_type: document.getElementById('crEvent').value.trim(),
      target_plugin: document.getElementById('crTarget').value.trim(),
      target_action: document.getElementById('crAction').value.trim(),
      payload_template: payload ? JSON.parse(payload) : {},
    };
    if (!body.event_type || !body.target_plugin || !body.target_action) return toast('请填写事件类型、目标插件与目标动作');
    await api('/api/rules/custom', { method: 'POST', body: JSON.stringify(body) });
    toast('自定义联动规则已创建');
    toggleCustomForm();
    await refreshAll();
  } catch (e) { toast('创建失败：' + e.message); }
}

async function deleteCustomRule(id) {
  await api('/api/rules/custom/' + encodeURIComponent(id), { method: 'DELETE' });
  toast('已删除自定义规则');
  await refreshAll();
}

function renderEvents() {
  const kw = (document.getElementById('evFilter').value || '').trim().toLowerCase();
  const rows = STATE.events.filter(e => !kw || (e.event_type || '').toLowerCase().includes(kw) || (e.source || '').toLowerCase().includes(kw));
  document.getElementById('eventBody').innerHTML = rows.length ? rows.map(e => {
    const disp = (e.dispatched || []).map(d =>
      `<span class="badge ${d.ok?'on':'off'}">${d.rule} → ${d.target.replace('astrbot_plugin_','')}.${d.action} (${d.ms}ms)</span>`
    ).join(' ');
    return `<tr>
      <td style="white-space:nowrap;color:var(--muted)">${(e.ts||'').slice(5)}</td>
      <td>${(e.source||'').replace('astrbot_plugin_','')}</td>
      <td><span class="code-inline">${e.event_type}</span></td>
      <td style="max-width:340px;word-break:break-all;font-size:12px;color:#cbd5e1">${JSON.stringify(e.payload || {}).slice(0,180)}</td>
      <td>${disp || '<span style="color:var(--muted);font-size:12px">已记录</span>'}</td>
    </tr>`;
  }).join('') : '<tr><td colspan="5" style="color:var(--muted);text-align:center">暂无跨插件事件</td></tr>';
}

async function emitTestEvent() {
  try {
    await api('/api/events/emit', {
      method: 'POST',
      body: JSON.stringify({
        source: 'astrbot_plugin_fortune',
        event_type: 'fortune.drawn',
        payload: { user_id: 'panel_test', nickname: '面板测试员', score: 92, grade: '大吉', group_id: 'panel_demo' },
      }),
    });
    toast('测试联动事件已派发');
    await refreshAll();
  } catch (e) { toast('派发失败：' + e.message); }
}

async function loadDataPanel(panel, btn) {
  if (btn) {
    btn.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('btn-primary'));
    btn.classList.add('btn-primary');
  }
  const wrap = document.getElementById('dataPanelContent');
  wrap.innerHTML = '<div style="color:var(--muted)">加载数据中...</div>';
  try {
    const res = await api('/api/data/' + panel);
    if (panel === 'points') {
      const lb = res.eco_leaderboard || [];
      wrap.innerHTML = `
        <h3 style="font-size:14px;margin-bottom:10px">🏆 全生态统一积分榜（汇总游戏 / 群统计 / 运势 / 互动）</h3>
        <table><thead><tr><th>排名</th><th>用户</th><th>总积分</th><th>来源明细</th></tr></thead><tbody>
        ${lb.length ? lb.map((u, i) => `<tr><td>#${i+1}</td><td>${u.nickname} (${u.user_id})</td><td><strong>${u.total}</strong></td><td>${JSON.stringify(u.sources||{})}</td></tr>`).join('') : '<tr><td colspan="4" style="color:var(--muted)">暂无积分记录</td></tr>'}
        </tbody></table>`;
    } else if (panel === 'antispam') {
      const bots = res.bot_ids || [];
      wrap.innerHTML = `
        <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;align-items:center;">
          <input type="text" id="newBotId" placeholder="输入 QQ/Bot ID 一键同步全生态">
          <button class="btn btn-primary btn-sm" onclick="markBotEverywhere()">标记为 Bot 并全生态同步</button>
          <span style="font-size:12px;color:var(--muted)">当前共享 Bot 名单：${bots.join(', ') || '空'}</span>
        </div>
        <pre class="json-box">${JSON.stringify(res.plugins, null, 2)}</pre>`;
    } else {
      wrap.innerHTML = `<pre class="json-box">${JSON.stringify(res, null, 2)}</pre>`;
    }
  } catch (e) { wrap.innerHTML = `<div style="color:var(--red)">加载失败：${e.message}</div>`; }
}

async function markBotEverywhere() {
  const bid = (document.getElementById('newBotId').value || '').trim();
  if (!bid) return toast('请输入 Bot ID');
  await api('/api/plugins/astrbot_plugin_anti_flood/action', {
    method: 'POST',
    body: JSON.stringify({ action: 'mark_bot', params: { bot_id: bid } }),
  });
  toast(`已标记 Bot ${bid} 并触发全生态同步`);
  await loadDataPanel('antispam');
  await refreshAll();
}

function populateActionPlugins() {
  const sel = document.getElementById('actPlugin');
  const prev = sel.value;
  const withAct = STATE.plugins.filter(p => p.online && p.actions && p.actions.length);
  sel.innerHTML = withAct.map(p => `<option value="${p.name}">${p.icon} ${p.display_name} (${p.name})</option>`).join('');
  if (prev && withAct.some(p => p.name === prev)) sel.value = prev;
  fillPluginActions();
}

function fillPluginActions() {
  const pname = document.getElementById('actPlugin').value;
  const p = STATE.plugins.find(x => x.name === pname);
  const sel = document.getElementById('actName');
  sel.innerHTML = (p && p.actions ? p.actions : []).map(a => `<option value="${a}">${a}</option>`).join('');
}

function jumpToAction(pname) {
  switchTab('data', document.querySelectorAll('.tab-btn')[2]);
  document.getElementById('actPlugin').value = pname;
  fillPluginActions();
}

async function runQuickAction() {
  const plugin = document.getElementById('actPlugin').value;
  const action = document.getElementById('actName').value;
  if (!plugin || !action) return toast('请选择插件与动作');
  try {
    const params = JSON.parse(document.getElementById('actParams').value || '{}');
    const res = await api('/api/plugins/' + encodeURIComponent(plugin) + '/action', {
      method: 'POST', body: JSON.stringify({ action, params }),
    });
    document.getElementById('actResult').textContent = JSON.stringify(res, null, 2);
    toast(res.ok ? '执行成功' : ('执行失败：' + res.error));
    await refreshAll();
  } catch (e) {
    document.getElementById('actResult').textContent = '错误：' + e.message;
  }
}

function renderConfigSidebar() {
  const list = STATE.plugins.filter(p => p.has_schema);
  document.getElementById('cfgPluginList').innerHTML = list.map(p =>
    `<div class="side-item ${STATE.currentCfgPlugin===p.name?'active':''}" onclick="openPluginConfig('${p.name}')">
      <span>${p.icon} ${p.display_name}</span>
      <span style="font-size:11px">${p.schema_count}</span>
    </div>`
  ).join('');
}

async function openPluginConfig(pname) {
  switchTab('config', document.querySelectorAll('.tab-btn')[3]);
  STATE.currentCfgPlugin = pname;
  renderConfigSidebar();
  try {
    const cfg = await api('/api/plugins/' + encodeURIComponent(pname) + '/config');
    STATE.currentCfgFields = cfg.fields || [];
    document.getElementById('cfgTitle').textContent = `${pname} 配置（${cfg.live ? '实时热更新' : '仅写盘'}）`;
    document.getElementById('cfgSaveBtn').style.display = 'inline-block';
    document.getElementById('cfgFormWrap').innerHTML = STATE.currentCfgFields.map(f => {
      let ctrl = '';
      const id = 'cf_' + f.key;
      if (f.type === 'bool') {
        ctrl = `<label class="switch"><input type="checkbox" id="${id}" ${f.value ? 'checked' : ''}><span class="slider"></span></label>`;
      } else if (f.type === 'int' || f.type === 'float') {
        ctrl = `<input type="number" step="${f.type==='float'?'0.01':'1'}" id="${id}" value="${f.value ?? ''}" style="width:220px">`;
      } else if (f.is_secret) {
        ctrl = `<input type="password" id="${id}" value="${f.value ?? ''}" placeholder="${f.has_value?'保持 ****** 即不修改原密文':'输入密文'}" style="width:100%">`;
      } else if (f.type === 'list') {
        const txt = Array.isArray(f.value) ? f.value.join(', ') : (f.value ?? '');
        ctrl = `<input type="text" id="${id}" value="${String(txt).replace(/"/g,'&quot;')}" placeholder="逗号分隔多项" style="width:100%">`;
      } else {
        ctrl = `<input type="text" id="${id}" value="${String(f.value ?? '').replace(/"/g,'&quot;')}" style="width:100%">`;
      }
      return `<div class="form-row">
        <div class="form-label">
          <strong>${f.key} ${f.is_secret ? '🔒' : ''}</strong>
          <span>${f.description || ''}</span>
          ${f.hint ? `<span style="color:var(--accent)">${f.hint}</span>` : ''}
        </div>
        <div>${ctrl}</div>
      </div>`;
    }).join('');
  } catch (e) { toast('读取配置失败：' + e.message); }
}

async function saveCurrentConfig() {
  if (!STATE.currentCfgPlugin) return;
  const payload = {};
  STATE.currentCfgFields.forEach(f => {
    const el = document.getElementById('cf_' + f.key);
    if (!el) return;
    if (f.type === 'bool') payload[f.key] = el.checked;
    else if (f.type === 'int') payload[f.key] = parseInt(el.value, 10);
    else if (f.type === 'float') payload[f.key] = parseFloat(el.value);
    else payload[f.key] = el.value;
  });
  try {
    const res = await api('/api/plugins/' + encodeURIComponent(STATE.currentCfgPlugin) + '/config', {
      method: 'POST', body: JSON.stringify(payload),
    });
    toast(`保存成功（变更 ${(res.changed_keys||[]).length} 项）`);
    await openPluginConfig(STATE.currentCfgPlugin);
  } catch (e) { toast('保存失败：' + e.message); }
}

refreshAll();
</script>
</body>
</html>
"""
