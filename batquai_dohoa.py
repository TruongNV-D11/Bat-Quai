import streamlit as st
import streamlit.components.v1 as components
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import time as time_mod
from datetime import datetime, time as dt_time
from PIL import Image

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v21.0",
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

st.title("☸️ PROFESSIONAL FENG SUI MASTER BAGUA ENGINE v21.0")
st.markdown("Hệ thống lập bản đồ Khí số chuyên nghiệp thực chiến: Tam Nguyên Cửu Vận, Tinh Bàn Huyền Không (Vận - Sơn - Hướng), Lưu Niên/Nguyệt, Bát Trạch 8 Quẻ Mệnh & 120 Phân Kim.")

# --- 1. DỮ LIỆU HỌC THUẬT: 24 SƠN HƯỚNG ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

SON_HUONG_24 = [
    {"name": "Nhâm", "deg_start": 337.5, "deg_end": 352.5, "elem": "Thủy", "dir": "Bắc", "palace": 1, "yuan": 1, "polarity": 1},
    {"name": "Tý",   "deg_start": 352.5, "deg_end": 7.5,   "elem": "Thủy", "dir": "Bắc", "palace": 1, "yuan": 0, "polarity": -1},
    {"name": "Quý",  "deg_start": 7.5,   "deg_end": 22.5,  "elem": "Thủy", "dir": "Bắc", "palace": 1, "yuan": 2, "polarity": -1},
    
    {"name": "Cấn",  "deg_start": 22.5,  "deg_end": 37.5,  "elem": "Thổ",  "dir": "Đông Bắc", "palace": 8, "yuan": 1, "polarity": 1},
    {"name": "Sửu",  "deg_start": 37.5,  "deg_end": 52.5,  "elem": "Thổ",  "dir": "Đông Bắc", "palace": 8, "yuan": 0, "polarity": -1},
    {"name": "Dần",  "deg_start": 52.5,  "deg_end": 67.5,  "elem": "Mộc",  "dir": "Đông Bắc", "palace": 8, "yuan": 2, "polarity": -1},
    
    {"name": "Giáp", "deg_start": 67.5,  "deg_end": 82.5,  "elem": "Mộc",  "dir": "Đông", "palace": 3, "yuan": 1, "polarity": 1},
    {"name": "Mão",  "deg_start": 82.5,  "deg_end": 97.5,  "elem": "Mộc",  "dir": "Đông", "palace": 3, "yuan": 0, "polarity": -1},
    {"name": "Ất",   "deg_start": 97.5,  "deg_end": 112.5, "elem": "Mộc",  "dir": "Đông", "palace": 3, "yuan": 2, "polarity": -1},
    
    {"name": "Tốn",  "deg_start": 112.5, "deg_end": 127.5, "elem": "Mộc",  "dir": "Đông Nam", "palace": 4, "yuan": 1, "polarity": 1},
    {"name": "Thìn", "deg_start": 127.5, "deg_end": 142.5, "elem": "Thổ",  "dir": "Đông Nam", "palace": 4, "yuan": 0, "polarity": -1},
    {"name": "Tỵ",   "deg_start": 142.5, "deg_end": 157.5, "elem": "Hỏa",  "dir": "Đông Nam", "palace": 4, "yuan": 2, "polarity": -1},
    
    {"name": "Bính", "deg_start": 157.5, "deg_end": 172.5, "elem": "Hỏa",  "dir": "Nam", "palace": 9, "yuan": 1, "polarity": -1},
    {"name": "Ngọ",  "deg_start": 172.5, "deg_end": 187.5, "elem": "Hỏa",  "dir": "Nam", "palace": 9, "yuan": 0, "polarity": 1},
    {"name": "Đinh", "deg_start": 187.5, "deg_end": 202.5, "elem": "Hỏa",  "dir": "Nam", "palace": 9, "yuan": 2, "polarity": 1},
    
    {"name": "Khôn", "deg_start": 202.5, "deg_end": 217.5, "elem": "Thổ",  "dir": "Tây Nam", "palace": 2, "yuan": 1, "polarity": -1},
    {"name": "Mùi",  "deg_start": 217.5, "deg_end": 232.5, "elem": "Thổ",  "dir": "Tây Nam", "palace": 2, "yuan": 0, "polarity": 1},
    {"name": "Thân", "deg_start": 232.5, "deg_end": 247.5, "elem": "Kim",  "dir": "Tây Nam", "palace": 2, "yuan": 2, "polarity": 1},
    
    {"name": "Canh", "deg_start": 247.5, "deg_end": 262.5, "elem": "Kim",  "dir": "Tây", "palace": 7, "yuan": 1, "polarity": -1},
    {"name": "Dậu",  "deg_start": 262.5, "deg_end": 277.5, "elem": "Kim",  "dir": "Tây", "palace": 7, "yuan": 0, "polarity": 1},
    {"name": "Tân",  "deg_start": 277.5, "deg_end": 292.5, "elem": "Kim",  "dir": "Tây", "palace": 7, "yuan": 2, "polarity": 1},
    
    {"name": "Càn",  "deg_start": 292.5, "deg_end": 307.5, "elem": "Kim",  "dir": "Tây Bắc", "palace": 6, "yuan": 1, "polarity": -1},
    {"name": "Tuất", "deg_start": 307.5, "deg_end": 322.5, "elem": "Thổ",  "dir": "Tây Bắc", "palace": 6, "yuan": 0, "polarity": 1},
    {"name": "Hợi",  "deg_start": 322.5, "deg_end": 337.5, "elem": "Thủy", "dir": "Tây Bắc", "palace": 6, "yuan": 2, "polarity": 1},
]

