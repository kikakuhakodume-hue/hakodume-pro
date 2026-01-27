import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches

# ==========================================
# 🔐 簡易パスワード認証機能
# ==========================================
def check_password():
    def password_entered():
        if st.session_state["password"] == "kikaku1969":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.set_page_config(page_title="Hakodume Pro", layout="wide")
        st.title("🔒 📦Hakodume Pass")
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("😕 パスワードが正しくありません")
        st.text_input("もう一度入力してください", type="password", on_change=password_entered, key="password")
        return False
    return True

if not check_password():
    st.stop()

# ==========================================
# 📦 シミュレーター本体
# ==========================================
st.title("📦 Hakodume : カートン入り数・重量・余白シミュレーター")

st.header("👇 どこから入力を始めますか？")
start_point = st.radio(
    "開始ポイントを選択してください",
    ["商品サイズから設計する", "手元のインナーサイズを直接入力する", "手元のカートンサイズを直接入力する"],
    horizontal=True
)

def draw_3d_box_with_size(h_val, w_val, d_val, h_qty, w_qty, d_qty, color, margin=0):
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')
    tw, th, td = (w_val * w_qty) + margin, (h_val * h_qty) + margin, (d_val * d_qty) + margin
    for r in range(int(w_qty)):      
        for c in range(int(h_qty)):  
            for l in range(int(d_qty)): 
                x, y, z = r * w_val, c * h_val, l * d_val
                ax.bar3d(x, y, z, w_val*0.95, h_val*0.95, d_val*0.95, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.text(tw/2, -td*0.15, 0, f"{tw:.1f}", color='red', fontsize=12, fontweight='bold', ha='center')
    ax.text(tw + tw*0.1, td/2, 0, f"{td:.1f}", color='blue', fontsize=12, fontweight='bold', ha='left')
    ax.text(-tw*0.15, 0, th/2, f"{th:.1f}", color='green', fontsize=12, fontweight='bold', va='center')
    max_dim = max(tw, th, td, 1); ax.set_xlim(-max_dim*0.1, max_dim); ax.set_ylim(-max_dim*0.1, max_dim); ax.set_zlim(0, max_dim)
    ax.set_axis_off(); ax.view_init(elev=20, azim=-35); st.pyplot(fig)

gross_h, gross_w, gross_d, total_items_in_carton = 0.0, 0.0, 0.0, 0

# --- A. 商品サイズから設計 ---
if start_point == "商品サイズから設計する":
    st.divider()
    st.subheader("1️⃣ 商品設計")
    c1, c2 = st.columns(2)
    with c1:
        h_orig = st.number_input("商品 H", value=100.0, min_value=1.0)
        w_orig = st.number_input("商品 W", value=50.0, min_value=1.0)
        d_orig = st.number_input("商品 D", value=30.0, min_value=1.0)
        face = st.selectbox("正面(W)方向", ["横(W)", "縦(H)", "奥行(D)"])
        it_w = w_orig if "横" in face else (h_orig if "縦" in face else d_orig)
        up_opts = [h_orig, w_orig, d_orig]; up_opts.remove(it_w)
        it_h = st.selectbox("高さ(H)方向", up_opts); it_d = [x for x in [h_orig, w_orig, d_orig] if x != it_w and x != it_h][0]
    with c2: draw_3d_box_with_size(it_h, it_w, it_d, 1, 1, 1, "skyblue")
    
    st.subheader("2️⃣ インナー設計")
    c3, c4 = st.columns(2)
    with c3:
        inner_type = st.radio("インナーの種類を選択", ["インナー袋 (+2mm)", "インナー箱 (+5mm)"], horizontal=True)
        inner_margin = 2.0 if "袋" in inner_type else 5.0
        inner_unit_qty = st.number_input("インナー1つあたりの入り数", value=10, min_value=1)
        q_w, q_d = st.number_input("並び 横", 1, 10, 2), st.number_input("並び 奥", 1, 10, 1)
        q_h = max(1, inner_unit_qty // (q_w * q_d))
        inn_h, inn_w, inn_d = (it_h * q_h) + inner_margin, (it_w * q_w) + inner_margin, (it_d * q_d) + inner_margin
        st.info(f"算出インナー寸: {inn_h:.1f}x{inn_w:.1f}x{inn_d:.1f}")
    with c4: draw_3d_box_with_size(it_h, it_w, it_d, q_h, q_w, q_d, "orange")
    
    st.subheader("3️⃣ カートン設計")
    c5, c6 = st.columns(2)
    with c5:
        cq_h, cq_w, cq_d = st.number_input("縦積数", 1, 10, 2), st.number_input("横並数", 1, 10, 1), st.number_input("奥並数", 1, 10, 2)
        gross_h, gross_w, gross_d = (inn_h * cq_h) + 10.0, (inn_w * cq_w) + 10.0, (inn_d * cq_d) + 10.0
        inner_count_in_carton = (cq_h * cq_w * cq_d)
        total_items_in_carton = inner_count_in_carton * inner_unit_qty
        st.metric("カートン内インナー数", f"{inner_count_in_carton} 個")
        st.success(f"📦 カートン総入り数: {total_items_in_carton} 個")
    with c6: draw_3d_box_with_size(inn_h, inn_w, inn_d, cq_h, cq_w, cq_d, "green", margin=10)

# --- B. インナーサイズから直接入力 ---
elif start_point == "手元のインナーサイズを直接入力する":
    st.divider()
    st.subheader("1️⃣ インナーサイズ直接入力")
    c1, c2 = st.columns(2)
    with c1:
        inner_unit_qty = st.number_input("インナー1つあたりの入り数", value=10, min_value=1)
        inn_h = st.number_input("インナー H (mm)", value=100.0, min_value=1.0)
        inn_w = st.number_input("インナー W (mm)", value=100.0, min_value=1.0)
        inn_d = st.number_input("インナー D (mm)", value=100.0, min_value=1.0)
    with c2: draw_3d_box_with_size(inn_h, inn_w, inn_d, 1, 1, 1, "orange")
    st.subheader("2️⃣ カートン設計")
    c3, c4 = st.columns(2)
    with c3:
        cq_h, cq_w, cq_d = st.number_input("カートン内 縦積数", 1, 10, 2), st.number_input("横並数", 1, 10, 1), st.number_input("奥並数", 1, 10, 2)
        gross_h, gross_w, gross_d = (inn_h * cq_h) + 10.0, (inn_w * cq_w) + 10.0, (inn_d * cq_d) + 10.0
        inner_count_in_carton = (cq_h * cq_w * cq_d)
        total_items_in_carton = inner_count_in_carton * inner_unit_qty
        st.success(f"📦 カートン総入り数: {total_items_in_carton} 個")
    with c4: draw_3d_box_with_size(inn_h, inn_w, inn_d, cq_h, cq_w, cq_d, "green", margin=10)

# --- C. カートンサイズから直接入力 ---
elif start_point == "手元のカートンサイズを直接入力する":
    st.divider()
    st.subheader("1️⃣ カートンサイズ直接入力")
    c1, c2 = st.columns(2)
    with c1:
        gross_h = st.number_input("カートン H (mm)", value=320.0, min_value=1.0)
        gross_w = st.number_input("カートン W (mm)", value=420.0, min_value=1.0)
        gross_d = st.number_input("カートン D (mm)", value=220.0, min_value=1.0)
        total_items_in_carton = st.number_input("カートン内の総入り数(個)", 20)
    with c2: draw_3d_box_with_size(gross_h, gross_w, gross_w, 1, 1, 1, "green")

# --- 4️⃣ パレット工程 (向きの選択を追加) ---
st.divider()
st.header("4️⃣ パレット積載シミュレーション")

# 🆕 カートンの載せる向きを選択する機能
st.subheader("🔄 カートンの載せる向き")
load_orient = st.radio(
    "パレットに対する底面を選択してください",
    [f"天天地地 (底面: {gross_w:.0f} x {gross_d:.0f})", 
     f"横倒し (底面: {gross_w:.0f} x {gross_h:.0f})", 
     f"縦倒し (底面: {gross_d:.0f} x {gross_h:.0f})"],
    horizontal=True
)

# 選択に応じてパレット上のW, D, H（高さ）を再定義
if "天天地地" in load_orient:
    pal_w, pal_d, pal_h = gross_w, gross_d, gross_h
elif "横倒し" in load_orient:
    pal_w, pal_d, pal_h = gross_w, gross_h, gross_d
else: # 縦倒し
    pal_w, pal_d, pal_h = gross_d, gross_h, gross_w

pal_size, h_limit = 1100.0, 1600.0
num_h = int(h_limit // pal_h) if pal_h > 0 else 0
pattern = st.selectbox("積み付け方を選択", ["ブロック積み", "煉瓦積み", "窓積み", "風車積み"])
col_top, col_side, col_res = st.columns([1, 0.8, 1])
w, d, boxes, count_per_layer = pal_w, pal_d, [], 0
occupied_w, occupied_d = 0.0, 0.0

if pattern == "ブロック積み":
    nx, ny = int(pal_size // w), int(pal_size // d)
    occupied_w, occupied_d = nx * w, ny * d
    for i in range(nx):
        for j in range(ny): boxes.append(((pal_size-occupied_w)/2 + i*w, (pal_size-occupied_d)/2 + j*d, w, d)); count_per_layer += 1
elif pattern == "煉瓦積み":
    nx, ny_side = int(pal_size // w), int((pal_size - d) // w)
    occupied_w, occupied_d = nx * w, d + (ny_side * w)
    for i in range(nx): boxes.append(((pal_size-occupied_w)/2 + i*w, (pal_size-occupied_d)/2, w, d)); count_per_layer += 1
    for j in range(ny_side): boxes.append(((pal_size-occupied_w)/2, (pal_size-occupied_d)/2 + d + j*w, d, w)); count_per_layer += 1
elif pattern == "窓積み":
    occupied_w, occupied_d = pal_size, pal_size
    boxes = [(0,0,w,d), (pal_size-w,0,w,d), (0,pal_size-d,w,d), (pal_size-w,pal_size-d,w,d)]; count_per_layer = 4
elif pattern == "風車積み":
    tw, td = w + d, w + d
    occupied_w, occupied_d = tw, td
    ox, oy = (pal_size-tw)/2, (pal_size-td)/2
    boxes = [(ox, oy, w, d), (ox+w, oy, d, w), (ox+d, oy+w, w, d), (ox, oy+d, d, w)]; count_per_layer = 4

side_margin_w = (pal_size - occupied_w) / 2
side_margin_d = (pal_size - occupied_d) / 2

with col_top:
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    ax1.add_patch(patches.Rectangle((0, 0), pal_size, pal_size, color='lightgray', alpha=0.3))
    for b in boxes: ax1.add_patch(patches.Rectangle((b[0], b[1]), b[2], b[3], edgecolor='black', facecolor='skyblue', alpha=0.8))
    
    if occupied_w > 0 and side_margin_w > 0:
        ax1.text(side_margin_w/2, pal_size/2, f"{side_margin_w:.1f}", color='red', fontweight='bold', ha='center', va='center', rotation=90)
        ax1.text(pal_size - side_margin_w/2, pal_size/2, f"{side_margin_w:.1f}", color='red', fontweight='bold', ha='center', va='center', rotation=90)
    if occupied_d > 0 and side_margin_d > 0:
        ax1.text(pal_size/2, side_margin_d/2, f"{side_margin_d:.1f}", color='red', fontweight='bold', ha='center', va='center')
        ax1.text(pal_size/2, pal_size - side_margin_d/2, f"{side_margin_d:.1f}", color='red', fontweight='bold', ha='center', va='center')

    ax1.set_xlim(-50, pal_size+50); ax1.set_ylim(-50, pal_size+50); ax1.set_aspect('equal'); ax1.axis('off'); st.pyplot(fig1)

with col_side:
    fig2, ax2 = plt.subplots(figsize=(4, 5))
    ax2.axhline(h_limit, color='red', linestyle='--')
    for i in range(num_h): ax2.add_patch(patches.Rectangle((100, i*pal_h), 300, pal_h, edgecolor='black', facecolor='lightgreen', alpha=0.7))
    ax2.set_xlim(0, 500); ax2.set_ylim(0, h_limit + 100); ax2.set_xticks([]); st.pyplot(fig2)

with col_res:
    st.metric("パレット上の箱数", f"{count_per_layer * num_h} 箱")
    st.metric("パレット総入り数", f"{(count_per_layer * num_h) * total_items_in_carton} 個")
    st.divider()
    st.subheader("📏 パレット余白情報")
    st.write(f"**横(W)方向:** 片側 {side_margin_w:.1f} mm")
    st.write(f"**奥行(D)方向:** 片側 {side_margin_d:.1f} mm")
    if side_margin_w < 0 or side_margin_d < 0: st.error("⚠️ パレットからはみ出しています！")
    st.info(f"積載高さ: {int(num_h * pal_h)} mm")
