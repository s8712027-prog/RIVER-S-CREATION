# MSR-LMMHD 單一整合技術平台 v1.0

版本：2026-08-21  
定位：可否證的工程設計基準，不是量產完成聲明  
全名：Modular Sealed Reciprocating Liquid-Metal MHD，模組化密閉往復式液態金屬磁流體平台

## 0. 設計裁決

本案應收斂成一個核心：**密閉、雙向往復、直接產生交流電的 Faraday 液態金屬 MHD 功率匣**。熱聲、波浪、壓力、直線往復與旋轉機械只是不同前端；它們都必須先在標準壓力／聲功埠形成零均值往復流，再接同一種 MSR-LMMHD 核心。

這個裁決有四個意義：

1. 液態金屬每半週反向時，感應電壓與電流同時反向，負載平均功率仍為正；**不需要流體整流器**。
2. 多領域共用的是核心物理、功率埠、控制與製造平台，不是假定同一幾何可跨所有頻率。
3. 旋轉來源以曲柄、偏心輪、液壓泵或壓力脈動器接入；Taylor–Couette 旋轉 MHD 不併入商用基線。
4. 磁場是耦合場，不是能源。淨輸出永遠不得大於熱／聲／機械輸入扣除全部損失。

現階段最強實驗錨點仍是十瓦級全熱機與數十瓦級受驅 MHD 樣機；商用化瓶頸是微伏至毫伏級損耗、千安級電流、端部電流、聲阻抗匹配與壽命，而不是缺少更複雜的新物理。

## 1. 一個核心、多個前端

### 1.1 核心邊界

核心內只保留下列不可變功能：

- 密閉 GaInSn 或經資格認證的其他導電液體；
- 可逆壓力—流量輸入；
- 外加永久磁場下的 Faraday 通道；
- 對置電極、絕緣 Hartmann 壁與受控電流回路；
- 原始低壓大電流交流端子；
- 壓力、位移／速度、溫度、電壓、電流、絕緣與漏液感測。

核心外才放置：

- 熱聲引擎、波浪液壓器、往復致動器或旋轉—壓力轉換器；
- 聲學慣量、順應性與頻率調諧件；
- 同步整流、DC/DC、儲能、逆變與併網保護；
- 散熱器、控制器與安全卸載裝置。

### 1.2 多前端接法

| 能源領域 | 前端功能 | 核心所見的共同變數 | 商用判定 |
|---|---|---|---|
| 廢熱／地熱／燃燒 | Backhaus–Swift 類行進波熱聲引擎 | $\hat p,\hat Q_v,\omega$ | 第一優先；已有完整熱機實驗 |
| 波浪／脈動壓力 | 雙作用隔膜、蓄壓與限幅 | $\hat p,\hat Q_v,\omega$ | 可用，但須處理寬頻與隨機輸入 |
| 直線往復 | 氣壓或液壓耦合器 | $\hat p,\hat Q_v,\omega$ | 最適合台架驗證與產品校正 |
| 旋轉軸功 | 偏心／曲柄或液壓脈動器 | $\hat p,\hat Q_v,\omega$ | 可接平台；一般旋轉發電機仍是比較基準 |

同一平台可有低、中、高頻 cassette 尺寸族；禁止用單一共振器宣稱可無調整涵蓋所有輸入。

### 1.3 功率埠

| 埠 | 努力變數 | 流變數 | 平均功率 |
|---|---|---|---|
| 熱埠 H | 熱端／冷端溫度 | 熱流 $\dot Q_h$ | 以可稽核淨吸熱計 |
| 聲／液壓埠 A | 壓力 $\hat p$ | 體積流率 $\hat Q_v$ | $\bar P_A=\tfrac12\Re\{\hat p\hat Q_v^*\}$ |
| 原始交流埠 E | $\hat V$ | $\hat I$ | $\bar P_E=\tfrac12\Re\{\hat V\hat I^*\}$ |
| 直流埠 D | $V_{dc}$ | $I_{dc}$ | $P_{dc}=V_{dc}I_{dc}$ |
| 輔助埠 X | 控制／冷卻供電 | — | 必須從淨輸出扣除 |

