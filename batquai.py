import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, time

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f0f6fc; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

st.title("☸️ PROFESSIONAL FENG SHUI MASTER BAGUA ENGINE")
st.markdown("Hệ thống lập bản đồ Khí số chuyên sâu: 24 Sơn Hướng, Tiết Khí Lập Xuân chuẩn xác và Định vị La Kinh.")

# --- 1. DỮ LIỆU CHUẨN HỌC THUẬT LỤC THẬP HOA GIÁP & 24 SƠN HƯỚNG ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Danh sách 24 Sơn Hướng (Bắt đầu từ Bắc 0° theo chiều kim đồng hồ)
# Mỗi sơn chiếm 15 độ
SON_HUONG_24 = [
    {"name": "Nhâm", "deg_start": 337.5, "deg_end": 352.5, "sector": "Bắc"},
    {"name": "Tý", "deg_start": 352.5, "deg_end": 7.5, "sector": "Bắc"},
    {"name": "Quý", "deg_start": 7.5, "deg_end": 22.5, "sector": "Bắc"},
    {"name": "Cấn", "deg_start": 22.5, "deg_end": 37.5, "sector": "Đông Bắc"},
    {"name": "Sửu", "deg_start": 37.5, "deg_end": 52.5, "sector": "Đông Bắc"},
    {"name": "Dần", "deg_start": 52.5, "deg_end": 67.5, "sector": "Đông Bắc"},
    {"name": "Giáp", "deg_start": 67.5, "deg_end": 82.5, "sector": "Đông"},
    {"name": "Mão", "deg_start": 82.5, "deg_end": 97.5, "sector": "Đông"},
    {"name": "Ất", "deg_start": 97.5, "deg_end": 112.5, "sector": "Đông"},
    {"name": "Tốn", "deg_start": 112.5, "deg_end": 127.5, "sector": "Đông Nam"},
    {"name": "Thìn", "deg_start": 127.5, "deg_end": 142.5, "sector": "Đông Nam"},
    {"name": "Tỵ", "deg_start": 142.5, "deg_end": 157.5, "sector": "Đông Nam"},
    {"name": "Bính", "deg_start": 157.5, "deg_end": 172.5, "sector": "Nam"},
    {"name": "Ngọ", "deg_start": 172.5, "deg_end": 187.5, "sector": "Nam"},
    {"name": "Đinh", "deg_start": 187.5, "deg_end": 202.5, "sector": "Nam"},
    {"name": "Khôn", "deg_start": 202.5, "deg_end": 217.5, "sector": "Tây Nam"},
    {"name": "Mùi", "deg_start": 217.5, "deg_end": 232.5, "sector": "Tây Nam"},
    {"name": "Thân", "deg_start": 232.5, "deg_end": 247.5, "sector": "Tây Nam"},
    {"name": "Canh", "deg_start": 247.5, "deg_end": 262.5, "sector": "Tây"},
    {"name": "Dậu", "deg_start": 262.5, "deg_end": 277.5, "sector": "Tây"},
    {"name": "Tân", "deg_start": 277.5, "deg_end": 292.5, "sector": "Tây"},
    {"name": "Càn", "deg_start": 292.5, "deg_end": 307.5, "sector": "Tây Bắc"},
    {"name": "Tuất", "deg_start": 307.5, "deg_end": 322.5, "sector": "Tây Bắc"},
    {"name": "Hợi", "deg_start": 322.5, "deg_end": 337.5, "sector": "Tây Bắc"},
]

def get_can_chi_academic(solar_date, solar_time, has_time):
    year = solar_date.year
    month = solar_date.month
    day = solar_date.day
    
    # Tiết Lập Xuân chuẩn hóa (mốc 4/2 lúc 04:14 sáng)
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
        1: {"name": "Khảm", "element": "Thủy", "dir": "Bắc", "angle": 0, "trigram": "☵", "palace": "Khảm Quái"},
        8: {"name": "Cấn", "element": "Thổ", "dir": "Đông Bắc", "angle": 45, "trigram": "☶", "palace": "Cấn Quái"},
        3: {"name": "Chấn", "element": "Mộc", "dir": "Đông", "angle": 90, "trigram": "☳", "palace": "Chấn Quái"},
        4: {"name": "Tốn", "element": "Mộc", "dir": "Đông Nam", "angle": 135, "trigram": "☴", "palace": "Tốn Quái"},
        9: {"name": "Ly", "element": "Hỏa", "dir": "Nam", "angle": 180, "trigram": "☲", "palace": "Ly Quái"},
        2: {"name": "Khôn", "element": "Thổ", "dir": "Tây Nam", "angle": 225, "trigram": "☷", "palace": "Khôn Quái"},
        7: {"name": "Đoài", "element": "Kim", "dir": "Tây", "angle": 270, "trigram": "☱", "palace": "Đoài Quái"},
        6: {"name": "Càn", "element": "Kim", "dir": "Tây Bắc", "angle": 315, "trigram": "☰", "palace": "Càn Quái"}
    }
    return can, chi, eff_year, quai_num, bagua_map

# --- 2. GIAO DIỆN NHẬP LIỆU CHUYÊN SÂU ---
with st.sidebar:
    st.header("🛠️ THAM SỐ LẬP QUẺ (MASTER)")
    d_input = st.date_input("Ngày sinh (Dương lịch)", value=datetime(1990, 5, 15))
    
    enable_time = st.checkbox("Kích hoạt Giờ sinh chính xác", value=True)
    t_input = None
    if enable_time:
        t_input = st.time_input("Giờ:Phút sinh", value=time(8, 30))
        
    gender = st.selectbox("Giới tính gia chủ", ["Nam", "Nữ"])
    current_yun = st.selectbox("Tam Nguyên Cửu Vận (Vận tinh)", ["Vận 9 (2024-2043)", "Vận 8 (2004-2023)"], index=0)
    
    run_master = st.button("🔮 Lập Bản Đồ La Kinh Chuyên Sâu", type="primary", use_container_width=True)

