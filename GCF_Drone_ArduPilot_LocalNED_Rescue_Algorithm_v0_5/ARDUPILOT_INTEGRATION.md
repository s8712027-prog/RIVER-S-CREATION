# GCF-Drone × ArduCopter：Guided/SITL 整合邊界

## 採用方式

GCF-Drone 使用 ArduCopter `GUIDED` 的位置型導航介面；v0.4 產生的是 `SET_POSITION_TARGET_LOCAL_NED` 的 position-only request（`MAV_FRAME_LOCAL_NED=1`、type mask `3576`）。這是高階導航目標，不是姿態、速率、馬達或 actuator 指令。

```text
GCF decision → NavigationIntent → ArduPilot Guided adapter → local-NED request
```

## 硬性 gate

adapter 只有在以下條件都成立時才建立位置 request：

- ArduCopter 已 armed 且在 `GUIDED` mode。
- EKF local-NED position 有效。
- EKF 的非 GNSS 位置來源明確被核可，例如 `external_nav`、`optical_flow` 或已驗證的 dead reckoning。
- route frame 到 local-NED 的剛性座標轉換在 GNSS 遺失前完成並鎖定。

其中任一項失敗，adapter 只輸出 `BLOCKED`、`REQUEST_GUIDED_HOLD` 或 `REQUEST_OPERATOR_OR_ARDUPILOT_FAILSAFE`，不會送出位置命令。

## 為何不能靠 GCF「假 GPS」

ArduCopter 的 Guided position target 是相對 EKF origin 的 local-NED 位置。當 EKF 沒有可信的位置來源時，位置型自主導航沒有合法座標基準；GCF 的 route-relative estimate 不能冒充 GNSS。應先讓 ArduPilot EKF3 正規使用 external navigation、visual odometry 或 optical flow 等來源，再讓 GCF 決定目標與航路。

Guided_NoGPS 只接受 attitude target；v0.4 不使用這種訊息，因為它會讓 GCF 跨入低階姿態控制責任。

## SITL 順序

1. 建立 ArduCopter SITL 與 `GUIDED` 任務。
2. 先驗證 local-NED origin、方向與 route-frame transform。
3. 模擬 GNSS loss，但維持 EKF3 external-nav/optical-flow local position。
4. 將 v0.4 request 僅寫入 log，對照 ArduPilot 位置、mode、EKF 健康與 geofence。
5. 再於 SITL 開啟 request transmission，確認 HOLD、BLOCKED、containment 與 pilot override。
6. HITL 與受控實飛前，保留原生 battery/RF/EKF/geofence failsafe。
