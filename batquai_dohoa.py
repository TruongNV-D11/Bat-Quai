import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np
import time as time_mod
from datetime import datetime, time as dt_time

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v21.2",
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
    .palace-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 8px;
        text-align: center;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☸️ PROFESSIONAL FENG SUI MASTER BAGUA ENGINE v21.2")
st.markdown("Hệ thống Khí số Chuyên sâu: Tinh bàn Huyền Không 3 Sao, Lưu Niên/Lưu Nguyệt, Bát Trạch và Vòng 120 Phân Kim chuẩn thực chiến.")

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

def tinh_van_huyen_khong(nam_nhap_trach):
    khoang_cach = (nam_nhap_trach - 1864) // 20
    van = (khoang_cach % 9) + 1
    return van

def phi_tinh_9_cung(center_star, direction=1):
    matrix = {}
    for dir_name, base_val in LO_SHU_BASE.items():
        steps = (base_val - 5) % 9
        star = ((center_star - 1 + direction * steps) % 9) + 1
        matrix[dir_name] = star
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
    huong_dir = facing_son["pol"] if huong_center == 5 else (1 if facing_son["yuan"] == 0 else -1)
    huong_chart = phi_tinh_9_cung(huong_center, direction=huong_dir)
    
    s_at_sit = son_chart[sitting_son["dir"]]
    h_at_fac = huong_chart[facing_son["dir"]]
    
    if s_at_sit == van_num and h_at_fac == van_num:
        cach_cuc = "🌟 VƯỢNG SƠN VƯỢNG HƯỚNG (Đại Cát)"
        cach_cuc_desc = "Đương lệnh Sơn tinh đáo Tọa, Hướng tinh đáo Hướng. Cực tốt cho cả nhân đinh và tài lộc."
    elif son_chart[facing_son["dir"]] == van_num and h_at_fac == van_num:
        cach_cuc = "💧 SONG TINH ĐÁO HƯỚNG (Vượng Tài)"
        cach_cuc_desc = "Cả Sơn tinh và Hướng tinh đương vận tụ tại Hướng. Lợi tài lộc nếu phía trước có thủy."
    elif s_at_sit == van_num and huong_chart[sitting_son["dir"]] == van_num:
        cach_cuc = "⛰️ SONG TINH ĐÁO TỌA (Vượng Đinh)"
        cach_cuc_desc = "Cả hai sao đương vận tụ ở Tọa. Lợi về sức khỏe, gia đạo."
    else:
        cach_cuc = "⚖️ CÁCH CỤC BIẾN HÓA / PHẢN NGÂM"
        cach_cuc_desc = "Cần bố trí công năng hợp lý tại các cung đặc thù để kích hoạt cát tinh."
        
    full_palaces = {}
    for p_name in LO_SHU_BASE.keys():
        full_palaces[p_name] = {
            "van": van_chart[p_name],
            "son": son_chart[p_name],
            "huong": huong_chart[p_name]
        }
        
    return {
        "sitting_son": sitting_son,
        "facing_son": facing_son,
        "sitting_deg": sitting_deg,
        "facing_deg": facing_deg,
        "palaces": full_palaces,
        "cach_cuc": cach_cuc,
        "cach_cuc_desc": cach_cuc_desc,
        "son_pol": "Thuận (+)" if son_dir == 1 else "Nghịch (-)",
        "huong_pol": "Thuận (+)" if huong_dir == 1 else "Nghịch (-)"
    }

def get_annual_monthly_stars(survey_year, survey_month):
    annual_center = ((1 - (survey_year - 2026) - 1) % 9) + 1
    annual_chart = phi_tinh_9_cung(annual_center, direction=1)
    
    chi_idx = (survey_year - 1984) % 12
    m1_star = 8 if chi_idx in [0, 3, 6, 9] else (5 if chi_idx in [1, 4, 7, 10] else 2)
    monthly_center = ((m1_star - (survey_month - 1) - 1) % 9) + 1
    monthly_chart = phi_tinh_9_cung(monthly_center, direction=1)
    
    return annual_center, annual_chart, monthly_center, monthly_chart

