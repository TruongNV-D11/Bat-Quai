import streamlit as st
import streamlit.components.v1 as components
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import time as time_mod
from datetime import datetime, time as dt_time

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v21.5",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f0f6fc; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

st.title("☸️ PROFESSIONAL FENG SUI MASTER BAGUA ENGINE v21.5")

# --- 1. DỮ LIỆU HỌC THUẬT: 24 SƠN HƯỚNG ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

SON_HUONG_24 = [
    {"name": "Nhâm", "deg_start": 337.5, "deg_end": 352.5, "elem": "Thủy", "dir": "Bắc", "yuan": 0, "pol": 1},
    {"name": "Tý",   "deg_start": 352.5, "deg_end": 7.5,   "elem": "Thủy", "dir": "Bắc", "yuan": 1, "pol": -1},
    {"name": "Quý",  "deg_start": 7.5,   "deg_end": 22.5,  "elem": "Thủy", "dir": "Bắc", "yuan": 2, "pol": -1},
    {"name": "Cấn",  "deg_start": 22.5,  "deg_end": 37.5,  "elem": "Thổ",  "dir": "Đông Bắc", "yuan": 0, "pol": 1},
    {"name": "Sửu",  "deg_start": 37.5,  "deg_end": 52.5,  "elem": "Thổ",  "dir": "Đông Bắc", "yuan": 1, "pol": -1},
    {"name": "Dần",  "deg_start": 52.5,  "deg_end": 67.5,  "elem": "Mộc",  "dir": "Đông Bắc", "yuan": 2, "pol": -1},
    {"name": "Giáp", "deg_start": 67.5,  "deg_end": 82.5,  "elem": "Mộc",  "dir": "Đông", "yuan": 0, "pol": 1},
    {"name": "Mão",  "deg_start": 82.5,  "deg_end": 97.5,  "elem": "Mộc",  "dir": "Đông", "yuan": 1, "pol": -1},
    {"name": "Ất",   "deg_start": 97.5,  "deg_end": 112.5, "elem": "Mộc",  "dir": "Đông", "yuan": 2, "pol": -1},
    {"name": "Tốn",  "deg_start": 112.5, "deg_end": 127.5, "elem": "Mộc",  "dir": "Đông Nam", "yuan": 0, "pol": 1},
    {"name": "Thìn", "deg_start": 127.5, "deg_end": 142.5, "elem": "Thổ",  "dir": "Đông Nam", "yuan": 1, "pol": -1},
    {"name": "Tỵ",   "deg_start": 142.5, "deg_end": 157.5, "elem": "Hỏa",  "dir": "Đông Nam", "yuan": 2, "pol": -1},
    {"name": "Bính", "deg_start": 157.5, "deg_end": 172.5, "elem": "Hỏa",  "dir": "Nam", "yuan": 0, "pol": 1},
    {"name": "Ngọ",  "deg_start": 172.5, "deg_end": 187.5, "elem": "Hỏa",  "dir": "Nam", "yuan": 1, "pol": -1},
    {"name": "Đinh", "deg_start": 187.5, "deg_end": 202.5, "elem": "Hỏa",  "dir": "Nam", "yuan": 2, "pol": -1},
    {"name": "Khôn", "deg_start": 202.5, "deg_end": 217.5, "elem": "Thổ",  "dir": "Tây Nam", "yuan": 0, "pol": 1},
    {"name": "Mùi",  "deg_start": 217.5, "deg_end": 232.5, "elem": "Thổ",  "dir": "Tây Nam", "yuan": 1, "pol": -1},
    {"name": "Thân", "deg_start": 232.5, "deg_end": 247.5, "elem": "Kim",  "dir": "Tây Nam", "yuan": 2, "pol": -1},
    {"name": "Canh", "deg_start": 247.5, "deg_end": 262.5, "elem": "Kim",  "dir": "Tây", "yuan": 0, "pol": 1},
    {"name": "Dậu",  "deg_start": 262.5, "deg_end": 277.5, "elem": "Kim",  "dir": "Tây", "yuan": 1, "pol": -1},
    {"name": "Tân",  "deg_start": 277.5, "deg_end": 292.5, "elem": "Kim",  "dir": "Tây", "yuan": 2, "pol": -1},
    {"name": "Càn",  "deg_start": 292.5, "deg_end": 307.5, "elem": "Kim",  "dir": "Tây Bắc", "yuan": 0, "pol": 1},
    {"name": "Tuất", "deg_start": 307.5, "deg_end": 322.5, "elem": "Thổ",  "dir": "Tây Bắc", "yuan": 1, "pol": -1},
    {"name": "Hợi",  "deg_start": 322.5, "deg_end": 337.5, "elem": "Thủy", "dir": "Tây Bắc", "yuan": 2, "pol": -1},
]