can, chi, eff_year, quai_num, bagua_dict = compute_master_cung_phi(d_input, t_input, enable_time, gender)
target_data = bagua_dict[quai_num]

# --- 3. HÀM VẼ LA KINH 24 SƠN HƯỚNG & BÁT QUÁI (PLOTLY) ---
def render_master_lakinh(active_num, data_map):
    fig = go.Figure()
    
    # Vòng ngoài: 24 Sơn Hướng (La Kinh Layer)
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]: # Xử lý qua mốc 360 độ
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
            
        rad = np.radians(90 - mid_deg)
        x = 1.3 * np.cos(rad)
        y = 1.3 * np.sin(rad)
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="text",
            text=[f"<b>{son['name']}</b>"],
            textfont=dict(color="#8b949e", size=9),
            hoverinfo="text",
            hovertext=f"Sơn: {son['name']} | Phương vị: {son['sector']} | Góc: {son['deg_start']}° - {son['deg_end']}°"
        ))

    # Vòng trong: 8 Quái Vị chính
    fig.add_shape(type="circle", x0=-1.6, y0=-1.6, x1=1.6, y1=1.6,
                  line=dict(color="#30363d", width=2), fillcolor="#0d1117")
    fig.add_shape(type="circle", x0=-1.1, y0=-1.1, x1=1.1, y1=1.1,
                  line=dict(color="#21262d", width=1), fillcolor="#161b22")
    fig.add_shape(type="circle", x0=-0.45, y0=-0.45, x1=0.45, y1=0.45,
                  line=dict(color="#58a6ff", width=2), fillcolor="#0d1117")

    for q_id, info in data_map.items():
        rad = np.radians(90 - info["angle"])
        x = 0.85 * np.cos(rad)
        y = 0.85 * np.sin(rad)
        
        is_active = (q_id == active_num)
        color = "#f85149" if is_active else "#8b949e"
        size = 38 if is_active else 22
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="text+markers",
            marker=dict(size=size, color=color, line=dict(width=2, color="#ffffff" if is_active else "#30363d")),
            text=[f"{info['trigram']}<br>{info['name']}"],
            textfont=dict(color="white" if is_active else "#c9d1d9", size=11 if is_active else 9),
            hoverinfo="text",
            hovertext=f"Quái: {info['palace']} | Hướng: {info['dir']} | Ngũ hành: {info['element']}"
        ))
        
        fig.add_shape(type="line", x0=0, y0=0, x1=x*0.75, y1=y*0.75,
                      line=dict(color="#f85149" if is_active else "#30363d", width=2 if is_active else 1, dash="dot"))

    # Trung Cung
    active_info = data_map[active_num]
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="text",
        text=[f"<b>TRUNG CUNG</b><br>{active_info['name']}<br>({active_info['element']})"],
        textfont=dict(color="#f85149", size=13)
    ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(range=[-1.7, 1.7], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-1.7, 1.7], showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19",
        width=650, height=650, margin=dict(l=10, r=10, t=10, b=10)
    )
    return fig

# --- 4. HIỂN THỊ KẾT QUẢ CHUYÊN SÂU CHO THẦY PHONG THỦY ---
col_left, col_right = st.columns([1.3, 1.7])

with col_left:
    st.subheader("📋 Báo cáo Khí số Chuyên môn")
    st.metric("Can Chi Niên Mệnh", f"Năm {can} {chi} ({eff_year})")
    if enable_time and t_input:
        st.metric("Thời khắc Lập xuân / Giờ sinh", t_input.strftime("%H:%M"))
    st.metric("Cung Mệnh (Bát Trạch)", f"{target_data['palace']} - {target_data['name']}")
    st.metric("Ngũ Hành Bản Mệnh", target_data['element'])
    st.metric("Phương vị Chủ đạo", target_data['dir'])
    st.metric("Vận tinh áp dụng", current_yun)
    
    st.info("🎯 **Chuẩn học thuật Thầy pháp:** Bản đồ đã tích hợp hệ tọa độ 24 sơn hướng ngoại vi, cho phép định hướng chính xác kinh tuyến la bàn và đồng bộ hóa với khí vận hiện tại.")

with col_right:
    st.subheader("🧭 Đồ họa La Kinh & Trục Khí Số")
    fig_master = render_master_lakinh(quai_num, bagua_dict)
    st.plotly_chart(fig_master, use_container_width=True)

---

<ElicitationsGroup message="Để phục vụ công tác thực địa và phân tích chuyên sâu hơn nữa:">
  <Elicitation label="Tính toán chi tiết 8 hướng Cát - Hung (Sinh Khí, Ngũ Quỷ...)" query="Xuất bảng chi tiết 4 hướng Cát và 4 hướng Hung kèm theo luận giải sơn hướng cụ thể cho gia chủ."/>
  <Elicitation label="Tích hợp Phi Tinh Huyền Không (Trạch Quái)" query="Xây dựng ma trận Phi Tinh 9 ô (Sơn tinh, Hướng tinh, Vận tinh) dựa trên tọa hướng công trình và vận tinh hiện tại."/>
</ElicitationsGroup>