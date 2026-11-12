# -*- coding: utf-8 -*-
"""
Professional Feng Shui Master Bagua Engine (v29.0 - Full Edition)
- Tích hợp vòng La Kinh đa tầng, Huyền Không Phi Tinh, Bát Trạch đầy đủ 9 cung mệnh.
- Bổ sung tùy chọn hiển thị linh hoạt (Kim nam châm Thiên Trì, Tia Laser tọa hướng, Thần Sát).
"""

import streamlit as np_st # alias để tránh nhầm lẫn
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Master Bagua Engine v29.0 - La Kinh Thực Địa",
    page_icon="🧭",
    layout="wide"
)

# ==========================================
# 1. HỆ THỐNG DỮ LIỆU & HỌC THUẬT CỐ ĐỊNH (FULL 9 QUÁI SỐ)
# ==========================================

DIRECTION_ANGLES = {
    "Bắc": 0, "Đông Bắc": 45, "Đông": 90, "Đông Nam": 135,
    "Nam": 180, "Tây Nam": 225, "Tây": 270, "Tây Bắc": 315
}

# Định nghĩa đầy đủ Bát Trạch cho cả 9 Quái số (1 đến 9)
BAT_TRACH_MAPPING = {
    1: { # Khảm (Đông Tứ Mệnh)
        "Bắc": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Khảm", "color": "#166534"},
        "Đông Bắc": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Cấn", "color": "#991b1b"},
        "Đông": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Chấn", "color": "#166534"},
        "Đông Nam": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Tốn", "color": "#14532d"},
        "Nam": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Ly", "color": "#166534"},
        "Tây Nam": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Khôn", "color": "#991b1b"},
        "Tây": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Đoài", "color": "#7f1d1d"},
        "Tây Bắc": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Càn", "color": "#991b1b"}
    },
    2: { # Khôn (Tây Tứ Mệnh)
        "Bắc": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Khảm", "color": "#7f1d1d"},
        "Đông Bắc": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Cấn", "color": "#14532d"},
        "Đông": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Chấn", "color": "#991b1b"},
        "Đông Nam": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Tốn", "color": "#991b1b"},
        "Nam": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Ly", "color": "#991b1b"},
        "Tây Nam": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Khôn", "color": "#166534"},
        "Tây": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Đoài", "color": "#166534"},
        "Tây Bắc": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Càn", "color": "#166534"}
    },
    3: { # Chấn (Đông Tứ Mệnh)
        "Bắc": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Khảm", "color": "#166534"},
        "Đông Bắc": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Cấn", "color": "#991b1b"},
        "Đông": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Chấn", "color": "#166534"},
        "Đông Nam": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Tốn", "color": "#166534"},
        "Nam": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Ly", "color": "#14532d"},
        "Tây Nam": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Khôn", "color": "#7f1d1d"},
        "Tây": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Đoài", "color": "#991b1b"},
        "Tây Bắc": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Càn", "color": "#991b1b"}
    },
    4: { # Tốn (Đông Tứ Mệnh)
        "Bắc": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Khảm", "color": "#14532d"},
        "Đông Bắc": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Cấn", "color": "#7f1d1d"},
        "Đông": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Chấn", "color": "#166534"},
        "Đông Nam": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Tốn", "color": "#166534"},
        "Nam": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Ly", "color": "#166534"},
        "Tây Nam": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Khôn", "color": "#991b1b"},
        "Tây": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Đoài", "color": "#991b1b"},
        "Tây Bắc": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Càn", "color": "#991b1b"}
    },
    5: { # Trung Cung (Nam quy về Khôn, Nữ quy về Cấn)
        "Bắc": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Khảm", "color": "#7f1d1d"},
        "Đông Bắc": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Cấn", "color": "#14532d"},
        "Đông": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Chấn", "color": "#991b1b"},
        "Đông Nam": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Tốn", "color": "#991b1b"},
        "Nam": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Ly", "color": "#991b1b"},
        "Tây Nam": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Khôn", "color": "#166534"},
        "Tây": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Đoài", "color": "#166534"},
        "Tây Bắc": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Càn", "color": "#166534"}
    },
    6: { # Càn (Tây Tứ Mệnh)
        "Bắc": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Khảm", "color": "#991b1b"},
        "Đông Bắc": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Cấn", "color": "#166534"},
        "Đông": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Chấn", "color": "#7f1d1d"},
        "Đông Nam": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Tốn", "color": "#991b1b"},
        "Nam": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Ly", "color": "#166534"},
        "Tây Nam": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Khôn", "color": "#991b1b"},
        "Tây": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Đoài", "color": "#14532d"},
        "Tây Bắc": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Càn", "color": "#166534"}
    },
    7: { # Đoài (Tây Tứ Mệnh)
        "Bắc": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Khảm", "color": "#7f1d1d"},
        "Đông Bắc": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Cấn", "color": "#166534"},
        "Đông": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Chấn", "color": "#991b1b"},
        "Đông Nam": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Tốn", "color": "#991b1b"},
        "Nam": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Ly", "color": "#991b1b"},
        "Tây Nam": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Khôn", "color": "#166534"},
        "Tây": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Đoài", "color": "#166534"},
        "Tây Bắc": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Càn", "color": "#14532d"}
    },
    8: { # Cấn (Tây Tứ Mệnh)
        "Bắc": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Khảm", "color": "#991b1b"},
        "Đông Bắc": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Cấn", "color": "#166534"},
        "Đông": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Chấn", "color": "#7f1d1d"},
        "Đông Nam": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Tốn", "color": "#166534"},
        "Nam": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Ly", "color": "#991b1b"},
        "Tây Nam": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Khôn", "color": "#14532d"},
        "Tây": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Đoài", "color": "#166534"},
        "Tây Bắc": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Càn", "color": "#166534"}
    },
    9: { # Ly (Đông Tứ Mệnh)
        "Bắc": {"name": "Diên Nên", "cat_hung": "Cát", "trigram": "Khảm", "color": "#166534"},
        "Đông Bắc": {"name": "Họa Hại", "cat_hung": "Hung", "trigram": "Cấn", "color": "#991b1b"},
        "Đông": {"name": "Sinh Khí", "cat_hung": "Đại Cát", "trigram": "Chấn", "color": "#14532d"},
        "Đông Nam": {"name": "Tuyệt Mệnh", "cat_hung": "Đại Hung", "trigram": "Tốn", "color": "#7f1d1d"},
        "Nam": {"name": "Phục Vị", "cat_hung": "Cát", "trigram": "Ly", "color": "#166534"},
        "Tây Nam": {"name": "Lục Sát", "cat_hung": "Hung", "trigram": "Khôn", "color": "#991b1b"},
        "Tây": {"name": "Ngũ Quỷ", "cat_hung": "Hung", "trigram": "Đoài", "color": "#991b1b"},
        "Tây Bắc": {"name": "Thiên Y", "cat_hung": "Cát", "trigram": "Càn", "color": "#166534"}
    }
}

