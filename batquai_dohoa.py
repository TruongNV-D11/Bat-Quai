import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np
import time as time_mod
from datetime import datetime, time as dt_time

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v20.0",
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
    .advice-box {
        background-color: #161b22;
        border-left: 4px solid #58a6ff;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☸️ PROFESSIONAL FENG SUI MASTER BAGUA ENGINE v20.0")
st.markdown("Hệ thống lập bản đồ Khí số chuyên nghiệp thực chiến: Tự động hóa Tam Nguyên Cửu Vận, Bát Trạch 8 Quẻ Mệnh, La Kinh 5 Tầng và Vạch chia độ chuẩn xác.")

# --- 1. DỮ LIỆU HỌC THUẬT: 24 SƠN HƯỚNG & MA TRẬN 9 VẬN HUYỀN KHÔNG PHI TINH ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

SON_HUONG_24 = [
    {"name": "Nhâm", "deg_start": 337.5, "deg_end": 352.5, "elem": "Thủy", "dir": "Bắc"},
    {"name": "Tý", "deg_start": 352.5, "deg_end": 7.5, "elem": "Thủy", "dir": "Bắc"},
    {"name": "Quý", "deg_start": 7.5, "deg_end": 22.5, "elem": "Thủy", "dir": "Bắc"},
    {"name": "Cấn", "deg_start": 22.5, "deg_end": 37.5, "elem": "Thổ", "dir": "Đông Bắc"},
    {"name": "Sửu", "deg_start": 37.5, "deg_end": 52.5, "elem": "Thổ", "dir": "Đông Bắc"},
    {"name": "Dần", "deg_start": 52.5, "deg_end": 67.5, "elem": "Mộc", "dir": "Đông Bắc"},
    {"name": "Giáp", "deg_start": 67.5, "deg_end": 82.5, "elem": "Mộc", "dir": "Đông"},
    {"name": "Mão", "deg_start": 82.5, "deg_end": 97.5, "elem": "Mộc", "dir": "Đông"},
    {"name": "Ất", "deg_start": 97.5, "deg_end": 112.5, "elem": "Mộc", "dir": "Đông"},
    {"name": "Tốn", "deg_start": 112.5, "deg_end": 127.5, "elem": "Mộc", "dir": "Đông Nam"},
    {"name": "Thìn", "deg_start": 127.5, "deg_end": 142.5, "elem": "Thổ", "dir": "Đông Nam"},
    {"name": "Tỵ", "deg_start": 142.5, "deg_end": 157.5, "elem": "Hỏa", "dir": "Đông Nam"},
    {"name": "Bính", "deg_start": 157.5, "deg_end": 172.5, "elem": "Hỏa", "dir": "Nam"},
    {"name": "Ngọ", "deg_start": 172.5, "deg_end": 187.5, "elem": "Hỏa", "dir": "Nam"},
    {"name": "Đinh", "deg_start": 187.5, "deg_end": 202.5, "elem": "Hỏa", "dir": "Nam"},
    {"name": "Khôn", "deg_start": 202.5, "deg_end": 217.5, "elem": "Thổ", "dir": "Tây Nam"},
    {"name": "Mùi", "deg_start": 217.5, "deg_end": 232.5, "elem": "Thổ", "dir": "Tây Nam"},
    {"name": "Thân", "deg_start": 232.5, "deg_end": 247.5, "elem": "Kim", "dir": "Tây Nam"},
    {"name": "Canh", "deg_start": 247.5, "deg_end": 262.5, "elem": "Kim", "dir": "Tây"},
    {"name": "Dậu", "deg_start": 262.5, "deg_end": 277.5, "elem": "Kim", "dir": "Tây"},
    {"name": "Tân", "deg_start": 277.5, "deg_end": 292.5, "elem": "Kim", "dir": "Tây"},
    {"name": "Càn", "deg_start": 292.5, "deg_end": 307.5, "elem": "Kim", "dir": "Tây Bắc"},
    {"name": "Tuất", "deg_start": 307.5, "deg_end": 322.5, "elem": "Thổ", "dir": "Tây Bắc"},
    {"name": "Hợi", "deg_start": 322.5, "deg_end": 337.5, "elem": "Thủy", "dir": "Tây Bắc"},
]

STAR_NAMES = {
    1: "Nhất Bạch (1)", 2: "Nhị Hắc (2)", 3: "Tam Bích (3)", 
    4: "Tứ Lục (4)", 5: "Ngũ Hoàng (5)", 6: "Lục Bạch (6)", 
    7: "Thất Xích (7)", 8: "Bát Bạch (8)", 9: "Cửu Tử (9)"
}

def tinh_van_huyen_khong(nam_nhap_trach):
    khoang_cach = (nam_nhap_trach - 1864) // 20
    van = (khoang_cach % 9) + 1
    return van

def get_fly_star_matrix(van_num):
    base_map = {
        "Bắc": 1, "Tây Nam": 2, "Đông": 3, "Đông Nam": 4, 
        "Trung Cung": 5, "Tây Bắc": 6, "Tây": 7, "Đông Bắc": 8, "Nam": 9
    }
    matrix = {}
    for dir_name, base_val in base_map.items():
        star_num = ((base_val - 5 + van_num - 1) % 9) + 1
        status = "Đương Vận (Vượng)" if star_num == van_num else ("Sinh Khí" if star_num == (van_num % 9 + 1) else "Bình/Hung")
        matrix[dir_name] = {"star": STAR_NAMES[star_num], "status": status, "num": star_num}
    return matrix

def analyze_exact_degree(deg):
    deg = deg % 360.0
    matched_son = None
    for son in SON_HUONG_24:
        if son["deg_start"] > son["deg_end"]:
            if deg >= son["deg_start"] or deg < son["deg_end"]:
                matched_son = son
                break
        else:
            if son["deg_start"] <= deg < son["deg_end"]:
                matched_son = son
                break
                
    dai_khong_vong = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]
    warning = "Tuyến chính vượng (An toàn)"
    for dkv in dai_khong_vong:
        if abs(deg - dkv) <= 1.5 or abs(deg - dkv) >= 358.5:
            warning = "⚠️ CẢNH BÁO: Phạm tuyến ĐẠI KHÔNG VONG (Ranh giới Bát Quái)"
            break
    else:
        for son in SON_HUONG_24:
            if abs(deg - son["deg_start"]) <= 1.0 or abs(deg - son["deg_start"]) >= 359.0:
                warning = "⚠️ LƯU Ý: Phạm tuyến TIỂU KHÔNG VONG (Ranh giới 24 Sơn)"
                break
                
    return matched_son, warning