def analyze_120_phan_kim(deg):
    deg = deg % 360.0
    son = get_son_by_degree(deg)
    offset = (deg - son["deg_start"]) % 360.0
    slot_idx = int(offset // 3.0)
    slot_idx = min(max(slot_idx, 0), 4)
    
    dai_khong_vong = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]
    for dkv in dai_khong_vong:
        if abs(deg - dkv) <= 1.0 or abs(deg - dkv) >= 359.0:
            return son, slot_idx, "ĐẠI KHÔNG VONG", "🔴 CỰC HUNG: Đè vạch ranh giới Bát Quái."
            
    if slot_idx == 2:
        return son, slot_idx, "CHÍNH TUYẾN (Ô 3/5 - Quy Giáp)", "🟢 CỰC VƯỢNG: Đúng tâm sơn, khí thuần nhất."
    elif slot_idx in [1, 3]:
        return son, slot_idx, f"VƯỢNG TƯỚNG (Ô {slot_idx+1}/5)", "🔵 CÁT: Nằm trong vùng vượng khí của sơn."
    else:
        return son, slot_idx, f"CÔ HƯ / TIỂU KHÔNG VONG (Ô {slot_idx+1}/5)", "🟠 HUNG / CÔ HƯ: Sát ranh giới chuyển sơn."

