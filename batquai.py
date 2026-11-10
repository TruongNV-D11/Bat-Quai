import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, time

st.set_page_config(
    page_title="Professional Feng Shui Master Bagua Engine v3.0",
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
st.markdown("Hệ thống lập bản đồ Khí số chuyên sâu: 24 Sơn Hướng, Bát Trạch Cát Hung và Định vị La Kinh chuẩn thực địa.")

# --- 1. DỮ LIỆU HỌC THUẬT LỤC THẬP HOA GIÁP & 24 SƠN HƯỚNG ---
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

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
        1: {"name": "Khảm", "element": "Thủy", "dir": "Chính Bắc", "angle": 0, "trigram": "☵", "palace": "Khảm Quái", "group": "Đông Tứ Mệnh"},
        8: {"name": "Cấn", "element": "Thổ", "dir": "Đông Bắc", "angle": 45, "trigram": "☶", "palace": "Cấn Quái", "group": "Tây Tứ Mệnh"},
        3: {"name": "Chấn", "element": "Mộc", "dir": "Chính Đông", "angle": 90, "trigram": "☳", "palace": "Chấn Quái", "group": "Đông Tứ Mệnh"},
        4: {"name": "Tốn", "element": "Mộc", "dir": "Đông Nam", "angle": 135, "trigram": "☴", "palace": "Tốn Quái", "group": "Đông Tứ Mệnh"},
        9: {"name": "Ly", "element": "Hỏa", "dir": "Chính Nam", "angle": 180, "trigram": "☲", "palace": "Ly Quái", "group": "Đông Tứ Mệnh"},
        2: {"name": "Khôn", "element": "Thổ", "dir": "Tây Nam", "angle": 225, "trigram": "☷", "palace": "Khôn Quái", "group": "Tây Tứ Mệnh"},
        7: {"name": "Đoài", "element": "Kim", "dir": "Chính Tây", "angle": 270, "trigram": "☱", "palace": "Đoài Quái", "group": "Tây Tứ Mệnh"},
        6: {"name": "Càn", "element": "Kim", "dir": "Tây Bắc", "angle": 315, "trigram": "☰", "palace": "Càn Quái", "group": "Tây Tứ Mệnh"}
    }
    return can, chi, eff_year, quai_num, bagua_map

# --- 2. GIAO DIỆN NHẬP LIỆU CHUYÊN SÂU ---
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
    
    run_master = st.button("🔮 Lập Bản Đồ La Kinh Chuyên Sâu", type="primary", use_container_width=True)

    st.markdown("""
        <div class="signature-box">
            <b>DIGITAL SIGNATURE</b><br>
            <b>Engineer:</b> TruongfNV<br>
            <b>Email:</b> truongnv.d11@gmail.com<br>
            <b>Hotline:</b> 0919855966<br>
            <i>System: Master Bagua Engine v3.0</i>
        </div>
    """, unsafe_allow_html=True)

# --- 3. HÀM VẼ LA KINH CHUYÊN SÂU GIỐNG MẪU THỰC TẾ ---
def render_master_lakinh(active_num, data_map, gender_str, eff_year_val):
    fig = go.Figure()
    
    # 1. Vòng ngoài cùng: 24 Sơn Hướng (Degree & Mountain labels)
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
            
        rad = np.radians(90 - mid_deg)
        x = 1.45 * np.cos(rad)
        y = 1.45 * np.sin(rad)
        
        # Vẽ nhãn tên Sơn
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="text",
            text=[f"<b>{son['name']}</b>"],
            textfont=dict(color="#f0f6fc", size=10),
            hoverinfo="text",
            hovertext=f"Sơn: {son['name']} | Phương vị: {son['sector']} | Góc: {son['deg_start']}° - {son['deg_end']}°"
        ))
        
        # Hiển thị số đo góc mốc chính
        if mid_deg % 45 == 0:
            x_deg = 1.65 * np.cos(rad)
            y_deg = 1.65 * np.sin(rad)
            fig.add_trace(go.Scatter(
                x=[x_deg], y=[y_deg], mode="text",
                text=[f"{mid_deg}°"],
                textfont=dict(color="#8b949e", size=9)
            ))

    # 2. Vòng trung gian: 8 Quái vị Bát Trạch (Cát / Hung mapping theo mẫu thực tế)
    # Định nghĩa màu nền cho từng cung (Cát: Xanh lá/Đỏ nổi bật, Hung: Xám đậm/Đỏ sậm)
    for q_id, info in data_map.items():
        rad = np.radians(90 - info["angle"])
        x_palace = 1.15 * np.cos(rad)
        y_palace = 1.15 * np.sin(rad)
        
        is_active = (q_id == active_num)
        
        # Vẽ khối quái vị chi tiết
        fig.add_trace(go.Scatter(
            x=[x_palace], y=[y_palace], mode="text",
            text=[f"<b>{info['name']}</b><br>({info['element']})"],
            textfont=dict(color="#ffffff" if is_active else "#c9d1d9", size=11),
            hoverinfo="text",
            hovertext=f"Cung: {info['palace']} | Hướng: {info['dir']} | Ngũ hành: {info['element']}"
        ))

    # 3. Vòng trong: Cửu cung bát quái và tâm Trung Cung
    fig.add_shape(type="circle", x0=-1.3, y0=-1.3, x1=1.3, y1=1.3,
                  line=dict(color="#30363d", width=2), fillcolor="#0d1117")
    fig.add_shape(type="circle", x0=-0.5, y0=-0.5, x1=0.5, y1=0.5,
                  line=dict(color="#ff7b72", width=2), fillcolor="#161b22")

    # Nội dung Trung Cung (Chủ nhà, Quẻ, Mệnh)
    active_info = data_map[active_num]
    center_text = f"<b>TRUNG CUNG</b><br>{gender_str} - {eff_year_val}<br>Quẻ: {active_info['name']}<br>({active_info['group']})"
    
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="text",
        text=[center_text],
        textfont=dict(color="#ff7b72", size=11)
    ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(range=[-1.8, 1.8], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-1.8, 1.8], showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19",
        width=700, height=700, margin=dict(l=10, r=10, t=10, b=10)
    )
    return fig

# --- 4. HIỂN THỊ KẾT QUẢ KHI BẤM NÚT ---
if run_master:
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
        
        st.info("🎯 **Chuẩn học thuật Thầy pháp:** Bản đồ hiển thị đầy đủ vòng 24 sơn hướng ngoại vi, góc độ độ số la bàn và chi tiết cung vị trung cung.")

    with col_right:
        st.subheader("🧭 Đồ họa La Kinh Chuẩn Thực Địa")
        fig_master = render_master_lakinh(quai_num, bagua_dict, gender, eff_year)
        st.plotly_chart(fig_master, use_container_width=True)
else:
    st.info("👈 **Vui lòng nhập thông số cá nhân ở thanh bên trái và bấm nút '🔮 Lập Bản Đồ La Kinh Chuyên Sâu' để khởi tạo đồ họa hiển thị.**")
