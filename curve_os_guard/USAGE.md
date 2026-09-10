# Curve OS Guard｜交付版使用說明

## 交付內容與需求

本交付版可完全離線執行，僅需 **Python 3.10 以上**，不需 Docker、資料庫、網路連線或第三方 Python 套件。系統為製程判讀與追溯助手，並非 PLC／DCS 的閉迴路控制器。

```text
curve_os_guard/
├── config/                  # 配方門檻；預載設定為未簽核示範
├── data/incoming/           # 待評估 CSV 與合成示範曲線
├── data/history/            # 僅放已審核的客戶歷史索引
├── data/runtime/            # 執行時報告與追加式稽核紀錄
├── docs/                    # 導入、部署與能力邊界文件
├── curve_os_core.py         # 資料品質、製程、近鄰與規則核心
├── curve_os_cli.py          # 命令列入口
├── app.py                   # 本機儀表板
├── run_curve_os.ps1         # Windows 啟動器
└── run_curve_os.sh          # Linux / macOS 啟動器
```

## 啟動示範

Windows PowerShell：

```powershell
cd curve_os_guard
.\run_curve_os.ps1
```

Linux / macOS：

```bash
cd curve_os_guard
chmod +x run_curve_os.sh
./run_curve_os.sh
```

啟動後開啟 `http://127.0.0.1:8765`。服務只綁定本機 `127.0.0.1`，不會向區網公開。按 `Ctrl+C` 即可停止。

示範曲線為合成資料。其結果只用來確認資料流程、規則與 UI 可運作，不代表任何客戶製程或成品品質。

## 評估客戶單卷

先將 UTF-8 CSV 放到 `data/incoming/`。必填欄位為 `timestamp,temp_c`；`setpoint_c` 為選填：

```csv
timestamp,temp_c,setpoint_c
2026-08-25T00:00:00+08:00,680.2,700
2026-08-25T00:01:00+08:00,686.1,700
```

Windows：

```powershell
python curve_os_cli.py --input data/incoming/CUSTOMER-COIL.csv --coil-id CUSTOMER-COIL-001
```

Linux / macOS：

```bash
python3 curve_os_cli.py --input data/incoming/CUSTOMER-COIL.csv --coil-id CUSTOMER-COIL-001
```

報告將寫入 `data/runtime/latest_report.json`，每次評估的摘要會追加到 `data/runtime/audit_log.jsonl`。

## 使用前必讀

1. `config/recipe_catalog.json` 預設為 `UNAPPROVED_DEMO`，不得直接用於生產判定。
2. 未匯入足夠的已標註客戶歷史卷前，`NOT_CALIBRATED` 是正確且預期的結果；系統不會捏造 failure probability。
3. `data/history/coil_records.json` 不會由單卷評估自動寫入。僅能由受控資料治理流程登錄已核實的歷史資料。
4. v2.0 的製程分段仍是 PoC 的固定三段邏輯，客戶 Shadow Mode 前須改為 recipe event、L2 狀態或經簽核的 zone 分段。
5. `setpoint_c` 目前可以讀取，但 v2.0 尚未逐點納入製程判讀；均熱偏差使用配方目標值。

詳見：

- `docs/CUSTOMER_ONBOARDING.md`：資料契約、角色分工與驗收清單
- `docs/COMMERCIAL_DEPLOYMENT.md`：PoC 至 Shadow Mode 的落地藍圖
- `docs/DOCUMENTATION_AUDIT.md`：已實作能力與待補門檻