帽號代表峰值相量；若使用 RMS 相量，平均功率式不再乘 $\tfrac12$。所有試驗檔必須註明慣例。

### 1.4 系統拓撲

~~~text
熱／波浪／壓力／直線／旋轉來源
  → 前端阻抗匹配、限幅與密閉壓力傳遞
  → 零均值往復液態金屬
  → 多層 Faraday cassette
  → 同相交流串聯、必要時多串並聯
  → 近端同步整流與主動阻抗合成
  → DC/DC、直流母線、儲能／逆變／負載
~~~

壓力可由共同機械壓板或絕緣隔膜分配給多個密閉 cell；液態金屬不得以連續導電歧管跨接原本要串聯的 cell。

## 2. AC-LMMHD 物理基準

### 2.1 座標、幾何與假設

定義流向為 $x$、電極間電流方向為 $y$、外加磁場為 $z$。電極間距 $d$，磁場方向通道厚度 $b$，有效磁場長度 $\ell$：

$$
A_f=db,\qquad A_j=\ell b,\qquad V_a=\ell db
$$

其中 $A_f$ 是流通截面、$A_j$ 是理想電流截面、$V_a$ 是有效液態金屬體積。第一階模型假定不可壓、物性常數、均勻速度與磁場、低磁 Reynolds 數及準靜態電磁場；端部、壁面與非均勻剖面必須用 3D 模型和量測校正。

準靜態控制式為：

$$
\nabla\cdot\mathbf u=0,\qquad
\rho\left(\frac{\partial\mathbf u}{\partial t}+\mathbf u\cdot\nabla\mathbf u\right)
=-\nabla p+\mu\nabla^2\mathbf u+\mathbf J\times\mathbf B
$$

$$
\mathbf J=\sigma(-\nabla\phi+\mathbf u\times\mathbf B),\qquad
\nabla\cdot\mathbf J=0
$$

一般情況下，開路電壓須由 $\int(\mathbf u\times\mathbf B)\cdot d\mathbf l$ 求得，Lorentz 功率須由體積積分求得；不能只用中心點 $B$ 與速度。

### 2.2 理想 Faraday cell

均勻速度 $u(t)$ 下：

$$
e_{oc}(t)=Bdu(t),\qquad
R_f=\frac{d}{\sigma\ell b}
$$

對純電阻且忽略其他寄生時，文獻常用 load factor：

$$
K_R=\frac{V_L}{e_{oc}}=\frac{R_L}{R_f+R_L}
$$

因此：

$$
J_y=\sigma Bu(1-K_R)
$$

$$
f_{L,x}=-J_yB=-\sigma B^2(1-K_R)u
$$

$$
\Delta p_{em}=\sigma B^2\ell(1-K_R)u
$$

負號表示 Lorentz 力永遠反抗當下流動。若 $U$ 是 RMS 速度：

$$
P_L=\sigma B^2V_aU^2K_R(1-K_R)
$$

$$
P_{J,f}=\sigma B^2V_aU^2(1-K_R)^2
$$

$$
P_{em,in}=\sigma B^2V_aU^2(1-K_R)=P_L+P_{J,f}
$$

若 $U$ 是峰值，上述三式都乘 $\tfrac12$。$K_R=0.5$ 只是在**速度被固定**、內外皆純電阻的假設下得到最大負載功率；它不是完整熱聲系統的通用最佳點。

短路 $K_R\to0$ 時制動與內部焦耳熱最大但負載功率為零；開路 $K_R\to1$ 時電壓最大而電流與電磁制動趨近零。兩者都不是安全停機的充分條件。

### 2.3 直接交流的成立條件

令 $u(t)=U_{pk}\sin\omega t$，則 $e_{oc}$ 與負載電流每半週同時換向；瞬時 $v_Li_L$ 在純電阻上保持非負。因此直接 oscillatory AC-LMMHD 不需 check valve、噴嘴整流或液態金屬循環泵。

這項簡化同時帶來三個新要求：

- 電極與各 cell 的極性、振幅與相位必須一致；
- 端部磁場中的 Stokes–Hartmann 邊界層與 steady streaming 不可忽略；
- PCS 必須在微歐姆等級的源阻抗下合成負載，不能把整流器當成理想電阻。