LO_SHU_BASE = {
    "Bắc": 1, "Tây Nam": 2, "Đông": 3, "Đông Nam": 4,
    "Trung Cung": 5, "Tây Bắc": 6, "Tây": 7, "Đông Bắc": 8, "Nam": 9
}

DIRECTION_ANGLES = {
    "Bắc": 0.0, "Đông Bắc": 45.0, "Đông": 90.0, "Đông Nam": 135.0,
    "Nam": 180.0, "Tây Nam": 225.0, "Tây": 270.0, "Tây Bắc": 315.0
}

def tinh_van_huyen_khong(nam_nhap_trach):
    return (((nam_nhap_trach - 1864) // 20) % 9) + 1

def phi_tinh_9_cung(center_star, direction=1):
    matrix = {}
    for dir_name, base_val in LO_SHU_BASE.items():
        steps = (base_val - 5) % 9
        matrix[dir_name] = ((center_star - 1 + direction * steps) % 9) + 1
    return matrix

def get_son_by_degree(deg):
    deg = deg % 360.0
    for son in SON_HUONG_24:
        if son["deg_start"] > son["deg_end"]:
            if deg >= son["deg_start"] or deg < son["deg_end"]:
                return son
        else:
            if son["deg_start"] <= deg < son["deg_end"]:
                return son
    return SON_HUONG_24[1]

def compute_full_xuan_kong_chart(van_num, facing_deg):
    sitting_deg = (facing_deg + 180.0) % 360.0
    facing_son = get_son_by_degree(facing_deg)
    sitting_son = get_son_by_degree(sitting_deg)
    
    van_chart = phi_tinh_9_cung(van_num, direction=1)
    son_center = van_chart[sitting_son["dir"]]
    son_dir = sitting_son["pol"] if son_center == 5 else (1 if sitting_son["yuan"] == 0 else -1)
    son_chart = phi_tinh_9_cung(son_center, direction=son_dir)
    
    huong_center = van_chart[facing_son["dir"]]
    huong_dir = facing_son["pol"] if huong_center == 5 else (1 if huong_center["yuan"] == 0 else -1)
    huong_chart = phi_tinh_9_cung(huong_center, direction=huong_dir)
    
    full_palaces = {p_name: {"van": van_chart[p_name], "son": son_chart[p_name], "huong": huong_chart[p_name]} for p_name in LO_SHU_BASE.keys()}
    return {
        "sitting_son": sitting_son, "facing_son": facing_son,
        "sitting_deg": sitting_deg, "facing_deg": facing_deg,
        "palaces": full_palaces,
        "cach_cuc": "🌟 VƯỢNG SƠN VƯỢNG HƯỚNG", "cach_cuc_desc": "Đương lệnh Sơn tinh đáo Tọa, Hướng tinh đáo Hướng."
    }

def get_annual_monthly_stars(survey_year, survey_month):
    annual_center = ((1 - (survey_year - 2026) - 1) % 9) + 1
    annual_chart = phi_tinh_9_cung(annual_center, direction=1)
    chi_idx = (survey_year - 1984) % 12
    m1_star = 8 if chi_idx in [0, 3, 6, 9] else (5 if chi_idx in [1, 4, 7, 10] else 2)
    monthly_center = ((m1_star - (survey_month - 1) - 1) % 9) + 1
    monthly_chart = phi_tinh_9_cung(monthly_center, direction=1)
    return annual_center, annual_chart, monthly_center, monthly_chart

BAT_TRACH_MAPPING = {
    1: {
        "Bắc": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☰", "name": "CÀN"}
    },
    9: {
        "Bắc": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☰", "name": "CÀN"}
    },
    3: {
        "Bắc": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☰", "name": "CÀN"}
    },
    4: {
        "Bắc": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☰", "name": "CÀN"}
    },
    6: {
        "Bắc": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☰", "name": "CÀN"}
    },
    2: {
        "Bắc": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☰", "name": "CÀN"}
    },
    7: {
        "Bắc": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☰", "name": "CÀN"}
    },
    8: {
        "Bắc": {"cat_hung": "Ngũ Quỷ", "color": "#da3633", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Phục Vị", "color": "#1f6feb", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hại", "color": "#9e6a03", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Tuyệt Mệnh", "color": "#8b0000", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "color": "#6e7681", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Sinh Khí", "color": "#2ea043", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Diên Niên", "color": "#238636", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Thiên Y", "color": "#58a6ff", "trigram": "☰", "name": "CÀN"}
    }
}

def get_can_chi_academic(solar_date, solar_time, has_time):
    year = solar_date.year
    month = solar_date.month
    day = solar_date.day
    eff_year = year
    if month < 2 or (month == 2 and day < 4):
        eff_year -= 1
    elif month == 2 and day == 4 and has_time and solar_time:
        if solar_time < dt_time(4, 14):
            eff_year -= 1
    offset = (eff_year - 1984) % 60
    return CAN[offset % 10], CHI[offset % 12], eff_year

def compute_master_cung_phi(solar_date, solar_time, has_time, sex):
    can, chi, eff_year = get_can_chi_academic(solar_date, solar_time, has_time)
    sum_digits = sum(int(c) for c in str(eff_year))
    while sum_digits > 9:
        sum_digits = sum(int(c) for c in str(sum_digits))
    val = (11 - sum_digits) if sex == "Nam" else (sum_digits + 4)
    if eff_year >= 2000:
        val = (9 - sum_digits) if sex == "Nam" else (sum_digits + 6)
    quai_num = val % 9
    if quai_num == 0: quai_num = 9
    if quai_num == 5: quai_num = 2 if sex == "Nam" else 8
    group = "Đông Tứ Mệnh" if quai_num in [1, 3, 4, 9] else "Tây Tứ Mệnh"
    return can, chi, eff_year, quai_num, group

# --- GIAO DIỆN NHẬP LIỆU ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False

with st.sidebar:
    st.header("🛠️ THAM SỐ LẬP QUẺ")
    d_input = st.date_input("Ngày sinh", value=datetime(1984, 9, 17), format="DD/MM/YYYY")
    enable_time = st.checkbox("Giờ sinh", value=True)
    t_input = st.time_input("Giờ", value=dt_time(8, 30)) if enable_time else None
    gender = st.selectbox("Giới tính", ["Nam", "Nữ"], index=1)
    
    build_year = st.number_input("Năm Nhập Trạch", min_value=1864, max_value=2100, value=2026)
    current_van = tinh_van_huyen_khong(build_year)
    survey_year = st.number_input("Năm Lưu Niên", min_value=1900, max_value=2100, value=2026)
    survey_month = st.selectbox("Tháng", list(range(1, 13)), index=10)
    
    exact_deg = st.number_input("Số độ Hướng nhà", min_value=0.0, max_value=360.0, value=45.0, step=0.5)
    show_laser = st.checkbox("Hiển thị Tia Hướng", value=True)
    
    if st.button("🔮 Lập Bản Đồ", type="primary"):
        st.session_state.initialized = True

def render_matplotlib_lakinh(quai_num, exact_deg_val, show_laser_flag, gender_str, eff_year, van_num, xk_chart, annual_chart, monthly_chart):
    fig, ax = plt.subplots(figsize=(8.6, 8.6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    mapping = BAT_TRACH_MAPPING[quai_num]
    
    def get_text_rotation(angle_deg):
        rot = -angle_deg
        if 90 < angle_deg <= 270:
            rot += 180
        return rot

    # 1. TẦNG BÁT TRẠCH & HẬU THIÊN (ĐỒNG NHẤT GÓC TÂM ±22.5°)
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        
        ax.bar(bar_start, width=np.radians(45), bottom=0.68, height=0.17, color=info["color"], alpha=0.9, edgecolor='white', linewidth=1.1, zorder=2)
        ax.text(rad, 0.765, info['cat_hung'], color='white', fontsize=8.5, fontweight='bold', ha='center', va='center', rotation=get_text_rotation(angle), rotation_mode='anchor', zorder=3)
                
        ax.bar(bar_start, width=np.radians(45), bottom=0.85, height=0.17, color='#1f242c', alpha=0.95, edgecolor='#30363d', linewidth=1.0, zorder=2)
        ax.text(rad, 0.935, f"{info['trigram']} {info['name']}", color='#f0f6fc', fontsize=8.0, fontweight='bold', ha='center', va='center', rotation=get_text_rotation(angle), rotation_mode='anchor', zorder=3)
                
    # 2. 24 SƠN HƯỚNG & NẠP ÂM (ĐỒNG NHẤT GÓC BẮT ĐẦU)
    for son in SON_HUONG_24:
        mid_deg = ((son["deg_start"] + son["deg_end"]) / 2) % 360
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        rot_son = get_text_rotation(mid_deg)
        
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.02, height=0.20, color='#161b22', alpha=0.9, edgecolor='#30363d', linewidth=0.8, zorder=2)
        ax.text(rad_son, 1.12, son['name'], color='#58a6ff', fontsize=8.5, fontweight='bold', ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)
                
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.22, height=0.16, color='#0d1117', alpha=0.9, edgecolor='#30363d', linewidth=0.6, zorder=2)
        ax.text(rad_son, 1.30, son['elem'], color='#c9d1d9', fontsize=7.2, fontweight='bold', ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)

    # 3. 120 PHÂN KIM
    for son in SON_HUONG_24:
        for slot in range(5):
            slot_start = (son["deg_start"] + slot * 3.0) % 360.0
            slot_mid = (slot_start + 1.5) % 360.0
            pk_color = '#2ea043' if slot == 2 else ('#1f6feb' if slot in [1, 3] else '#30363d')
            ax.bar(np.radians(slot_start), width=np.radians(3.0), bottom=1.38, height=0.07, color=pk_color, alpha=0.9, edgecolor='#0b0f19', linewidth=0.4, zorder=2)

    # 4. VÒNG CHIA ĐỘ
    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        line_len = 0.04 if d_tick % 15 == 0 else (0.025 if d_tick % 5 == 0 else 0.012)
        col = '#FFD700' if d_tick % 15 == 0 else ('white' if d_tick % 5 == 0 else '#6e7681')
        ax.plot([rad_t, rad_t], [1.45, 1.45 + line_len], color=col, lw=1.2 if d_tick % 15 == 0 else 0.4, zorder=2)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.58, f"{d_tick}°", color='#c9d1d9', fontsize=7.5, ha='center', va='center', zorder=3)

    # 5. 2 VÒNG TRONG CÙNG (ĐỒNG NHẤT GÓC TÂM ±22.5°, KHỚP 100% CÁC CUNG BÊN NGOÀI)
    for dir_name, angle in DIRECTION_ANGLES.items():
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        rot_angle = get_text_rotation(angle)
        
        y_star = annual_chart[dir_name]
        m_star = monthly_chart[dir_name]
        ax.bar(bar_start, width=np.radians(45), bottom=0.48, height=0.20, color='#161f2f', alpha=0.98, edgecolor='#30363d', linewidth=1.2, zorder=10)
        ym_color = '#ff7b72' if y_star in [2, 5] else ('#3fb950' if y_star in [1, 8, 9] else '#d2a8ff')
        ax.text(rad, 0.58, f"N:{y_star} | T:{m_star}", color=ym_color, fontsize=7.8, fontweight='bold', ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=11)

        p_info = xk_chart["palaces"][dir_name]
        ax.bar(bar_start, width=np.radians(45), bottom=0.28, height=0.20, color='#0f172a', alpha=0.98, edgecolor='#30363d', linewidth=1.2, zorder=10)
        ax.text(rad, 0.38, f"S:{p_info['son']} H:{p_info['huong']}\n[V:{p_info['van']}]", color='#38bdf8', fontsize=7.5, fontweight='bold', ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=11)

    # Thập tự & Tia laser
    ax.plot([0, np.pi], [1.45, 1.45], color='#ff7b72', linestyle='--', lw=1.1, alpha=0.75, zorder=15)
    ax.plot([np.pi/2, 3*np.pi/2], [1.45, 1.45], color='#58a6ff', linestyle='--', lw=1.1, alpha=0.75, zorder=15)
    
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        ax.annotate('', xy=(fac_rad, 1.47), xytext=(0, 0), arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.0, width=1.8, headwidth=8), zorder=18)
        ax.plot([0, sit_rad], [0, 1.45], color='#FFD700', linestyle=':', lw=1.8, alpha=0.9, zorder=17)
                    
    ax.fill([0, 0.15, np.pi, -0.15], [0.55, 0.06, 0, 0.06], color='#FF3333', alpha=0.5, zorder=20)
    ax.fill([np.pi, np.pi - 0.15, 0, np.pi + 0.15], [0.55, 0.06, 0, 0.06], color='#E0E0E0', alpha=0.4, zorder=20)
    ax.scatter([0], [0], color='#FFD700', s=25, zorder=21, edgecolors='black', linewidth=0.5)
    
    ax.text(0, 0, f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str} ({eff_year})", color='#ff7b72', fontsize=7.2, fontweight='bold', ha='center', va='center', zorder=22, bbox=dict(boxstyle='round,pad=0.25', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.4))
            
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='#30363d', linestyle='--', linewidth=0.8)
    ax.spines['polar'].set_color('#8b949e')
    plt.tight_layout()
    return fig

# --- HIỂN THỊ KẾT QUẢ ---
if st.session_state.initialized:
    can, chi, eff_year, quai_num, group_name = compute_master_cung_phi(d_input, t_input, enable_time, gender)
    xk_chart = compute_full_xuan_kong_chart(current_van, exact_deg)
    ann_center, annual_chart, mon_center, monthly_chart = get_annual_monthly_stars(survey_year, survey_month)
    
    col_left, col_right = st.columns([1.25, 1.75])
    with col_left:
        st.subheader("📋 Báo cáo Khí số")
        st.metric("Can Chi", f"{can} {chi} ({eff_year})")
        st.metric("Nhóm Mệnh", group_name)
    with col_right:
        st.subheader("🧭 Đồ họa La Kinh v21.5")
        fig_mpl = render_matplotlib_lakinh(quai_num, exact_deg, show_laser, gender, eff_year, current_van, xk_chart, annual_chart, monthly_chart)
        st.pyplot(fig_mpl)
else:
    st.info("👈 Vui lòng bấm **'🔮 Lập Bản Đồ'** ở thanh bên trái.")
