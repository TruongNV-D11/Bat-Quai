import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np
import time as time_mod
from datetime import datetime, time as dt_time

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

st.title("☸️ PROFESSIONAL FENG SUI MASTER BAGUA ENGINE v21.0")
st.markdown("Hệ thống Khí số Chuyên sâu: Tinh bàn Huyền Không 3 Sao (Vận - Sơn - Hướng), Phi Tinh Lưu Niên/Lưu Nguyệt, Bát Trạch Cung Phi và Vòng 120 Phân Kim.")

# --- 1. DỮ LIỆU HỌC THUẬT: 24 SƠN HƯỚNG (KÈM NGUYÊN LONG & ÂM DƯƠNG) ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# yuan_long: 0 = Địa Nguyên Long, 1 = Thiên Nguyên Long, 2 = Nhân Nguyên Long
# polarity: 1 = Dương (Phi Thuận), -1 = Âm (Phi Nghịch) theo quy tắc Tam Nguyên Long Lạc Thư
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

# Quy tắc Âm Dương của 9 số Lạc Thư theo Tam Nguyên Long [Số sao][Nguyên Long: 0=Địa, 1=Thiên, 2=Nhân]
# 1 = Dương (Thuận), -1 = Âm (Nghịch). Với sao 5 (Ngũ Hoàng), lấy theo Âm Dương của Sơn/Hướng gốc.
STAR_POLARITY = {
    1: [1, -1, -1],   # Nhâm(+), Tý(-), Quý(-)
    2: [-1, 1, 1],    # Mùi(-), Khôn(+), Thân(+) -> Lưu ý: Khôn(Địa +, Thân Nhân +, Mùi Thiên -) -> Chuẩn Huyền Không: Khôn(+), Mùi(-), Thân(-) => Địa: +, Thiên: -, Nhân: -
    3: [1, -1, -1],   # Giáp(+), Mão(-), Ất(-)
    4: [1, -1, -1],   # Tốn(+), Thìn(-), Tỵ(-)
    6: [1, -1, -1],   # Càn(+), Tuất(-), Hợi(-)
    7: [1, -1, -1],   # Canh(+), Dậu(-), Tân(-)
    8: [1, -1, -1],   # Cấn(+), Sửu(-), Dần(-)
    9: [1, -1, -1],   # Bính(+), Ngọ(-), Đinh(-)
}
# Lưu ý học thuật chuẩn: Trong 8 quẻ Hậu Thiên, cả 8 cung đều có:
# Địa Nguyên Long (Nhâm, Cấn, Giáp, Tốn, Bính, Khôn, Canh, Càn) = DƯƠNG (+1)
# Thiên Nguyên Long (Tý, Sửu, Mão, Thìn, Ngọ, Mùi, Dậu, Tuất) = ÂM (-1)
# Nhân Nguyên Long (Quý, Dần, Ất, Tỵ, Đinh, Thân, Tân, Hợi) = ÂM (-1)

STAR_NAMES = {
    1: "Nhất Bạch (1)", 2: "Nhị Hắc (2)", 3: "Tam Bích (3)", 
    4: "Tứ Lục (4)", 5: "Ngũ Hoàng (5)", 6: "Lục Bạch (6)", 
    7: "Thất Xích (7)", 8: "Bát Bạch (8)", 9: "Cửu Tử (9)"
}

STAR_SHORT = {
    1: "1 Bạch", 2: "2 Hắc", 3: "3 Bích",
    4: "4 Lục", 5: "5 Hoàng", 6: "6 Bạch",
    7: "7 Xích", 8: "8 Bạch", 9: "9 Tử"
}

LO_SHU_BASE = {
    "Bắc": 1, "Tây Nam": 2, "Đông": 3, "Đông Nam": 4,
    "Trung Cung": 5, "Tây Bắc": 6, "Tây": 7, "Đông Bắc": 8, "Nam": 9
}

def tinh_van_huyen_khong(nam_nhap_trach):
    khoang_cach = (nam_nhap_trach - 1864) // 20
    van = (khoang_cach % 9) + 1
    return van

