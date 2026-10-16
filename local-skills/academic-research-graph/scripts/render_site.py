#!/usr/bin/env python3
"""Render graph.json into a standalone interactive, increment-aware HTML network with optional embedded paper figures."""
from __future__ import annotations

import argparse
import base64
import copy
import html
import json
import mimetypes
import os
from pathlib import Path
from typing import Any

LABELS = {
    "zh-CN": {
        "nodes": "节点", "edges": "关系", "search_label": "搜索论文或概念",
        "search_placeholder": "标题、作者、角色…", "relation_filter": "关系过滤",
        "all_relations": "全部关系", "cluster_filter": "集群过滤", "all_clusters": "全部集群",
        "min_relevance": "最低相关度", "view": "视图", "fit": "适应画布", "reset": "重置布局",
        "main_only": "只看主链路", "conflict_only": "只看冲突相关", "latest_only": "只看本次增量",
        "legend": "图例", "main_path": "主链路", "conflict": "冲突/批评",
        "benchmark": "Benchmark/数据集", "repository": "代码仓库", "latest_increment": "本次新增/更新",
        "coverage": "覆盖与版本", "empty": "点击节点查看论文信息；点击边查看关系与证据。",
        "core_relation": "与核心问题的关系", "identifiers": "标识符", "links": "链接",
        "seed": "种子", "frontier": "最新前沿", "relevance": "相关度", "quality": "质量启发式",
        "claim": "论点", "paper_relation": "论文关系", "evidence_level": "证据级别",
        "confidence": "置信度", "citation_direction": "引用方向", "conflict_type": "冲突类型",
        "evidence_ids": "证据 ID", "unlabeled": "未标注", "none": "无", "unclassified": "未分类",
        "expand": "继续调研此节点", "expand_title": "节点增量调研请求", "expand_focus": "本次调研问题",
        "expand_direction": "扩展方向", "expand_depth": "最大深度", "candidate_budget": "候选预算",
        "analysis_budget": "深读预算", "download_request": "下载调研请求", "copy_request": "复制请求 JSON",
        "static_notice": "此静态页面只生成请求；宿主 Agent 执行检索并把 patch 合并回图谱。",
        "copied": "请求已复制", "downloaded": "请求已下载", "revision": "图谱版本",
        "graph_id": "图谱 ID", "last_expansion": "最近扩展", "added_revision": "加入版本",
        "updated_revision": "更新版本", "publication": "发表信息", "publication_status": "发表状态",
        "publication_venue": "发表场所", "publication_versions": "版本记录", "peer_reviewed": "同行评审",
        "yes": "是", "no": "否", "unknown": "未知", "top_venue": "顶会",
        "venue_tier_basis": "顶会标注依据", "has_preprint": "含预印本版本",
        "paper_guide": "论文内容导读", "reader_audience": "面向本领域相关但未读过论文的读者",
        "background": "背景与前置问题", "problem": "论文要解决什么", "approach": "核心思路与做法",
        "key_findings": "主要发现", "why_it_matters": "为什么重要", "limitations": "局限与适用边界",
        "concepts_to_know": "需要先理解的概念",
        "featured_figure": "论文代表性主图", "figure_reader_note": "读图提示",
        "figure_source": "图像来源", "figure_selection": "选择理由",
        "figure_reconstruction": "分析者示意重绘（非论文原图）",
        "figure_unavailable": "图像资源不可用，仍保留来源与说明。",
        "figure_rights": "许可/使用依据",
        "figure_kinds": {"method_overview":"方法总览", "architecture":"架构图", "pipeline":"流程图", "conceptual_diagram":"概念示意", "qualitative_result":"定性结果", "benchmark_summary":"结果汇总", "other":"其他"},
        "publication_statuses": {"preprint_only":"仅预印本", "under_review":"审稿中", "accepted":"已录用", "in_press":"待刊", "published":"已正式发表", "withdrawn":"已撤稿", "retracted":"已撤回", "unknown":"状态未知"},
        "publication_types": {"preprint":"预印本", "conference_paper":"会议论文", "journal_article":"期刊论文", "workshop_paper":"研讨会论文", "technical_report":"技术报告", "book_chapter":"书籍章节", "thesis":"学位论文", "other":"其他"},
        "version_kinds": {"preprint":"预印本", "conference":"会议版", "journal":"期刊版", "workshop":"研讨会版", "technical_report":"技术报告", "other":"其他版本"},
        "directions": {
            "backward":"向来源", "forward":"向后续", "both":"双向", "related":"相关工作",
            "conflicts":"冲突与批评", "benchmark_use":"Benchmark 使用", "repository":"代码与仓库"
        }
    },
    "en": {
        "nodes": "Nodes", "edges": "Edges", "search_label": "Search papers or concepts",
        "search_placeholder": "Title, author, role…", "relation_filter": "Relationship filter",
        "all_relations": "All relationships", "cluster_filter": "Cluster filter", "all_clusters": "All clusters",
        "min_relevance": "Minimum relevance", "view": "View", "fit": "Fit canvas", "reset": "Reset layout",
        "main_only": "Main lineage only", "conflict_only": "Conflict-related only", "latest_only": "Latest increment only",
        "legend": "Legend", "main_path": "Main lineage", "conflict": "Conflict/criticism",
        "benchmark": "Benchmark/dataset", "repository": "Repository/code", "latest_increment": "Added/updated now",
        "coverage": "Coverage and revision", "empty": "Click a node for paper details; click an edge for relationship evidence.",
        "core_relation": "Relation to the focal question", "identifiers": "Identifiers", "links": "Links",
        "seed": "Seed", "frontier": "Latest frontier", "relevance": "Relevance", "quality": "Quality heuristic",
        "claim": "Claim", "paper_relation": "Paper relationship", "evidence_level": "Evidence level",
        "confidence": "Confidence", "citation_direction": "Citation direction", "conflict_type": "Conflict type",
        "evidence_ids": "Evidence IDs", "unlabeled": "Unlabeled", "none": "None", "unclassified": "Unclassified",
        "expand": "Continue research from this node", "expand_title": "Node-centered expansion request", "expand_focus": "Research focus",
        "expand_direction": "Direction", "expand_depth": "Maximum depth", "candidate_budget": "Candidate budget",
        "analysis_budget": "Deep-reading budget", "download_request": "Download research request", "copy_request": "Copy request JSON",
        "static_notice": "This static page only creates a request; the host agent performs retrieval and merges the patch.",
        "copied": "Request copied", "downloaded": "Request downloaded", "revision": "Graph revision",
        "graph_id": "Graph ID", "last_expansion": "Latest expansion", "added_revision": "Added in revision",
        "updated_revision": "Updated in revision", "publication": "Publication", "publication_status": "Publication status",
        "publication_venue": "Venue", "publication_versions": "Version record", "peer_reviewed": "Peer reviewed",
        "yes": "Yes", "no": "No", "unknown": "Unknown", "top_venue": "Top-tier venue",
        "venue_tier_basis": "Tier basis", "has_preprint": "Preprint version available",
        "paper_guide": "Paper guide", "reader_audience": "For a field-relevant reader who has not read the paper",
        "background": "Background", "problem": "Problem", "approach": "Core idea and approach",
        "key_findings": "Key findings", "why_it_matters": "Why it matters", "limitations": "Limitations and scope",
        "concepts_to_know": "Concepts to know",
        "featured_figure": "Featured paper figure", "figure_reader_note": "How to read it",
        "figure_source": "Figure source", "figure_selection": "Why this figure",
        "figure_reconstruction": "Analyst reconstruction (not an original paper figure)",
        "figure_unavailable": "The image asset is unavailable; attribution and explanation are retained.",
        "figure_rights": "License/usage basis",
        "figure_kinds": {"method_overview":"Method overview", "architecture":"Architecture", "pipeline":"Pipeline", "conceptual_diagram":"Conceptual diagram", "qualitative_result":"Qualitative result", "benchmark_summary":"Result summary", "other":"Other"},
        "publication_statuses": {"preprint_only":"Preprint only", "under_review":"Under review", "accepted":"Accepted", "in_press":"In press", "published":"Published", "withdrawn":"Withdrawn", "retracted":"Retracted", "unknown":"Unknown status"},
        "publication_types": {"preprint":"Preprint", "conference_paper":"Conference paper", "journal_article":"Journal article", "workshop_paper":"Workshop paper", "technical_report":"Technical report", "book_chapter":"Book chapter", "thesis":"Thesis", "other":"Other"},
        "version_kinds": {"preprint":"Preprint", "conference":"Conference version", "journal":"Journal version", "workshop":"Workshop version", "technical_report":"Technical report", "other":"Other version"},
        "directions": {
            "backward":"Backward/origins", "forward":"Forward/descendants", "both":"Both", "related":"Related work",
            "conflicts":"Conflicts and criticism", "benchmark_use":"Benchmark use", "repository":"Code and repository"
        }
    }
}

