"""AstrBot 插件生态中枢单页 Web 管理面板（SnowLuma 控制台风格：极简云白/深空双模 + 可折叠图标侧栏，纯静态无外部 CDN）。"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN" class="light" data-density="cozy">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AstrBot 插件生态中枢 · 控制台</title>
<style>
/* ==================== 一、SnowLuma OKLCH 色彩与双模主题变量 ==================== */
:root, html.light {
  --background: oklch(99% 0.004 240);
  --foreground: oklch(20% 0.03 250);
  --card: oklch(100% 0 0);
  --card-soft: oklch(98.8% 0.004 240);
  --card-foreground: oklch(20% 0.03 250);
  --popover: oklch(100% 0 0);
  --sidebar: oklch(98% 0.006 240);
  --sidebar-foreground: oklch(25% 0.025 250);
  --sidebar-border: oklch(92% 0.01 240);
  --sidebar-accent: oklch(94% 0.025 230);
  --sidebar-accent-foreground: oklch(35% 0.08 230);

  --primary: oklch(68.5% 0.155 230);
  --primary-hover: oklch(63% 0.16 230);
  --primary-foreground: oklch(99% 0.005 240);
  --primary-soft: oklch(94.5% 0.032 230);
  --primary-border: oklch(82% 0.08 230);

  --secondary: oklch(96% 0.012 240);
  --muted: oklch(96% 0.012 240);
  --muted-foreground: oklch(50% 0.02 250);
  --accent: oklch(94% 0.03 230);
  --accent-foreground: oklch(35% 0.07 230);

  --border: oklch(92% 0.01 240);
  --border-soft: oklch(94% 0.008 240);
  --input: oklch(90% 0.012 240);
  --ring: oklch(68.5% 0.155 230);

  --success: oklch(62% 0.15 160);
  --success-soft: oklch(94% 0.04 160);
  --success-border: oklch(84% 0.08 160);
  --warning: oklch(68% 0.16 75);
  --warning-soft: oklch(95% 0.05 85);
  --warning-border: oklch(86% 0.09 82);
  --destructive: oklch(58% 0.21 27);
  --destructive-soft: oklch(95% 0.04 27);
  --destructive-border: oklch(86% 0.09 27);
  --purple: oklch(60% 0.17 295);
  --purple-soft: oklch(95% 0.035 295);

  --topbar-bg: oklch(99% 0.004 240 / 0.72);
  --shadow-card: 0 1px 2px oklch(20% 0.03 250 / 0.05), 0 12px 32px -22px oklch(20% 0.03 250 / 0.28);
  --shadow-card-hover: 0 2px 6px oklch(20% 0.03 250 / 0.07), 0 16px 36px -22px oklch(68.5% 0.155 230 / 0.32);
  --shadow-xs: 0 1px 2px oklch(20% 0.03 250 / 0.06);

  --topo-bg: oklch(98.5% 0.006 235);
  --topo-node-fill: oklch(100% 0 0);
  --topo-pill-fill: oklch(100% 0 0 / 0.92);
  --topo-pill-stroke: oklch(89% 0.014 240);
  --topo-pill-text: oklch(26% 0.03 250);
  --topo-radar: oklch(68.5% 0.155 230 / 0.16);

  --radius: 1rem;
  --radius-md: 0.75rem;
  --radius-sm: 0.5rem;
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
  --sidebar-w: 64px;
}

html.dark {
  --background: oklch(16% 0.02 250);
  --foreground: oklch(96% 0.01 240);
  --card: oklch(20% 0.025 250);
  --card-soft: oklch(22% 0.024 250);
  --card-foreground: oklch(96% 0.01 240);
  --popover: oklch(20% 0.025 250);
  --sidebar: oklch(18% 0.022 250);
  --sidebar-foreground: oklch(92% 0.012 240);
  --sidebar-border: oklch(26% 0.02 250);
  --sidebar-accent: oklch(28% 0.05 230);
  --sidebar-accent-foreground: oklch(85% 0.1 230);

  --primary: oklch(75% 0.14 230);
  --primary-hover: oklch(79% 0.13 230);
  --primary-foreground: oklch(15% 0.02 250);
  --primary-soft: oklch(28% 0.055 230);
  --primary-border: oklch(44% 0.09 230);

  --secondary: oklch(25% 0.025 250);
  --muted: oklch(24% 0.02 250);
  --muted-foreground: oklch(68% 0.02 240);
  --accent: oklch(28% 0.05 230);
  --accent-foreground: oklch(85% 0.1 230);

  --border: oklch(28% 0.02 250);
  --border-soft: oklch(25% 0.02 250);
  --input: oklch(30% 0.022 250);
  --ring: oklch(75% 0.14 230);

  --success: oklch(72% 0.15 160);
  --success-soft: oklch(26% 0.05 160);
  --success-border: oklch(40% 0.09 160);
  --warning: oklch(78% 0.15 80);
  --warning-soft: oklch(28% 0.05 78);
  --warning-border: oklch(44% 0.09 78);
  --destructive: oklch(68% 0.19 27);
  --destructive-soft: oklch(27% 0.06 27);
  --destructive-border: oklch(42% 0.11 27);
  --purple: oklch(76% 0.14 295);
  --purple-soft: oklch(28% 0.055 295);

  --topbar-bg: oklch(16% 0.02 250 / 0.72);
  --shadow-card: 0 1px 2px oklch(0% 0 0 / 0.36), 0 16px 38px -24px oklch(0% 0 0 / 0.72), inset 0 1px oklch(100% 0 0 / 0.025);
  --shadow-card-hover: 0 2px 8px oklch(0% 0 0 / 0.44), 0 18px 40px -22px oklch(75% 0.14 230 / 0.25), inset 0 1px oklch(100% 0 0 / 0.04);
  --shadow-xs: 0 1px 2px oklch(0% 0 0 / 0.30);

  --topo-bg: oklch(18% 0.022 250);
  --topo-node-fill: oklch(22% 0.026 250);
  --topo-pill-fill: oklch(18% 0.022 250 / 0.92);
  --topo-pill-stroke: oklch(32% 0.025 250);
  --topo-pill-text: oklch(92% 0.012 240);
  --topo-radar: oklch(75% 0.14 230 / 0.18);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

/* 极简细滚动条 */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: color-mix(in oklab, var(--muted-foreground) 25%, transparent); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: color-mix(in oklab, var(--muted-foreground) 45%, transparent); }
* { scrollbar-width: thin; scrollbar-color: color-mix(in oklab, var(--muted-foreground) 25%, transparent) transparent; }

html, body {
  min-height: 100vh;
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  transition: background-color 0.2s var(--ease), color 0.2s var(--ease);
}

/* ==================== 二、应用壳层：可折叠左侧栏 + 吸顶磨砂顶栏 ==================== */
.app-shell {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  z-index: 45;
  width: 64px;
  background: var(--sidebar);
  color: var(--sidebar-foreground);
  border-right: 1px solid var(--sidebar-border);
  display: flex;
  flex-direction: column;
  transition: width 0.24s var(--ease), box-shadow 0.24s var(--ease);
  overflow: hidden;
  user-select: none;
}
.sidebar:hover,
.sidebar.pinned {
  width: 248px;
}
.sidebar:hover:not(.pinned) {
  box-shadow: 12px 0 36px -18px oklch(20% 0.03 250 / 0.22);
}
html.dark .sidebar:hover:not(.pinned) {
  box-shadow: 12px 0 40px -12px oklch(0% 0 0 / 0.65);
}

.sidebar-brand {
  height: 64px;
  padding: 0 14px;
  display: flex;
  align-items: center;
  gap: 11px;
  flex-shrink: 0;
  border-bottom: 1px solid transparent;
}
.brand-avatar {
  width: 36px; height: 36px;
  border-radius: 999px;
  background: linear-gradient(145deg, color-mix(in oklab, var(--primary) 18%, var(--card)), color-mix(in oklab, var(--primary) 8%, var(--card)));
  border: 1px solid color-mix(in oklab, var(--primary) 28%, transparent);
  color: var(--primary);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 10px -4px color-mix(in oklab, var(--primary) 45%, transparent);
}
.brand-text {
  min-width: 0;
  opacity: 0;
  transform: translateX(-4px);
  transition: opacity 0.18s var(--ease), transform 0.18s var(--ease);
  white-space: nowrap;
}
.sidebar:hover .brand-text,
.sidebar.pinned .brand-text {
  opacity: 1;
  transform: translateX(0);
}
.brand-title-row {
  display: flex; align-items: center; gap: 6px;
}
.brand-title-row strong {
  font-size: 14.5px; font-weight: 700; letter-spacing: -0.015em; color: var(--foreground);
}
.ver-tag {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 999px;
  background: var(--primary-soft);
  color: var(--accent-foreground);
}
.brand-sub {
  font-size: 11px; color: var(--muted-foreground); margin-top: 1px;
}

.sidebar-nav {
  flex: 1;
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
  overflow-x: hidden;
}
.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 44px;
  padding: 9px 13px;
  border: none;
  border-radius: 12px;
  background: transparent;
  color: var(--muted-foreground);
  cursor: pointer;
  text-align: left;
  font-family: var(--font-sans);
  transition: background-color 0.16s var(--ease), color 0.16s var(--ease);
}
.nav-item svg {
  width: 19px; height: 19px;
  flex-shrink: 0;
  transition: color 0.16s var(--ease), transform 0.16s var(--ease);
}
.nav-item:hover {
  background: color-mix(in oklab, var(--sidebar-accent) 55%, transparent);
  color: var(--foreground);
}
.nav-item.active {
  background: var(--sidebar-accent);
  color: var(--sidebar-accent-foreground);
}
.nav-item.active svg {
  color: var(--primary);
}
.nav-label {
  min-width: 0;
  opacity: 0;
  transform: translateX(-4px);
  transition: opacity 0.16s var(--ease), transform 0.16s var(--ease);
  white-space: nowrap;
}
.sidebar:hover .nav-label,
.sidebar.pinned .nav-label {
  opacity: 1;
  transform: translateX(0);
}
.nav-label .nl-main {
  display: block; font-size: 13.5px; font-weight: 600; line-height: 1.25;
}
.nav-label .nl-sub {
  display: block; font-size: 11px; color: var(--muted-foreground); line-height: 1.3; margin-top: 1px;
}

.sidebar-foot {
  padding: 10px 10px 12px;
  border-top: 1px solid var(--sidebar-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-shrink: 0;
}
.foot-copy {
  font-size: 11px;
  color: var(--muted-foreground);
  white-space: nowrap;
  padding-left: 4px;
  opacity: 0;
  transition: opacity 0.16s var(--ease);
}
.sidebar:hover .foot-copy,
.sidebar.pinned .foot-copy { opacity: 1; }

.pin-btn {
  width: 36px; height: 34px;
  border-radius: 9px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--muted-foreground);
  cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  margin-left: auto;
  transition: all 0.16s var(--ease);
}
.pin-btn:hover { background: var(--accent); color: var(--foreground); }
.sidebar.pinned .pin-btn {
  background: var(--primary-soft);
  color: var(--primary);
  border-color: color-mix(in oklab, var(--primary) 25%, transparent);
}

/* 主内容区域跟随侧栏钉住状态平滑让位 */
.main-wrap {
  flex: 1;
  min-width: 0;
  margin-left: 64px;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.24s var(--ease);
}
body.sidebar-pinned .main-wrap {
  margin-left: 248px;
}
@media (max-width: 820px) {
  body.sidebar-pinned .main-wrap { margin-left: 64px; }
}

/* 吸顶半透明磨砂顶栏（复刻 SnowLuma header） */
.topbar {
  position: sticky;
  top: 0;
  z-index: 30;
  height: 64px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--topbar-bg);
  backdrop-filter: blur(20px) saturate(150%);
  -webkit-backdrop-filter: blur(20px) saturate(150%);
  border-bottom: 1px solid color-mix(in oklab, var(--border) 65%, transparent);
}
.top-route {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 0;
}
.top-route-icon {
  color: var(--primary);
  display: inline-flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.top-route h1 {
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--foreground);
  white-space: nowrap;
}
.top-route .route-sub {
  font-size: 12.5px;
  color: var(--muted-foreground);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.top-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: nowrap;
}

/* 状态药丸（复刻 SnowLuma `● 已连接` 实时运行胶囊） */
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 11px;
  border-radius: 999px;
  background: var(--success-soft);
  color: var(--success);
  font-size: 12px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  transition: background-color 0.2s, color 0.2s;
}
.status-pill.offline {
  background: var(--destructive-soft);
  color: var(--destructive);
}
.status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: currentColor;
  animation: softPulse 2s ease-in-out infinite;
  flex-shrink: 0;
}
.status-pill.offline .status-dot { animation: none; }
@keyframes softPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%      { opacity: 0.45; transform: scale(0.82); }
}
.uptime-mono {
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 500;
  opacity: 0.92;
}

.auth-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 11.5px;
  font-weight: 500;
  background: var(--secondary);
  color: var(--muted-foreground);
  border: 1px solid var(--border);
  white-space: nowrap;
}
.auth-pill.secured {
  background: var(--primary-soft);
  color: var(--accent-foreground);
  border-color: var(--primary-border);
}
@media (max-width: 980px) { .auth-pill { display: none; } }

/* 3 段主题切换胶囊（跟随系统 / 浅色 / 深色 — 1:1 复刻 SnowLuma 右上角） */
.theme-switcher {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 3px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: color-mix(in oklab, var(--card) 75%, transparent);
  box-shadow: var(--shadow-xs);
}
.theme-btn {
  width: 30px; height: 30px;
  border-radius: 999px;
  border: none;
  background: transparent;
  color: var(--muted-foreground);
  cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center;
  transition: all 0.18s var(--ease);
}
.theme-btn:hover { color: var(--foreground); background: var(--secondary); }
.theme-btn.active {
  background: var(--primary);
  color: var(--primary-foreground);
  box-shadow: 0 2px 8px -2px color-mix(in oklab, var(--primary) 65%, transparent);
}

.ghost-icon-btn {
  width: 36px; height: 36px;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--muted-foreground);
  cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center;
  transition: all 0.16s var(--ease);
}
.ghost-icon-btn:hover { background: var(--accent); color: var(--foreground); }
.ghost-icon-btn.danger:hover { background: var(--destructive-soft); color: var(--destructive); }
.spin-once { animation: spin360 0.55s var(--ease); }
@keyframes spin360 { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* ==================== 三、内容主区与 SnowLuma 核心卡片规范 ==================== */
.content {
  width: 100%;
  max-width: 1520px;
  margin: 0 auto;
  padding: 20px 28px 64px;
}
@media (max-width: 720px) { .content { padding: 16px 14px 48px; } }

.section { display: none; animation: fadeIn 0.22s var(--ease); }
.section.active { display: block; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

.ui-card {
  background: var(--card);
  color: var(--card-foreground);
  border: 1px solid color-mix(in oklab, var(--border) 80%, transparent);
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  padding: 20px 22px;
  margin-bottom: 18px;
  transition: border-color 0.2s var(--ease), box-shadow 0.2s var(--ease);
}
.card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}
.card-title-wrap { min-width: 0; }
.card-title {
  font-size: 15.5px;
  font-weight: 600;
  letter-spacing: -0.015em;
  color: var(--foreground);
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-title svg { color: var(--primary); flex-shrink: 0; }
.card-desc {
  font-size: 12.5px;
  color: var(--muted-foreground);
  margin-top: 3px;
}

/* 顶部操作行 + 淡天空蓝提示/生态横幅（复刻 SnowLuma CTA Banner） */
.overview-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.cta-banner {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 13px 18px;
  margin-bottom: 16px;
  border-radius: var(--radius);
  border: 1px solid color-mix(in oklab, var(--primary) 34%, transparent);
  background: color-mix(in oklab, var(--primary) 6.5%, var(--card));
  cursor: pointer;
  transition: background-color 0.18s var(--ease), border-color 0.18s var(--ease);
}
.cta-banner:hover {
  background: color-mix(in oklab, var(--primary) 11%, var(--card));
  border-color: color-mix(in oklab, var(--primary) 48%, transparent);
}
.cta-icon {
  width: 36px; height: 36px;
  border-radius: 999px;
  background: color-mix(in oklab, var(--primary) 16%, transparent);
  color: var(--primary);
  display: inline-flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.cta-text { flex: 1; min-width: 0; }
.cta-text strong { display: block; font-size: 13.5px; font-weight: 600; color: var(--foreground); }
.cta-text span { display: block; font-size: 12px; color: var(--muted-foreground); margin-top: 1px; }
.cta-arrow { color: var(--primary); flex-shrink: 0; }

/* 5 列 SnowLuma KPI 指标卡（左侧 40px 圆角图标块 + 右侧三行数据） */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}
@media (max-width: 1220px) { .kpi-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 760px)  { .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 480px)  { .kpi-grid { grid-template-columns: 1fr; } }

.kpi-card {
  background: var(--card);
  border: 1px solid color-mix(in oklab, var(--border) 80%, transparent);
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  padding: 15px 16px;
  display: flex;
  align-items: center;
  gap: 13px;
  min-width: 0;
  cursor: pointer;
  transition: border-color 0.18s var(--ease), background-color 0.18s var(--ease), transform 0.18s var(--ease);
}
.kpi-card:hover {
  border-color: color-mix(in oklab, var(--primary) 42%, transparent);
  background: color-mix(in oklab, var(--accent) 26%, var(--card));
  transform: translateY(-1px);
}
.kpi-icon {
  width: 42px; height: 42px;
  border-radius: 12px;
  background: color-mix(in oklab, var(--primary) 12%, transparent);
  color: var(--primary);
  display: inline-flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.kpi-icon.solid {
  border-radius: 999px;
  background: var(--primary);
  color: var(--primary-foreground);
  box-shadow: 0 4px 14px -4px color-mix(in oklab, var(--primary) 70%, transparent);
}
.kpi-body { min-width: 0; flex: 1; }
.kpi-label {
  font-size: 11.5px;
  font-weight: 500;
  color: var(--muted-foreground);
  letter-spacing: 0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.kpi-val {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.25;
  margin-top: 2px;
  color: var(--foreground);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.kpi-val .denom {
  font-size: 13px; font-weight: 500; color: var(--muted-foreground); margin-left: 2px;
}
.kpi-sub {
  font-size: 11.5px;
  color: var(--muted-foreground);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 总览双列网格（左：生态联动拓扑 / 右：最近跨插件事件，复刻 SnowLuma 双卡结构） */
.overview-two-col {
  display: grid;
  grid-template-columns: 1.55fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}
@media (max-width: 1120px) { .overview-two-col { grid-template-columns: 1fr; } }
.overview-two-col .ui-card { margin-bottom: 0; display: flex; flex-direction: column; }

/* SnowLuma 虚线空态容器 */
.empty-inset {
  flex: 1;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 32px 16px;
  border-radius: var(--radius-md);
  border: 1px dashed var(--border);
  color: var(--muted-foreground);
  text-align: center;
}
.empty-inset svg { opacity: 0.4; }
.empty-inset span { font-size: 13px; }

.recent-ev-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.recent-ev-item {
  padding: 10px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-soft);
  background: var(--card-soft);
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.recent-ev-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

/* ==================== 四、按钮、表单、徽章与开关（1:1 SnowLuma） ==================== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 36px;
  padding: 0 14px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--foreground);
  cursor: pointer;
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 500;
  box-shadow: var(--shadow-xs);
  transition: all 0.16s var(--ease);
  white-space: nowrap;
}
.btn:hover { background: var(--accent); border-color: color-mix(in oklab, var(--primary) 35%, var(--border)); color: var(--accent-foreground); }
.btn:active { transform: scale(0.97); }
.btn-primary {
  background: var(--primary);
  border-color: var(--primary);
  color: var(--primary-foreground);
  box-shadow: 0 2px 10px -3px color-mix(in oklab, var(--primary) 60%, transparent);
}
.btn-primary:hover {
  background: var(--primary-hover);
  border-color: var(--primary-hover);
  color: var(--primary-foreground);
}
.btn-danger {
  background: var(--destructive-soft);
  border-color: var(--destructive-border);
  color: var(--destructive);
  box-shadow: none;
}
.btn-danger:hover {
  background: var(--destructive);
  border-color: var(--destructive);
  color: #fff;
}
.btn-ghost {
  background: transparent;
  border-color: transparent;
  box-shadow: none;
  color: var(--muted-foreground);
}
.btn-ghost:hover { background: var(--accent); color: var(--foreground); border-color: transparent; }
.btn-sm { height: 30px; padding: 0 11px; font-size: 12px; border-radius: 8px; }
.btn-icon { width: 30px; height: 30px; padding: 0; border-radius: 8px; }

.link-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border: none;
  background: transparent;
  color: var(--muted-foreground);
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 6px;
  transition: color 0.15s, background-color 0.15s;
}
.link-btn:hover { color: var(--primary); background: var(--primary-soft); }

input[type="text"], input[type="password"], input[type="number"], select, textarea {
  height: 36px;
  background: var(--card);
  color: var(--foreground);
  border: 1px solid var(--input);
  border-radius: 9px;
  padding: 0 12px;
  font-family: var(--font-sans);
  font-size: 13px;
  outline: none;
  transition: border-color 0.16s var(--ease), box-shadow 0.16s var(--ease);
}
textarea { height: auto; min-height: 92px; padding: 10px 12px; font-family: var(--font-mono); font-size: 12px; }
input::placeholder, textarea::placeholder { color: var(--muted-foreground); opacity: 0.75; }
select { cursor: pointer; }
input:focus, select:focus, textarea:focus {
  border-color: var(--ring);
  box-shadow: 0 0 0 3px color-mix(in oklab, var(--ring) 22%, transparent);
}
.filter-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }

.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 999px;
  white-space: nowrap;
}
.badge.on { background: var(--success-soft); color: var(--success); }
.badge.on::before { content: ""; width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
.badge.off { background: var(--destructive-soft); color: var(--destructive); }
.badge.proto {
  background: var(--primary-soft);
  color: var(--accent-foreground);
  font-family: var(--font-mono);
  font-size: 10.5px;
}

.switch { position: relative; display: inline-block; width: 42px; height: 24px; flex-shrink: 0; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; inset: 0;
  background: color-mix(in oklab, var(--foreground) 18%, transparent);
  border-radius: 999px;
  transition: background-color 0.2s var(--ease);
}
.slider:before {
  content: ""; position: absolute;
  height: 18px; width: 18px; left: 3px; bottom: 3px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.24);
  transition: transform 0.2s var(--ease);
}
input:checked + .slider { background: var(--primary); }
input:checked + .slider:before { transform: translateX(18px); }

/* ==================== 五、生态联动拓扑图（适配浅色/深色双模） ==================== */
.topo-toolbar { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.topo-legends { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.legend-pill {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 9px; border-radius: 999px;
  font-size: 11px; font-weight: 500; color: var(--muted-foreground);
  background: var(--secondary); border: 1px solid var(--border-soft);
}
.legend-dot { width: 7px; height: 7px; border-radius: 50%; }
.topo-zoom-group {
  display: inline-flex; align-items: center; gap: 3px;
  padding: 2px; border-radius: 9px;
  background: var(--secondary); border: 1px solid var(--border);
}
.topo-wrap {
  position: relative;
  width: 100%;
  height: 410px;
  border-radius: var(--radius-md);
  background: var(--topo-bg);
  border: 1px solid var(--border-soft);
  overflow: hidden;
  cursor: grab;
  user-select: none;
}
.topo-wrap.dragging { cursor: grabbing; }
svg.topo { width: 100%; height: 100%; display: block; }
.topo-hint {
  position: absolute; left: 12px; bottom: 10px;
  font-size: 11px; color: var(--muted-foreground);
  background: var(--topo-pill-fill);
  border: 1px solid var(--border-soft);
  padding: 3px 9px; border-radius: 999px;
  pointer-events: none;
}
.topo-tooltip {
  position: absolute; top: 10px; left: 12px; z-index: 5;
  pointer-events: none; opacity: 0; transform: translateY(-4px);
  transition: opacity 0.16s var(--ease), transform 0.16s var(--ease);
  background: var(--popover);
  border: 1px solid var(--primary-border);
  box-shadow: var(--shadow-card);
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 12px;
  color: var(--foreground);
}
.topo-tooltip.show { opacity: 1; transform: translateY(0); }

.topo-radar { transform-origin: 600px 270px; animation: slowSpin 95s linear infinite; }
.topo-radar-rev { transform-origin: 600px 270px; animation: slowSpin 135s linear infinite reverse; }
@keyframes slowSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.topo-edge-base {
  fill: none; stroke-width: 1.4; stroke-opacity: 0.22;
  transition: stroke-opacity 0.2s var(--ease), stroke-width 0.2s var(--ease);
}
.topo-edge-flow {
  fill: none; stroke-width: 1.6; stroke-opacity: 0.42;
  stroke-dasharray: 4 18;
  animation: flowDash 3.6s linear infinite;
  transition: stroke-opacity 0.2s var(--ease), stroke-width 0.2s var(--ease);
}
@keyframes flowDash { from { stroke-dashoffset: 44; } to { stroke-dashoffset: 0; } }
.topo-node { cursor: pointer; transition: opacity 0.2s var(--ease); }

svg.topo.has-hover .topo-node { opacity: 0.18 !important; }
svg.topo.has-hover .topo-node.hi { opacity: 1 !important; }
svg.topo.has-hover .topo-edge-base { stroke-opacity: 0.05; }
svg.topo.has-hover .topo-edge-flow { stroke-opacity: 0.04; }
svg.topo.has-hover .topo-edge-base.hi { stroke-opacity: 0.65; stroke-width: 2.1; }
svg.topo.has-hover .topo-edge-flow.hi { stroke-opacity: 0.95; stroke-width: 2.3; animation-duration: 1.4s; }

/* ==================== 六、插件全景卡片、规则、日志表格与子标签 ==================== */
.plugin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(305px, 1fr));
  gap: 14px;
}
.p-card, .rule-card {
  background: var(--card-soft);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px 17px;
  display: flex;
  flex-direction: column;
  gap: 9px;
  transition: border-color 0.18s var(--ease), background-color 0.18s var(--ease), box-shadow 0.18s var(--ease);
}
.p-card:hover, .rule-card:hover {
  border-color: color-mix(in oklab, var(--primary) 42%, transparent);
  background: var(--card);
  box-shadow: var(--shadow-card-hover);
}
.p-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.p-title {
  font-weight: 600; font-size: 14px; color: var(--foreground);
  display: flex; align-items: center; gap: 8px; min-width: 0;
}
.p-icon-tile {
  width: 28px; height: 28px;
  border-radius: 8px;
  background: var(--primary-soft);
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 14px; flex-shrink: 0;
}
.p-badges { display: flex; gap: 5px; flex-shrink: 0; align-items: center; }
.p-meta {
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: var(--muted-foreground);
  font-variant-numeric: tabular-nums;
}
.p-desc {
  font-size: 12.5px;
  line-height: 1.58;
  color: var(--muted-foreground);
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  min-height: 39px;
}
.metrics { display: flex; flex-wrap: wrap; gap: 6px; }
.metric-chip {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 11px; padding: 3px 8px; border-radius: 7px;
  background: var(--secondary); border: 1px solid var(--border-soft);
}
.metric-chip .mk { color: var(--muted-foreground); }
.metric-chip .mv { color: var(--foreground); font-family: var(--font-mono); font-weight: 600; font-variant-numeric: tabular-nums; }
.metric-chip.empty { color: var(--muted-foreground); opacity: 0.7; }
.p-foot {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: auto; padding-top: 10px;
  border-top: 1px solid var(--border-soft);
}
.p-foot-meta {
  font-family: var(--font-mono); font-size: 11px; color: var(--muted-foreground); font-variant-numeric: tabular-nums;
}

.rule-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(345px, 1fr)); gap: 14px; }
.custom-form-box {
  display: none;
  background: var(--card-soft);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 15px;
  margin-bottom: 16px;
}

table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td {
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border-soft);
  vertical-align: top;
}
th {
  color: var(--muted-foreground);
  font-weight: 600;
  font-size: 11.5px;
  letter-spacing: 0.02em;
  background: var(--card-soft);
}
tbody tr:hover { background: color-mix(in oklab, var(--accent) 30%, transparent); }

/* SnowLuma 下划线 + 浅底标签（复刻 /debug 页签） */
.underline-tabs {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  border-bottom: 1px solid var(--border);
  margin-bottom: 16px;
}
.u-tab {
  position: relative;
  min-height: 40px;
  padding: 8px 14px;
  border: none;
  border-radius: 10px 10px 0 0;
  background: transparent;
  color: var(--muted-foreground);
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.16s var(--ease);
}
.u-tab:hover { color: var(--foreground); background: var(--secondary); }
.u-tab.active {
  color: var(--primary);
  background: color-mix(in oklab, var(--primary) 6%, transparent);
  font-weight: 600;
}
.u-tab.active::after {
  content: "";
  position: absolute; left: 8px; right: 8px; bottom: -1px;
  height: 2px; border-radius: 2px; background: var(--primary);
}

.warn-banner {
  display: flex; align-items: center; gap: 9px;
  padding: 10px 14px; margin-bottom: 14px;
  border-radius: var(--radius-md);
  background: var(--warning-soft);
  border: 1px solid var(--warning-border);
  color: var(--warning);
  font-size: 12.5px;
}

.split-layout { display: grid; grid-template-columns: 248px 1fr; gap: 18px; }
@media (max-width: 860px) { .split-layout { grid-template-columns: 1fr; } }
.side-rail {
  border: 1px solid var(--border);
  background: var(--card-soft);
  border-radius: var(--radius-md);
  padding: 6px;
  display: flex; flex-direction: column; gap: 3px;
  max-height: 70vh; overflow-y: auto;
}
.side-item {
  padding: 9px 11px; border-radius: 9px; cursor: pointer; font-size: 13px;
  display: flex; justify-content: space-between; align-items: center;
  color: var(--muted-foreground);
  border: 1px solid transparent;
  transition: all 0.15s var(--ease);
}
.side-item:hover { background: var(--secondary); color: var(--foreground); }
.side-item.active {
  background: var(--accent);
  color: var(--accent-foreground);
  border-color: color-mix(in oklab, var(--primary) 26%, transparent);
  font-weight: 600;
}
.side-count {
  font-family: var(--font-mono); font-size: 11px;
  padding: 1px 7px; border-radius: 999px;
  background: var(--card); color: var(--muted-foreground);
  border: 1px solid var(--border-soft);
}

.form-row {
  display: grid; grid-template-columns: 245px 1fr; gap: 14px; align-items: start;
  padding: 14px 0; border-bottom: 1px solid var(--border-soft);
}
@media (max-width: 720px) { .form-row { grid-template-columns: 1fr; } }
.form-label strong { font-family: var(--font-mono); font-size: 12.5px; display: block; color: var(--foreground); }
.form-label span { font-size: 12px; color: var(--muted-foreground); display: block; margin-top: 3px; line-height: 1.5; }

.action-bar-grid {
  display: grid; grid-template-columns: 240px 200px 1fr auto; gap: 10px; align-items: center; margin-bottom: 12px;
}
@media (max-width: 900px) { .action-bar-grid { grid-template-columns: 1fr; } }

pre.json-box {
  background: var(--card-soft);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  overflow: auto; max-height: 380px;
  font-size: 12px; line-height: 1.6;
  color: var(--foreground);
  font-family: var(--font-mono);
}
.code-inline {
  font-family: var(--font-mono);
  background: var(--primary-soft);
  color: var(--accent-foreground);
  padding: 2px 7px; border-radius: 6px; font-size: 11.5px;
}

.toast {
  position: fixed; right: 24px; bottom: 24px; z-index: 90;
  background: var(--popover);
  border: 1px solid var(--primary-border);
  color: var(--foreground);
  padding: 11px 16px; border-radius: 12px; font-size: 13px; font-weight: 500;
  display: none;
  box-shadow: var(--shadow-card-hover);
}

/* SnowLuma 等高线登录弹层 */
.modal-bg {
  position: fixed; inset: 0; z-index: 80;
  background: color-mix(in oklab, var(--background) 84%, transparent);
  backdrop-filter: blur(12px);
  display: none; align-items: center; justify-content: center; padding: 20px;
}
.modal-waves {
  position: absolute; inset: 0; pointer-events: none; opacity: 0.45; overflow: hidden;
}
.modal-card {
  position: relative; z-index: 1;
  background: var(--card);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-card-hover);
  border-radius: var(--radius);
  padding: 28px;
  width: 100%; max-width: 446px;
}
.modal-card h3 { margin-bottom: 8px; font-size: 18px; font-weight: 700; letter-spacing: -0.015em; }
.modal-card p { font-size: 13px; color: var(--muted-foreground); margin-bottom: 18px; line-height: 1.65; }
</style>
</head>
<body>

<div class="app-shell">
  <!-- 左侧可折叠图标侧栏（复刻 SnowLuma Sidebar） -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-brand">
      <div class="brand-avatar" aria-hidden="true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 3a14.5 14.5 0 0 0 0 18 14.5 14.5 0 0 0 0-18"/><path d="M3 12h18"/></svg>
      </div>
      <div class="brand-text">
        <div class="brand-title-row">
          <strong>AstrBot Hub</strong>
          <span class="ver-tag" id="hubVerTag">v1.2</span>
        </div>
        <div class="brand-sub">插件生态中枢控制台</div>
      </div>
    </div>

    <nav class="sidebar-nav" role="tablist">
      <button class="nav-item active" data-tab="dashboard" onclick="switchTab('dashboard', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1.5"/><rect width="7" height="7" x="14" y="3" rx="1.5"/><rect width="7" height="7" x="14" y="14" rx="1.5"/><rect width="7" height="7" x="3" y="14" rx="1.5"/></svg>
        <span class="nav-label"><span class="nl-main">总览</span><span class="nl-sub">生态全景与联动拓扑</span></span>
      </button>
      <button class="nav-item" data-tab="rules" onclick="switchTab('rules', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/></svg>
        <span class="nav-label"><span class="nl-main">联动管线</span><span class="nl-sub">内置与自定义规则</span></span>
      </button>
      <button class="nav-item" data-tab="events" onclick="switchTab('events', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>
        <span class="nav-label"><span class="nl-main">事件日志</span><span class="nl-sub">跨插件实时事件流</span></span>
      </button>
      <button class="nav-item" data-tab="data" onclick="switchTab('data', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/></svg>
        <span class="nav-label"><span class="nl-main">聚合数据</span><span class="nl-sub">记忆 / 积分 / 运维视图</span></span>
      </button>
      <button class="nav-item" data-tab="config" onclick="switchTab('config', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="16" x2="16" y1="18" y2="22"/></svg>
        <span class="nav-label"><span class="nl-main">插件配置</span><span class="nl-sub">Schema 在线热更新</span></span>
      </button>
      <button class="nav-item" data-tab="debug" onclick="switchTab('debug', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/><path d="M12 20v-9"/><path d="M6.53 9C4.6 8.8 3 7.1 3 5"/><path d="M6 13H2"/><path d="M3 21c0-2.1 1.7-3.9 3.8-4"/><path d="M20.97 5c0 2.1-1.6 3.8-3.5 4"/><path d="M22 13h-4"/><path d="M17.2 17c2.1.1 3.8 1.9 3.8 4"/></svg>
        <span class="nav-label"><span class="nl-main">调试台</span><span class="nl-sub">hub_action 动作触发器</span></span>
      </button>
    </nav>

    <div class="sidebar-foot">
      <span class="foot-copy">© 2026 AstrBot Hub</span>
      <button class="pin-btn" id="pinSidebarBtn" onclick="toggleSidebarPin()" title="钉住 / 取消钉住侧栏">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="17" y2="22"/><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/></svg>
      </button>
    </div>
  </aside>

  <!-- 右侧主视图：吸顶顶栏 + 内容区 -->
  <div class="main-wrap">
    <header class="topbar">
      <div class="top-route">
        <span class="top-route-icon" id="topRouteIcon">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1.5"/><rect width="7" height="7" x="14" y="3" rx="1.5"/><rect width="7" height="7" x="14" y="14" rx="1.5"/><rect width="7" height="7" x="3" y="14" rx="1.5"/></svg>
        </span>
        <h1 id="topRouteTitle">总览</h1>
        <span class="route-sub" id="topRouteSub">AstrBot 插件生态中枢 · 实时运行状态</span>
      </div>

      <div class="top-right">
        <span class="status-pill" id="statusPill" title="服务端监听与实时运行时间">
          <span class="status-dot" id="statusDot"></span>
          <span id="statusText">已连接</span>
          <span class="uptime-mono" id="subInfo">--</span>
        </span>
        <span class="auth-pill" id="authBadge">检测中</span>

        <!-- SnowLuma 风格 3 段主题切换（跟随系统 / 浅色 / 深色） -->
        <div class="theme-switcher" role="group" aria-label="主题切换">
          <button class="theme-btn" id="th-system" onclick="setTheme('system')" title="跟随系统">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>
          </button>
          <button class="theme-btn" id="th-light" onclick="setTheme('light')" title="浅色模式">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
          </button>
          <button class="theme-btn" id="th-dark" onclick="setTheme('dark')" title="深色模式">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
          </button>
        </div>

        <button class="ghost-icon-btn" id="refreshBtn" onclick="refreshAll(true)" title="立即刷新">
          <svg id="refreshIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.64-6.36"/><polyline points="21 3 21 9 15 9"/></svg>
        </button>
        <button class="ghost-icon-btn danger" id="logoutBtn" style="display:none" onclick="doLogout()" title="退出登录">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>
        </button>
      </div>
    </header>

    <main class="content">
      <!-- ==================== ROUTE 1: 总览 ==================== -->
      <section id="tab-dashboard" class="section active">
        <div class="cta-banner" id="ecoBanner" onclick="switchTab('rules')">
          <span class="cta-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/></svg>
          </span>
          <div class="cta-text">
            <strong id="bannerTitle">AstrBot 插件生态中枢运行中</strong>
            <span id="bannerSub">前往「联动管线」查看或调整 10 条内置自动化联动规则与自定义工作流。</span>
          </div>
          <svg class="cta-arrow" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
        </div>

        <div class="kpi-grid" id="kpiGrid"></div>

        <!-- 双列核心模块：左侧联动拓扑，右侧最近跨插件事件 -->
        <div class="overview-two-col">
          <div class="ui-card">
            <div class="card-head">
              <div class="card-title-wrap">
                <div class="card-title">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M14.2 9.8 17.5 6.5"/><path d="M6.5 17.5 9.8 14.2"/><path d="M9.8 9.8 6.5 6.5"/><path d="M17.5 17.5 14.2 14.2"/></svg>
                  <span>全生态插件联动拓扑</span>
                </div>
                <div class="card-desc">各生态插件节点连接关系与实时联动流向（点击节点可直达配置）</div>
              </div>
              <div class="topo-toolbar">
                <div class="topo-legends">
                  <span class="legend-pill"><span class="legend-dot" style="background:#0ea5e9"></span>效率</span>
                  <span class="legend-pill"><span class="legend-dot" style="background:#10b981"></span>防扰</span>
                  <span class="legend-pill"><span class="legend-dot" style="background:#f59e0b"></span>运维</span>
                  <span class="legend-pill"><span class="legend-dot" style="background:#a855f7"></span>娱乐</span>
                </div>
                <div class="topo-zoom-group" title="缩放与平移画布">
                  <button class="btn btn-icon btn-ghost" onclick="topoZoom(1.18)" aria-label="放大">+</button>
                  <button class="btn btn-icon btn-ghost" onclick="topoZoom(1/1.18)" aria-label="缩小">−</button>
                  <button class="btn btn-sm btn-ghost" onclick="topoResetView()">重置</button>
                </div>
              </div>
            </div>
            <div class="topo-wrap" id="topoWrap">
              <div class="topo-tooltip" id="topoTooltip"></div>
              <svg class="topo" id="topoSvg" viewBox="0 0 1200 540" preserveAspectRatio="xMidYMid meet"></svg>
              <div class="topo-hint">悬停聚焦关联链路 · 滚轮缩放 / 拖拽画布</div>
            </div>
          </div>

          <div class="ui-card">
            <div class="card-head">
              <div class="card-title-wrap">
                <div class="card-title">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
                  <span>最近联动动态</span>
                </div>
                <div class="card-desc">最近 6 条跨插件事件与自动派发记录</div>
              </div>
              <button class="link-btn" onclick="switchTab('events')">查看日志 →</button>
            </div>
            <div id="recentEventsPreview" style="flex:1;display:flex;flex-direction:column;"></div>
          </div>
        </div>

        <!-- 插件运行全景（复刻 SnowLuma 主机资源宽卡） -->
        <div class="ui-card">
          <div class="card-head">
            <div class="card-title-wrap">
              <div class="card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/></svg>
                <span>插件运行全景</span>
              </div>
              <div class="card-desc" id="pluginPanoramaDesc">已发现插件状态、协议版本、运行指标与快捷入口</div>
            </div>
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
              <input type="text" id="pluginSearch" placeholder="搜索插件名 / 说明..." style="min-width:210px" oninput="renderPlugins()">
              <button class="btn btn-sm" onclick="refreshAll(true)">刷新</button>
            </div>
          </div>
          <div class="plugin-grid" id="pluginGrid"></div>
        </div>
      </section>

      <!-- ==================== ROUTE 2: 联动管线 ==================== -->
      <section id="tab-rules" class="section">
        <div class="ui-card">
          <div class="card-head">
            <div class="card-title-wrap">
              <div class="card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                <span>自动化联动管线</span>
              </div>
              <div class="card-desc">内置 13 条跨插件联动规则 + 自定义触发管线，开关实时生效</div>
            </div>
            <div class="filter-row">
              <button class="btn btn-sm" onclick="emitTestEvent()">发送测试事件</button>
              <button class="btn btn-primary btn-sm" onclick="toggleCustomForm()">+ 新建自定义规则</button>
            </div>
          </div>
          <div id="customRuleForm" class="custom-form-box">
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:10px;">
              <input type="text" id="crName" placeholder="规则名称（如 运势通知备忘）">
              <input type="text" id="crSource" placeholder="源插件（如 astrbot_plugin_fortune 或 *）">
              <input type="text" id="crEvent" placeholder="事件类型（如 fortune.drawn 或 *）">
              <input type="text" id="crTarget" placeholder="目标插件（如 astrbot_plugin_chat_digest）">
              <input type="text" id="crAction" placeholder="目标动作（如 add_highlight）">
            </div>
            <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
              <input type="text" id="crPayload" style="flex:1;min-width:260px;font-family:var(--font-mono);font-size:12px" placeholder='附加参数 JSON（可选，如 {"tags":["自定义"]}）'>
              <button class="btn btn-primary btn-sm" onclick="createCustomRule()">保存规则</button>
            </div>
          </div>
          <div class="rule-grid" id="ruleGrid"></div>
        </div>
      </section>

      <!-- ==================== ROUTE 3: 事件日志 ==================== -->
      <section id="tab-events" class="section">
        <div class="ui-card">
          <div class="card-head">
            <div class="card-title-wrap">
              <div class="card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>
                <span>实时跨插件事件流</span>
              </div>
              <div class="card-desc">每 15 秒自动同步最新总线事件与联动目标执行耗时</div>
            </div>
            <div class="filter-row">
              <input type="text" id="evFilter" placeholder="按事件类型或源插件过滤..." style="min-width:220px" oninput="renderEvents()">
              <button class="btn btn-sm" onclick="emitTestEvent()">派发测试联动事件</button>
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

      <!-- ==================== ROUTE 4: 聚合数据 ==================== -->
      <section id="tab-data" class="section">
        <div class="ui-card">
          <div class="card-head">
            <div class="card-title-wrap">
              <div class="card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/></svg>
                <span>跨插件聚合数据视图</span>
              </div>
              <div class="card-desc">一站式检视群聊记忆、备忘提醒、防扰安全、统一积分榜与运维状态</div>
            </div>
          </div>
          <div class="underline-tabs">
            <button class="u-tab active" onclick="loadDataPanel('digest', this)">📝 群聊记忆</button>
            <button class="u-tab" onclick="loadDataPanel('memo', this)">⏰ 备忘提醒</button>
            <button class="u-tab" onclick="loadDataPanel('antispam', this)">🛡️ 防扰安全</button>
            <button class="u-tab" onclick="loadDataPanel('points', this)">🏆 生态积分榜</button>
            <button class="u-tab" onclick="loadDataPanel('ops', this)">🚀 运维监控</button>
            <button class="u-tab" onclick="loadDataPanel('tools', this)">🧰 工具与指令</button>
          </div>
          <div id="dataPanelContent"></div>
        </div>
      </section>

      <!-- ==================== ROUTE 5: 插件配置 ==================== -->
      <section id="tab-config" class="section">
        <div class="ui-card">
          <div class="card-head">
            <div class="card-title-wrap">
              <div class="card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/></svg>
                <span>全插件在线配置编辑器</span>
              </div>
              <div class="card-desc">自动解析 _conf_schema.json，支持敏感字段自动脱敏保护与实时热更新</div>
            </div>
          </div>
          <div class="split-layout">
            <div class="side-rail" id="cfgPluginList"></div>
            <div>
              <div class="card-head" style="margin-bottom:10px">
                <div class="card-title" id="cfgTitle">请选择左侧插件</div>
                <button class="btn btn-primary btn-sm" id="cfgSaveBtn" style="display:none" onclick="saveCurrentConfig()">保存并热更新</button>
              </div>
              <div id="cfgFormWrap" style="color:var(--muted-foreground);font-size:13px;">点击左侧插件查看并编辑其配置项。</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== ROUTE 6: 调试台 ==================== -->
      <section id="tab-debug" class="section">
        <div class="ui-card">
          <div class="card-head">
            <div class="card-title-wrap">
              <div class="card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/></svg>
                <span>快捷跨插件动作调试台（hub_action）</span>
              </div>
              <div class="card-desc">直接调用任意已接入协议的在线插件动作并检视 JSON 响应</div>
            </div>
          </div>
          <div class="warn-banner">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
            <span>调试动作将直接作用于实时运行中的插件实例（如写入备忘、同步 Bot 或发送邮件），请核对 JSON 参数后执行。</span>
          </div>
          <div class="action-bar-grid">
            <select id="actPlugin" onchange="fillPluginActions()"></select>
            <select id="actName"></select>
            <input type="text" id="actParams" style="font-family:var(--font-mono);font-size:12px" placeholder='JSON 参数，例如 {"umo":"default:GroupMessage:1001","content":"测试备忘"}' value="{}">
            <button class="btn btn-primary" onclick="runQuickAction()">执行动作</button>
          </div>
          <pre class="json-box" id="actResult">等待执行...</pre>
        </div>
      </section>
    </main>
  </div>
</div>

<!-- SnowLuma 风格等高线登录弹层 -->
<div class="modal-bg" id="loginModal">
  <svg class="modal-waves" viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <g fill="none" stroke="var(--primary)" stroke-opacity="0.26" stroke-width="1.2">
      <path d="M-80 120 C 260 20, 520 260, 860 140 C 1050 70, 1180 180, 1300 120"/>
      <path d="M-80 210 C 240 120, 540 340, 880 220 C 1060 155, 1180 260, 1300 200"/>
      <path d="M-80 320 C 260 220, 520 440, 860 330 C 1060 260, 1190 360, 1300 300"/>
      <path d="M-80 440 C 280 350, 540 540, 900 440 C 1080 390, 1190 470, 1300 420"/>
      <path d="M-80 560 C 300 480, 580 650, 920 550 C 1090 500, 1200 570, 1300 540"/>
    </g>
  </svg>
  <div class="modal-card">
    <div style="display:flex;align-items:center;gap:11px;margin-bottom:14px;">
      <div class="brand-avatar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      </div>
      <div>
        <h3 style="margin:0">AstrBot 插件生态中枢</h3>
        <div style="font-size:12px;color:var(--muted-foreground)">管理员身份验证</div>
      </div>
    </div>
    <p>当前面板已启用 Token 访问控制。请输入配置中的 <span class="code-inline">web_token</span> 或自动生成的管理员令牌（可在私聊中发送 <span class="code-inline">/中枢 面板</span> 查看）。</p>
    <input type="password" id="loginToken" style="width:100%;height:44px;border-radius:12px;margin-bottom:14px" placeholder="请输入管理员 Token" onkeydown="if(event.key==='Enter')doLogin()">
    <button class="btn btn-primary" style="width:100%;height:44px;border-radius:12px;font-size:14.5px" onclick="doLogin()">登录控制台</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let STATE = { overview: null, plugins: [], rules: [], events: [], currentCfgPlugin: null, currentCfgFields: [] };
let TOPO_VIEW = { scale: 1, tx: 0, ty: 0, dragging: false, startX: 0, startY: 0, origTx: 0, origTy: 0 };
let TOPO_META = { nodes: {}, adj: {} };
let UPTIME_SYNC = { host: '', port: '', baseSeconds: 0, syncedAt: 0, online: false };
let _refreshInFlight = false;
let CURRENT_THEME = localStorage.getItem('astrbot_hub_theme') || 'light';

const ROUTE_META = {
  dashboard: { title: '总览', sub: 'AstrBot 插件生态中枢 · 实时运行状态' },
  rules:     { title: '联动管线', sub: '内置 13 条跨插件联动规则与自定义工作流' },
  events:    { title: '事件日志', sub: '跨插件事件总线实时流与执行耗时' },
  data:      { title: '聚合数据', sub: '记忆摘要、备忘提醒、防扰安全与统一积分榜' },
  config:    { title: '插件配置', sub: '自动读取 _conf_schema.json · 在线热更新' },
  debug:     { title: '调试台', sub: '快捷调用已接入插件的 hub_action 接口' },
};

/* ==================== 主题切换（跟随系统 / 浅色 / 深色） & 侧栏钉住 ==================== */
const _darkMedia = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

function applyTheme(mode) {
  const isDark = mode === 'dark' || (mode === 'system' && _darkMedia && _darkMedia.matches);
  document.documentElement.classList.toggle('dark', isDark);
  document.documentElement.classList.toggle('light', !isDark);
  ['system', 'light', 'dark'].forEach(k => {
    const el = document.getElementById('th-' + k);
    if (el) el.classList.toggle('active', k === mode);
  });
}

function setTheme(mode) {
  CURRENT_THEME = mode;
  localStorage.setItem('astrbot_hub_theme', mode);
  applyTheme(mode);
}

if (_darkMedia && _darkMedia.addEventListener) {
  _darkMedia.addEventListener('change', () => {
    if (CURRENT_THEME === 'system') applyTheme('system');
  });
}
applyTheme(CURRENT_THEME);

function initSidebarPin() {
  const pinned = localStorage.getItem('astrbot_hub_sidebar_pinned') === '1';
  document.getElementById('sidebar').classList.toggle('pinned', pinned);
  document.body.classList.toggle('sidebar-pinned', pinned);
}
function toggleSidebarPin() {
  const sb = document.getElementById('sidebar');
  const next = !sb.classList.contains('pinned');
  sb.classList.toggle('pinned', next);
  document.body.classList.toggle('sidebar-pinned', next);
  localStorage.setItem('astrbot_hub_sidebar_pinned', next ? '1' : '0');
}
initSidebarPin();

/* ==================== 工具函数与实时运行时间 ==================== */
function formatUptime(totalSec) {
  const s = Math.max(0, Math.floor(Number(totalSec) || 0));
  if (s < 60) return `${s}s`;
  const days = Math.floor(s / 86400);
  const hrs = Math.floor((s % 86400) / 3600);
  const mins = Math.floor((s % 3600) / 60);
  const secs = s % 60;
  const pad = n => String(n).padStart(2, '0');
  if (days > 0) return `${days}d ${pad(hrs)}h ${pad(mins)}m ${pad(secs)}s`;
  if (hrs > 0) return `${hrs}h ${pad(mins)}m ${pad(secs)}s`;
  return `${mins}m ${pad(secs)}s`;
}

function renderUptimeLine() {
  const el = document.getElementById('subInfo');
  const pill = document.getElementById('statusPill');
  const stTxt = document.getElementById('statusText');
  if (!el || !UPTIME_SYNC.syncedAt) return;
  if (!UPTIME_SYNC.online) {
    if (pill) pill.classList.add('offline');
    if (stTxt) stTxt.textContent = '连接中断';
    el.textContent = '正在重试...';
    return;
  }
  if (pill) pill.classList.remove('offline');
  if (stTxt) stTxt.textContent = '已连接';
  const elapsed = Math.floor((Date.now() - UPTIME_SYNC.syncedAt) / 1000);
  const curSec = UPTIME_SYNC.baseSeconds + Math.max(0, elapsed);
  const fmt = formatUptime(curSec);
  el.textContent = `· ${fmt}`;
  const kpiUp = document.getElementById('kpiUptimeVal');
  if (kpiUp) kpiUp.textContent = fmt;
}

function esc(v) {
  return String(v ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

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
  document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
  const sec = document.getElementById('tab-' + id);
  if (sec) sec.classList.add('active');
  const activeBtn = btn || document.querySelector(`.nav-item[data-tab="${id}"]`);
  if (activeBtn) {
    activeBtn.classList.add('active');
    const ic = activeBtn.querySelector('svg');
    const topIc = document.getElementById('topRouteIcon');
    if (ic && topIc) {
      topIc.innerHTML = ic.outerHTML;
      const svg = topIc.querySelector('svg');
      if (svg) { svg.setAttribute('width', '17'); svg.setAttribute('height', '17'); }
    }
  }
  const meta = ROUTE_META[id] || ROUTE_META.dashboard;
  document.getElementById('topRouteTitle').textContent = meta.title;
  document.getElementById('topRouteSub').textContent = meta.sub;
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
    document.getElementById('logoutBtn').style.display = 'inline-flex';
    toast('登录成功');
    await refreshAll();
  } catch (e) { toast('登录失败：' + e.message); }
}

async function doLogout() {
  await api('/api/logout', { method: 'POST' });
  document.getElementById('loginModal').style.display = 'flex';
}

async function refreshAll(manual = false, silent = false) {
  if (_refreshInFlight) return;
  _refreshInFlight = true;
  if (manual) {
    const ic = document.getElementById('refreshIcon');
    if (ic) {
      ic.classList.remove('spin-once');
      void ic.offsetWidth;
      ic.classList.add('spin-once');
    }
  }
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

    const hubPlug = STATE.plugins.find(p => p.name === 'astrbot_plugin_hub');
    if (hubPlug && hubPlug.version) {
      document.getElementById('hubVerTag').textContent = 'v' + hubPlug.version;
    }

    const auth = ov.auth || {};
    const badge = document.getElementById('authBadge');
    badge.textContent = auth.required ? '🔐 Token 鉴权' : '本机免登';
    badge.className = 'auth-pill' + (auth.required ? ' secured' : '');
    document.getElementById('logoutBtn').style.display = auth.required ? 'inline-flex' : 'none';

    UPTIME_SYNC = {
      host: ov.server.host,
      port: ov.server.port,
      baseSeconds: Number(ov.server.uptime_seconds || 0),
      syncedAt: Date.now(),
      online: true,
    };
    renderUptimeLine();

    const eco = STATE.plugins.filter(p => p.ecosystem);
    const onlineEco = eco.filter(p => p.online).length;
    const activeRules = STATE.rules.filter(r => r.enabled).length;
    document.getElementById('bannerTitle').textContent =
      `已接入 ${onlineEco}/${eco.length} 个自研生态插件 · ${activeRules}/${STATE.rules.length} 条联动管线在线`;
    document.getElementById('bannerSub').textContent =
      `监听 ${ov.server.host}:${ov.server.port} · 生态协议 v1 · 点击管理自动化联动规则与自定义工作流`;
    document.getElementById('pluginPanoramaDesc').textContent =
      `共发现 ${STATE.plugins.length} 个插件（自研生态 ${eco.length} 个），支持按分类筛选、快捷动作与在线热更新`;

    renderKPIs(ov);
    const topoHovering = !!document.querySelector('#topoSvg.has-hover') || TOPO_VIEW.dragging;
    if (!silent || !topoHovering) {
      renderTopology(ov);
    }
    renderRecentEventsPreview();
    renderPlugins();
    renderRules();
    renderEvents();
    renderConfigSidebar();
    populateActionPlugins();
  } catch (e) {
    if (e.message === '需要登录鉴权') {
      UPTIME_SYNC.online = false;
    } else {
      UPTIME_SYNC.online = false;
      renderUptimeLine();
      if (!silent) toast('刷新失败：' + e.message);
    }
  } finally {
    _refreshInFlight = false;
  }
}

function renderKPIs(ov) {
  const eco = STATE.plugins.filter(p => p.ecosystem);
  const onlineEco = eco.filter(p => p.online).length;
  const activeRules = STATE.rules.filter(r => r.enabled).length;
  const protoCount = STATE.plugins.filter(p => p.protocol_version >= 1).length;
  const elapsed = UPTIME_SYNC.syncedAt ? Math.floor((Date.now() - UPTIME_SYNC.syncedAt) / 1000) : 0;
  const curUp = formatUptime(UPTIME_SYNC.baseSeconds + Math.max(0, elapsed));

  const kpis = [
    {
      solid: true,
      tab: 'dashboard',
      icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
      label: '服务运行',
      valId: 'kpiUptimeVal',
      valHtml: esc(curUp),
      sub: `${esc(ov.server.host)}:${esc(ov.server.port)} · 正常`,
    },
    {
      tab: 'dashboard',
      icon: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/></svg>',
      label: '自研生态插件',
      valHtml: `${onlineEco}<span class="denom">/ ${eco.length}</span>`,
      sub: `协议接入 ${protoCount} · 总计 ${STATE.plugins.length}`,
    },
    {
      tab: 'rules',
      icon: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
      label: '活跃联动管线',
      valHtml: `${activeRules}<span class="denom">/ ${STATE.rules.length}</span>`,
      sub: ov.auto_linkage_enabled ? '自动联动已开启' : '自动联动已暂停',
    },
    {
      tab: 'events',
      icon: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>',
      label: '跨插件事件',
      valHtml: `${Number(ov.event_count || 0)}`,
      sub: `累计触发联动 ${Number(ov.total_rule_triggers || 0)} 次`,
    },
    {
      tab: 'data',
      icon: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>',
      label: '生态积分人数',
      valHtml: `${Number(ov.eco_users || 0)}`,
      sub: '游戏 / 群统计 / 运势互通',
    },
  ];
  document.getElementById('kpiGrid').innerHTML = kpis.map(k =>
    `<div class="kpi-card" onclick="switchTab('${k.tab}')">
      <div class="kpi-icon ${k.solid ? 'solid' : ''}">${k.icon}</div>
      <div class="kpi-body">
        <div class="kpi-label">${k.label}</div>
        <div class="kpi-val" ${k.valId ? `id="${k.valId}"` : ''}>${k.valHtml}</div>
        <div class="kpi-sub">${k.sub}</div>
      </div>
    </div>`
  ).join('');
}

function renderRecentEventsPreview() {
  const wrap = document.getElementById('recentEventsPreview');
  const recent = (STATE.events || []).slice(0, 6);
  if (!recent.length) {
    wrap.innerHTML = `<div class="empty-inset">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
      <span>暂无跨插件联动事件</span>
      <button class="btn btn-sm" style="margin-top:4px" onclick="emitTestEvent()">发送一条测试事件</button>
    </div>`;
    return;
  }
  wrap.innerHTML = `<div class="recent-ev-list">${recent.map(e => {
    const disp = (e.dispatched || []);
    const okCnt = disp.filter(d => d.ok).length;
    const statusBadge = disp.length
      ? `<span class="badge ${okCnt === disp.length ? 'on' : 'off'}">${okCnt}/${disp.length} 成功</span>`
      : `<span class="badge proto">已记录</span>`;
    return `<div class="recent-ev-item">
      <div class="recent-ev-top">
        <span class="code-inline">${esc(e.event_type)}</span>
        ${statusBadge}
      </div>
      <div style="display:flex;justify-content:space-between;font-size:11.5px;color:var(--muted-foreground);font-family:var(--font-mono)">
        <span>${esc(String(e.source||'').replace('astrbot_plugin_',''))}</span>
        <span>${esc(String(e.ts||'').slice(5))}</span>
      </div>
    </div>`;
  }).join('')}</div>`;
}

/* ==================== 拓扑图辐射状双弧防重叠布局与画布交互 ==================== */
function _placeArc(items, cx, cy, rx, ry, startDeg, endDeg, outMap, color) {
  const n = items.length;
  if (!n) return;
  items.forEach((p, i) => {
    const deg = n === 1 ? (startDeg + endDeg) / 2 : startDeg + (endDeg - startDeg) * (i / (n - 1));
    const rad = deg * Math.PI / 180;
    const x = cx + Math.cos(rad) * rx;
    const y = cy + Math.sin(rad) * ry;
    outMap[p.name] = { x, y, color, plugin: p };
  });
}

function _applyTopoTransform() {
  const vp = document.getElementById('topoViewport');
  if (!vp) return;
  vp.setAttribute('transform', `translate(${TOPO_VIEW.tx.toFixed(1)}, ${TOPO_VIEW.ty.toFixed(1)}) scale(${TOPO_VIEW.scale.toFixed(3)})`);
}

function topoZoom(factor) {
  const cx = 600, cy = 270;
  const next = Math.max(0.65, Math.min(2.2, TOPO_VIEW.scale * factor));
  const ratio = next / TOPO_VIEW.scale;
  TOPO_VIEW.tx = cx - (cx - TOPO_VIEW.tx) * ratio;
  TOPO_VIEW.ty = cy - (cy - TOPO_VIEW.ty) * ratio;
  TOPO_VIEW.scale = next;
  _applyTopoTransform();
}

function topoResetView() {
  TOPO_VIEW.scale = 1;
  TOPO_VIEW.tx = 0;
  TOPO_VIEW.ty = 0;
  _applyTopoTransform();
}

function _initTopoCanvasEvents() {
  const wrap = document.getElementById('topoWrap');
  if (!wrap || wrap._bound) return;
  wrap._bound = true;

  wrap.addEventListener('wheel', (e) => {
    e.preventDefault();
    topoZoom(e.deltaY < 0 ? 1.1 : 1 / 1.1);
  }, { passive: false });

  wrap.addEventListener('pointerdown', (e) => {
    if (e.target.closest('.topo-node')) return;
    TOPO_VIEW.dragging = true;
    TOPO_VIEW.startX = e.clientX;
    TOPO_VIEW.startY = e.clientY;
    TOPO_VIEW.origTx = TOPO_VIEW.tx;
    TOPO_VIEW.origTy = TOPO_VIEW.ty;
    wrap.classList.add('dragging');
    wrap.setPointerCapture(e.pointerId);
  });

  wrap.addEventListener('pointermove', (e) => {
    if (!TOPO_VIEW.dragging) return;
    const rect = wrap.getBoundingClientRect();
    const scaleX = 1200 / Math.max(1, rect.width);
    const scaleY = 540 / Math.max(1, rect.height);
    TOPO_VIEW.tx = TOPO_VIEW.origTx + (e.clientX - TOPO_VIEW.startX) * scaleX;
    TOPO_VIEW.ty = TOPO_VIEW.origTy + (e.clientY - TOPO_VIEW.startY) * scaleY;
    _applyTopoTransform();
  });

  const endDrag = () => {
    TOPO_VIEW.dragging = false;
    wrap.classList.remove('dragging');
  };
  wrap.addEventListener('pointerup', endDrag);
  wrap.addEventListener('pointercancel', endDrag);
}

function _highlightTopoNode(nodeName) {
  const svg = document.getElementById('topoSvg');
  const tip = document.getElementById('topoTooltip');
  if (!svg) return;
  if (!nodeName) {
    svg.classList.remove('has-hover');
    svg.querySelectorAll('.hi').forEach(el => el.classList.remove('hi'));
    if (tip) tip.classList.remove('show');
    return;
  }
  const neighbors = TOPO_META.adj[nodeName] || new Set();
  svg.classList.add('has-hover');
  svg.querySelectorAll('.topo-node').forEach(el => {
    const n = el.getAttribute('data-node');
    if (n === nodeName || neighbors.has(n)) el.classList.add('hi');
    else el.classList.remove('hi');
  });
  svg.querySelectorAll('.topo-edge-base, .topo-edge-flow').forEach(el => {
    const s = el.getAttribute('data-src');
    const t = el.getAttribute('data-dst');
    if (s === nodeName || t === nodeName) el.classList.add('hi');
    else el.classList.remove('hi');
  });
  const info = TOPO_META.nodes[nodeName];
  if (tip && info) {
    const p = info.plugin;
    tip.innerHTML = `<strong>${esc(p.icon)} ${esc(p.display_name)}</strong> `
      + `<span style="font-family:var(--font-mono);color:var(--muted-foreground);font-size:11px">v${esc(p.version)}</span>`
      + `<div style="color:var(--muted-foreground);font-size:11px;margin-top:3px">状态：${p.online ? '<span style="color:var(--success);font-weight:600">在线</span>' : '<span style="color:var(--destructive)">离线</span>'} · 关联节点 ${neighbors.size} 个 · 点击打开配置</div>`;
    tip.classList.add('show');
  }
}

function renderTopology(ov) {
  _initTopoCanvasEvents();
  const svg = document.getElementById('topoSvg');
  const CX = 600, CY = 270;
  const groups = {
    hub:        { color: '#0ea5e9', items: [] },
    efficiency: { color: '#0ea5e9', items: [] },
    guard:      { color: '#10b981', items: [] },
    ops:        { color: '#f59e0b', items: [] },
    fun:        { color: '#a855f7', items: [] },
  };
  STATE.plugins.filter(p => p.ecosystem).forEach(p => {
    const g = groups[p.category] || groups.efficiency;
    g.items.push(p);
  });

  const pos = {};
  groups.hub.items.forEach(p => {
    pos[p.name] = { x: CX, y: CY, color: groups.hub.color, plugin: p, isHub: true };
  });

  const eff = groups.efficiency.items;
  if (eff.length <= 5) {
    _placeArc(eff, CX, CY, 445, 200, 136, 224, pos, groups.efficiency.color);
  } else {
    const outerN = Math.ceil(eff.length * 0.62);
    _placeArc(eff.slice(0, outerN), CX, CY, 495, 222, 130, 230, pos, groups.efficiency.color);
    _placeArc(eff.slice(outerN), CX, CY, 292, 152, 146, 214, pos, groups.efficiency.color);
  }
  _placeArc(groups.guard.items, CX, CY, 250, 198, 240, 300, pos, groups.guard.color);
  const ops = groups.ops.items;
  if (ops.length <= 5) {
    _placeArc(ops, CX, CY, 468, 204, -46, 46, pos, groups.ops.color);
  } else {
    const outerN = Math.ceil(ops.length * 0.65);
    _placeArc(ops.slice(0, outerN), CX, CY, 490, 216, -46, 46, pos, groups.ops.color);
    _placeArc(ops.slice(outerN), CX, CY, 292, 140, -34, 34, pos, groups.ops.color);
  }
  _placeArc(groups.fun.items, CX, CY, 355, 204, 52, 128, pos, groups.fun.color);

  const adj = {};
  const edgeMap = new Map();
  Object.keys(pos).forEach(k => { adj[k] = new Set(); });

  STATE.rules.filter(r => r.enabled).forEach(r => {
    (r.sources || []).forEach(s => {
      (r.targets || []).forEach(t => {
        if (pos[s] && pos[t] && s !== t) {
          adj[s].add(t);
          adj[t].add(s);
          const ek = s + '->' + t;
          if (!edgeMap.has(ek)) edgeMap.set(ek, { s, t, color: pos[s].color });
        }
      });
    });
  });

  const hubName = groups.hub.items[0] ? groups.hub.items[0].name : '';
  let spokeHtml = '';
  if (hubName && pos[hubName]) {
    Object.entries(pos).forEach(([name, pt]) => {
      if (name === hubName) return;
      spokeHtml += `<line x1="${CX}" y1="${CY}" x2="${pt.x.toFixed(1)}" y2="${pt.y.toFixed(1)}" stroke="${pt.color}" stroke-opacity="0.09" stroke-width="1" stroke-dasharray="2 6"/>`;
    });
  }

  let edgesHtml = '';
  edgeMap.forEach(({ s, t, color }) => {
    const a = pos[s], b = pos[t];
    const c1x = a.x + (CX - a.x) * 0.34 + (b.y - a.y) * 0.08;
    const c1y = a.y + (CY - a.y) * 0.34 - (b.x - a.x) * 0.05;
    const c2x = b.x + (CX - b.x) * 0.34 + (b.y - a.y) * 0.08;
    const c2y = b.y + (CY - b.y) * 0.34 - (b.x - a.x) * 0.05;
    const d = `M ${a.x.toFixed(1)} ${a.y.toFixed(1)} C ${c1x.toFixed(1)} ${c1y.toFixed(1)}, ${c2x.toFixed(1)} ${c2y.toFixed(1)}, ${b.x.toFixed(1)} ${b.y.toFixed(1)}`;
    const sEsc = esc(s), tEsc = esc(t);
    edgesHtml += `<path class="topo-edge-base" d="${d}" stroke="${color}" data-src="${sEsc}" data-dst="${tEsc}"/>`;
    edgesHtml += `<path class="topo-edge-flow" d="${d}" stroke="${color}" data-src="${sEsc}" data-dst="${tEsc}"/>`;
  });

  let nodesHtml = '';
  Object.entries(pos).forEach(([name, pt]) => {
    const p = pt.plugin;
    const isHub = !!pt.isHub;
    const r = isHub ? 36 : 17;
    const opacity = p.online ? 1 : 0.42;
    const pNameEsc = esc(p.name);
    const labelText = p.display_name || p.name;
    let estW = 16;
    for (const ch of labelText) estW += ch.charCodeAt(0) > 127 ? 11.2 : 6.6;
    const pillW = Math.max(54, Math.min(132, Math.round(estW)));
    const pillH = 20;
    const labelY = isHub ? (pt.y + 52) : (pt.y + 29);

    if (isHub) {
      nodesHtml += `<g class="topo-node" data-node="${pNameEsc}" style="opacity:${opacity}" onclick="openPluginConfig('${pNameEsc}')">
        <circle cx="${pt.x}" cy="${pt.y}" r="52" fill="#0ea5e9" fill-opacity="0.12"/>
        <circle cx="${pt.x}" cy="${pt.y}" r="${r}" fill="#0ea5e9" stroke="#38bdf8" stroke-width="2.5"/>
        <text x="${pt.x}" y="${pt.y + 7}" text-anchor="middle" font-size="22">${esc(p.icon)}</text>
        <rect x="${(pt.x - pillW / 2).toFixed(1)}" y="${(labelY - 14).toFixed(1)}" width="${pillW}" height="${pillH + 2}" rx="11" fill="var(--topo-pill-fill)" stroke="#0ea5e9" stroke-opacity="0.55" stroke-width="1"/>
        <text x="${pt.x}" y="${labelY}" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--topo-pill-text)">${esc(labelText)}</text>
      </g>`;
    } else {
      nodesHtml += `<g class="topo-node" data-node="${pNameEsc}" style="opacity:${opacity}" onclick="openPluginConfig('${pNameEsc}')">
        <circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="${r + 5}" fill="${pt.color}" fill-opacity="0.10"/>
        <circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="${r}" fill="var(--topo-node-fill)" stroke="${pt.color}" stroke-opacity="0.72" stroke-width="1.6"/>
        <text x="${pt.x.toFixed(1)}" y="${(pt.y + 5).toFixed(1)}" text-anchor="middle" font-size="13">${esc(p.icon)}</text>
        <rect x="${(pt.x - pillW / 2).toFixed(1)}" y="${(labelY - 13.5).toFixed(1)}" width="${pillW}" height="${pillH}" rx="10" fill="var(--topo-pill-fill)" stroke="var(--topo-pill-stroke)" stroke-width="0.9"/>
        <text x="${pt.x.toFixed(1)}" y="${labelY.toFixed(1)}" text-anchor="middle" font-size="10.8" font-weight="500" fill="var(--topo-pill-text)">${esc(labelText)}</text>
      </g>`;
    }
  });

  TOPO_META = { nodes: pos, adj };
  const radarHtml = `<g pointer-events="none">
    <circle class="topo-radar" cx="${CX}" cy="${CY}" r="142" fill="none" stroke="var(--topo-radar)" stroke-width="1" stroke-dasharray="3 7"/>
    <circle class="topo-radar-rev" cx="${CX}" cy="${CY}" r="228" fill="none" stroke="var(--topo-radar)" stroke-width="1" stroke-dasharray="2 10"/>
    <ellipse cx="${CX}" cy="${CY}" rx="472" ry="206" fill="none" stroke="var(--topo-radar)" stroke-opacity="0.55" stroke-width="1" stroke-dasharray="4 10"/>
  </g>`;

  svg.innerHTML = `<g id="topoViewport">${radarHtml}${spokeHtml}${edgesHtml}${nodesHtml}</g>`;
  _applyTopoTransform();

  svg.querySelectorAll('.topo-node').forEach(el => {
    const n = el.getAttribute('data-node');
    el.addEventListener('mouseenter', () => _highlightTopoNode(n));
    el.addEventListener('mouseleave', () => _highlightTopoNode(null));
  });
}

function renderPlugins() {
  const cat = document.getElementById('catFilter').value;
  const kw = document.getElementById('pluginSearch').value.trim().toLowerCase();
  const list = STATE.plugins.filter(p => {
    if (cat !== 'all' && p.category !== cat) return false;
    if (kw && !(p.name.toLowerCase().includes(kw) || p.display_name.toLowerCase().includes(kw) || p.desc.toLowerCase().includes(kw))) return false;
    return true;
  });
  document.getElementById('pluginGrid').innerHTML = list.length ? list.map(p => {
    const mChips = Object.entries(p.metrics || {}).slice(0, 5).map(([k, v]) =>
      `<span class="metric-chip"><span class="mk">${esc(k)}</span><span class="mv">${esc(v)}</span></span>`
    ).join('');
    const pName = esc(p.name);
    return `<div class="p-card">
      <div class="p-head">
        <div class="p-title"><span class="p-icon-tile">${esc(p.icon)}</span><span>${esc(p.display_name)}</span></div>
        <div class="p-badges">
          ${p.protocol_version ? '<span class="badge proto">联动 v'+esc(p.protocol_version)+'</span>' : ''}
          <span class="badge ${p.online?'on':'off'}">${p.online?'在线':'离线'}</span>
        </div>
      </div>
      <div class="p-meta">${pName} · v${esc(p.version)}</div>
      <div class="p-desc">${esc(p.desc || '暂无描述')}</div>
      <div class="metrics">${mChips || '<span class="metric-chip empty">无运行指标</span>'}</div>
      <div class="p-foot">
        <span class="p-foot-meta">动作 ${(p.actions||[]).length} · 配置项 ${Number(p.schema_count||0)}</span>
        <div style="display:flex;gap:6px">
          ${p.has_schema ? `<button class="btn btn-sm" onclick="openPluginConfig('${pName}')">配置</button>` : ''}
          ${(p.actions||[]).length ? `<button class="btn btn-sm btn-primary" onclick="jumpToAction('${pName}')">调试</button>` : ''}
        </div>
      </div>
    </div>`;
  }).join('') : '<div class="empty-inset" style="grid-column:1/-1"><span>没有匹配当前筛选条件的插件</span></div>';
}

function renderRules() {
  document.getElementById('ruleGrid').innerHTML = STATE.rules.map(r => {
    const rid = esc(r.id);
    return `<div class="rule-card">
      <div class="p-head">
        <div>
          <strong style="font-size:14px;color:var(--foreground)">${esc(r.name)}</strong>
          <div class="p-meta" style="margin-top:2px">ID: ${rid} · ${r.builtin ? '内置管线' : '自定义规则'}</div>
        </div>
        <label class="switch">
          <input type="checkbox" ${r.enabled ? 'checked' : ''} onchange="toggleRule('${rid}', this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div style="font-size:12.5px;color:var(--muted-foreground);line-height:1.58">${esc(r.description || '')}</div>
      <div style="font-size:11.5px;color:var(--muted-foreground);display:flex;align-items:center;gap:6px;flex-wrap:wrap">
        <span>事件</span><span class="code-inline">${esc((r.events||[]).join(', '))}</span>
      </div>
      <div class="p-foot">
        <span class="p-foot-meta">触发 ${Number(r.triggered_count || 0)} 次 ${r.last_triggered ? '· ' + esc(String(r.last_triggered).slice(5)) : ''}</span>
        ${r.builtin ? '' : `<button class="btn btn-sm btn-danger" onclick="deleteCustomRule('${rid}')">删除</button>`}
      </div>
    </div>`;
  }).join('');
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
  f.style.display = f.style.display === 'none' || !f.style.display ? 'block' : 'none';
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
      `<span class="badge ${d.ok?'on':'off'}">${esc(d.rule)} → ${esc(String(d.target||'').replace('astrbot_plugin_',''))}.${esc(d.action)} (${Number(d.ms||0)}ms)</span>`
    ).join(' ');
    return `<tr>
      <td style="white-space:nowrap;color:var(--muted-foreground);font-family:var(--font-mono);font-size:12px">${esc(String(e.ts||'').slice(5))}</td>
      <td style="font-family:var(--font-mono);font-size:12px">${esc(String(e.source||'').replace('astrbot_plugin_',''))}</td>
      <td><span class="code-inline">${esc(e.event_type)}</span></td>
      <td style="max-width:340px;word-break:break-all;font-size:12px;font-family:var(--font-mono);color:var(--muted-foreground)">${esc(JSON.stringify(e.payload || {}).slice(0,180))}</td>
      <td>${disp || '<span style="color:var(--muted-foreground);font-size:12px">已记录</span>'}</td>
    </tr>`;
  }).join('') : '<tr><td colspan="5" style="color:var(--muted-foreground);text-align:center;padding:28px">暂无跨插件事件</td></tr>';
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
    btn.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  const wrap = document.getElementById('dataPanelContent');
  wrap.innerHTML = '<div style="color:var(--muted-foreground);padding:12px 0">加载数据中...</div>';
  try {
    const res = await api('/api/data/' + encodeURIComponent(panel));
    if (panel === 'points') {
      const lb = res.eco_leaderboard || [];
      wrap.innerHTML = `
        <h3 style="font-size:14px;margin-bottom:12px;color:var(--foreground)">🏆 全生态统一积分榜（汇总游戏 / 群统计 / 运势 / 互动）</h3>
        <table><thead><tr><th>排名</th><th>用户</th><th>总积分</th><th>来源明细</th></tr></thead><tbody>
        ${lb.length ? lb.map((u, i) => `<tr><td style="font-family:var(--font-mono);color:var(--primary);font-weight:600">#${i+1}</td><td>${esc(u.nickname)} <span style="font-family:var(--font-mono);font-size:11.5px;color:var(--muted-foreground)">(${esc(u.user_id)})</span></td><td style="font-family:var(--font-mono);font-variant-numeric:tabular-nums"><strong>${Number(u.total||0)}</strong></td><td style="font-family:var(--font-mono);font-size:12px;color:var(--muted-foreground)">${esc(JSON.stringify(u.sources||{}))}</td></tr>`).join('') : '<tr><td colspan="4" style="color:var(--muted-foreground);text-align:center;padding:24px">暂无积分记录</td></tr>'}
        </tbody></table>`;
    } else if (panel === 'antispam') {
      const bots = res.bot_ids || [];
      wrap.innerHTML = `
        <div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap;align-items:center;">
          <input type="text" id="newBotId" placeholder="输入 QQ/Bot ID 一键同步全生态">
          <button class="btn btn-primary btn-sm" onclick="markBotEverywhere()">标记为 Bot 并全生态同步</button>
          <span style="font-size:12px;color:var(--muted-foreground);font-family:var(--font-mono)">当前共享 Bot 名单：${esc(bots.join(', ') || '空')}</span>
        </div>
        <pre class="json-box">${esc(JSON.stringify(res.plugins, null, 2))}</pre>`;
    } else {
      wrap.innerHTML = `<pre class="json-box">${esc(JSON.stringify(res, null, 2))}</pre>`;
    }
  } catch (e) { wrap.innerHTML = `<div style="color:var(--destructive)">加载失败：${esc(e.message)}</div>`; }
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
  sel.innerHTML = withAct.map(p => `<option value="${esc(p.name)}">${esc(p.icon)} ${esc(p.display_name)} (${esc(p.name)})</option>`).join('');
  if (prev && withAct.some(p => p.name === prev)) sel.value = prev;
  fillPluginActions();
}

function fillPluginActions() {
  const pname = document.getElementById('actPlugin').value;
  const p = STATE.plugins.find(x => x.name === pname);
  const sel = document.getElementById('actName');
  sel.innerHTML = (p && p.actions ? p.actions : []).map(a => `<option value="${esc(a)}">${esc(a)}</option>`).join('');
}

function jumpToAction(pname) {
  switchTab('debug');
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
  document.getElementById('cfgPluginList').innerHTML = list.map(p => {
    const pName = esc(p.name);
    return `<div class="side-item ${STATE.currentCfgPlugin===p.name?'active':''}" onclick="openPluginConfig('${pName}')">
      <span>${esc(p.icon)} ${esc(p.display_name)}</span>
      <span class="side-count">${Number(p.schema_count||0)}</span>
    </div>`;
  }).join('');
}

async function openPluginConfig(pname) {
  switchTab('config');
  STATE.currentCfgPlugin = pname;
  renderConfigSidebar();
  try {
    const cfg = await api('/api/plugins/' + encodeURIComponent(pname) + '/config');
    STATE.currentCfgFields = cfg.fields || [];
    document.getElementById('cfgTitle').textContent = `${pname} 配置（${cfg.live ? '实时热更新' : '仅写盘'}）`;
    document.getElementById('cfgSaveBtn').style.display = 'inline-flex';
    document.getElementById('cfgFormWrap').innerHTML = STATE.currentCfgFields.map(f => {
      let ctrl = '';
      const id = 'cf_' + esc(f.key);
      if (f.type === 'bool') {
        ctrl = `<label class="switch"><input type="checkbox" id="${id}" ${f.value ? 'checked' : ''}><span class="slider"></span></label>`;
      } else if (f.type === 'int' || f.type === 'float') {
        ctrl = `<input type="number" step="${f.type==='float'?'0.01':'1'}" id="${id}" value="${esc(f.value ?? '')}" style="width:220px;font-family:var(--font-mono)">`;
      } else if (f.is_secret) {
        ctrl = `<input type="password" id="${id}" value="${esc(f.value ?? '')}" placeholder="${f.has_value?'保持 ****** 即不修改原密文':'输入密文'}" style="width:100%">`;
      } else if (f.type === 'list') {
        const txt = Array.isArray(f.value) ? f.value.join(', ') : (f.value ?? '');
        ctrl = `<input type="text" id="${id}" value="${esc(txt)}" placeholder="逗号分隔多项" style="width:100%">`;
      } else {
        ctrl = `<input type="text" id="${id}" value="${esc(f.value ?? '')}" style="width:100%">`;
      }
      return `<div class="form-row">
        <div class="form-label">
          <strong>${esc(f.key)} ${f.is_secret ? '🔒' : ''}</strong>
          <span>${esc(f.description || '')}</span>
          ${f.hint ? `<span style="color:var(--primary)">${esc(f.hint)}</span>` : ''}
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

/* 每秒本地平滑递增运行时间（与服务端 uptime_seconds 基准对齐） */
setInterval(renderUptimeLine, 1000);

/* 每 15 秒静默同步后端状态、运行时间、KPI 与事件流（切回前台时立即同步） */
setInterval(() => {
  const modal = document.getElementById('loginModal');
  if (document.hidden || (modal && modal.style.display === 'flex')) return;
  refreshAll(false, true);
}, 15000);

document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    const modal = document.getElementById('loginModal');
    if (!modal || modal.style.display !== 'flex') refreshAll(false, true);
  }
});
</script>
</body>
</html>
"""
