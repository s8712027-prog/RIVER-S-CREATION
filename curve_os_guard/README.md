# Curve OS Guard｜商用導入原型

這是一個可在工控網路離線運行的 CAL 爐溫曲線判讀原型。它的目的，是將每卷鋼捲的時序曲線轉為可追溯的資料品質判定、製程合規判定、相似歷史案例與受安全約束的工程建議。

> **示範聲明：** 預載 CSV 是合成資料，所有畫面均標示 DEMO。系統在沒有客戶歷史「卷號—最終檢驗結果」資料前，會顯示 `NOT_CALIBRATED`，不會宣稱失敗機率。

## 一鍵啟動

先安裝 Python 3.10+；本原型沒有第三方套件與網路依賴。

```powershell
cd outputs\curve_os_guard
.\run_curve_os.ps1
```

命令列先輸出評估摘要，然後開啟瀏覽器前往 `http://127.0.0.1:8765`。服務只綁定本機迴圈位址，不對區網暴露。

## 客戶資料接入

將一卷資料放入 `data/incoming/`，以 UTF-8 CSV 提供下列最小欄位：

```csv
timestamp,temp_c,setpoint_c
2026-08-25T00:00:00+08:00,680.2,700
2026-08-25T00:01:00+08:00,686.1,700
```

再執行：

```powershell
python curve_os_cli.py --input data/incoming/CUSTOMER-COIL.csv --coil-id CUSTOMER-COIL-001
```

正式導入時，請以來源系統的不可變 `coil_id` 與 UTC 或明確時區 timestamp 作為主鍵；不要以檔名作為唯一身分。

完整的資料欄位、歷史索引結構、工作坊責任與分期驗收，請使用 [docs/CUSTOMER_ONBOARDING.md](docs/CUSTOMER_ONBOARDING.md)。目前版本的已知能力邊界與文件審核結論見 [docs/DOCUMENTATION_AUDIT.md](docs/DOCUMENTATION_AUDIT.md)。

## 判讀契約

| 層次 | 輸出 | 用途 | 不應混用的概念 |
|---|---|---|---|
| 資料品質 | completeness、採樣穩定、感測器合理性、雜訊 | 判斷能否進入分析 | 成品品質 |
| 製程合規 | 升／冷卻速率、均熱偏差、均熱波動、停留時間 | 判斷是否偏離配方 | 資料雜訊 |
| 指紋與近鄰 | 相位對齊曲線形狀與製程特徵 | 協助追查歷史案例 | 因果預測 |
| 結果風險 | 由高相似且已標註的歷史卷加權 | 輔助品質判斷 | 未驗證的 AI 機率 |

系統不會藉由調整 B-Spline 或濾波強度，把原始資料品質或製程合規分數「調高」以通過 Gate。所有配方界線、權重與版本需由客戶製程／品質單位核准後寫入 `config/recipe_catalog.json`。預載設定的 `approval_status` 是 `UNAPPROVED_DEMO`，不得用作生產判定。

## 上線所需資料

第一階段先收集每卷：`coil_id`、timestamp、溫度、setpoint、鋼種、厚度、配方版本、爐區／感測器 ID。第二階段再連結最終檢驗結果或不良代碼，才可校準風險推論。

歷史索引目前保留為 `data/history/coil_records.json` 的可審閱接口；量產導入應改成：原始曲線 Parquet／物件儲存、業務 metadata SQLite 或 PostgreSQL、向量索引 pgvector 或受控本地 ANN。示範資料與客戶正式資料必須分區，且示範資料不得參與風險計算。

## 交付範圍與下一步

這版適合售前展示與資料接入 PoC。正式部署前，須完成資料映射、配方規格簽核、事件式製程分段、歷史結果標註、回測門檻、角色權限、稽核保留與客戶 OT／資安審查。詳見 [docs/COMMERCIAL_DEPLOYMENT.md](docs/COMMERCIAL_DEPLOYMENT.md) 與 [USAGE.md](USAGE.md)。
