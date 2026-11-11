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

    # 1. VẼ CÁC TẦNG NGOÀI TRƯỚC (ZORDER THẤP)
    # TẦNG 3: BÁT TRẠCH CÁT / HUNG
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.60, height=0.17,
               color=info["color"], alpha=0.9, edgecolor='white', linewidth=1.1, zorder=2)
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.685, info['cat_hung'], color='white', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=3)
                
    # TẦNG 4: QUẺ VỊ HẬU THIÊN
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.77, height=0.17,
               color='#1f242c', alpha=0.95, edgecolor='#30363d', linewidth=1.0, zorder=2)
        trig_text = f"{info['trigram']} {info['name']}"
        rot_angle = get_text_rotation(angle)
        ax.text(rad, 0.855, trig_text, color='#f0f6fc', fontsize=8.0, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=3)
                
    # TẦNG 5: 24 SƠN HƯỚNG
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=0.94, height=0.22,
               color='#161b22', alpha=0.9, edgecolor='#30363d', linewidth=0.8, zorder=2)
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.05, son['name'], color='#58a6ff', fontsize=8.5, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=3)
                
    # TẦNG 6: NGŨ HÀNH NẠP ÂM
    for son in SON_HUONG_24:
        mid_deg = (son["deg_start"] + son["deg_end"]) / 2
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        ax.bar(rad_son, width=np.radians(15), bottom=1.16, height=0.18,
               color='#0d1117', alpha=0.9, edgecolor='#30363d', linewidth=0.6, zorder=2)
        rot_angle = get_text_rotation(mid_deg)
        ax.text(rad_son, 1.25, son['elem'], color='#c9d1d9', fontsize=7.2, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=3)

    # TẦNG 7: VÒNG 120 PHÂN KIM
    for son in SON_HUONG_24:
        for slot in range(5):
            slot_start = (son["deg_start"] + slot * 3.0) % 360.0
            slot_mid = (slot_start + 1.5) % 360.0
            rad_pk = np.radians(slot_mid)
            pk_color = '#2ea043' if slot == 2 else ('#1f6feb' if slot in [1, 3] else '#30363d')
            ax.bar(rad_pk, width=np.radians(3.0), bottom=1.34, height=0.08,
                   color=pk_color, alpha=0.9, edgecolor='#0b0f19', linewidth=0.4, zorder=2)

    # VÒNG NGOÀI CÙNG: VẠCH CHIA ĐỘ
    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        line_len = 0.05 if d_tick % 15 == 0 else (0.03 if d_tick % 5 == 0 else 0.015)
        lw = 1.2 if d_tick % 15 == 0 else (0.8 if d_tick % 5 == 0 else 0.4)
        col = '#FFD700' if d_tick % 15 == 0 else ('white' if d_tick % 5 == 0 else '#6e7681')
        ax.plot([rad_t, rad_t], [1.42, 1.42 + line_len], color=col, lw=lw, zorder=2)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.56, f"{d_tick}°", color='#c9d1d9', fontsize=7.5, ha='center', va='center', zorder=3)

    # 2. VẼ 2 VÒNG TRONG CÙNG SAU CÙNG VỚI ZORDER CAO ĐẢM BẢO KHÔNG BỊ ĐÈ CHỮ
    # TẦNG 2: PHI TINH LƯU NIÊN & NGUYỆT (r: 0.42 -> 0.60)
    for dir_name, angle in DIRECTION_ANGLES.items():
        y_star = annual_chart[dir_name]
        m_star = monthly_chart[dir_name]
        rad = np.radians(angle)
        cell_bg = '#2c1518' if y_star in [2, 5] else ('#122620' if y_star in [1, 8, 9] else '#161b22')
        ax.bar(rad, width=np.radians(45), bottom=0.42, height=0.18,
               color=cell_bg, alpha=0.98, edgecolor='#30363d', linewidth=1.0, zorder=5)
        rot_angle = get_text_rotation(angle)
        ym_text = f"N:{y_star} | T:{m_star}"
        ym_color = '#ff7b72' if y_star in [2, 5] else ('#3fb950' if y_star in [1, 8, 9] else '#d2a8ff')
        ax.text(rad, 0.51, ym_text, color=ym_color, fontsize=7.2, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=6)

    # TẦNG 1: TINH BÀN HUYỀN KHÔNG 3 SAO (r: 0.24 -> 0.42)
    for dir_name, angle in DIRECTION_ANGLES.items():
        p_info = xk_chart["palaces"][dir_name]
        rad = np.radians(angle)
        ax.bar(rad, width=np.radians(45), bottom=0.24, height=0.18,
               color='#111827', alpha=0.98, edgecolor='#30363d', linewidth=1.0, zorder=5)
        rot_angle = get_text_rotation(angle)
        star_text = f"S:{p_info['son']} H:{p_info['huong']}\n[V:{p_info['van']}]"
        ax.text(rad, 0.33, star_text, color='#38bdf8', fontsize=7.0, fontweight='bold',
                ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=6)

    # THẬP TỰ & TIA LASER
    ax.plot([0, np.pi], [1.42, 1.42], color='#ff7b72', linestyle='--', lw=1.1, alpha=0.75, zorder=10)
    ax.plot([np.pi/2, 3*np.pi/2], [1.42, 1.42], color='#58a6ff', linestyle='--', lw=1.1, alpha=0.75, zorder=10)
    
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        ax.annotate('', xy=(fac_rad, 1.44), xytext=(0, 0),
                    arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.0, width=1.8, headwidth=8), zorder=14)
        ax.plot([0, sit_rad], [0, 1.42], color='#FFD700', linestyle=':', lw=1.8, alpha=0.9, zorder=13)
                    
    # TRUNG CUNG / THIÊN TRÌ
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
