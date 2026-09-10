# ANN/A M2 bounded external control 結果（2026-08-29）

## 最終判定

**Fail**。目前的 local-capability policy 保留 `provisional`，不得依這兩段素材的結果調參後重跑。

這次失敗不是影片解碼、PyAV、素材接入或持久狀態斷裂。兩段素材已各完成唯一一次 reader 執行；本控制檢查只讀既有 append-only ledger 與 ingest reports，沒有開啟影片、neutral archive，也沒有重跑 reader。

## 預先凍結的分割與規則

- Formation：`110234`
- Heldout：`113017`
- 分割依取得時間先決定，未依結果更換。
- 每段 frozen read budget：64。
- Pass 必須同時滿足：
  - formation 與 heldout 都有可用結構；
  - heldout match 的 exact evidence 與 formation 不同；
  - observed support 嚴格高於 reversed-order control；
  - observed support 嚴格高於每一個 adjacency-broken control。
- 可評估但未超過控制為 Fail；缺少可用結構或控制試驗為 Inconclusive。

## 音訊結果：Fail

| 指標 | 數值 |
|---|---:|
| formation candidates | 61 |
| heldout observed structures | 58 |
| heldout supported candidates | 1 |
| distinct exact evidence | 1/1 |
| reversed-order matches | 0 |
| adjacency-broken trials | 31 |
| adjacency-broken mean | 0.4516 |
| adjacency-broken maximum | 2 |
| empirical null p upper | 0.40625 |

音訊的正面證據是：找到 1 個 formation/heldout 共通的結構，兩側 exact evidence 不同，而且 observed `1` 高於 reversed `0`。

否決點是：adjacency-broken controls 最高可產生 `2` 個 match，而 observed 只有 `1`。因此這個 match 尚不能區分「真正的相鄰時間結構」與「破壞相鄰後仍會出現的組合碰撞」。

## 視覺結果：Inconclusive

兩段均形成 0 個 visual temporal structures，因此沒有 formation candidate、heldout structure 或可執行的 adjacency-broken trial。這是證據缺席，不是視覺 representation 已被證偽。

## Frontier 與結構形成

| 指標 | Formation | Heldout |
|---|---:|---:|
| maximum start window | 63 | 63 |
| adjacent triples | 62 | 62 |
| audio temporal structures | 61 | 58 |
| visual temporal structures | 0 | 0 |

Reader 有完整抵達 bounded frontier，也形成大量音訊局部結構；失敗發生在控制特異性，而不是讀取範圍或結構形成量不足。

## 狀態完整性

- persistent sources：2
- ledger records：129
- terminal record hash：`e523ec56f5598cdcbd11ca7f3d5c7238f7797a7d046e81a4aa98a655d4f5131b`
- ledger SHA-256 before/after：`7b78a6e4894e84067d693864ba946b1ab4ce1f939e92fc5f424172232d883479`
- hash chain：valid
- CRC state：unchanged
- 控制後再次核對 ledger hash：仍完全相同
- 完整單元測試：270/270 通過

## 這次結果代表什麼

已確認的工程里程碑仍成立：PyAV 可用、兩段真實來源可一次解碼、狀態可跨執行持久接續、控制檢查可在不重播 reader 的情況下讀取 frozen evidence。

尚未成立的是學習主張：目前音訊結構沒有超過 adjacency-broken null envelope，視覺又沒有可評估結構，所以不能把 provisional policy 升級為 externally validated。

## 下一個合法邊界

依凍結規格，本次結果到此停止：

- 不用這兩段影片調參；
- 不重新解碼、重跑 reader 或換分割；
- 不因 Fail 臨時增加 gate 或放寬 Pass 門檻；
- 保留原始失敗結果作為之後獨立開發週期的約束。

若未來另開模型開發週期，應把問題明確定義為「提高 temporal adjacency specificity，同時保留 distinct exact provenance 與 frontier reach」，並只能在與這兩段外部素材分離的開發資料或合成測試上設計候選。這兩段只能保留為已揭露的失敗證據，不能再當未見驗證資料。

