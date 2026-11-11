import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np
import time as time_mod
from datetime import datetime, time as dt_time

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v15.0",
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

st.title("☸️ PROFESSIONAL FENG SUI MASTER BAGUA ENGINE v15.0")
st.markdown("Hệ thống lập bản đồ Khí số chuẩn thực chiến: Tự động hóa Vận tinh theo Năm khảo sát, Bát Trạch Quẻ Mệnh và La Kinh 5 Tầng.")

# --- 1. DỮ LIỆU HỌC THUẬT: 24 SƠN HƯỚNG & MA TRẬN PHI TINH THEO NĂM ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

SON_HUONG_24 = [
    {"name": "Nhâm", "deg_start": 337.5, "deg_end": 352.5, "elem": "Thủy"},
    {"name": "Tý", "deg_start": 352.5, "deg_end": 7.5, "elem": "Thủy"},
    {"name": "Quý", "deg_start": 7.5, "deg_end": 22.5, "elem": "Thủy"},
    {"name": "Cấn", "deg_start": 22.5, "deg_end": 37.5, "elem": "Thổ"},
    {"name": "Sửu", "deg_start": 37.5, "deg_end": 52.5, "elem": "Thổ"},
    {"name": "Dần", "deg_start": 52.5, "deg_end": 67.5, "elem": "Mộc"},
    {"name": "Giáp", "deg_start": 67.5, "deg_end": 82.5, "elem": "Mộc"},
    {"name": "Mão", "deg_start": 82.5, "deg_end": 97.5, "elem": "Mộc"},
    {"name": "Ất", "deg_start": 97.5, "deg_end": 112.5, "elem": "Mộc"},
    {"name": "Tốn", "deg_start": 112.5, "deg_end": 127.5, "elem": "Mộc"},
    {"name": "Thìn", "deg_start": 127.5, "deg_end": 142.5, "elem": "Thổ"},
    {"name": "Tỵ", "deg_start": 142.5, "deg_end": 157.5, "elem": "Hỏa"},
    {"name": "Bính", "deg_start": 157.5, "deg_end": 172.5, "elem": "Hỏa"},
    {"name": "Ngọ", "deg_start": 172.5, "deg_end": 187.5, "elem": "Hỏa"},
    {"name": "Đinh", "deg_start": 187.5, "deg_end": 202.5, "elem": "Hỏa"},
    {"name": "Khôn", "deg_start": 202.5, "deg_end": 217.5, "elem": "Thổ"},
    {"name": "Mùi", "deg_start": 217.5, "deg_end": 232.5, "elem": "Thổ"},
    {"name": "Thân", "deg_start": 232.5, "deg_end": 247.5, "elem": "Kim"},
    {"name": "Canh", "deg_start": 247.5, "deg_end": 262.5, "elem": "Kim"},
    {"name": "Dậu", "deg_start": 262.5, "deg_end": 277.5, "elem": "Kim"},
    {"name": "Tân", "deg_start": 277.5, "deg_end": 292.5, "elem": "Kim"},
    {"name": "Càn", "deg_start": 292.5, "deg_end": 307.5, "elem": "Kim"},
    {"name": "Tuất", "deg_start": 307.5, "deg_end": 322.5, "elem": "Thổ"},
    {"name": "Hợi", "deg_start": 322.5, "deg_end": 337.5, "elem": "Thủy"},
]

# Hàm tự động phân định Vận theo năm xây dựng/khảo sát thực tế
def get_yun_by_year(year):
    if 1984 <= year <= 2003:
        return "Vận 7 (1984-2003)"
    elif 2004 <= year <= 2023:
        return "Vận 8 (2004-2023)"
    elif 2024 <= year <= 2043:
        return "Vận 9 (2024-2043)"
    elif year >= 2044:
        return "Vận 1 (2044-2063)"
    else:
        return "Vận trước 1984"