FIVE_POLARITY = {
    0: {1: -1, 2: 1, 3: -1, 4: -1, 6: 1, 7: 1, 8: -1, 9: 1},
    1: {1: 1, 2: -1, 3: 1, 4: 1, 6: -1, 7: -1, 8: 1, 9: -1},
    2: {1: -1, 2: 1, 3: -1, 4: -1, 6: 1, 7: 1, 8: -1, 9: 1}
}

BASE_PALACE_MAP = {
    "Bắc": 1, "Tây Nam": 2, "Đông": 3, "Đông Nam": 4, 
    "Trung Cung": 5, "Tây Bắc": 6, "Tây": 7, "Đông Bắc": 8, "Nam": 9
}

DIRECTION_ANGLES = {
    "Bắc": 0.0, "Đông Bắc": 45.0, "Đông": 90.0, "Đông Nam": 135.0,
    "Nam": 180.0, "Tây Nam": 225.0, "Tây": 270.0, "Tây Bắc": 315.0
}

def tinh_van_huyen_khong(nam_nhap_trach):
    khoang_cach = (nam_nhap_trach - 1864) // 20
    van = (khoang_cach % 9) + 1
    return van

def fly_stars_from_center(center_star, polarity=1):
    chart = {}
    for dir_name, base_palace in BASE_PALACE_MAP.items():
        step = (base_palace - 5) % 9
        if polarity == 1:
            star = ((center_star - 1 + step) % 9) + 1
        else:
            star = ((center_star - 1 - step) % 9) + 1
        chart[dir_name] = star
    return chart

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

def get_star_polarity(star_num, yuan_idx, ref_palace):
    if star_num == 5:
        return FIVE_POLARITY[yuan_idx].get(ref_palace, 1)
    for s in SON_HUONG_24:
        if s["palace"] == star_num and s["yuan"] == yuan_idx:
            return s["polarity"]
    return 1