BAT_TRACH_MAPPING = {
    1: {  # Khảm
        "Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☰", "name": "CÀN"}
    },
    9: {  # Ly
        "Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
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
        "Tây Nam": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☰", "name": "CÀN"}
    },
    4: {  # Tốn
        "Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☶", "name": "CẤN"},
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
        "Nam": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☰", "name": "CÀN"}
    },
    2: {  # Khôn
        "Bắc": {"cat_hung": "Tuyệt Mệnh", "type": "Hung", "color": "#8b0000", "trigram": "☵", "name": "KHẢM"},
        "Đông Bắc": {"cat_hung": "Sinh Khí", "type": "Cát", "color": "#2ea043", "trigram": "☶", "name": "CẤN"},
        "Đông": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☳", "name": "CHẤN"},
        "Đông Nam": {"cat_hung": "Lục Sát", "type": "Hung", "color": "#6e7681", "trigram": "☴", "name": "TỐN"},
        "Nam": {"cat_hung": "Ngũ Quỷ", "type": "Hung", "color": "#da3633", "trigram": "☲", "name": "LY"},
        "Tây Nam": {"cat_hung": "Phục Vị", "type": "Cát", "color": "#1f6feb", "trigram": "☷", "name": "KHÔN"},
        "Tây": {"cat_hung": "Thiên Y", "type": "Cát", "color": "#58a6ff", "trigram": "☱", "name": "ĐOÀI"},
        "Tây Bắc": {"cat_hung": "Diên Niên", "type": "Cát", "color": "#238636", "trigram": "☰", "name": "CÀN"}
    },
    7: {  # Đoài
        "Bắc": {"cat_hung": "Họa Hại", "type": "Hung", "color": "#9e6a03", "trigram": "☵", "name": "KHẢM"},
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
    return CAN[offset % 10], CHI[offset % 12], effective_year

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
        
    quai_num = val_nam if sex == "Nam" else val_nu
    quai_num = quai_num % 9
    if quai_num == 0: quai_num = 9
    if quai_num == 5: quai_num = 2 if sex == "Nam" else 8
        
    group = "Đông Tứ Mệnh" if quai_num in [1, 3, 4, 9] else "Tây Tứ Mệnh"
    return can, chi, eff_year, quai_num, group

# --- GIAO DIỆN NHẬP LIỆU ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "play_spin" not in st.session_state:
    st.session_state.play_spin = False

with st.sidebar:
    st.header("🛠️ THAM SỐ LẬP QUẺ (MASTER)")
    d_input = st.date_input("Ngày sinh (Dương lịch)", value=datetime(1984, 9, 17), format="DD/MM/YYYY")
    enable_time = st.checkbox("Kích hoạt Giờ sinh", value=True)
    t_input = st.time_input("Giờ:Phút sinh", value=dt_time(8, 30)) if enable_time else None
    gender = st.selectbox("Giới tính gia chủ", ["Nam", "Nữ"], index=1)
    
    st.markdown("---")
    st.subheader("⏳ Thời Gian & Lưu Niên")
    build_year = st.number_input("Năm Xây Nhà / Nhập Trạch", min_value=1864, max_value=2100, value=2026, step=1)
    current_van = tinh_van_huyen_khong(build_year)
    
    col_y, col_m = st.columns(2)
    with col_y:
        survey_year = st.number_input("Năm Lưu Niên", min_value=1900, max_value=2100, value=2026, step=1)
    with col_m:
        survey_month = st.selectbox("Tháng", list(range(1, 13)), index=10)
        
    st.info(f"📌 Vận: **Vận {current_van}** | Lưu Niên: **{survey_year}**")
    
    st.markdown("---")
    st.subheader("🧭 Đo Đạc Thực Địa")
    quick_dir = st.selectbox("Chọn nhanh phương vị", list(DIRECTION_ANGLES.keys()), index=1)
    exact_deg = st.number_input("Số độ Hướng nhà (0° - 360°)", min_value=0.0, max_value=360.0, value=45.0, step=0.5, format="%.1f")
    show_laser = st.checkbox("Hiển thị Tia Chỉ Hướng & Tọa", value=True)
    
    run_btn = st.button("🔮 Lập Bản Đồ La Kinh Chuyên Sâu", type="primary", use_container_width=True)
    if run_btn:
        st.session_state.initialized = True
        st.session_state.play_spin = True

# --- HÀM VẼ LA KINH CHUẨN THỰC CHIẾN (SAFE ZORDER & FIXED RENDER) ---
def render_matplotlib_lakinh(quai_num, exact_deg_val, show_laser_flag, gender_str, eff_year, van_num, xk_chart, annual_chart, monthly_chart):
    plt.close('all')
    
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

    # 1. VẼ CÁC TẦNG BÊN NGOÀI
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        # Tầng 3: Bát Trạch
        ax.bar(rad, width=np.radians(45), bottom=0.60, height=0.17,
               color=info["color"], alpha=0.9, edgecolor='white', linewidth=1.1, zorder=2)
        ax.text(rad, 0.685, info['cat_hung'], color='white', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=get_text_rotation(angle), rotation_mode='anchor', zorder=3)
                
        # Tầng 4: Hậu Thiên Bát Quái
        ax.bar(rad, width=np.radians(45), bottom=0.77, height=0.17,
               color='#1f242c', alpha=0.95, edgecolor='#30363d', linewidth=1.0, zorder=2)
        ax.text(rad, 0.855, f"{info['trigram']} {info['name']}", color='#f0f6fc', fontsize=8.0, fontweight='bold',
                ha='center', va='center', rotation=get_text_rotation(angle), rotation_mode='anchor', zorder=3)
                
    # Tầng 5 & 6: 24 Sơn Hướng & Nạp Âm
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        rot_son = get_text_rotation(mid_deg)
        
        ax.bar(rad_son, width=np.radians(15), bottom=0.94, height=0.22,
               color='#161b22', alpha=0.9, edgecolor='#30363d', linewidth=0.8, zorder=2)
        ax.text(rad_son, 1.05, son['name'], color='#58a6ff', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)
                
        ax.bar(rad_son, width=np.radians(15), bottom=1.16, height=0.18,
               color='#0d1117', alpha=0.9, edgecolor='#30363d', linewidth=0.6, zorder=2)
        ax.text(rad_son, 1.25, son['elem'], color='#c9d1d9', fontsize=7.2, fontweight='bold',
                ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)

    # Tầng 7: 120 Phân Kim
    for son in SON_HUONG_24:
        for slot in range(5):
            slot_start = (son["deg_start"] + slot * 3.0) % 360.0
            slot_mid = (slot_start + 1.5) % 360.0
            rad_pk = np.radians(slot_mid)
            pk_color = '#2ea043' if slot == 2 else ('#1f6feb' if slot in [1, 3] else '#30363d')
            ax.bar(rad_pk, width=np.radians(3.0), bottom=1.34, height=0.08,
                   color=pk_color, alpha=0.9, edgecolor='#0b0f19', linewidth=0.4, zorder=2)

    # Vòng ngoài cùng: Chia độ
    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        line_len = 0.05 if d_tick % 15 == 0 else (0.03 if d_tick % 5 == 0 else 0.015)
        lw = 1.2 if d_tick % 15 == 0 else (0.8 if d_tick % 5 == 0 else 0.4)
        col = '#FFD700' if d_tick % 15 == 0 else ('white' if d_tick % 5 == 0 else '#6e7681')
        ax.plot([rad_t, rad_t], [1.42, 1.42 + line_len], color=col, lw=lw, zorder=2)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.56, f"{d_tick}°", color='#c9d1d9', fontsize=7.5, ha='center', va='center', zorder=3)

    # 2. VẼ 2 VÒNG TRONG CÙNG (LƯU NIÊN & HUYỀN KHÔNG 3 SAO) VỚI ZORDER CAO TUYỆT ĐỐI
    for dir_name, angle in DIRECTION_ANGLES.items():
        y_star = annual_chart[dir_name]
        m_star = monthly_chart[dir_name]
        rad = np.radians(angle)
        rot_angle = get_text_rotation(angle)
        
        # Tầng 2: Lưu Niên / Nguyệt
        cell_bg = '#2c1518' if y_star in [2, 5] else ('#122620' if y_star in [1, 8, 9] else '#161b22')
        ax.bar(rad, width=np.radians(45), bottom=0.42, height=0.18,
               color=cell_bg, alpha=0.98, edgecolor='#30363d', linewidth=1.0, zorder=5)
        ym_color = '#ff7b72' if y_star in [2, 5] else ('#3fb950' if y_star in [1, 8, 9] else '#d2a8ff')
        ax.text(rad, 0.51, f"N:{y_star} | T:{m_star}", color=ym_color, fontsize=7.2, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=6)

        # Tầng 1: Huyền Không 3 Sao
        p_info = xk_chart["palaces"][dir_name]
        ax.bar(rad, width=np.radians(45), bottom=0.24, height=0.18,
               color='#111827', alpha=0.98, edgecolor='#30363d', linewidth=1.0, zorder=5)
        ax.text(rad, 0.33, f"S:{p_info['son']} H:{p_info['huong']}\n[V:{p_info['van']}]", color='#38bdf8', fontsize=7.0, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=6)

    # Thập tự & Tia laser hướng
    ax.plot([0, np.pi], [1.42, 1.42], color='#ff7b72', linestyle='--', lw=1.1, alpha=0.75, zorder=10)
    ax.plot([np.pi/2, 3*np.pi/2], [1.42, 1.42], color='#58a6ff', linestyle='--', lw=1.1, alpha=0.75, zorder=10)
    
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        ax.annotate('', xy=(fac_rad, 1.44), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.0, width=1.8, headwidth=8), zorder=14)
        ax.plot([0, sit_rad], [0, 1.42], color='#FFD700', linestyle=':', lw=1.8, alpha=0.9, zorder=13)
                    
    # Trung cung / Thiên Trì
    ax.fill([0, 0.15, np.pi, -0.15], [0.65, 0.08, 0, 0.08], color='#FF3333', alpha=0.4, zorder=15)
    ax.fill([np.pi, np.pi - 0.15, 0, np.pi + 0.15], [0.65, 0.08, 0, 0.08], color='#E0E0E0', alpha=0.3, zorder=15)
    ax.scatter([0], [0], color='#FFD700', s=20, zorder=16, edgecolors='black', linewidth=0.5)
    
    group_name = "Đông Tứ Mệnh" if quai_num in [1, 3, 4, 9] else "Tây Tứ Mệnh"
    center_text = f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str} ({eff_year})\n{group_name}"
    ax.text(0, 0, center_text, color='#ff7b72', fontsize=7.0, fontweight='bold',
            ha='center', va='center', zorder=17,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.4))
            
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='#30363d', linestyle='--', linewidth=0.8)
    ax.spines['polar'].set_color('#8b949e')
    plt.tight_layout()
    return fig

