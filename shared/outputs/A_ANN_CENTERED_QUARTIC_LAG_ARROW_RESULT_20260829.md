# ANN/A 新表示法實跑結果（2026-08-29）

## 結論

這次不是修復成功，而是完成了一個可判讀、不可重跑的開發性 FAIL。

新的 centered quartic lag-arrow（CQLA）在合成資料上通過數學性質、反序、
不變量、控制組與 fail-closed 評估器測試；但凍結後用六份既有 neutral
archive 做唯一一次 3+3 實跑時，沒有任何正向狀態轉移到 held-out 來源。
因此候選表示法已被拒絕，沒有接入目前 provisional reader。

## 實跑數字

- formation dictionary：9
- held-out forward support：0
- held-out raw-reverse support：0
- 三個 held-out 的 forward：0 / 0 / 0
- 三個 held-out 的 reverse：0 / 0 / 0
- 62 個控制組最大 support：1
- raw reversal identity：通過
- PCM polarity/channel invariants：通過
- exact evidence disjointness：通過
- 最終決定：`reject-development-candidate`
- 報告 SHA-256：
  `328dccacccaa09baf50e3ac973a93051bb02d63e7d4edf495c8a2181e25ad3c5`
- 完整明確測試清單：285 tests + 3 subtests，全數通過

## 這代表什麼

接入、archive、PCM 與 runner 都正常；這不是 PyAV 問題。失敗點在表示法：
每個來源內都有大量狀態，但完整的 rank/sign 類別太依賴單一來源。三個
formation 來源只留下 9 個共同類別，到了 held-out 完全沒有轉移。

目前 reader 原本的規則沒有被改回去：來源本地學習仍然不要求 exact key
跨來源重現。CQLA 是隔離的表示法開發實驗，不是現行 reader 的學習契約。

## 不做的事

- 不換 lag、不刪欄位、不放寬 2-of-3、不換六份 archive 後重跑。
- 不把這個結果解讀成外部泛化。
- 不重新開啟或解碼已刪除／本機原始影片。
- 不把 CQLA 接入 provisional reader。

## 下一條可推進的路

下一個分支應改成「來源層級的方向統計」，不再要求 exact categorical key
跨來源重現。建議研究 normalized imaginary trispectral time-arrow：用固定的
四階跨頻率相位耦合量表達時間方向；反序會翻轉虛部方向，四階量可維持
polarity，不以波形或離散 key 相等作判準。

正確順序是：先在完全不讀 archive 的情況下凍結數學契約、surrogate 控制與
合成測試；只有 synthetic gate 通過後，才可另做一次新的舊 archive
development run。既有素材只能支持開發，不可再稱為 untouched external
validation。


