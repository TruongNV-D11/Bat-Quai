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

    # 1. TẦNG BÁT TRẠCH & HẬU THIÊN (r: 0.68 -> 1.02)
    for dir_name, angle in DIRECTION_ANGLES.items():
        info = mapping[dir_name]
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        
        ax.bar(bar_start, width=np.radians(45), bottom=0.68, height=0.17, color=info["color"], alpha=0.9, edgecolor='white', linewidth=1.1, zorder=2)
        ax.text(rad, 0.765, info['cat_hung'], color='white', fontsize=8.5, fontweight='bold', ha='center', va='center', rotation=get_text_rotation(angle), rotation_mode='anchor', zorder=3)
                
        ax.bar(bar_start, width=np.radians(45), bottom=0.85, height=0.17, color='#1f242c', alpha=0.95, edgecolor='#30363d', linewidth=1.0, zorder=2)
        ax.text(rad, 0.935, f"{info['trigram']} {info['name']}", color='#f0f6fc', fontsize=8.0, fontweight='bold', ha='center', va='center', rotation=get_text_rotation(angle), rotation_mode='anchor', zorder=3)
                
    # 2. 24 SƠN HƯỚNG & NẠP ÂM (r: 1.02 -> 1.38)
    for son in SON_HUONG_24:
        mid_deg = ((son["deg_start"] + son["deg_end"]) / 2) % 360
        if son["deg_start"] > son["deg_end"]:
            mid_deg = ((son["deg_start"] + son["deg_end"] + 360) / 2) % 360
        rad_son = np.radians(mid_deg)
        rot_son = get_text_rotation(mid_deg)
        
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.02, height=0.20, color='#161b22', alpha=0.9, edgecolor='#30363d', linewidth=0.8, zorder=2)
        ax.text(rad_son, 1.12, son['name'], color='#58a6ff', fontsize=8.5, fontweight='bold', ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)
                
        ax.bar(np.radians(son["deg_start"]), width=np.radians(15), bottom=1.22, height=0.16, color='#0d1117', alpha=0.9, edgecolor='#30363d', linewidth=0.6, zorder=2)
        ax.text(rad_son, 1.30, son['elem'], color='#c9d1d9', fontsize=7.2, fontweight='bold', ha='center', va='center', rotation=rot_son, rotation_mode='anchor', zorder=3)

    # 3. 120 PHÂN KIM
    for son in SON_HUONG_24:
        for slot in range(5):
            slot_start = (son["deg_start"] + slot * 3.0) % 360.0
            slot_mid = (slot_start + 1.5) % 360.0
            pk_color = '#2ea043' if slot == 2 else ('#1f6feb' if slot in [1, 3] else '#30363d')
            ax.bar(np.radians(slot_start), width=np.radians(3.0), bottom=1.38, height=0.07, color=pk_color, alpha=0.9, edgecolor='#0b0f19', linewidth=0.4, zorder=2)

    # 4. VÒNG CHIA ĐỘ
    for d_tick in range(360):
        rad_t = np.radians(d_tick)
        line_len = 0.04 if d_tick % 15 == 0 else (0.025 if d_tick % 5 == 0 else 0.012)
        col = '#FFD700' if d_tick % 15 == 0 else ('white' if d_tick % 5 == 0 else '#6e7681')
        ax.plot([rad_t, rad_t], [1.45, 1.45 + line_len], color=col, lw=1.2 if d_tick % 15 == 0 else 0.4, zorder=2)
        if d_tick % 45 == 0:
            ax.text(rad_t, 1.58, f"{d_tick}°", color='#c9d1d9', fontsize=7.5, ha='center', va='center', zorder=3)

    # 5. 2 VÒNG TRONG CÙNG (ĐÃ NỚI RỘNG BÁN KÍNH VÀ THU GỌN CHỮ HIỂN THỊ RÕ RÀNG)
    for dir_name, angle in DIRECTION_ANGLES.items():
        rad = np.radians(angle)
        bar_start = np.radians(angle - 22.5)
        rot_angle = get_text_rotation(angle)
        
        # Tầng 2: Lưu Niên / Nguyệt (r: 0.48 -> 0.68)
        y_star = annual_chart[dir_name]
        m_star = monthly_chart[dir_name]
        ax.bar(bar_start, width=np.radians(45), bottom=0.48, height=0.20, color='#1c2333', alpha=0.99, edgecolor='#30363d', linewidth=1.2, zorder=10)
        ym_color = '#ff7b72' if y_star in [2, 5] else ('#3fb950' if y_star in [1, 8, 9] else '#d2a8ff')
        ax.text(rad, 0.58, f"N:{y_star} T:{m_star}", color=ym_color, fontsize=7.2, fontweight='bold', ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=12)

        # Tầng 1: Huyền Không 3 Sao (r: 0.28 -> 0.48)
        p_info = xk_chart["palaces"][dir_name]
        ax.bar(bar_start, width=np.radians(45), bottom=0.28, height=0.20, color='#111827', alpha=0.99, edgecolor='#30363d', linewidth=1.2, zorder=10)
        ax.text(rad, 0.38, f"S:{p_info['son']} H:{p_info['huong']} [V{p_info['van']}]", color='#38bdf8', fontsize=6.8, fontweight='bold', ha='center', va='center', rotation=rot_angle, rotation_mode='anchor', zorder=12)

    # Thập tự & Tia laser
    ax.plot([0, np.pi], [1.45, 1.45], color='#ff7b72', linestyle='--', lw=1.1, alpha=0.75, zorder=15)
    ax.plot([np.pi/2, 3*np.pi/2], [1.45, 1.45], color='#58a6ff', linestyle='--', lw=1.1, alpha=0.75, zorder=15)
    
    if show_laser_flag and exact_deg_val is not None:
        fac_rad = np.radians(exact_deg_val)
        sit_rad = np.radians((exact_deg_val + 180.0) % 360.0)
        ax.annotate('', xy=(fac_rad, 1.47), xytext=(0, 0), arrowprops=dict(facecolor='#00ffcc', edgecolor='#00ffcc', lw=2.0, width=1.8, headwidth=8), zorder=18)
        ax.plot([0, sit_rad], [0, 1.45], color='#FFD700', linestyle=':', lw=1.8, alpha=0.9, zorder=17)
                    
    ax.fill([0, 0.15, np.pi, -0.15], [0.55, 0.06, 0, 0.06], color='#FF3333', alpha=0.5, zorder=20)
    ax.fill([np.pi, np.pi - 0.15, 0, np.pi + 0.15], [0.55, 0.06, 0, 0.06], color='#E0E0E0', alpha=0.4, zorder=20)
    ax.scatter([0], [0], color='#FFD700', s=25, zorder=21, edgecolors='black', linewidth=0.5)
    
    ax.text(0, 0, f"🧭 THIÊN TRÌ\nVận {van_num} | {gender_str} ({eff_year})", color='#ff7b72', fontsize=7.2, fontweight='bold', ha='center', va='center', zorder=22, bbox=dict(boxstyle='round,pad=0.25', facecolor='#0d1117', edgecolor='#ff7b72', lw=1.4))
            
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='#30363d', linestyle='--', linewidth=0.8)
    ax.spines['polar'].set_color('#8b949e')
    plt.tight_layout()
    return fig