HTML_TEMPLATE = r'''<!doctype html>
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#0b1020;--panel:#121a2e;--panel2:#17223b;--text:#e8edf7;--muted:#9eabc2;--line:#55627a;--accent:#ffb454;--danger:#ff667a;--blue:#58a6ff;--purple:#bf8cff;--green:#63d39b;--cyan:#64d8e8}
*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);overflow:hidden}
header{height:58px;display:flex;align-items:center;gap:14px;padding:0 18px;border-bottom:1px solid #27324a;background:#0e1528}
header h1{font-size:16px;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:46vw}header .focus{font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.app{height:calc(100vh - 58px);display:grid;grid-template-columns:300px minmax(420px,1fr) 400px}.sidebar,.detail{background:var(--panel);overflow:auto}.sidebar{border-right:1px solid #27324a;padding:14px}.detail{border-left:1px solid #27324a;padding:16px}.canvas{position:relative;overflow:hidden;background:radial-gradient(circle at 50% 45%,#15223c 0,#0b1020 62%)}svg{width:100%;height:100%;display:block;cursor:grab}svg:active{cursor:grabbing}
label{display:block;font-size:12px;color:var(--muted);margin:12px 0 5px}input,select,textarea{width:100%;background:#0e1528;border:1px solid #35415a;color:var(--text);border-radius:8px;padding:9px}textarea{min-height:92px;resize:vertical}button{background:#263553;color:var(--text);border:1px solid #3a4a69;border-radius:8px;padding:8px 10px;cursor:pointer}button:hover{background:#314363}button.primary{background:#3b536f;border-color:#5f7fa0}.row{display:flex;gap:8px}.row>*{flex:1}.stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}.stat{background:var(--panel2);padding:10px;border-radius:9px}.stat b{display:block;font-size:18px}.stat span{font-size:11px;color:var(--muted)}
.legend{font-size:12px;line-height:1.8}.swatch{display:inline-block;width:24px;height:3px;vertical-align:middle;margin-right:7px;background:var(--line)}.swatch.main{height:5px;background:var(--accent)}.swatch.conflict{height:0;border-top:3px dashed var(--danger)}.swatch.bench{background:var(--blue)}.swatch.repo{background:var(--purple)}.swatch.increment{height:0;border-top:3px dotted var(--cyan)}
.node circle{stroke:#d8e1f0;stroke-width:1.2}.node.seed circle{stroke:var(--accent);stroke-width:3}.node.frontier circle{stroke:var(--green);stroke-width:3}.node.incremental circle{stroke:var(--cyan);stroke-width:4;stroke-dasharray:3 2}.node text{fill:var(--text);font-size:11px;pointer-events:none;text-shadow:0 1px 2px #000}.edge{stroke:var(--line);stroke-opacity:.63;fill:none}.edge.main{stroke:var(--accent);stroke-width:4;stroke-opacity:.92}.edge.conflict{stroke:var(--danger);stroke-width:3;stroke-dasharray:8 6;stroke-opacity:.95}.edge.benchmark{stroke:var(--blue);stroke-width:2.5}.edge.repository{stroke:var(--purple);stroke-width:2.5}.edge.incremental{stroke:var(--cyan);stroke-width:3.5;stroke-dasharray:3 5;stroke-opacity:.95}.edge-hit{stroke:transparent;stroke-width:14;fill:none;cursor:pointer}
.card{background:var(--panel2);border:1px solid #2c3953;border-radius:12px;padding:13px;margin:10px 0}.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}h2{font-size:19px;line-height:1.3;margin:6px 0 10px}h3{font-size:14px;margin:18px 0 7px}p{font-size:13px;line-height:1.55;color:#d6deec;white-space:pre-line}.meta{font-size:12px;color:var(--muted);line-height:1.6}.pill{display:inline-block;padding:3px 7px;margin:3px 4px 3px 0;background:#25344f;border-radius:999px;font-size:11px}.pill.danger{background:#5a2834}.pill.main{background:#5a4323}.pill.increment{background:#164b55}.pill.top{background:#654a12;border:1px solid #e5b94f;font-weight:700}.publication-card{border-color:#4a5873}.figure-card{border-color:#536b88;background:#111c31;padding:0;overflow:hidden}.figure-head{padding:13px 13px 8px}.figure-media{position:relative;background:#f7f8fb;border-top:1px solid #33445f;border-bottom:1px solid #33445f;min-height:72px;display:flex;align-items:center;justify-content:center}.figure-media img{display:block;width:100%;height:auto;max-height:430px;object-fit:contain}.figure-body{padding:11px 13px 13px}.figure-caption{font-size:12px;line-height:1.5;color:#dce5f2;margin:0 0 8px}.figure-note{background:#192943;border-left:3px solid #7da9d7;padding:8px 10px;margin:9px 0;font-size:12px;line-height:1.5}.figure-missing{padding:26px 18px;color:#536174;text-align:center;font-size:12px}.figure-attribution{font-size:10.5px;color:var(--muted);line-height:1.5}.reader-guide{border-color:#3c5870;background:#16243b}.reader-guide h3{margin-top:14px}.reader-guide ul{padding-left:19px;margin:6px 0}.reader-guide li{font-size:13px;line-height:1.5;color:#d6deec;margin:5px 0}.concept-row{padding:7px 0;border-top:1px solid #2c3953}.concept-row:first-child{border-top:0}.version-row{padding:5px 0;border-top:1px solid #2c3953}.version-row:first-child{border-top:0}.link{display:block;color:#8fc7ff;text-decoration:none;margin:5px 0;font-size:12px}.empty{color:var(--muted);font-size:13px;margin-top:30px}.warning{color:#ffd28a}.small{font-size:11px;color:var(--muted)}.toast{position:fixed;right:20px;bottom:20px;background:#20364a;border:1px solid #4d718f;padding:10px 14px;border-radius:9px;display:none;z-index:10}
@media(max-width:1050px){.app{grid-template-columns:240px 1fr 340px}}@media(max-width:800px){body{overflow:auto}.app{height:auto;display:block}.sidebar,.detail{border:0}.canvas{height:70vh}}
</style>
</head>
<body>
<header><h1 id="pageTitle"></h1><div class="focus" id="pageFocus"></div></header>
<div class="app">
<aside class="sidebar">
  <div class="stats"><div class="stat"><b id="nodeCount">0</b><span>__NODES__</span></div><div class="stat"><b id="edgeCount">0</b><span>__EDGES__</span></div></div>
  <label>__SEARCH_LABEL__</label><input id="search" placeholder="__SEARCH_PLACEHOLDER__">
  <label>__RELATION_FILTER__</label><select id="edgeType"><option value="">__ALL_RELATIONS__</option></select>
  <label>__CLUSTER_FILTER__</label><select id="cluster"><option value="">__ALL_CLUSTERS__</option></select>
  <label>__MIN_RELEVANCE__ <span id="relValue">0.00</span></label><input id="relevance" type="range" min="0" max="1" step="0.05" value="0">
  <label>__VIEW__</label><div class="row"><button id="fit">__FIT__</button><button id="reset">__RESET__</button></div>
  <label><input id="mainOnly" type="checkbox" style="width:auto"> __MAIN_ONLY__</label>
  <label><input id="conflictOnly" type="checkbox" style="width:auto"> __CONFLICT_ONLY__</label>
  __LATEST_FILTER_ROW__
  <h3>__LEGEND__</h3><div class="legend"><div><span class="swatch main"></span>__MAIN_PATH__</div><div><span class="swatch conflict"></span>__CONFLICT__</div><div><span class="swatch bench"></span>__BENCHMARK__</div><div><span class="swatch repo"></span>__REPOSITORY__</div>__LATEST_LEGEND_ROW__</div>
  <h3>__COVERAGE__</h3><div id="coverage" class="small"></div>
</aside>
<main class="canvas"><svg id="graph" aria-label="Academic research graph"></svg></main>
<aside class="detail"><div id="detail" class="empty">__EMPTY__</div></aside>
</div><div class="toast" id="toast"></div>
<script>
const DATA=__GRAPH_DATA__;
const UI=__UI_DATA__;
const LANG=__LANG_JSON__;
const svg=document.getElementById('graph'),detail=document.getElementById('detail'),ns='http://www.w3.org/2000/svg';
const state={nodes:[],edges:[],scale:1,tx:0,ty:0,drag:null,pan:null,anim:null};
const typeColors={paper:'#5477c7',concept:'#d08770',benchmark:'#3aa6b9',repository:'#9a6ac7',dataset:'#4fa67a'};
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function localized(obj,scalar,mapName){const map=obj?.[mapName];if(LANG==='bilingual'&&map){const z=map['zh-CN'],e=map.en;return [z,e].filter(Boolean).join('\n');}if(map&&map[LANG])return map[LANG];return obj?.[scalar]??''}
function titleOf(n){return localized(n,'title','titles')||n.id}function summaryOf(n){return localized(n,'summary','summaries')}function roleOf(n){return localized(n,'role','roles')}function explanationOf(e){return localized(e,'explanation','explanations')}
function readerPayloads(n){const rs=n.reader_summary||{};if(LANG==='bilingual'){return [['zh-CN',rs['zh-CN']],['en',rs.en]].filter(x=>x[1])}const p=rs[LANG]||rs['zh-CN']||rs.en;return p?[[LANG,p]]:[]}
function bulletList(items){return Array.isArray(items)&&items.length?`<ul>${items.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}
function readerGuide(n){if(n.type!=='paper')return'';const payloads=readerPayloads(n);if(!payloads.length)return `<div class="card reader-guide"><div class="eyebrow">${UI.paper_guide}</div><p>${esc(summaryOf(n))}</p></div>`;return payloads.map(([code,r])=>{const concepts=Array.isArray(r.concepts)&&r.concepts.length?`<h3>${UI.concepts_to_know}</h3>${r.concepts.map(c=>`<div class="concept-row"><b>${esc(c.term)}</b><p>${esc(c.explanation)}</p></div>`).join('')}`:'';const langLabel=LANG==='bilingual'?` · ${esc(code)}`:'';return `<div class="card reader-guide"><div class="eyebrow">${UI.paper_guide}${langLabel}</div><div class="small">${UI.reader_audience}</div><h3>${UI.background}</h3><p>${esc(r.background||'')}</p><h3>${UI.problem}</h3><p>${esc(r.problem||'')}</p>${concepts}<h3>${UI.approach}</h3><p>${esc(r.approach||'')}</p><h3>${UI.key_findings}</h3>${bulletList(r.key_findings)}<h3>${UI.why_it_matters}</h3><p>${esc(r.why_it_matters||'')}</p><h3>${UI.limitations}</h3>${bulletList(r.limitations)}</div>`}).join('')}
function safeHttpUrl(v){const x=String(v||'');return /^https?:\/\//i.test(x)?x:''}
function safeImageSrc(v){const x=String(v||'');return /^data:image\/[a-zA-Z0-9.+-]+;base64,/.test(x)||/^https:\/\//i.test(x)||/^(?:\.\.\/|\.\/|assets\/)/.test(x)?x:''}
function figureCard(n){if(n.type!=='paper'||!n.featured_figure)return'';const f=n.featured_figure||{},src=safeImageSrc(f._resolved_src||f.asset?.data_uri||''),caption=localized(f,'caption','captions'),alt=localized(f,'alt_text','alt_texts')||caption,note=localized(f,'reader_note','reader_notes'),reason=localized(f,'selection_reason','selection_reasons'),source=f.source||{},kind=UI.figure_kinds[f.kind]||f.kind||UI.unlabeled,sourceUrl=safeHttpUrl(source.url),assetLink=sourceUrl?`<a class="link" href="${esc(sourceUrl)}" target="_blank" rel="noopener">${UI.figure_source} ↗</a>`:'',label=f.label?` · ${esc(f.label)}`:'',recon=f.display_kind==='analyst_reconstruction'?`<span class="pill danger">${UI.figure_reconstruction}</span>`:'',rights=[source.license,source.rights_status].filter(Boolean).join(' · '),location=[source.paper_version,source.figure_number,source.page?`p. ${source.page}`:''].filter(Boolean).join(' · '),citation=source.citation||'',image=src?`<div class="figure-media"><img class="featured-image" src="${esc(src)}" alt="${esc(alt)}" loading="lazy"><div class="figure-missing" hidden>${UI.figure_unavailable}</div></div>`:`<div class="figure-media"><div class="figure-missing">${UI.figure_unavailable}</div></div>`,noteHtml=note?`<div class="figure-note"><b>${UI.figure_reader_note}</b><br>${esc(note)}</div>`:'',reasonHtml=reason?`<div class="small"><b>${UI.figure_selection}:</b> ${esc(reason)}</div>`:'';return `<div class="card figure-card"><div class="figure-head"><div class="eyebrow">${UI.featured_figure} · ${esc(kind)}${label}</div>${recon}</div>${image}<div class="figure-body"><div class="figure-caption">${esc(caption)}</div>${noteHtml}${reasonHtml}<div class="figure-attribution">${esc(citation)}${location?`<br>${esc(location)}`:''}${rights?`<br>${UI.figure_rights}: ${esc(rights)}`:''}${f._asset_warning?`<br><span class="warning">${esc(f._asset_warning)}</span>`:''}</div>${assetLink}</div></div>`}
function bindFigureFallback(){detail.querySelectorAll('img.featured-image').forEach(img=>img.addEventListener('error',()=>{img.style.display='none';const fallback=img.parentElement?.querySelector('.figure-missing');if(fallback)fallback.hidden=false},{once:true}))}
function latestRevision(){return Number(DATA.meta?.revision||1)}
function latestIncrementRevision(){const current=latestRevision(),inc=DATA.meta?.latest_increment,hist=DATA.meta?.expansion_history||[];if(inc&&Number(inc.revision)===current&&current>1)return current;const last=hist.length?hist[hist.length-1]:null;return last&&Number(last.revision)===current&&current>1?current:null}
function hasIncrement(){return latestIncrementRevision()!==null}
function changedLatest(x){const r=latestIncrementRevision();return r!==null&&(Number(x.added_in_revision||0)===r||Number(x.updated_in_revision||0)===r)}
function revisionMeta(x){if(!hasIncrement())return'';const parts=[];if(x.added_in_revision)parts.push(`${UI.added_revision}: ${esc(x.added_in_revision)}`);if(x.updated_in_revision)parts.push(`${UI.updated_revision}: ${esc(x.updated_in_revision)}`);return parts.length?`<br>${parts.join(' · ')}`:''}
function publicationInfo(n){const p=n.publication||{},pv=p.primary_venue||{};let status=p.status||n.status||'unknown',type=p.type||'';const venue=pv.short_name||pv.name||n.venue||'';if(!type){if(status==='preprint_only')type='preprint';else if(pv.type==='conference')type='conference_paper';else if(pv.type==='journal')type='journal_article';else if(pv.type==='workshop')type='workshop_paper';else type='other'}const tier=pv.tier||n.venue_tier||(n.is_top_venue?'top':'unknown'),basis=pv.tier_basis||n.venue_tier_basis||'',versions=Array.isArray(p.versions)?p.versions:[];const ids=n.identifiers||{},hasPreprint=status==='preprint_only'||versions.some(v=>v.kind==='preprint')||Boolean(ids.arXiv||ids.arxiv);return{status,type,venue,tier,basis,peerReviewed:p.peer_reviewed,versions,hasPreprint}}
function publicationCard(n){if(n.type!=='paper')return'';const p=publicationInfo(n),statusLabel=UI.publication_statuses[p.status]||p.status,typeLabel=UI.publication_types[p.type]||p.type;let pills=`<span class="pill">${esc(statusLabel)}</span>`;if(p.venue)pills+=`<span class="pill">${esc(typeLabel)} · ${esc(p.venue)}</span>`;else pills+=`<span class="pill">${esc(typeLabel)}</span>`;if(p.tier==='top')pills+=`<span class="pill top" title="${esc(p.basis||UI.unlabeled)}">★ ${UI.top_venue}</span>`;if(p.hasPreprint&&p.status!=='preprint_only')pills+=`<span class="pill">${UI.has_preprint}</span>`;const peer=p.peerReviewed===true?UI.yes:p.peerReviewed===false?UI.no:UI.unknown;const basis=p.tier==='top'?`<br>${UI.venue_tier_basis}: ${esc(p.basis||UI.unlabeled)}`:'';const versions=p.versions.length?`<h3>${UI.publication_versions}</h3>${p.versions.map(v=>{const kind=UI.version_kinds[v.kind]||v.kind||UI.unlabeled,venue=v.venue?` · ${esc(v.venue)}`:'',date=v.date?` · ${esc(v.date)}`:'',primary=v.is_primary?' ★':'';return `<div class="version-row small"><b>${esc(kind)}${primary}</b>${venue}${date}${v.identifier?`<br>${esc(v.identifier)}`:''}</div>`}).join('')}`:'';return `<div class="card publication-card"><div class="eyebrow">${UI.publication}</div><div>${pills}</div><div class="meta">${UI.publication_status}: ${esc(statusLabel)}${p.venue?`<br>${UI.publication_venue}: ${esc(p.venue)}`:''}<br>${UI.peer_reviewed}: ${peer}${basis}</div>${versions}</div>`}
function relationClass(e){const r=(e.relationship||[]).join(' ');if(e.conflict||/critic|contradict|fail/.test(r))return'conflict';if(/benchmark|dataset/.test(r))return'benchmark';if(/repository|implement|code_/.test(r))return'repository';return''}
function initPositions(){const w=svg.clientWidth||900,h=svg.clientHeight||700;DATA.nodes.forEach((n,i)=>{const a=(i/Math.max(DATA.nodes.length,1))*Math.PI*2;n.x=w/2+Math.cos(a)*(120+(i%7)*18);n.y=h/2+Math.sin(a)*(120+(i%5)*22);n.vx=0;n.vy=0})}
function filtered(){const q=document.getElementById('search').value.trim().toLowerCase(),et=document.getElementById('edgeType').value,cl=document.getElementById('cluster').value,min=+document.getElementById('relevance').value,main=document.getElementById('mainOnly').checked,conflict=document.getElementById('conflictOnly').checked,latest=Boolean(document.getElementById('latestOnly')?.checked);
 let nodes=DATA.nodes.filter(n=>(n.relevance??1)>=min&&(!cl||n.cluster===cl)&&(!q||JSON.stringify([n.title,n.titles,n.authors,n.role,n.roles,n.summary,n.summaries,n.reader_summary,n.cluster,n.venue,n.status,n.publication,n.featured_figure]).toLowerCase().includes(q))&&(!latest||changedLatest(n)));
 let ids=new Set(nodes.map(n=>n.id));let edges=DATA.edges.filter(e=>ids.has(e.source)&&ids.has(e.target)&&(!et||(e.relationship||[]).includes(et))&&(!main||e.main_path)&&(!conflict||e.conflict)&&(!latest||changedLatest(e)));
 if(main||conflict||et||latest){ids=new Set(edges.flatMap(e=>[e.source,e.target]).concat(nodes.map(n=>n.id)));nodes=DATA.nodes.filter(n=>ids.has(n.id)&&(!latest||changedLatest(n)||edges.some(e=>e.source===n.id||e.target===n.id)))}return{nodes,edges}}
function populate(){document.getElementById('pageTitle').textContent=localized(DATA.meta,'title','titles')||DATA.meta.title;document.getElementById('pageFocus').textContent=localized(DATA.meta,'focus','focuses')||DATA.meta.focus;
 const rel=[...new Set(DATA.edges.flatMap(e=>e.relationship||[]))].sort(),clusters=[...new Set(DATA.nodes.map(n=>n.cluster).filter(Boolean))].sort(),et=document.getElementById('edgeType'),cl=document.getElementById('cluster');rel.forEach(x=>et.insertAdjacentHTML('beforeend',`<option>${esc(x)}</option>`));clusters.forEach(x=>cl.insertAdjacentHTML('beforeend',`<option>${esc(x)}</option>`));
 const m=DATA.meta||{},hist=m.expansion_history||[];const rows=[`${UI.graph_id}: <b>${esc(m.graph_id||UI.none)}</b>`,`${UI.revision}: <b>${esc(m.revision||1)}</b>`,...Object.entries(m.coverage||{}).map(([k,v])=>`${esc(k)}: <b>${esc(v)}</b>`)];if(hist.length)rows.push(`${UI.last_expansion}: <b>${esc(hist[hist.length-1].id||'')}</b>`);document.getElementById('coverage').innerHTML=rows.join('<br>')+(m.warnings?.length?'<br><br><span class="warning">'+m.warnings.map(esc).join('<br>')+'</span>':'')}
function render(){const f=filtered();state.nodes=f.nodes;state.edges=f.edges;document.getElementById('nodeCount').textContent=f.nodes.length;document.getElementById('edgeCount').textContent=f.edges.length;svg.innerHTML='';const defs=document.createElementNS(ns,'defs');defs.innerHTML='<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#7d8aa3"/></marker>';svg.appendChild(defs);const viewport=document.createElementNS(ns,'g');viewport.id='viewport';svg.appendChild(viewport);
 state.edges.forEach(e=>{const g=document.createElementNS(ns,'g'),p=document.createElementNS(ns,'path'),hit=document.createElementNS(ns,'path');p.setAttribute('class',`edge ${e.main_path?'main ':''}${relationClass(e)} ${changedLatest(e)?'incremental':''}`);hit.setAttribute('class','edge-hit');hit.addEventListener('click',ev=>{ev.stopPropagation();showEdge(e)});g.append(p,hit);viewport.appendChild(g)});
 state.nodes.forEach(n=>{const g=document.createElementNS(ns,'g');g.setAttribute('class',`node ${n.is_seed?'seed ':''}${n.latest_frontier?'frontier ':''}${changedLatest(n)?'incremental':''}`);const c=document.createElementNS(ns,'circle'),t=document.createElementNS(ns,'text');c.setAttribute('r',n.is_seed?13:10);c.setAttribute('fill',typeColors[n.type]||'#66758f');t.setAttribute('x','14');t.setAttribute('y','4');const label=titleOf(n);t.textContent=label.length>40?label.slice(0,37)+'…':label;g.append(c,t);g.addEventListener('click',ev=>{ev.stopPropagation();showNode(n)});g.addEventListener('pointerdown',ev=>{ev.stopPropagation();state.drag={n,px:ev.clientX,py:ev.clientY};g.setPointerCapture(ev.pointerId)});g.addEventListener('pointermove',ev=>{if(state.drag?.n===n){n.x+=(ev.clientX-state.drag.px)/state.scale;n.y+=(ev.clientY-state.drag.py)/state.scale;state.drag.px=ev.clientX;state.drag.py=ev.clientY;updatePositions()}});g.addEventListener('pointerup',()=>state.drag=null);viewport.appendChild(g)});applyTransform();updatePositions();startSimulation()}
function updatePositions(){const byId=Object.fromEntries(DATA.nodes.map(n=>[n.id,n]));[...svg.querySelectorAll('.edge')].forEach((p,i)=>{const e=state.edges[i],a=byId[e.source],b=byId[e.target];if(!a||!b)return;const d=`M ${a.x} ${a.y} L ${b.x} ${b.y}`;p.setAttribute('d',d);p.nextSibling?.setAttribute('d',d)});[...svg.querySelectorAll('.node')].forEach((g,i)=>{const n=state.nodes[i];g.setAttribute('transform',`translate(${n.x},${n.y})`)})}
function startSimulation(){cancelAnimationFrame(state.anim);let ticks=0;const byId=Object.fromEntries(DATA.nodes.map(n=>[n.id,n]));function step(){const nodes=state.nodes,edges=state.edges;for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){let a=nodes[i],b=nodes[j],dx=b.x-a.x,dy=b.y-a.y,d2=dx*dx+dy*dy+.1,d=Math.sqrt(d2),f=Math.min(1.8,1200/d2);a.vx-=dx/d*f;a.vy-=dy/d*f;b.vx+=dx/d*f;b.vy+=dy/d*f}edges.forEach(e=>{let a=byId[e.source],b=byId[e.target];if(!a||!b)return;let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)||1,target=e.main_path?115:145,f=(d-target)*.003;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f});nodes.forEach(n=>{n.vx+=(svg.clientWidth/2-n.x)*.0004;n.vy+=(svg.clientHeight/2-n.y)*.0004;n.vx*=.86;n.vy*=.86;n.x+=n.vx;n.y+=n.vy});updatePositions();if(++ticks<420)state.anim=requestAnimationFrame(step)}step()}
function applyTransform(){const vp=document.getElementById('viewport');if(vp)vp.setAttribute('transform',`translate(${state.tx},${state.ty}) scale(${state.scale})`)}
function showNode(n){const links=Object.entries(n.urls||{}).map(([k,v])=>`<a class="link" href="${esc(v)}" target="_blank" rel="noopener">${esc(k)} ↗</a>`).join(''),ids=Object.entries(n.identifiers||{}).map(([k,v])=>`<span class="pill">${esc(k)}: ${esc(v)}</span>`).join(''),claims=(n.claims||[]).map(c=>`<div class="card"><div class="eyebrow">${UI.claim}</div><p>${esc(localized(c,'text','texts')||c.claim||JSON.stringify(c))}</p></div>`).join('');
 detail.innerHTML=`<div class="eyebrow">${esc(n.type)} · ${esc(roleOf(n))}</div><h2>${esc(titleOf(n))}</h2>${titleOf(n)!==n.title?`<div class="meta">${esc(n.title)}</div>`:''}<div class="meta">${esc((n.authors||[]).join(', '))}<br>${esc(n.year??'')}</div><div>${n.is_seed?`<span class="pill main">${UI.seed}</span>`:''}${n.latest_frontier?`<span class="pill">${UI.frontier}</span>`:''}${changedLatest(n)?`<span class="pill increment">${UI.latest_increment}</span>`:''}${n.cluster?`<span class="pill">${esc(n.cluster)}</span>`:''}</div>${figureCard(n)}${publicationCard(n)}${readerGuide(n)}<h3>${UI.core_relation}</h3><p>${esc(summaryOf(n))}</p><div class="meta">${UI.relevance} ${(n.relevance??0).toFixed(2)} · ${UI.quality} ${(n.quality??0).toFixed(2)}${revisionMeta(n)}</div><h3>${UI.identifiers}</h3><div>${ids||`<span class="small">${UI.none}</span>`}</div><h3>${UI.links}</h3>${links||`<div class="small">${UI.none}</div>`}${claims}<button class="primary" id="expandButton">${UI.expand}</button><div id="expansionBox"></div>`;bindFigureFallback();document.getElementById('expandButton').onclick=()=>showExpansionForm(n)}
function showExpansionForm(n){const box=document.getElementById('expansionBox');const dirs=Object.entries(UI.directions).map(([v,l])=>`<option value="${v}" ${v==='both'?'selected':''}>${esc(l)}</option>`).join('');const defaultFocus=LANG==='en'?`Continue research from "${titleOf(n)}", focusing on its origins, descendants, conflicts, and latest developments.`:`从“${titleOf(n)}”继续调研，重点梳理其来源、后续工作、冲突与最新进展。`;box.innerHTML=`<div class="card"><div class="eyebrow">${UI.expand_title}</div><label>${UI.expand_focus}</label><textarea id="expFocus">${esc(defaultFocus)}</textarea><label>${UI.expand_direction}</label><select id="expDirection">${dirs}</select><div class="row"><div><label>${UI.expand_depth}</label><input id="expDepth" type="number" min="1" max="8" value="2"></div><div><label>${UI.candidate_budget}</label><input id="expCandidates" type="number" min="10" value="120"></div></div><label>${UI.analysis_budget}</label><input id="expAnalysis" type="number" min="5" value="35"><p class="small">${UI.static_notice}</p><div class="row"><button id="downloadExp">${UI.download_request}</button><button id="copyExp">${UI.copy_request}</button></div></div>`;document.getElementById('downloadExp').onclick=()=>exportRequest(n,false);document.getElementById('copyExp').onclick=()=>exportRequest(n,true)}
function makeRequest(n){return{operation:'expand',base_graph:'graph.json',base_graph_id:DATA.meta?.graph_id||'',base_revision:Number(DATA.meta?.revision||1),start_node_id:n.id,start_node_title:n.title,focus:document.getElementById('expFocus').value,direction:document.getElementById('expDirection').value,mode:'standard',max_depth:Number(document.getElementById('expDepth').value||2),candidate_budget:Number(document.getElementById('expCandidates').value||120),analysis_budget:Number(document.getElementById('expAnalysis').value||35),output_language:LANG,summary_policy:DATA.meta?.summary_policy||{audience:'field_familiar_unread',exposition_depth:'explanatory',explain_background:true,define_paper_specific_terms:true,expand_acronyms_on_first_use:true,name_comparison_baselines:true,require_limitations_and_scope:true},figure_policy:DATA.meta?.figure_policy||{enabled:true,selection_mode:'selective',max_per_paper:1,require_source_attribution:true,require_alt_text:true,embed_local_assets:true,allow_remote_images:false,max_embedded_bytes:2500000},allow_main_path_revision:true,created_at:new Date().toISOString()}}
async function exportRequest(n,copyOnly){const req=makeRequest(n),text=JSON.stringify(req,null,2);if(copyOnly){try{await navigator.clipboard.writeText(text);toast(UI.copied)}catch{downloadText(text,`expansion_request.${safe(n.id)}.json`);toast(UI.downloaded)}}else{downloadText(text,`expansion_request.${safe(n.id)}.json`);toast(UI.downloaded)}}function safe(s){return String(s).replace(/[^a-zA-Z0-9._-]+/g,'-')}function downloadText(text,name){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type:'application/json'}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(()=>t.style.display='none',1800)}
function showEdge(e){const a=DATA.nodes.find(n=>n.id===e.source),b=DATA.nodes.find(n=>n.id===e.target);detail.innerHTML=`<div class="eyebrow">${UI.paper_relation}</div><h2>${esc(a?titleOf(a):e.source)} → ${esc(b?titleOf(b):e.target)}</h2><div>${(e.relationship||[]).map(r=>`<span class="pill ${e.conflict?'danger':''}">${esc(r)}</span>`).join('')}${changedLatest(e)?`<span class="pill increment">${UI.latest_increment}</span>`:''}</div><p>${esc(explanationOf(e))}</p><div class="meta">${UI.evidence_level}: ${esc(e.evidence_level||UI.unlabeled)}<br>${UI.confidence}: ${Number(e.confidence||0).toFixed(2)}<br>${UI.citation_direction}: ${esc(e.citation_direction||UI.unlabeled)}<br>${e.main_path?UI.main_path+'<br>':''}${e.conflict?`${UI.conflict_type}: ${esc(e.conflict_type||UI.unclassified)}<br>`:''}${UI.evidence_ids}: ${esc((e.evidence_ids||[]).join(', ')||UI.none)}${revisionMeta(e)}</div>`}
function fit(){const n=state.nodes;if(!n.length)return;const xs=n.map(x=>x.x),ys=n.map(x=>x.y),minx=Math.min(...xs)-80,maxx=Math.max(...xs)+180,miny=Math.min(...ys)-80,maxy=Math.max(...ys)+80;state.scale=Math.min(svg.clientWidth/(maxx-minx),svg.clientHeight/(maxy-miny),1.5);state.tx=(svg.clientWidth-(minx+maxx)*state.scale)/2;state.ty=(svg.clientHeight-(miny+maxy)*state.scale)/2;applyTransform()}
svg.addEventListener('wheel',e=>{e.preventDefault();state.scale=Math.max(.2,Math.min(4,state.scale*(e.deltaY<0?1.12:.89)));applyTransform()},{passive:false});svg.addEventListener('pointerdown',e=>{if(e.target===svg){state.pan={x:e.clientX,y:e.clientY,tx:state.tx,ty:state.ty};svg.setPointerCapture(e.pointerId)}});svg.addEventListener('pointermove',e=>{if(state.pan){state.tx=state.pan.tx+e.clientX-state.pan.x;state.ty=state.pan.ty+e.clientY-state.pan.y;applyTransform()}});svg.addEventListener('pointerup',()=>state.pan=null);
['search','edgeType','cluster','relevance','mainOnly','conflictOnly','latestOnly'].forEach(id=>document.getElementById(id)?.addEventListener('input',()=>{document.getElementById('relValue').textContent=(+document.getElementById('relevance').value).toFixed(2);render()}));document.getElementById('fit').onclick=fit;document.getElementById('reset').onclick=()=>{state.scale=1;state.tx=state.ty=0;initPositions();render()};window.addEventListener('resize',fit);populate();initPositions();render();setTimeout(fit,450);
</script></body></html>'''


