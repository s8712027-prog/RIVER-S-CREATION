# ANN/A 舊 archive development 結果（2026-08-29）

## 結論

已依使用者要求改用過去保存的 neutral archives，不再要求原始影片或持續提供新素材。六段 archive 完成一次 local ordinal-moment v2 development evaluation，結果為 **Fail**；v2 保持隔離且不啟用。

這不是素材或 PyAV 問題：六段都能正常讀取，全部為 16 kHz、雙聲道，前 64 個 100 ms windows 的容量一致。原始影片沒有被尋找、開啟或重新解碼，RGB 也沒有被讀取。

## 凍結分組

- Formation：`095108`、`095413`、`095744`
- Heldout：`101128`、`101506`、`103439`

分組按取得時間先固定，不依特徵或結果挑選。這些是既有資料，因此本輪只屬 retrospective development，不能宣稱 untouched external validation。

## 結果

| 指標 | 數值 |
|---|---:|
| formation dictionary | 15 |
| forward supported | 1 |
| raw reverse supported | 2 |
| frozen individual controls | 59 |
| control maximum | 3 |
| per-heldout forward | 1 / 4 / 1 |
| per-heldout reverse | 1 / 2 / 4 |

必要完整性檢查全部通過：

- raw reversal identity：valid
- PCM invariants：valid
- exact evidence disjointness：valid
- 每個來源 occurrence capacity：128

因此否決點位於 representation，而非執行管線。v2 雖形成 15 個跨 formation 的 oriented keys，但只有 1 個在至少兩個 heldout sources 重現；reverse 有 2 個，控制最高可達 3。H1 forward/reverse 平手，H3 明顯偏向 reverse。

## 驗證與邊界

- 完整回歸：273/273 通過
- 結果報告 SHA-256：`9c4e49c77648c0b1740a078ac85414bab84b459e119a9341f0e64a8d2446c1d5`
- 不可在另一組舊 archive 上重跑 v2
- 不可依結果修改 microbins、moments、threshold、controls 或 split
- active provisional reader 未修改

後續仍可使用其餘既有 neutral archives 研究一個全新的 branch-level hypothesis，但必須先說明新的 source-transferable time-asymmetric sensor property，再凍結角色與控制；不能再做 count、delta、prediction、complete trajectory 或 parity-moment 的近鄰變形。

