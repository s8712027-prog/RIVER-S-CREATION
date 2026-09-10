# Curve OS Guard｜客戶導入文件

適用對象：製程、品質、資訊、設備單位  
對應版本：Guard 商用原型 `guard-v2.0`  
產品定位：製程判讀與追溯助手；**非閉迴路控制器**。

> 預載曲線與配方均為合成／未簽核示範。未取得足夠「高相似且已標註」的客戶歷史卷前，系統會輸出 `NOT_CALIBRATED`，不會輸出經校準的失敗機率。

## 1. 目錄與資料保存原則

```text
curve_os_guard/
├── config/recipe_catalog.json      # 配方門檻；必須帶版本與簽核狀態
├── data/incoming/                  # 待評估曲線 CSV
├── data/history/coil_records.json  # 已審核、可檢索的歷史索引
├── data/runtime/                   # latest_report.json 與 audit_log.jsonl
├── curve_os_core.py                # 評估核心
├── curve_os_cli.py                 # 命令列入口
├── app.py                          # 僅綁定 127.0.0.1 的本機 HMI
├── README.md
└── COMMERCIAL_DEPLOYMENT.md
```

- 示範資料與客戶正式資料必須分區；`synthetic=true` 的資料不得參與風險推論。
- CSV 輸入應另存不可變副本；量產時改以 Parquet 或受控物件儲存保存原始曲線。
- `recipe_catalog.json` 每次變更需更新 `config_version`，並登錄簽核紀錄與生效日。`UNAPPROVED_DEMO` 的設定不得用於生產判定。
- 評估產出的 `latest_report.json` **不會自動寫入** `coil_records.json`。歷史索引必須經資料治理流程驗證、補上最終品質標籤後才可登錄。

## 2. 配方設定與簽核

設定檔是單一 recipe family 的最小可簽核接口；實際數值須來自現行工藝卡或已核准的例外範圍。下列欄位是必要治理資訊：

```json
{
  "config_version": "1.0",
  "approval_status": "APPROVED",
  "approval_record": "QMS-CHANGE-0001",
  "effective_from": "2026-09-01T00:00:00+08:00",
  "recipe_family": "CR980_CAL_ZONE1",
  "soaking_setpoint_c": 750,
  "data_quality_gate": 0.75,
  "process_quality_gate": 0.80,
  "acceptance_limits": {
    "soaking_stability_c": {"min": null, "max": 12.0, "tolerance": 3.0}
  }
}
```

簽核前請確認：

1. `recipe_family` 與 MES／配方系統命名一致。
2. 所有 `acceptance_limits`、權重與 Gate 均有製程與品質共同確認的來源。
3. 門檻改動不可以「讓分數通過」為目的；必須有回測、工藝或品質依據。
4. 現行 v2.0 以 `soaking_setpoint_c` 計算均熱偏差。若要依每筆 CSV 的 `setpoint_c` 計算，須在 Shadow Mode 前完成映射與測試。

## 3. 客戶資料接入檢查清單

### A. 第一階段：可評估曲線

| 項目 | 最低要求 | 導入備註 |
|---|---|---|
| 檔案格式 | UTF-8 CSV | 欄位名稱須完全一致 |
| 必要欄位 | `timestamp`, `temp_c` | 一卷至少 24 點 |
| 選填欄位 | `setpoint_c` | v2.0 可讀取，尚未逐點參與判讀 |
| 時間 | 含時區，或書面約定 UTC／廠區時間 | 禁止混用時區 |
| 卷號 | 來源系統不可變 `coil_id` | CLI 參數傳入，勿以檔名取代 |
| 製程 context | 鋼種、厚度、配方版本、zone／感測器 ID | Shadow Mode 前必須可對應 recipe family |

最小 CSV 範例：

```csv
timestamp,temp_c,setpoint_c
2026-08-25T00:00:00+08:00,680.2,700
2026-08-25T00:01:00+08:00,686.1,700
```

### B. 第二階段：風險校準

| 項目 | 要求 |
|---|---|
| 最終品質標籤 | 明確對應 `PASS`／`DEFECT` 或受管控的不良代碼 |
| 標籤優先序 | 建議：檢驗結果 > 客訴 > 報廢／降級；由品質單位書面定義 |
| 歷史案例 | 同 recipe family、資料品質通過且具可追溯標籤 |
| 驗證方法 | 使用時間正確的 train/test 切分，禁止未來資料洩漏 |

v2.0 的風險推論最少需要 5 筆相似度 ≥ 0.85 的已標註近鄰；在此之前固定顯示 `NOT_CALIBRATED`。這個門檻是原型保護條件，不代表客戶已完成統計驗證。

### C. 歷史索引最小契約

`data/history/coil_records.json` 應由受控匯入程序寫入；每筆至少需要：

```json
{
  "coil_id": "CUSTOMER-COIL-001",
  "recipe_family": "CR980_CAL_ZONE1",
  "synthetic": false,
  "recorded_at": "2026-08-25T08:00:00+08:00",
  "data_quality": {"pass": true},
  "fingerprint": [0.01, -0.02],
  "outcome": "PASS"
}
```

實際 `fingerprint` 長度必須與當前 encoder 版本一致。任何 encoder、特徵尺度或分段方式變更，都必須重建索引，且不得混用不同版本的向量。

## 4. 操作與責任

```powershell
# 評估單卷（本機離線）
python curve_os_cli.py --input data/incoming/CUSTOMER-COIL.csv --coil-id CUSTOMER-COIL-001

# 一鍵啟動示範與本機頁面
.\run_curve_os.ps1
```

儀表板預設為 `http://127.0.0.1:8765`，不對外網或區網開放。輸出報告在 `data/runtime/latest_report.json`；稽核追蹤採追加式 `data/runtime/audit_log.jsonl`。

| 工作 | 建議責任單位 |
|---|---|
| 欄位映射與資料契約 | 資訊 + 製程 |
| 配方門檻簽核 | 製程 + 品質 |
| 品質標籤定義與回填 | 品質 |
| 告警覆核與處置 | 製程／設備（依 finding 類型） |
| 稽核、帳號與 OT 資安 | 資訊／資安 |

## 5. 分期驗收

| 階段 | 目標 | 客戶提供 | 驗收結果 |
|---|---|---|---|
| 0. 資料盤點（1–2 週） | 資料可用性與責任確認 | historian／MES schema、配方、檢驗欄位 | 映射與資料契約簽核 |
| 1. Shadow Mode（4–6 週） | 唯讀評估，不影響生產 | 連續歷史或即時曲線 | 每卷可追溯報告、異常與人工覆核差異 |
| 2. Case Intelligence（6–10 週） | 近鄰案例與結果回測 | 已標註最終品質結果 | 查找時間、precision／recall、風險校準報告 |
| 3. Advisory | 受約束工程建議 | SOP、角色與簽核流程 | 建議採納率、稽核軌跡；無自動控制下發 |

Shadow Mode 維持唯讀。與 PLC／DCS 的寫入連線不屬於初始產品範圍。

## 6. 客戶工作坊的三項決策

1. 選定第一個納入的鋼種／配方 family：資料完整、規格穩定且不良成本明確者優先。
2. 確認最終品質標籤與優先序：檢驗值、客訴、不良代碼與報廢的關係須能追溯。
3. 指定 finding 覆核與處置回填責任人：每類告警必須有製程、品質或設備的明確 owner。