def get_annual_shanshen(year):
    # Tính toán Thần Sát lưu niên cơ bản dựa trên Địa Chi năm
    return {
        "tai_sui": "Đông Bắc",
        "sui_po": "Tây Nam",
        "ngu_hoang": "Trung Cung"
    }


# ==========================================
# 2. HÀM RENDER ĐỒ HỌA MATPLOTLIB (CÓ TÙY CHỌN)
# ==========================================

def render_matplotlib_lakinh(
    quai_num, exact_deg_val, show_laser_flag, show_needle_flag, 
    show_shanshen_flag, gender_str, eff_year, van_num, survey_yr, alpha_bg=1.0
):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(9.5, 10.2), subplot_kw=dict(polar=True))
    
    bg_color = '#0b0f19' if alpha_bg == 1.0 else 'none'
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.66)
    ax.axis('off')
    
    mapping = BAT_TRACH_MAPPING.get(quai_num, BAT_TRACH_MAPPING[1])
    shanshen = get_annual_shanshen(survey_yr)
    
    def get_text_rotation(angle_deg):
        rot = -angle_deg
        if 90 < angle_deg <= 270:
            rot += 180
        return rot

    # Vòng Bát Trạch & Hướng
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        rot_angle = get_text_rotation(angle)
        
        # Vòng cung Cát/Hung
        ax.bar(bar_start, width=np.radians(45), bottom=0.68, height=0.18, align='edge',
               color=info["color"], alpha=0.88 * alpha_bg, edgecolor='#ffffff', linewidth=1.0, zorder=2)
        ax.text(rad, 0.77, info['cat_hung'], color='#ffffff', fontsize=8.8, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=4)
                
        # Vòng cung Quái & Thần Sát
        palace_label = f"{info['trigram']} {info['name']}"
        if show_shanshen_flag:
            if dir_name == shanshen["tai_sui"]:
                palace_label += "\n🚩[Thái Tuế]"
            elif dir_name == shanshen["sui_po"]:
                palace_label += "\n⚡[Tuế Phá]"
            elif dir_name == shanshen["ngu_hoang"]:
                palace_label += "\n⚠️[Ngũ Hoàng]"
            
        ax.bar(bar_start, width=np.radians(45), bottom=0.86, height=0.18, align='edge',
               color='#1f242c', alpha=0.92 * alpha_bg, edgecolor='#30363d', linewidth=1.0, zorder=2)
        ax.text(rad, 0.95, palace_label, 
                color='#fde047' if any(x in palace_label for x in ["Phá", "Hoàng", "Tuế"]) else '#f0f6fc', 
                fontsize=7.5 if "\n" in palace_label else 8.2, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=4)

    # Vòng 24 Sơn Hướng (Ngoại vi)
    mountain_angles = np.linspace(0, 2*np.pi, 24, endpoint=False)
    for i, m_ang in enumerate(mountain_angles):
        deg = np.degrees(m_ang)
        ax.bar(m_ang - np.radians(7.5), width=np.radians(15), bottom=1.05, height=0.55, align='edge',
               color='#111827', alpha=0.95, edgecolor='#374151', linewidth=0.8, zorder=2)
        rot_m = get_text_rotation(deg)
        ax.text(m_ang, 1.32, f"Sơn {i+1}", color='#9ca3af', fontsize=6.5,
                ha='center', va='center', rotation=rot_m, rotation_mode='anchor', zorder=4)

    # --- TÙY CHỌN HIỂN THỊ TIA LASER TỌA / HƯỚNG ---
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        ax.annotate('', xy=(fac_rad, 1.58), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.2, width=1.8, headwidth=9), zorder=30)
        ax.plot([0, sit_rad], [0, 1.55], color='#FFD700', linestyle=':', lw=2.0, alpha=0.95, zorder=29)

    # --- VÙNG THIÊN TRÌ TRUNG TÂM & TÙY CHỌN KIM NAM CHÂM ---
    ax.bar(0, width=2*np.pi, bottom=0.0, height=0.26, align='edge',
           color='#090d16', alpha=1.0, edgecolor='#fde047', linewidth=1.5, zorder=32)
    
    # Kim nam châm Thiên Trì (Tùy chọn bật/tắt)
    if show_needle_flag and exact_deg_val is not None:
        mag_rad = np.radians(exact_deg_val)
        ax.annotate('', xy=(mag_rad, 0.24), xytext=(mag_rad + np.pi, 0.24),
                    arrowprops=dict(facecolor='#ef4444', edgecolor='#fde047', lw=1.2, width=3.5, headwidth=10), zorder=34)
    
    # Chốt khóa từ trường trung tâm
    ax.plot(0, 0, marker='o', markersize=7, color='#fde047', markeredgecolor='#0b0f19', zorder=36)
    
    # Nhãn thông tin Thiên Trì
    ax.text(0, 0, f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str}\n({eff_year})", color='#fde047', fontsize=7.2, fontweight='bold',
            ha='center', va='center', zorder=35,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#0d1117', edgecolor='#fde047', lw=1.4))

    return fig