## 3. 互易二埠與耦合阻抗

以體積流率 $\hat Q_v=A_f\hat u$ 定義電機耦合常數：

$$
g=\frac{e_{oc}}{Q_v}=\frac{B}{b}
$$

理想互易關係為 $e_{oc}=gQ_v$、$\Delta p_{em}=gI$。峰值相量二埠寫成：

$$
\hat V=g\hat Q_v-Z_i(\omega)\hat I
$$

$$
\Delta\hat p=Z_h(\omega)\hat Q_v+g\hat I
$$

其中：

$$
Z_i=R_f+R_{electrode}+R_{contact}+R_{bus}+j\omega L_{loop}+Z_{end,e}
$$

$$
Z_h=R_v+j\omega L_h+\frac{1}{j\omega C_h}+Z_{end,h}
$$

接上 $Z_L$ 後：

$$
\hat I=\frac{g\hat Q_v}{Z_i+Z_L},\qquad
K(\omega)=\frac{Z_L}{Z_i+Z_L}
$$

電氣端反射回聲／液壓端的阻抗為：

$$
Z_{em}(\omega)=\frac{g^2}{Z_i+Z_L}
$$

因此 PCS 改變的不只是輸出電功，也直接改變共振頻率附近的阻尼、速度與壓力。固定源速度時，純電阻最大功率在 $R_L=R_i$；固定 Thevenin 源且含電抗時是共軛匹配；但自激熱聲整機須以**淨 DC 功率與穩定裕度**共同最佳化。

相量功率可直接分解：

$$
\bar P_{em}=\frac12|g\hat Q_v|^2\Re\left\{\frac{1}{Z_i+Z_L}\right\}
$$

$$
\bar P_L=\frac12|g\hat Q_v|^2\frac{\Re\{Z_L\}}{|Z_i+Z_L|^2}
$$

Chen 等人在完整熱聲耦合實驗中定義 $K=R_e/(R_e+R_i)$；固定速度理論預測 $K=0.5$，但實測峰值約在 $K=0.86$，有效區約 $0.80$–$0.88$。這正是必須採二埠耦合模型、不可硬編一個最佳 $K$ 的證據。

## 4. 必報無因次群

以 Hartmann 壁法向半尺度 $a$、RMS 或明確標示的特徵速度 $U$、角頻率 $\omega$ 定義：

| 參數 | 定義 | 工程含義 |
|---|---|---|
| Reynolds | $Re=Ua/\nu$ | 慣性相對黏性 |
| Hartmann | $Ha=Ba\sqrt{\sigma/(\rho\nu)}$ | Lorentz 相對黏性 |
| Interaction | $N=Ha^2/Re=\sigma B^2a/(\rho U)$ | Lorentz 相對慣性 |
| Oscillation | $R_\omega=\omega a^2/\nu=\alpha^2$ | 非定常相對黏性；$\alpha$ 為 Womersley 數 |
| Oscillatory interaction | $N_\omega=Ha^2/R_\omega=\sigma B^2/(\rho\omega)$ | Lorentz 相對非定常慣性 |
| Magnetic Reynolds | $Rm=\mu_0\sigma Ua$ | 誘發磁場相對外加磁場 |
| Stroke ratio | $\varepsilon_s=U/(\omega a)$ | 位移振幅相對通道尺度 |
| Wall conductance | $C_w=\sigma_wt_w/(\sigma a)$ | 壁面分流能力；尺度須隨實際壁向重定義 |
| Electrical reactance | $\beta_e=\omega L_{loop}/R_\Sigma$ | 寄生電感相對微歐姆電阻 |

純電阻負載的近似非定常電磁阻尼為：

$$
\Gamma_{em}\approx(1-K_R)N_\omega
$$

混合 Stokes–Hartmann 層的特徵根可寫為：

$$
(qa)^2\approx(1-K_R)Ha^2+jR_\omega
$$

短路強磁極限 $\delta_H\sim a/Ha$，無磁高頻極限 $\delta_S\sim\sqrt{2\nu/\omega}$。高 $Ha$ 代表剖面變平且邊界層變薄，也代表幾何、壁電導與端部電流更敏感；單報「$Ha=699$」不能證明效率或穩定。