def compute_xuan_kong_chart(van_num, facing_deg):
    van_chart = fly_stars_from_center(van_num, polarity=1)
    facing_son = get_son_by_degree(facing_deg)
    sitting_deg = (facing_deg + 180.0) % 360.0
    sitting_son = get_son_by_degree(sitting_deg)
    
    son_center = van_chart[sitting_son["dir"]]
    huong_center = van_chart[facing_son["dir"]]
    
    son_pol = get_star_polarity(son_center, sitting_son["yuan"], sitting_son["palace"])
    huong_pol = get_star_polarity(huong_center, facing_son["yuan"], facing_son["palace"])
    
    son_chart = fly_stars_from_center(son_center, son_pol)
    huong_chart = fly_stars_from_center(huong_center, huong_pol)
    
    palaces = {}
    for d_name in BASE_PALACE_MAP.keys():
        palaces[d_name] = {
            "van": van_chart[d_name],
            "son": son_chart[d_name],
            "huong": huong_chart[d_name]
        }
        
    f_dir = facing_son["dir"]
    s_dir = sitting_son["dir"]
    if palaces[f_dir]["huong"] == van_num and palaces[s_dir]["son"] == van_num:
        cuc_dien = "Vượng Sơn Vượng Hướng (Đại Cát - Đinh Tài lưỡng vượng)"
    elif palaces[f_dir]["huong"] == van_num and palaces[f_dir]["son"] == van_num:
        cuc_dien = "Song Tinh Đáo Hướng (Vượng Tài - Cần có Thủy ở hướng trước)"
    elif palaces[s_dir]["huong"] == van_num and palaces[s_dir]["son"] == van_num:
        cuc_dien = "Song Tinh Đáo Tọa (Vượng Đinh - Cần có Sơn/Tọa vững sau nhà)"
    elif palaces[f_dir]["son"] == van_num and palaces[s_dir]["huong"] == van_num:
        cuc_dien = "Thượng Sơn Hạ Thủy (Cách cục nghịch - Cần hóa giải bố cục)"
    else:
        cuc_dien = "Cách cục Hỗn hợp / Bình hòa (Xét chi tiết từng cung)"
        
    return {
        "facing_son": facing_son,
        "sitting_son": sitting_son,
        "cuc_dien": cuc_dien,
        "palaces": palaces
    }

def get_annual_monthly_charts(year_num, month_num):
    annual_center = ((11 - (year_num % 9)) % 9)
    if annual_center == 0:
        annual_center = 9
    annual_chart = fly_stars_from_center(annual_center, polarity=1)
    
    chi_idx = (year_num - 1984) % 12
    if chi_idx in [0, 3, 6, 9]:
        m_base = 8
    elif chi_idx in [1, 4, 7, 10]:
        m_base = 5
    else:
        m_base = 2
    monthly_center = ((m_base - (month_num - 1) - 1) % 9) + 1
    monthly_chart = fly_stars_from_center(monthly_center, polarity=1)
    
    return annual_chart, monthly_chart

