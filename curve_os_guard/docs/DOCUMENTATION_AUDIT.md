# 文件審核紀錄｜Guard v2.0

審核基準：`curve_os_core.py`、`curve_os_cli.py`、`app.py` 與目前設定檔。日期：2026-08-25。

| 項目 | 審核結論 | 文件處置 |
|---|---|---|
| 離線、本機 HMI、無第三方依賴 | 已實作 | 列為現有能力 |
| CSV 最小契約 `timestamp,temp_c`，至少 24 點 | 已實作 | 列為現有能力 |
| `setpoint_c` | 可讀取，但 v2.0 未逐點用於計算 | 列為選填欄位與 Shadow Mode 前缺口 |
| 製程分段 | 目前固定依序列等分升溫／均熱／冷卻 | 不宣稱為真實 recipe event 分段；列為升級門檻 |
| 資料品質 | 有時間順序、取樣抖動、合理溫度、二階差分雜訊檢查 | 列為現有能力；「completeness」僅代表成功解析的 CSV，不代表 historian 覆蓋率 |
| 歷史索引 | 讀取既有 `coil_records.json`、排除自身／示範／未通過資料品質資料 | 明確標注不會自動寫入歷史索引 |
| 相似案例 | cosine similarity，限同 recipe family | 列為 PoC 能力；大量資料再轉受控 ANN／pgvector |
| 失敗風險 | 最少 5 筆 similarity ≥ 0.85 且已標註近鄰才估計 | 未達條件一律 `NOT_CALIBRATED`；正式使用前仍需時間切分回測與校準 |
| 建議 | 規則型 finding，提示依 SOP 檢查 | 列為 advisory，不得自動下發 setpoint |
| 稽核 | 目前記錄時間、coil ID、狀態、輸入 SHA-256、報告版本 | 配方版本、簽核 ID、操作者與存取控制列為 Shadow Mode 前缺口 |
| 配方簽核 | 程式可容納額外 metadata，但目前 demo 設定未簽核 | 已於設定檔標示 `UNAPPROVED_DEMO` |

## 結論

文件內容已保留可立即展示與資料接入的功能，但將未實作的歷史登錄、事件式分段、逐點 setpoint、完整稽核和預測驗證明確列為商用導入門檻。客戶在完成這些門檻前，只能將本產品作為唯讀 PoC／Shadow Mode 的判讀輔助。