每個工況至少同時回報 $Ha,Re,N,R_\omega,N_\omega,Rm,\varepsilon_s,C_w,K$ 與 $\beta_e$。只有量到 $Rm\ll1$ 才可把外加磁場視為不受流動影響。

## 5. 商用 cassette

### 5.1 單 cell

建議基線為近 1:1 矩形截面、短而均勻的有效磁場區、電極在平行磁場的兩壁、Hartmann 壁絕緣。1:1 不是普遍最優，而是 2026 實驗在聲學阻抗、電極配置與邊界層之間採用的可驗證起點。

每個 cell 應包含：

- 316L／合格 Ni–Cr 合金主承壓殼；
- 有效段可更換的陶瓷或經驗證絕緣 liner；
- 可更換電極 cartridge 與 Kelvin 端子；
- 永磁體、低渦電流磁轭、實測 3D $B(x,y,z,T)$ map；
- 端部漸變磁場、絕緣 guard 區與可換 end insert；
- 惰性氣體／真空充填口、膨脹容積、洩漏與絕緣監測；
- 二次圍堵、過壓、過溫與行程限制。

### 5.2 多層、串聯與並聯

沿磁場間隙將液態金屬分成多個薄、全電氣隔離的層，可縮短渦電流迴路；每層配置獨立電極。各層以共同壓力機構聲學並聯，以同相 AC 端子電氣串聯：

$$
V_{oc,s}=N_sV_{oc,c},\qquad Z_{i,s}=N_sZ_{i,c},\qquad I_s=I_c
$$

相位一致時，串聯把功率升成較高電壓而不把千安電流再相加。所需串聯數初估為：

$$
N_s\ge
\left\lceil\frac{V_{AC,target}}{K_RBdU_{pk}}\right\rceil
$$

多個串聯 string 再並聯可提高功率，但每 string 必須有電流量測、均流與故障隔離。禁止用連續液態金屬端歧管連接電氣串聯層，否則會形成旁路。

堆疊 gate：cell 電壓幅值變異係數小於 5%、相位差小於 3°、任一 cell 可隔離且不使其餘 cell 失壓。

### 5.3 端部、壁面與材料

- Jiang 等人的 2023 數值研究顯示，塑形端部外磁場可使端部內焦耳熱近乎減半並使模擬效率提高約 9.5%；這是 $B(x)$ 優化方向，**不是實驗保證**。
- 2026 研究亦把多層通道與增強端部磁場列為降低渦電流、端部電流的後續方法。
- 靜態 2000 h、最高 200 °C 的材料研究發現 GaInSn 對 Al、Cu、黃銅攻擊嚴重，而不鏽鋼與 Ni–Cr 合金未見明顯腐蝕；這不能替代往復、通電、應力與溫循壽命試驗。
- 銅只能位於經驗證的導電／擴散屏障後或作可更換耗材；氧化層與合金化會改變接觸電阻。
- 2026 樣機以氮氣預填抑制可見氧化；商用品仍須定義含氧量、充填程序、氣泡與導電率漂移 gate。

## 6. 超低壓大電流 PCS

2023 GaInSn 樣機在 15 Hz、約 4.3 m/s 下報告約 113–114 mV、1720 A、68 W，負載約 $3.9\times10^{-5}\ \Omega$；最大實驗 MHD 效率約 27%。這說明 PCS 必須先處理源阻抗，而不是直接套用一般低壓電源模組。

基線拓撲：

~~~text
多 cell 同相 AC 串聯
 → 極短層疊母排
 → 四象限同步橋／主動整流器
 → 多相交錯升壓
 → DC link
 → 儲能、負載或逆變
~~~

設計規則：

1. 優先在整流前串升 AC 電壓；不得逐 cell 用二極體整流。
2. 半導體、母排、接點、熔斷與感測器一律用 $I^2R$ 實測損失建模。
3. $1000\ \mathrm A_{rms}$ 下每 $1\ \mu\Omega$ 即耗 1 W；所有接點都需四線式微歐姆量測。
4. 以層疊母排、最小迴路面積與近端整流降低 $L_{loop}$，並驗證 $\beta_e<0.1$ 或以控制補償。
5. 整流器必須能合成 $Z_L=R_L+jX_L$，而不只追蹤電阻最大功率點。
6. 輔助電源、閘極驅動、感測、冷卻與待機功耗都從 $P_{dc}$ 扣除。