def analyze_exact_degree(deg):
    deg = deg % 360.0
    matched_son = get_son_by_degree(deg)
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
    col_y, col_m = st.columns(2)
    with col_y:
        survey_year = st.number_input("Năm Xây / Xét", min_value=1864, max_value=2100, value=2026, step=1)
    with col_m:
        survey_month = st.number_input("Tháng Âm lịch", min_value=1, max_value=12, value=10, step=1)
    current_van = tinh_van_huyen_khong(survey_year)
    st.info(f"📌 Tự động nhận diện: Vận {current_van} (Lưu niên {survey_year} - Tháng {survey_month})")
    st.markdown("---")
    st.subheader("🧭 Đo Đạc Hướng Nhà Thực Địa")
    quick_dir = st.selectbox("Chọn nhanh phương vị", list(DIRECTION_ANGLES.keys()), index=0)
    exact_deg = st.number_input(
        "Độ số Hướng Nhà (0.0° - 360.0°)",
        min_value=0.0, max_value=360.0,
        value=DIRECTION_ANGLES[quick_dir], step=0.5, format="%.1f"
    )
    show_laser = st.checkbox("Hiển thị Tia Laser Tọa / Hướng trên La Kinh", value=True)
    run_btn = st.button("🔮 Lập Bản Đồ La Kinh Chuyên Sâu", type="primary", use_container_width=True)
    if run_btn:
        st.session_state.initialized = True
        st.session_state.play_spin = True
        
    st.markdown("""
    <div class="signature-box">
        <b>DIGITAL SIGNATURE</b><br>
        Engineer: TruongfNV<br>
        Email: truongnv.d11@gmail.com<br>
        Hotline: 0919855966<br>
        System: Master Bagua Engine v21.0
    </div>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ LA KINH 7 TẦNG CHUYÊN SÂU ---
def render_matplotlib_lakinh(quai_num, exact_deg_val, show_laser_flag, gender_str, eff_year, van_num, xk_chart, annual_chart, monthly_chart, alpha_bg=1.0):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(8.8, 8.8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#0b0f19' if alpha_bg == 1.0 else 'none')
    ax.set_facecolor('#0b0f19' if alpha_bg == 1.0 else 'none')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.66)
    
    mapping = BAT_TRACH_MAPPING[quai_num]
    
    def get_text_rotation(angle_deg):
        rot = -angle_deg
        if 90 < angle_deg <= 270:
            rot += 180
        return rot

    # 1. TẦNG BÁT TRẠCH & HẬU THIÊN (r: 0.72 -> 1.04)
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        rot_angle = get_text_rotation(angle)
        
        ax.bar(bar_start, width=np.radians(45), bottom=0.72, height=0.16, align='edge',
               color=info["color"], alpha=0.85 * alpha_bg, edgecolor='white', linewidth=1.1, zorder=2)
        ax.text(rad, 0.80, info['cat_hung'], color='white', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=3)
                
        ax.bar(bar_start, width=np.radians(45), bottom=0.88, height=0.16, align='edge',
               color='#1f242c', alpha=0.90 * alpha_bg, edgecolor='#30363d', linewidth=1.0, zorder=2)
        ax.text(rad, 0.96, f"{info['trigram']} {info['name']}", color='#f0f6fc', fontsize=8.0, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=3)

    # 2. 24 SƠN HƯỚNG & NẠP ÂM (r: 1.04 -> 1.38)
    for son in SON_HUONG_24:
        mid_deg = ((son["deg_start"] + son["deg_end"]) / 2) % 360
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        rot_son = get_text_rotation(mid_deg)
        
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.04, height=0.19, align='edge',
               color='#161b22', alpha=0.85 * alpha_bg, edgecolor='#30363d', linewidth=0.8, zorder=2)
        ax.text(rad_son, 1.135, son['name'], color='#58a6ff', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)
                
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.23, height=0.15, align='edge',
               color='#0d1117', alpha=0.85 * alpha_bg, edgecolor='#30363d', linewidth=0.6, zorder=2)
        ax.text(rad_son, 1.305, son['elem'], color='#c9d1d9', fontsize=7.2, fontweight='bold',
                ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)

    # 3. 120 PHÂN KIM (r: 1.38 -> 1.45)
    for son in SON_HUONG_24:
        for slot in range(5):
            slot_start = (son["deg_start"] + slot * 3.0) % 360.0
            pk_color = '#2ea043' if slot == 2 else ('#1f6feb' if slot in [1, 3] else '#30363d')
            ax.bar(np.radians(slot_start), width=np.radians(3.0), bottom=1.38, height=0.07, align='edge',
                   color=pk_color, alpha=0.85 * alpha_bg, edgecolor='#0b0f19', linewidth=0.4, zorder=2)

    # 4. VÒNG CHIA ĐỘ (r: 1.45 -> 1.58)
    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        line_len = 0.04 if d_tick % 15 == 0 else (0.025 if d_tick % 5 == 0 else 0.012)
        col = '#FFD700' if d_tick % 15 == 0 else ('white' if d_tick % 5 == 0 else '#6e7681')
        ax.plot([rad_t, rad_t], [1.45, 1.45 + line_len], color=col, lw=1.2 if d_tick % 15 == 0 else 0.4, zorder=2)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.58, f"{d_tick}°", color='#c9d1d9', fontsize=7.5, ha='center', va='center', zorder=3)

    # 5. 2 VÒNG TRONG CÙNG (ĐÃ ĐẨY BÁN KÍNH LÊN RÕ RÀNG: r: 0.42 -> 0.72)
    for dir_name, angle in DIRECTION_ANGLES.items():
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        rot_angle = get_text_rotation(angle)
        
        # Tầng 2: Lưu Niên / Nguyệt (r: 0.57 -> 0.72)
        y_star = annual_chart[dir_name]
        m_star = monthly_chart[dir_name]
        ax.bar(bar_start, width=np.radians(45), bottom=0.57, height=0.15, align='edge',
               color='#1c2333', alpha=0.95 * alpha_bg, edgecolor='#30363d', linewidth=1.2, zorder=10)
        ym_color = '#ff7b72' if y_star in [2, 5] else ('#3fb950' if y_star in [1, 8, 9] else '#d2a8ff')
        ax.text(rad, 0.645, f"N:{y_star} T:{m_star}", color=ym_color, fontsize=7.5, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=15)

        # Tầng 1: Huyền Không 3 Sao (r: 0.42 -> 0.57)
        p_info = xk_chart["palaces"][dir_name]
        ax.bar(bar_start, width=np.radians(45), bottom=0.42, height=0.15, align='edge',
               color='#111827', alpha=0.95 * alpha_bg, edgecolor='#30363d', linewidth=1.2, zorder=10)
        ax.text(rad, 0.495, f"S:{p_info['son']} H:{p_info['huong']} [V{p_info['van']}]", color='#38bdf8', fontsize=7.0, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=15)

    # Thập tự & Tia laser (Hướng & Tọa)
    ax.plot([0, np.pi], [1.45, 1.45], color='#ff7b72', linestyle='--', lw=1.1, alpha=0.75, zorder=16)
    ax.plot([np.pi/2, 3*np.pi/2], [1.45, 1.45], color='#58a6ff', linestyle='--', lw=1.1, alpha=0.75, zorder=16)
    
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        ax.annotate('', xy=(fac_rad, 1.47), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.0, width=1.8, headwidth=8), zorder=18)
        ax.plot([0, sit_rad], [0, 1.45], color='#FFD700', linestyle=':', lw=1.8, alpha=0.9, zorder=17)
                    
    # Thiên Trì Trung Cung
    ax.fill([0, 0.15, np.pi, -0.15], [0.42, 0.05, 0, 0.05], color='#FF3333', alpha=0.35, zorder=11)
    ax.fill([np.pi, np.pi - 0.15, 0, np.pi + 0.15], [0.42, 0.05, 0, 0.05], color='#E0E0E0', alpha=0.25, zorder=11)
    ax.scatter([0], [0], color='#FFD700', s=25, zorder=21, edgecolors='black', linewidth=0.5)
    
    ax.text(0, 0, f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str} ({eff_year})", color='#ff7b72', fontsize=7.0, fontweight='bold',
            ha='center', va='center', zorder=22,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.4))
            
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='#30363d', linestyle='--', linewidth=0.8)
    ax.spines['polar'].set_color('#8b949e')
    plt.tight_layout()
    return fig

# --- 4. HIỂN THỊ KẾT QUẢ ---
if st.session_state.initialized:
    can, chi, eff_year, quai_num, group_name = compute_master_cung_phi(d_input, t_input, enable_time, gender)
    mapping = BAT_TRACH_MAPPING[quai_num]
    xk_chart = compute_xuan_kong_chart(current_van, exact_deg)
    annual_chart, monthly_chart = get_annual_monthly_charts(survey_year, survey_month)
    son_info, khong_vong_msg = analyze_exact_degree(exact_deg)
    
    if st.session_state.play_spin:
        spin_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 400px; background-color: #0b0f19; color: #f0f6fc; font-family: sans-serif;">
            <div style="font-size: 60px; animation: spinCompass 2s infinite linear; margin-bottom: 20px;">☸️</div>
            <div style="font-size: 18px; font-weight: bold; color: #58a6ff;">Đang lập Tinh Bàn & La Kinh 7 Tầng cho năm {survey_year} (Vận {current_van})...</div>
        </div>
        <style>
        @keyframes spinCompass {{
            0% {{ transform: rotate(0deg) scale(0.8); opacity: 0.5; }}
            50% {{ transform: rotate(720deg) scale(1.1); opacity: 1; }}
            100% {{ transform: rotate(1440deg) scale(0.8); opacity: 0.5; }}
        }}
        </style>
        """
        placeholder = st.empty()
        with placeholder.container():
            components.html(spin_html, height=450)
        time_mod.sleep(2.5)
        placeholder.empty()
        st.session_state.play_spin = False

    col_left, col_right = st.columns([1.25, 1.75])
    with col_left:
        st.subheader("📋 Báo cáo Khí số Chuyên môn")
        c1, c2 = st.columns(2)
        c1.metric("Niên Mệnh", f"{can} {chi} ({eff_year})")
        c2.metric("Nhóm Mệnh", group_name)
        
        dir_name = son_info["dir"]
        survey_info = mapping[dir_name]
        p_facing = xk_chart["palaces"][dir_name]
        st.success(
            f"🧭 Tọa {xk_chart['sitting_son']['name']} — Hướng {son_info['name']} ({exact_deg:.1f}°):\n\n"
            f"- Bát Trạch: {survey_info['cat_hung']} ({survey_info['type']})\n"
            f"- Tinh Bàn Hướng: Sơn {p_facing['son']} | Hướng {p_facing['huong']} | Vận {p_facing['van']}\n"
            f"- Cách cục: {xk_chart['cuc_dien']}\n"
            f"- Phân Kim: {khong_vong_msg}"
        )
        
        st.markdown("### 🏛️ Gợi ý Bố trí Công năng Thực chiến")
        for d_key, info in mapping.items():
            if info["type"] == "Cát":
                p_star = xk_chart["palaces"][d_key]
                y_s = annual_chart[d_key]
                m_s = monthly_chart[d_key]
                st.markdown(f"""
                <div class="advice-box">
                    <b>{d_key} ({info['cat_hung']} - Cát):</b> Tinh bàn [S:{p_star['son']} H:{p_star['huong']} V:{p_star['van']}] | Lưu niên: {y_s}, Tháng: {m_s}.<br>
                    <i>Gợi ý: Đặt {('Cửa chính / Phòng khách' if info['cat_hung']=='Sinh Khí' else ('Phòng ngủ / Giường ngủ' if info['cat_hung']=='Thiên Y' else 'Bàn thờ / Văn phòng'))}.</i>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        tab1, tab2 = st.tabs(["🧭 La Kinh 7 Tầng Chuyên Sâu", "🏠 Áp La Kinh Lên Mặt Bằng Nhà"])
        with tab1:
            fig_mpl = render_matplotlib_lakinh(
                quai_num, exact_deg, show_laser, gender, eff_year,
                current_van, xk_chart, annual_chart, monthly_chart, alpha_bg=1.0
            )
            st.pyplot(fig_mpl)
        with tab2:
            st.markdown("Tải lên hình ảnh sơ đồ mặt bằng nhà (PNG/JPG) để đặt La Kinh trong suốt vào tâm nhà:")
            uploaded_plan = st.file_uploader("Chọn ảnh mặt bằng", type=["png", "jpg", "jpeg"])
            if uploaded_plan is not None:
                opacity_val = st.slider("Độ mờ nền La Kinh (để nhìn rõ nét vẽ mặt bằng bên dưới)", 0.15, 0.85, 0.45, 0.05)
                plan_img = Image.open(uploaded_plan)
                fig_overlay = render_matplotlib_lakinh(
                    quai_num, exact_deg, show_laser, gender, eff_year,
                    current_van, xk_chart, annual_chart, monthly_chart, alpha_bg=opacity_val
                )
                ax_img = fig_overlay.add_axes([0.08, 0.08, 0.84, 0.84], zorder=-1)
                ax_img.imshow(plan_img)
                ax_img.axis('off')
                st.pyplot(fig_overlay, transparent=True)
            else:
                st.info("⬆️ Vui lòng tải lên tệp hình ảnh bản vẽ mặt bằng để kích hoạt tính năng soi cung vị trên kiến trúc thực tế.")
else:
    st.info("👈 Vui lòng nhập thông số cá nhân ở thanh bên trái và bấm nút '🔮 Lập Bản Đồ La Kinh Chuyên Sâu' để khởi tạo đồ họa hiển thị.")
