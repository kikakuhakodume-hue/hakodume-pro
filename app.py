import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects

# ==========================================
# 🔐 簡易パスワード認証機能（Enterキー対応）
# ==========================================
def check_password():
    if "password_correct" not in st.session_state:
        st.set_page_config(page_title="Hakodume Pro", layout="wide")
        st.title("📦 Hakodume Pass")
        
        pwd = st.text_input("パスワードを入力してください", type="password", key="auth_pwd")
        
        if pwd: 
            if pwd == "kikaku1969":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("😕 パスワードが正しくありません")
        
        st.button("ログイン") 
        return False
    return True

if not check_password():
    st.stop()

# ==========================================
# 📦 共通：3D描画関数（文字化け回避のため図面のみD表記）
# ==========================================
def draw_3d_box_with_size(h_val, w_val, d_val, h_qty, w_qty, d_qty, color, m_d, m_w, m_h, is_main_chart=True):
    try:
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111, projection='3d')
        total_d = (d_val * d_qty) + m_d
        total_w = (w_val * w_qty) + m_w
        total_h = (h_val * h_qty) + m_h
        
        for l in range(int(d_qty)):      
            for r in range(int(w_qty)):  
                for c in range(int(h_qty)): 
                    x, y, z = r * w_val, l * d_val, c * h_val
                    ax.bar3d(x, y, z, w_val*0.9, d_val*0.9, h_val*0.9, color=color, alpha=0.6, edgecolor='black', linewidth=0.3)
        
        fs = 9
        off = max(total_w, total_d, total_h) * 0.25
        txt_style = [path_effects.withStroke(linewidth=2, foreground='white')]
        
        ax.text(-off, 0, total_h/2, f"H:{total_h:.1f}", color='green', fontsize=fs, fontweight='bold', path_effects=txt_style, zorder=100)
        ax.text(total_w/2, -off, 0, f"W:{total_w:.1f}", color='red', fontsize=fs, fontweight='bold', path_effects=txt_style, zorder=100)
        # 修正：図面ラベルの四角（文字化け）を消すため「D」表記に変更
        ax.text(total_w + off, total_d/2, 0, f"D:{total_d:.1f}", color='blue', fontsize=fs, fontweight='bold', path_effects=txt_style, zorder=100)
        
        max_dim = max(total_w, total_d, total_h, 100)
        limit = max_dim * 1.3
        ax.set_xlim(0, limit); ax.set_ylim(0, limit); ax.set_zlim(0, limit)
        ax.set_axis_off(); ax.view_init(elev=20, azim=-35)
        st.pyplot(fig)
    except: st.write("数値を入力してください")

# ==========================================
# 📋 メインUI（入力ラベルは日本語を維持）
# ==========================================
st.title("📦 Hakodume Pro : カートン設計シミュレーター")

start_point = st.radio("開始ポイント", ["商品サイズから設計", "インナーサイズを直接入力", "カートンサイズを直接入力"], horizontal=True, key="nav_root")
g_d, g_w, g_h, total_qty, total_kg = 0.0, 0.0, 0.0, 0, 0.0