# --- MA TRẬN BÁT TRẠCH CHUẨN XÁC CHO 8 QUẺ MỆNH ---
BAT_TRACH_MAPPING = {
    1: {  # Khảm (Đông Tứ Mệnh)
        "Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☰", "name": "CÀN"}
    },
    9: {  # Ly (Đông Tứ Mệnh)
        "Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☰", "name": "CÀN"}
    },
    3: {  # Chấn (Đông Tứ Mệnh)
        "Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☰", "name": "CÀN"}
    },
    4: {  # Tốn (Đông Tứ Mệnh)
        "Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☰", "name": "CÀN"}
    },
    6: {  # Càn (Tây Tứ Mệnh)
        "Bắc": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☰", "name": "CÀN"}
    },
    2: {  # Khôn (Tây Tứ Mệnh)
        "Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☰", "name": "CÀN"}
    },
    7: {  # Đoài (Tây Tứ Mệnh)
        "Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☰", "name": "CÀN"}
    },
    8: {  # Cấn (Tây Tứ Mệnh)
        "Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☰", "name": "CÀN"}
    }
}

DIRECTION_ANGLES = {
    "Bắc": 0.0, "Đông Bắc": 45.0, "Đông": 90.0, "Đông Nam": 135.0,
    "Nam": 180.0, "Tây Nam": 225.0, "Tây": 270.0, "Tây Bắc": 315.0
}