FLYING_STAR_MATRIX = {
    "Vận 9 (2024-2043)": {
        "Nam": {"star": "Cửu Tử (9)", "status": "Đương Vận (Đại Cát)"},
        "Bắc": {"star": "Nhất Bạch (1)", "status": "Sinh Khí"},
        "Tây Nam": {"star": "Nhị Hắc (2)", "status": "Bệnh Phù"},
        "Đông": {"star": "Tam Bích (3)", "status": "Thị Phi"},
        "Đông Nam": {"star": "Tứ Lục (4)", "status": "Văn Sương"},
        "Trung Cung": {"star": "Ngũ Hoàng (5)", "status": "Đại Sát"},
        "Tây Bắc": {"star": "Lục Bạch (6)", "status": "Quý Nhân"},
        "Tây": {"star": "Thất Xích (7)", "status": "Phá Quân"},
        "Đông Bắc": {"star": "Bát Bạch (8)", "status": "Tiến Khí"}
    },
    "Vận 8 (2004-2023)": {
        "Đông Bắc": {"star": "Bát Bạch (8)", "status": "Đương Vận (Đại Cát)"},
        "Nam": {"star": "Cửu Tử (9)", "status": "Tiến Khí"},
        "Bắc": {"star": "Nhất Bạch (1)", "status": "Sinh Khí"},
        "Tây Nam": {"star": "Thất Xích (7)", "status": "Thoái Khí"},
        "Đông": {"star": "Lục Bạch (6)", "status": "Cát Tinh"},
        "Đông Nam": {"star": "Ngũ Hoàng (5)", "status": "Đại Sát"},
        "Tây": {"star": "Tam Bích (3)", "status": "Thị Phi"},
        "Tây Bắc": {"star": "Nhị Hắc (2)", "status": "Bệnh Phù"},
        "Trung Cung": {"star": "Tứ Lục (4)", "status": "Văn Sương"}
    },
    "Vận 7 (1984-2003)": {
        "Tây": {"star": "Thất Xích (7)", "status": "Đương Vận (Đại Cát)"},
        "Đông Bắc": {"star": "Cửu Tử (9)", "status": "Tiến Khí"},
        "Nam": {"star": "Bát Bạch (8)", "status": "Sinh Khí"},
        "Bắc": {"star": "Lục Bạch (6)", "status": "Cát Tinh"},
        "Tây Nam": {"star": "Ngũ Hoàng (5)", "status": "Đại Sát"},
        "Đông": {"star": "Nhị Hắc (2)", "status": "Bệnh Phù"},
        "Đông Nam": {"star": "Tam Bích (3)", "status": "Thị Phi"},
        "Tây Bắc": {"star": "Nhất Bạch (1)", "status": "Cát Tinh"},
        "Trung Cung": {"star": "Tứ Lục (4)", "status": "Văn Sương"}
    },
    "Vận 1 (2044-2063)": {
        "Bắc": {"star": "Nhất Bạch (1)", "status": "Đương Vận (Đại Cát)"},
        "Tây Nam": {"star": "Nhị Hắc (2)", "status": "Bệnh Phù"},
        "Đông": {"star": "Tam Bích (3)", "status": "Thị Phi"},
        "Đông Nam": {"star": "Tứ Lục (4)", "status": "Văn Sương"},
        "Trung Cung": {"star": "Ngũ Hoàng (5)", "status": "Đại Sát"},
        "Tây Bắc": {"star": "Lục Bạch (6)", "status": "Quý Nhân"},
        "Tây": {"star": "Thất Xích (7)", "status": "Phá Quân"},
        "Đông Bắc": {"star": "Bát Bạch (8)", "status": "Tiến Khí"},
        "Nam": {"star": "Cửu Tử (9)", "status": "Sinh Khí"}
    }
}