if start_point == "商品サイズから設計":
    st.divider(); st.subheader("1️⃣ 商品設計")
    c1, c2 = st.columns(2)
    with c1:
        v_h = st.number_input("商品 高さ(H)", value=100.0, step=0.1, format="%.1f", key="a1_h")
        v_w = st.number_input("商品 横幅(W)", value=50.0, step=0.1, format="%.1f", key="a1_w")
        v_d = st.number_input("商品 縦(D)", value=30.0, step=0.1, format="%.1f", key="a1_d")
        v_weight = st.number_input("⚖️ 商品単体重量(g)", value=0.0, step=1.0, format="%.1f", key="a1_weight")
        f_d_label = st.selectbox("縦(D)にする辺", ["縦(D)", "横幅(W)", "高さ(H)"], key="a1_fd")
        it_d = v_d if "縦(D)" in f_d_label else (v_w if "横幅" in f_d_label else v_h)
        rem = [v_d, v_w, v_h]; rem.remove(it_d)
        it_w = st.selectbox("横幅(W)にする辺", rem, key="a1_fw")
        it_h = [x for x in [v_d, v_w, v_h] if x != it_d and x != it_w][0]
    with c2: draw_3d_box_with_size(it_h, it_w, it_d, 1, 1, 1, "skyblue", 0, 0, 0, is_main_chart=True)
    
    st.subheader("2️⃣ インナー設計")
    c3, c4 = st.columns(2)
    with c3:
        i_qty = st.number_input("入り数", value=10, key="a2_qty")
        i_qd = st.number_input("商品並び縦(D)", value=1, key="a2_qd")
        i_qw = st.number_input("商品並び横(W)", value=2, key="a2_qw")
        i_qh = max(1, i_qty // (i_qw * i_qd)) if (i_qw * i_qd) > 0 else 1
        st.write(f"（高さ方向 {i_qh} 段）")
        la1, la2, la3 = st.columns(3)
        with la1: i_plus_h = st.number_input("高さ(H)＋", value=2.0, step=0.1, format="%.1f", key="a2_ph")
        with la2: i_plus_w = st.number_input("横幅(W)＋", value=2.0, step=0.1, format="%.1f", key="a2_pw")
        with la3: i_plus_d = st.number_input("縦(D)＋", value=2.0, step=0.1, format="%.1f", key="a2_pd")
        inn_d, inn_w, inn_h = (it_d * i_qd) + i_plus_d, (it_w * i_qw) + i_plus_w, (it_h * i_qh) + i_plus_h
        st.info(f"インナー外寸: H{inn_h:.1f} x W{inn_w:.1f} x 縦(D){inn_d:.1f}")
    with c4: draw_3d_box_with_size(it_h, it_w, it_d, i_qh, i_qw, i_qd, "orange", i_plus_d, i_plus_w, i_plus_h, is_main_chart=True)
    
    st.subheader("3️⃣ カートン設計")
    c5, c6 = st.columns(2)
    with c5:
        cq_h = st.number_input("インナー積み数(H)", value=2, key="a3_cqh")
        cq_w = st.number_input("インナー並び横(W)", value=1, key="a3_cqw")
        cq_d = st.number_input("インナー並び縦(D)", value=2, key="a3_cqd")
        lb1, lb2, lb3 = st.columns(3)
        with lb1: c_plus_h = st.number_input("高さ(H)＋", value=10.0, step=0.1, format="%.1f", key="a3_cph")
        with lb2: c_plus_w = st.number_input("横幅(W)＋", value=10.0, step=0.1, format="%.1f", key="a3_cpw")
        with lb3: c_plus_d = st.number_input("縦(D)＋", value=10.0, step=0.1, format="%.1f", key="a3_cpd")
        g_d, g_w, g_h = (inn_d * cq_d) + c_plus_d, (inn_w * cq_w) + c_plus_w, (inn_h * cq_h) + c_plus_h
        total_qty = (cq_d * cq_w * cq_h) * i_qty
        total_kg = (total_qty * v_weight) / 1000.0
        st.info(f"カートン外寸: H{g_h:.1f} x W{g_w:.1f} x 縦(D){g_d:.1f}")
        st.metric("📦 カートン総入り数", f"{total_qty} 個"); st.metric("⚖️ 総重量", f"{total_kg:.1f} kg")
    with c6: draw_3d_box_with_size(inn_h, inn_w, inn_d, cq_h, cq_w, cq_d, "green", c_plus_d, c_plus_w, c_plus_h, is_main_chart=True)

elif start_point == "インナーサイズを直接入力":
    st.divider(); st.subheader("1️⃣ インナー入力")
    c1, c2 = st.columns(2)
    with c1:
        i_qty = st.number_input("入り数", value=10, key="b1_qty")
        v_weight = st.number_input("重量(g)", value=0.0, step=1.0, format="%.1f", key="b1_w")
        inn_h = st.number_input("インナー 高さ(H)", value=150.0, step=0.1, format="%.1f", key="b1_ih")
        inn_w = st.number_input("インナー 横幅(W)", value=200.0, step=0.1, format="%.1f", key="b1_iw")
        inn_d = st.number_input("インナー 縦(D)", value=100.0, step=0.1, format="%.1f", key="b1_id")
    with c2: draw_3d_box_with_size(inn_h, inn_w, inn_d, 1, 1, 1, "orange", 0, 0, 0, is_main_chart=True)
    
    st.subheader("2️⃣ カートン設計")
    c3, c4 = st.columns(2)
    with c3:
        cq_h = st.number_input("インナー積み数(H)", value=2, key="b2_cqh")
        cq_w = st.number_input("インナー並び横(W)", value=1, key="b2_cqw")
        cq_d = st.number_input("インナー並び縦(D)", value=2, key="b2_cqd")
        lb4, lb5, lb6 = st.columns(3)
        with lb4: b2_h_plus = st.number_input("高さ(H)＋", value=10.0, step=0.1, format="%.1f", key="b2_cph_val")
        with lb5: b2_w_plus = st.number_input("横幅(W)＋", value=10.0, step=0.1, format="%.1f", key="b2_cpw_val")
        with lb6: b2_d_plus = st.number_input("縦(D)＋", value=10.0, step=0.1, format="%.1f", key="b2_cpd_val")
        g_d, g_w, g_h = (inn_d * cq_d) + b2_d_plus, (inn_w * cq_w) + b2_w_plus, (inn_h * cq_h) + b2_h_plus
        total_qty = (cq_d * cq_w * cq_h) * i_qty
        total_kg = (total_qty * v_weight) / 1000.0
        st.info(f"カートン外寸: H{g_h:.1f} x W{g_w:.1f} x 縦(D){g_d:.1f}")
        st.metric("⚖️ 総重量", f"{total_kg:.1f} kg")
    with c4: draw_3d_box_with_size(inn_h, inn_w, inn_d, cq_h, cq_w, cq_d, "green", b2_d_plus, b2_w_plus, b2_h_plus, is_main_chart=True)

else:
    st.divider(); st.subheader("1️⃣ カートン直接入力")
    c1, c2 = st.columns(2)
    with c1:
        g_h = st.number_input("カートン 高さ(H)", value=320.0, step=0.1, format="%.1f", key="c1_gh")
        g_w = st.number_input("カートン 横幅(W)", value=420.0, step=0.1, format="%.1f", key="c1_gw")
        g_d = st.number_input("カートン 縦(D)", value=220.0, step=0.1, format="%.1f", key="c1_gd")
        total_qty = st.number_input("総入り数", value=20, key="c1_qty")
        total_kg = st.number_input("総重量(kg)", value=0.0, step=0.1, format="%.1f", key="c1_kg")
        st.info(f"カートン外寸: H{g_h:.1f} x W{g_w:.1f} x 縦(D){g_d:.1f}")
    with c2: draw_3d_box_with_size(g_h, g_w, g_d, 1, 1, 1, "green", 0, 0, 0, is_main_chart=True)

# ==========================================
# 4️⃣ パレット積載シミュレーション
# ==========================================
st.divider(); st.header("4️⃣ パレット積載シミュレーション")
l_orient = st.radio("底面を選択", [f"天天地地 (W{g_w:.1f}x縦(D){g_d:.1f})", f"横倒し (W{g_w:.1f}xH{g_h:.1f})", f"縦倒し (縦(D){g_d:.1f}xH{g_h:.1f})"], key="pal_orient")
if "天天地地" in l_orient: p_w, p_d, p_h = g_w, g_d, g_h
elif "横倒し" in l_orient: p_w, p_d, p_h = g_w, g_h, g_d
else: p_w, p_d, p_h = g_d, g_h, g_w

pal_size, h_limit = 1100.0, 1600.0
num_h = int(h_limit // p_h) if p_h > 0 else 0
pattern = st.selectbox("積み付け方", ["ブロック積み", "風車積み", "窓積み"], key="pal_patt")

boxes, cpl = [], 0
if pattern == "ブロック積み":
    nx = int(pal_size // p_w) if p_w > 0 else 0
    ny = int(pal_size // p_d) if p_d > 0 else 0
    off_x, off_y = (pal_size - nx*p_w)/2, (pal_size - ny*p_d)/2
    for i in range(nx):
        for j in range(ny): boxes.append((off_x + i*p_w, off_y + j*p_d, p_w, p_d)); cpl += 1
elif pattern == "風車積み":
    block_w, block_d = p_w + p_d, p_w + p_d
    off_x, off_y = (pal_size - block_w)/2, (pal_size - block_d)/2
    boxes = [(off_x, off_y, p_w, p_d), (off_x + p_w, off_y, p_d, p_w), (off_x + p_d, off_y + p_w, p_w, p_d), (off_x, off_y + p_d, p_d, p_w)]
    cpl = 4
else:
    boxes = [(0,0,p_w,p_d), (pal_size-p_w,0,p_w,p_d), (0,pal_size-p_d,p_w,p_d), (pal_size-p_w,pal_size-p_d,p_w,p_d)]; cpl = 4

col1, col2, col3 = st.columns([1, 0.8, 1])
with col1:
    st.write("#### 俯瞰図")
    fig_p, ax_p = plt.subplots(figsize=(5,5))
    ax_p.add_patch(patches.Rectangle((0, 0), pal_size, pal_size, color='gray', alpha=0.1))
    for b in boxes: ax_p.add_patch(patches.Rectangle((b[0], b[1]), b[2], b[3], edgecolor='black', facecolor='skyblue', alpha=0.8))
    if boxes:
        min_x, max_x = min(b[0] for b in boxes), max(b[0] + b[2] for b in boxes)
        min_y, max_y = min(b[1] for b in boxes), max(b[1] + b[3] for b in boxes)
        gap_l, gap_r, gap_f, gap_b = min_x, max(0.0, pal_size-max_x), min_y, max(0.0, pal_size-max_y)
        if gap_l > 5:
            ax_p.annotate('', xy=(0, pal_size/2), xytext=(min_x, pal_size/2), arrowprops=dict(arrowstyle='<->', color='red'))
            ax_p.text(gap_l/2, pal_size/2, f'{gap_l:.1f}', color='red', fontsize=9, fontweight='bold', ha='center', backgroundcolor='white')
        if gap_r > 5:
            ax_p.annotate('', xy=(max_x, pal_size/2), xytext=(pal_size, pal_size/2), arrowprops=dict(arrowstyle='<->', color='red'))
            ax_p.text(pal_size - gap_r/2, pal_size/2, f'{gap_r:.1f}', color='red', fontsize=9, fontweight='bold', ha='center', backgroundcolor='white')
        if gap_f > 5:
            ax_p.annotate('', xy=(pal_size/2, 0), xytext=(pal_size/2, min_y), arrowprops=dict(arrowstyle='<->', color='red'))
            ax_p.text(pal_size/2, gap_f/2, f'{gap_f:.1f}', color='red', fontsize=9, fontweight='bold', va='center', backgroundcolor='white')
        if gap_b > 5:
            ax_p.annotate('', xy=(pal_size/2, max_y), xytext=(pal_size/2, pal_size), arrowprops=dict(arrowstyle='<->', color='red'))
            ax_p.text(pal_size/2, pal_size - gap_b/2, f'{gap_b:.1f}', color='red', fontsize=9, fontweight='bold', va='center', backgroundcolor='white')
    ax_p.set_xlim(-50, pal_size+50); ax_p.set_ylim(-50, pal_size+50); ax_p.set_aspect('equal'); ax_p.axis('off'); st.pyplot(fig_p)

with col2:
    st.write("#### 側面図")
    fig_s, ax_s = plt.subplots(figsize=(4, 5))
    ax_s.axhline(h_limit, color='red', linestyle='--')
    for i in range(num_h): ax_s.add_patch(patches.Rectangle((100, i*p_h), 300, p_h, edgecolor='black', facecolor='lightgreen', alpha=0.7))
    ax_s.set_xlim(0, 500); ax_s.set_ylim(0, h_limit + 100); ax_s.set_xticks([]); ax_s.set_yticks([]); st.pyplot(fig_s)

with col3:
    st.subheader("📊 積載データ")
    st.metric("📦 パレット総数", f"{cpl * num_h} 箱 ({num_h}段)")
    st.metric("⚖️ パレット総重量", f"{(cpl * num_h) * total_kg:.1f} kg")
    if boxes:
        min_x, max_x = min(b[0] for b in boxes), max(b[0] + b[2] for b in boxes)
        min_y, max_y = min(b[1] for b in boxes), max(b[1] + b[3] for b in boxes)
        st.divider(); st.markdown("### 📏 パレットの隙間 (mm)")
        st.write(f"**左:** {min_x:.1f} / **右:** {max(0.0, pal_size - max_x):.1f}")
        st.write(f"**手前:** {min_y:.1f} / **奥:** {max(0.0, pal_size - max_y):.1f}")
        if max_x > pal_size or max_y > pal_size: st.error("⚠️ はみ出し注意")
        else: st.success("✅ 正常積載")
        st.info(f"積載高さ: {int(num_h * p_h)} mm")