def _safe_local_asset(base_dir: Path, value: str) -> Path | None:
    candidate = Path(value)
    if candidate.is_absolute():
        return None
    resolved = (base_dir / candidate).resolve()
    try:
        resolved.relative_to(base_dir.resolve())
    except ValueError:
        return None
    return resolved


def prepare_figure_assets(data: dict[str, Any], graph_path: Path, output_path: Path) -> dict[str, Any]:
    result = copy.deepcopy(data)
    policy = result.get("meta", {}).get("figure_policy") or {}
    if policy.get("enabled", True) is False:
        return result
    embed_local = policy.get("embed_local_assets", True)
    allow_remote = policy.get("allow_remote_images", False)
    max_bytes = int(policy.get("max_embedded_bytes", 2_500_000) or 2_500_000)
    base_dir = graph_path.parent.resolve()
    for node in result.get("nodes", []):
        figure = node.get("featured_figure")
        if not isinstance(figure, dict):
            continue
        asset = figure.get("asset")
        if not isinstance(asset, dict):
            figure["_asset_warning"] = "Figure asset metadata is missing."
            continue
        data_uri = asset.get("data_uri")
        if isinstance(data_uri, str) and data_uri.startswith("data:image/"):
            figure["_resolved_src"] = data_uri
            continue
        local_value = asset.get("path")
        if isinstance(local_value, str) and local_value:
            local_path = _safe_local_asset(base_dir, local_value)
            if local_path and local_path.is_file():
                size = local_path.stat().st_size
                if embed_local and size <= max_bytes:
                    mime = asset.get("mime_type") or mimetypes.guess_type(local_path.name)[0] or "application/octet-stream"
                    if str(mime).startswith("image/"):
                        payload = base64.b64encode(local_path.read_bytes()).decode("ascii")
                        figure["_resolved_src"] = f"data:{mime};base64,{payload}"
                    else:
                        figure["_asset_warning"] = "Local asset is not a supported image MIME type."
                elif embed_local:
                    figure["_asset_warning"] = f"Local figure exceeds embedding limit ({size} > {max_bytes} bytes)."
                else:
                    figure["_resolved_src"] = Path(os.path.relpath(local_path, output_path.parent.resolve())).as_posix()
            else:
                figure["_asset_warning"] = "Local figure asset was not found or used an unsafe path."
        if not figure.get("_resolved_src"):
            remote = asset.get("url")
            if allow_remote and isinstance(remote, str) and remote.startswith("https://"):
                figure["_resolved_src"] = remote
            elif isinstance(remote, str) and remote:
                figure.setdefault("_asset_warning", "Remote figure loading is disabled by policy.")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("index.html"))
    args = parser.parse_args()

    data = json.loads(args.graph.read_text(encoding="utf-8"))
    data = prepare_figure_assets(data, args.graph, args.output)
    lang = data.get("meta", {}).get("output_language", "zh-CN")
    ui_lang = "en" if lang == "en" else "zh-CN"
    ui = LABELS[ui_lang]
    title = data.get("meta", {}).get("title", "Academic Research Graph")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    ui_payload = json.dumps(ui, ensure_ascii=False).replace("</", "<\\/")
    meta = data.get("meta", {})
    current_revision = int(meta.get("revision", 1) or 1)
    latest_increment = meta.get("latest_increment")
    history = meta.get("expansion_history") or []
    last_history_revision = history[-1].get("revision") if history and isinstance(history[-1], dict) else None
    has_increment = current_revision > 1 and (
        (isinstance(latest_increment, dict) and latest_increment.get("revision") == current_revision)
        or last_history_revision == current_revision
    )
    replacements = {
        "__LANG__": "zh-CN" if lang != "en" else "en",
        "__TITLE__": html.escape(str(title)),
        "__GRAPH_DATA__": payload,
        "__UI_DATA__": ui_payload,
        "__LANG_JSON__": json.dumps(lang),
        "__NODES__": ui["nodes"], "__EDGES__": ui["edges"], "__SEARCH_LABEL__": ui["search_label"],
        "__SEARCH_PLACEHOLDER__": ui["search_placeholder"], "__RELATION_FILTER__": ui["relation_filter"],
        "__ALL_RELATIONS__": ui["all_relations"], "__CLUSTER_FILTER__": ui["cluster_filter"],
        "__ALL_CLUSTERS__": ui["all_clusters"], "__MIN_RELEVANCE__": ui["min_relevance"],
        "__VIEW__": ui["view"], "__FIT__": ui["fit"], "__RESET__": ui["reset"],
        "__MAIN_ONLY__": ui["main_only"], "__CONFLICT_ONLY__": ui["conflict_only"],
        "__LEGEND__": ui["legend"],
        "__MAIN_PATH__": ui["main_path"], "__CONFLICT__": ui["conflict"],
        "__BENCHMARK__": ui["benchmark"], "__REPOSITORY__": ui["repository"],
        "__LATEST_INCREMENT__": ui["latest_increment"], "__COVERAGE__": ui["coverage"],
        "__LATEST_FILTER_ROW__": (f'<label><input id="latestOnly" type="checkbox" style="width:auto"> {ui["latest_only"]}</label>' if has_increment else ""),
        "__LATEST_LEGEND_ROW__": (f'<div><span class="swatch increment"></span>{ui["latest_increment"]}</div>' if has_increment else ""),
        "__EMPTY__": ui["empty"],
    }
    output = HTML_TEMPLATE
    for key, value in replacements.items():
        output = output.replace(key, str(value))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
