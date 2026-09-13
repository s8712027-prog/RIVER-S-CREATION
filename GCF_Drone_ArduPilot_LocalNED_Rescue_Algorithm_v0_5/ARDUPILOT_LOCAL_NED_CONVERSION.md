# ArduPilot local-NED 雙向轉換

## 核心原則

```text
ArduPilot EKF local-NED telemetry → GCF route frame
GCF rescue waypoint → ArduPilot EKF local-NED target
```

這是固定座標轉換，不是 GPS replacement。轉換必須在 GNSS／定位可信時建立，並在失訊期間鎖定；GNSS degraded/lost 時不可重新建立 origin 或旋轉角。

## 軸向

| GCF route frame | ArduPilot local-NED |
| --- | --- |
| route X | North 經旋轉後的分量 |
| route Y | East 經旋轉後的分量 |
| altitude up | `-Down` |

ArduPilot 接收的 position-only Guided request 使用 `MAV_FRAME_LOCAL_NED`，位置相對 EKF origin，並採 North、East、Down。

## 失訊時的 gate

GCF 可在 GNSS lost 時持續自己的 route-relative propagation；但要將救援航點送到 ArduPilot，必須同時有：

1. pre-loss locked route-to-local-NED alignment；
2. 有效的 ArduPilot local-NED EKF 位置；
3. 核可的非 GNSS EKF source，例如 external navigation 或 optical flow；
4. ArduCopter 處在 Guided，且保留原生 geofence、EKF、電量與 RC failsafe。

缺任何一項即輸出 HOLD／failsafe request，不建立 position target。
