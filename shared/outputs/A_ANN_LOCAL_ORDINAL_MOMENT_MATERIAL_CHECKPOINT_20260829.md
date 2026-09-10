# ANN/A local ordinal-moment v2 素材完整性 checkpoint（2026-08-29）

## 目前狀態

九個角色已在任何影片讀取之前完成凍結，但第一次允許的 raw-container hash 階段發現原先登記的四個來源目前不在固定路徑：

- F1：`螢幕錄製 2026-08-29 030156.mp4`
- F2：`螢幕錄製 2026-08-29 030437.mp4`
- F3：`螢幕錄製 2026-08-29 030634.mp4`
- H1：`螢幕錄製 2026-08-29 032547.mp4`

因此目前停在 **attempt marker 之前的素材完整性阻塞**；real-data runner 尚未建立，沒有影片被 probe、decode 或 feature-read，也沒有執行 development evaluator。

## 新 MOV 的凍結角色

依事前固定的檔名流水號順序：

- H2：`IMG_0270.MOV`
- H3：`IMG_0271.MOV`
- X1：`IMG_0272.MOV`
- X2：`IMG_0273.MOV`
- X3：`IMG_0274.MOV`

這五段已僅做 raw-container SHA-256；五個雜湊皆不同。X1–X3 仍未 probe、decode 或 feature-read。

`IMG_0275.MOV`、`IMG_0276.MOV`、`IMG_0277.MOV` 明確排除於本次九來源實驗，保持未開啟，也不能在檢查失敗後替補既有角色。

## 為何不能直接拿多出的影片補位

F1–H1 的角色在影片開啟前已不可逆凍結。看到路徑缺失後再換成另一段，會讓素材選擇受到檢查結果影響，破壞 single-shot 與 fail-closed 邊界。

合法續接只有一種：把原本四個確切檔案恢復到原登記路徑，再繼續計算它們的 container hashes。不能使用轉檔、裁切、複製品或其他來源替換。

## 已核對的凍結狀態

- role manifest SHA-256：`e757527f775d68b3292619235e4d98db415011984275c0f73347dd98f7fda3ad`
- charter、implementation、tests 與 active reader 雜湊均符合 v8 凍結值。
- active provisional reader 未修改。
- local ordinal-moment v2 仍是 isolated inactive candidate。

