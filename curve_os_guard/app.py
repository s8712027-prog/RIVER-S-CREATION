"""Local browser dashboard; standard-library only and never exposed by default."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from curve_os_cli import DEMO_INPUT, RUNTIME, run_evaluation


def latest_report() -> dict:
    path = RUNTIME / "latest_report.json"
    if not path.exists():
        return run_evaluation(DEMO_INPUT, "DEMO-B20260824-001")
    return json.loads(path.read_text(encoding="utf-8"))


PAGE = r'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Curve OS Guard</title><style>
:root{--ink:#eaf1f7;--muted:#92a1b1;--panel:#122233;--line:#284056;--accent:#58d6a2;--warn:#ffba5c;--bad:#ff7070}*{box-sizing:border-box}body{margin:0;background:#091522;color:var(--ink);font-family:Inter,"Microsoft JhengHei",sans-serif}header{padding:28px 6%;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;align-items:center}.tag{color:#091522;background:var(--warn);font-size:12px;font-weight:800;padding:6px 10px;border-radius:20px}h1{margin:0;font-size:25px}header p{margin:6px 0 0;color:var(--muted)}main{max-width:1220px;margin:0 auto;padding:25px 20px}.notice{background:#263044;border-left:4px solid var(--warn);padding:13px 16px;border-radius:5px;color:#f9d29a}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0}.card,.block{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.label{font-size:12px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}.score{font-size:36px;font-weight:750;margin:6px 0}.ok{color:var(--accent)}.attention{color:var(--warn)}.na{color:var(--muted)}.wide{grid-column:span 2}section{margin-top:16px}h2{font-size:16px;margin:0 0 12px}.rows{display:grid;gap:9px}.row{display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:9px;font-size:14px}.row span:last-child{font-weight:650}table{width:100%;border-collapse:collapse;font-size:14px}td,th{text-align:left;padding:9px 6px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-weight:500}.finding{border-left:3px solid var(--warn);padding:11px 13px;margin:8px 0;background:#182b3d}.muted{color:var(--muted)}button{border:0;border-radius:6px;background:var(--accent);color:#092017;font-weight:750;padding:10px 14px;cursor:pointer}svg{width:100%;height:230px;background:#0d1b29;border-radius:7px}@media(max-width:800px){.grid{grid-template-columns:repeat(2,1fr)}.wide{grid-column:span 2}}@media(max-width:500px){.grid{grid-template-columns:1fr}.wide{grid-column:span 1}}
</style></head><body><header><div><h1>Curve OS Guard</h1><p>CAL 爐溫曲線的離線品質、製程與案例判讀</p></div><span class="tag">DEMO · 非客戶生產結果</span></header><main><div class="notice">此頁僅使用明確標示的合成曲線。接入客戶資料後，才能建立經校準的品質風險模型；在此之前，系統不會輸出 failure probability。</div><div class="grid" id="scores"></div><section class="block"><h2>曲線概覽</h2><svg id="chart" viewBox="0 0 900 230" preserveAspectRatio="none"></svg></section><div class="grid"><section class="block wide"><h2>製程特徵</h2><div class="rows" id="features"></div></section><section class="block wide"><h2>Guard 發現與建議</h2><div id="findings"></div></section></div><section class="block"><h2>相似已驗證歷史卷</h2><p class="muted" id="neighbor-note"></p><table><thead><tr><th>Coil</th><th>相似度</th><th>最終結果</th><th>記錄時間</th></tr></thead><tbody id="neighbors"></tbody></table></section><p class="muted" id="meta"></p><button onclick="refresh()">重新執行示範評估</button></main><script>
const labels={heating_rate_c_per_min:'升溫速率 (°C/min)',soaking_mean_error_c:'均熱均值偏差 (°C)',soaking_stability_c:'均熱波動 (°C)',soaking_duration_min:'均熱時間 (min)',cooling_rate_c_per_min:'冷卻速率 (°C/min)',residual_energy_c:'殘差能量 (°C)'};
const score=(title,value,status,note)=>`<div class="card"><div class="label">${title}</div><div class="score ${status}">${value}</div><div class="muted">${note}</div></div>`;
function draw(curve){let min=Math.min(...curve.map(x=>x.temp_c))-20,max=Math.max(...curve.map(x=>x.temp_c))+20;let pts=curve.map((x,i)=>`${i/(curve.length-1)*900},${220-(x.temp_c-min)/(max-min)*200}`).join(' ');document.querySelector('#chart').innerHTML=`<line x1="0" y1="220" x2="900" y2="220" stroke="#38516a"/><polyline points="${pts}" fill="none" stroke="#58d6a2" stroke-width="2"/><text x="8" y="20" fill="#92a1b1" font-size="12">${max.toFixed(0)}°C</text><text x="8" y="216" fill="#92a1b1" font-size="12">${min.toFixed(0)}°C</text>`}
function render(r){let pq=r.process_quality;document.querySelector('#scores').innerHTML=score('資料品質',r.data_quality.score,r.data_quality.pass?'ok':'attention',r.data_quality.pass?'可進行製程判讀':'拒絕後續推論')+score('製程合規',pq?pq.score:'—',pq?(pq.pass?'ok':'attention'):'na',pq?(pq.pass?'符合已設定規格':'需要工程確認'):'未評估')+score('風險推論',r.risk.status==='ESTIMATED'?r.risk.risk_score:'未校準',r.risk.status==='ESTIMATED'?'attention':'na',r.risk.message)+score('系統狀態',r.status,r.status==='PROCESS_PASS'?'ok':'attention',`Coil ${r.coil_id}`);if(r.curve)draw(r.curve);document.querySelector('#features').innerHTML=Object.entries(r.features||{}).map(([k,v])=>`<div class="row"><span>${labels[k]||k}</span><span>${v}</span></div>`).join('')||'<p class="muted">資料未通過 Gate。</p>';document.querySelector('#findings').innerHTML=r.findings.map(x=>`<div class="finding"><b>${x.severity}</b> · ${x.evidence}<br><span class="muted">${x.suggestion}</span></div>`).join('');document.querySelector('#neighbor-note').textContent=r.neighbors.length?'僅顯示排除自身、非示範且資料品質通過的資料。':'尚未接入可用的客戶歷史卷；示範卷不參與相似案例與風險推論。';document.querySelector('#neighbors').innerHTML=r.neighbors.map(n=>`<tr><td>${n.coil_id}</td><td>${n.similarity}</td><td>${n.outcome||'未標註'}</td><td>${n.recorded_at||'—'}</td></tr>`).join('')||'<tr><td colspan="4" class="muted">尚無可用客戶歷史案例。</td></tr>';document.querySelector('#meta').textContent=`報告版本 ${r.report_version} · 評估時間 ${r.evaluated_at} · 資料雜湊 ${r.source_sha256.slice(0,16)}…`}
async function refresh(){let r=await fetch('/api/evaluate',{method:'POST'});render(await r.json())}fetch('/api/report').then(x=>x.json()).then(render);
</script></body></html>'''


class Handler(BaseHTTPRequestHandler):
    def response(self, data: bytes, content_type: str) -> None:
        self.send_response(200); self.send_header("Content-Type", content_type); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self) -> None:
        if self.path == "/api/report": self.response(json.dumps(latest_report(), ensure_ascii=False).encode(), "application/json; charset=utf-8")
        elif self.path == "/": self.response(PAGE.encode(), "text/html; charset=utf-8")
        else: self.send_error(404)
    def do_POST(self) -> None:
        if self.path == "/api/evaluate": self.response(json.dumps(run_evaluation(DEMO_INPUT, "DEMO-B20260824-001"), ensure_ascii=False).encode(), "application/json; charset=utf-8")
        else: self.send_error(404)
    def log_message(self, format: str, *args: object) -> None: pass


if __name__ == "__main__":
    print("Curve OS Guard dashboard: http://127.0.0.1:8765")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