def phi_tinh_9_cung(center_star, direction=1):
    """Phi tinh từ Trung cung qua 8 cung theo quỹ đạo Lạc Thư (5->6->7->8->9->1->2->3->4)"""
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
    """Lập Tinh bàn Huyền Không Phi Tinh 3 sao (Vận - Sơn - Hướng) & Định danh Cách cục"""
    sitting_deg = (facing_deg + 180.0) % 360.0
    facing_son = get_son_by_degree(facing_deg)
    sitting_son = get_son_by_degree(sitting_deg)
    
    # 1. Vận bàn (luôn phi thuận)
    van_chart = phi_tinh_9_cung(van_num, direction=1)
    
    # 2. Sơn bàn (lấy sao Vận tại cung Tọa nhập Trung cung)
    son_center = van_chart[sitting_son["dir"]]
    if son_center == 5:
        son_dir = sitting_son["pol"]
    else:
        son_dir = 1 if sitting_son["yuan"] == 0 else -1
    son_chart = phi_tinh_9_cung(son_center, direction=son_dir)
    
    # 3. Hướng bàn (lấy sao Vận tại cung Hướng nhập Trung cung)
    huong_center = van_chart[facing_son["dir"]]
    if huong_center == 5:
        huong_dir = facing_son["pol"]
    else:
        huong_dir = 1 if facing_son["yuan"] == 0 else -1
    huong_chart = phi_tinh_9_cung(huong_center, direction=huong_dir)
    
    # 4. Phân tích cách cục tổng thể
    s_at_sit = son_chart[sitting_son["dir"]]
    h_at_sit = huong_chart[sitting_son["dir"]]
    s_at_fac = son_chart[facing_son["dir"]]
    h_at_fac = huong_chart[facing_son["dir"]]
    
    if s_at_sit == van_num and h_at_fac == van_num:
        cach_cuc = "🌟 VƯỢNG SƠN VƯỢNG HƯỚNG (Đại Cát - Đinh Tài Lưỡng Vượng)"
        cach_cuc_desc = "Đương lệnh Sơn tinh đáo Tọa, đương lệnh Hướng tinh đáo Hướng. Cực tốt cho cả nhân đinh sức khỏe lẫn tài lộc."
    elif s_at_fac == van_num and h_at_fac == van_num:
        cach_cuc = "💧 SONG TINH ĐÁO HƯỚNG (Vượng Tài - Cần Thủy Pháp)"
        cach_cuc_desc = "Cả Sơn tinh và Hướng tinh đương vận đều tụ tại Hướng. Rất lợi tài lộc nếu phía trước có minh đường rộng, hồ nước hoặc ngã ba đường; phía sau cần sơn thế vững chãi để giữ đinh."
    elif s_at_sit == van_num and h_at_sit == van_num:
        cach_cuc = "⛰️ SONG TINH ĐÁO TỌA (Vượng Đinh - Lợi Nhân Đinh)"
        cach_cuc_desc = "Cả hai sao đương vận đều tụ ở Tọa. Lợi về sức khỏe, gia đạo, học hành; tài lộc phát chậm, cần bố trí thủy khí hợp lý ở phía sau hoặc kích hoạt cung tài."
    elif h_at_sit == van_num and s_at_fac == van_num:
        cach_cuc = "⚠️ THƯỢNG SƠN HẠ THỦY (Cách Cục Nghịch - Cần Hóa Giải)"
        cach_cuc_desc = "Sơn tinh đương vận chạy ra Hướng, Hướng tinh đương vận lùi về Tọa. Dễ hao tài tổn đinh nếu địa hình không đáp ứng 'Tọa không Hướng thực' (sau có nước, trước có núi cao)."
    else:
        cach_cuc = "⚖️ CÁCH CỤC BIẾN HÓA / PHỤC NGÂM - PHẢN NGÂM"
        cach_cuc_desc = "Các sao đương vận phân bố lệch cung, cần xét kỹ tổ hợp sao tại cửa chính, phòng ngủ và bếp để kích hoạt cát tinh."
        
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
    """Tính Phi Tinh Lưu Niên (nhập Trung cung nghịch mỗi năm) & Lưu Nguyệt"""
    # Mốc chuẩn: Năm 2026 (Bính Ngọ) sao Nhất Bạch (1) nhập Trung cung. Mỗi năm lùi 1 số.
    annual_center = ((1 - (survey_year - 2026) - 1) % 9) + 1
    annual_chart = phi_tinh_9_cung(annual_center, direction=1)
    
    # Lưu Nguyệt: Căn cứ Địa Chi của năm (Tý Ngọ Mão Dậu -> T1 khởi 8; Thìn Tuất Sửu Mùi -> T1 khởi 5; Dần Thân Tỵ Hợi -> T1 khởi 2)
    chi_idx = (survey_year - 1984) % 12
    if chi_idx in [0, 3, 6, 9]:      # Tý, Mão, Ngọ, Dậu
        m1_star = 8
    elif chi_idx in [1, 4, 7, 10]:   # Sửu, Thìn, Mùi, Tuất
        m1_star = 5
    else:                            # Dần, Tỵ, Thân, Hợi
        m1_star = 2
    monthly_center = ((m1_star - (survey_month - 1) - 1) % 9) + 1
    monthly_chart = phi_tinh_9_cung(monthly_center, direction=1)
    
    return annual_center, annual_chart, monthly_center, monthly_chart