## 7. 控制與保護

控制器每週期以同步取樣估算 $\hat p,\hat Q_v,\hat V,\hat I$，線上辨識 $Z_i,Z_h,g$，再以主動整流器調整複數 $Z_L$。目標函數為：

$$
\max\ P_{dc,net}
\quad\text{subject to}\quad
p_{min/max},\ x_{stroke},\ I,\ T,\ B,\ \Delta R,\ \text{stability margin}
$$

建議狀態機：

- Purge／Fill：確認含氧、液位、絕緣與無氣泡；
- Start：高 $K$、低電磁制動，逐步建立振幅；
- Capture：緩升實部負載，補償電抗並鎖定共振；
- Optimize：在壓力、行程、溫度限制內最大化淨 DC；
- Derate：溫度、相位差或接觸電阻漂移時降載；
- Trip：切斷熱／機械源、接入聲學 dump 或旁通，再隔離故障 string。

開路會移除電磁阻尼，可能讓熱聲振幅過大；短路會產生最大制動與內部焦耳熱，也可能過流。故障安全必須同時具備源切斷、壓力卸載／聲學 dump、限流與熱容量驗證，不能只選開路或短路。

永磁場作基線。只有量到 trim coil 所增加的淨 DC 功率大於線圈與冷卻功耗，才可保留主動磁場調節。

## 8. 效率帳與文獻錨點

效率必須逐埠定義：

$$
\eta_{TA}=\frac{P_A}{\dot Q_{h,net}},\qquad
\eta_{MHD}=\frac{P_{AC}}{P_A},\qquad
\eta_{PCS}=\frac{P_{DC}}{P_{AC}}
$$

$$
\eta_{heat\to DC}=\eta_{TA}\eta_{MHD}\eta_{PCS}
$$

商用淨效率另須扣除泵、控制、冷卻、磁場調節、待機與熱源介面耗能。MHD 週期平均能量帳為：

$$
P_A=P_{AC}+P_{J,fluid}+P_{contact/electrode/bus}
+P_{end/leak}+P_{yoke}+P_{visc}
$$

| 原始研究 | 已實測 | 正確解讀 |
|---|---|---|
| Zhu 等，Applied Energy 2023 | 15 Hz 下 68 W、聲功至電功 24%，最大實驗約 27% | 已證明往復 AC-LMMHD；尚未證明含 PCS 的淨 DC |
| Chen 等，The Innovation Energy 2026 | $B=0.65$ T；885 K、3.2 MPa 下 13.5 W、熱效率 11.0%、電流幅值 700 A、$K=0.82$；5 h 漂移最大 2.7% | 已證明完整熱聲—LMMHD 可運轉；5 h 不是商用壽命 |
| Chen 等，2026 典型波形 | 壓力幅 1.10 bar、電流幅 330 A、相差 88.7° | 證明聲學相位與電氣負載必須共同控制 |

2026 論文的熱效率以平均負載電功除以扣除其定義熱漏後的淨加熱功率；不得直接稱為含整流、逆變、冷卻及場站輔助的 fuel-to-wire 效率。

## 9. 尺寸化流程

每一頻帶 cassette 依下列順序設計：

1. 由前端量到可用 $\hat p,\hat Q_v,\omega$ 與源阻抗，不以名目熱功率代替。
2. 選擇 $B,d,b$ 後，以 $e_{oc}=BdU$ 估算 cell 電壓。
3. 由目標 $P_L$ 反算有效體積：

$$
V_a=\frac{P_L}{\sigma B^2U^2K_R(1-K_R)}
$$

4. 由 $R_f=d/(\sigma\ell b)$ 與 $I_{pk}=\sigma BU_{pk}(1-K_R)\ell b$ 尺寸化電極、母排及 PCS。
5. 以 $N_s$ 把 AC 電壓升至可高效率整流的範圍，再決定 string 並聯數。
6. 計算全部無因次群、邊界層、壓降、行程、熱與應力；禁止只用功率密度外推。
7. 以 3D MHD 模型求端部電流、壁面分流、磁轭渦流和非均勻速度。
8. 把 $Z_i,Z_h$ 匯入完整前端模型，掃描 $Z_L$、頻率、熱端條件與容差。
9. 先製作單 cell，再製作 series stack；只有實測通過 gate 才放大。

