"""
海帆智擎 · 智慧海洋绿色助航平台（拓展版）
说明：用于竞赛演示，不作为实船控制或官方CII核算依据。
"""
import math
from datetime import datetime
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="海帆智擎 · 智慧海洋绿色助航平台",
    page_icon=":ocean:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
/* ============================================================
   海帆智擎 · Forge Industrial Design System
   石墨黑 + 单一烬橙强调色  |  工业手册质感  |  极克制
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800;900&family=Geist+Mono:wght@400;500;600;700&display=swap');

/* ── Tokens ── */
:root{
  --bg0:#0c0c0c; --bg1:#111111; --bg2:#161616; --bg3:#1a1a1a;
  --surface:#1e1e1e; --surface2:#222222; --raised:#282828;
  --ember:#e07830; --ember-dim:#c06820; --ember-subtle:rgba(224,120,48,.10);
  --patina:#6b9e7a; --patina-subtle:rgba(107,158,122,.10);
  --gold:#c88830; --gold-subtle:rgba(200,136,48,.10);
  --forge-red:#c04848; --red-subtle:rgba(192,72,72,.10);
  --text:#d4d0c8; --text-dim:#a09890; --text-muted:#706860;
  --hairline:rgba(255,255,255,.06); --border:rgba(255,255,255,.10);
  --radius-sm:4px; --radius-md:6px; --radius-lg:8px;
}

/* ── Canvas ── */
html,body,.stApp{
  background:linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 50%, var(--bg2) 100%);
  color:var(--text);
}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background-image:radial-gradient(rgba(255,255,255,.015) 1px, transparent 1px);background-size:32px 32px;mask-image:linear-gradient(to bottom,rgba(0,0,0,.4),rgba(0,0,0,.08) 80%,transparent);}
.block-container{padding-top:1.2rem!important;padding-bottom:2.4rem!important;max-width:1520px!important;position:relative;z-index:1;}
header,#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;visibility:hidden!important;}

/* ── Typography ── */
h1,h2,h3,h4,h5,h6{color:var(--text)!important;letter-spacing:-.01em;font-weight:650;}
h1{font-size:clamp(1.7rem,3vw,2.4rem)!important;letter-spacing:-.02em;font-weight:750;}
h2{font-size:1.35rem!important;font-weight:700;}
h3{font-size:1.1rem!important;font-weight:650;}
p,li,span,label,div,button,input,select,textarea{font-family:"Geist","PingFang SC","Microsoft YaHei","Segoe UI",system-ui,sans-serif;}
[data-testid="stMarkdownContainer"] p{color:var(--text-dim);line-height:1.75;}

/* ── Sidebar ── */
[data-testid="stSidebar"]{
  background:var(--bg0)!important;
  border-right:1px solid var(--hairline)!important;
}
[data-testid="stSidebarContent"]{padding:1.2rem 1rem!important;}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{color:var(--text)!important;font-weight:700;}
[data-testid="stSidebar"] label{color:var(--text-dim)!important;font-size:12px;font-weight:600;}
[data-testid="stSidebar"] span,[data-testid="stSidebar"] p{color:var(--text-dim)!important;}
[data-testid="stSidebar"] hr{border-color:var(--hairline)!important;margin:14px 0!important;}

/* ── Buttons ── */
.stButton>button{
  width:100%;min-height:2.5rem;border-radius:var(--radius-sm)!important;
  border:1px solid var(--border)!important;
  background:var(--surface)!important;
  color:var(--text)!important;font-weight:600!important;letter-spacing:.01em!important;
  font-size:13px!important;transition:all .15s ease!important;
}
.stButton>button:hover{
  border-color:var(--ember)!important;
  background:var(--raised)!important;
  color:#fff!important;
}
.stButton>button:active{transform:scale(.985)!important;transition:all .06s ease!important;}
.stButton>button[kind="secondary"]{background:var(--bg2)!important;}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] div{color:var(--text-dim)!important;}
.stSlider [data-baseweb="slider"] [class*="track"]{background:rgba(255,255,255,.08)!important;height:4px!important;border-radius:2px!important;}
.stSlider [role="slider"]{
  background:var(--ember)!important;border:1px solid var(--ember-dim)!important;
  transition:background .15s ease!important;
}

/* ── Inputs ── */
.stNumberInput input,.stSelectbox [data-baseweb="select"]{
  background:var(--bg1)!important;color:var(--text)!important;
  border:1px solid var(--border)!important;border-radius:var(--radius-sm)!important;
  font-family:"Geist Mono","Cascadia Code",monospace!important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{gap:2px;border-bottom:1px solid var(--hairline);padding:0 2px;}
.stTabs [data-baseweb="tab"]{
  height:40px;padding:0 18px;
  background:transparent;border:1px solid transparent;
  border-bottom:none;border-radius:var(--radius-sm) var(--radius-sm) 0 0;
  color:var(--text-dim)!important;font-weight:550;font-size:13px;
  transition:all .15s ease;
}
.stTabs [data-baseweb="tab"]:hover{color:var(--text)!important;background:var(--bg2);}
.stTabs [aria-selected="true"]{
  background:var(--surface)!important;color:var(--ember)!important;font-weight:650;
  border-color:var(--hairline);border-bottom-color:var(--surface);
}

/* ── Cards ── */
.card{
  background:var(--surface);border:1px solid var(--hairline);border-radius:var(--radius-md);
  padding:18px 20px;min-height:118px;
}
.card.compact{min-height:auto;padding:12px 14px;}
.k-label{font-size:10px;color:var(--text-muted);margin-bottom:8px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;}
.k-value{font-size:30px;line-height:1.08;font-weight:750;color:var(--ember);font-feature-settings:"tnum" 1;font-family:"Geist Mono","Cascadia Code",monospace;}
.k-sub{font-size:11px;color:var(--text-muted);margin-top:8px;}

/* ── Status Pills ── */
.mode-pill{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:3px;border:1px solid var(--border);background:var(--bg2);color:var(--text-dim);font-weight:600;font-size:12px;}
.mode-pill.green{border-color:rgba(107,158,122,.30);color:#8cba94;}
.mode-pill.yellow{border-color:rgba(200,136,48,.30);color:#d4a860;}
.mode-pill.red{border-color:rgba(192,72,72,.30);color:#d47878;}
.section-title{font-size:18px;font-weight:700;color:var(--text);margin:6px 0 14px;letter-spacing:-.01em;}
.notice{background:var(--bg2);border:1px solid var(--hairline);border-radius:var(--radius-md);padding:14px 18px;color:var(--text-dim);line-height:1.8;}

/* ── Progress Bars ── */
.bar-wrap{height:6px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden;margin:8px 0 12px;}
.bar{height:100%;background:var(--ember);border-radius:3px;}

/* ── Status Chip ── */
.status-chip{display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(107,158,122,.25);background:var(--patina-subtle);color:#8cba94;border-radius:3px;padding:5px 10px;font-size:11px;font-weight:600;}
.dot{width:6px;height:6px;border-radius:2px;background:var(--patina);}

/* ── Compare Card ── */
.compare-card{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-md);padding:18px 20px;display:flex;justify-content:space-between;gap:18px;align-items:center;}
.compare-card .big{font-size:16px;color:var(--text);font-weight:700;}
.compare-card .good{color:#8cba94;}
.compare-card .line{height:5px;border-radius:3px;background:rgba(255,255,255,.06);overflow:hidden;margin-top:10px;}
.compare-card .line i{display:block;height:100%;background:var(--ember);}

/* ── Tables ── */
.table-wrap{border:1px solid var(--hairline);border-radius:var(--radius-sm);overflow:hidden;background:var(--surface);}
.table-wrap table{width:100%;border-collapse:collapse;font-size:13px;}
.table-wrap th,.table-wrap td{padding:10px 14px;border-bottom:1px solid var(--hairline);text-align:left;}
.table-wrap th{background:var(--bg2);color:var(--text-dim);font-weight:600;font-size:11px;letter-spacing:.04em;}
.table-wrap td{color:var(--text-dim);}
.table-wrap tr:last-child td{border-bottom:none;}
.table-wrap tbody tr:hover{background:var(--bg2);}

/* ── Tags ── */
.small-tag{display:inline-flex;padding:3px 9px;border-radius:3px;border:1px solid var(--hairline);background:var(--bg2);font-size:10px;color:var(--text-dim);font-weight:600;letter-spacing:.04em;}
.route-badge{display:flex;align-items:center;justify-content:space-between;gap:12px;border:1px solid var(--hairline);background:var(--bg2);padding:8px 12px;border-radius:var(--radius-sm);margin-top:10px;}
.route-track{height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden;margin-top:8px;}
.route-track i{display:block;height:100%;background:var(--ember);border-radius:3px;transition:width .6s ease;}
.toast-note{padding:10px 12px;border-radius:var(--radius-sm);border:1px solid var(--hairline);background:var(--bg2);color:var(--text-dim);line-height:1.7;}

/* ── Weather Grid ── */
.weather-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:10px 0 16px;}
.weather-card{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-sm);padding:14px;}
.weather-card:hover{border-color:var(--border);}
.weather-card b{display:block;color:var(--text);font-size:22px;margin-top:4px;font-family:"Geist Mono",monospace;font-weight:600;}
.status-ok{color:#8cba94;font-weight:700;}.status-warn{color:#d4a860;font-weight:700;}.status-bad{color:#d47878;font-weight:700;}

/* ── Pipeline ── */
.pipeline{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:12px;}
.pipe-node{border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);padding:12px;text-align:center;color:var(--text-dim);font-size:12px;}
.pipe-node:hover{border-color:var(--ember);}
.pipe-arrow{display:flex;align-items:center;justify-content:center;color:var(--ember);font-weight:700;font-size:16px;}

/* ── Twin Panel ── */
.twin-panel{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-md);padding:18px;}
.health-dot{display:inline-block;width:7px;height:7px;border-radius:2px;background:var(--patina);margin-right:6px;}
.health-dot.warn{background:var(--gold);}

/* ── Health Grid ── */
.health-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:12px 0 18px;}
.health-card{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-sm);padding:16px;}
.health-card span{display:block;font-size:10px;color:var(--text-muted);margin-bottom:8px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;}
.health-card b{display:block;font-size:28px;color:var(--ember);font-family:"Geist Mono",monospace;font-weight:700;}
.health-card small{display:block;margin-top:6px;color:var(--text-muted);}

/* ── Zone Chips ── */
.zone-chip{display:inline-block;padding:4px 10px;border-radius:3px;font-size:11px;font-weight:600;border:1px solid var(--hairline);}
.zone-high{background:var(--ember-subtle);color:#e8a870;border-color:rgba(224,120,48,.25);}
.zone-mid{background:var(--patina-subtle);color:#8cba94;border-color:rgba(107,158,122,.25);}
.zone-low{background:rgba(255,255,255,.04);color:#a09890;border-color:rgba(255,255,255,.08);}
.zone-stop{background:var(--red-subtle);color:#d47878;border-color:rgba(192,72,72,.25);}
.report-card{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-md);padding:18px;line-height:1.9;color:var(--text-dim);}

/* ── AI Engine ── */
.ai-engine-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:14px 0 18px;}
.ai-role-card{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-md);padding:16px;min-height:148px;}
.ai-role-card .role-icon{font-size:26px;margin-bottom:8px;font-weight:800;color:var(--ember);font-family:"Geist Mono",monospace;}
.ai-role-card h4{color:var(--text);margin:0 0 8px;font-size:15px;font-weight:650;}
.ai-role-card p{font-size:12px;line-height:1.7;color:var(--text-dim);}
.decision-box{border:1px solid rgba(224,120,48,.20);background:var(--surface);border-radius:var(--radius-md);padding:18px;}
.decision-box b{color:var(--text);}
.flow-row{display:grid;grid-template-columns:1fr 36px 1fr 36px 1fr;gap:8px;align-items:stretch;margin:12px 0;}
.flow-node{border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);padding:12px;text-align:center;color:var(--text-dim);font-size:13px;}
.flow-arrow{display:flex;align-items:center;justify-content:center;color:var(--ember);font-size:20px;font-weight:700;}
.model-badge{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--hairline);background:var(--bg2);border-radius:3px;padding:4px 10px;font-size:11px;color:var(--text-dim);font-weight:600;margin:3px 5px 3px 0;}
.warn-line{border-left:3px solid var(--gold);background:var(--bg2);padding:10px 14px;border-radius:0 var(--radius-sm) var(--radius-sm) 0;color:var(--text-dim);margin:10px 0;}
.safe-line{border-left:3px solid var(--ember);background:var(--bg2);padding:10px 14px;border-radius:0 var(--radius-sm) var(--radius-sm) 0;color:var(--text-dim);margin:10px 0;}

/* ── Operations ── */
.ops-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:16px;margin:12px 0 18px;}
.action-card{border:1px solid rgba(224,120,48,.25);background:var(--surface);border-radius:var(--radius-md);padding:18px;}
.action-card h3{margin:0 0 8px;color:var(--text);font-size:18px;font-weight:700;}
.action-card .action-main{font-size:28px;color:var(--ember);font-weight:800;letter-spacing:-.01em;margin:8px 0;}
.action-list{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:12px;}
.action-item{border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);padding:12px;color:var(--text-dim);line-height:1.6;}
.action-item b{color:var(--text);}
.sop-card{border:1px solid rgba(200,136,48,.25);background:var(--bg2);border-radius:var(--radius-md);padding:16px;line-height:1.8;color:#d4a860;}
.sop-card b{color:#e8c888;}
.workstep{display:flex;gap:12px;align-items:flex-start;margin:10px 0;padding:12px;border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);}
.workstep .num{width:26px;height:26px;border-radius:3px;display:grid;place-items:center;background:var(--ember);color:#0c0c0c;font-weight:800;flex:0 0 26px;font-size:13px;}
.workstep b{color:var(--text);}
.op-badge{display:inline-flex;align-items:center;border-radius:3px;padding:4px 10px;border:1px solid var(--hairline);background:var(--bg2);color:var(--text-dim);font-size:11px;font-weight:600;margin:2px 4px 2px 0;}
.op-badge.green{border-color:rgba(107,158,122,.25);color:#8cba94;}
.op-badge.yellow{border-color:rgba(200,136,48,.25);color:#d4a860;}
.op-badge.red{border-color:rgba(192,72,72,.25);color:#d47878;}

/* ── Highlight Grid ── */
.highlight-grid{display:grid;grid-template-columns:1.15fr 1.15fr 1fr;gap:14px;margin:16px 0 20px;}
.highlight-card{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-md);padding:18px;min-height:152px;}
.highlight-card h4{margin:10px 0 8px;color:var(--text);font-size:19px;font-weight:700;}
.highlight-card p{color:var(--text-dim);font-size:12px;line-height:1.7;margin:0 0 12px;}
.highlight-card .hl-num{font-size:13px;color:var(--ember);font-weight:700;font-family:"Geist Mono",monospace;}
.source-chip{display:inline-flex;margin-top:8px;padding:2px 8px;border-radius:3px;border:1px solid var(--hairline);background:var(--bg2);color:var(--text-dim);font-size:10px;font-weight:600;}

/* ── Evidence Web ── */
.part-legend-web{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 16px;}
.part-legend-web span{display:inline-flex;gap:5px;align-items:center;border:1px solid var(--hairline);background:var(--bg2);border-radius:3px;padding:4px 10px;color:var(--text-dim);font-size:11px;}
.part-legend-web b{color:var(--ember);}
.energy-flow-web{display:grid;grid-template-columns:1fr 30px 1fr 30px 1fr 30px 1fr;gap:6px;margin:12px 0 16px;}
.energy-flow-web .node{border:1px solid var(--hairline);border-radius:var(--radius-sm);padding:12px;text-align:center;background:var(--bg2);color:var(--text);font-weight:700;font-size:12px;}
.energy-flow-web .node:hover{border-color:var(--ember);}
.energy-flow-web .arrow{display:flex;align-items:center;justify-content:center;color:var(--ember);font-size:18px;font-weight:700;}
.evidence-web{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:12px 0 18px;}
.evidence-web-card{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-md);padding:16px;}
.evidence-web-card img{width:100%;height:260px;object-fit:contain;background:#fff;border-radius:var(--radius-sm);border:1px solid var(--hairline);}
.evidence-web-card h4{margin:10px 0 6px;color:var(--text);}
.evidence-web-card p{color:var(--text-dim);font-size:12px;line-height:1.7;}
.boundary-web{border:1px solid rgba(200,136,48,.20);background:var(--bg2);border-radius:var(--radius-md);padding:16px 18px;line-height:1.85;color:#d4a860;}
.boundary-web li{margin:7px 0;}
.linkage-web{border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-md);padding:14px 16px;line-height:1.8;color:var(--text-dim);margin:10px 0 18px;}

/* ── Landing Shell ── */
.landing-shell{display:grid;grid-template-columns:1.45fr .8fr;gap:18px;margin-bottom:16px;}
.landing-main,.landing-side{position:relative;overflow:hidden;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface);}
.landing-main{padding:32px 34px;min-height:290px;}
.landing-side{padding:22px;min-height:290px;}
.landing-title{position:relative;z-index:2;font-size:42px;line-height:1.06;font-weight:800;color:var(--text);letter-spacing:-.02em;margin:14px 0 10px;}
.landing-sub{position:relative;z-index:2;font-size:16px;font-weight:650;color:var(--ember);margin-bottom:8px;}
.landing-desc{position:relative;z-index:2;max-width:880px;color:var(--text-dim);line-height:1.85;font-size:13px;margin-bottom:18px;}
.kpi-strip{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px;}
.kpi-mini{border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);padding:12px 14px;}
.kpi-mini:hover{border-color:var(--ember);}
.kpi-mini span{display:block;color:var(--text-muted);font-size:10px;font-weight:600;margin-bottom:6px;letter-spacing:.05em;text-transform:uppercase;}
.kpi-mini b{display:block;color:var(--ember);font-size:22px;line-height:1.08;font-family:"Geist Mono",monospace;font-weight:700;}
.kpi-mini small{display:block;color:var(--text-muted);font-size:10px;margin-top:5px;}
.workflow-ribbon{position:relative;z-index:2;margin-top:16px;border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);padding:11px;color:var(--text-dim);font-weight:600;text-align:center;letter-spacing:.01em;font-size:12px;}
.side-title{font-size:17px;color:var(--text);font-weight:700;margin:14px 0 12px;}
.side-item{display:flex;justify-content:space-between;gap:12px;align-items:center;border-bottom:1px solid var(--hairline);padding:9px 0;color:var(--text-dim);}
.side-item span{color:var(--text-muted);font-size:12px;font-weight:600;}
.side-item b{color:var(--text);font-size:14px;text-align:right;}
.route-card-polish{margin-top:14px;border:1px solid rgba(224,120,48,.20);background:var(--bg2);border-radius:var(--radius-sm);padding:12px;}
.route-card-polish .route-top{display:flex;justify-content:space-between;color:var(--text);font-weight:700;}
.route-card-polish .route-track{margin-top:10px;height:5px;background:rgba(255,255,255,.06);}
.scenario-panel{border:1px solid var(--hairline);border-radius:var(--radius-md);padding:16px 18px;margin:12px 0 16px;background:var(--surface);}
.scenario-head{display:flex;justify-content:space-between;gap:14px;align-items:flex-end;margin-bottom:12px;}
.scenario-head h3{margin:0;color:var(--text);font-size:18px;}
.scenario-head p{margin:5px 0 0;color:var(--text-dim);font-size:12px;}
.demo-flow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:8px 0 20px;}
.demo-step{border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);padding:14px 15px;}
.demo-step:hover{border-color:var(--ember);}
.demo-step .num{display:inline-flex;width:26px;height:26px;border-radius:3px;align-items:center;justify-content:center;background:var(--ember);color:#0c0c0c;font-weight:800;margin-bottom:8px;font-size:13px;}
.demo-step h4{margin:0 0 6px;color:var(--text);font-size:15px;}
.demo-step p{margin:0;color:var(--text-dim);font-size:11px;line-height:1.7;}

/* ── Portal / Data Status ── */
.portal-top{display:flex;justify-content:flex-end;margin:-2px 0 12px;}
.portal-top a{text-decoration:none;display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:var(--radius-sm);background:var(--bg2);border:1px solid var(--hairline);color:var(--text-dim);font-weight:600;font-size:12px;transition:all .15s ease;}
.portal-top a:hover{border-color:var(--ember);color:var(--text);}
.data-status-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:12px 0 18px;}
.data-status-item{border:1px solid var(--hairline);background:var(--surface);border-radius:var(--radius-sm);padding:13px 15px;}
.data-status-item small{display:block;color:var(--text-muted);font-size:10px;margin-bottom:6px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;}
.data-status-item b{display:block;color:var(--text);font-size:14px;line-height:1.5;}
.reason-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:12px 0 16px;}
.reason-card{border:1px solid var(--hairline);background:var(--bg2);border-radius:var(--radius-sm);padding:14px 15px;line-height:1.7;color:var(--text-dim);}
.reason-card:hover{border-color:var(--border);}
.reason-card b{display:block;color:var(--text);margin-bottom:6px;font-size:14px;}
.term-chip{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--hairline);background:var(--bg2);border-radius:3px;padding:4px 10px;color:var(--text-dim);font-size:11px;font-weight:600;margin:2px 5px 2px 0;}