BAT_TRACH_MAPPING = {
    1: {  # Khảm
        "Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☰", "name": "CÀN"}
    },
    9: {  # Ly (Nam 1973 - Chuẩn xác)
        "Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☰", "name": "CÀN"}
    },
    3: {  # Chấn
        "Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☰", "name": "CÀN"}
    },
    4: {  # Tốn
        "Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☰", "name": "CÀN"}
    },
    6: {  # Càn
        "Bắc": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☰", "name": "CÀN"}
    },
    2: {  # Khôn
        "Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☰", "name": "CÀN"}
    },
    7: {  # Đoài
        "Bắc": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☰", "name": "CÀN"}
    },
    8: {  # Cấn
        "Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Họa Hải", "type": "Hung", "color": "#9e6a03", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☰", "name": "CÀN"}
    }
}

DIRECTION_ANGLES = {
    "Bắc": 0, "Đông Bắc": 45, "Đông": 90, "Đông Nam": 135,
    "Nam": 180, "Tây Nam": 225, "Tây": 270, "Tây Bắc": 315
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

# --- 2. GIAO DIỆN NHẬP LIỆU & SESSION STATE ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False

with st.sidebar:
    st.header("🛠️ THAM SỐ LẬP QUẺ (MASTER)")
    
    d_input = st.date_input(
        "Ngày sinh (Dương lịch)", 
        value=datetime(1974, 2, 2),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31),
        format="DD/MM/YYYY"
    )
    
    enable_time = st.checkbox("Kích hoạt Giờ sinh chính xác", value=True)
    t_input = None
    if enable_time:
        t_input = st.time_input("Giờ:Phút sinh", value=dt_time(8, 30))
        
    gender = st.selectbox("Giới tính gia chủ", ["Nam", "Nữ"])
    
    # Thay thế phần chọn Vận cứng nhắc bằng Năm xây dựng/khảo sát tự động nhận diện
    survey_year = st.number_input("Năm Xây Nhà / Nhập Trạch", min_value=1984, max_value=2063, value=2026, step=1)
    auto_yun_key = get_yun_by_year(survey_year)
    st.info(f"📌 Nhận diện Vận: **{auto_yun_key}**")
    
    target_survey_dir = st.selectbox(
        "🧭 Hướng Khảo Sát Thực Địa (Nhà/Cửa/Bàn Thờ)", 
        ["Không chọn", "Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]
    )
    
    run_btn = st.button("🔮 Lập Bản Đồ La Kinh Chuyên Sâu", type="primary", use_container_width=True)
    if run_btn:
        st.session_state.initialized = True

    st.markdown("""
        <div class="signature-box">
            <b>DIGITAL SIGNATURE</b><br>
            <b>Engineer:</b> TruongfNV<br>
            <b>Email:</b> truongnv.d11@gmail.com<br>
            <b>Hotline:</b> 0919855966<br>
            <i>System: Master Bagua Engine v15.0</i>
        </div>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ LA KINH 5 TẦNG TỰ ĐỘNG THEO NĂM KHẢO SÁT ---
def render_matplotlib_lakinh(quai_num, survey_direction, gender_str, eff_year, current_yun_key):
    fig, ax = plt.subplots(figsize=(7.8, 7.8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    mapping = BAT_TRACH_MAPPING[quai_num]
    star_matrix = FLYING_STAR_MATRIX.get(current_yun_key, FLYING_STAR_MATRIX["Vận 9 (2024-2043)"])

    def get_text_rotation(angle_deg):
        rot = -angle_deg
        if 90 < angle_deg <= 270:
            rot += 180
        return rot

    # TẦNG 1: Vận Tinh Huyền Không tự động theo Năm (Bán kính 0.35 -> 0.52)
    for dir_name, angle in DIRECTION_ANGLES.items():
        star_info = star_matrix.get(dir_name, {"star": "", "status": ""})
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.35, height=0.17, 
               color='#111827', alpha=0.95, edgecolor='#30363d', linewidth=1.0)
        
        rot_angle = get_text_rotation(angle)
        star_text = f"V: {star_info['star']}"
        ax.text(rad, 0.435, star_text, color='#38bdf8', fontsize=8, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # TẦNG 2: 8 hướng Bát Trạch Cát/Hung chuẩn Mệnh chủ (Bán kính 0.52 -> 0.72)
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.52, height=0.20, 
               color=info["color"], alpha=0.9, edgecolor='white', linewidth=1.2)
        
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.62, info['cat_hung'], color='white', fontsize=9, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # TẦNG 3: Quẻ vị Hậu Thiên (Bán kính 0.72 -> 0.92)
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.72, height=0.20, 
               color='#1f242c', alpha=0.95, edgecolor='#30363d', linewidth=1.0)
        
        trig_text = f"{info['trigram']} {info['name']}"
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.82, trig_text, color='#f0f6fc', fontsize=8.5,
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # TẦNG 4: 24 Sơn Hướng - Địa bàn chính châm (Bán kính 0.92 -> 1.18)
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=0.92, height=0.26,
               color='#161b22', alpha=0.9, edgecolor='#30363d', linewidth=0.8)
        
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.05, son['name'], color='#58a6ff', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # TẦNG 5: Ngũ Hành Nạp Âm chuẩn 24 Sơn (Bán kính 1.18 -> 1.42)
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=1.18, height=0.24,
               color='#0d1117', alpha=0.9, edgecolor='#30363d', linewidth=0.6)
        
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.30, son['elem'], color='#8b949e', fontsize=7.5,
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # Vòng chia độ nhỏ chi tiết ngoài cùng
    for d_tick in range(0, 360):
        rad_t = np.radians(d_tick)
        if d_tick % 5 == 0:
            line_len = 0.04 if d_tick % 15 == 0 else 0.025
            ax.plot([rad_t, rad_t], [1.42, 1.42 + line_len], color='#8b949e', lw=1.0)
            if d_tick % 45 == 0:
                ax.text(rad_t, 1.55, f"{d_tick}°", color='#8b949e', fontsize=8, ha='center', va='center')
        else:
            ax.plot([rad_t, rad_t], [1.42, 1.42 + 0.01], color='#484f58', lw=0.5)

    # Thập tự thiên tâm hoàn chỉnh 4 chiều
    ax.plot([0, np.radians(180)], [0, 1.42], color='#ff7b72', linestyle='--', lw=1.2, alpha=0.8)
    ax.plot([np.radians(180), np.radians(360)], [0, 1.42], color='#ff7b72', linestyle='--', lw=1.2, alpha=0.8)
    ax.plot([np.radians(90), np.radians(270)], [0, 1.42], color='#58a6ff', linestyle='--', lw=1.2, alpha=0.8)
    ax.plot([np.radians(270), np.radians(450)], [0, 1.42], color='#58a6ff', linestyle='--', lw=1.2, alpha=0.8)

    # Trục định hướng thực địa
    if survey_direction != "Không chọn" and survey_direction in DIRECTION_ANGLES:
        target_deg = DIRECTION_ANGLES[survey_direction]
        target_rad = np.radians(target_deg)
        ax.annotate('', xy=(target_rad, 1.38), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='white', lw=2, width=3, headwidth=10))

    # Trung Cung / Thiên Trì
    group_name = "Đông Tứ Mệnh" if quai_num in [1, 3, 4, 9] else "Tây Tứ Mệnh"
    center_text = f"🧭 THIÊN TRÌ\n{gender_str} ({eff_year})\nNhóm: {group_name}"
    ax.text(0, 0, center_text, color='#ff7b72', fontsize=7.5, fontweight='bold',
            ha='center', va='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.5))

    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='#30363d', linestyle='--', linewidth=1)
    ax.spines['polar'].set_color('#8b949e')

    plt.tight_layout()
    return fig

# --- 4. HIỂN THỊ KẾT QUẢ KÈM HIỆU ỨNG ---
if st.session_state.initialized:
    can, chi, eff_year, quai_num, group_name = compute_master_cung_phi(d_input, t_input, enable_time, gender)
    mapping = BAT_TRACH_MAPPING[quai_num]
    star_matrix = FLYING_STAR_MATRIX.get(auto_yun_key, FLYING_STAR_MATRIX["Vận 9 (2024-2043)"])

    spin_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 450px; background-color: #0b0f19; color: #f0f6fc; font-family: sans-serif;">
        <div id="compass-container" style="position: relative; width: 260px; height: 260px; border: 4px solid #58a6ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #161b22 0%, #0d1117 100%); box-shadow: 0 0 25px rgba(88, 166, 255, 0.4); animation: spinCompass 3.5s cubic-bezier(0.15, 0.85, 0.15, 1.0) forwards;">
            <div style="font-size: 50px;">☸️</div>
            <div style="position: absolute; top: 10px; font-weight: bold; color: #ff7b72; font-size: 14px;">BẮC (0°)</div>
            <div style="position: absolute; bottom: 10px; font-weight: bold; color: #8b949e; font-size: 14px;">NAM (180°)</div>
        </div>
        <h3 id="status-text" style="margin-top: 25px; color: #58a6ff; letter-spacing: 1px;">Đang nạp Khí số cho năm {survey_year} ({auto_yun_key})...</h3>
    </div>
    
    <style>
    @keyframes spinCompass {{
        0% {{ transform: rotate(0deg) scale(0.8); opacity: 0.5; }}
        50% {{ transform: rotate(1080deg) scale(1.05); opacity: 1; }}
        100% {{ transform: rotate(1440deg) scale(1); opacity: 1; }}
    }}
    </style>
    
    <script>
    setTimeout(function() {{
        document.getElementById("status-text").innerText = "✨ Đã đồng bộ hoàn tất La Kinh Phong Thủy!";
    }}, 3000);
    </script>
    """
    
    placeholder = st.empty()
    with placeholder.container():
        components.html(spin_html, height=500)
        time_mod.sleep(3.5)
    placeholder.empty()

    col_left, col_right = st.columns([1.3, 1.7])

    with col_left:
        st.subheader("📋 Báo cáo Khí số Chuyên môn")
        st.metric("Ngày sinh ghi nhận", d_input.strftime("%d/%m/%Y"))
        st.metric("Can Chi Niên Mệnh", f"Năm {can} {chi} ({eff_year})")
        if enable_time and t_input:
            st.metric("Thời khắc Lập xuân / Giờ sinh", t_input.strftime("%H:%M"))
        st.metric("Nhóm Mệnh", group_name)
        st.metric("Thời gian khảo sát / Xây nhà", f"Năm {survey_year} ({auto_yun_key})")
        
        if target_survey_dir != "Không chọn":
            survey_info = mapping[target_survey_dir]
            star_v = star_matrix.get(target_survey_dir, {})
            st.success(f"📌 **Khảo sát hướng {target_survey_dir}:**\n- Bát Trạch: **{survey_info['cat_hung']}** ({survey_info['type']})\n- Vận Tinh: **{star_v.get('star')}** - *{star_v.get('status')}*")

        st.markdown("### 🏛️ Gợi ý Bố trí Công năng Thực chiến")
        for d_key, info in mapping.items():
            if info["type"] == "Cát":
                star_v = star_matrix.get(d_key, {})
                st.markdown(f"""
                    <div class="advice-box">
                        <b>{d_key} ({info['cat_hung']} - Cát | V: {star_v.get('star')}):</b> Thích hợp đặt {('Cửa chính / Phòng khách' if info['cat_hung']=='Sinh Khí' else ('Phòng ngủ / Giường ngủ' if info['cat_hung']=='Thiên Y' else 'Bàn thờ / Văn phòng'))}.
                    </div>
                """, unsafe_allow_html=True)

    with col_right:
        st.subheader("🧭 Đồ họa La Kinh Huyền Không & Bát Trạch 5 Tầng")
        fig_mpl = render_matplotlib_lakinh(quai_num, target_survey_dir, gender, eff_year, auto_yun_key)
        st.pyplot(fig_mpl)
else:
    st.info("👈 **Vui lòng nhập thông số cá nhân ở thanh bên trái và bấm nút '🔮 Lập Bản Đồ La Kinh Chuyên Sâu' để khởi tạo đồ họa hiển thị.**")