2026 實驗指出液態金屬通道長度變化 10% 可造成約 10% 慣量變化與約 6% 共振頻率變化。因此商用設計必須提供可調 compliance／resonator trim，並控制充填質量與幾何公差。

## 10. 可否證 technical gates

以下是本案建議的工程 gate，不是文獻已達成的產品規格。

### G0 — 定義與可追溯性

- 幾何、流體批次、溫度物性、$B$ map、負載與相量慣例完整；
- 原始波形共同時鐘；儀器校正與不確定度可追溯；
- 未通過後續 gate 時，主張維持 research prototype。

### G1 — 互易與能量閉合

- $e_{oc}/(BdU)=1\pm10\%$，或由 3D 積分模型在同一容差內預測；
- $F_{em}/(IBd)=1\pm10\%$；
- 一週期能量殘差小於輸入 5%，或落在合併量測不確定度內；
- $V$–$I$、$\Delta p$–$Q_v$ 模型在設計包絡內殘差小於 10%。

### G2 — 寄生損失

- 電極＋接觸＋母排電阻不超過理論流體電阻的 25%；
- 壁面／絕緣漏電小於負載電流 1%；
- 端部損失小於聲功輸入 10%，磁轭渦流小於 5%；
- $\beta_e<0.1$，否則須證明主動補償後的淨增益；
- 開、短路與 $B=0$ 對照可排除熱電與感應雜訊。

### G3 — 單 cassette

- 先重現 $\eta_{acoustic\to AC}\ge25\%$ 的連續穩態基線；
- 商用候選目標 $\eta_{acoustic\to AC}\ge30\%$；
- 所有效率均以同步量得的聲功為分母，不以模擬流速替代。

### G4 — stack 與 PCS

- 幅值變異係數小於 5%、cell 相位差小於 3°；
- stack PCS 峰值工況效率不低於 95%，且完整負載範圍有地圖；
- 單 cell 開路／短路故障可隔離，不造成液態金屬電氣旁路；
- 若 MHD 為 30%、PCS 為 95%，則 AC 至 DC 鏈上限僅約 28.5%，不得重複計算效率。

### G5 — 完整熱機

- 在 850–900 K 類工況，以總可稽核熱輸入與全部輔助功耗計，重現 $\eta_{heat\to DC,net}\ge10\%$；
- 熱源關閉、待機、啟動與冷卻能耗分列；
- 任何 kW 主張必須來自實測 DC 母線，不得由單 cell 功率密度直接外推。

### G6 — 壽命與材料

- 第一階段 1000 h；15 Hz 約 $5.4\times10^7$ 次循環；
- 第二階段 10,000 h；15 Hz 約 $5.4\times10^8$ 次循環；
- 輸出、內阻與壓降漂移各小於 5%，無漏液、絕緣失效、電極剝落或不可逆氣泡；
- coupon → 往復循環 loop → 通電 electrode → 完整 cassette 依序通過，不能用靜態浸泡跳級。

### G7 — 模組化與商用放大

- 先完成約 100 W 密閉 AC／DC cassette，再完成實測 1 kW DC stack；
- N+1 string 可在不停整機的條件下隔離故障模組；
- 模組具有可追蹤序號、材料批次、充填質量、$B$ map 與阻抗指紋；
- 只有 1 kW stack 通過熱循環、壓力規範、EMC、維修與成本審查後，才進入社區／車用應用評估。

## 11. 主要失效模式與設計回應