# --- HIỂN THỊ KẾT QUẢ ---
if st.session_state.initialized:
    can, chi, eff_year, quai_num, group_name = compute_master_cung_phi(d_input, t_input, enable_time, gender)
    mapping = BAT_TRACH_MAPPING[quai_num]
    
    xk_chart = compute_full_xuan_kong_chart(current_van, exact_deg)
    ann_center, annual_chart, mon_center, monthly_chart = get_annual_monthly_stars(survey_year, survey_month)
    pk_son, pk_slot, pk_title, pk_desc = analyze_120_phan_kim(exact_deg)
    
    if st.session_state.play_spin:
        spin_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 400px; background-color: #0b0f19; color: #f0f6fc; font-family: sans-serif;">
            <div style="width: 220px; height: 220px; border: 4px solid #58a6ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #161b22 0%, #0d1117 100%); box-shadow: 0 0 25px rgba(88, 166, 255, 0.4);">
                <div style="font-size: 45px;">☸️</div>
            </div>
            <h3 style="margin-top: 20px; color: #58a6ff;">Đang khởi tạo La Kinh v21.2 (Safe Z-Order & Render)...</h3>
        </div>
        """
        placeholder = st.empty()
        with placeholder.container():
            components.html(spin_html, height=410)
            time_mod.sleep(2.0)
        placeholder.empty()
        st.session_state.play_spin = False

    col_left, col_right = st.columns([1.25, 1.75])
    with col_left:
        st.subheader("📋 Báo cáo Khí số Chuyên môn")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Can Chi", f"{can} {chi} ({eff_year})")
            st.metric("Vận Trạch", f"Vận {current_van}")
        with c2:
            st.metric("Nhóm Mệnh", group_name)
            st.metric("Lưu Niên", f"N:{ann_center} | T:{mon_center}")
            
        st.markdown("### 🎯 Phân Tích Tọa Hướng & 120 Phân Kim")
        st.info(
            f"**Tọa {xk_chart['sitting_son']['name']} ({xk_chart['sitting_deg']:.1f}°) — Hướng {xk_chart['facing_son']['name']} ({exact_deg:.1f}°)**\n\n"
            f"- **Phân Kim ({pk_title}):** {pk_desc}\n"
            f"- **Bát Trạch:** {mapping[xk_chart['facing_son']['dir']]['cat_hung']} ({mapping[xk_chart['facing_son']['dir']]['type']})"
        )
        st.success(f"**{xk_chart['cach_cuc']}**\n\n{xk_chart['cach_cuc_desc']}")

    with col_right:
        st.subheader("🧭 Đồ họa La Kinh Chuyên Sâu v21.2")
        fig_mpl = render_matplotlib_lakinh(
            quai_num, exact_deg, show_laser, gender, eff_year, current_van,
            xk_chart, annual_chart, monthly_chart
        )
        st.pyplot(fig_mpl)
else:
    st.info("👈 Vui lòng nhập thông số và bấm nút **'🔮 Lập Bản Đồ La Kinh Chuyên Sâu'** ở thanh bên trái.")