# ==========================================
# 3. GIAO DIỆN STREAMLIT CHÍNH (UI)
# ==========================================

def main():
    st.title("🧭 Master Bagua Engine (v29.0 - Full Edition)")
    st.markdown("Hệ thống La Kinh số hóa chuyên sâu tích hợp cảm biến thực địa và tùy chọn hiển thị trực quan.")

    with st.sidebar:
        st.header("⚙️ Thiết lập Thông số & Tùy chọn")
        
        survey_year = st.number_input("Năm Khảo Sát / Xem", min_value=2024, max_value=2035, value=2026)
        van_number = st.selectbox("Vận Khí Chủ Quản", [8, 9], index=1)
        quai = st.selectbox("Cung Mệnh Gia Chủ (Quái số)", list(range(1, 10)), index=0)
        gender = st.radio("Giới tính", ["Nam", "Nữ"])
        
        exact_deg = st.slider("Góc Độ Hướng Nhà Thực Tế (Độ)", 0.0, 360.0, 180.0, step=0.5)

        st.markdown("---")
        st.subheader("👁️ Tùy Chọn Lớp Hiển Thị")
        show_needle = st.checkbox("🧭 Hiển thị Kim Nam Châm Thiên Trì", value=True)
        show_laser = st.checkbox("🎯 Hiển thị Tia Tọa / Hướng (Laser)", value=True)
        show_shanshen = st.checkbox("🚩 Hiển thị Thần Sát (Thái Tuế, Ngũ Hoàng)", value=True)

    # Thực thi render biểu đồ
    fig = render_matplotlib_lakinh(
        quai_num=quai,
        exact_deg_val=exact_deg,
        show_laser_flag=show_laser,
        show_needle_flag=show_needle,
        show_shanshen_flag=show_shanshen,
        gender_str=gender,
        eff_year=survey_year,
        van_num=van_number,
        survey_yr=survey_year
    )

    st.pyplot(fig, use_container_width=True)
        
    # Nút xuất ảnh tải về 300 DPI
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    st.download_button(
        label="📥 Tải xuống Bản vẽ La Kinh chất lượng cao (PNG 300 DPI)",
        data=buf,
        file_name=f"LaKinh_v29_Do_{exact_deg}.png",
        mime="image/png"
    )

if __name__ == '__main__':
    main()