| 失效模式 | 可觀測量 | 設計回應 |
|---|---|---|
| 接觸電阻上升 | 四線 $R$, 局部溫升, 諧波 | 可換電極、屏障層、惰性充填 |
| 壁面分流 | 漏電、輸出偏低、熱點 | 絕緣 liner、guard、$C_w$ gate |
| 端部電流／steady streaming | 端部溫升、DC 流偏置、壓降 | $B(x)$ 塑形、端部長度、3D 驗證 |
| 磁轭渦流 | 磁轭溫升、相位偏移 | 分段／疊片磁路、薄層 cell |
| 聲阻抗失配 | 頻率漂移、壓力升但電功降 | compliance trim、主動複數負載 |
| 開路過振幅 | 壓力／行程超限 | 聲學 dump、源切斷，不單靠開路 |
| 短路過熱 | 千安過流、液體升溫 | 限流、短時制動額定、源切斷 |
| 氧化／氣泡 | 導電率下降、波形失真 | 真空／惰性充填、含氧與液位監測 |
| 腐蝕／脆化／漏液 | 質量損失、金屬離子、洩漏 | 分級材料驗證與二次圍堵 |
| cell 失相 | stack 電壓下降、環流 | 每 cell 相量量測與 string 隔離 |

## 12. 商用主張邊界

完成 G1–G3 可稱「受驗證 AC-LMMHD cassette」；完成 G4 可稱「DC 功率模組」；完成 G5–G7 才可稱「商用候選熱能發電平台」。

在此之前不得聲稱：

- 磁場、自生電流或微量啟動能提供持續淨能源；
- 11% 文獻熱效率等於本案含 PCS 與輔助系統的淨效率；
- 5 h 穩定等於免維護壽命；
- Taylor–Couette、磁性微粒或 GCF 評分已提高實測淨輸出；
- 由十瓦樣機直接線性推得 kW、車用或社區部署可行。

## 13. 主要原始／官方來源

1. H. Chen et al., “A thermoacoustically-driven liquid metal magnetohydrodynamic generation system with a thermal efficiency of 11%,” The Innovation Energy 3, 100139 (2026). [期刊頁面](https://www.the-innovation.org/article/doi/10.59717/j.xinn-energy.2026.100139)；[全文 PDF](https://www.the-innovation.org/data/article/energy/preview/pdf/XINNENERGY-2025-0057.pdf)。
2. S. Zhu et al., “Experimental and numerical study of a liquid metal magnetohydrodynamic generator for thermoacoustic power generation,” Applied Energy 348, 121453 (2023). [DOI／出版頁](https://doi.org/10.1016/j.apenergy.2023.121453)。
3. C. Jiang et al., “A method to optimize the external magnetic field to suppress the end current in liquid metal magnetohydrodynamic generators,” Energy 282, 128251 (2023). [DOI／出版頁](https://doi.org/10.1016/j.energy.2023.128251)。
4. J. C. Domínguez-Lozoya, H. Perales Valdivia, S. Cuevas García, “Analysis of the oscillatory liquid metal flow in an alternate MHD generator,” Revista Mexicana de Física 65, 239–250 (2019). [DOI／期刊頁](https://doi.org/10.31349/RevMexFis.65.239)；[全文 PDF](https://www.scielo.org.mx/pdf/rmf/v65n3/0035-001X-rmf-65-03-239.pdf)。
5. L. Bühler and S. Horanyi, “Experimental Investigations of MHD Flows in a Sudden Expansion,” FZKA 7245, Forschungszentrum Karlsruhe (2006). [KIT 官方報告](https://publikationen.bibliothek.kit.edu/270065516/3814840)。
6. P. Geddis et al., “Effect of static liquid galinstan on common metals and non-metals at temperatures up to 200 °C,” Canadian Journal of Chemistry 98, 787–798 (2020). [DOI](https://doi.org/10.1139/cjc-2020-0227)。
7. T. Sato et al., “Method to Reduce the Contact Resistivity between Galinstan and a Copper Electrode for Electrical Connection in Flexible Devices,” ACS Applied Materials & Interfaces 13, 18247–18254 (2021). [DOI／出版頁](https://doi.org/10.1021/acsami.1c00431)。

---

**最終工程結論：**可商用化的整合不是把熱聲、旋轉、往復與微粒子塞入同一腔體，而是把它們收斂到同一個可量測的壓力—流量埠，使用密閉直接 AC Faraday cassette、電氣串聯多層與主動阻抗 PCS。平台是否成立，最終由能量閉合、寄生損失、堆疊相位、淨 DC、千小時循環與可維修性共同判定。