/* ── Hero (old) ── */
.hero{position:relative;overflow:hidden;border:1px solid var(--hairline);border-radius:var(--radius-md);padding:28px 30px;margin-bottom:18px;background:var(--surface);}
.hero-title{font-size:40px;line-height:1.06;font-weight:800;color:var(--text);margin:0;letter-spacing:-.02em;}
.hero-sub{margin-top:12px;font-size:15px;color:var(--ember);font-weight:650;}
.hero-desc{max-width:850px;margin-top:10px;color:var(--text-dim);font-size:13px;line-height:1.8;}
.ai-orb{width:72px;height:72px;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;background:var(--ember);color:#0c0c0c;}
.ship-svg{width:100%;min-height:240px;border-radius:var(--radius-sm);background:var(--bg1);border:1px solid var(--hairline);overflow:hidden;}
.footer-note{color:var(--text-muted);font-size:10px;text-align:right;margin-top:12px;}

/* ── Shimmer ── */
.shimmer-bar{height:3px;background:linear-gradient(90deg,transparent 0%,rgba(224,120,48,.25) 50%,transparent 100%);background-size:200% 100%;animation:shimmer 2s linear infinite;border-radius:2px;margin-top:4px;}
@keyframes shimmer{0%{background-position:-200% 0;}100%{background-position:200% 0;}}

/* ── Responsive ── */
@media(max-width:1150px){
  .landing-shell,.demo-flow{grid-template-columns:1fr;}
  .kpi-strip{grid-template-columns:repeat(2,1fr);}
  .highlight-grid{grid-template-columns:1fr!important;}
}
@media(max-width:1100px){
  .weather-grid,.pipeline,.health-grid,.ai-engine-grid,.data-status-strip{grid-template-columns:repeat(2,1fr);}
  .ops-grid,.action-list,.evidence-web,.reason-grid{grid-template-columns:1fr;}
  .compare-card{flex-direction:column;text-align:center;}
}

</style>
""",
    unsafe_allow_html=True,
)


try:
    _portal_href = (Path(__file__).parent / "index.html").resolve().as_uri()
except Exception:
    _portal_href = "index.html"
st.markdown(f'<div class="portal-top"><a href="{_portal_href}" target="_blank">← 返回统一入口页</a></div>', unsafe_allow_html=True)


ROUTE_PRESETS = {
    "印度洋季风": dict(wind_speed=12.5, wind_angle=85, ship_speed=14.0, engine_load=74, back_pressure=3.2, sea_state=3, route_distance=5200),
    "南海航段": dict(wind_speed=9.0, wind_angle=70, ship_speed=13.5, engine_load=68, back_pressure=2.8, sea_state=2, route_distance=1200),
    "北大西洋": dict(wind_speed=16.0, wind_angle=110, ship_speed=15.0, engine_load=82, back_pressure=3.9, sea_state=5, route_distance=3400),
    "中东—东亚": dict(wind_speed=12.6, wind_angle=128, ship_speed=14.2, engine_load=72, back_pressure=3.2, sea_state=2, route_distance=6200),
}
DEMO_SCENARIOS = {
    "横风 12m/s · 高效助航": dict(wind_speed=12.0, wind_angle=90, ship_speed=14.0, engine_load=72, back_pressure=3.2, sea_state=3, device_count=4, note="高效助航，推力最大"),
    "微风 5m/s · 低收益待机": dict(wind_speed=5.0, wind_angle=60, ship_speed=14.0, engine_load=70, back_pressure=3.2, sea_state=2, device_count=4, note="自动待机，避免无效取能"),
    "背压 4.8kPa · 主机保护": dict(wind_speed=11.0, wind_angle=95, ship_speed=14.0, engine_load=78, back_pressure=4.8, sea_state=3, device_count=4, note="触发保护，旁通优先"),
    "海况 7级 · 安全锁定": dict(wind_speed=14.0, wind_angle=105, ship_speed=13.5, engine_load=74, back_pressure=3.6, sea_state=7, device_count=4, note="安全锁定，全旁通"),
}
DEFAULTS = ROUTE_PRESETS["中东—东亚"].copy()
DEFAULTS.update(device_count=4, dwt=150000, ship_type="散货船/油轮", annual_days=250)
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
st.session_state.setdefault("preset_name", "中东—东亚")
st.session_state.setdefault("demo_name", "")


def set_route(name):
    for k, v in ROUTE_PRESETS[name].items():
        st.session_state[k] = v
    st.session_state["preset_name"] = name
    st.session_state["demo_name"] = ""


def set_demo(name):
    cfg = DEMO_SCENARIOS[name]
    for k, v in cfg.items():
        if k != "note":
            st.session_state[k] = v
    st.session_state["preset_name"] = name
    st.session_state["demo_name"] = name


def calc_single_thrust(wind_speed, wind_angle, ship_speed, rpm, sea_state):
    ship_ms = ship_speed * 0.5144
    rad = math.radians(wind_angle)
    rel_x = wind_speed * math.cos(rad) - ship_ms
    rel_y = wind_speed * math.sin(rad)
    rel_wind = math.sqrt(rel_x ** 2 + rel_y ** 2)
    side = abs(math.sin(rad))
    tip_speed = rpm * 2 * math.pi / 60 * 3.5
    spin_ratio = np.clip(tip_speed / max(wind_speed, 1.0), 0, 5)
    rho, D, H = 1.225, 7.0, 24.0
    area = D * H
    cl = np.clip(0.8 + 1.1 * spin_ratio, 0.5, 6.5)
    sea_factor = max(0.55, 1 - 0.06 * max(sea_state - 2, 0))
    lift = 0.5 * rho * area * cl * rel_wind ** 2
    thrust = lift * side * sea_factor / 1000
    return float(thrust), float(rel_wind), float(spin_ratio), float(cl)


def decide_mode(wind_speed, wind_angle, back_pressure, sea_state):
    side = abs(math.sin(math.radians(wind_angle)))
    if sea_state >= 7 or wind_speed > 24 or wind_speed < 2:
        return "恶劣海况安全模式", "极端风况/海况，入口阀关闭，旁通阀全开。"
    if back_pressure >= 4.5:
        return "主机保护模式", "排气背压接近演示阈值，优先保证主机排烟安全。"
    if wind_speed < 6 or side < 0.30:
        return "低收益待机模式", "风速或侧风分量不足，建议低速或间歇运行。"
    return "高效助航模式", "风况适合助航，建议进入高效取能与推力输出状态。"


def recommend_rpm(wind_speed, mode):
    if mode == "高效助航模式":
        return int(np.clip(wind_speed * 11.5, 80, 220))
    if mode == "低收益待机模式":
        return int(np.clip(wind_speed * 7, 25, 90))
    if mode == "主机保护模式":
        return int(np.clip(wind_speed * 3.5, 0, 45))
    return 0


def valve_openings(mode, back_pressure, sea_state):
    if mode == "高效助航模式":
        inlet = np.clip(78 - 4 * max(back_pressure - 3.0, 0), 55, 92)
        bypass = 100 - inlet
    elif mode == "低收益待机模式":
        inlet, bypass = 18, 82
    elif mode == "主机保护模式":
        inlet, bypass = 12, 88
    else:
        inlet, bypass = 0, 100
    if sea_state >= 5 and mode != "恶劣海况安全模式":
        inlet *= 0.72
        bypass = min(100, 100 - inlet + 12)
    return float(inlet), float(bypass)


def cii_rating(value, ship_type):
    thresholds = {
        "散货船/油轮": [3.8, 4.6, 5.4, 6.4],
        "集装箱船": [6.5, 7.6, 8.8, 10.2],
        "LNG运输船": [7.2, 8.4, 9.6, 11.2],
    }[ship_type]
    if value <= thresholds[0]:
        return "A"
    if value <= thresholds[1]:
        return "B"
    if value <= thresholds[2]:
        return "C"
    if value <= thresholds[3]:
        return "D"
    return "E"


def cii_demo(dwt, route_distance, ship_speed, annual_days, ship_type, save_rate):
    annual_nm = max(route_distance, ship_speed * 24 * annual_days)
    base_fuel_t_day = 32 * (dwt / 50000) ** 0.55 * (ship_speed / 14) ** 3
    annual_fuel = base_fuel_t_day * annual_days
    co2_factor = 3.114
    base_co2 = annual_fuel * co2_factor
    improved_co2 = base_co2 * (1 - save_rate / 100)
    base_cii = base_co2 * 1_000_000 / (dwt * annual_nm)
    improved_cii = improved_co2 * 1_000_000 / (dwt * annual_nm)
    return dict(
        annual_nm=annual_nm,
        base_fuel=annual_fuel,
        improved_fuel=annual_fuel * (1 - save_rate / 100),
        base_co2=base_co2,
        improved_co2=improved_co2,
        base_cii=base_cii,
        improved_cii=improved_cii,
        base_rating=cii_rating(base_cii, ship_type),
        improved_rating=cii_rating(improved_cii, ship_type),
    )


def metric_card(label, value, sub="", source="演示工况"):
    return f"<div class='card'><div class='k-label'>{label}</div><div class='k-value'>{value}</div><div class='k-sub'>{sub}</div><div class='source-chip'>{source}</div></div>"


def html_table(df: pd.DataFrame):
    head = "".join([f"<th>{c}</th>" for c in df.columns])
    body_rows = []
    for _, row in df.iterrows():
        tds = "".join([f"<td>{row[c]}</td>" for c in df.columns])
        body_rows.append(f"<tr>{tds}</tr>")
    body = "".join(body_rows)
    return f"<div class='table-wrap'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def alt_line(df, x, ys, title=""):
    base = df.melt(x, ys, var_name="指标", value_name="数值")
    return (
        alt.Chart(base)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X(f"{x}:Q", title=x, axis=alt.Axis(labelColor="#8eb6d5", titleColor="#d4b888", gridColor="rgba(148,163,184,.12)")),
            y=alt.Y("数值:Q", title=None, axis=alt.Axis(labelColor="#8eb6d5", gridColor="rgba(148,163,184,.12)")),
            color=alt.Color("指标:N", scale=alt.Scale(range=["#22d3ee", "#7eb798", "#fbbf24"]), legend=alt.Legend(labelColor="#e8d8c0", titleColor="#e8d8c0")),
            tooltip=[x, "指标", alt.Tooltip("数值:Q", format=".1f")],
        )
        .properties(height=300, title=title)
        .configure(background="transparent")
        .configure_view(strokeOpacity=0)
        .configure_title(color="#eff9ff", fontSize=16, anchor="start")
    )


def alt_bar(df, x, ys, title=""):
    base = df.melt(x, ys, var_name="指标", value_name="数值")
    return (
        alt.Chart(base)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X(f"{x}:O", title=x, axis=alt.Axis(labelColor="#8eb6d5", titleColor="#d4b888", grid=False)),
            y=alt.Y("数值:Q", title=None, axis=alt.Axis(labelColor="#8eb6d5", gridColor="rgba(148,163,184,.12)")),
            color=alt.Color("指标:N", scale=alt.Scale(range=["#22d3ee", "#7eb798"]), legend=alt.Legend(labelColor="#e8d8c0", titleColor="#e8d8c0")),
            tooltip=[x, "指标", alt.Tooltip("数值:Q", format=".1f")],
        )
        .properties(height=310, title=title)
        .configure(background="transparent")
        .configure_view(strokeOpacity=0)
        .configure_title(color="#eff9ff", fontSize=16, anchor="start")
    )



def sankey_figure(inlet, bypass):
    rotor = inlet * 0.88
    thrust = rotor * 0.82
    fig = go.Figure(
        data=[go.Sankey(
            arrangement="snap",
            node=dict(
                pad=18,
                thickness=18,
                line=dict(color="rgba(255,255,255,.14)", width=1),
                label=[
                    "主机废气\n100%",
                    "轴流透平\n取能",
                    "旁通排出\n安全余量",
                    "滚筒帆旋转",
                    "马格努斯推力"
                ],
                color=["#3b82b6", "#e8b866", "#8a8278", "#5eead4", "#22d3ee"],
            ),
            link=dict(
                source=[0, 0, 1, 3],
                target=[1, 2, 3, 4],
                value=[float(inlet), float(bypass), float(rotor), float(thrust)],
                color=[
                    "rgba(56,189,248,.58)",
                    "rgba(148,163,184,.26)",
                    "rgba(94,234,212,.48)",
                    "rgba(34,211,238,.52)"
                ],
            ),
        )]
    )
    fig.update_layout(
        title=dict(text="废气余能—滚筒帆—推力输出能量流", font=dict(color="#eaf6ff", size=16)),
        font=dict(color="#f0e8d8", size=12, family="Microsoft YaHei"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=12, r=12, t=48, b=8),
        height=360,
    )
    return fig



# =========================
# SMART OCEAN EXTENSIONS
# =========================
# 航线数据库只保留四条主航线；每条航线包含典型航路节点。
# 运行时可尝试接入 Open-Meteo Weather API 与 Marine API 获取实时风浪/海流数据；
# 若联网失败或接口暂不可用，则自动回退到本地演示样本，保证演示稳定。
ROUTE_DATABASE = {
    "印度洋季风": {
        "desc": "从西印度洋至东印度洋，适合展示季风侧风窗口与滚筒帆高效助航。",
        "distance_nm": 5200,
        "nodes": [
            {"name": "亚丁湾外海", "lat": 12.6, "lon": 50.5, "stage": "离港外海"},
            {"name": "索马里海盆", "lat": 7.8, "lon": 57.2, "stage": "西印度洋"},
            {"name": "赤道季风带", "lat": 2.5, "lon": 66.0, "stage": "季风核心区"},
            {"name": "中印度洋", "lat": -1.5, "lon": 78.0, "stage": "远洋巡航"},
            {"name": "安达曼海西侧", "lat": 7.2, "lon": 92.0, "stage": "东印度洋"},
            {"name": "马六甲入口", "lat": 5.7, "lon": 96.0, "stage": "狭水道前"},
        ],
    },
    "南海航段": {
        "desc": "覆盖南海北部—中部—南部海域，适合展示近海风浪变化、台风季风险和航线适配。",
        "distance_nm": 1200,
        "nodes": [
            {"name": "北部湾口", "lat": 20.0, "lon": 109.0, "stage": "近海入口"},
            {"name": "南海北部", "lat": 18.0, "lon": 113.0, "stage": "北部航段"},
            {"name": "西沙外海", "lat": 16.2, "lon": 112.6, "stage": "岛礁外海"},
            {"name": "南海中部", "lat": 13.0, "lon": 115.0, "stage": "中部航段"},
            {"name": "南沙北缘", "lat": 10.5, "lon": 116.5, "stage": "南部航段"},
            {"name": "巴士/苏禄方向", "lat": 8.6, "lon": 119.0, "stage": "出海通道"},
        ],
    },
    "北大西洋": {
        "desc": "北美东岸至西欧近海，适合展示高纬大风浪航线下的安全锁定与风助收益平衡。",
        "distance_nm": 3400,
        "nodes": [
            {"name": "北美东岸外海", "lat": 40.7, "lon": -73.9, "stage": "离港外海"},
            {"name": "纽芬兰东南", "lat": 43.0, "lon": -55.0, "stage": "西大西洋"},
            {"name": "北大西洋中部", "lat": 46.5, "lon": -38.0, "stage": "高风浪区"},
            {"name": "亚速尔北部", "lat": 43.0, "lon": -28.0, "stage": "中东大西洋"},
            {"name": "比斯开湾外缘", "lat": 47.5, "lon": -15.0, "stage": "欧洲外海"},
            {"name": "西欧近海", "lat": 50.5, "lon": -6.5, "stage": "近港航段"},
        ],
    },
    "中东—东亚": {
        "desc": "波斯湾/阿曼湾—印度洋—马六甲—南海—东亚，适合展示长航线节能、CII改善和多海区策略切换。",
        "distance_nm": 6200,
        "nodes": [
            {"name": "霍尔木兹外海", "lat": 25.2, "lon": 56.4, "stage": "离港外海"},
            {"name": "阿拉伯海", "lat": 18.5, "lon": 64.0, "stage": "西印度洋"},
            {"name": "印度洋季风区", "lat": 7.5, "lon": 78.5, "stage": "季风侧风区"},
            {"name": "马六甲入口", "lat": 5.0, "lon": 95.0, "stage": "狭水道前"},
            {"name": "南海中部", "lat": 14.5, "lon": 112.0, "stage": "南海航段"},
            {"name": "东亚目的港外海", "lat": 22.3, "lon": 121.0, "stage": "近港航段"},
        ],
    },
}
FOUR_ROUTE_NAMES = list(ROUTE_DATABASE.keys())


def resolve_route_name(name: str) -> str:
    """保证气象数据库只使用四条主航线。四场景演示不作为独立航线。"""
    if name in ROUTE_DATABASE:
        return name
    if "微风" in name:
        return "南海航段"
    if "海况" in name and "7" in name:
        return "北大西洋"
    if "横风" in name:
        return "印度洋季风"
    return "中东—东亚"


def route_nodes_df(route_name: str) -> pd.DataFrame:
    route_name = resolve_route_name(route_name)
    rows = []
    for i, node in enumerate(ROUTE_DATABASE[route_name]["nodes"], start=1):
        rows.append({"序号": i, "航线": route_name, **node})
    return pd.DataFrame(rows)


def interpolate_path(points, n=18):
    lats, lons, names, stages = [], [], [], []
    if len(points) < 2:
        return pd.DataFrame()
    steps_per_segment = max(2, n // (len(points) - 1))
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        lat1, lon1, name1, stage1 = p1["lat"], p1["lon"], p1["name"], p1["stage"]
        lat2, lon2, name2, stage2 = p2["lat"], p2["lon"], p2["name"], p2["stage"]
        for j in range(steps_per_segment):
            f = j / steps_per_segment
            lats.append(lat1 + (lat2 - lat1) * f)
            lons.append(lon1 + (lon2 - lon1) * f)
            names.append(name1 if f < 0.5 else name2)
            stages.append(stage1 if f < 0.5 else stage2)
    last = points[-1]
    lats.append(last["lat"]); lons.append(last["lon"]); names.append(last["name"]); stages.append(last["stage"])
    return pd.DataFrame({"lat": lats[:n], "lon": lons[:n], "海区": names[:n], "航段": stages[:n]})


def wave_to_sea_state(wave_height_m):
    """演示用浪高-海况等级映射，非正式海况判定。"""
    if pd.isna(wave_height_m):
        return 3
    if wave_height_m < 0.1:
        return 0
    if wave_height_m < 0.5:
        return 2
    if wave_height_m < 1.25:
        return 3
    if wave_height_m < 2.5:
        return 4
    if wave_height_m < 4.0:
        return 5
    if wave_height_m < 6.0:
        return 6
    if wave_height_m < 9.0:
        return 7
    return 8


def strategy_from_conditions(wind_speed, wind_dir, wave_height, sea_state_level, current_kn=0.0):
    side_factor = abs(math.sin(math.radians(float(wind_dir) if not pd.isna(wind_dir) else 90)))
    wind_assist = float(np.clip((wind_speed or 0) * side_factor * (1 - sea_state_level * 0.035), 0, 25))
    risk_score = 0
    if wave_height >= 4.0 or sea_state_level >= 7:
        risk_score += 3
    elif wave_height >= 2.5 or sea_state_level >= 5:
        risk_score += 2
    elif wave_height >= 1.25:
        risk_score += 1
    if wind_speed >= 18:
        risk_score += 1
    if current_kn >= 1.2:
        risk_score += 1
    if risk_score >= 4:
        risk = "高"; strategy = "安全锁定"
    elif risk_score >= 2:
        risk = "中"; strategy = "保守助航"
    elif wind_assist >= 8:
        risk = "低"; strategy = "高效助航"
    elif wind_assist >= 4:
        risk = "低"; strategy = "低速观测"
    else:
        risk = "低"; strategy = "待机节能"
    return wind_assist, risk, strategy


def _safe_current(obj, key, default=np.nan):
    try:
        return obj.get("current", {}).get(key, default)
    except Exception:
        return default


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_open_meteo_route(route_name: str):
    """获取四条航线节点的实时/近实时气象与海况。失败则抛出异常，外层回退到样本库。"""
    route_name = resolve_route_name(route_name)
    nodes = ROUTE_DATABASE[route_name]["nodes"]
    lat_str = ",".join([str(n["lat"]) for n in nodes])
    lon_str = ",".join([str(n["lon"]) for n in nodes])
    weather_params = {
        "latitude": lat_str,
        "longitude": lon_str,
        "current": "wind_speed_10m,wind_direction_10m,wind_gusts_10m",
        "wind_speed_unit": "ms",
        "timezone": "UTC",
        "cell_selection": "sea",
    }
    marine_params = {
        "latitude": lat_str,
        "longitude": lon_str,
        "current": "wave_height,wave_direction,wave_period,ocean_current_velocity,ocean_current_direction,sea_surface_temperature",
        "length_unit": "metric",
        "timezone": "UTC",
        "cell_selection": "sea",
    }
    w_resp = requests.get("https://api.open-meteo.com/v1/forecast", params=weather_params, timeout=8)
    m_resp = requests.get("https://marine-api.open-meteo.com/v1/marine", params=marine_params, timeout=8)
    w_resp.raise_for_status(); m_resp.raise_for_status()
    w_json = w_resp.json(); m_json = m_resp.json()
    if isinstance(w_json, dict):
        w_json = [w_json]
    if isinstance(m_json, dict):
        m_json = [m_json]
    rows = []
    for i, node in enumerate(nodes):
        w = w_json[i] if i < len(w_json) else {}
        m = m_json[i] if i < len(m_json) else {}
        wind_speed = _safe_current(w, "wind_speed_10m")
        wind_dir = _safe_current(w, "wind_direction_10m")
        wind_gust = _safe_current(w, "wind_gusts_10m")
        wave_h = _safe_current(m, "wave_height")
        wave_dir = _safe_current(m, "wave_direction")
        wave_period = _safe_current(m, "wave_period")
        cur_ms = _safe_current(m, "ocean_current_velocity")
        cur_dir = _safe_current(m, "ocean_current_direction")
        sst = _safe_current(m, "sea_surface_temperature")
        cur_kn = float(cur_ms) * 1.94384 if not pd.isna(cur_ms) else np.nan
        sea_lvl = wave_to_sea_state(wave_h)
        potential, risk, strategy = strategy_from_conditions(float(wind_speed or 0), float(wind_dir or 0), float(wave_h or 0), sea_lvl, 0 if pd.isna(cur_kn) else cur_kn)
        update_time = _safe_current(w, "time", datetime.utcnow().strftime("%Y-%m-%dT%H:%M"))
        rows.append({
            "序号": i + 1,
            "航线": route_name,
            "海区": node["name"],
            "航段": node["stage"],
            "lat": node["lat"],
            "lon": node["lon"],
            "风速(m/s)": round(float(wind_speed), 1) if not pd.isna(wind_speed) else np.nan,
            "阵风(m/s)": round(float(wind_gust), 1) if not pd.isna(wind_gust) else np.nan,
            "风向(°)": int(round(float(wind_dir))) if not pd.isna(wind_dir) else np.nan,
            "浪高(m)": round(float(wave_h), 1) if not pd.isna(wave_h) else np.nan,
            "浪向(°)": int(round(float(wave_dir))) if not pd.isna(wave_dir) else np.nan,
            "浪周期(s)": round(float(wave_period), 1) if not pd.isna(wave_period) else np.nan,
            "流速(kn)": round(float(cur_kn), 2) if not pd.isna(cur_kn) else np.nan,
            "流向(°)": int(round(float(cur_dir))) if not pd.isna(cur_dir) else np.nan,
            "海温(℃)": round(float(sst), 1) if not pd.isna(sst) else np.nan,
            "海况等级": sea_lvl,
            "风助潜力": round(potential, 1),
            "风险等级": risk,
            "建议策略": strategy,
            "数据源": "Open-Meteo实时",
            "更新时间": update_time,
        })
    return pd.DataFrame(rows)


def build_route_weather_sample(route_name, wind_speed, wind_angle, sea_state):
    route_name = resolve_route_name(route_name)
    points = ROUTE_DATABASE[route_name]["nodes"]
    df = interpolate_path(points, 18)
    if df.empty:
        return df
    idx = np.arange(len(df))
    base_wind = wind_speed + 2.2 * np.sin(idx / 2.7) + 0.7 * np.cos(idx / 3.3)
    df.insert(0, "航线", route_name)
    df.insert(0, "序号", np.arange(1, len(df) + 1))
    df["风速(m/s)"] = np.clip(base_wind, 0.5, 28).round(1)
    df["阵风(m/s)"] = np.clip(df["风速(m/s)"] + 2.6 + 0.5 * np.cos(idx / 2), 0.8, 34).round(1)
    df["风向(°)"] = ((wind_angle + idx * 7 + 12 * np.sin(idx / 3)) % 360).round(0).astype(int)
    df["浪高(m)"] = np.clip(0.45 + sea_state * 0.32 + 0.18 * np.sin(idx / 2), 0.2, 7.5).round(1)
    df["浪向(°)"] = ((df["风向(°)"] + 35 + idx * 2) % 360).astype(int)
    df["浪周期(s)"] = np.clip(4.0 + df["浪高(m)"] * 1.6, 3.0, 14.0).round(1)
    df["流速(kn)"] = np.clip(0.4 + 0.25 * np.cos(idx / 2.5), 0.1, 1.3).round(2)
    df["流向(°)"] = ((df["风向(°)"] + 80) % 360).astype(int)
    df["海温(℃)"] = np.clip(28 - np.abs(df["lat"]) * 0.18 + 0.4 * np.sin(idx / 2), 4, 31).round(1)
    df["海况等级"] = np.clip(np.round(sea_state + 0.8 * np.sin(idx / 4)), 0, 9).astype(int)
    potentials, risks, strategies = [], [], []
    for _, row in df.iterrows():
        p, r, s = strategy_from_conditions(row["风速(m/s)"], row["风向(°)"], row["浪高(m)"], row["海况等级"], row["流速(kn)"])
        potentials.append(round(p, 1)); risks.append(r); strategies.append(s)
    df["风助潜力"] = potentials
    df["风险等级"] = risks
    df["建议策略"] = strategies
    df["数据源"] = "本地演示样本"
    df["更新时间"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return df


def get_route_weather(route_name, wind_speed, wind_angle, sea_state, use_live=True):
    route_name = resolve_route_name(route_name)
    if use_live:
        try:
            live = fetch_open_meteo_route(route_name)
            if not live.empty:
                return live, "live", "可接入 Open-Meteo 实时风浪/海流数据；当前演示以本地样本库回放为主。"
        except Exception as exc:
            return build_route_weather_sample(route_name, wind_speed, wind_angle, sea_state), "fallback", f"实时海况接口暂不可用，已自动切换为本地演示样本。原因：{type(exc).__name__}"
    return build_route_weather_sample(route_name, wind_speed, wind_angle, sea_state), "sample", "当前使用本地演示样本库。"


def route_weather_map(df):
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=df["lon"], lat=df["lat"], mode="lines+markers+text",
        text=df["海区"], textposition="top center",
        marker=dict(size=10, color=df["风助潜力"], colorscale=[[0,"#f5e6d0"],[0.35,"#d4b896"],[0.7,"#e8b866"],[1,"#d4983a"]], colorbar=dict(title="风助潜力"), line=dict(width=1, color="#f0e8d8")),
        line=dict(width=3, color="#22d3ee"),
        hovertemplate="%{text}<br>风速 %{customdata[0]} m/s<br>浪高 %{customdata[1]} m<br>流速 %{customdata[3]} kn<br>策略 %{customdata[2]}<extra></extra>",
        customdata=np.stack([df["风速(m/s)"], df["浪高(m)"], df["建议策略"], df["流速(kn)"], df["风险等级"]], axis=-1),
        name="航线气象点"
    ))
    fig.update_geos(
        projection_type="natural earth",
        showcountries=True, countrycolor="rgba(148,163,184,.28)",
        showland=True, landcolor="rgba(36,76,108,.78)",
        showocean=True, oceancolor="rgba(8,44,74,.92)",
        lataxis=dict(showgrid=True, gridcolor="rgba(56,189,248,.14)"),
        lonaxis=dict(showgrid=True, gridcolor="rgba(56,189,248,.14)"),
    )
    fig.update_layout(
        height=430, margin=dict(l=5, r=5, t=30, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0e8d8", family="Microsoft YaHei"),
        title=dict(text="典型航区气象/海况分布：节点风浪、海流与运行策略", font=dict(color="#eaf6ff", size=16)),
    )
    return fig


def build_sensor_frame(wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state, rpm, inlet, bypass):
    ts = datetime.now().strftime("%H:%M:%S")
    rows = [
        ["AWS-01", "超声风速风向仪", "NMEA0183 / UDP", f"{wind_speed:.1f} m/s, {wind_angle}°", "2 Hz", "在线", ts],
        ["GPS-AIS", "船位与航速接口", "NMEA2000 / AIS", f"{ship_speed:.1f} kn", "1 Hz", "在线", ts],
        ["ME-LOAD", "主机负荷读取", "Modbus TCP", f"{engine_load}%", "1 Hz", "在线", ts],
        ["EBP-01", "排气背压传感器", "4-20mA / ADC", f"{back_pressure:.1f} kPa", "10 Hz", "在线" if back_pressure < 4.5 else "预警", ts],
        ["RPM-ENC", "滚筒转速编码器", "CAN Bus", f"{rpm} rpm", "20 Hz", "在线", ts],
        ["VALVE-IN", "透平入口阀执行器", "CANopen", f"{inlet:.0f}%", "5 Hz", "在线", ts],
        ["VALVE-BY", "旁通阀执行器", "CANopen", f"{bypass:.0f}%", "5 Hz", "在线" if bypass < 85 else "保护", ts],
        ["IMU-WAVE", "海况/姿态估计", "IMU + Edge", f"海况{sea_state}级", "20 Hz", "在线" if sea_state < 7 else "预警", ts],
    ]
    return pd.DataFrame(rows, columns=["点位", "设备/接口", "协议", "实时值", "频率", "状态", "更新时间"])


def sensor_latency_chart():
    df = pd.DataFrame({
        "链路": ["传感器采集", "边缘清洗", "安全规则", "助航策略建议", "控制输出", "可视化刷新"],
        "延迟(ms)": [80, 45, 30, 120, 60, 55],
    })
    fig = go.Figure(go.Bar(x=df["链路"], y=df["延迟(ms)"], marker=dict(color="#22d3ee")))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=35, b=10), title="实船接口链路延迟示意", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0e8d8", family="Microsoft YaHei"), yaxis=dict(gridcolor="rgba(148,163,184,.15)"), xaxis=dict(gridcolor="rgba(148,163,184,.08)"))
    return fig


def build_twin_replay(route_name, wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state, device_count, use_live=False):
    route_name = resolve_route_name(route_name)
    df, _, _ = get_route_weather(route_name, wind_speed, wind_angle, sea_state, use_live=use_live)
    if df.empty:
        return df
    n = len(df)
    if n < 12:
        # 实时接口通常只返回节点级数据；为了回放更平滑，对节点插值扩展。
        base_nodes = ROUTE_DATABASE[route_name]["nodes"]
        df = build_route_weather_sample(route_name, wind_speed, wind_angle, sea_state)
        n = len(df)
    df = df.copy().reset_index(drop=True)
    df["时间"] = [f"T+{i:02d}h" for i in range(n)]
    df["船速(kn)"] = np.clip(ship_speed + 0.45 * np.sin(np.arange(n) / 2), 6, 21).round(1)
    df["主机负荷(%)"] = np.clip(engine_load + 6 * np.cos(np.arange(n) / 4), 30, 100).round(0).astype(int)
    df["背压(kPa)"] = np.clip(back_pressure + 0.28 * np.sin(np.arange(n) / 3), 1, 5.2).round(2)
    df["模式"] = [decide_mode(float(w), wind_angle, float(bp), int(ss))[0] for w, bp, ss in zip(df["风速(m/s)"], df["背压(kPa)"], df["海况等级"])]
    df["推荐转速(rpm)"] = [recommend_rpm(float(w), m) for w, m in zip(df["风速(m/s)"], df["模式"])]
    df["估算推力(kN)"] = [round(calc_single_thrust(float(w), wind_angle, ship_speed, int(r), int(ss))[0] * device_count * (1 - 0.03 * (device_count - 1)), 1) for w, r, ss in zip(df["风速(m/s)"], df["推荐转速(rpm)"], df["海况等级"])]
    df["健康度(%)"] = np.clip(97 - df["海况等级"] * 1.8 - np.maximum(df["背压(kPa)"] - 3.5, 0) * 6, 72, 99).round(1)
    return df


def twin_replay_figure(df, idx):
    idx = int(np.clip(idx, 0, len(df) - 1))
    current = df.iloc[idx]
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=df["lon"], lat=df["lat"], mode="lines", line=dict(width=3, color="rgba(125,211,252,.70)"), name="计划航线"
    ))
    fig.add_trace(go.Scattergeo(
        lon=df.loc[:idx, "lon"], lat=df.loc[:idx, "lat"], mode="lines+markers", line=dict(width=5, color="#7eb798"), marker=dict(size=7, color="#7eb798"), name="已回放轨迹"
    ))
    fig.add_trace(go.Scattergeo(
        lon=[current["lon"]], lat=[current["lat"]], mode="markers+text", text=["当前船位"], textposition="top center", marker=dict(size=18, color="#fbbf24", symbol="star"), name="当前船位"
    ))
    fig.update_geos(
        projection_type="natural earth", showcountries=True, countrycolor="rgba(148,163,184,.28)", showland=True, landcolor="rgba(15,40,58,.8)", showocean=True, oceancolor="rgba(2,12,28,.95)", lataxis=dict(showgrid=True, gridcolor="rgba(56,189,248,.14)"), lonaxis=dict(showgrid=True, gridcolor="rgba(56,189,248,.14)"),
    )
    fig.update_layout(height=430, margin=dict(l=5, r=5, t=30, b=5), title=f"数字孪生回放：{current['时间']} · {current['海区']}", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0e8d8", family="Microsoft YaHei"))
    return fig




def zone_badge(zone: str) -> str:
    cls = {
        "高效助航区": "zone-high",
        "谨慎运行区": "zone-mid",
        "低收益待机区": "zone-low",
        "安全锁定区": "zone-stop",
    }.get(zone, "zone-low")
    return f"<span class='zone-chip {cls}'>{zone}</span>"


def classify_assist_zone(row) -> str:
    potential = float(row.get("风助潜力", 0))
    risk = str(row.get("风险等级", "低"))
    sea = int(row.get("海况等级", 0))
    wave = float(row.get("浪高(m)", 0))
    wind = float(row.get("风速(m/s)", 0))
    if risk == "高" or sea >= 6 or wave >= 4.0 or wind >= 22:
        return "安全锁定区"
    if potential >= 8 and risk != "高" and sea <= 5:
        return "高效助航区"
    if potential >= 5:
        return "谨慎运行区"
    return "低收益待机区"


def zone_strategy(zone: str, device_count: int) -> str:
    if zone == "高效助航区":
        return f"开启{device_count}座滚筒帆，高效助航，优先保持侧风收益"
    if zone == "谨慎运行区":
        return f"开启{max(1, device_count-1)}座滚筒帆，中低转速运行并监测载荷"
    if zone == "安全锁定区":
        return "入口阀关闭，旁通优先，滚筒帆低速/停机保护"
    return "低速待机，仅保留状态监测，避免无效取能"


def build_assist_zone_frame(route_name, wind_speed, wind_angle, ship_speed, back_pressure, sea_state, device_count, use_live=False):
    df, data_mode, source_msg = get_route_weather(route_name, wind_speed, wind_angle, sea_state, use_live=use_live)
    if df.empty:
        return df, data_mode, source_msg
    df = df.copy().reset_index(drop=True)
    total_distance = ROUTE_DATABASE[resolve_route_name(route_name)]["distance_nm"]
    segment_distance = total_distance / max(len(df), 1)
    zones, strategies, rpm_list, thrust_list, save_list, distance_list = [], [], [], [], [], []
    for _, row in df.iterrows():
        zone = classify_assist_zone(row)
        wind = float(row["风速(m/s)"])
        local_sea = int(row["海况等级"])
        local_bp = float(np.clip(back_pressure + 0.08 * max(float(row["浪高(m)"]) - 2, 0), 1, 5.2))
        local_mode = "高效助航模式" if zone == "高效助航区" else "低收益待机模式" if zone == "低收益待机区" else "恶劣海况安全模式" if zone == "安全锁定区" else decide_mode(wind, wind_angle, local_bp, local_sea)[0]
        rpm_local = recommend_rpm(wind, local_mode)
        active_devices = device_count if zone == "高效助航区" else max(1, device_count - 1) if zone == "谨慎运行区" else 0 if zone == "安全锁定区" else 1
        thrust = 0 if active_devices == 0 else calc_single_thrust(wind, wind_angle, ship_speed, rpm_local, local_sea)[0] * active_devices * (1 - 0.03 * max(active_devices - 1, 0))
        save = 0 if active_devices == 0 else float(np.clip(3.5 + thrust * 0.045, 0, 30))
        zones.append(zone)
        strategies.append(zone_strategy(zone, device_count))
        rpm_list.append(int(rpm_local))
        thrust_list.append(round(thrust, 1))
        save_list.append(round(save, 1))
        distance_list.append(round(segment_distance, 0))
    df["助航区类型"] = zones
    df["建议策略"] = strategies
    df["推荐转速(rpm)"] = rpm_list
    df["估算推力(kN)"] = thrust_list
    df["节能潜力(%)"] = save_list
    df["代表航段距离(nm)"] = distance_list
    df["助航区"] = df["助航区类型"].map(zone_badge)
    return df, data_mode, source_msg


def assist_zone_summary(zone_df):
    if zone_df.empty:
        return pd.DataFrame()
    out = zone_df.groupby("助航区类型", as_index=False).agg(
        航段数量=("海区", "count"),
        代表距离_nm=("代表航段距离(nm)", "sum"),
        平均风速_ms=("风速(m/s)", "mean"),
        平均浪高_m=("浪高(m)", "mean"),
        平均推力_kN=("估算推力(kN)", "mean"),
        平均节能潜力_pct=("节能潜力(%)", "mean"),
    )
    order = ["高效助航区", "谨慎运行区", "低收益待机区", "安全锁定区"]
    out["排序"] = out["助航区类型"].apply(lambda x: order.index(x) if x in order else 99)
    out = out.sort_values("排序").drop(columns="排序")
    for c in ["平均风速_ms", "平均浪高_m", "平均推力_kN", "平均节能潜力_pct"]:
        out[c] = out[c].round(1)
    out["助航区"] = out["助航区类型"].map(zone_badge)
    return out[["助航区", "航段数量", "代表距离_nm", "平均风速_ms", "平均浪高_m", "平均推力_kN", "平均节能潜力_pct"]]


def assist_zone_map(zone_df):
    colors = {
        "高效助航区": "#22d3ee",
        "谨慎运行区": "#5eead4",
        "低收益待机区": "#bfdbfe",
        "安全锁定区": "#818cf8",
    }
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=zone_df["lon"], lat=zone_df["lat"], mode="lines",
        line=dict(width=3, color="rgba(125,211,252,.70)"), name="计划航线"
    ))
    for zone, part in zone_df.groupby("助航区类型"):
        fig.add_trace(go.Scattergeo(
            lon=part["lon"], lat=part["lat"], mode="markers+text",
            text=part["海区"], textposition="top center",
            marker=dict(size=12, color=colors.get(zone, "#8a8278"), line=dict(width=1, color="#f0e8d8")),
            name=zone,
            customdata=np.stack([part["风速(m/s)"], part["浪高(m)"], part["估算推力(kN)"], part["节能潜力(%)"], part["建议策略"]], axis=-1),
            hovertemplate="%{text}<br>风速 %{customdata[0]} m/s<br>浪高 %{customdata[1]} m<br>推力 %{customdata[2]} kN<br>节能潜力 %{customdata[3]}%<br>%{customdata[4]}<extra></extra>",
        ))
    fig.update_geos(
        projection_type="natural earth",
        showcountries=True, countrycolor="rgba(148,163,184,.28)",
        showland=True, landcolor="rgba(36,76,108,.78)",
        showocean=True, oceancolor="rgba(8,44,74,.92)",
        lataxis=dict(showgrid=True, gridcolor="rgba(56,189,248,.14)"),
        lonaxis=dict(showgrid=True, gridcolor="rgba(56,189,248,.14)"),
    )
    fig.update_layout(
        height=430, margin=dict(l=5, r=5, t=30, b=5),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0e8d8", family="Microsoft YaHei"),
        title=dict(text="典型航区识别：高效、谨慎、待机与锁定区段分布", font=dict(color="#eaf6ff", size=16)),
        legend=dict(orientation="h", y=-0.05),
    )
    return fig


def assist_zone_distance_chart(summary_df):
    clean = summary_df.copy()
    clean["助航区类型"] = clean["助航区"].str.replace(r"<[^>]+>", "", regex=True)
    fig = go.Figure(go.Bar(
        x=clean["助航区类型"], y=clean["代表距离_nm"],
        marker=dict(color=["#22d3ee" if x == "高效助航区" else "#5eead4" if x == "谨慎运行区" else "#bfdbfe" if x == "低收益待机区" else "#818cf8" for x in clean["助航区类型"]], line=dict(color="rgba(255,255,255,.28)", width=0.8))
    ))
    fig.update_layout(height=300, title=dict(text="典型航区代表航程分布", font=dict(color="#eaf6ff", size=16)), margin=dict(l=10, r=10, t=45, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0e8d8", family="Microsoft YaHei"), yaxis_title="代表距离 / nm", yaxis=dict(gridcolor="rgba(148,163,184,.15)"))
    return fig


def build_carbon_ledger(route_name, ship_type, dwt, ship_speed, device_count, zone_df):
    route_name = resolve_route_name(route_name)
    distance_nm = ROUTE_DATABASE[route_name]["distance_nm"]
    voyage_days = max(distance_nm / max(ship_speed * 24, 1), 0.1)
    base_fuel_day = 32 * (dwt / 50000) ** 0.55 * (ship_speed / 14) ** 3
    co2_factor = 3.114
    if zone_df.empty:
        avg_save = 0
        high_nm = 0
    else:
        avg_save = float(np.average(zone_df["节能潜力(%)"], weights=zone_df["代表航段距离(nm)"]))
        high_nm = float(zone_df.loc[zone_df["助航区类型"].eq("高效助航区"), "代表航段距离(nm)"].sum())
    base_fuel = base_fuel_day * voyage_days
    improved_fuel = base_fuel * (1 - avg_save / 100)
    fuel_saved = base_fuel - improved_fuel
    co2_base = base_fuel * co2_factor
    co2_after = improved_fuel * co2_factor
    co2_saved = co2_base - co2_after
    freight_work = dwt * distance_nm
    base_cii = co2_base * 1_000_000 / freight_work
    improved_cii = co2_after * 1_000_000 / freight_work
    rows = [
        ["航线", route_name, "固定四航线数据库"],
        ["航程", f"{distance_nm:,.0f} nm", "航线预设距离"],
        ["预计航行时间", f"{voyage_days:.1f} 天", f"按 {ship_speed:.1f} kn 估算"],
        ["基准燃油消耗", f"{base_fuel:.1f} 吨", "不开启系统"],
        ["开启后燃油消耗", f"{improved_fuel:.1f} 吨", f"按航线平均节能 {avg_save:.1f}%"],
        ["节省燃油", f"{fuel_saved:.1f} 吨", "航次级收益"],
        ["基准CO₂排放", f"{co2_base:.1f} 吨", "燃油排放因子 3.114 tCO₂/t fuel"],
        ["开启后CO₂排放", f"{co2_after:.1f} 吨", "开启海帆智擎"],
        ["CO₂减排", f"{co2_saved:.1f} 吨", "航次碳账本核心指标"],
        ["绿色助航里程", f"{high_nm:,.0f} nm", "高收益助航区累计距离"],
        ["CII评级变化", f"{cii_rating(base_cii, ship_type)} → {cii_rating(improved_cii, ship_type)}", "竞赛演示估算"],
    ]
    ledger = pd.DataFrame(rows, columns=["账本项目", "结果", "说明"])
    return ledger, dict(distance_nm=distance_nm, voyage_days=voyage_days, base_fuel=base_fuel, improved_fuel=improved_fuel, fuel_saved=fuel_saved, co2_base=co2_base, co2_after=co2_after, co2_saved=co2_saved, avg_save=avg_save, high_nm=high_nm, base_cii=base_cii, improved_cii=improved_cii)


def carbon_ledger_chart(stats):
    fig = go.Figure()
    fig.add_trace(go.Bar(name="基准工况", x=["燃油消耗(吨)", "CO₂排放(吨)"], y=[stats["base_fuel"], stats["co2_base"]], marker=dict(color="#bfd3e6")))
    fig.add_trace(go.Bar(name="开启海帆智擎", x=["燃油消耗(吨)", "CO₂排放(吨)"], y=[stats["improved_fuel"], stats["co2_after"]], marker=dict(color="#22d3ee")))
    fig.update_layout(barmode="group", height=330, title=dict(text="航次碳账本：节油与减排对比", font=dict(color="#eaf6ff", size=16)), margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0e8d8", family="Microsoft YaHei"), yaxis=dict(gridcolor="rgba(148,163,184,.15)"))
    return fig


def build_voyage_report(route_name, stats, zone_summary, health_df=None):
    route_name = resolve_route_name(route_name)
    high_nm = stats.get("high_nm", 0)
    zone_text = "暂无区段统计"
    if zone_summary is not None and not zone_summary.empty:
        parts = []
        for _, row in zone_summary.iterrows():
            label = str(row["助航区"])
            for token in ["<span class='zone-chip zone-high'>", "<span class='zone-chip zone-mid'>", "<span class='zone-chip zone-low'>", "<span class='zone-chip zone-stop'>", "</span>"]:
                label = label.replace(token, "")
            parts.append(f"{label} {float(row['代表距离_nm']):.0f}nm")
        zone_text = "、".join(parts)
    health_text = ""
    if health_df is not None and not health_df.empty:
        min_row = health_df.sort_values("健康度(%)").iloc[0]
        health_text = f"当前最低健康部件为{min_row['部件']}，健康度{min_row['健康度(%)']:.1f}%，建议{min_row['维护建议']}。"
    return (
        f"本航次选取{route_name}航线，预计航程{stats['distance_nm']:.0f} nm，航行时间约{stats['voyage_days']:.1f}天。"
        f"平台根据航线气象数据库识别出高收益助航里程约{high_nm:.0f} nm，区段统计为：{zone_text}。"
        f"在当前滚筒帆协同方案下，估算航次燃油消耗由{stats['base_fuel']:.1f}吨降低至{stats['improved_fuel']:.1f}吨，"
        f"节省燃油{stats['fuel_saved']:.1f}吨，减少CO₂排放{stats['co2_saved']:.1f}吨，CII指标由{stats['base_cii']:.2f}改善至{stats['improved_cii']:.2f}。"
        f"{health_text}本报告用于竞赛演示与方案复盘，正式航行和合规核算需接入船级社/主管机构认可数据。"
    )


def build_health_frame(wind_speed, sea_state, back_pressure, rpm, inlet, bypass, engine_load, device_count):
    load_factor = engine_load / 100
    sea_penalty = max(0, sea_state - 3) * 2.2
    bp_penalty = max(0, back_pressure - 3.5) * 8
    rpm_penalty = max(0, rpm - 150) * 0.035
    rows = []
    items = [
        ("RS-BRG", "滚筒帆轴承组", 96 - sea_penalty - rpm_penalty * 1.8, "振动/温升趋势", "检查润滑与轴承振动谱"),
        ("RS-SHELL", "滚筒帆筒体结构", 97 - sea_penalty * 1.1 - max(0, wind_speed - 18) * 0.5, "结构载荷与疲劳", "复核强风航段载荷"),
        ("TURBINE", "废气轴流透平", 95 - bp_penalty * 0.45 - load_factor * 2, "转速/排温/叶片风险", "检查透平叶片积碳与间隙"),
        ("GEARBOX", "减速齿轮箱", 94 - rpm_penalty * 1.1 - sea_penalty * 0.5, "油温/齿面磨损", "采样润滑油并检查齿面"),
        ("IN-VALVE", "透平入口阀", 96 - abs(inlet - 65) * 0.045 - bp_penalty * 0.4, "阀门响应时间", "靠港后做开闭响应测试"),
        ("BY-VALVE", "旁通阀", 95 - max(0, bypass - 75) * 0.12 - bp_penalty * 0.8, "安全旁通能力", "优先检查密封与执行器"),
        ("EBP-SENSOR", "排气背压传感器", 97 - bp_penalty * 0.35, "漂移/校准状态", "校验零点和量程"),
        ("EDGE-GW", "边缘数据网关", 98 - max(0, sea_state - 5) * 1.2, "丢包率/延迟", "检查网络与时间同步"),
    ]
    for code, comp, health, risk, advice in items:
        h = float(np.clip(health, 58, 99))
        if h >= 90:
            status, level = "健康", "低"
        elif h >= 78:
            status, level = "关注", "中"
        else:
            status, level = "预警", "高"
        rul = int(np.clip((h - 55) * 70, 120, 3600))
        rows.append([code, comp, round(h, 1), status, level, rul, risk, advice])
    return pd.DataFrame(rows, columns=["点位", "部件", "健康度(%)", "状态", "风险等级", "预计剩余寿命(h)", "监测依据", "维护建议"])


def health_radar_chart(health_df):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=health_df["健康度(%)"], theta=health_df["部件"], fill="toself",
        name="设备健康度", line=dict(color="#7eb798"), fillcolor="rgba(126,183,152,.18)"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[50, 100], gridcolor="rgba(148,163,184,.18)"), angularaxis=dict(gridcolor="rgba(148,163,184,.12)")),
        height=410, title="设备健康雷达图", margin=dict(l=20, r=20, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0e8d8", family="Microsoft YaHei")
    )
    return fig


def maintenance_plan(health_df):
    rows = []
    for _, row in health_df.iterrows():
        h = float(row["健康度(%)"])
        if h < 78:
            priority, window = "P1", "立即/本航次内"
        elif h < 88:
            priority, window = "P2", "靠港后"
        else:
            priority, window = "P3", "例行维护"
        rows.append([priority, row["部件"], row["风险等级"], row["预计剩余寿命(h)"], window, row["维护建议"]])
    out = pd.DataFrame(rows, columns=["优先级", "对象", "风险等级", "剩余寿命(h)", "建议窗口", "维护动作"])
    return out.sort_values(["优先级", "剩余寿命(h)"])



def _clip_score(v):
    return float(np.clip(v, 0, 100))



def current_data_status_bar(use_live_weather=False, demo_locked=False):
    """统一数据状态条：说明数据来源、模型边界和控制权限，增强可信度。"""
    data_source = "在线海况接口 + 本地航线样本库" if use_live_weather else "本地航线样本库"
    live_state = "在线接口可切换" if use_live_weather else "离线演示稳定模式"
    model_state = "演示级轻量评分模型 + 安全规则校核"
    control_state = "辅助推荐，人工确认优先"
    lock_state = "演示锁定：开启" if demo_locked else "演示锁定：未开启"
    return f"""
<div class="data-status-strip">
  <div class="data-status-item"><small>数据源</small><b>{data_source}</b></div>
  <div class="data-status-item"><small>数据状态</small><b>{live_state}</b></div>
  <div class="data-status-item"><small>模型状态</small><b>{model_state}</b></div>
  <div class="data-status-item"><small>控制权限</small><b>{control_state}<br>{lock_state}</b></div>
</div>
"""


def ai_reason_cards(ai_result, wind_speed, wind_angle, back_pressure, sea_state):
    """把智能推荐原因转成可读卡片，避免黑箱感。"""
    side = abs(math.sin(math.radians(wind_angle)))
    factors = ai_result.get("factors", pd.DataFrame()).copy()
    if not factors.empty:
        top_factors = factors.sort_values("相对贡献(%)", ascending=False).head(3)["影响因素"].tolist()
    else:
        top_factors = ["风速收益", "风向角/侧风分量", "背压安全"]

    reasons = []
    if wind_speed < 6:
        reasons.append(("风速收益不足", f"当前风速 {wind_speed:.1f} m/s，低于高效助航区间，系统倾向待机或低速运行。"))
    elif wind_speed > 24:
        reasons.append(("风速超过安全边界", f"当前风速 {wind_speed:.1f} m/s，触发风速边界约束。"))
    else:
        reasons.append(("风速处于可用区间", f"当前风速 {wind_speed:.1f} m/s，可支持滚筒帆产生有效助航收益。"))

    if side >= 0.70:
        reasons.append(("侧风分量较高", f"风向角 {wind_angle}°，侧风分量 {side:.2f}，有利于马格努斯推力转化为助航推力。"))
    else:
        reasons.append(("侧风分量偏低", f"风向角 {wind_angle}°，侧风分量 {side:.2f}，系统会降低助航收益预期。"))

    if back_pressure >= 4.5:
        reasons.append(("背压触发保护", f"排气背压 {back_pressure:.1f} kPa，系统优先保护主机排烟安全，旁通阀优先开启。"))
    else:
        reasons.append(("背压安全通过", f"排气背压 {back_pressure:.1f} kPa，未触发主机保护阈值，允许废气余能取能。"))

    if sea_state >= 7:
        reasons.append(("海况触发安全锁定", f"海况 {sea_state} 级，系统进入安全锁定，避免恶劣海况下结构载荷风险。"))
    else:
        reasons.append(("海况允许运行", f"海况 {sea_state} 级，未触发安全锁定，系统可继续进行智能助航推荐。"))

    cards = "".join([f"<div class='reason-card'><b>{title}</b>{desc}</div>" for title, desc in reasons])
    top = " / ".join(top_factors)
    return f"""
<div class="notice">
  <b>本次推荐的主要依据：</b>{top}。系统先进行助航收益与风险评分，再经过背压、海况、风速边界和人工优先级等安全规则校核。
</div>
<div class="reason-grid">{cards}</div>
"""

def ai_decision_engine(wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state, device_count, rpm, inlet, bypass, total_thrust, save_rate, health_df=None):
    """轻量可解释AI决策引擎：用于竞赛演示，输出预测、识别、推荐、诊断与安全约束结果。"""
    side_factor = abs(math.sin(math.radians(wind_angle)))
    wind_score = _clip_score((wind_speed - 3) / 13 * 100)
    angle_score = _clip_score(side_factor * 100)
    speed_score = _clip_score((ship_speed - 8) / 8 * 100)
    engine_score = _clip_score(100 - abs(engine_load - 72) * 1.5)
    sea_safety = _clip_score(100 - sea_state * 11)
    back_safety = _clip_score(100 - max(back_pressure - 2.8, 0) * 34)
    device_bonus = _clip_score(68 + device_count * 5)

    raw_score = _clip_score(
        0.23 * wind_score +
        0.24 * angle_score +
        0.10 * speed_score +
        0.10 * engine_score +
        0.18 * sea_safety +
        0.15 * back_safety
    )
    assist_score = _clip_score(raw_score * 0.86 + device_bonus * 0.14)
    risk_score = _clip_score(100 - (0.45 * sea_safety + 0.45 * back_safety + 0.10 * engine_score))

    if assist_score >= 78:
        raw_mode = "高效助航模式"
    elif assist_score >= 58:
        raw_mode = "普通助航模式"
    elif assist_score >= 38:
        raw_mode = "低收益待机模式"
    else:
        raw_mode = "安全锁定模式"

    safety_rules = []
    final_mode = raw_mode
    override = False
    if sea_state >= 7:
        final_mode = "恶劣海况安全模式"
        override = True
        safety_rules.append(["海况等级约束", f"{sea_state}级", "触发", "入口阀关闭，旁通阀全开"])
    else:
        safety_rules.append(["海况等级约束", f"{sea_state}级", "通过", "允许智能推荐"])
    if back_pressure >= 4.5:
        final_mode = "主机保护模式"
        override = True
        safety_rules.append(["排气背压约束", f"{back_pressure:.1f} kPa", "触发", "旁通优先，保护主机排烟"])
    else:
        safety_rules.append(["排气背压约束", f"{back_pressure:.1f} kPa", "通过", "允许透平取能"])
    if wind_speed < 2 or wind_speed > 24:
        final_mode = "恶劣海况安全模式"
        override = True
        safety_rules.append(["风速边界约束", f"{wind_speed:.1f} m/s", "触发", "风速极端，限制运行"])
    elif wind_speed < 6 or side_factor < 0.30:
        if final_mode not in ["主机保护模式", "恶劣海况安全模式"]:
            final_mode = "低收益待机模式"
            override = True
        safety_rules.append(["收益下限约束", f"侧风分量 {side_factor:.2f}", "触发", "避免无效取能"])
    else:
        safety_rules.append(["风况收益约束", f"侧风分量 {side_factor:.2f}", "通过", "可产生有效马格努斯推力"])
    safety_rules.append(["人工优先级", "驾驶台/人工急停", "常开", "人工指令高于智能推荐"])

    factors = pd.DataFrame([
        ["风速收益", wind_score, "风速越接近适用区间，滚筒帆助航潜力越高"],
        ["风向角/侧风分量", angle_score, "接近横风时马格努斯推力更有利于助航"],
        ["船速适配", speed_score, "航速影响相对风速和推进替代收益"],
        ["主机负荷适配", engine_score, "主机负荷影响废气能量可用性"],
        ["海况安全", sea_safety, "海况越差，系统越保守"],
        ["背压安全", back_safety, "背压越高，越需要旁通保护"],
    ], columns=["影响因素", "评分", "解释"])
    weight_map = {
        "风速收益": 0.23,
        "风向角/侧风分量": 0.24,
        "船速适配": 0.10,
        "主机负荷适配": 0.10,
        "海况安全": 0.18,
        "背压安全": 0.15,
    }
    factors["权重"] = factors["影响因素"].map(weight_map)
    factors["贡献度"] = (factors["评分"] * factors["权重"]).round(1)
    total_contrib = float(factors["贡献度"].sum()) or 1
    factors["相对贡献(%)"] = (factors["贡献度"] / total_contrib * 100).round(1)
    factors = factors.sort_values("相对贡献(%)", ascending=False)

    health_risk = np.nan
    weakest = "暂未接入"
    if health_df is not None and not health_df.empty:
        weakest_row = health_df.sort_values("健康度(%)").iloc[0]
        health_risk = float(np.clip(100 - health_df["健康度(%)"].mean(), 0, 100))
        weakest = str(weakest_row["部件"])

    output_df = pd.DataFrame([
        ["助航收益预测", f"{total_thrust:.1f} kN", "当前工况下多装置协同推力估算"],
        ["推荐滚筒转速", f"{rpm} rpm", "由风况收益与安全边界共同决定"],
        ["阀门推荐", f"入口阀 {inlet:.0f}% / 旁通阀 {bypass:.0f}%", "安全优先的执行建议"],
        ["航线助航评分", f"{assist_score:.1f}/100", "用于识别高收益助航区"],
        ["风险评分", f"{risk_score:.1f}/100", "海况与背压风险综合"],
        ["节能潜力", f"{save_rate:.1f}%", "用于航次碳账本估算"],
        ["健康风险", f"{health_risk:.1f}/100" if not pd.isna(health_risk) else "未接入", f"薄弱部件：{weakest}"],
    ], columns=["模型输出", "结果", "说明"])

    safety_df = pd.DataFrame(safety_rules, columns=["安全规则", "当前值", "状态", "控制动作"])
    status_text = "模型建议已被安全规则修正" if override else "模型建议通过安全规则校验"
    recommendation = (
        f"当前智能决策引擎给出的模型原始建议为{raw_mode}，最终建议为{final_mode}。"
        f"系统预测智能助航评分为{assist_score:.1f}/100，风险评分为{risk_score:.1f}/100。"
        f"建议转速{rpm} rpm，入口阀{inlet:.0f}%，旁通阀{bypass:.0f}%。"
        f"{status_text}。轻量评分模型只负责趋势估算和辅助推荐，最终执行仍受主机背压、海况等级和人工控制约束。"
    )
    return {
        "assist_score": assist_score,
        "risk_score": risk_score,
        "raw_mode": raw_mode,
        "final_mode": final_mode,
        "override": override,
        "status_text": status_text,
        "factors": factors,
        "outputs": output_df,
        "safety": safety_df,
        "recommendation": recommendation,
    }


def ai_feature_chart(factors):
    data = factors.sort_values("相对贡献(%)", ascending=True)
    fig = go.Figure(go.Bar(
        x=data["相对贡献(%)"], y=data["影响因素"], orientation="h",
        marker=dict(color=["#e0c8a0", "#d4b878", "#c89848", "#b87828", "#a86818", "#d4983a"][-len(data):]),
        text=[f"{v:.1f}%" for v in data["相对贡献(%)"]], textposition="outside"
    ))
    fig.update_layout(
        height=360, title=dict(text="本次决策依据：关键因素贡献度", font=dict(color="#eaf6ff", size=16)),
        margin=dict(l=10, r=30, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0e8d8", family="Microsoft YaHei"),
        xaxis=dict(title="相对贡献 / %", gridcolor="rgba(148,163,184,.15)"),
        yaxis=dict(gridcolor="rgba(148,163,184,.08)")
    )
    return fig


def ai_score_gauge(title, value, color="#22d3ee"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "/100", "font": {"color": "#eff9ff", "size": 34}},
        title={"text": title, "font": {"color": "#f0e8d8", "size": 16}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#8eb6d5"},
            "bar": {"color": color},
            "bgcolor": "rgba(255,255,255,.05)",
            "borderwidth": 1,
            "bordercolor": "rgba(125,211,252,.22)",
            "steps": [
                {"range": [0, 40], "color": "rgba(191,219,254,.22)"},
                {"range": [40, 70], "color": "rgba(125,211,252,.18)"},
                {"range": [70, 100], "color": "rgba(34,211,238,.14)"},
            ],
        },
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=35, b=10), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#f0e8d8", family="Microsoft YaHei"))
    return fig



# =========================
# PRACTICAL OPERATION WORKBENCH
# =========================
def operational_alerts(wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state, mode, sensor_df, health_df):
    """将当前工况转换为值班告警与处置动作，让平台体现真实工作流程。"""
    rows = []
    def add(level, event, trigger, action, owner="驾驶台/轮机员", record="事件日志"):
        rows.append([level, event, trigger, action, owner, record])

    side_factor = abs(math.sin(math.radians(wind_angle)))
    if sea_state >= 7:
        add("P1", "恶劣海况锁定", f"海况 {sea_state} 级", "保持旁通阀全开，滚筒帆降速/停转，进入人工确认", "驾驶台", "海况、航速、转速")
    elif sea_state >= 5:
        add("P2", "海况升高", f"海况 {sea_state} 级", "限制目标转速，缩短监测周期，观察横摇与载荷", "驾驶台", "海况、姿态、载荷")

    if back_pressure >= 4.8:
        add("P1", "排气背压接近保护阈值", f"{back_pressure:.1f} kPa", "旁通优先，暂停继续提高取能比例，通知轮机员复核", "轮机员", "背压、阀位、主机负荷")
    elif back_pressure >= 4.2:
        add("P2", "背压偏高", f"{back_pressure:.1f} kPa", "降低入口阀开度，保留旁通安全余量", "轮机员", "背压趋势")

    if wind_speed < 6 or side_factor < 0.30:
        add("P3", "风助收益不足", f"风速 {wind_speed:.1f} m/s，侧风分量 {side_factor:.2f}", "保持低收益待机，避免无效取能", "驾驶台", "风速、风向")
    elif wind_speed >= 18:
        add("P2", "强风运行", f"风速 {wind_speed:.1f} m/s", "限制转速爬升率，关注结构振动", "驾驶台/轮机员", "风速、转速、振动")

    if health_df is not None and not health_df.empty:
        weak = health_df.sort_values("健康度(%)").iloc[0]
        if float(weak["健康度(%)"]) < 78:
            add("P1", "设备健康预警", f"{weak['部件']} {weak['健康度(%)']:.1f}%", str(weak["维护建议"]), "轮机员", "健康度、振动、温度")
        elif float(weak["健康度(%)"]) < 88:
            add("P2", "设备关注", f"{weak['部件']} {weak['健康度(%)']:.1f}%", str(weak["维护建议"]), "轮机员", "维护记录")

    if sensor_df is not None and not sensor_df.empty:
        warn_count = int(sensor_df["状态"].astype(str).isin(["预警", "保护", "离线"]).sum())
        if warn_count > 0:
            add("P2", "接口状态异常", f"{warn_count} 个点位需关注", "检查边缘网关数据质量，必要时切换人工确认", "数据/驾驶台", "接口状态")

    if not rows:
        add("P4", "无即时告警", "所有关键阈值通过", "按计划执行当前助航策略，每15分钟复核一次", "驾驶台", "例行记录")
    return pd.DataFrame(rows, columns=["优先级", "事件", "触发条件", "处置动作", "责任角色", "记录字段"])


def data_quality_frame(sensor_df, route_name, use_live=False):
    """把传感器/气象数据转换成可运维的数据质量面板。"""
    rows = []
    if sensor_df is not None and not sensor_df.empty:
        for _, row in sensor_df.iterrows():
            status = str(row["状态"])
            if status == "在线":
                score = 98
                action = "正常入库"
            elif status == "保护":
                score = 86
                action = "保留数据并标记保护状态"
            elif status == "预警":
                score = 78
                action = "参与决策但触发人工复核"
            else:
                score = 55
                action = "剔除异常值，切换冗余/人工输入"
            rows.append([row["点位"], row["设备/接口"], row["协议"], row["频率"], status, score, action])
    rows.append(["WX-ROUTE", f"{resolve_route_name(route_name)}航线气象/海况", "API/本地样本", "按节点刷新", "实时" if use_live else "样本", 92 if use_live else 84, "用于航线助航区识别和航次复盘"])
    rows.append(["LOG-VOY", "航次运行日志", "CSV/TXT导出", "人工确认", "可追溯", 95, "用于赛后复盘、模型训练样本沉淀"])
    return pd.DataFrame(rows, columns=["数据点", "数据来源", "接口/协议", "刷新频率", "状态", "质量评分", "系统处理"])


def build_voyage_task_sheet(route_name, zone_df, mode, rpm, inlet, bypass, device_count):
    """把航线识别结果转成可执行任务单。"""
    if zone_df is None or zone_df.empty:
        return pd.DataFrame(columns=["序号", "海区/航段", "助航区", "计划动作", "目标参数", "值班检查", "记录要求"])
    rows = []
    for _, row in zone_df.iterrows():
        zone = str(row.get("助航区类型", row.get("助航区", "低收益待机区")))
        if "高收益" in zone:
            action = "开启助航，优先多装置协同"
            target = f"{device_count}座，{int(row.get('推荐转速(rpm)', rpm))} rpm，入口阀{max(55, inlet):.0f}%"
            check = "每15分钟复核风向、背压、转速和振动"
        elif "谨慎" in zone:
            action = "限制转速，保守助航"
            target = f"{device_count}座，中低转速，旁通保留≥{max(35, bypass):.0f}%"
            check = "关注浪高、横摇和背压变化"
        elif "安全" in zone:
            action = "安全锁定，旁通优先"
            target = "入口阀关闭/低开度，旁通阀全开"
            check = "人工确认，禁止自动提高转速"
        else:
            action = "待机观测，暂不主动取能"
            target = "低速保持，等待有效侧风窗口"
            check = "记录风速风向，观察是否进入侧风区"
        rows.append([
            int(row.get("序号", len(rows)+1)),
            f"{row.get('海区','')} / {row.get('航段','')}",
            zone,
            action,
            target,
            check,
            "写入航次日志：时间、模式、阀位、背压、推力、异常事件",
        ])
    return pd.DataFrame(rows, columns=["序号", "海区/航段", "助航区", "计划动作", "目标参数", "值班检查", "记录要求"])


def practical_work_report(route_name, current_mode, rpm, inlet, bypass, total_thrust, save_rate, alerts_df, task_df, quality_df):
    p1 = int((alerts_df["优先级"] == "P1").sum()) if alerts_df is not None and not alerts_df.empty else 0
    p2 = int((alerts_df["优先级"] == "P2").sum()) if alerts_df is not None and not alerts_df.empty else 0
    high_count = int(task_df["助航区"].astype(str).str.contains("高收益").sum()) if task_df is not None and not task_df.empty else 0
    quality = float(quality_df["质量评分"].mean()) if quality_df is not None and not quality_df.empty else 0
    return (
        "海帆智擎值班工作台运行摘要\n"
        f"航线：{resolve_route_name(route_name)}\n"
        f"当前最终模式：{current_mode}\n"
        f"推荐转速：{rpm} rpm；入口阀：{inlet:.0f}%；旁通阀：{bypass:.0f}%\n"
        f"当前估算总推力：{total_thrust:.1f} kN；节能潜力：{save_rate:.1f}%\n"
        f"告警状态：P1 {p1}项，P2 {p2}项。\n"
        f"航线任务：识别出 {high_count} 个高收益助航节点，任务单已生成。\n"
        f"数据质量：综合评分 {quality:.1f}/100，可用于本轮辅助决策和航次复盘。\n"
        "工作闭环：感知数据采集 → 边缘清洗 → AI/规则推荐 → 值班确认 → 执行记录 → 航次复盘。"
    )


def alert_priority_color(priority: str) -> str:
    return {"P1": "red", "P2": "yellow", "P3": "green", "P4": "green"}.get(str(priority), "green")


with st.sidebar:
    st.markdown("### 航线场景预设")
    cols = st.columns(2)
    for i, name in enumerate(ROUTE_PRESETS.keys()):
        with cols[i % 2]:
            st.button(name, use_container_width=True, key=f"route_{i}", on_click=set_route, args=(name,))

    st.markdown("---")
    st.markdown("### 工况快速演示")
    st.caption("一键切换典型工况，快速呈现系统在不同海况下的智能响应。")
    for i, name in enumerate(DEMO_SCENARIOS.keys()):
        st.button(name, use_container_width=True, key=f"demo_{i}", on_click=set_demo, args=(name,))

    st.markdown("---")
    st.markdown("### 工况参数")
    wind_speed = st.slider("表观风速 AWS (m/s)", 0.0, 30.0, key="wind_speed", step=0.1)
    wind_angle = st.slider("风向角 AWA (°)", -180, 180, key="wind_angle", step=1)
    ship_speed = st.slider("船速 STW (kn)", 0.0, 22.0, key="ship_speed", step=0.1)
    engine_load = st.slider("主机负荷 ME Load (%)", 0, 100, key="engine_load", step=1)
    back_pressure = st.slider("排气背压 EBP (kPa，演示阈值5.0)", 0.0, 5.5, key="back_pressure", step=0.1)
    sea_state = st.slider("海况等级 Sea State", 0, 9, key="sea_state", step=1)
    device_count = st.slider("滚筒帆装置数量", 1, 6, key="device_count", step=1)

mode, reason = decide_mode(wind_speed, wind_angle, back_pressure, sea_state)
rpm = recommend_rpm(wind_speed, mode)
inlet, bypass = valve_openings(mode, back_pressure, sea_state)
single_thrust, rel_ws, spin_ratio, cl = calc_single_thrust(wind_speed, wind_angle, ship_speed, rpm, sea_state)
interference = 1 - 0.03 * (device_count - 1)
total_thrust = single_thrust * device_count * interference
save_rate = float(np.clip(4 + total_thrust * 0.020 + (inlet / 100) * 5, 0, 32))
confidence = float(np.clip(92 - sea_state * 2 - abs(back_pressure - 3.2) * 2, 65, 96))
cii = cii_demo(st.session_state.get("dwt", 150000), st.session_state.get("route_distance", 6200), ship_speed, st.session_state.get("annual_days", 250), st.session_state.get("ship_type", "散货船/油轮"), save_rate)
mode_class = "green" if mode == "高效助航模式" else "yellow" if mode in ["低收益待机模式", "主机保护模式"] else "red"
route_total = st.session_state.get("route_distance", 6200)
# 航线进度不再写死，而是随航速、风况、海况和运行模式变化。
# 这是竞赛演示用的“航线模拟进度”，用于体现不同场景下系统响应会改变航行态势。
mode_bonus = 0.07 if mode == "高效助航模式" else (-0.06 if mode in ["主机保护模式", "恶劣海况安全模式"] else -0.02)
route_ratio = float(np.clip(0.18 + ship_speed / 38 + wind_speed / 160 - sea_state / 70 + mode_bonus, 0.18, 0.82))
route_done = round(route_total * route_ratio, 0)
route_left = max(route_total - route_done, 0)
route_zone = "季风侧风富集区" if mode == "高效助航模式" else ("安全减速控制区" if mode in ["主机保护模式", "恶劣海况安全模式"] else "低风收益观测区")
route_pct = route_ratio * 100

# 船舶态势图中的滚筒帆布局。按装置数量选择对称布局，避免简单切片导致帆位偏到甲板外。
ROTOR_LAYOUTS = {
    1: [(390, 166, -18)],
    2: [(340, 160, -22), (440, 160, -14)],
    3: [(390, 124, -24), (340, 205, 22), (440, 205, 14)],
    4: [(335, 132, -26), (445, 132, -14), (335, 202, 22), (445, 202, 14)],
    5: [(310, 130, -28), (390, 122, -20), (470, 132, -12), (345, 205, 20), (435, 205, 14)],
    6: [(300, 132, -30), (390, 120, -22), (480, 134, -12), (300, 202, 22), (390, 212, 16), (480, 200, 10)],
}
rotor_positions = ROTOR_LAYOUTS.get(int(device_count), ROTOR_LAYOUTS[4])
rotor_svg = "".join([
    f'<g transform="translate({x},{y})">'
    f'<circle r="23" fill="rgba(34,211,238,.16)" stroke="#22d3ee" stroke-width="2"/>'
    f'<rect x="-13" y="-34" width="26" height="56" rx="10" fill="#dbeafe" stroke="#d4b896"/>'
    f'<rect x="-13" y="-34" width="26" height="56" rx="10" fill="url(#ship)" opacity=".16"/>'
    f'<path d="M26 0 L68 {dy}" stroke="#7eb798" stroke-width="5" marker-end="url(#arrow)"/>'
    f'<text x="72" y="{dy+4}" fill="#7eb798" font-size="14" font-weight="700">推力</text>'
    f'</g>'
    for x, y, dy in rotor_positions
])

st.markdown(
    f"""
<div class="landing-shell">
  <div class="landing-main">
    <div class="small-tag">智慧海洋 · 绿色助航 · 船岸协同</div>
    <div class="landing-title">海帆智擎<br>智慧海洋绿色助航平台</div>
    <div class="landing-sub">废气余能驱动型智能滚筒帆系统</div>
    <div class="landing-desc">
      当前场景：<b>{st.session_state.get('preset_name','中东—东亚')}</b>。平台围绕“航线气象感知、AI智能推荐、滚筒帆助航、碳减排核算、设备健康复盘”构建智慧海洋应用闭环。
    </div>
    <div class="kpi-strip">
      <div class="kpi-mini"><span>推荐转速</span><b>{rpm} rpm</b><small>安全约束后输出</small></div>
      <div class="kpi-mini"><span>协同总推力</span><b>{total_thrust:.1f} kN</b><small>{device_count}座滚筒帆</small></div>
      <div class="kpi-mini"><span>节能潜力</span><b>{save_rate:.1f}%</b><small>演示工况估算</small></div>
      <div class="kpi-mini"><span>CII改善</span><b>{cii['base_rating']} → {cii['improved_rating']}</b><small>绿色航运价值</small></div>
    </div>
    <div class="workflow-ribbon">海况/船况感知 → 智能决策推荐 → 安全规则校核 → 助航执行建议 → 碳账本与孪生复盘</div>
  </div>
  <div class="landing-side">
    <div class="status-chip"><span class="dot"></span> 系统正常运行</div>
    <div class="side-title">当前演示状态</div>
    <div class="side-item"><span>运行模式</span><b>{mode}</b></div>
    <div class="side-item"><span>入口阀 / 旁通阀</span><b>{inlet:.0f}% / {bypass:.0f}%</b></div>
    <div class="side-item"><span>风速 / 风向角</span><b>{wind_speed:.1f} m/s · {wind_angle}°</b></div>
    <div class="side-item"><span>背压 / 海况</span><b>{back_pressure:.1f} kPa · {sea_state}级</b></div>
    <div class="route-card-polish">
      <div class="route-top"><span>航线模拟进度</span><b>{route_pct:.0f}%</b></div>
      <div style="margin-top:8px;color:#e6fbff;">已航行 <b>{route_done:,.0f} nm</b>　剩余 <b>{route_left:,.0f} nm</b></div>
      <div class="route-track"><i style="width:{route_pct:.0f}%"></i></div>
      <div style="margin-top:9px;color:#bbf7d0;font-weight:900;">当前位于{route_zone}</div>
    </div>
    <div class="footer-note">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# 首页快速演示区
st.markdown("""
<div class="scenario-panel">
  <div class="scenario-head">
    <div>
      <h3>四种典型工况快速切换</h3>
      <p>四种典型工况覆盖高效助航、低收益待机、主机保护和安全锁定，呈现系统在不同海况下的响应能力。</p>
    </div>
    <div class="small-tag">一键切换 · 参数联动 · 自动刷新</div>
  </div>
</div>
""", unsafe_allow_html=True)

scene_cols = st.columns(4)
for col, name in zip(scene_cols, DEMO_SCENARIOS.keys()):
    with col:
        st.button(name, use_container_width=True, key=f"main_demo_{name}", on_click=set_demo, args=(name,))

st.markdown("""
<div class="highlight-grid">
  <div class="highlight-card">
    <div class="small-tag">首要展示</div>
    <h4>智能决策引擎</h4>
    <p>把风况、海况、船速、主机背压和设备健康状态转化为可解释的 智能助航评分、风险评分和最终安全建议。</p>
    <div class="hl-num">预测 · 推荐 · 安全校核</div>
  </div>
  <div class="highlight-card">
    <div class="small-tag">智慧海洋核心</div>
    <h4>典型航区识别</h4>
    <p>基于四条典型航线识别适合启用滚筒帆的海区，体现“从单点仿真到航线级决策”的升级。</p>
    <div class="hl-num">航线识别 · 策略生成</div>
  </div>
  <div class="highlight-card">
    <div class="small-tag">绿色价值落地</div>
    <h4>航次碳账本</h4>
    <p>把助航效果量化为节省燃油、CO₂减排和 CII 改善，让作品从展示系统变成绿色航运评估工具。</p>
    <div class="hl-num">收益核算 · 绿色价值</div>
  </div>
</div>

<div class="demo-flow">
  <div class="demo-step"><div class="num">1</div><h4>态势总览</h4><p>全局掌握船舶运行状态、滚筒帆协同推力与节能潜力。</p></div>
  <div class="demo-step"><div class="num">2</div><h4>智能决策</h4><p>轻量评分模型综合工况参数，输出转速与阀门推荐策略。</p></div>
  <div class="demo-step"><div class="num">3</div><h4>航区识别</h4><p>基于四条典型航线自动判别高收益助航区与风险航段。</p></div>
  <div class="demo-step"><div class="num">4</div><h4>收益核算</h4><p>量化节油、减排与CII改善，生成可追溯的航次碳账本。</p></div>
</div>
""", unsafe_allow_html=True)


tabs = st.tabs(["态势总览", "智能决策引擎", "典型航区", "航次碳账本", "助航策略建议", "航线气象库", "设备健康", "多装置协同", "CII合规计算", "结构证据", "智慧演示台"])

with tabs[0]:
    st.markdown(
        f"""
<div class="compare-card">
  <div style="flex:1;">
    <div class="big">不开系统：<span style="color:#fbbf24;">CII评级 {cii['base_rating']}</span>　|　开启海帆智擎：<span class="good">CII评级 {cii['improved_rating']} ↑</span></div>
    <div style="margin-top:8px;color:#e8d8c0;">年省燃油：<b>{cii['base_fuel']-cii['improved_fuel']:.0f} 吨</b>　|　CO₂减排：<b>{cii['base_co2']-cii['improved_co2']:.0f} 吨</b></div>
    <div class="line"><i></i></div>
  </div>
  <div style="text-align:right; min-width:260px;">
    <div class="small-tag">系统价值总览</div>
    <div style="margin-top:8px;color:#f0fbff;">智能决策引擎 · 典型航区识别 · 航次碳账本</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        ("推荐转速", f"{rpm} rpm", "Rotor RPM · 规则推荐区间"),
        ("单座推力", f"{single_thrust:.1f} kN", "简化气动模型"),
        ("协同总推力", f"{total_thrust:.1f} kN", f"{device_count}座装置 · 多装置修正"),
        ("入口阀", f"{inlet:.0f}%", "Inlet Valve"),
        ("旁通阀", f"{bypass:.0f}%", "Bypass"),
        ("评分稳定性", f"{confidence:.1f}%", "演示级评分"),
    ]
    for col, item in zip([c1, c2, c3, c4, c5, c6], cards):
        col.markdown(metric_card(*item), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    left, mid, right = st.columns([1.05, 1.25, 1])
    with left:
        st.markdown("<div class='section-title'>智能控制建议</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="card" style="min-height:310px;">
  <div style="display:flex;gap:16px;align-items:center;margin-bottom:16px;"><div class="ai-orb">智控</div><div><div class="k-label">当前运行模式</div><div class="mode-pill {mode_class}">{mode}</div></div></div>
  <p style="color:#c8eaff;line-height:1.8;">{reason}</p>
  <p style="color:#c8eaff;line-height:1.8;">建议保持 <b>{device_count}</b> 座滚筒帆协同运行，目标转速 <b>{rpm} rpm</b>，入口阀约 <b>{inlet:.0f}%</b>，旁通阀约 <b>{bypass:.0f}%</b>。</p>
  <p style="color:#c8eaff;line-height:1.8;">当前总助航推力约 <b>{total_thrust:.1f} kN</b>，航次节能潜力约 <b>{save_rate:.1f}%</b>。</p>
  <p style="color:#9fd9f1;line-height:1.8;">模型定位：<b>辅助推荐</b>，安全规则优先于 智能推荐。</p>
</div>
""",
            unsafe_allow_html=True,
        )
    with mid:
        st.markdown("<div class='section-title'>船舶与滚筒帆态势</div>", unsafe_allow_html=True)
        ship_svg = f"""
<div class="ship-svg">
<svg viewBox="0 0 760 320" width="100%" height="320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ship" x1="0" x2="1"><stop offset="0" stop-color="#1a1612"/><stop offset="1" stop-color="#8b6914"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="760" height="320" fill="transparent"/>
  <g opacity=".18" stroke="#e8b866" stroke-width="1">{''.join([f'<line x1="{i}" y1="0" x2="{i}" y2="320"/>' for i in range(40,760,55)])}{''.join([f'<line x1="0" y1="{i}" x2="760" y2="{i}"/>' for i in range(30,320,45)])}</g>
  <path d="M165 235 C145 200 145 116 168 86 C232 40 510 40 610 95 C648 118 650 205 610 230 C510 285 245 285 165 235Z" fill="url(#ship)" stroke="#d4b896" stroke-width="2" opacity=".95"/>
  <path d="M218 222 C205 198 204 122 220 96 C288 72 494 74 572 106 C598 132 598 198 572 219 C492 252 287 250 218 222Z" fill="#181410" opacity=".55" stroke="#8a8278" stroke-width="1"/>
  <path d="M635 160 L700 126 L700 194 Z" fill="#c07020" opacity=".9" filter="url(#glow)"/><text x="664" y="113" fill="#d4b896" font-size="18" font-weight="700">航向 {int(abs(wind_angle))}°</text>
  {rotor_svg}
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#7eb798"/></marker></defs>
  <g opacity=".82"><path d="M180 245 C120 260 92 278 70 305" stroke="#f97316" stroke-width="9" stroke-linecap="round" opacity=".5"/><path d="M180 235 C110 226 85 219 58 202" stroke="#e0f2fe" stroke-width="10" stroke-linecap="round" opacity=".28"/></g>
  <path d="M110 84 C200 30 410 22 650 62" stroke="#d4b896" stroke-dasharray="12 12" stroke-width="3" opacity=".75" fill="none"/>
  <text x="36" y="50" fill="#d4b888" font-size="18" font-weight="700">相对风速 {rel_ws:.1f} m/s</text>
  <path d="M50 78 L130 118" stroke="#e8b866" stroke-width="5" marker-end="url(#wind)" filter="url(#glow)"/><defs><marker id="wind" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#e8b866"/></marker></defs>
</svg>
</div>
"""
        st.markdown(ship_svg, unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-title'>安全与能效</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="card" style="min-height:310px;">
  <div class="k-label">排气背压</div><div class="bar-wrap"><div class="bar" style="width:{min(back_pressure/5*100,100):.0f}%"></div></div><p>{back_pressure:.1f}/5.0 kPa（演示阈值）</p>
  <div class="k-label">主机负荷</div><div class="bar-wrap"><div class="bar" style="width:{engine_load:.0f}%"></div></div><p>{engine_load}%</p>
  <div class="k-label">模型稳定性</div><div class="bar-wrap"><div class="bar" style="width:{confidence:.0f}%"></div></div><p>{confidence:.1f}%</p>
  <div class="k-label">航次节能潜力</div><div class="bar-wrap"><div class="bar" style="width:{save_rate/32*100:.0f}%"></div></div><p>{save_rate:.1f}%</p>
</div>
""",
            unsafe_allow_html=True,
        )

with tabs[4]:
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown("<div class='section-title'>助航策略建议表</div>", unsafe_allow_html=True)
        result_df = pd.DataFrame({
            "指标": ["表观风速", "风向角", "船速", "海况", "推荐转速", "单座推力", "协同总推力", "航次节能潜力", "运行模式"],
            "数值": [f"{wind_speed:.1f} m/s", f"{wind_angle}°", f"{ship_speed:.1f} kn", f"{sea_state}级", f"{rpm} rpm", f"{single_thrust:.1f} kN", f"{total_thrust:.1f} kN", f"{save_rate:.1f}%", mode],
        })
        st.markdown(html_table(result_df), unsafe_allow_html=True)
    with right:
        st.markdown("<div class='section-title'>安全规则说明</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='notice'><b>安全规则优先于智能推荐。</b><br>当排气背压接近 5.0 kPa 演示阈值、海况等级过高或风速极端时，系统自动进入保护或安全模式。当前判定依据：{reason}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(metric_card("模型定位", "辅助推荐", "不直接控制实船设备"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(sankey_figure(inlet, bypass), use_container_width=True, config={"displayModeBar": False}, key="sankey_energy_flow")

with tabs[7]:
    st.markdown("<div class='section-title'>多装置协同仿真</div>", unsafe_allow_html=True)
    rows = []
    for n in range(1, 7):
        factor = 1 - 0.03 * (n - 1)
        thrust_n = single_thrust * n * factor
        save_n = float(np.clip(4 + thrust_n * 0.020 + (inlet / 100) * 5, 0, 32))
        rows.append({"装置数量": n, "总推力(kN)": round(thrust_n, 1), "航次节能潜力(%)": round(save_n, 1), "干扰修正系数": round(factor, 2)})
    df_multi = pd.DataFrame(rows)
    st.altair_chart(alt_bar(df_multi, "装置数量", ["总推力(kN)", "航次节能潜力(%)"], "多座滚筒帆协同收益"), use_container_width=True)
    st.markdown(html_table(df_multi), unsafe_allow_html=True)
    st.caption("展示不同装置数量下的总推力与节能潜力变化。")

with tabs[8]:
    st.markdown("<div class='section-title'>CII合规计算</div>", unsafe_allow_html=True)
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        ship_type = st.selectbox("船型", ["散货船/油轮", "集装箱船", "LNG运输船"], key="ship_type")
    with col_b:
        dwt = st.number_input("DWT", min_value=10000, max_value=350000, step=10000, key="dwt")
    with col_c:
        route_distance = st.number_input("单航段距离(nm)", min_value=300, max_value=15000, step=100, key="route_distance")
    with col_d:
        annual_days = st.slider("年航行天数", 100, 320, key="annual_days")
    cii = cii_demo(dwt, route_distance, ship_speed, annual_days, ship_type, save_rate)
    g1, g2, g3 = st.columns([1, 1, 1])
    g1.markdown(metric_card("不开启系统", f"{cii['base_rating']}级", f"CII {cii['base_cii']:.2f} gCO₂/(DWT·nm)"), unsafe_allow_html=True)
    g2.markdown(metric_card("开启海帆智擎", f"{cii['improved_rating']}级", f"CII {cii['improved_cii']:.2f} gCO₂/(DWT·nm)"), unsafe_allow_html=True)
    g3.markdown(metric_card("预计年度减排", f"{cii['base_co2']-cii['improved_co2']:.0f} 吨", f"燃油减少 {cii['base_fuel']-cii['improved_fuel']:.0f} 吨"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

with tabs[5]:
    st.markdown("<div class='section-title'>四航线气象数据库 + 海况接入</div>", unsafe_allow_html=True)

    db_c1, db_c2, db_c3 = st.columns([1.1, 1, 1])
    with db_c1:
        route_name_for_db = st.selectbox("选择航线数据库", FOUR_ROUTE_NAMES, index=FOUR_ROUTE_NAMES.index(resolve_route_name(st.session_state.get("preset_name", "中东—东亚"))))
    with db_c2:
        use_live_marine = st.toggle("接入实时海况 API", value=True, help="调用 Open-Meteo Weather API 与 Marine API。若失败自动回退到本地样本。")
    with db_c3:
        if st.button("刷新海况数据", use_container_width=True):
            fetch_open_meteo_route.clear()
            st.toast("已请求刷新海况数据")

    weather_df, data_mode, source_msg = get_route_weather(route_name_for_db, wind_speed, wind_angle, sea_state, use_live=use_live_marine)
    route_desc = ROUTE_DATABASE[route_name_for_db]["desc"]
    st.markdown(f"<div class='notice'><b>{route_name_for_db}</b>：{route_desc}<br>数据状态：{source_msg}</div>", unsafe_allow_html=True)

    if not weather_df.empty:
        avg_wind = weather_df["风速(m/s)"].mean()
        avg_wave = weather_df["浪高(m)"].mean()
        avg_current = weather_df["流速(kn)"].mean()
        high_potential = int((weather_df["风助潜力"] > 8).sum())
        high_risk = int((weather_df["风险等级"] == "高").sum())
        source_label = "实时接口" if data_mode == "live" else "演示样本"
        st.markdown(
            f"""
<div class="weather-grid">
  <div class="weather-card"><span>数据源</span><b>{source_label}</b><small>{weather_df['更新时间'].iloc[0]}</small></div>
  <div class="weather-card"><span>平均风速</span><b>{avg_wind:.1f} m/s</b><small>航线节点均值</small></div>
  <div class="weather-card"><span>平均浪高</span><b>{avg_wave:.1f} m</b><small>用于安全模式判断</small></div>
  <div class="weather-card"><span>平均海流</span><b>{avg_current:.2f} kn</b><small>用于航线风险评估</small></div>
</div>
<div class="weather-grid">
  <div class="weather-card"><span>航线距离</span><b>{ROUTE_DATABASE[route_name_for_db]['distance_nm']:,} nm</b><small>数据库预设距离</small></div>
  <div class="weather-card"><span>高风助节点</span><b>{high_potential} 个</b><small>适合进入高效助航</small></div>
  <div class="weather-card"><span>高风险节点</span><b>{high_risk} 个</b><small>需触发安全策略</small></div>
  <div class="weather-card"><span>节点数量</span><b>{len(weather_df)} 个</b><small>当前展示采样点</small></div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.plotly_chart(route_weather_map(weather_df), use_container_width=True, config={"displayModeBar": False}, key="route_weather_map")
        show_cols = ["序号", "航线", "海区", "航段", "风速(m/s)", "阵风(m/s)", "风向(°)", "浪高(m)", "浪向(°)", "浪周期(s)", "流速(kn)", "流向(°)", "海温(℃)", "海况等级", "风助潜力", "风险等级", "建议策略", "数据源"]
        st.markdown(html_table(weather_df[show_cols]), unsafe_allow_html=True)
        st.download_button(
            "下载当前航线气象数据库 CSV",
            data=weather_df[show_cols].to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"{route_name_for_db}_航线气象数据库.csv",
            mime="text/csv",
            use_container_width=True,
        )

with tabs[2]:
    st.markdown("<div class='section-title'>典型航区识别</div>", unsafe_allow_html=True)

    zc1, zc2, zc3 = st.columns([1.1, 1, 1])
    with zc1:
        zone_route = st.selectbox("选择典型航区航线", FOUR_ROUTE_NAMES, index=FOUR_ROUTE_NAMES.index(resolve_route_name(st.session_state.get("preset_name", "中东—东亚"))), key="zone_route")
    with zc2:
        zone_live = st.toggle("使用实时海况数据识别", value=False, key="zone_live", help="开启后调用实时海况接口；网络不稳定时建议关闭。")
    with zc3:
        zone_sensitivity = st.slider("安全保守系数", 0.8, 1.3, 1.0, 0.1, help="系数越高，越容易把航段判定为谨慎或安全锁定。")

    zone_df, zone_mode, zone_msg = build_assist_zone_frame(zone_route, wind_speed, wind_angle, ship_speed, back_pressure * zone_sensitivity, sea_state, device_count, use_live=zone_live)
    if not zone_df.empty:
        zone_sum = assist_zone_summary(zone_df)
        high_nm = float(zone_df.loc[zone_df["助航区类型"].eq("高效助航区"), "代表航段距离(nm)"].sum())
        caution_nm = float(zone_df.loc[zone_df["助航区类型"].eq("谨慎运行区"), "代表航段距离(nm)"].sum())
        stop_nm = float(zone_df.loc[zone_df["助航区类型"].eq("安全锁定区"), "代表航段距离(nm)"].sum())
        best_node = zone_df.sort_values(["风助潜力", "估算推力(kN)"], ascending=False).iloc[0]
        avg_zone_save = float(np.average(zone_df["节能潜力(%)"], weights=zone_df["代表航段距离(nm)"]))

        st.markdown(f"<div class='notice'>数据状态：{zone_msg}<br>识别结论：{zone_route} 中高收益助航里程约 <b>{high_nm:,.0f} nm</b>，建议优先关注 <b>{best_node['海区']}</b>，该节点风助潜力最高。</div>", unsafe_allow_html=True)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.markdown(metric_card("高收益助航里程", f"{high_nm:,.0f} nm", "推荐全开滚筒帆"), unsafe_allow_html=True)
        m2.markdown(metric_card("谨慎运行里程", f"{caution_nm:,.0f} nm", "中低转速运行"), unsafe_allow_html=True)
        m3.markdown(metric_card("安全锁定里程", f"{stop_nm:,.0f} nm", "旁通优先"), unsafe_allow_html=True)
        m4.markdown(metric_card("典型代表海区", str(best_node["海区"]), f"推力 {best_node['估算推力(kN)']} kN"), unsafe_allow_html=True)
        m5.markdown(metric_card("航线平均节能", f"{avg_zone_save:.1f}%", "按区段加权"), unsafe_allow_html=True)

        left_z, right_z = st.columns([1.25, 1])
        with left_z:
            st.plotly_chart(assist_zone_map(zone_df), use_container_width=True, config={"displayModeBar": False}, key="assist_zone_map_main")
        with right_z:
            st.plotly_chart(assist_zone_distance_chart(zone_sum), use_container_width=True, config={"displayModeBar": False}, key="assist_zone_distance_main")

        show_zone_cols = ["序号", "海区", "航段", "风速(m/s)", "浪高(m)", "海况等级", "风助潜力", "风险等级", "助航区", "推荐转速(rpm)", "估算推力(kN)", "节能潜力(%)", "建议策略"]
        st.markdown(html_table(zone_df[show_zone_cols]), unsafe_allow_html=True)
        st.download_button(
            "下载典型航区识别结果 CSV",
            data=zone_df.drop(columns=["助航区"]).to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"{zone_route}_典型航区识别.csv",
            mime="text/csv",
            use_container_width=True,
        )

with tabs[3]:
    st.markdown("<div class='section-title'>航次碳账本</div>", unsafe_allow_html=True)

    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        ledger_route = st.selectbox("碳账本航线", FOUR_ROUTE_NAMES, index=FOUR_ROUTE_NAMES.index(resolve_route_name(st.session_state.get("preset_name", "中东—东亚"))), key="ledger_route")
    with bc2:
        ledger_ship_type = st.selectbox("船型", ["散货船/油轮", "集装箱船", "LNG运输船"], key="ledger_ship_type")
    with bc3:
        ledger_dwt = st.number_input("载重吨 DWT", min_value=10000, max_value=350000, value=int(st.session_state.get("dwt", 150000)), step=10000, key="ledger_dwt")
    with bc4:
        ledger_speed = st.slider("平均航速 kn", 8.0, 20.0, float(ship_speed), 0.5, key="ledger_speed")

    ledger_zone_df, _, _ = build_assist_zone_frame(ledger_route, wind_speed, wind_angle, ledger_speed, back_pressure, sea_state, device_count, use_live=False)
    ledger_df, ledger_stats = build_carbon_ledger(ledger_route, ledger_ship_type, ledger_dwt, ledger_speed, device_count, ledger_zone_df)
    ledger_zone_sum = assist_zone_summary(ledger_zone_df)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(metric_card("节省燃油", f"{ledger_stats['fuel_saved']:.1f} 吨", "本航次估算"), unsafe_allow_html=True)
    k2.markdown(metric_card("CO₂减排", f"{ledger_stats['co2_saved']:.1f} 吨", "本航次估算"), unsafe_allow_html=True)
    k3.markdown(metric_card("平均节能", f"{ledger_stats['avg_save']:.1f}%", "按助航区加权"), unsafe_allow_html=True)
    k4.markdown(metric_card("绿色助航里程", f"{ledger_stats['high_nm']:,.0f} nm", "高效助航区"), unsafe_allow_html=True)
    k5.markdown(metric_card("CII变化", f"{cii_rating(ledger_stats['base_cii'], ledger_ship_type)} → {cii_rating(ledger_stats['improved_cii'], ledger_ship_type)}", "演示估算"), unsafe_allow_html=True)

    left_b, right_b = st.columns([1, 1])
    with left_b:
        st.plotly_chart(carbon_ledger_chart(ledger_stats), use_container_width=True, config={"displayModeBar": False}, key="carbon_ledger_chart")
    with right_b:
        st.markdown(html_table(ledger_df), unsafe_allow_html=True)

    report_text = build_voyage_report(ledger_route, ledger_stats, ledger_zone_sum)
    st.markdown(f"<div class='report-card'><b>自动生成航次复盘摘要</b><br>{report_text}</div>", unsafe_allow_html=True)
    st.download_button(
        "下载航次碳账本与复盘摘要 TXT",
        data=report_text,
        file_name=f"{ledger_route}_航次碳账本摘要.txt",
        mime="text/plain",
        use_container_width=True,
    )

with tabs[6]:
    st.markdown("<div class='section-title'>设备健康管理与维护建议</div>", unsafe_allow_html=True)

    health_df = build_health_frame(wind_speed, sea_state, back_pressure, rpm, inlet, bypass, engine_load, device_count)
    avg_health = float(health_df["健康度(%)"].mean())
    min_row = health_df.sort_values("健康度(%)").iloc[0]
    p1_count = int((health_df["健康度(%)"] < 78).sum())
    p2_count = int(((health_df["健康度(%)"] >= 78) & (health_df["健康度(%)"] < 88)).sum())
    min_rul = int(health_df["预计剩余寿命(h)"].min())

    h1, h2, h3, h4, h5 = st.columns(5)
    h1.markdown(metric_card("综合健康度", f"{avg_health:.1f}%", "全系统平均"), unsafe_allow_html=True)
    h2.markdown(metric_card("薄弱部件", str(min_row["部件"]), f"{min_row['健康度(%)']:.1f}%"), unsafe_allow_html=True)
    h3.markdown(metric_card("高优先级任务", f"{p1_count} 项", "P1立即/本航次"), unsafe_allow_html=True)
    h4.markdown(metric_card("靠港检查任务", f"{p2_count} 项", "P2靠港后"), unsafe_allow_html=True)
    h5.markdown(metric_card("最短剩余寿命", f"{min_rul} h", "演示估算"), unsafe_allow_html=True)

    left_h, right_h = st.columns([1, 1])
    with left_h:
        st.plotly_chart(health_radar_chart(health_df), use_container_width=True, config={"displayModeBar": False}, key="health_radar_chart")
    with right_h:
        plan_df = maintenance_plan(health_df)
        st.markdown(html_table(plan_df), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>设备健康明细</div>", unsafe_allow_html=True)
    st.markdown(html_table(health_df), unsafe_allow_html=True)

    maintenance_text = (
        f"当前综合健康度为{avg_health:.1f}%，最低健康部件为{min_row['部件']}（{min_row['健康度(%)']:.1f}%）。"
        f"系统建议优先关注{min_row['监测依据']}，维护动作：{min_row['维护建议']}。"
        f"若后续接入实船振动、温度、转速和阀门响应数据，可将该模块升级为预测性维护模型。"
    )
    st.markdown(f"<div class='report-card'><b>维护建议摘要</b><br>{maintenance_text}</div>", unsafe_allow_html=True)
    st.download_button(
        "下载设备健康与维护建议 CSV",
        data=health_df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="设备健康管理与维护建议.csv",
        mime="text/csv",
        use_container_width=True,
    )


with tabs[1]:
    st.markdown("<div class='section-title'>智能决策引擎：从数据到可执行建议</div>", unsafe_allow_html=True)

    # 设备健康作为AI诊断输入
    ai_health_df = build_health_frame(wind_speed, sea_state, back_pressure, rpm, inlet, bypass, engine_load, device_count)
    ai_result = ai_decision_engine(
        wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state,
        device_count, rpm, inlet, bypass, total_thrust, save_rate, ai_health_df
    )

    st.markdown("""
<div class="ai-engine-grid">
  <div class="ai-role-card"><div class="role-icon">&Sigma;</div><h4>预测</h4><p>预测当前工况下的助航推力、推荐转速、节能潜力和阀门开度。</p></div>
  <div class="ai-role-card"><div class="role-icon">&equiv;</div><h4>识别</h4><p>识别整条航线中的高收益助航区、谨慎运行区、待机区和安全锁定区。</p></div>
  <div class="ai-role-card"><div class="role-icon">&there4;</div><h4>推荐</h4><p>在主机背压、海况等级和人工控制约束下生成运行模式与执行建议。</p></div>
  <div class="ai-role-card"><div class="role-icon">&loz;</div><h4>诊断</h4><p>结合设备健康参数，评估薄弱部件、维护优先级和剩余寿命。</p></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="flow-row">
  <div class="flow-node"><b>多源数据输入</b><br>航线气象 / 船速航向 / 主机背压 / 设备健康</div>
  <div class="flow-arrow">→</div>
  <div class="flow-node"><b>演示级轻量评分</b><br>评分模型 / 推力估算 / 风险识别 / 健康诊断</div>
  <div class="flow-arrow">→</div>
  <div class="flow-node"><b>安全约束输出</b><br>转速 / 阀门 / 模式 / 维护 / 复盘建议</div>
</div>
""", unsafe_allow_html=True)

    g1, g2, g3, g4 = st.columns(4)
    g1.markdown(metric_card("智能助航评分", f"{ai_result['assist_score']:.1f}/100", "航线与当前工况综合"), unsafe_allow_html=True)
    g2.markdown(metric_card("运行风险评分", f"{ai_result['risk_score']:.1f}/100", "海况/背压/机况约束"), unsafe_allow_html=True)
    g3.markdown(metric_card("模型原始建议", ai_result["raw_mode"], "模型推荐"), unsafe_allow_html=True)
    g4.markdown(metric_card("最终安全建议", ai_result["final_mode"], ai_result["status_text"]), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>本次决策依据</div>", unsafe_allow_html=True)
    st.markdown(ai_reason_cards(ai_result, wind_speed, wind_angle, back_pressure, sea_state), unsafe_allow_html=True)

    left_ai, right_ai = st.columns([1, 1])
    with left_ai:
        st.plotly_chart(ai_score_gauge("智能助航评分", ai_result["assist_score"], "#22d3ee"), use_container_width=True, config={"displayModeBar": False}, key="ai_assist_score_gauge")
    with right_ai:
        st.plotly_chart(ai_score_gauge("风险评分", ai_result["risk_score"], "#d4b896" if ai_result["risk_score"] < 55 else "#d4983a"), use_container_width=True, config={"displayModeBar": False}, key="ai_risk_score_gauge")

    c_left, c_right = st.columns([1.15, 1])
    with c_left:
        st.plotly_chart(ai_feature_chart(ai_result["factors"]), use_container_width=True, config={"displayModeBar": False}, key="ai_feature_chart")
    with c_right:
        st.markdown("<div class='section-title'>智能决策输出矩阵</div>", unsafe_allow_html=True)
        st.markdown(html_table(ai_result["outputs"]), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>规则约束条件</div>", unsafe_allow_html=True)
    st.markdown(html_table(ai_result["safety"]), unsafe_allow_html=True)

    st.markdown(f"<div class='decision-box'><b>智能决策生成的本次运行建议</b><br>{ai_result['recommendation']}</div>", unsafe_allow_html=True)


    ai_report = (
        "海帆智擎智能决策引擎报告\n"
        f"当前智能助航评分：{ai_result['assist_score']:.1f}/100\n"
        f"当前运行风险评分：{ai_result['risk_score']:.1f}/100\n"
        f"模型原始建议：{ai_result['raw_mode']}\n"
        f"最终安全建议：{ai_result['final_mode']}\n"
        f"推荐说明：{ai_result['recommendation']}\n"
    )
    st.download_button(
        "下载智能决策引擎报告 TXT",
        data=ai_report,
        file_name="海帆智擎_智能决策引擎报告.txt",
        mime="text/plain",
        use_container_width=True,
    )




with tabs[9]:
    st.markdown("<div class='section-title'>装置结构与传动链路证据区</div>", unsafe_allow_html=True)
    st.markdown("""
<div class="linkage-web">
该区域用于把作品从“纯仪表盘”拉回到“器件/装置/软件一体化”。以下图片为本项目结构建模图，用于展示双排气管路、透平/阀门组件、滚筒帆底部支承、轴承圈、传动部件和能量链路。网页中的推力、节能、CII 等数字仍为演示级趋势估算，结构图片用于增强硬件创新可信度。
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="energy-flow-web"><div class="node">主机废气<br><small>排气能量输入</small></div><div class="arrow">→</div><div class="node">轴流透平<br><small>取能与背压约束</small></div><div class="arrow">→</div><div class="node">齿轮/传动单元<br><small>转速匹配</small></div><div class="arrow">→</div><div class="node">滚筒帆旋转<br><small>马格努斯助航力</small></div></div>
<div class="part-legend-web"><span><b>1/2</b>排气入口与支路</span><span><b>3</b>透平/叶轮单元</span><span><b>4</b>控制执行机构</span><span><b>5</b>滚筒帆筒体</span><span><b>7/8</b>阀门组件</span><span><b>9</b>齿轮传动件</span><span><b>11/12</b>轴承与密封圈</span><span><b>201/202</b>双排气管路</span></div>
""", unsafe_allow_html=True)

    evidence_items = [
        ("assets/evidence/evidence_02_rotor_base_assembly.jpg", "旋筒帆底座与双排气管路装配", "展示滚筒帆底部支承、双排气管路、阀门组件与传动机构的空间关系。"),
        ("assets/evidence/evidence_01_pipe_top.jpg", "双管路与旁通阀总体布置", "体现排气主通道、取能支路和旁通支路之间的连接关系。"),
        ("assets/evidence/evidence_05_turbine_valve_pipeline.jpg", "废气透平—阀门—管路连接", "为“废气余能驱动型滚筒帆”提供实体结构依据。"),
        ("assets/evidence/evidence_03_exploded_structure.jpg", "滚筒帆爆炸结构图", "展示筒体、轴承圈、底座与传动部件的分解关系。"),
        ("assets/evidence/evidence_04_rotor_column_support.jpg", "立式滚筒帆与底部支承结构", "展示高筒体与底部轴承、支承及连接件的关系。"),
        ("assets/evidence/evidence_06_turbine_drive_unit.jpg", "透平/齿轮驱动单元局部", "突出取能部件、齿轮传动和执行机构。"),
        ("assets/evidence/evidence_07_support_connection.jpg", "底部传动与滚筒帆支承连接", "补充滚筒帆底部支承与管路接口之间的结构完整性证据。"),
    ]
    img_root = Path(__file__).resolve().parent
    cols = st.columns(2)
    for i, (rel_path, title, desc) in enumerate(evidence_items):
        with cols[i % 2]:
            img_path = img_root / rel_path
            st.image(str(img_path), caption=title, use_container_width=True)
            st.markdown(
                f"<div class='evidence-web-card'><h4>{title}</h4><p>{desc}</p></div>",
                unsafe_allow_html=True,
            )

    st.markdown("""
<div class="linkage-web">
<b>证据定位：</b>以上图片用于说明硬件结构、管路走向和传动路径。后续进入工程化阶段后，应继续补充台架实验、CFD/风洞分析、主机背压安全验证、阀门响应测试和船级社规范校核。
</div>
""", unsafe_allow_html=True)



# =========================
# SMART DEMO CONSOLE
# Added for competition presentation: AI explainability, abnormal scenarios, route-level assist windows.
# =========================
with tabs[10]:
    st.markdown("<div class='section-title'>智慧演示台：解释、处置与航线级助航窗口</div>", unsafe_allow_html=True)
    st.markdown(
        """
<div class='notice'>
该页面把平台的“智慧性”集中展示为三件事：<b>解释为什么这样推荐</b>、<b>遇到异常工况自动给出处置</b>、<b>从整条航线识别最优助航窗口</b>。当前为竞赛原型，采用简化模型、本地样本库与安全规则校核，不作为实船自动控制指令。
</div>
""",
        unsafe_allow_html=True,
    )

    smart_health_df = build_health_frame(wind_speed, sea_state, back_pressure, rpm, inlet, bypass, engine_load, device_count)
    smart_ai = ai_decision_engine(
        wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state,
        device_count, rpm, inlet, bypass, total_thrust, save_rate, smart_health_df
    )

    st.markdown("<div class='section-title'>一、AI 决策解释卡</div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    s1.markdown(metric_card("综合助航评分", f"{smart_ai['assist_score']:.1f}/100", "越高越适合开启助航"), unsafe_allow_html=True)
    s2.markdown(metric_card("综合风险评分", f"{smart_ai['risk_score']:.1f}/100", "越高越需要保守运行"), unsafe_allow_html=True)
    s3.markdown(metric_card("模型原始建议", smart_ai["raw_mode"], "轻量评分模型输出"), unsafe_allow_html=True)
    s4.markdown(metric_card("最终安全建议", smart_ai["final_mode"], smart_ai["status_text"]), unsafe_allow_html=True)
    st.markdown(ai_reason_cards(smart_ai, wind_speed, wind_angle, back_pressure, sea_state), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>二、异常工况自动处置</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='safe-line'>点击下方按钮可一键切换典型异常工况，观察系统如何从追求节能转向安全保护。建议录屏时依次演示“低收益待机 → 主机保护 → 安全锁定”。</div>",
        unsafe_allow_html=True,
    )
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("横风高效助航", key="smart_demo_crosswind", use_container_width=True):
            set_demo("横风 12m/s · 高效助航")
            st.rerun()
    with b2:
        if st.button("微风低收益待机", key="smart_demo_lowwind", use_container_width=True):
            set_demo("微风 5m/s · 低收益待机")
            st.rerun()
    with b3:
        if st.button("背压过高保护", key="smart_demo_backpressure", use_container_width=True):
            set_demo("背压 4.8kPa · 主机保护")
            st.rerun()
    with b4:
        if st.button("海况7级锁定", key="smart_demo_seastate", use_container_width=True):
            set_demo("海况 7级 · 安全锁定")
            st.rerun()

    sensor_now = build_sensor_frame(wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state, rpm, inlet, bypass)
    alert_df = operational_alerts(wind_speed, wind_angle, ship_speed, engine_load, back_pressure, sea_state, mode, sensor_now, smart_health_df)
    a1, a2 = st.columns([1.05, 1])
    with a1:
        st.markdown("<div class='section-title'>系统处置建议</div>", unsafe_allow_html=True)
        st.markdown(html_table(alert_df), unsafe_allow_html=True)
    with a2:
        sop_lines = []
        if mode == "高效助航模式":
            sop_lines = ["确认背压与海况在安全阈值内", f"入口阀逐步开至 {inlet:.0f}%", f"目标转速稳定在 {rpm} rpm", "每15分钟复核风速、背压、振动和阀位"]
        elif mode == "低收益待机模式":
            sop_lines = ["保持低速或间歇运行", "避免无效取能造成额外阻力", "持续观察侧风分量是否回升", "进入高收益窗口后再提高转速"]
        elif mode == "主机保护模式":
            sop_lines = ["旁通阀优先打开，保证主机排烟", "禁止继续提高入口阀开度", "通知轮机员复核背压传感器", "背压恢复后再人工确认是否恢复助航"]
        else:
            sop_lines = ["入口阀关闭，旁通阀全开", "滚筒帆降速或锁定", "驾驶台人工确认海况与航速", "待海况降低后重新评估"]
        st.markdown("<div class='section-title'>值班 SOP</div>", unsafe_allow_html=True)
        st.markdown("<div class='sop-card'><b>当前模式：</b>" + mode + "<br>" + "<br>".join([f"{i+1}. {x}" for i, x in enumerate(sop_lines)]) + "</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>三、航线级最优助航窗口</div>", unsafe_allow_html=True)
    wc1, wc2, wc3 = st.columns([1.1, 1, 1])
    with wc1:
        smart_route = st.selectbox("选择航线", FOUR_ROUTE_NAMES, index=FOUR_ROUTE_NAMES.index(resolve_route_name(st.session_state.get("preset_name", "中东—东亚"))), key="smart_window_route")
    with wc2:
        smart_live = st.toggle("尝试实时海况接入", value=False, key="smart_window_live", help="网络不稳定时建议关闭，系统会自动回退到本地样本库。")
    with wc3:
        smart_conservative = st.slider("安全保守系数", 0.8, 1.3, 1.0, 0.1, key="smart_window_conservative")

    smart_zone_df, smart_zone_mode, smart_zone_msg = build_assist_zone_frame(
        smart_route, wind_speed, wind_angle, ship_speed, back_pressure * smart_conservative, sea_state, device_count, use_live=smart_live
    )
    if not smart_zone_df.empty:
        smart_sum = assist_zone_summary(smart_zone_df)
        high_df = smart_zone_df[smart_zone_df["助航区类型"].eq("高效助航区")].copy()
        high_nm = float(high_df["代表航段距离(nm)"].sum()) if not high_df.empty else 0.0
        total_nm = float(smart_zone_df["代表航段距离(nm)"].sum()) or 1.0
        cover = high_nm / total_nm * 100
        best = smart_zone_df.sort_values(["风助潜力", "估算推力(kN)"], ascending=False).iloc[0]
        avg_save = float(np.average(smart_zone_df["节能潜力(%)"], weights=smart_zone_df["代表航段距离(nm)"]))
        w1, w2, w3, w4 = st.columns(4)
        w1.markdown(metric_card("高效助航窗口", f"{len(high_df)} 个", f"覆盖 {cover:.0f}% 航程"), unsafe_allow_html=True)
        w2.markdown(metric_card("高效助航里程", f"{high_nm:,.0f} nm", "按代表航段距离估算"), unsafe_allow_html=True)
        w3.markdown(metric_card("最优海区", str(best["海区"]), f"推力 {best['估算推力(kN)']} kN"), unsafe_allow_html=True)
        w4.markdown(metric_card("航线平均节能", f"{avg_save:.1f}%", "按航段加权估算"), unsafe_allow_html=True)
        st.markdown(f"<div class='notice'>数据状态：{smart_zone_msg}<br>系统判断：建议在 <b>{best['海区']}</b> 优先开启高效助航；若进入谨慎运行区，应降低转速并保留旁通安全余量。</div>", unsafe_allow_html=True)
        c_map, c_chart = st.columns([1.2, 1])
        with c_map:
            st.plotly_chart(assist_zone_map(smart_zone_df), use_container_width=True, config={"displayModeBar": False}, key="assist_zone_map_smart_demo")
        with c_chart:
            st.plotly_chart(assist_zone_distance_chart(smart_sum), use_container_width=True, config={"displayModeBar": False}, key="assist_zone_distance_smart_demo")
        show_cols = ["序号", "海区", "航段", "风速(m/s)", "浪高(m)", "海况等级", "风助潜力", "风险等级", "助航区", "推荐转速(rpm)", "估算推力(kN)", "节能潜力(%)", "建议策略"]
        st.markdown(html_table(smart_zone_df[show_cols]), unsafe_allow_html=True)
        task_sheet = build_voyage_task_sheet(smart_route, smart_zone_df, mode, rpm, inlet, bypass, device_count)
        st.download_button(
            "下载智慧演示台结果 CSV",
            data=smart_zone_df[show_cols].to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"{smart_route}_智慧助航窗口识别.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.download_button(
            "下载航段任务单 CSV",
            data=task_sheet.to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"{smart_route}_航段执行任务单.csv",
            mime="text/csv",
            use_container_width=True,
        )
