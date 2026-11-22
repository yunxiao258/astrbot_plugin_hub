# -*- coding: utf-8 -*-
"""AstrBot 插件生态中枢单页 Web 管理面板（VisionOS / Linear 深色高级毛玻璃风格，纯静态无外部 CDN，国内离线可用）。"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AstrBot 插件生态中枢 · 管理面板</title>
<style>
:root {
  --bg-deep: #050811;
  --bg-mid: #070b14;
  --glass-bg: linear-gradient(155deg, rgba(17, 25, 40, 0.50) 0%, rgba(14, 21, 36, 0.28) 100%);
  --glass-card: linear-gradient(160deg, rgba(20, 30, 48, 0.48) 0%, rgba(15, 23, 40, 0.26) 100%);
  --glass-card-hover: linear-gradient(160deg, rgba(26, 39, 62, 0.58) 0%, rgba(17, 26, 44, 0.36) 100%);
  --glass-recessed: rgba(5, 8, 17, 0.62);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-border-hover: rgba(255, 255, 255, 0.16);
  --glass-highlight: inset 0 1px 0 0 rgba(255, 255, 255, 0.14);
  --glass-highlight-strong: inset 0 1px 0 0 rgba(255, 255, 255, 0.22);
  --glass-shadow: 0 12px 32px rgba(0, 0, 0, 0.38);
  --glass-shadow-hover: 0 18px 42px rgba(0, 0, 0, 0.48);

  --text: #f1f5f9;
  --text-soft: #cbd5e1;
  --muted: #8b9bb4;
  --muted-dim: rgba(139, 155, 180, 0.72);

  --accent: #38bdf8;
  --accent-bright: #7dd3fc;
  --indigo: #818cf8;
  --green: #34d399;
  --amber: #fbbf24;
  --red: #f87171;
  --purple: #c084fc;

  --radius: 16px;
  --radius-sm: 10px;
  --font-sans: "Inter", "HarmonyOS Sans SC", "PingFang SC", -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
  --font-mono: "JetBrains Mono", "Cascadia Code", "Fira Code", ui-monospace, SFMono-Regular, Consolas, monospace;
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

/* 极细半透明滚动条 */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.20);
  border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.38); }
* { scrollbar-width: thin; scrollbar-color: rgba(148, 163, 184, 0.22) transparent; }

html, body {
  min-height: 100vh;
  background-color: var(--bg-deep);
  background-image: radial-gradient(ellipse 90% 65% at 50% -10%, #0d1629 0%, #070b14 55%, #050811 100%);
  color: var(--text);
  font-family: var(--font-sans);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

/* ==================== 一、全局环境光画布、点阵网格与微噪点 ==================== */
.ambient-canvas {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.aurora-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(135px);
  will-change: transform, opacity;
}
.orb-cyan {
  width: 620px; height: 620px;
  top: -180px; left: -120px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.17) 0%, rgba(14, 165, 233, 0.04) 60%, transparent 100%);
  animation: driftOrbA 24s ease-in-out infinite alternate;
}
.orb-indigo {
  width: 720px; height: 720px;
  top: 18%; right: -190px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.16) 0%, rgba(59, 130, 246, 0.05) 62%, transparent 100%);
  animation: driftOrbB 28s ease-in-out infinite alternate;
}
.orb-violet {
  width: 640px; height: 640px;
  bottom: -240px; left: 32%;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.13) 0%, rgba(139, 92, 246, 0.03) 65%, transparent 100%);
  animation: driftOrbC 32s ease-in-out infinite alternate;
}

@keyframes driftOrbA {
  0%   { transform: translate3d(0, 0, 0) scale(1); opacity: 0.92; }
  50%  { transform: translate3d(55px, 38px, 0) scale(1.07); opacity: 1; }
  100% { transform: translate3d(20px, 72px, 0) scale(0.96); opacity: 0.85; }
}
@keyframes driftOrbB {
  0%   { transform: translate3d(0, 0, 0) scale(1); opacity: 0.88; }
  50%  { transform: translate3d(-60px, -42px, 0) scale(1.08); opacity: 1; }
  100% { transform: translate3d(-25px, 40px, 0) scale(0.95); opacity: 0.82; }
}
@keyframes driftOrbC {
  0%   { transform: translate3d(0, 0, 0) scale(1); opacity: 0.85; }
  50%  { transform: translate3d(48px, -36px, 0) scale(1.06); opacity: 1; }
  100% { transform: translate3d(-40px, -18px, 0) scale(0.97); opacity: 0.80; }
}

.ambient-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255, 255, 255, 0.055) 1px, transparent 1px);
  background-size: 26px 26px;
  mask-image: radial-gradient(ellipse 85% 75% at 50% 35%, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.22) 72%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 85% 75% at 50% 35%, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.22) 72%, transparent 100%);
}

.ambient-noise {
  position: absolute;
  inset: 0;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.82' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 180px 180px;
}

/* 主层级高于背景画布 */
.topbar, .container { position: relative; z-index: 2; }

/* ==================== 二、顶部悬浮毛玻璃导航栏 ==================== */
.topbar {
  position: sticky;
  top: 0;
  z-index: 40;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
  padding: 12px 28px;
  background: rgba(7, 11, 20, 0.62);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.32);
}
.topbar::after {
  content: "";
  position: absolute;
  left: 0; right: 0; bottom: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.10) 18%, rgba(56,189,248,0.28) 50%, rgba(255,255,255,0.10) 82%, transparent 100%);
  pointer-events: none;
}

.brand { display: flex; align-items: center; gap: 13px; }
.brand-logo {
  width: 38px; height: 38px;
  border-radius: 11px;
  background: linear-gradient(140deg, rgba(56, 189, 248, 0.28) 0%, rgba(99, 102, 241, 0.34) 100%);
  border: 1px solid rgba(125, 211, 252, 0.30);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.28), 0 0 22px rgba(56, 189, 248, 0.22);
  display: flex; align-items: center; justify-content: center;
  font-size: 19px;
}
.brand h1 {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.015em;
  background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.brand-sub-wrap {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-top: 2px;
}
.pulse-dot {
  position: relative;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px rgba(52, 211, 153, 0.85);
  flex-shrink: 0;
  transition: background 0.25s var(--ease), box-shadow 0.25s var(--ease);
}
.pulse-dot::after {
  content: "";
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 1.5px solid rgba(52, 211, 153, 0.6);
  animation: pulseRing 2.4s cubic-bezier(0.2, 0.7, 0.3, 1) infinite;
}
.pulse-dot.offline {
  background: var(--red);
  box-shadow: 0 0 8px rgba(248, 113, 113, 0.75);
}
.pulse-dot.offline::after { animation: none; opacity: 0; }
@keyframes pulseRing {
  0%   { transform: scale(0.75); opacity: 0.9; }
  75%  { transform: scale(1.95); opacity: 0; }
  100% { transform: scale(1.95); opacity: 0; }
}
.brand small {
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}

/* 分段控制器（Segmented Control）胶囊槽 */
.nav-tabs {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  border-radius: 999px;
  background: rgba(5, 8, 17, 0.58);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.48), 0 1px 0 rgba(255, 255, 255, 0.05);
  flex-wrap: wrap;
}
.tab-btn {
  padding: 7px 16px;
  border-radius: 999px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.01em;
  transition: color 0.22s var(--ease), background 0.22s var(--ease), border-color 0.22s var(--ease), box-shadow 0.22s var(--ease);
}
.tab-btn:hover {
  color: var(--text);
  background: rgba(255, 255, 255, 0.05);
}
.tab-btn.active {
  color: #f8fafc;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.14) 0%, rgba(56, 189, 248, 0.12) 100%);
  border-color: rgba(125, 211, 252, 0.34);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.26), 0 0 18px rgba(56, 189, 248, 0.20);
}

.top-actions { display: flex; align-items: center; gap: 9px; }

/* 低饱和高级磨砂状态胶囊 */
.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  padding: 5px 12px;
  border-radius: 999px;
  background: rgba(52, 211, 153, 0.09);
  color: #a7f3d0;
  border: 1px solid rgba(52, 211, 153, 0.24);
  backdrop-filter: blur(12px);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.10);
}
.pill.warn {
  background: rgba(148, 163, 184, 0.09);
  color: #cbd5e1;
  border-color: rgba(255, 255, 255, 0.13);
}

/* 统一磨砂玻璃按钮 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.10);
  background: rgba(255, 255, 255, 0.055);
  backdrop-filter: blur(12px);
  color: var(--text-soft);
  cursor: pointer;
  font-family: var(--font-sans);
  font-size: 12.5px;
  font-weight: 500;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.10);
  transition: all 0.2s var(--ease);
}
.btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.11);
  border-color: rgba(125, 211, 252, 0.35);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18), 0 0 14px rgba(56, 189, 248, 0.16);
}
.btn:active { transform: scale(0.97); }
.btn-primary {
  background: linear-gradient(180deg, rgba(56, 189, 248, 0.26) 0%, rgba(37, 99, 235, 0.34) 100%);
  border-color: rgba(125, 211, 252, 0.42);
  color: #f0f9ff;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.28), 0 4px 16px rgba(37, 99, 235, 0.24);
}
.btn-primary:hover {
  background: linear-gradient(180deg, rgba(56, 189, 248, 0.36) 0%, rgba(37, 99, 235, 0.46) 100%);
  border-color: rgba(125, 211, 252, 0.65);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.34), 0 0 22px rgba(56, 189, 248, 0.30);
}
.btn-danger {
  background: rgba(248, 113, 113, 0.11);
  border-color: rgba(248, 113, 113, 0.30);
  color: #fecaca;
}
.btn-danger:hover {
  background: rgba(248, 113, 113, 0.22);
  border-color: rgba(248, 113, 113, 0.55);
  box-shadow: 0 0 14px rgba(248, 113, 113, 0.22);
}
.btn-sm { padding: 5px 12px; font-size: 12px; }
.btn-icon { width: 30px; height: 30px; padding: 0; border-radius: 9px; font-size: 14px; }
.spin-once { animation: spin360 0.55s var(--ease); }
@keyframes spin360 { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* ==================== 三、主容器与通用玻璃容器 ==================== */
.container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 24px 28px 68px;
}
.section { display: none; animation: fadeSlideIn 0.28s var(--ease); }
.section.active { display: block; }
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.panel-box {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  box-shadow: var(--glass-highlight), var(--glass-shadow);
  padding: 22px 24px;
  margin-bottom: 22px;
  overflow: hidden;
}
.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 18px;
}
.panel-head h2 {
  font-size: 15.5px;
  font-weight: 600;
  letter-spacing: 0.01em;
  color: #f8fafc;
  display: flex;
  align-items: center;
  gap: 8px;
}
.filter-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }

/* ==================== 四、顶部 5 个核心 KPI 指标卡 ==================== */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 22px;
}
@media (max-width: 1180px) { .kpi-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 720px)  { .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 480px)  { .kpi-grid { grid-template-columns: 1fr; } }

.kpi {
  --kpi-glow: #38bdf8;
  --mx: 50%;
  --my: 0%;
  position: relative;
  background: var(--glass-card);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  box-shadow: var(--glass-highlight), var(--glass-shadow);
  padding: 20px 22px 19px;
  overflow: hidden;
  transition: transform 0.25s var(--ease), border-color 0.25s var(--ease), box-shadow 0.25s var(--ease), background 0.25s var(--ease);
}
/* 左侧语义极细发光指示条 */
.kpi::before {
  content: "";
  position: absolute;
  left: 0; top: 18px; bottom: 18px;
  width: 2.5px;
  border-radius: 0 4px 4px 0;
  background: linear-gradient(180deg, transparent 0%, var(--kpi-glow) 50%, transparent 100%);
  box-shadow: 0 0 12px var(--kpi-glow);
  opacity: 0.85;
}
/* 柔和语义微光与鼠标跟随高光层 */
.kpi::after {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(240px circle at var(--mx) var(--my), rgba(255, 255, 255, 0.08), transparent 65%),
    radial-gradient(220px circle at 0% 0%, var(--kpi-glow-soft, rgba(56, 189, 248, 0.13)), transparent 72%);
  opacity: 0.78;
  pointer-events: none;
  transition: opacity 0.25s var(--ease);
}
.kpi:hover {
  transform: translateY(-2px);
  background: var(--glass-card-hover);
  border-color: var(--glass-border-hover);
  box-shadow: var(--glass-highlight-strong), var(--glass-shadow-hover);
}
.kpi:hover::after { opacity: 1; }

.kpi-c-cyan   { --kpi-glow: #38bdf8; --kpi-glow-soft: rgba(56, 189, 248, 0.14); }
.kpi-c-indigo { --kpi-glow: #818cf8; --kpi-glow-soft: rgba(129, 140, 248, 0.14); }
.kpi-c-green  { --kpi-glow: #34d399; --kpi-glow-soft: rgba(52, 211, 153, 0.14); }
.kpi-c-amber  { --kpi-glow: #fbbf24; --kpi-glow-soft: rgba(251, 191, 36, 0.13); }
.kpi-c-purple { --kpi-glow: #c084fc; --kpi-glow-soft: rgba(192, 132, 252, 0.14); }

.kpi .label {
  position: relative; z-index: 1;
  color: var(--muted);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.02em;
  margin-bottom: 10px;
}
.kpi .val {
  position: relative; z-index: 1;
  font-family: var(--font-mono);
  font-size: 30px;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.025em;
  font-variant-numeric: tabular-nums;
  background: linear-gradient(180deg, #ffffff 10%, #cbd5e1 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.kpi .val .denom {
  font-size: 17px;
  font-weight: 500;
  color: rgba(148, 163, 184, 0.55);
  -webkit-text-fill-color: rgba(148, 163, 184, 0.55);
  margin-left: 2px;
}
.kpi .sub {
  position: relative; z-index: 1;
  font-size: 11.5px;
  color: var(--muted-dim);
  margin-top: 9px;
  font-family: var(--font-sans);
}

/* ==================== 五、全生态插件联动拓扑图 ==================== */
.topo-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.topo-legends {
  display: flex;
  align-items: center;
  gap: 7px;
  flex-wrap: wrap;
}
.legend-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11.5px;
  color: var(--text-soft);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
}
.legend-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.topo-zoom-group {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px;
  border-radius: 11px;
  background: rgba(5, 8, 17, 0.52);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.topo-wrap {
  position: relative;
  width: 100%;
  height: 490px;
  border-radius: 14px;
  background: radial-gradient(ellipse 65% 65% at 50% 50%, rgba(15, 28, 54, 0.42) 0%, rgba(5, 8, 17, 0.52) 100%);
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: inset 0 2px 18px rgba(0, 0, 0, 0.45);
  overflow: hidden;
  cursor: grab;
  user-select: none;
}
.topo-wrap.dragging { cursor: grabbing; }
svg.topo {
  width: 100%;
  height: 100%;
  display: block;
}
.topo-hint {
  position: absolute;
  left: 14px; bottom: 12px;
  font-size: 11px;
  color: rgba(148, 163, 184, 0.58);
  background: rgba(5, 8, 17, 0.58);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 4px 10px;
  border-radius: 999px;
  pointer-events: none;
}
.topo-tooltip {
  position: absolute;
  top: 12px; left: 14px;
  z-index: 5;
  pointer-events: none;
  opacity: 0;
  transform: translateY(-4px);
  transition: opacity 0.18s var(--ease), transform 0.18s var(--ease);
  background: rgba(9, 14, 26, 0.84);
  backdrop-filter: blur(16px) saturate(160%);
  border: 1px solid rgba(125, 211, 252, 0.24);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.14), 0 10px 26px rgba(0,0,0,0.45);
  border-radius: 11px;
  padding: 8px 12px;
  font-size: 12px;
  color: var(--text);
}
.topo-tooltip.show { opacity: 1; transform: translateY(0); }

/* SVG 流动光点与交互高亮 */
.topo-radar {
  transform-origin: 600px 270px;
  animation: slowSpin 90s linear infinite;
}
.topo-radar-rev {
  transform-origin: 600px 270px;
  animation: slowSpin 130s linear infinite reverse;
}
@keyframes slowSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.topo-edge-base {
  fill: none;
  stroke-width: 1.35;
  stroke-opacity: 0.18;
  transition: stroke-opacity 0.24s var(--ease), stroke-width 0.24s var(--ease);
}
.topo-edge-flow {
  fill: none;
  stroke-width: 1.5;
  stroke-opacity: 0.32;
  stroke-dasharray: 4 18;
  animation: flowDash 3.6s linear infinite;
  transition: stroke-opacity 0.24s var(--ease), stroke-width 0.24s var(--ease);
}
@keyframes flowDash {
  from { stroke-dashoffset: 44; }
  to   { stroke-dashoffset: 0; }
}
.topo-node {
  cursor: pointer;
  transition: opacity 0.24s var(--ease);
}
.topo-node .node-ring {
  transition: stroke-opacity 0.22s var(--ease), filter 0.22s var(--ease);
}
.topo-node:hover .node-ring {
  stroke-opacity: 1;
}

/* 悬停聚焦态：淡出无关元素，高亮关联链路 */
svg.topo.has-hover .topo-node { opacity: 0.16 !important; }
svg.topo.has-hover .topo-node.hi { opacity: 1 !important; }
svg.topo.has-hover .topo-edge-base { stroke-opacity: 0.04; }
svg.topo.has-hover .topo-edge-flow { stroke-opacity: 0.03; }
svg.topo.has-hover .topo-edge-base.hi { stroke-opacity: 0.62; stroke-width: 2.1; }
svg.topo.has-hover .topo-edge-flow.hi { stroke-opacity: 0.95; stroke-width: 2.3; animation-duration: 1.4s; }

/* ==================== 六、内凹暗色毛玻璃表单控件 ==================== */
input[type="text"], input[type="password"], input[type="number"], select, textarea {
  background: var(--glass-recessed);
  color: var(--text);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 10px;
  padding: 8px 13px;
  font-family: var(--font-sans);
  font-size: 13px;
  outline: none;
  backdrop-filter: blur(12px);
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.45);
  transition: border-color 0.2s var(--ease), box-shadow 0.2s var(--ease), background 0.2s var(--ease);
}
input::placeholder, textarea::placeholder { color: rgba(139, 155, 180, 0.56); }
select { cursor: pointer; }
select option { background: #0b1120; color: #f1f5f9; }
input:focus, select:focus, textarea:focus {
  border-color: rgba(56, 189, 248, 0.58);
  background: rgba(7, 12, 24, 0.78);
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.45), 0 0 0 3px rgba(56, 189, 248, 0.15);
}

/* ==================== 七、插件运行全景网格与卡片 ==================== */
.plugin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: 16px;
}
.p-card, .rule-card {
  --mx: 50%;
  --my: 0%;
  position: relative;
  background: var(--glass-card);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  box-shadow: var(--glass-highlight), var(--glass-shadow);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 11px;
  overflow: hidden;
  transition: transform 0.24s var(--ease), border-color 0.24s var(--ease), box-shadow 0.24s var(--ease), background 0.24s var(--ease);
}
.p-card::after, .rule-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(280px circle at var(--mx) var(--my), rgba(125, 211, 252, 0.08), transparent 65%);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s var(--ease);
}
.p-card:hover, .rule-card:hover {
  transform: translateY(-2px);
  background: var(--glass-card-hover);
  border-color: rgba(125, 211, 252, 0.24);
  box-shadow: var(--glass-highlight-strong), var(--glass-shadow-hover);
}
.p-card:hover::after, .rule-card:hover::after { opacity: 1; }

.p-head {
  position: relative; z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.p-title {
  font-weight: 600;
  font-size: 14.5px;
  color: #f8fafc;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.p-icon-tile {
  width: 28px; height: 28px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.055);
  border: 1px solid rgba(255, 255, 255, 0.09);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}
.p-badges { display: flex; gap: 6px; flex-shrink: 0; align-items: center; }

/* 霓虹玻璃描边微章 */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  padding: 2.5px 9px;
  border-radius: 999px;
  letter-spacing: 0.01em;
  backdrop-filter: blur(8px);
}
.badge.on {
  background: rgba(52, 211, 153, 0.10);
  color: #6ee7b7;
  border: 1px solid rgba(52, 211, 153, 0.30);
}
.badge.on::before {
  content: "";
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 6px #34d399;
}
.badge.off {
  background: rgba(248, 113, 113, 0.10);
  color: #fca5a5;
  border: 1px solid rgba(248, 113, 113, 0.28);
}
.badge.proto {
  background: rgba(56, 189, 248, 0.10);
  color: #7dd3fc;
  border: 1px solid rgba(56, 189, 248, 0.30);
  font-family: var(--font-mono);
  font-size: 10.5px;
}

.p-meta {
  position: relative; z-index: 1;
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: rgba(139, 155, 180, 0.70);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}
.p-desc {
  position: relative; z-index: 1;
  font-size: 12.5px;
  line-height: 1.6;
  color: rgba(203, 213, 225, 0.76);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}
.metrics {
  position: relative; z-index: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.metric-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  padding: 3px 9px;
  border-radius: 7px;
  background: rgba(255, 255, 255, 0.035);
  border: 1px solid rgba(255, 255, 255, 0.075);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
}
.metric-chip .mk { color: rgba(139, 155, 180, 0.80); }
.metric-chip .mv {
  color: #f1f5f9;
  font-family: var(--font-mono);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.metric-chip.empty { color: rgba(139, 155, 180, 0.55); }

.p-foot {
  position: relative; z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 11px;
  border-top: 1px solid rgba(255, 255, 255, 0.065);
}
.p-foot-meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: rgba(139, 155, 180, 0.72);
  font-variant-numeric: tabular-nums;
}

/* ==================== 八、联动规则、表格、侧边配置与弹窗 ==================== */
.rule-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 14px;
}
.custom-form-box {
  display: none;
  background: rgba(5, 8, 17, 0.54);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

/* 磨砂拨动开关 */
.switch { position: relative; display: inline-block; width: 42px; height: 23px; flex-shrink: 0; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; inset: 0;
  background: rgba(148, 163, 184, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 999px;
  transition: all 0.22s var(--ease);
}
.slider:before {
  content: ""; position: absolute;
  height: 17px; width: 17px; left: 2px; bottom: 2px;
  background: #e2e8f0;
  border-radius: 50%;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.45);
  transition: all 0.22s var(--ease);
}
input:checked + .slider {
  background: rgba(52, 211, 153, 0.32);
  border-color: rgba(52, 211, 153, 0.55);
  box-shadow: 0 0 12px rgba(52, 211, 153, 0.25);
}
input:checked + .slider:before {
  transform: translateX(19px);
  background: #ffffff;
}

table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td {
  text-align: left;
  padding: 11px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  vertical-align: top;
}
th {
  color: var(--muted);
  font-weight: 600;
  font-size: 11.5px;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.02);
}
tbody tr { transition: background 0.16s var(--ease); }
tbody tr:hover { background: rgba(255, 255, 255, 0.03); }

.split-layout { display: grid; grid-template-columns: 270px 1fr; gap: 20px; }
@media (max-width: 860px) { .split-layout { grid-template-columns: 1fr; } }

.side-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 4px;
}
.side-item {
  padding: 10px 13px;
  border-radius: 11px;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--muted);
  border: 1px solid transparent;
  transition: all 0.18s var(--ease);
}
.side-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text);
}
.side-item.active {
  background: linear-gradient(180deg, rgba(56, 189, 248, 0.16) 0%, rgba(56, 189, 248, 0.08) 100%);
  color: #f0f9ff;
  border-color: rgba(125, 211, 252, 0.30);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.16);
}
.side-count {
  font-family: var(--font-mono);
  font-size: 11px;
  padding: 1px 7px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  color: var(--muted);
}

.form-row {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 14px;
  align-items: start;
  padding: 14px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
@media (max-width: 720px) { .form-row { grid-template-columns: 1fr; } }
.form-label strong {
  font-family: var(--font-mono);
  font-size: 12.5px;
  display: block;
  color: #f1f5f9;
}
.form-label span {
  font-size: 12px;
  color: var(--muted);
  display: block;
  margin-top: 3px;
  line-height: 1.5;
}

.sub-tabs {
  display: inline-flex;
  gap: 5px;
  flex-wrap: wrap;
  padding: 4px;
  border-radius: 999px;
  background: rgba(5, 8, 17, 0.50);
  border: 1px solid rgba(255, 255, 255, 0.07);
}
.action-bar-grid {
  display: grid;
  grid-template-columns: 240px 200px 1fr auto;
  gap: 10px;
  align-items: center;
  margin-bottom: 12px;
}
@media (max-width: 900px) { .action-bar-grid { grid-template-columns: 1fr; } }

pre.json-box {
  background: rgba(5, 8, 17, 0.68);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 14px 16px;
  overflow: auto;
  max-height: 380px;
  font-size: 12px;
  line-height: 1.6;
  color: #cbd5e1;
  font-family: var(--font-mono);
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.45);
}

.code-inline {
  font-family: var(--font-mono);
  background: rgba(56, 189, 248, 0.10);
  border: 1px solid rgba(56, 189, 248, 0.22);
  padding: 2px 7px;
  border-radius: 6px;
  font-size: 11.5px;
  color: var(--accent-bright);
}

.toast {
  position: fixed;
  right: 24px; bottom: 24px;
  z-index: 90;
  background: rgba(12, 19, 34, 0.86);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(125, 211, 252, 0.35);
  color: #f8fafc;
  padding: 11px 18px;
  border-radius: 12px;
  font-size: 13px;
  display: none;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18), 0 14px 36px rgba(0, 0, 0, 0.55);
}

.modal-bg {
  position: fixed;
  inset: 0;
  z-index: 80;
  background: rgba(3, 6, 15, 0.72);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.modal-card {
  background: linear-gradient(155deg, rgba(17, 25, 42, 0.82) 0%, rgba(10, 15, 28, 0.76) 100%);
  backdrop-filter: blur(26px) saturate(180%);
  -webkit-backdrop-filter: blur(26px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.20), 0 24px 64px rgba(0, 0, 0, 0.65);
  border-radius: 18px;
  padding: 28px;
  width: 100%;
  max-width: 420px;
}
.modal-card h3 { margin-bottom: 10px; font-size: 17px; font-weight: 600; }
.modal-card p { font-size: 13px; color: var(--muted); margin-bottom: 16px; line-height: 1.65; }
</style>
</head>
<body>

<!-- 环境光氛围层：极光弥散球 + 精密点阵网格 + 2% 微噪点 -->
<div class="ambient-canvas" aria-hidden="true">
  <div class="aurora-orb orb-cyan"></div>
  <div class="aurora-orb orb-indigo"></div>
  <div class="aurora-orb orb-violet"></div>
  <div class="ambient-grid"></div>
  <div class="ambient-noise"></div>
</div>

<header class="topbar">
  <div class="brand">
    <div class="brand-logo">🎛️</div>
    <div>
      <h1>AstrBot 插件生态中枢</h1>
      <div class="brand-sub-wrap">
        <span class="pulse-dot" id="statusDot" aria-hidden="true"></span>
        <small id="subInfo">加载中...</small>
      </div>
    </div>
  </div>
  <nav class="nav-tabs" role="tablist">
    <button class="tab-btn active" onclick="switchTab('dashboard', this)">全景仪表盘</button>
    <button class="tab-btn" onclick="switchTab('rules', this)">联动规则与事件流</button>
    <button class="tab-btn" onclick="switchTab('data', this)">跨插件数据与操作</button>
    <button class="tab-btn" onclick="switchTab('config', this)">在线配置编辑器</button>
  </nav>
  <div class="top-actions">
    <span class="pill" id="authBadge">检测中</span>
    <button class="btn btn-sm" id="refreshBtn" onclick="refreshAll(true)">
      <svg id="refreshIcon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.64-6.36"/><polyline points="21 3 21 9 15 9"/></svg>
      <span>刷新</span>
    </button>
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
        <div class="topo-toolbar">
          <div class="topo-legends">
            <span class="legend-pill"><span class="legend-dot" style="background:#38bdf8;box-shadow:0 0 8px #38bdf8"></span>效率记忆</span>
            <span class="legend-pill"><span class="legend-dot" style="background:#34d399;box-shadow:0 0 8px #34d399"></span>防扰安全</span>
            <span class="legend-pill"><span class="legend-dot" style="background:#fbbf24;box-shadow:0 0 8px #fbbf24"></span>运维监控</span>
            <span class="legend-pill"><span class="legend-dot" style="background:#c084fc;box-shadow:0 0 8px #c084fc"></span>娱乐积分</span>
          </div>
          <div class="topo-zoom-group" title="缩放与平移画布">
            <button class="btn btn-icon" onclick="topoZoom(1.18)" aria-label="放大">+</button>
            <button class="btn btn-icon" onclick="topoZoom(1/1.18)" aria-label="缩小">−</button>
            <button class="btn btn-sm" style="border-radius:8px;padding:4px 9px" onclick="topoResetView()">重置</button>
          </div>
        </div>
      </div>
      <div class="topo-wrap" id="topoWrap">
        <div class="topo-tooltip" id="topoTooltip"></div>
        <svg class="topo" id="topoSvg" viewBox="0 0 1200 540" preserveAspectRatio="xMidYMid meet"></svg>
        <div class="topo-hint">悬停节点聚焦关联链路 · 点击节点打开配置 · 滚轮缩放 / 拖拽画布</div>
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
          <input type="text" id="pluginSearch" placeholder="搜索插件名 / 说明..." style="min-width:220px" oninput="renderPlugins()">
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
      <div id="customRuleForm" class="custom-form-box">
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
      <div class="action-bar-grid">
        <select id="actPlugin" onchange="fillPluginActions()"></select>
        <select id="actName"></select>
        <input type="text" id="actParams" style="font-family:var(--font-mono);font-size:12px" placeholder='JSON 参数，例如 {"umo":"default:GroupMessage:1001","content":"测试备忘"}' value="{}">
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
    <input type="password" id="loginToken" style="width:100%;margin-bottom:14px" placeholder="请输入管理员 Token" onkeydown="if(event.key==='Enter')doLogin()">
    <button class="btn btn-primary" style="width:100%;padding:9px 16px" onclick="doLogin()">登录管理面板</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let STATE = { overview: null, plugins: [], rules: [], events: [], currentCfgPlugin: null, currentCfgFields: [] };
let TOPO_VIEW = { scale: 1, tx: 0, ty: 0, dragging: false, startX: 0, startY: 0, origTx: 0, origTy: 0 };
let TOPO_META = { nodes: {}, adj: {} };
let UPTIME_SYNC = { host: '', port: '', baseSeconds: 0, syncedAt: 0, online: false };
let _refreshInFlight = false;

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
  const dot = document.getElementById('statusDot');
  if (!el || !UPTIME_SYNC.syncedAt) return;
  if (!UPTIME_SYNC.online) {
    if (dot) dot.classList.add('offline');
    el.textContent = `监听 ${UPTIME_SYNC.host}:${UPTIME_SYNC.port} · 连接中断，正在重试...`;
    return;
  }
  if (dot) dot.classList.remove('offline');
  const elapsed = Math.floor((Date.now() - UPTIME_SYNC.syncedAt) / 1000);
  const curSec = UPTIME_SYNC.baseSeconds + Math.max(0, elapsed);
  el.textContent = `监听 ${UPTIME_SYNC.host}:${UPTIME_SYNC.port} · 运行 ${formatUptime(curSec)} · 生态协议 v1`;
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

/* 卡片跟随鼠标的微弱高光反射 */
document.addEventListener('pointermove', (e) => {
  const card = e.target.closest('.kpi, .p-card, .rule-card');
  if (!card) return;
  const rect = card.getBoundingClientRect();
  card.style.setProperty('--mx', (e.clientX - rect.left).toFixed(1) + 'px');
  card.style.setProperty('--my', (e.clientY - rect.top).toFixed(1) + 'px');
}, { passive: true });

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

    const auth = ov.auth || {};
    const badge = document.getElementById('authBadge');
    badge.textContent = auth.required ? '🔐 Token 鉴权已启用' : '🔓 本机免登模式';
    badge.className = 'pill' + (auth.required ? '' : ' warn');
    document.getElementById('logoutBtn').style.display = auth.required ? 'inline-flex' : 'none';

    UPTIME_SYNC = {
      host: ov.server.host,
      port: ov.server.port,
      baseSeconds: Number(ov.server.uptime_seconds || 0),
      syncedAt: Date.now(),
      online: true,
    };
    renderUptimeLine();

    renderKPIs(ov);
    const topoHovering = !!document.querySelector('#topoSvg.has-hover') || TOPO_VIEW.dragging;
    if (!silent || !topoHovering) {
      renderTopology(ov);
    }
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
  const kpis = [
    {
      cls: 'kpi-c-cyan',
      label: '自研生态插件',
      valHtml: `${onlineEco}<span class="denom">/ ${eco.length}</span>`,
      sub: `共发现插件 ${STATE.plugins.length} 个`,
    },
    {
      cls: 'kpi-c-indigo',
      label: '协议联动接入',
      valHtml: `${STATE.plugins.filter(p => p.protocol_version >= 1).length}`,
      sub: '支持 hub_status + hub_action',
    },
    {
      cls: 'kpi-c-green',
      label: '活跃联动管线',
      valHtml: `${activeRules}<span class="denom">/ ${STATE.rules.length}</span>`,
      sub: ov.auto_linkage_enabled ? '自动联动已开启' : '自动联动已暂停',
    },
    {
      cls: 'kpi-c-amber',
      label: '累计跨插件事件',
      valHtml: `${Number(ov.event_count || 0)}`,
      sub: `总触发联动 ${Number(ov.total_rule_triggers || 0)} 次`,
    },
    {
      cls: 'kpi-c-purple',
      label: '生态统一积分人数',
      valHtml: `${Number(ov.eco_users || 0)}`,
      sub: '跨游戏 / 群统计 / 运势 / 互动',
    },
  ];
  document.getElementById('kpiGrid').innerHTML = kpis.map(k =>
    `<div class="kpi ${k.cls}"><div class="label">${k.label}</div><div class="val">${k.valHtml}</div><div class="sub">${k.sub}</div></div>`
  ).join('');
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
    const linkCount = neighbors.size;
    tip.innerHTML = `<strong style="color:#f8fafc">${esc(p.icon)} ${esc(p.display_name)}</strong> `
      + `<span style="font-family:var(--font-mono);color:var(--muted);font-size:11px">v${esc(p.version)}</span>`
      + `<div style="color:var(--muted);font-size:11px;margin-top:3px">状态：${p.online ? '<span style="color:#34d399">在线</span>' : '<span style="color:#f87171">离线</span>'} · 关联节点 ${linkCount} 个 · 点击打开配置</div>`;
    tip.classList.add('show');
  }
}

function renderTopology(ov) {
  _initTopoCanvasEvents();
  const svg = document.getElementById('topoSvg');
  const CX = 600, CY = 270;
  const groups = {
    hub:        { color: '#38bdf8', items: [] },
    efficiency: { color: '#38bdf8', items: [] },
    guard:      { color: '#34d399', items: [] },
    ops:        { color: '#fbbf24', items: [] },
    fun:        { color: '#c084fc', items: [] },
  };
  STATE.plugins.filter(p => p.ecosystem).forEach(p => {
    const g = groups[p.category] || groups.efficiency;
    g.items.push(p);
  });

  const pos = {};
  // 中心核心节点
  groups.hub.items.forEach(p => {
    pos[p.name] = { x: CX, y: CY, color: groups.hub.color, plugin: p, isHub: true };
  });

  // 左侧：效率记忆（超 5 个自动拆分为外弧 + 内弧，彻底杜绝节点与标签重叠）
  const eff = groups.efficiency.items;
  if (eff.length <= 5) {
    _placeArc(eff, CX, CY, 445, 200, 136, 224, pos, groups.efficiency.color);
  } else {
    const outerN = Math.ceil(eff.length * 0.62);
    _placeArc(eff.slice(0, outerN), CX, CY, 480, 212, 136, 224, pos, groups.efficiency.color);
    _placeArc(eff.slice(outerN), CX, CY, 290, 152, 146, 214, pos, groups.efficiency.color);
  }

  // 上方弧：防扰安全
  _placeArc(groups.guard.items, CX, CY, 250, 196, 240, 300, pos, groups.guard.color);

  // 右侧弧：运维监控（同样支持超 5 个自动双弧展开）
  const ops = groups.ops.items;
  if (ops.length <= 5) {
    _placeArc(ops, CX, CY, 468, 204, -46, 46, pos, groups.ops.color);
  } else {
    const outerN = Math.ceil(ops.length * 0.62);
    _placeArc(ops.slice(0, outerN), CX, CY, 485, 212, -46, 46, pos, groups.ops.color);
    _placeArc(ops.slice(outerN), CX, CY, 295, 152, -34, 34, pos, groups.ops.color);
  }

  // 下方弧：娱乐积分
  _placeArc(groups.fun.items, CX, CY, 330, 198, 56, 124, pos, groups.fun.color);

  // 构建邻接表与去重平滑贝塞尔连线
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

  // 同时补充生态核心与各一级模块之间的微弱星型引力线，增强中枢拓扑空间感
  const hubName = groups.hub.items[0] ? groups.hub.items[0].name : '';
  let spokeHtml = '';
  if (hubName && pos[hubName]) {
    Object.entries(pos).forEach(([name, pt]) => {
      if (name === hubName) return;
      const sx = esc(hubName), tx = esc(name);
      spokeHtml += `<line x1="${CX}" y1="${CY}" x2="${pt.x.toFixed(1)}" y2="${pt.y.toFixed(1)}" stroke="${pt.color}" stroke-opacity="0.06" stroke-width="1" stroke-dasharray="2 6" data-src="${sx}" data-dst="${tx}"/>`;
    });
  }

  let edgesHtml = '';
  edgeMap.forEach(({ s, t, color }) => {
    const a = pos[s], b = pos[t];
    // 向中心轻微弯曲的三次贝塞尔控制点，曲线柔顺不生硬
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
    // 按中英文字符宽度动态估算微玻璃胶囊宽度
    let estW = 16;
    for (const ch of labelText) estW += ch.charCodeAt(0) > 127 ? 11.2 : 6.6;
    const pillW = Math.max(54, Math.min(132, Math.round(estW)));
    const pillH = 20;
    const labelY = isHub ? (pt.y + 52) : (pt.y + 29);

    if (isHub) {
      nodesHtml += `<g class="topo-node" data-node="${pNameEsc}" style="opacity:${opacity}" onclick="openPluginConfig('${pNameEsc}')">
        <circle cx="${pt.x}" cy="${pt.y}" r="54" fill="url(#hubCoreHalo)" opacity="0.9"/>
        <circle class="node-ring" cx="${pt.x}" cy="${pt.y}" r="${r}" fill="url(#hubCoreFill)" stroke="url(#hubCoreStroke)" stroke-width="2" filter="url(#glowCore)"/>
        <circle cx="${pt.x}" cy="${pt.y}" r="${r - 4}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="0.9"/>
        <text x="${pt.x}" y="${pt.y + 7}" text-anchor="middle" font-size="22">${esc(p.icon)}</text>
        <rect x="${(pt.x - pillW / 2).toFixed(1)}" y="${(labelY - 14).toFixed(1)}" width="${pillW}" height="${pillH + 2}" rx="11" fill="rgba(7,12,24,0.86)" stroke="rgba(125,211,252,0.38)" stroke-width="1"/>
        <text x="${pt.x}" y="${labelY}" text-anchor="middle" font-size="11.5" font-weight="600" fill="#f0f9ff">${esc(labelText)}</text>
      </g>`;
    } else {
      nodesHtml += `<g class="topo-node" data-node="${pNameEsc}" style="opacity:${opacity}" onclick="openPluginConfig('${pNameEsc}')">
        <circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="${r + 6}" fill="${pt.color}" fill-opacity="0.09"/>
        <circle class="node-ring" cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="${r}" fill="rgba(12,19,34,0.82)" stroke="${pt.color}" stroke-opacity="0.68" stroke-width="1.5"/>
        <circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="${r - 2}" fill="${pt.color}" fill-opacity="0.14"/>
        <text x="${pt.x.toFixed(1)}" y="${(pt.y + 5).toFixed(1)}" text-anchor="middle" font-size="13">${esc(p.icon)}</text>
        <rect x="${(pt.x - pillW / 2).toFixed(1)}" y="${(labelY - 13.5).toFixed(1)}" width="${pillW}" height="${pillH}" rx="10" fill="rgba(6,10,20,0.82)" stroke="rgba(255,255,255,0.11)" stroke-width="0.85"/>
        <text x="${pt.x.toFixed(1)}" y="${labelY.toFixed(1)}" text-anchor="middle" font-size="10.8" font-weight="500" fill="#e2e8f0">${esc(labelText)}</text>
      </g>`;
    }
  });

  TOPO_META = { nodes: pos, adj };

  const defsHtml = `<defs>
    <radialGradient id="hubCoreHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#6366f1" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="hubCoreFill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="rgba(56,189,248,0.34)"/>
      <stop offset="100%" stop-color="rgba(79,70,229,0.38)"/>
    </linearGradient>
    <linearGradient id="hubCoreStroke" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7dd3fc"/>
      <stop offset="100%" stop-color="#a5b4fc"/>
    </linearGradient>
    <filter id="glowCore" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>`;

  const radarHtml = `<g pointer-events="none">
    <circle class="topo-radar" cx="${CX}" cy="${CY}" r="142" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1" stroke-dasharray="3 7"/>
    <circle class="topo-radar-rev" cx="${CX}" cy="${CY}" r="228" fill="none" stroke="rgba(56,189,248,0.09)" stroke-width="1" stroke-dasharray="2 10"/>
    <ellipse cx="${CX}" cy="${CY}" rx="472" ry="206" fill="none" stroke="rgba(255,255,255,0.045)" stroke-width="1" stroke-dasharray="4 10"/>
  </g>`;

  svg.innerHTML = `${defsHtml}<g id="topoViewport">${radarHtml}${spokeHtml}${edgesHtml}${nodesHtml}</g>`;
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
  document.getElementById('pluginGrid').innerHTML = list.map(p => {
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
          ${(p.actions||[]).length ? `<button class="btn btn-sm btn-primary" onclick="jumpToAction('${pName}')">操作</button>` : ''}
        </div>
      </div>
    </div>`;
  }).join('');
}

function renderRules() {
  document.getElementById('ruleGrid').innerHTML = STATE.rules.map(r => {
    const rid = esc(r.id);
    return `<div class="rule-card">
      <div class="p-head">
        <div>
          <strong style="font-size:14px;color:#f8fafc">${esc(r.name)}</strong>
          <div class="p-meta" style="margin-top:2px">ID: ${rid} · ${r.builtin ? '内置管线' : '自定义规则'}</div>
        </div>
        <label class="switch">
          <input type="checkbox" ${r.enabled ? 'checked' : ''} onchange="toggleRule('${rid}', this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div style="font-size:12.5px;color:var(--text-soft);line-height:1.58">${esc(r.description || '')}</div>
      <div style="font-size:11.5px;color:var(--muted);display:flex;align-items:center;gap:6px;flex-wrap:wrap">
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
      <td style="white-space:nowrap;color:var(--muted);font-family:var(--font-mono);font-size:12px">${esc(String(e.ts||'').slice(5))}</td>
      <td style="font-family:var(--font-mono);font-size:12px">${esc(String(e.source||'').replace('astrbot_plugin_',''))}</td>
      <td><span class="code-inline">${esc(e.event_type)}</span></td>
      <td style="max-width:340px;word-break:break-all;font-size:12px;font-family:var(--font-mono);color:var(--text-soft)">${esc(JSON.stringify(e.payload || {}).slice(0,180))}</td>
      <td>${disp || '<span style="color:var(--muted);font-size:12px">已记录</span>'}</td>
    </tr>`;
  }).join('') : '<tr><td colspan="5" style="color:var(--muted);text-align:center;padding:24px">暂无跨插件事件</td></tr>';
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
  wrap.innerHTML = '<div style="color:var(--muted);padding:12px 0">加载数据中...</div>';
  try {
    const res = await api('/api/data/' + encodeURIComponent(panel));
    if (panel === 'points') {
      const lb = res.eco_leaderboard || [];
      wrap.innerHTML = `
        <h3 style="font-size:14px;margin-bottom:12px;color:#f8fafc">🏆 全生态统一积分榜（汇总游戏 / 群统计 / 运势 / 互动）</h3>
        <table><thead><tr><th>排名</th><th>用户</th><th>总积分</th><th>来源明细</th></tr></thead><tbody>
        ${lb.length ? lb.map((u, i) => `<tr><td style="font-family:var(--font-mono);color:var(--accent-bright)">#${i+1}</td><td>${esc(u.nickname)} <span style="font-family:var(--font-mono);font-size:11.5px;color:var(--muted)">(${esc(u.user_id)})</span></td><td style="font-family:var(--font-mono);font-variant-numeric:tabular-nums"><strong>${Number(u.total||0)}</strong></td><td style="font-family:var(--font-mono);font-size:12px;color:var(--text-soft)">${esc(JSON.stringify(u.sources||{}))}</td></tr>`).join('') : '<tr><td colspan="4" style="color:var(--muted);text-align:center;padding:20px">暂无积分记录</td></tr>'}
        </tbody></table>`;
    } else if (panel === 'antispam') {
      const bots = res.bot_ids || [];
      wrap.innerHTML = `
        <div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap;align-items:center;">
          <input type="text" id="newBotId" placeholder="输入 QQ/Bot ID 一键同步全生态">
          <button class="btn btn-primary btn-sm" onclick="markBotEverywhere()">标记为 Bot 并全生态同步</button>
          <span style="font-size:12px;color:var(--muted);font-family:var(--font-mono)">当前共享 Bot 名单：${esc(bots.join(', ') || '空')}</span>
        </div>
        <pre class="json-box">${esc(JSON.stringify(res.plugins, null, 2))}</pre>`;
    } else {
      wrap.innerHTML = `<pre class="json-box">${esc(JSON.stringify(res, null, 2))}</pre>`;
    }
  } catch (e) { wrap.innerHTML = `<div style="color:var(--red)">加载失败：${esc(e.message)}</div>`; }
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
  document.getElementById('cfgPluginList').innerHTML = list.map(p => {
    const pName = esc(p.name);
    return `<div class="side-item ${STATE.currentCfgPlugin===p.name?'active':''}" onclick="openPluginConfig('${pName}')">
      <span>${esc(p.icon)} ${esc(p.display_name)}</span>
      <span class="side-count">${Number(p.schema_count||0)}</span>
    </div>`;
  }).join('');
}

async function openPluginConfig(pname) {
  switchTab('config', document.querySelectorAll('.tab-btn')[3]);
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
          ${f.hint ? `<span style="color:var(--accent-bright)">${esc(f.hint)}</span>` : ''}
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