def analyze_120_phan_kim(deg):
    """Phân tích Vòng 120 Phân Kim (120 ô, mỗi ô 3 độ, 5 ô trên mỗi Sơn 15 độ)"""
    deg = deg % 360.0
    son = get_son_by_degree(deg)
    
    # Tính góc lệch từ điểm bắt đầu của Sơn (0 -> 15 độ)
    offset = (deg - son["deg_start"]) % 360.0
    slot_idx = int(offset // 3.0)  # 0, 1, 2, 3, 4
    slot_idx = min(max(slot_idx, 0), 4)
    
    # Kiểm tra Đại Không Vong (ranh giới 8 quái: 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5)
    dai_khong_vong = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]
    for dkv in dai_khong_vong:
        if abs(deg - dkv) <= 1.0 or abs(deg - dkv) >= 359.0:
            return son, slot_idx, "ĐẠI KHÔNG VONG", "🔴 CỰC HUNG: Đè vạch ranh giới Bát Quái (Sai lệch âm dương khí trường)."
            
    if slot_idx == 2:
        return son, slot_idx, "CHÍNH TUYẾN (Ô 3/5 - Quy Giáp)", "🟢 CỰC VƯỢNG: Đúng tâm sơn (Chính châm), khí thuần nhất, đại cát."
    elif slot_idx in [1, 3]:
        return son, slot_idx, f"VƯỢNG TƯỚNG (Ô {slot_idx+1}/5 - Phân Kim Cát)", "🔵 CÁT: Nằm trong vùng vượng khí của sơn, sử dụng tốt."
    else:
        return son, slot_idx, f"CÔ HƯ / TIỂU KHÔNG VONG (Ô {slot_idx+1}/5)", "🟠 HUNG / CÔ HƯ: Sát ranh giới chuyển sơn (tuyến Không Vong / Quy Giáp lệch), khí tạp, nên vi chỉnh hướng thêm 2°-3° vào tâm sơn."

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
    
    st.markdown("---")
    st.subheader("⏳ Thời Gian & Lưu Niên")
    build_year = st.number_input("Năm Xây Nhà / Nhập Trạch (Tính Vận)", min_value=1864, max_value=2100, value=2026, step=1)
    current_van = tinh_van_huyen_khong(build_year)
    
    col_y, col_m = st.columns(2)
    with col_y:
        survey_year = st.number_input("Năm Lưu Niên", min_value=1900, max_value=2100, value=2026, step=1)
    with col_m:
        survey_month = st.selectbox("Tháng Tiết Khí", list(range(1, 13)), index=10) # Tháng 11 (Bính Tý/Kỷ Hợi)
        
    st.info(f"📌 Vận Trạch: **Vận {current_van}** | Lưu Niên: **{survey_year}**")
    
    st.markdown("---")
    st.subheader("🧭 Đo Đạc Thực Địa (Số Độ)")
    quick_dir = st.selectbox(
        "Chọn nhanh phương vị (hoặc nhập độ chính xác bên dưới)",
        list(DIRECTION_ANGLES.keys()), index=1 # Mặc định Đông Bắc (45°)
    )
    exact_deg = st.number_input(
        "Số độ Hướng nhà thực tế (0.0° - 360.0°)",
        min_value=0.0, max_value=360.0,
        value=DIRECTION_ANGLES[quick_dir], step=0.5, format="%.1f"
    )
    show_laser = st.checkbox("Hiển thị Tia Chỉ Hướng & Tọa độ", value=True)
    
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
            <i>System: Master Bagua Engine v21.0</i>
        </div>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ LA KINH 7 TẦNG CHUYÊN NGHIỆP ---
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
        
    # TẦNG 1 (r: 0.30 -> 0.50): TINH BÀN HUYỀN KHÔNG 3 SAO (SƠN - HƯỚNG / VẬN)
    for dir_name, angle in DIRECTION_ANGLES.items():
        p_info = xk_chart["palaces"][dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.30, height=0.20,
               color='#111827', alpha=0.95, edgecolor='#30363d', linewidth=1.0)
        rot_angle = get_text_rotation(angle)
        # Hiển thị chuẩn Tinh bàn: Sơn [trái] - Hướng [phải] / Vận [dưới]
        star_text = f"S:{p_info['son']} | H:{p_info['huong']}\n[V:{p_info['van']}]"
        ax.text(rad, 0.40, star_text, color='#38bdf8', fontsize=6.4, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # TẦNG 2 (r: 0.50 -> 0.66): PHI TINH LƯU NIÊN & LƯU NGUYỆT
    for dir_name, angle in DIRECTION_ANGLES.items():
        y_star = annual_chart[dir_name]
        m_star = monthly_chart[dir_name]
        rad = np.radians(angle)
        # Tô nền cảnh báo nhẹ nếu gặp Ngũ Hoàng (5) hoặc Nhị Hắc (2) Lưu Niên
        cell_bg = '#2c1518' if y_star in [2, 5] else ('#122620' if y_star in [1, 8, 9] else '#161b22')
        ax.bar(rad, width=np.radians(45), bottom=0.50, height=0.16,
               color=cell_bg, alpha=0.95, edgecolor='#30363d', linewidth=0.9)
        rot_angle = get_text_rotation(angle)
        ym_text = f"N:{y_star} | T:{m_star}"
        ym_color = '#ff7b72' if y_star in [2, 5] else ('#3fb950' if y_star in [1, 8, 9] else '#d2a8ff')
        ax.text(rad, 0.58, ym_text, color=ym_color, fontsize=6.5, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # TẦNG 3 (r: 0.66 -> 0.85): 8 HƯỚNG BÁT TRẠCH CÁT / HUNG
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.66, height=0.19,
               color=info["color"], alpha=0.9, edgecolor='white', linewidth=1.1)
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.755, info['cat_hung'], color='white', fontsize=8.0, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # TẦNG 4 (r: 0.85 -> 1.02): QUẺ VỊ HẬU THIÊN BÁT QUÁI
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.85, height=0.17,
               color='#1f242c', alpha=0.95, edgecolor='#30363d', linewidth=1.0)
        trig_text = f"{info['trigram']} {info['name']}"
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.935, trig_text, color='#f0f6fc', fontsize=7.5,
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # TẦNG 5 (r: 1.02 -> 1.24): 24 SƠN HƯỚNG - ĐỊA BÀN CHÍNH CHÂM
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=1.02, height=0.22,
               color='#161b22', alpha=0.9, edgecolor='#30363d', linewidth=0.8)
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.13, son['name'], color='#58a6ff', fontsize=7.8, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')
                
    # TẦNG 6 (r: 1.24 -> 1.42): NGŨ HÀNH NẠP ÂM 24 SƠN
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=1.24, height=0.18,
               color='#0d1117', alpha=0.9, edgecolor='#30363d', linewidth=0.6)
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.33, son['elem'], color='#c9d1d9', fontsize=6.8,
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor')

    # TẦNG 7 (r: 1.42 -> 1.50): VÒNG 120 PHÂN KIM (120 Ô x 3°, 5 Ô / SƠN)
    for son in SON_HUONG_24:
        for slot in range(5):
            slot_start = (son["deg_start"] + slot * 3.0) % 360.0
            slot_mid = (slot_start + 1.5) % 360.0
            rad_pk = np.radians(slot_mid)
            # Ô 2 (index 2) là Chính tuyến cực vượng, Ô 1 & 3 là Vượng Tướng, Ô 0 & 4 là Cô Hư/Không Vong
            if slot == 2:
                pk_color = '#2ea043'      # Xanh lá sáng - Chính Tuyến
            elif slot in [1, 3]:
                pk_color = '#1f6feb'      # Xanh dương - Vượng Tướng
            else:
                pk_color = '#30363d'      # Xám tối - Cô Hư / Giáp ranh
            ax.bar(rad_pk, width=np.radians(3.0), bottom=1.42, height=0.08,
                   color=pk_color, alpha=0.9, edgecolor='#0b0f19', linewidth=0.4)

    # VÒNG NGOÀI CÙNG (r: 1.50 -> 1.56): VẠCH CHIA ĐỘ CHI TIẾT (1° VÀ 5° ĐẾN 360°)
    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        if d_tick % 15 == 0:
            line_len = 0.055
            lw = 1.2
            col = '#FFD700'
        elif d_tick % 5 == 0:
            line_len = 0.035
            lw = 0.8
            col = 'white'
        else:
            line_len = 0.018
            lw = 0.4
            col = '#6e7681'
        ax.plot([rad_t, rad_t], [1.50, 1.50 + line_len], color=col, lw=lw)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.65, f"{d_tick}°", color='#c9d1d9', fontsize=7.5, ha='center', va='center')
            
    # THẬP TỰ THIÊN TÂM 4 CHIỀU (DỌC & NGANG)
    ax.plot([0, np.pi], [1.50, 1.50], color='#ff7b72', linestyle='--', lw=1.1, alpha=0.75, zorder=10)
    ax.plot([np.pi/2, 3*np.pi/2], [1.50, 1.50], color='#58a6ff', linestyle='--', lw=1.1, alpha=0.75, zorder=10)
    
    # TIA LASER CHỈ HƯỚNG (XANH NGỌC) & TỌA (VÀNG CAM)
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        # Tia Hướng
        ax.annotate('', xy=(fac_rad, 1.52), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.0, width=1.8, headwidth=8),
                    zorder=14)
        # Tia Tọa (nét đứt vàng)
        ax.plot([0, sit_rad], [0, 1.50], color='#FFD700', linestyle=':', lw=1.8, alpha=0.9, zorder=13)
                    
    # TRUNG CUNG / THIÊN TRÌ & KIM LA BÀN CHÌM
    ax.fill([0, 0.15, np.pi, -0.15], [0.85, 0.12, 0, 0.12], color='#FF3333', alpha=0.4, zorder=4)
    ax.fill([np.pi, np.pi - 0.15, 0, np.pi + 0.15], [0.85, 0.12, 0, 0.12], color='#E0E0E0', alpha=0.3, zorder=4)
    ax.scatter([0], [0], color='#FFD700', s=20, zorder=12, edgecolors='black', linewidth=0.5)
    
    group_name = "Đông Tứ Mệnh" if quai_num in [1, 3, 4, 9] else "Tây Tứ Mệnh"
    center_text = f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str} ({eff_year})\n{group_name}"
    ax.text(0, 0, center_text, color='#ff7b72', fontsize=7.0, fontweight='bold',
            ha='center', va='center', zorder=15,
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.4))
            
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
    
    # Tính toán các hệ thống chuyên sâu
    xk_chart = compute_full_xuan_kong_chart(current_van, exact_deg)
    ann_center, annual_chart, mon_center, monthly_chart = get_annual_monthly_stars(survey_year, survey_month)
    pk_son, pk_slot, pk_title, pk_desc = analyze_120_phan_kim(exact_deg)
    
    if st.session_state.play_spin:
        spin_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 420px; background-color: #0b0f19; color: #f0f6fc; font-family: sans-serif;">
            <div id="compass-container" style="position: relative; width: 240px; height: 240px; border: 4px solid #58a6ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #161b22 0%, #0d1117 100%); box-shadow: 0 0 25px rgba(88, 166, 255, 0.4); animation: spinCompass 2.5s cubic-bezier(0.15, 0.85, 0.15, 1.0) forwards;">
                <div style="font-size: 46px;">☸️</div>
                <div style="position: absolute; top: 10px; font-weight: bold; color: #ff7b72; font-size: 13px;">BẮC (0°)</div>
                <div style="position: absolute; bottom: 10px; font-weight: bold; color: #8b949e; font-size: 13px;">NAM (180°)</div>
            </div>
            <h3 style="margin-top: 20px; color: #58a6ff; letter-spacing: 1px;">Đang lập Tinh bàn Huyền Không 3 Sao & 120 Phân Kim (v21.0)...</h3>
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
            components.html(spin_html, height=430)
            time_mod.sleep(2.5)
        placeholder.empty()
        st.session_state.play_spin = False

    col_left, col_right = st.columns([1.25, 1.75])
    with col_left:
        st.subheader("📋 Báo cáo Khí số Chuyên môn")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Can Chi Niên Mệnh", f"{can} {chi} ({eff_year})")
            st.metric("Vận Trạch", f"Vận {current_van} ({build_year})")
        with c2:
            st.metric("Nhóm Mệnh", group_name)
            st.metric("Lưu Niên / Nguyệt", f"N:{ann_center} | T:{mon_center}")
            
        # KẾT QUẢ PHÂN TÍCH 120 PHÂN KIM & TỌA HƯỚNG
        st.markdown("### 🎯 Phân Tích Tọa Hướng & 120 Phân Kim")
        st.info(
            f"**Tọa {xk_chart['sitting_son']['name']} ({xk_chart['sitting_deg']:.1f}°) — Hướng {xk_chart['facing_son']['name']} ({exact_deg:.1f}°)**\n\n"
            f"- **Phân Kim ({pk_title}):** {pk_desc}\n"
            f"- **Bát Trạch Hướng Nhà:** {mapping[xk_chart['facing_son']['dir']]['cat_hung']} ({mapping[xk_chart['facing_son']['dir']]['type']})\n"
            f"- **Quỹ đạo Phi Tinh:** Sơn tinh phi **{xk_chart['son_pol']}** | Hướng tinh phi **{xk_chart['huong_pol']}**"
        )
        
        st.success(f"**{xk_chart['cach_cuc']}**\n\n{xk_chart['cach_cuc_desc']}")

        # CẢNH BÁO LƯU NIÊN & LƯU NGUYỆT
        st.markdown(f"### 📅 Phi Tinh Lưu Niên ({survey_year}) & Tháng {survey_month}")
        ngu_hoang_dir = [k for k, v in annual_chart.items() if v == 5 and k != "Trung Cung"]
        nhi_hac_dir = [k for k, v in annual_chart.items() if v == 2 and k != "Trung Cung"]
        tai_loc_dirs = [k for k, v in annual_chart.items() if v in [1, 8, 9] and k != "Trung Cung"]
        
        st.markdown(f"""
            <div class="advice-box" style="border-left-color: #ff7b72;">
                <b>⚠️ Hung Tinh Lưu Niên cần hóa giải:</b><br>
                • <b>Ngũ Hoàng Đại Sát (5):</b> Bay tới cung <b>{', '.join(ngu_hoang_dir)}</b> (Tránh động thổ, sửa chữa, đặt chuông gió kim loại tĩnh để hóa giải).<br>
                • <b>Nhị Hắc Bệnh Phù (2):</b> Bay tới cung <b>{', '.join(nhi_hac_dir)}</b> (Giữ sạch sẽ, thoáng khí, dùng hành Kim tiết khí Thổ).
            </div>
            <div class="advice-box" style="border-left-color: #3fb950;">
                <b>✨ Cát Tinh Lưu Niên kích hoạt Tài Lộc:</b><br>
                • Các sao vượng <b>Nhất Bạch (1), Bát Bạch (8), Cửu Tử (9)</b> đang chiếu tại: <b>{', '.join(tai_loc_dirs)}</b>.
            </div>
        """, unsafe_allow_html=True)

        # GỢI Ý CÔNG NĂNG BÁT TRẠCH
        st.markdown("### 🏛️ Bố trí Công năng Bát Trạch")
        for d_key, info in mapping.items():
            if info["type"] == "Cát":
                p_xk = xk_chart["palaces"][d_key]
                st.markdown(f"""
                    <div class="advice-box">
                        <b>{d_key} ({info['cat_hung']} - Cát | Sơn {p_xk['son']} - Hướng {p_xk['huong']}):</b> Ưu tiên đặt {('Cửa chính / Phòng khách' if info['cat_hung']=='Sinh Khí' else ('Phòng ngủ / Giường ngủ' if info['cat_hung']=='Thiên Y' else 'Bàn thờ / Văn phòng'))}.
                    </div>
                """, unsafe_allow_html=True)
                
    with col_right:
        st.subheader("🧭 Đồ họa La Kinh Huyền Không 7 Tầng & 120 Phân Kim")
        fig_mpl = render_matplotlib_lakinh(
            quai_num, exact_deg, show_laser, gender, eff_year, current_van,
            xk_chart, annual_chart, monthly_chart
        )
        st.pyplot(fig_mpl)
        
        # BẢNG CỬU CUNG TINH BÀN HUYỀN KHÔNG TRỰC QUAN (3x3)
        st.markdown("#### 🔢 Ma Trận Cửu Cung Huyền Không Phi Tinh (Sơn Tinh | Hướng Tinh / Vận Tinh)")
        grid_rows = [
            ["Đông Nam", "Nam", "Tây Nam"],
            ["Đông", "Trung Cung", "Tây"],
            ["Đông Bắc", "Bắc", "Tây Bắc"]
        ]
        for row in grid_rows:
            cols = st.columns(3)
            for idx, p_name in enumerate(row):
                p_data = xk_chart["palaces"][p_name]
                y_s = annual_chart[p_name]
                m_s = monthly_chart[p_name]
                border_col = "#00ffcc" if p_name == xk_chart["facing_son"]["dir"] else ("#FFD700" if p_name == xk_chart["sitting_son"]["dir"] else "#30363d")
                tag = " [HƯỚNG]" if p_name == xk_chart["facing_son"]["dir"] else (" [TỌA]" if p_name == xk_chart["sitting_son"]["dir"] else "")
                with cols[idx]:
                    st.markdown(f"""
                        <div class="palace-card" style="border: 1.5px solid {border_col};">
                            <div style="font-size: 11px; color: #8b949e;"><b>{p_name.upper()}{tag}</b></div>
                            <div style="font-size: 16px; font-weight: bold; color: #f0f6fc; margin: 4px 0;">
                                <span style="color: #ff7b72;">{p_data['son']}</span> &nbsp;|&nbsp; <span style="color: #38bdf8;">{p_data['huong']}</span>
                            </div>
                            <div style="font-size: 12px; color: #c9d1d9;">Vận: <b>{p_data['van']}</b> &nbsp;•&nbsp; N:<b>{y_s}</b> / T:<b>{m_s}</b></div>
                        </div>
                    """, unsafe_allow_html=True)
else:
    st.info("👈 Vui lòng nhập thông số cá nhân, năm xây nhà, số độ thực địa ở thanh bên trái và bấm nút **'🔮 Lập Bản Đồ La Kinh Chuyên Sâu'**.")