def get_can_chi_academic(solar_date, solar_time, has_time):
    year = solar_date.year
    month = solar_date.month
    day = solar_date.day
    effective_year = year
    if month < 2 or (month == 2 and day < 4):
        effective_year -= 1
    elif month == 2 and day == 4 and has_time and solar_time:
        if solar_time < dt_time(4, 14):
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
    group = "Đông Tứ Mệnh" if quai_num in [1, 3, 4, 9] else "Tây Tứ Mệnh"
    return can, chi, eff_year, quai_num, group

# --- 2. GIAO DIỆN NHẬP LIỆU & SESSION STATE TỐI ƯU ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "play_spin" not in st.session_state:
    st.session_state.play_spin = False

with st.sidebar:
    st.header("🛠️ THAM SỐ LẬP QUẺ (MASTER)")
    d_input = st.date_input(
        "Ngày sinh (Dương lịch)",
        value=datetime(1973, 9, 17),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31),
        format="DD/MM/YYYY"
    )
    enable_time = st.checkbox("Kích hoạt Giờ sinh chính xác", value=True)
    t_input = None
    if enable_time:
        t_input = st.time_input("Giờ:Phút sinh", value=dt_time(8, 30))
    gender = st.selectbox("Giới tính gia chủ", ["Nam", "Nữ"], index=0)
    survey_year = st.number_input("Năm Xây Nhà / Nhập Trạch", min_value=1864, max_value=2100, value=2026, step=1)
    current_van = tinh_van_huyen_khong(survey_year)
    st.info(f"📌 Tự động nhận diện: Vận {current_van}")
    st.markdown("---")
    st.subheader("🧭 Đo Đạc Thực Địa")
    enable_survey = st.checkbox("Bật tia chỉ hướng thực tế", value=False)
    exact_deg = None
    if enable_survey:
        quick_dir = st.selectbox(
            "Chọn nhanh phương vị (hoặc chỉnh độ bên dưới)",
            list(DIRECTION_ANGLES.keys()), index=0
        )
        exact_deg = st.number_input(
            "Số độ đo thực tế (0.0° - 360.0°)",
            min_value=0.0, max_value=360.0,
            value=DIRECTION_ANGLES[quick_dir], step=0.5, format="%.1f"
        )
    run_btn = st.button("🔮 Lập Bản Đồ La Kinh Chuyên Sâu", type="primary", use_container_width=True)
    if run_btn:
        st.session_state.initialized = True
        st.session_state.play_spin = True
        
    st.markdown("""
        <div class="signature-box">
            <b>DIGITAL SIGNATURE</b><br>
            <b>Engineer:</b> TruongfNV<br>
            <b>Email:</b> truongnv.d11@gmail.com<br>
            <b>Hotline:</b> 0919855966<br>
            <i>System: Master Bagua Engine v20.0</i>
        </div>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ LA KINH 5 TẦNG TỐI ƯU THỰC CHIẾN ---
def render_matplotlib_lakinh(quai_num, exact_deg_val, gender_str, eff_year, van_num):
    fig, ax = plt.subplots(figsize=(7.8, 7.8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    mapping = BAT_TRACH_MAPPING[quai_num]
    star_matrix = get_fly_star_matrix(van_num)
    
    def get_text_rotation(angle_deg):
        rot = -angle_deg
        if 90 < angle_deg <= 270:
            rot += 180
        return rot
        
    # TẦNG 1: Vận Tinh Huyền Không
    for dir_name, angle in DIRECTION_ANGLES.items():
        star_info = star_matrix.get(dir_name, {"star": "", "status": ""})
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.33, height=0.18,
               color='#111827', alpha=0.95, edgecolor='#30363d', linewidth=1.0)
        rot_angle = get_text_rotation(angle)
        star_text = f"V{van_num}: {star_info['star']}"
        ax.text(rad, 0.42, star_text, color='#38bdf8', fontsize=6.3, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # TẦNG 2: 8 hướng Bát Trạch Cát/Hung
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.51, height=0.22,
               color=info["color"], alpha=0.9, edgecolor='white', linewidth=1.2)
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.62, info['cat_hung'], color='white', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # TẦNG 3: Quẻ vị Hậu Thiên
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.73, height=0.20,
               color='#1f242c', alpha=0.95, edgecolor='#30363d', linewidth=1.0)
        trig_text = f"{info['trigram']} {info['name']}"
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.83, trig_text, color='#f0f6fc', fontsize=8,
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # TẦNG 4: 24 Sơn Hướng - Địa bàn chính châm
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=0.93, height=0.25,
               color='#161b22', alpha=0.9, edgecolor='#30363d', linewidth=0.8)
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.05, son['name'], color='#58a6ff', fontsize=8, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # TẦNG 5: Ngũ Hành Nạp Âm chuẩn 24 Sơn
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=1.18, height=0.24,
               color='#0d1117', alpha=0.9, edgecolor='#30363d', linewidth=0.6)
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.30, son['elem'], color='#c9d1d9', fontsize=7.2,
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # VÒNG NGOÀI CÙNG: VẠCH CHIA ĐỘ CHI TIẾT (1° VÀ 5° ĐẾN 360°)
    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        if d_tick % 15 == 0:
            line_len = 0.05
            lw = 1.2
            col = '#FFD700'
        elif d_tick % 5 == 0:
            line_len = 0.03
            lw = 0.8
            col = 'white'
        else:
            line_len = 0.015
            lw = 0.4
            col = '#6e7681'
        ax.plot([rad_t, rad_t], [1.42, 1.42 + line_len], color=col, lw=lw)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.56, f"{d_tick}°", color='#c9d1d9', fontsize=7.5, ha='center', va='center')
            
    # THẬP TỰ THIÊN TÂM GỌN GÀNG (DỌC & NGANG)
    ax.plot([0, np.pi], [1.42, 1.42], color='#ff7b72', linestyle='--', lw=1.2, alpha=0.8, zorder=10)
    ax.plot([np.pi/2, 3*np.pi/2], [1.42, 1.42], color='#58a6ff', linestyle='--', lw=1.2, alpha=0.8, zorder=10)
    
    # TIA LASER CHỈ HƯỚNG ĐO ĐẠC THỰC ĐỊA (0° - 360°)
    if exact_deg_val is not None:
        target_rad = np.radians(exact_deg_val)
        ax.annotate('', xy=(target_rad, 1.45), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.2, width=2, headwidth=9),
                    zorder=14)
                    
    # TRUNG CUNG / THIÊN TRÌ & KIM LA BÀN CHÌM
    ax.fill([0, 0.15, np.pi, -0.15], [0.85, 0.12, 0, 0.12], color='#FF3333', alpha=0.4, zorder=4)
    ax.fill([np.pi, np.pi - 0.15, 0, np.pi + 0.15], [0.85, 0.12, 0, 0.12], color='#E0E0E0', alpha=0.3, zorder=4)
    ax.scatter([0], [0], color='#FFD700', s=20, zorder=12, edgecolors='black', linewidth=0.5)
    
    group_name = "Đông Tứ Mệnh" if quai_num in [1, 3, 4, 9] else "Tây Tứ Mệnh"
    center_text = f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str} ({eff_year})\nNhóm: {group_name}"
    ax.text(0, 0, center_text, color='#ff7b72', fontsize=7.5, fontweight='bold',
            ha='center', va='center', zorder=15,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.5))
            
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='#30363d', linestyle='--', linewidth=1)
    ax.spines['polar'].set_color('#8b949e')
    plt.tight_layout()
    return fig

# --- 4. HIỂN THỊ KẾT QUẢ ---
if st.session_state.initialized:
    can, chi, eff_year, quai_num, group_name = compute_master_cung_phi(d_input, t_input, enable_time, gender)
    mapping = BAT_TRACH_MAPPING[quai_num]
    star_matrix = get_fly_star_matrix(current_van)
    
    if st.session_state.play_spin:
        spin_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 450px; background-color: #0b0f19; color: #f0f6fc; font-family: sans-serif;">
            <div id="compass-container" style="position: relative; width: 260px; height: 260px; border: 4px solid #58a6ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #161b22 0%, #0d1117 100%); box-shadow: 0 0 25px rgba(88, 166, 255, 0.4); animation: spinCompass 3.0s cubic-bezier(0.15, 0.85, 0.15, 1.0) forwards;">
                <div style="font-size: 50px;">☸️</div>
                <div style="position: absolute; top: 10px; font-weight: bold; color: #ff7b72; font-size: 14px;">BẮC (0°)</div>
                <div style="position: absolute; bottom: 10px; font-weight: bold; color: #8b949e; font-size: 14px;">NAM (180°)</div>
            </div>
            <h3 id="status-text" style="margin-top: 25px; color: #58a6ff; letter-spacing: 1px;">Đang khởi tạo La Kinh Pro v20.0 cho năm {survey_year} (Vận {current_van})...</h3>
        </div>
        <style>
        @keyframes spinCompass {{
            0% {{ transform: rotate(0deg) scale(0.8); opacity: 0.5; }}
            50% {{ transform: rotate(1080deg) scale(1.05); opacity: 1; }}
            100% {{ transform: rotate(1440deg) scale(1); opacity: 1; }}
        }}
        </style>
        """
        placeholder = st.empty()
        with placeholder.container():
            components.html(spin_html, height=450)
            time_mod.sleep(3.0)
        placeholder.empty()
        st.session_state.play_spin = False

    col_left, col_right = st.columns([1.3, 1.7])
    with col_left:
        st.subheader("📋 Báo cáo Khí số Chuyên môn")
        st.metric("Ngày sinh ghi nhận", d_input.strftime("%d/%m/%Y"))
        st.metric("Can Chi Niên Mệnh", f"Năm {can} {chi} ({eff_year})")
        if enable_time and t_input:
            st.metric("Thời khắc Lập xuân / Giờ sinh", t_input.strftime("%H:%M"))
        st.metric("Nhóm Mệnh", group_name)
        st.metric("Thời gian khảo sát / Xây nhà", f"Năm {survey_year} (Vận {current_van})")
        
        if exact_deg is not None:
            son_info, khong_vong_msg = analyze_exact_degree(exact_deg)
            dir_name = son_info["dir"]
            survey_info = mapping[dir_name]
            star_v = star_matrix.get(dir_name, {})
            st.success(
                f"📌 Kết quả đo thực địa ({exact_deg:.1f}°):\n"
                f"- Tọa độ: Hướng {dir_name} — Sơn {son_info['name']} ({son_info['elem']})\n"
                f"- Bát Trạch: {survey_info['cat_hung']} ({survey_info['type']})\n"
                f"- Vận Tinh (Vận {current_van}): {star_v.get('star')}\n"
                f"- Trạng thái tuyến: {khong_vong_msg}"
            )
            
        st.markdown("### 🏛️ Gợi ý Bố trí Công năng Thực chiến")
        for d_key, info in mapping.items():
            if info["type"] == "Cát":
                star_v = star_matrix.get(d_key, {})
                st.markdown(f"""
                    <div class="advice-box">
                        <b>{d_key} ({info['cat_hung']} - Cát | V{current_van}: {star_v.get('star')}):</b> Thích hợp đặt {('Cửa chính / Phòng khách' if info['cat_hung']=='Sinh Khí' else ('Phòng ngủ / Giường ngủ' if info['cat_hung']=='Thiên Y' else 'Bàn thờ / Văn phòng'))}.
                    </div>
                """, unsafe_allow_html=True)
                
    with col_right:
        st.subheader("🧭 Đồ họa La Kinh Huyền Không & Bát Trạch 5 Tầng")
        fig_mpl = render_matplotlib_lakinh(quai_num, exact_deg, gender, eff_year, current_van)
        st.pyplot(fig_mpl)
else:
    st.info("👈 Vui lòng nhập thông số cá nhân ở thanh bên trái và bấm nút '🔮 Lập Bản Đồ La Kinh Chuyên Sâu' để khởi tạo đồ họa hiển thị.")
