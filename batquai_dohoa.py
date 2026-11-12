import streamlit as st
import streamlit.components.v1 as components
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io
import time as time_mod
from datetime import datetime, time as dt_time
from PIL import Image

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v28.0",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f0f6fc; }
    .stMetric { background-color: #161b22; padding: 10px !important; border-radius: 8px; border: 1px solid #30363d; }
    .signature-box { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        padding: 8px; 
        border-radius: 6px; 
        font-size: 11px; 
        color: #8b949e; 
        margin-top: 15px;
    }
    .advice-box {
        background-color: #161b22;
        border-left: 3px solid #58a6ff;
        padding: 8px 10px;
        border-radius: 4px;
        margin-bottom: 8px;
        font-size: 12.5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☸️ PROFESSIONAL FENG SUI MASTER BAGUA ENGINE v28.0")
st.markdown("Hệ thống lập bản đồ Khí số chuẩn Thầy Phong thủy: Tam Nguyên Cửu Vận, Tinh Bàn Huyền Không, Thần Sát Hàng Năm, Áp Mặt Bằng & Quản Lý Hồ Sơ Cục Bộ.")

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

STAR_META = {
    1: {"name": "1 Bạch", "elem": "Thủy", "bg": "#1e3a8a", "fg": "#93c5fd", "type": "Cát"},
    2: {"name": "2 Hắc",  "elem": "Thổ",  "bg": "#7f1d1d", "fg": "#fca5a5", "type": "Hung"},
    3: {"name": "3 Bích", "elem": "Mộc",  "bg": "#7c2d12", "fg": "#fdba74", "type": "Hung"},
    4: {"name": "4 Lục",  "elem": "Mộc",  "bg": "#14532d", "fg": "#86efac", "type": "Bình"},
    5: {"name": "5 Hoàng","elem": "Thổ",  "bg": "#991b1b", "fg": "#fef08a", "type": "Đại Hung"},
    6: {"name": "6 Bạch", "elem": "Kim",  "bg": "#334155", "fg": "#f1f5f9", "type": "Cát"},
    7: {"name": "7 Xích", "elem": "Kim",  "bg": "#4c1d95", "fg": "#f5d0fe", "type": "Hung"},
    8: {"name": "8 Bạch", "elem": "Thổ",  "bg": "#713f12", "fg": "#fde047", "type": "Cát"},
    9: {"name": "9 Tử",   "elem": "Hỏa",  "bg": "#831843", "fg": "#fde047", "type": "Đại Cát"}
}

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
    elif palaces[f_dir]["huong"] == van_num and palaces[f_dir]["huong"] == van_num:
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

def get_annual_shanshen(year_num):
    chi_idx = (year_num - 1984) % 12
    chi_names = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    year_chi = chi_names[chi_idx]
    
    chi_to_dir = {
        "Tý": "Bắc", "Ngọ": "Nam", "Mão": "Đông", "Dậu": "Tây",
        "Thìn": "Đông Nam", "Tuất": "Tây Bắc", "Sửu": "Đông Bắc", "Mùi": "Tây Nam",
        "Dần": "Đông Bắc", "Thân": "Tây Nam", "Tỵ": "Đông Nam", "Hợi": "Tây Bắc"
    }
    tai_sui_dir = chi_to_dir.get(year_chi, "Bắc")
    
    opposite_dir = {
        "Bắc": "Nam", "Nam": "Bắc", "Đông": "Tây", "Tây": "Đông",
        "Đông Bắc": "Tây Nam", "Tây Nam": "Đông Bắc", "Đông Nam": "Tây Bắc", "Tây Bắc": "Đông Nam"
    }
    sui_po_dir = opposite_dir.get(tai_sui_dir, "Nam")
    
    annual_center = ((11 - (year_num % 9)) % 9)
    if annual_center == 0: annual_center = 9
    ngu_hoang_dir = "Trung Cung"
    for d_name, p_num in BASE_PALACE_MAP.items():
        if p_num == annual_center:
            ngu_hoang_dir = d_name
            break
            
    return {
        "year_chi": year_chi,
        "tai_sui": tai_sui_dir,
        "sui_po": sui_po_dir,
        "ngu_hoang": ngu_hoang_dir
    }

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

BAT_TRACH_MAPPING = {
    1: {  # Khảm
        "Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☰", "name": "CÀN"}
    },
    9: {  # Ly
        "Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☰", "name": "CÀN"}
    },
    3: {  # Chấn
        "Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☰", "name": "CÀN"}
    },
    4: {  # Tốn
        "Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☰", "name": "CÀN"}
    },
    6: {  # Càn
        "Bắc": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☰", "name": "CÀN"}
    },
    2: {  # Khôn
        "Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☰", "name": "CÀN"}
    },
    7: {  # Đoài
        "Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☰", "name": "CÀN"}
    },
    8: {  # Cấn
        "Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#b91c1c", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1d4ed8", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9a3412", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#7f1d1d", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#4b5563", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#16a34a", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#15803d", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#0284c7", "trigram": "☰", "name": "CÀN"}
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

if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "play_spin" not in st.session_state:
    st.session_state.play_spin = False
if "saved_profiles" not in st.session_state:
    st.session_state.saved_profiles = []

with st.sidebar:
    st.header("🛠️ THAM SỐ LẬP QUẺ (MASTER)")
    
    client_name = st.text_input("Tên Khách hàng / Dự án", value="Nguyễn Văn A")
    
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
        
    st.markdown("---")
    st.subheader("🗂️ Quản lý Hồ sơ Quẻ")
    if st.button("💾 Lưu hồ sơ hiện tại vào danh sách", use_container_width=True):
        if st.session_state.initialized:
            can_p, chi_p, eff_y, q_num, g_name = compute_master_cung_phi(d_input, t_input, enable_time, gender)
            profile_item = {
                "name": client_name,
                "birth": f"{d_input.strftime('%d/%m/%Y')} ({can_p} {chi_p})",
                "gender": gender,
                "survey_year": survey_year,
                "deg": exact_deg,
                "group": g_name
            }
            st.session_state.saved_profiles.append(profile_item)
            st.success(f"Đã lưu hồ sơ của **{client_name}** thành công!")
        else:
            st.warning("Vui lòng lập bản đồ trước khi lưu.")
            
    if len(st.session_state.saved_profiles) > 0:
        with st.expander(f"📁 Danh sách hồ sơ đã lưu ({len(st.session_state.saved_profiles)})"):
            for idx, p in enumerate(st.session_state.saved_profiles):
                st.markdown(f"**{idx+1}. {p['name']}** - {p['deg']}° (Năm {p['survey_year']})")
            if st.button("🗑️ Xóa sạch danh sách"):
                st.session_state.saved_profiles = []
                st.rerun()

    st.markdown("""
    <div class="signature-box">
        <b>DIGITAL SIGNATURE</b><br>
        Engineer: TruongfNV<br>
        Email: truongnv.d11@gmail.com<br>
        Hotline: 0919855966<br>
        System: Master Bagua Engine v28.0
    </div>
    """, unsafe_allow_html=True)

def render_matplotlib_lakinh(quai_num, exact_deg_val, show_laser_flag, gender_str, eff_year, van_num, xk_chart, annual_chart, monthly_chart, survey_yr, alpha_bg=1.0, plan_img=None, rot_val=0, off_x=0, off_y=0, zoom_val=100):
    plt.close('all')
    fig = plt.figure(figsize=(10.5, 12.5))
    fig.patch.set_facecolor('#0b0f19')
    
    # 🌟 MỘT TRỤC DUY NHẤT ĐỒNG TÂM TUYỆT ĐỐI (DESCARTES KẾT HỢP POLAR OVERLAY)
    # Dùng hệ trục Descartes [0, 1] cho toàn bộ khung vẽ để dễ dàng đặt ảnh nền mặt bằng căn chỉnh chính xác 100% tại tâm
    ax_base = fig.add_axes([0.04, 0.17, 0.92, 0.81])
    ax_base.set_facecolor('#0b0f19')
    ax_base.set_xlim(-1.0, 1.0)
    ax_base.set_ylim(-1.0, 1.0)
    ax_base.axis('off')
    
    if plan_img is not None:
        scale_f = zoom_val / 100.0
        if rot_val != 0:
            p_img = plan_img.rotate(rot_val, expand=True)
        else:
            p_img = plan_img
        img_arr = np.array(p_img)
        
        # Tính toán tọa độ hiển thị ảnh nền đúng ngay tâm (0,0) với offset X, Y và Zoom mượt mà
        span = 1.8 * scale_f
        dx = off_x / 250.0
        dy = off_y / 250.0
        xmin = -span / 2.0 + dx
        xmax = span / 2.0 + dx
        ymin = -span / 2.0 + dy
        ymax = span / 2.0 + dy
        
        ax_base.imshow(img_arr, extent=[xmin, xmax, ymin, ymax], alpha=1.0, zorder=1)

    # Đặt trục cực (polar=True) đè khít hoàn hảo lên trên trục nền với cùng tỷ lệ khung
    ax = fig.add_axes([0.04, 0.17, 0.92, 0.81], polar=True)
    ax.set_facecolor('none')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.66)
    
    mapping = BAT_TRACH_MAPPING[quai_num]
    shanshen = get_annual_shanshen(survey_yr)
    
    def get_text_rotation(angle_deg):
        rot = -angle_deg
        if 90 < angle_deg <= 270:
            rot += 180
        return rot

    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        rot_angle = get_text_rotation(angle)
        
        ax.bar(bar_start, width=np.radians(45), bottom=0.68, height=0.18, align='edge',
               color=info["color"], alpha=0.88 * alpha_bg, edgecolor='#ffffff', linewidth=1.0, zorder=2)
        ax.text(rad, 0.77, info['cat_hung'], color='#ffffff', fontsize=8.8, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=4)
                
        palace_label = f"{info['trigram']} {info['name']}"
        if dir_name == shanshen["tai_sui"]:
            palace_label += "\n🚩[Thái Tuế]"
        elif dir_name == shanshen["sui_po"]:
            palace_label += "\n⚡[Tuế Phá]"
        elif dir_name == shanshen["ngu_hoang"]:
            palace_label += "\n⚠️[Ngũ Hoàng]"
            
        ax.bar(bar_start, width=np.radians(45), bottom=0.86, height=0.18, align='edge',
               color='#1f242c', alpha=0.92 * alpha_bg, edgecolor='#30363d', linewidth=1.0, zorder=2)
        ax.text(rad, 0.95, palace_label, color='#fde047' if "Phá" in palace_label or "Hoàng" in palace_label or "Tuế" in palace_label else '#f0f6fc', 
                fontsize=7.5 if "\n" in palace_label else 8.2, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=4)

    elem_colors = {"Thủy": "#38bdf8", "Mộc": "#4ade80", "Hỏa": "#f87171", "Thổ": "#facc15", "Kim": "#e2e8f0"}
    for son in SON_HUONG_24:
        mid_deg = ((son["deg_start"] + son["deg_end"]) / 2) % 360
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        rot_son = get_text_rotation(mid_deg)
        
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.04, height=0.19, align='edge',
               color='#161b22', alpha=0.88 * alpha_bg, edgecolor='#30363d', linewidth=0.8, zorder=2)
        ax.text(rad_son, 1.135, son['name'], color='#58a6ff', fontsize=8.6, fontweight='bold',
                ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=4)
                
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.23, height=0.15, align='edge',
               color='#0d1117', alpha=0.88 * alpha_bg, edgecolor='#30363d', linewidth=0.6, zorder=2)
        ax.text(rad_son, 1.305, son['elem'], color=elem_colors.get(son['elem'], '#c9d1d9'), fontsize=7.4, fontweight='bold',
                ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=4)

    for son in SON_HUONG_24:
        for slot in range(5):
            slot_start = (son["deg_start"] + slot * 3.0) % 360.0
            pk_color = '#2ea043' if slot == 2 else ('#1f6feb' if slot in [1, 3] else '#30363d')
            ax.bar(np.radians(slot_start), width=np.radians(3.0), bottom=1.38, height=0.07, align='edge',
                   color=pk_color, alpha=0.88 * alpha_bg, edgecolor='#0b0f19', linewidth=0.4, zorder=2)

    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        line_len = 0.04 if d_tick % 15 == 0 else (0.025 if d_tick % 5 == 0 else 0.012)
        col = '#FFD700' if d_tick % 15 == 0 else ('white' if d_tick % 5 == 0 else '#6e7681')
        ax.plot([rad_t, rad_t], [1.45, 1.45 + line_len], color=col, lw=1.2 if d_tick % 15 == 0 else 0.4, zorder=2)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.58, f"{d_tick}°", color='#f0f6fc', fontsize=8.0, fontweight='bold', ha='center', va='center', zorder=4)

    for dir_name, angle in DIRECTION_ANGLES.items():
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        rot_angle = get_text_rotation(angle)
        
        y_star = annual_chart.get(dir_name, 1)
        m_star = monthly_chart.get(dir_name, 1)
        y_meta = STAR_META[y_star]
        
        ax.bar(bar_start, width=np.radians(45), bottom=0.48, height=0.20, align='edge',
               color=y_meta["bg"], alpha=0.95 * alpha_bg, edgecolor='#ffffff', linewidth=0.8, zorder=20)
        ym_label = f"N:{y_star} | T:{m_star}"
        ax.text(rad, 0.58, ym_label, color=y_meta["fg"], fontsize=8.2, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=25)

        p_info = xk_chart["palaces"].get(dir_name, {"son": 1, "huong": 1, "van": van_num})
        s_star = p_info['son']
        h_star = p_info['huong']
        v_star = p_info['van']
        h_meta = STAR_META[h_star]
        
        ax.bar(bar_start, width=np.radians(45), bottom=0.24, height=0.24, align='edge',
               color=h_meta["bg"], alpha=0.95 * alpha_bg, edgecolor='#cbd5e1', linewidth=0.9, zorder=20)
        xk_label = f"S:{s_star} H:{h_star}\n[V:{v_star}]"
        ax.text(rad, 0.36, xk_label, color=h_meta["fg"], fontsize=7.8, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=25)

    ax.plot([0, np.pi], [1.45, 1.45], color='#ff7b72', linestyle='--', lw=0.9, alpha=0.45, zorder=15)
    ax.plot([np.pi/2, 3*np.pi/2], [1.45, 1.45], color='#58a6ff', linestyle='--', lw=0.9, alpha=0.45, zorder=15)
    
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        ax.annotate('', xy=(fac_rad, 1.48), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.2, width=1.8, headwidth=9), zorder=30)
        ax.plot([0, sit_rad], [0, 1.45], color='#FFD700', linestyle=':', lw=2.0, alpha=0.95, zorder=29)
                    
    ax.bar(0, width=2*np.pi, bottom=0.0, height=0.24, align='edge',
           color='#090d16', alpha=1.0, edgecolor='#fde047', linewidth=1.3, zorder=32)
    ax.plot(0, 0, marker='o', markersize=6, color='#fde047', markeredgecolor='#0b0f19', zorder=36)
    
    ax.text(0, 0, f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str}\n({eff_year})", color='#fde047', fontsize=7.0, fontweight='bold',
            ha='center', va='center', zorder=35,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#0d1117', edgecolor='#fde047', lw=1.2))
            
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)
    ax.spines['polar'].set_color('#8b949e')
    
    # --- KHUNG CHÚ GIẢI PHÍA DƯỚI ---
    ax_leg = fig.add_axes([0.04, 0.015, 0.92, 0.13])
    ax_leg.set_xlim(0, 1)
    ax_leg.set_ylim(0, 1)
    ax_leg.axis('off')
    
    outer_box = mpatches.FancyBboxPatch((0.0, 0.0), 1.0, 1.0,
                                        boxstyle="round,pad=0.01,rounding_size=0.05",
                                        facecolor='#161b22', edgecolor='#58a6ff', linewidth=1.2)
    ax_leg.add_patch(outer_box)
    
    line1 = f"DỰ ÁN: {client_name}   |   NIÊN HẠN {survey_yr} ({shanshen['year_chi']})   —   🚩 Thái Tuế: {shanshen['tai_sui']}   |   ⚡ Tuế Phá: {shanshen['sui_po']}   |   ⚠️ Ngũ Hoàng: {shanshen['ngu_hoang']}"
    ax_leg.text(0.5, 0.78, line1, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#f0f6fc')
    
    line2 = "• Vòng 1: S (Sơn Tinh) | H (Hướng Tinh) | [V] (Vận Tinh)      • Vòng 2: N (Lưu Niên) | T (Lưu Nguyệt)"
    ax_leg.text(0.5, 0.52, line2, ha='center', va='center', fontsize=8.1, color='#c9d1d9')
    
    badges = [
        {"text": "9 Tử - Đại Cát (Hồng/Tím)", "bg": STAR_META[9]["bg"], "fg": STAR_META[9]["fg"], "x": 0.135, "w": 0.22},
        {"text": "1 Bạch - Cát (Xanh dương)", "bg": STAR_META[1]["bg"], "fg": STAR_META[1]["fg"], "x": 0.370, "w": 0.22},
        {"text": "8 Bạch - Tài (Vàng nâu)",   "bg": STAR_META[8]["bg"], "fg": STAR_META[8]["fg"], "x": 0.605, "w": 0.21},
        {"text": "2H, 3B, 5H - Hung (Đỏ)",    "bg": STAR_META[2]["bg"], "fg": STAR_META[2]["fg"], "x": 0.835, "w": 0.22},
    ]
    
    ax_leg.text(0.018, 0.23, "MÀU NỀN:", ha='left', va='center', fontsize=8.0, fontweight='bold', color='#8b949e')
    
    for b in badges:
        bx = b["x"] - b["w"] / 2 + 0.045
        by = 0.09
        bh = 0.28
        pill = mpatches.FancyBboxPatch((bx, by), b["w"] - 0.005, bh,
                                       boxstyle="round,pad=0.005,rounding_size=0.03",
                                       facecolor=b["bg"], edgecolor='#cbd5e1', linewidth=0.7)
        ax_leg.add_patch(pill)
        ax_leg.text(bx + (b["w"] - 0.005)/2, by + bh/2, b["text"],
                    ha='center', va='center', fontsize=7.5, fontweight='bold', color=b["fg"])
                    
    return fig

if st.session_state.initialized:
    can, chi, eff_year, quai_num, group_name = compute_master_cung_phi(d_input, t_input, enable_time, gender)
    mapping = BAT_TRACH_MAPPING[quai_num]
    xk_chart = compute_xuan_kong_chart(current_van, exact_deg)
    annual_chart, monthly_chart = get_annual_monthly_charts(survey_year, survey_month)
    son_info, khong_vong_msg = analyze_exact_degree(exact_deg)
    shanshen_info = get_annual_shanshen(survey_year)
    
    if st.session_state.play_spin:
        spin_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 400px; background-color: #0b0f19; color: #f0f6fc; font-family: sans-serif;">
            <div style="font-size: 60px; animation: spinCompass 2s infinite linear; margin-bottom: 20px;">☸️</div>
            <div style="font-size: 18px; font-weight: bold; color: #58a6ff;">Đang khởi tạo Master Engine v28.0 cho khách hàng: {client_name}...</div>
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
        time_mod.sleep(2.0)
        placeholder.empty()
        st.session_state.play_spin = False

    col_left, col_right = st.columns([0.95, 2.05])
    
    with col_left:
        st.subheader(f"📋 Khí số: {client_name}")
        c1, c2 = st.columns(2)
        c1.metric("Niên Mệnh", f"{can} {chi} ({eff_year})")
        c2.metric("Nhóm Mệnh", group_name)
        
        dir_name = son_info["dir"]
        survey_info = mapping[dir_name]
        p_facing = xk_chart["palaces"][dir_name]
        st.success(
            f"🧭 Tọa {xk_chart['sitting_son']['name']} — Hướng {son_info['name']} ({exact_deg:.1f}°):\n\n"
            f"- Bát Trạch: {survey_info['cat_hung']} ({survey_info['type']})\n"
            f"- Tinh Bàn Hướng: Sơn {STAR_META[p_facing['son']]['name']} | Hướng {STAR_META[p_facing['huong']]['name']}\n"
            f"- Cách cục: {xk_chart['cuc_dien']}\n"
            f"- Thần Sát năm {survey_year}: Thái Tuế ({shanshen_info['tai_sui']}), Ngũ Hoàng ({shanshen_info['ngu_hoang']})\n"
            f"- Phân Kim: {khong_vong_msg}"
        )
        
        st.markdown("### 🏛️ Gợi ý Bố trí Công năng")
        for d_key, info in mapping.items():
            if info["type"] == "Cát":
                p_star = xk_chart["palaces"][d_key]
                y_s = annual_chart[d_key]
                m_s = monthly_chart[d_key]
                st.markdown(f"""
                <div class="advice-box">
                    <b>{d_key} ({info['cat_hung']} - Cát):</b> Sơn {STAR_META[p_star['son']]['name']}, Hướng {STAR_META[p_star['huong']]['name']} | Niên: {STAR_META[y_s]['name']}, Tháng: {STAR_META[m_s]['name']}.<br>
                    <i>Gợi ý: Đặt {('Cửa chính / Phòng khách' if info['cat_hung']=='Sinh Khí' else ('Phòng ngủ / Giường ngủ' if info['cat_hung']=='Thiên Y' else 'Bàn thờ / Văn phòng'))}.</i>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        tab1, tab2, tab3 = st.tabs(["🧭 La Kinh Chuyên Sâu", "🏠 Áp Mặt Bằng Nhà", "📖 Hướng dẫn & Giới thiệu"])
        
        with tab1:
            fig_mpl = render_matplotlib_lakinh(
                quai_num, exact_deg, show_laser, gender, eff_year,
                current_van, xk_chart, annual_chart, monthly_chart, survey_year, alpha_bg=1.0
            )
            st.pyplot(fig_mpl)
            
            buf = io.BytesIO()
            fig_mpl.savefig(buf, format="png", dpi=300, bbox_inches='tight', facecolor=fig_mpl.get_facecolor(), edgecolor='none')
            buf.seek(0)
            st.download_button(
                label=f"📥 Tải xuống Bản vẽ La Kinh - {client_name} (PNG 300 DPI)",
                data=buf,
                file_name=f"LaKinh_{client_name.replace(' ', '_')}_{survey_year}.png",
                mime="image/png",
                use_container_width=True
            )
            
        with tab2:
            st.markdown("### 🎛️ Căn chỉnh Tâm, Góc Xoay & Thu Phóng Bản vẽ Mặt bằng")
            uploaded_plan = st.file_uploader("Chọn ảnh mặt bằng nhà (PNG/JPG)", type=["png", "jpg", "jpeg"])
            
            if uploaded_plan is not None:
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    opacity_val = st.slider("Độ trong suốt La Kinh", 0.15, 0.90, 0.45, 0.05)
                    rotate_plan = st.slider("Góc xoay mặt bằng (°)", -180, 180, 0, 1)
                with col_s2:
                    offset_x = st.slider("Dịch ngang (X)", -200, 200, 0, 5)
                    offset_y = st.slider("Dịch dọc (Y)", -200, 200, 0, 5)
                with col_s3:
                    zoom_scale = st.slider("Thu phóng bản vẽ (Zoom %)", 40, 200, 100, 5)
                    
                plan_img = Image.open(uploaded_plan)
                
                # Render đồng tâm tuyệt đối trong một hệ quy chiếu chung duy nhất
                fig_overlay = render_matplotlib_lakinh(
                    quai_num, exact_deg, show_laser, gender, eff_year,
                    current_van, xk_chart, annual_chart, monthly_chart, survey_year,
                    alpha_bg=opacity_val, plan_img=plan_img, rot_val=rotate_plan,
                    off_x=offset_x, off_y=offset_y, zoom_val=zoom_scale
                )
                
                st.pyplot(fig_overlay)
                
                buf_overlay = io.BytesIO()
                fig_overlay.savefig(buf_overlay, format="png", dpi=300, bbox_inches='tight', facecolor=fig_overlay.get_facecolor(), edgecolor='none')
                buf_overlay.seek(0)
                st.download_button(
                    label=f"📥 Tải xuống Mặt bằng áp La Kinh - {client_name} (PNG 300 DPI)",
                    data=buf_overlay,
                    file_name=f"MatBang_LaKinh_{client_name.replace(' ', '_')}_{survey_year}.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.info("⬆️ Vui lòng tải lên tệp hình ảnh bản vẽ mặt bằng để kích hoạt các thanh trượt căn chỉnh, thu phóng và tải hồ sơ.")

        with tab3:
            st.markdown("### ☸️ Giới thiệu Về Hệ thống La Kinh Kỹ Thuật Số (Master Grade v28.0)")
            st.markdown("""
            Trong phong thủy thực trạch, La Kinh là **bản đồ năng lượng không gian đa chiều**, là công cụ cốt lõi của các chuyên gia và thầy phong thủy. 
            
            Ứng dụng **Professional Feng Shui Master Bagua Engine v28.0** đã hợp nhất tuyệt đối tâm hiển thị của ảnh mặt bằng nền và vòng tròn La Kinh trên cùng một hệ quy chiếu, giải quyết triệt để 100% hiện tượng lệch tâm hoặc nhân đôi bóng.
            """)
else:
    st.info("👈 Vui lòng nhập thông tin khách hàng và thông số ở thanh bên trái, sau đó bấm nút '🔮 Lập Bản Đồ La Kinh Chuyên Sâu' để khởi tạo hệ thống.")
