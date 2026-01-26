import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches

# ==========================================
# 🔐 簡易パスワード認証機能
# ==========================================
def check_password():
    """正しいパスワードが入力されたら True を返す"""
    def password_entered():
        if st.session_state["password"] == "kikaku1969":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # セキュリティのため入力を削除
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # パスワード入力画面の表示
        st.set_page_config(page_title="Hakodume Pro - Login", layout="centered")
        st.title("🔒 📦 Hakodumeシミュレーション ")
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # パスワードが間違っている場合
        st.error("😕 パスワードが正しくありません")
        st.text_input("もう一度入力してください", type="password", on_change=password_entered, key="password")
        return False
    else:
        # 認証成功
        return True

# 認証チェック。失敗した場合はここで停止
if not check_password():
    st.stop()

# ==========================================
# 📦 以下、シミュレーター本体のコード
# ==========================================
st.set_page_config(page_title="Hakodume Pro", layout="wide")
st.title("📦 Hakodume : カートン入り数・重量・余白シミュレーター")

# --- 共通描画関数 (安定版) ---
def draw_3d_box_with_size(h_val, w_val, d_val, h_qty, w_qty, d_qty, color, margin=0):
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')
    tw, th, td = (w_val * w_qty) + margin, (h_val * h_qty) + margin, (d_val * d_qty) + margin
    for r in range(int(w_qty)):      
        for c in range(int(h_qty)):  
            for l in range(int(d_qty)): 
                x, y, z = r * w_val, c * h_val, l * d_val
                ax.bar3d(x, y, z, w_val*0.95, h_val*0.95, d_val*0.95, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # サイズラベル
    ax.text(tw/2, -td*0.15, 0, f"{int(tw)}", color='red', fontsize=12, fontweight='bold', ha='center')
    ax.text(tw + tw*0.1, td/2, 0, f"{int(td)}", color='blue', fontsize=12, fontweight='bold', ha='left')
    ax.text(-tw*0.15, 0, th/2, f"{int(th)}", color='green', fontsize=12, fontweight='bold', va='center')
    
    max_dim = max(tw, th, td, 1)
    ax.set_xlim(-max_dim*0.1, max_dim); ax.set_ylim(-max_dim*0.1, max_dim); ax.set_zlim(0, max_dim)
    ax.set_axis_off()          
    ax.view_init(elev=20, azim=-35) 
    st.pyplot(fig)

# 1️⃣ 商品設計
st.header("1️⃣ 商品設計（サイズと重量）")
c1, c2 = st.columns([1, 1])
with c1:
    h_orig = st.number_input("商品 本来の縦 (H)", value=100)
    w_orig = st.number_input("商品 本来の横 (W)", value=50)
    d_orig = st.number_input("商品 本来の奥行 (D)", value=30)
    item_weight = st.number_input("商品1個の重量 (g)", value=200)
    face = st.selectbox("正面(W)に向ける辺", ["横(W)を向ける", "縦(H)を向ける", "奥行(D)を向ける"])
    it_w = w_orig if "横(W)" in face else (h_orig if "縦(H)" in face else d_orig)
    up_options = [h_orig, w_orig, d_orig]; up_options.remove(it_w)
    it_h = st.selectbox("高さ(H)に向ける辺", up_options, format_func=lambda x: f"{x}mm")
    it_d = [x for x in [h_orig, w_orig, d_orig] if x != it_w and x != it_h][0]
    st.info(f"配置サイズ: H{it_h} x W{it_w} x D{it_d}")
with c2:
    draw_3d_box_with_size(it_h, it_w, it_d, 1, 1, 1, "skyblue")

st.divider()

# 2️⃣ インナー設計
st.header("2️⃣ インナー設計 (10個入り)")
c3, c4 = st.columns([1, 1])
with c3:
    inner_type = st.radio("包装形態を選択", ["インナー箱 (+5mm)", "インナー袋 (+3mm)"], horizontal=True)
    inner_margin = 5 if "箱" in inner_type else 3
    q_w = st.number_input("横(W)並び数", 1, 10, 2)
    q_d = st.number_input("奥行(D)並び数", 1, 10, 1)
    q_h = 10 // (q_w * q_d)
    inn_w = (it_w * q_w) + inner_margin
    inn_h = (it_h * q_h) + inner_margin
    inn_d = (it_d * q_d) + inner_margin
    st.info(f"✨ {inner_type}設定（遊び {inner_margin}mm 加算済み）")
    st.code(f"インナー外寸 H: {inn_h} / W: {inn_w} / D: {inn_d}")
with c4:
    draw_3d_box_with_size(it_h, it_w, it_d, q_h, q_w, q_d, "orange")

st.divider()

# 3️⃣ カートン設計 & 重量計算
st.header("3️⃣ カートン設計 & 重量計算")
c5, c6 = st.columns([1, 1])
with c5:
    cq_h = st.number_input("縦(H)に積む箱数", 1, 10, 2)
    cq_w = st.number_input("横(W)に並べる箱数", 1, 10, 1)
    cq_d = st.number_input("奥行(D)に並べる箱数", 1, 10, 2)
    box_empty_weight = st.number_input("段ボール・梱包材の重量 (g)", value=500)
    inners_per_carton = (cq_h * cq_w * cq_d)
    total_items_in_carton = inners_per_carton * 10
    carton_weight_kg = ((item_weight * total_items_in_carton) + box_empty_weight) / 1000
    gross_h, gross_w, gross_d = (inn_h * cq_h)+10, (inn_w * cq_w)+10, (inn_d * cq_d)+10
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("📦 1カートンの総重量", f"{carton_weight_kg:.2f} kg")
    with col_stat2:
        st.metric("🔢 カートン内商品総数", f"{total_items_in_carton} 個")
    st.code(f"カートン外寸 H: {int(gross_h)} / W: {int(gross_w)} / D: {int(gross_d)}")
with c6:
    draw_3d_box_with_size(inn_h, inn_w, inn_d, cq_h, cq_w, cq_d, "green", margin=10)

st.divider()

# 4️⃣ パレット積載
st.header("4️⃣ パレット積載シミュレーション (1100x1100 / 高さ1600mm)")
pal_size = 1100
h_limit = 1600
num_h = int(h_limit // gross_h)
pattern = st.selectbox("積み付け方を選択", ["ブロック積み", "煉瓦積み", "窓積み", "風車積み (ピンホール)"])
col_top, col_side, col_res = st.columns([1, 0.8, 1])
w, d = gross_w, gross_d
count_per_layer = 0
boxes = []
total_w_occupied, total_d_occupied = 0, 0

if pattern == "ブロック積み":
    nx, ny = int(pal_size // w), int(pal_size // d)
    total_w_occupied, total_d_occupied = nx * w, ny * d
    offset_w, offset_d = (pal_size - total_w_occupied) / 2, (pal_size - total_d_occupied) / 2
    for i in range(nx):
        for j in range(ny):
            boxes.append((offset_w + i*w, offset_d + j*d, w, d))
            count_per_layer += 1
elif pattern == "煉瓦積み":
    nx = int(pal_size // w); ny_side = int((pal_size - d) // w)
    total_w_occupied = max(nx * w, d); total_d_occupied = d + (ny_side * w)
    offset_w, offset_d = (pal_size - total_w_occupied) / 2, (pal_size - total_d_occupied) / 2
    for i in range(nx): boxes.append((offset_w + i*w, offset_d, w, d)); count_per_layer += 1
    for j in range(ny_side): boxes.append((offset_w, offset_d + d + j*w, d, w)); count_per_layer += 1
elif pattern == "窓積み":
    boxes = [(0,0,w,d), (pal_size-w,0,w,d), (0,pal_size-d,w,d), (pal_size-w,pal_size-d,w,d)]
    count_per_layer = 4; total_w_occupied, total_d_occupied = pal_size, pal_size
elif pattern == "風車積み (ピンホール)":
    total_w_occupied, total_d_occupied = w + d, w + d
    offset_w, offset_d = (pal_size - total_w_occupied) / 2, (pal_size - total_d_occupied) / 2
    boxes = [(offset_w, offset_d, w, d), (offset_w + w, offset_d, d, w), (offset_w + d, offset_d + w, w, d), (offset_w, offset_d + d, d, w)]
    count_per_layer = 4

margin_x = (pal_size - total_w_occupied) / 2 if count_per_layer > 0 else 0
margin_y = (pal_size - total_d_occupied) / 2 if count_per_layer > 0 else 0

with col_top:
    st.subheader("パレット平面図")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    ax1.set_xlim(-100, pal_size + 100); ax1.set_ylim(-100, pal_size + 100)
    ax1.add_patch(patches.Rectangle((0, 0), pal_size, pal_size, color='lightgray', alpha=0.3, edgecolor='black'))
    for b in boxes: ax1.add_patch(patches.Rectangle((b[0], b[1]), b[2], b[3], edgecolor='black', facecolor='skyblue', alpha=0.8))
    
    if count_per_layer > 0:
        ax1.annotate('', xy=(0, pal_size/2), xytext=(margin_x, pal_size/2), arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax1.text(margin_x/2, pal_size/2 + 20, f'{int(margin_x)}', color='red', ha='center', fontweight='bold', fontsize=12)
        ax1.annotate('', xy=(pal_size/2, 0), xytext=(pal_size/2, margin_y), arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax1.text(pal_size/2 + 20, margin_y/2, f'{int(margin_y)}', color='red', va='center', fontweight='bold', fontsize=12)

    ax1.set_aspect('equal'); ax1.axis('off'); st.pyplot(fig1)

with col_side:
    st.subheader("積載段数")
    fig2, ax2 = plt.subplots(figsize=(4, 5))
    ax2.set_xlim(0, 500); ax2.set_ylim(0, h_limit + 100)
    ax2.axhline(h_limit, color='red', linestyle='--')
    for i in range(num_h):
        ax2.add_patch(patches.Rectangle((100, i*gross_h), 300, gross_h, edgecolor='black', facecolor='lightgreen', alpha=0.7))
    ax2.set_ylabel("高さ (mm)"); ax2.set_xticks([]); st.pyplot(fig2)

with col_res:
    total_cartons = count_per_layer * num_h
    total_items_on_pallet = total_cartons * total_items_in_carton
    st.subheader("🏁 最終結果")
    st.metric("パレット上の箱数", f"{total_cartons} 箱")
    st.metric("総入り数", f"{int(total_items_on_pallet)} 個")
    st.info(f"積載高さ: {int(num_h * gross_h)} mm")
