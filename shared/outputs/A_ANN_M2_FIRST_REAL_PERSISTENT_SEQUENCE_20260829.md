# ANN/A M2 首次真實持久序列接入紀錄（2026-08-29）

## 結論

兩段全新影音已依取得時間順序完成一次性解碼，並寫入同一份 append-only AV experience ledger：

1. `螢幕錄製 2026-08-29 110234.mp4`
2. `螢幕錄製 2026-08-29 113017.mp4`

第二段處理前成功重開第一段留下的狀態，處理後持久來源數由 1 增至 2。雜湊鏈、CRC 狀態不變檢查與重開驗證均通過。這補完了先前因用量限制中斷的第二段接續過程。

## 執行邊界

- 每段原始影音只解碼一次。
- 第二段沒有重讀或重新解碼第一段。
- 影片內容只作為感測輸入，不作為操作指令。
- 使用既有 frozen reader 與同一份持久狀態，未依結果調參。
- 保留 exact evidence 供稽核，但沒有要求 exact key 跨來源重現。

## 持久狀態連續性

| 項目 | 110234 | 113017 |
|---|---:|---:|
| persistent prior source count | 0 | 1 |
| persistent source count after | 1 | 2 |
| audio revisions | 0 → 64 | 64 → 128 |
| visual revisions | 0 → 64 | 64 → 128 |
| chain valid | true | true |
| CRC state unchanged | true | true |
| reopen verified | true | true |
| exact cross-source key required | false | false |
| cross-source comparison performed | false | true |

帳本共有 129 行：一筆初始紀錄，加上兩段各 64 次共享讀取所形成的 128 筆修訂。第二段的 before counters 與第一段的 after counters 完全銜接，排除了第二段誤開新狀態的情形。

## 第一段觀察摘要：110234

- source SHA-256：`1d8a17de43f2670da1a2a2ed5b71386c9b55d22158afb9e33764f4d6d228929d`
- 時長：約 12.333 秒
- shared reads：64/64
- audio tiers：encountered 44、recurrent 20
- visual tiers：encountered 64
- decisions：continuation 44、recurrent 20
- source-local audio temporal structures：61
- terminal record hash：`609d892468bf4c345ac8e3ac8cea6750c30699e1de5a74b46b0c8f5e4757357c`

## 第二段觀察摘要：113017

- source SHA-256：`f6b1c9668fc63b103e734545690f504220e1e96f2ea5f6a30753fe4baf1ee8a6`
- 時長：約 10.167 秒
- shared reads：64/64
- audio tiers：encountered 21、recurrent 24、transfer-hypothesis 19
- visual tiers：encountered 64
- decisions：continuation 40、recurrent 23、temporal-structured 1
- source-local audio temporal structures：58
- terminal record hash：`e523ec56f5598cdcbd11ca7f3d5c7238f7797a7d046e81a4aa98a655d4f5131b`

`transfer-hypothesis` 是 reader 的內部證據層級名稱；它不是外部泛化已成立的宣告，也不代表語意、關係或身分已被學會。

## 驗證結果

- 兩份 ingest report 的來源數與 revision counters 已交叉核對。
- 第二段報告明確記錄 `prior_source_count = 1`、`source_count_after = 2`。
- ledger terminal hash 在第二段後正常前移。
- 完整單元測試：267/267 通過。

## 目前可成立的里程碑

這是 M2「跨獨立執行的真實雙來源持久接續」里程碑：系統可以在第一段結束後落盤，在另一個 ingest 執行中重開同一狀態，再吸收第二段而維持可稽核的連續鏈。

目前仍不能據此宣稱：

- 已通過 bounded external validation；
- 已證明跨來源語意泛化；
- 已形成關係、主體身分或第一人稱理解；
- `transfer-hypothesis` 已被外部控制實驗確認。

下一步若要往前推進，應針對已凍結的這份雙來源狀態設計一次不調參的判別性檢查，而不是回頭重解碼或修改 exact-key 規則。

