import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, time

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v5.0",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f0f6fc; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; }
    .signature-box { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        padding: 10px; 
        border-radius: 6px; 
        font-size: 12px; 
        color: #8b949e; 
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☸️ PROFESSIONAL FENG SHUI MASTER BAGUA ENGINE")
st.markdown("Hệ thống lập bản đồ Khí số chuyên sâu: 24 Sơn Hướng, Bát Trạch Cát Hung đa tầng và Định vị La Kinh chuẩn thực địa.")

# --- 1. DỮ LIỆU HỌC THUẬT LỤC THẬP HOA GIÁP & 24 SƠN HƯỚNG ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

SON_HUONG_24 = [
    {"name": "Nhâm", "deg_start": 337.5, "deg_end": 352.5},
    {"name": "Tý", "deg_start": 352.5, "deg_end": 7.5},
    {"name": "Quý", "deg_start": 7.5, "deg_end": 22.5},
    {"name": "Cấn", "deg_start": 22.5, "deg_end": 37.5},
    {"name": "Sửu", "deg_start": 37.5, "deg_end": 52.5},
    {"name": "Dần", "deg_start": 52.5, "deg_end": 67.5},
    {"name": "Giáp", "deg_start": 67.5, "deg_end": 82.5},
    {"name": "Mão", "deg_start": 82.5, "deg_end": 97.5},
    {"name": "Ất", "deg_start": 97.5, "deg_end": 112.5},
    {"name": "Tốn", "deg_start": 112.5, "deg_end": 127.5},
    {"name": "Thìn", "deg_start": 127.5, "deg_end": 142.5},
    {"name": "Tỵ", "deg_start": 142.5, "deg_end": 157.5},
    {"name": "Bính", "deg_start": 157.5, "deg_end": 172.5},
    {"name": "Ngọ", "deg_start": 172.5, "deg_end": 187.5},
    {"name": "Đinh", "deg_start": 187.5, "deg_end": 202.5},
    {"name": "Khôn", "deg_start": 202.5, "deg_end": 217.5},
    {"name": "Mùi", "deg_start": 217.5, "deg_end": 232.5},
    {"name": "Thân", "deg_start": 232.5, "deg_end": 247.5},
    {"name": "Canh", "deg_start": 247.5, "deg_end": 262.5},
    {"name": "Dậu", "deg_start": 262.5, "deg_end": 277.5},
    {"name": "Tân", "deg_start": 277.5, "deg_end": 292.5},
    {"name": "Càn", "deg_start": 292.5, "deg_end": 307.5},
    {"name": "Tuất", "deg_start": 307.5, "deg_end": 322.5},
    {"name": "Hợi", "deg_start": 322.5, "deg_end": 337.5},
]

def get_can_chi_academic(solar_date, solar_time, has_time):
    year = solar_date.year
    month = solar_date.month
    day = solar_date.day
    
    effective_year = year
    if month < 2 or (month == 2 and day < 4):
        effective_year -= 1
    elif month == 2 and day == 4 and has_time and solar_time:
        if solar_time < time(4, 14):
            effective_year -= 1

    offset = (effective_year - 1984) % 60
    can_idx = offset % 10
    chi_idx = offset % 12
    return CAN[can_idx], CHI[chi_idx], effective_year

def compute_master_cung_phi(solar_date, solar_time, has_time, sex):
    can, chi, eff_year = get_can_chi_academic(solar_date, solar_time, has_time)
    
    sum_digits = sum(int(char) for char in str(eff_year))
    while sum_digits > 9:
        sum_digits = sum(int(char) for char in str(sum_digits))
        
    if eff_year < 2000:
        val_nam = 11 - sum_digits
        val_nu = sum_digits + 4
    else:
        val_nam = 9 - sum_digits
        val_nu = sum_digits + 6
        
    def normalize_val(v, s):
        v = v % 9
        if v == 0: v = 9
        if v == 5:
            return 2 if s == "Nam" else 8
        return v

    quai_num = normalize_val(val_nam if sex == "Nam" else val_nu, sex)
    
    bagua_map = {
        1: {"name": "KHẢM", "element": "Thủy", "dir": "CHÍNH BẮC", "angle": 0, "trigram": "☵", "palace": "Khảm Quái", "group": "Đông Tứ Mệnh", "color": "#1f6feb"},
        8: {"name": "CẤN", "element": "Thổ", "dir": "ĐÔNG BẮC", "angle": 45, "trigram": "☶", "palace": "Cấn Quái", "group": "Tây Tứ Mệnh", "color": "#d29922"},
        3: {"name": "CHẤN", "element": "Mộc", "dir": "CHÍNH ĐÔNG", "angle": 90, "trigram": "☳", "palace": "Chấn Quái", "group": "Đông Tứ Mệnh", "color": "#238636"},
        4: {"name": "TỐN", "element": "Mộc", "dir": "ĐÔNG NAM", "angle": 135, "trigram": "☴", "palace": "Tốn Quái", "group": "Đông Tứ Mệnh", "color": "#2ea043"},
        9: {"name": "LY", "element": "Hỏa", "dir": "CHÍNH NAM", "angle": 180, "trigram": "☲", "palace": "Ly Quái", "group": "Đông Tứ Mệnh", "color": "#da3633"},
        2: {"name": "KHÔN", "element": "Thổ", "dir": "TÂY NAM", "angle": 225, "trigram": "☷", "palace": "Khôn Quái", "group": "Tây Tứ Mệnh", "color": "#9e6a03"},
        7: {"name": "ĐOÀI", "element": "Kim", "dir": "CHÍNH TÂY", "angle": 270, "trigram": "☱", "palace": "Đoài Quái", "group": "Tây Tứ Mệnh", "color": "#8957e5"},
        6: {"name": "CÀN", "element": "Kim", "dir": "TÂY BẮC", "angle": 315, "trigram": "☰", "palace": "Càn Quái", "group": "Tây Tứ Mệnh", "color": "#6e7681"}
    }
    return can, chi, eff_year, quai_num, bagua_map

# --- 2. GIAO DIỆN NHẬP LIỆU & SESSION STATE ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False

with st.sidebar:
    st.header("🛠️ THAM SỐ LẬP QUẺ (MASTER)")
    
    d_input = st.date_input(
        "Ngày sinh (Dương lịch)", 
        value=datetime(1990, 5, 15),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31),
        format="DD/MM/YYYY"
    )
    
    enable_time = st.checkbox("Kích hoạt Giờ sinh chính xác", value=True)
    t_input = None
    if enable_time:
        t_input = st.time_input("Giờ:Phút sinh", value=time(8, 30))
        
    gender = st.selectbox("Giới tính gia chủ", ["Nam", "Nữ"])
    current_yun = st.selectbox("Tam Nguyên Cửu Vận (Vận tinh)", ["Vận 9 (2024-2043)", "Vận 8 (2004-2023)"], index=0)
    
    if st.button("🔮 Lập Bản Đồ La Kinh Chuyên Sâu", type="primary", use_container_width=True):
        st.session_state.initialized = True

    st.markdown("""
        <div class="signature-box">
            <b>DIGITAL SIGNATURE</b><br>
            <b>Engineer:</b> TruongfNV<br>
            <b>Email:</b> truongnv.d11@gmail.com<br>
            <b>Hotline:</b> 0919855966<br>
            <i>System: Master Bagua Engine v5.0</i>
        </div>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ LA KINH BẰNG MATPLOTLIB (CHẮC CHẮN HIỂN THỊ) ---
def render_matplotlib_lakinh(active_num, data_map, gender_str, eff_year_val):
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')

    # Thiết lập hướng Bắc lên trên (0 độ) và chiều kim đồng hồ
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # 1. Vẽ vòng 8 cung Quái vị (bán kính từ 0.4 đến 0.9)
    angles_bagua = [0, 45, 90, 135, 180, 225, 270, 315]
    for q_id, info in data_map.items():
        deg = info["angle"]
        rad = np.radians(deg)
        is_active = (q_id == active_num)
        color = "#f85149" if is_active else info["color"]

        # Vẽ ô màu sector cho quái vị
        ax.bar(rad, width=np.radians(45), bottom=0.35, height=0.55, 
               color=color, alpha=0.9, edgecolor='white', linewidth=1.5)

        # Đặt chữ quái vị
        text_label = f"{info['trigram']}\n{info['name']}"
        ax.text(rad, 0.62, text_label, color='white', fontsize=11, fontweight='bold',
                ha='center', va='center')

    # 2. Vẽ vòng 24 Sơn Hướng ngoài cùng (bán kính từ 0.9 đến 1.3)
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)

        ax.bar(rad_son, width=np.radians(15), bottom=0.9, height=0.4,
               color='#161b22', alpha=0.8, edgecolor='#30363d', linewidth=0.8)
        
        ax.text(rad_son, 1.12, son['name'], color='#f0f6fc', fontsize=10,
                ha='center', va='center')

    # 3. Vòng độ số góc (Degree markers ngoài cùng)
    for deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = np.radians(deg)
        ax.text(rad, 1.42, f"{deg}°", color='#8b949e', fontsize=9, ha='center', va='center')

    # 4. Trung Cung (Tâm)
    active_info = data_map[active_num]
    center_text = f"TRUNG CUNG\n{gender_str} ({eff_year_val})\nQuẻ: {active_info['name']}\n({active_info['group']})"
    ax.text(0, 0, center_text, color='#ff7b72', fontsize=9, fontweight='bold',
            ha='center', va='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.5))

    # Tinh chỉnh giao diện trục polar
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='#30363d', linestyle='--', linewidth=1)
    ax.spines['polar'].set_color('#8b949e')

    plt.tight_layout()
    return fig

# --- 4. HIỂN THỊ KẾT QUẢ ---
if st.session_state.initialized:
    can, chi, eff_year, quai_num, bagua_dict = compute_master_cung_phi(d_input, t_input, enable_time, gender)
    target_data = bagua_dict[quai_num]

    col_left, col_right = st.columns([1.3, 1.7])

    with col_left:
        st.subheader("📋 Báo cáo Khí số Chuyên môn")
        st.metric("Ngày sinh ghi nhận", d_input.strftime("%d/%m/%Y"))
        st.metric("Can Chi Niên Mệnh", f"Năm {can} {chi} ({eff_year})")
        if enable_time and t_input:
            st.metric("Thời khắc Lập xuân / Giờ sinh", t_input.strftime("%H:%M"))
        st.metric("Cung Mệnh (Bát Trạch)", f"{target_data['palace']} - {target_data['name']}")
        st.metric("Ngũ Hành Bản Mệnh", target_data['element'])
        st.metric("Phương vị Chủ đạo", target_data['dir'])
        st.metric("Nhóm Mệnh", target_data['group'])
        st.metric("Vận tinh áp dụng", current_yun)
        
        st.info("🎯 **Chuẩn học thuật Thầy pháp:** Bản đồ hiển thị đầy đủ vòng 24 sơn hướng, khối màu phong thủy Bát Trạch trực quan và tọa độ Trung Cung.")

    with col_right:
        st.subheader("🧭 Đồ họa La Kinh Màu Sắc Đa Tầng")
        fig_mpl = render_matplotlib_lakinh(quai_num, bagua_dict, gender, eff_year)
        st.pyplot(fig_mpl)
else:
    st.info("👈 **Vui lòng nhập thông số cá nhân ở thanh bên trái và bấm nút '🔮 Lập Bản Đồ La Kinh Chuyên Sâu' để khởi tạo đồ họa hiển thị.**")
