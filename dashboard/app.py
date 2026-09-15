import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# ============================================================
# CẤU HÌNH TRANG STREAMLIT
# ============================================================
st.set_page_config(
    page_title="EPL Analytics Hub | Premier League Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS giao diện Premier League hiện đại & Card bóng đá
st.markdown("""
<style>
    /* Gradient Header - Phong cách bóng đá Châu Âu đẳng cấp */
    .main-header {
        background: linear-gradient(135deg, #17001a 0%, #38003c 70%, #4a004f 100%);
        border-left: 6px solid #00ff87;
        padding: 24px 28px;
        border-radius: 14px;
        color: #ffffff !important;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }
    .main-header h1 {
        color: #ffffff !important;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #00ff87 !important;
        margin-top: 6px;
        font-size: 1.08rem;
        font-weight: 600;
    }
    
    /* Card số liệu KPI - Nền tím đậm sang trọng, tương phản cao trên mọi màn hình */
    .metric-card {
        background: linear-gradient(135deg, #240026 0%, #38003c 100%);
        border: 1px solid rgba(0, 255, 135, 0.4);
        border-radius: 12px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2);
        transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #00ff87;
        box-shadow: 0 8px 20px rgba(0, 255, 135, 0.3);
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #00ff87 !important;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #f1f5f9 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 6px;
        font-weight: 700;
    }
    
    /* Profile card cầu thủ - Đảm bảo chữ trắng & neon green luôn sáng rõ */
    .player-card {
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }
    .player-card-1 {
        background: linear-gradient(135deg, #1e092b 0%, #2f0d42 100%);
        border: 2px solid #8b5cf6;
    }
    .player-card-2 {
        background: linear-gradient(135deg, #0a2318 0%, #133928 100%);
        border: 2px solid #00ff87;
    }
    .player-card h2 {
        color: #ffffff !important;
        margin-bottom: 6px;
        font-weight: 800;
        font-size: 1.6rem;
    }
    .player-card p {
        color: #e2e8f0 !important;
        font-size: 0.95rem;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .player-card p b {
        color: #ffffff !important;
        font-weight: 700;
    }
    .player-card h3 {
        color: #00ff87 !important;
        margin-top: 8px;
        font-weight: 700;
        font-size: 1.15rem;
    }
    
    /* Tab navigation styling - Khắc phục hoàn toàn lỗi chữ bị chìm */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #334155;
        padding-bottom: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #1e293b !important;
        border-radius: 8px 8px 0px 0px;
        padding: 8px 20px;
        font-weight: 700;
        border: 1px solid #334155;
        border-bottom: none;
        margin-right: 4px;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] span {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #334155 !important;
    }
    .stTabs [data-baseweb="tab"]:hover p,
    .stTabs [data-baseweb="tab"]:hover div,
    .stTabs [data-baseweb="tab"]:hover span {
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #38003c !important;
        border: 1.5px solid #00ff87 !important;
        border-bottom: none !important;
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] div,
    .stTabs [aria-selected="true"] span {
        color: #00ff87 !important;
        font-weight: 800 !important;
    }
    
    /* Bảng dữ liệu st.table - Tiêu đề & nội dung nổi bật */
    [data-testid="stTable"] table {
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden;
    }
    [data-testid="stTable"] th {
        background-color: #240026 !important;
        color: #00ff87 !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        padding: 10px 14px !important;
    }
    [data-testid="stTable"] td {
        font-weight: 600 !important;
        padding: 9px 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DỮ LIỆU CÓ CACHING & DỰ PHÒNG ĐA NỀN TẢNG
# ============================================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    candidates = [
        (os.path.join(base_dir, 'data', 'processed', 'matches_clean.csv'),
         os.path.join(base_dir, 'data', 'processed', 'players_clean.csv')),
        (os.path.join('data', 'processed', 'matches_clean.csv'),
         os.path.join('data', 'processed', 'players_clean.csv')),
        (os.path.join('..', 'data', 'processed', 'matches_clean.csv'),
         os.path.join('..', 'data', 'processed', 'players_clean.csv')),
    ]
    
    matches_path = None
    players_path = None
    for m_path, p_path in candidates:
        if os.path.exists(m_path) and os.path.exists(p_path):
            matches_path = m_path
            players_path = p_path
            break
            
    if not matches_path or not players_path:
        st.error("""
        ### ❌ Không tìm thấy tệp dữ liệu đã xử lý!
        Ứng dụng cần 2 tệp dữ liệu sau trong `data/processed/`:
        - `matches_clean.csv`
        - `players_clean.csv`
        """)
        st.stop()
    
    matches_df = pd.read_csv(matches_path, low_memory=False)
    players_df = pd.read_csv(players_path, low_memory=False)
    
    # Feature bổ sung cho Match
    matches_df['Date'] = pd.to_datetime(matches_df['Date'])
    matches_df['TotalGoals'] = matches_df['FTHG'] + matches_df['FTAG']
    matches_df['TotalShots'] = matches_df['HS'] + matches_df['AS']
    matches_df['TotalShotsOnTarget'] = matches_df['HST'] + matches_df['AST']
    matches_df['TotalCorners'] = matches_df['HC'] + matches_df['AC']
    matches_df['TotalFouls'] = matches_df['HF'] + matches_df['AF']
    matches_df['TotalYellowCards'] = matches_df['HY'] + matches_df['AY']
    matches_df['TotalRedCards'] = matches_df['HR'] + matches_df['AR']
    
    return matches_df, players_df

matches_df, players_df = load_data()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg", width=140)
    st.title("EPL Analytics Hub")
    st.markdown("---")
    
    selected_page = st.radio(
        "Chọn Chức Năng Phân Tích:",
        [
            "📊 Trang 1: Tổng Quan & Lịch Sử EPL",
            "🏆 Trang 2: Hiệu Suất CLB & Chiến Thuật",
            "👟 Trang 3: Phân Tích Cầu Thủ & xG",
            "⚔️ Trang 4: So Sánh Đối Đầu Cầu Thủ",
            "🔮 Trang 5: AI Match Predictor"
        ]
    )
    
    st.markdown("---")
    st.markdown(f"""
    **Quy mô dữ liệu (100% Thuần EPL):**
    - 🏟️ **Trận đấu:** {len(matches_df):,} trận ({matches_df['Season'].nunique()} mùa giải: 1993 - 2025)
    - 👟 **Cầu thủ:** {len(players_df):,} bản ghi ({players_df['Player'].nunique():,} cầu thủ)
    - 🌍 **Quốc gia:** {players_df['Country'].nunique()} quốc tịch đại diện
    - 📈 **Tổng dữ liệu:** {len(matches_df) + len(players_df):,} bản ghi
    """)

# ============================================================
# TRANG 1: TỔNG QUAN & LỊCH SỬ EPL (32 MÙA GIẢI 1993 - 2025)
# ============================================================
if selected_page == "📊 Trang 1: Tổng Quan & Lịch Sử EPL":
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 Tổng Quan & Xu Hướng Lịch Sử Ngoại Hạng Anh</h1>
        <p>Khai phá toàn bộ 32 mùa giải Premier League hiện đại (1993/94 – 2024/25) với {len(matches_df):,} trận đấu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bộ lọc mùa giải
    all_seasons = sorted(matches_df['Season'].unique())
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        selected_seasons = st.multiselect(
            "Chọn các mùa giải muốn phân tích:",
            options=all_seasons,
            default=all_seasons[-10:] # mặc định chọn 10 mùa gần nhất để trực quan
        )
    with col_f2:
        st.write("")
        st.write("")
        if st.button("Chọn Toàn Bộ 32 Mùa"):
            selected_seasons = all_seasons
            
    if not selected_seasons:
        selected_seasons = all_seasons
        
    filtered_matches = matches_df[matches_df['Season'].isin(selected_seasons)].copy()
    
    # KPI Metrics
    total_m = len(filtered_matches)
    total_g = int(filtered_matches['TotalGoals'].sum())
    avg_g = filtered_matches['TotalGoals'].mean() if total_m > 0 else 0
    home_win_pct = (filtered_matches['FTR'] == 'H').mean() * 100 if total_m > 0 else 0
    avg_shots = filtered_matches[filtered_matches['TotalShots'] > 0]['TotalShots'].mean() if len(filtered_matches[filtered_matches['TotalShots'] > 0]) > 0 else 0
    
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_m:,}</div><div class="metric-label">Tổng Số Trận</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_g:,}</div><div class="metric-label">Tổng Bàn Thắng</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{avg_g:.2f}</div><div class="metric-label">Bàn Thắng TB / Trận</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{home_win_pct:.1f}%</div><div class="metric-label">Tỷ Lệ Chủ Nhà Thắng</div></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{avg_shots:.1f}</div><div class="metric-label">Cú Sút TB / Trận</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    # Tổ chức theo TABS
    tab1_overview, tab2_homeadv, tab3_choropleth = st.tabs([
        "📈 Xu Hướng Lịch Sử & Bàn Thắng",
        "🏟️ Lợi Thế Sân Nhà & Tác Động COVID-19",
        "🌍 Bản Đồ Dấu Ấn Toàn Cầu Của EPL (World Choropleth Map)"
    ])
    
    with tab1_overview:
        col_c1, col_c2 = st.columns([3, 2])
        with col_c1:
            # Xu hướng bàn thắng theo mùa
            season_goals = filtered_matches.groupby('Season').agg(
                TotalGoals=('TotalGoals', 'sum'),
                AvgGoals=('TotalGoals', 'mean'),
                Matches=('Date', 'count')
            ).reset_index()
            
            fig_goals = go.Figure()
            fig_goals.add_trace(go.Bar(
                x=season_goals['Season'],
                y=season_goals['TotalGoals'],
                name='Tổng bàn thắng',
                marker=dict(color='#8b5cf6', line=dict(color='#00ff87', width=1)),
                opacity=0.85
            ))
            fig_goals.add_trace(go.Scatter(
                x=season_goals['Season'],
                y=season_goals['AvgGoals'],
                name='Bàn thắng TB / trận',
                yaxis='y2',
                line=dict(color='#00ff87', width=3),
                mode='lines+markers'
            ))
            fig_goals.update_layout(
                title="<b>Xu Hướng Tổng Bàn Thắng & Bàn Thắng Trung Bình Qua Từng Mùa</b>",
                yaxis=dict(title="Tổng số bàn thắng"),
                yaxis2=dict(title="Bàn thắng TB / trận", overlaying='y', side='right'),
                height=420,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(fig_goals, width='stretch')
            
        with col_c2:
            # Donut chart kết quả
            res_counts = filtered_matches['FTR'].map({'H': 'Chủ Nhà Thắng', 'D': 'Hòa', 'A': 'Đội Khách Thắng'}).value_counts().reset_index()
            res_counts.columns = ['Kết Quả', 'Số Trận']
            fig_pie = px.pie(
                res_counts, values='Số Trận', names='Kết Quả',
                title="<b>Tỷ Lệ Phân Bố Kết Quả Trận Đấu</b>",
                hole=0.45,
                color='Kết Quả',
                color_discrete_map={'Chủ Nhà Thắng': '#2ecc71', 'Hòa': '#f39c12', 'Đội Khách Thắng': '#e74c3c'}
            )
            fig_pie.update_layout(height=420, margin=dict(l=20, r=20, t=60, b=20))
            st.plotly_chart(fig_pie, width='stretch')
            
    with tab2_homeadv:
        # Lợi thế sân nhà theo mùa
        home_adv = filtered_matches.groupby('Season').agg(
            HomeWinRate=('FTR', lambda x: (x == 'H').mean() * 100),
            AwayWinRate=('FTR', lambda x: (x == 'A').mean() * 100),
            DrawRate=('FTR', lambda x: (x == 'D').mean() * 100)
        ).reset_index()
        
        fig_adv = go.Figure()
        fig_adv.add_trace(go.Scatter(x=home_adv['Season'], y=home_adv['HomeWinRate'], name='Chủ nhà thắng (%)', line=dict(color='#2ecc71', width=3), mode='lines+markers'))
        fig_adv.add_trace(go.Scatter(x=home_adv['Season'], y=home_adv['AwayWinRate'], name='Khách thắng (%)', line=dict(color='#e74c3c', width=2, dash='dot'), mode='lines+markers'))
        fig_adv.add_trace(go.Scatter(x=home_adv['Season'], y=home_adv['DrawRate'], name='Hòa (%)', line=dict(color='#f39c12', width=2, dash='dash'), mode='lines+markers'))
        
        if '2020-2021' in home_adv['Season'].values:
            fig_adv.add_vrect(
                x0='2020-2021', x1='2020-2021', fillcolor="red", opacity=0.15,
                annotation_text="COVID-19 (Không khán giả: 37.9%)", annotation_position="top left"
            )
        fig_adv.update_layout(
            title="<b>Biến Thiên Lợi Thế Sân Nhà Qua Các Mùa Giải (Home Advantage)</b>",
            yaxis=dict(title="Tỷ lệ phần trăm (%)", range=[15, 65]),
            height=420,
            hovermode='x unified'
        )
        st.plotly_chart(fig_adv, width='stretch')
        st.info("💡 **Phát hiện thú vị:** Suốt 32 năm lịch sử EPL, tỷ lệ đội nhà giành chiến thắng luôn ổn định quanh mức **46 - 48%**. Riêng duy nhất mùa dịch COVID-19 (2020-21) khi các sân vận động đóng cửa không đón khán giả, tỷ lệ thắng sân nhà sụt giảm chạm đáy chỉ còn **37.9%**, chứng minh vai trò to lớn của sức ép cổ động viên đối với kết quả trận đấu!")

    with tab3_choropleth:
        st.markdown("### 🌍 Dấu Ấn Toàn Cầu Của Giải Ngoại Hạng Anh (World Footprint)")
        st.write("Giải Ngoại hạng Anh là giải đấu quốc tế nhất hành tinh. Bản đồ nhiệt dưới đây trực quan hóa sự hiện diện và đóng góp của các quốc gia trên khắp năm châu vào giải đấu:")
        
        # Nhóm quốc tịch
        nation_stats = players_df.groupby(['ISO_A3', 'Country']).agg(
            TotalPlayers=('Player', 'nunique'),
            TotalGoals=('Goals', 'sum'),
            TotalAssists=('Assists', 'sum'),
            TotalxG=('xG', 'sum')
        ).reset_index()
        
        col_m1, col_m2 = st.columns([1, 3])
        with col_m1:
            choro_metric = st.selectbox(
                "Chỉ số hiển thị trên bản đồ:",
                options=['TotalGoals', 'TotalPlayers', 'TotalAssists', 'TotalxG'],
                format_func=lambda x: {
                    'TotalGoals': '⚽ Tổng Số Bàn Thắng',
                    'TotalPlayers': '👥 Số Lượng Cầu Thủ',
                    'TotalAssists': '👟 Tổng Số Kiến Tạo',
                    'TotalxG': '🎯 Tổng Bàn Thắng Kỳ Vọng (xG)'
                }[x]
            )
            
            top_nations = nation_stats.sort_values(choro_metric, ascending=False).head(10)
            st.markdown(f"**Top 10 Quốc Gia Dẫn Đầu:**")
            for idx, r in top_nations.reset_index().iterrows():
                st.write(f"**{idx+1}. {r['Country']}**: {r[choro_metric]:,.1f}" if 'xG' in choro_metric else f"**{idx+1}. {r['Country']}**: {int(r[choro_metric]):,}")
                
        with col_m2:
            fig_map = px.choropleth(
                nation_stats,
                locations='ISO_A3',
                color=choro_metric,
                hover_name='Country',
                hover_data={'ISO_A3': False, 'TotalPlayers': True, 'TotalGoals': True, 'TotalAssists': True},
                color_continuous_scale='Viridis',
                title=f"<b>Bản Đồ Phân Bố {choro_metric} Của Các Quốc Gia Tại Premier League</b>"
            )
            fig_map.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                height=480,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_map, width='stretch')

# ============================================================
# TRANG 2: HIỆU SUẤT CLB & CHIẾN THUẬT (1993 - 2025)
# ============================================================
elif selected_page == "🏆 Trang 2: Hiệu Suất CLB & Chiến Thuật":
    st.markdown(f"""
    <div class="main-header">
        <h1>🏆 Hiệu Suất Câu Lạc Bộ & Phân Tích Chiến Thuật</h1>
        <p>Bảng tổng sắp 32 năm lịch sử, ma trận tương quan chiến thuật (Tactical Heatmap) và nhóm Big Six</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1_standings, tab2_heatmap, tab3_big6 = st.tabs([
        "🥇 Bảng Xếp Hạng & Bàn Thắng CLB",
        "🗺️ Ma Trận Tương Quan (Tactical Heatmap) & Điểm Số CLB",
        "⚔️ So Sánh Nhóm Big Six"
    ])
    
    # Tính bảng xếp hạng hàm tổng quát
    def compute_table(df_subset):
        records = []
        teams = set(df_subset['HomeTeam'].unique()).union(set(df_subset['AwayTeam'].unique()))
        for t in teams:
            h = df_subset[df_subset['HomeTeam'] == t]
            a = df_subset[df_subset['AwayTeam'] == t]
            
            p = len(h) + len(a)
            w = (h['FTR'] == 'H').sum() + (a['FTR'] == 'A').sum()
            d = (h['FTR'] == 'D').sum() + (a['FTR'] == 'D').sum()
            l = (h['FTR'] == 'A').sum() + (a['FTR'] == 'H').sum()
            gf = h['FTHG'].sum() + a['FTAG'].sum()
            ga = h['FTAG'].sum() + a['FTHG'].sum()
            pts = w * 3 + d
            shots = h['HS'].sum() + a['AS'].sum()
            sot = h['HST'].sum() + a['AST'].sum()
            
            conv_rate = (gf / shots * 100) if shots > 0 else 0
            shot_acc = (sot / shots * 100) if shots > 0 else 0
            
            records.append({
                'Team': t, 'P': p, 'W': w, 'D': d, 'L': l,
                'GF': int(gf), 'GA': int(ga), 'GD': int(gf - ga),
                'Pts': int(pts), 'Shots': int(shots), 'SoT': int(sot),
                'ConversionRate': conv_rate, 'ShotAccuracy': shot_acc
            })
        table_df = pd.DataFrame(records).sort_values(by=['Pts', 'GD', 'GF'], ascending=False).reset_index(drop=True)
        table_df.index = table_df.index + 1
        return table_df
        
    with tab1_standings:
        col_opt1, col_opt2 = st.columns([2, 2])
        with col_opt1:
            view_mode = st.radio("Chế độ xem:", ["Bảng Tổng Sắp Toàn Lịch Sử (32 Mùa)", "Xem Chi Tiết Từng Mùa Giải"], horizontal=True)
        with col_opt2:
            all_s_list = sorted(matches_df['Season'].unique().tolist(), reverse=True)
            chosen_s = st.selectbox("Chọn mùa giải:", all_s_list, disabled=(view_mode != "Xem Chi Tiết Từng Mùa Giải"))
            
        target_df = matches_df if view_mode.startswith("Bảng Tổng Sắp") else matches_df[matches_df['Season'] == chosen_s]
        table_result = compute_table(target_df)
        
        col_t1, col_t2 = st.columns([3, 2])
        with col_t1:
            st.markdown(f"### 📋 Bảng Xếp Hạng ({'Toàn Bộ 32 Mùa Giải' if view_mode.startswith('Bảng Tổng Sắp') else f'Mùa {chosen_s}'})")
            st.dataframe(
                table_result[['Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'ConversionRate']].style.format({
                    'ConversionRate': '{:.1f}%'
                }).background_gradient(subset=['Pts', 'GD'], cmap='Purples'),
                height=480,
                width='stretch'
            )
        with col_t2:
            st.markdown("### ⚽ Top CLB Ghi Nhiều Bàn Thắng Nhất")
            top10_gf = table_result.head(10)
            fig_clubs = px.bar(
                top10_gf, x='GF', y='Team', orientation='h',
                color='ConversionRate',
                color_continuous_scale=[[0, '#34d399'], [1, '#065f46']],
                labels={'GF': 'Số bàn thắng', 'ConversionRate': 'Tỷ lệ chuyển hóa (%)'}
            )
            fig_clubs.update_traces(texttemplate='<b>%{x:,} bàn</b> (%{marker.color:.1f}%)', textposition='outside')
            max_gf = top10_gf['GF'].max() * 1.25 if len(top10_gf) > 0 else 100
            fig_clubs.update_layout(yaxis={'categoryorder': 'total ascending'}, height=480, xaxis=dict(range=[0, max_gf]))
            st.plotly_chart(fig_clubs, width='stretch')
            
    with tab2_heatmap:
        col_hm1, col_hm2 = st.columns(2)
        with col_hm1:
            st.markdown("### 🗺️ Ma Trận Tương Quan Chiến Thuật (Tactical Correlation Heatmap)")
            # Tính correlation giữa các chỉ số trận đấu
            corr_cols = ['FTHG', 'FTAG', 'HS', 'AS', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY']
            valid_corr_matches = matches_df[(matches_df['HS'] > 0) & (matches_df['HST'] > 0)][corr_cols]
            corr_matrix = valid_corr_matches.corr().round(2)
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title="<b>Ma Trận Hệ Số Tương Quan Pearson Giữa Các Chỉ Số Trận Đấu</b>"
            )
            fig_corr.update_layout(height=480)
            st.plotly_chart(fig_corr, width='stretch')
            
        with col_hm2:
            st.markdown("### 📅 Heatmap Điểm Số CLB Qua Các Mùa Giải (Season Performance)")
            # Lấy top 12 CLB đá nhiều nhất
            top_teams = matches_df['HomeTeam'].value_counts().head(12).index.tolist()
            recent_seasons = sorted(matches_df['Season'].unique())[-15:] # 15 mùa gần nhất
            
            matrix_data = []
            for tm in top_teams:
                row = []
                for s in recent_seasons:
                    s_m = matches_df[(matches_df['Season'] == s) & ((matches_df['HomeTeam'] == tm) | (matches_df['AwayTeam'] == tm))]
                    if len(s_m) > 0:
                        tbl = compute_table(s_m)
                        tm_row = tbl[tbl['Team'] == tm]
                        pts = tm_row['Pts'].values[0] if len(tm_row) > 0 else 0
                    else:
                        pts = 0
                    row.append(pts)
                matrix_data.append(row)
                
            fig_team_hm = px.imshow(
                matrix_data,
                labels=dict(x="Mùa Giải", y="CLB", color="Điểm Số"),
                x=recent_seasons,
                y=top_teams,
                color_continuous_scale='Magma',
                text_auto=True,
                title="<b>Điểm Số Đạt Được Của Top CLB Qua 15 Mùa Giải Gần Đây</b>"
            )
            fig_team_hm.update_layout(height=480)
            st.plotly_chart(fig_team_hm, width='stretch')

    with tab3_big6:
        st.markdown("### ⚔️ So Sánh Trực Tiếp Nhóm \"Big Six\" (Arsenal, Chelsea, Liverpool, Man City, Man United, Tottenham)")
        big_six = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester City', 'Manchester United', 'Tottenham']
        all_table = compute_table(matches_df)
        b6_df = all_table[all_table['Team'].isin(big_six)].sort_values('Pts', ascending=False)
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            fig_b6_pts = px.bar(
                b6_df, x='Team', y='Pts',
                title="<b>Tổng Điểm Số Đạt Được Trong Kỷ Nguyên Ngoại Hạng Anh</b>",
                color='Team',
                color_discrete_sequence=px.colors.qualitative.Set1,
                text='Pts'
            )
            fig_b6_pts.update_traces(texttemplate='<b>%{y:,} đ</b>', textposition='outside')
            max_pts = b6_df['Pts'].max() * 1.15 if len(b6_df) > 0 else 100
            fig_b6_pts.update_layout(yaxis=dict(range=[0, max_pts]), height=420)
            st.plotly_chart(fig_b6_pts, width='stretch')
        with col_b2:
            fig_b6_eff = px.scatter(
                b6_df, x='ShotAccuracy', y='ConversionRate',
                size='GF', color='Team', text='Team',
                title="<b>Tỷ Lệ Sút Trúng Đích vs Chuyển Hóa Cơ Hội (Kích thước = Tổng bàn thắng)</b>",
                labels={'ShotAccuracy': 'Sút trúng đích (%)', 'ConversionRate': 'Chuyển hóa bàn thắng (%)'}
            )
            fig_b6_eff.update_traces(textposition='top center')
            st.plotly_chart(fig_b6_eff, width='stretch')

# ============================================================
# TRANG 3: PHÂN TÍCH CẦU THỦ & xG (VIOLIN PLOT, SCATTER, TREEMAP)
# ============================================================
elif selected_page == "👟 Trang 3: Phân Tích Cầu Thủ & xG":
    st.markdown("""
    <div class="main-header">
        <h1>👟 Phân Tích Cầu Thủ & Chỉ Số Kỳ Vọng ($xG, xA$)</h1>
        <p>Phân tích hiệu suất dứt điểm, kiến tạo, phân phối mật độ Violin plot và cây phân cấp bàn thắng</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bộ lọc cầu thủ
    col_pf1, col_pf2, col_pf3, col_pf4 = st.columns(4)
    with col_pf1:
        rec_type = st.selectbox("Cấp độ dữ liệu:", ["Tổng hợp mùa giải (Season Summary)", "Nhật ký trận đấu (Match Performance)", "Tất cả bản ghi"])
    with col_pf2:
        p_seasons = ["Tất cả các mùa"] + sorted(players_df['Season'].unique().tolist(), reverse=True)
        chosen_p_season = st.selectbox("Chọn mùa giải:", p_seasons)
    with col_pf3:
        p_clubs = ["Tất cả CLB"] + sorted(players_df['Club'].dropna().unique().tolist())
        chosen_p_club = st.selectbox("Chọn Câu Lạc Bộ:", p_clubs)
    with col_pf4:
        chosen_p_pos = st.selectbox("Vị trí thi đấu:", ["Tất cả", "Forward", "Midfielder", "Defender", "Goalkeeper"])
        
    # Áp dụng bộ lọc
    p_df = players_df.copy()
    if rec_type == "Tổng hợp mùa giải (Season Summary)":
        p_df = p_df[p_df['RecordType'] == 'Season Summary']
    elif rec_type == "Nhật ký trận đấu (Match Performance)":
        p_df = p_df[p_df['RecordType'] == 'Match Performance']
        
    if chosen_p_season != "Tất cả các mùa":
        p_df = p_df[p_df['Season'] == chosen_p_season]
    if chosen_p_club != "Tất cả CLB":
        p_df = p_df[p_df['Club'] == chosen_p_club]
    if chosen_p_pos != "Tất cả":
        p_df = p_df[p_df['PositionGroup'] == chosen_p_pos]
        
    # Gom nhóm theo cầu thủ nếu xem tổng hợp
    if chosen_p_season == "Tất cả các mùa" and rec_type != "Nhật ký trận đấu (Match Performance)":
        p_display = p_df.groupby('Player').agg({
            'Club': 'last', 'PositionGroup': 'last', 'Country': 'last',
            'Appearances': 'sum', 'Minutes': 'sum',
            'Goals': 'sum', 'Assists': 'sum', 'Shots': 'sum', 'KeyPasses': 'sum',
            'YellowCards': 'sum', 'RedCards': 'sum',
            'xG': 'sum', 'xA': 'sum', 'npxG': 'sum'
        }).reset_index()
    else:
        p_display = p_df.copy()
        
    p_display['xG_Diff'] = p_display['Goals'] - p_display['xG']
    p_display = p_display[p_display['Minutes'] >= 90].copy() # Lọc cầu thủ đá ít nhất 90 phút
    
    # TABS
    tab1_scatter, tab2_violin, tab3_treemap, tab4_table = st.tabs([
        "🎯 Bàn Thắng Thực Tế vs Bàn Thắng Kỳ Vọng (xG)",
        "🎻 Phân Phối Mật Độ (Violin Plot)",
        "🌳 Cây Phân Cấp Bàn Thắng (Treemap)",
        "📊 Bảng Xếp Hạng Chi Tiết Cầu Thủ"
    ])
    
    with tab1_scatter:
        st.markdown("### 🎯 Bàn Thắng Thực Tế vs Bàn Thắng Kỳ Vọng ($xG$)")
        st.write("Đường chéo nét đứt $y=x$ là mốc chuẩn kỳ vọng: Các điểm **nằm phía trên đường chéo** là những sát thủ **vượt kỳ vọng (Overperformers)**; các điểm nằm phía dưới thể hiện sự phung phí cơ hội.")
        
        max_axis = max(p_display['Goals'].max() if len(p_display)>0 else 10, p_display['xG'].max() if len(p_display)>0 else 10) + 2
        
        fig_scatter = px.scatter(
            p_display, x='xG', y='Goals',
            color='PositionGroup',
            hover_name='Player',
            hover_data=['Club', 'Minutes', 'Shots', 'xG_Diff'],
            labels={'xG': 'Bàn Thắng Kỳ Vọng (xG)', 'Goals': 'Bàn Thắng Thực Tế'},
            title="<b>Biểu Đồ Phân Tán: Bàn Thắng Thực Tế vs xG</b>",
            color_discrete_map={'Forward': '#e74c3c', 'Midfielder': '#3498db', 'Defender': '#2ecc71', 'Goalkeeper': '#f1c40f'}
        )
        fig_scatter.add_shape(
            type="line", line=dict(dash='dash', color='gray', width=2),
            x0=0, x1=max_axis, y0=0, y1=max_axis
        )
        fig_scatter.update_layout(height=520)
        st.plotly_chart(fig_scatter, width='stretch')
        
    with tab2_violin:
        st.markdown("### 🎻 Phân Phối Mật Độ Xác Suất (Violin Plot)")
        st.write("Biểu đồ Violin kết hợp giữa đường cong mật độ (KDE) và khung Boxplot bên trong để chỉ ra sự phân hóa giữa các vị trí:")
        
        v_col1, v_col2 = st.columns([1, 3])
        with v_col1:
            v_metric = st.selectbox(
                "Chọn chỉ số phân tích mật độ:",
                ['xG', 'Goals', 'xA', 'Assists', 'Shots', 'Minutes'],
                format_func=lambda x: {
                    'xG': '🎯 Bàn Thắng Kỳ Vọng (xG)',
                    'Goals': '⚽ Bàn Thắng Thực Tế',
                    'xA': '👟 Kiến Tạo Kỳ Vọng (xA)',
                    'Assists': '🎯 Kiến Tạo Thực Tế',
                    'Shots': '🚀 Số Cú Sút',
                    'Minutes': '⏱️ Số Phút Thi Đấu'
                }[x]
            )
        with v_col2:
            fig_violin = px.violin(
                p_display,
                y=v_metric,
                x='PositionGroup',
                color='PositionGroup',
                box=True, # Hiển thị boxplot bên trong
                points="all", # Hiển thị các chấm dữ liệu
                hover_data=['Player', 'Club'],
                title=f"<b>Phân Phối Mật Độ Chỉ Số {v_metric} Theo Nhóm Vị Trí</b>",
                color_discrete_map={'Forward': '#e74c3c', 'Midfielder': '#3498db', 'Defender': '#2ecc71', 'Goalkeeper': '#f1c40f'}
            )
            fig_violin.update_layout(height=480)
            st.plotly_chart(fig_violin, width='stretch')
            
    with tab3_treemap:
        st.markdown("### 🌳 Cây Phân Cấp Đóng Góp Bàn Thắng (Treemap)")
        st.write("Nhấp vào từng ô Câu Lạc Bộ để phóng to và xem chi tiết đóng góp của từng chân sút trong đội hình:")
        
        top_scorers_tree = p_display[p_display['Goals'] > 0].copy()
        if len(top_scorers_tree) > 0:
            fig_tree = px.treemap(
                top_scorers_tree,
                path=['Club', 'Player'],
                values='Goals',
                color='xG_Diff',
                color_continuous_scale='RdYlGn',
                title="<b>Cơ Cấu Bàn Thắng: Câu Lạc Bộ -> Cầu Thủ (Màu sắc thể hiện độ vượt kỳ vọng xG)</b>"
            )
            fig_tree.update_layout(height=520)
            st.plotly_chart(fig_tree, width='stretch')
        else:
            st.info("Không có dữ liệu bàn thắng phù hợp với bộ lọc hiện tại.")
            
    with tab4_table:
        st.markdown("### 📊 Bảng Xếp Hạng Chi Tiết Cầu Thủ")
        top_n = st.slider("Số lượng cầu thủ hiển thị:", 10, 100, 20)
        sort_by = st.selectbox("Sắp xếp theo:", ['Goals', 'xG', 'Assists', 'xA', 'xG_Diff', 'Shots', 'Minutes'])
        
        sorted_p = p_display.sort_values(sort_by, ascending=False).head(top_n)
        show_cols = ['Player', 'Club', 'PositionGroup', 'Country', 'Appearances', 'Minutes', 'Goals', 'xG', 'xG_Diff', 'Assists', 'xA', 'Shots']
        st.dataframe(
            sorted_p[[c for c in show_cols if c in sorted_p.columns]].style.format({
                'xG': '{:.2f}', 'xA': '{:.2f}', 'xG_Diff': '{:+.2f}'
            }).background_gradient(subset=['Goals', 'xG_Diff'], cmap='RdYlGn'),
            height=420,
            width='stretch'
        )

# ============================================================
# TRANG 4: SO SÁNH ĐỐI ĐẦU CẦU THỦ (RADAR SPIDER CHART)
# ============================================================
elif selected_page == "⚔️ Trang 4: So Sánh Đối Đầu Cầu Thủ":
    st.markdown("""
    <div class="main-header">
        <h1>⚔️ So Sánh Đối Đầu Trực Diện Cầu Thủ (Head-to-Head)</h1>
        <p>So sánh đa giác kỹ năng Radar Spider Chart 8 chiều và bảng thống kê chi tiết sự nghiệp</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chuẩn bị dữ liệu tổng hợp sự nghiệp EPL cho mỗi cầu thủ
    career = players_df[players_df['RecordType'] == 'Season Summary'].groupby('Player').agg({
        'Club': lambda x: ', '.join(x.unique()[:3]),
        'PositionGroup': 'last',
        'Country': 'last',
        'Appearances': 'sum',
        'Minutes': 'sum',
        'Goals': 'sum',
        'Assists': 'sum',
        'Shots': 'sum',
        'KeyPasses': 'sum',
        'YellowCards': 'sum',
        'RedCards': 'sum',
        'xG': 'sum',
        'xA': 'sum'
    }).reset_index()
    
    # Tính Per 90
    career['M90'] = career['Minutes'] / 90.0
    career = career[career['M90'] >= 5.0].copy() # Tối thiểu 5 trận 90 phút
    
    career['G90'] = career['Goals'] / career['M90']
    career['A90'] = career['Assists'] / career['M90']
    career['xG90'] = career['xG'] / career['M90']
    career['xA90'] = career['xA'] / career['M90']
    career['Shots90'] = career['Shots'] / career['M90']
    career['KP90'] = career['KeyPasses'] / career['M90']
    career['DisciplineScore'] = np.clip(100 - (career['YellowCards'] * 5 + career['RedCards'] * 15) / career['M90'] * 10, 0, 100)
    
    all_players_list = sorted(career['Player'].tolist())
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p1_default = all_players_list.index("Harry Kane") if "Harry Kane" in all_players_list else 0
        player1 = st.selectbox("Chọn Cầu Thủ 1:", all_players_list, index=p1_default)
    with col_p2:
        p2_default = all_players_list.index("Mohamed Salah") if "Mohamed Salah" in all_players_list else min(1, len(all_players_list)-1)
        player2 = st.selectbox("Chọn Cầu Thủ 2:", all_players_list, index=p2_default)
        
    p1_data = career[career['Player'] == player1].iloc[0]
    p2_data = career[career['Player'] == player2].iloc[0]
    
    # Profile Cards
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown(f"""
        <div class="player-card player-card-1">
            <h2>🔴 {player1}</h2>
            <p><b>CLB:</b> {p1_data['Club']} &nbsp;|&nbsp; <b>Vị trí:</b> {p1_data['PositionGroup']} &nbsp;|&nbsp; <b>Quốc tịch:</b> {p1_data['Country']}</p>
            <h3>⚽ {int(p1_data['Goals'])} Bàn &nbsp;|&nbsp; 👟 {int(p1_data['Assists'])} Kiến Tạo &nbsp;|&nbsp; ⏱️ {int(p1_data['Minutes']):,} Phút</h3>
        </div>
        """, unsafe_allow_html=True)
    with col_c2:
        st.markdown(f"""
        <div class="player-card player-card-2">
            <h2>🟢 {player2}</h2>
            <p><b>CLB:</b> {p2_data['Club']} &nbsp;|&nbsp; <b>Vị trí:</b> {p2_data['PositionGroup']} &nbsp;|&nbsp; <b>Quốc tịch:</b> {p2_data['Country']}</p>
            <h3>⚽ {int(p2_data['Goals'])} Bàn &nbsp;|&nbsp; 👟 {int(p2_data['Assists'])} Kiến Tạo &nbsp;|&nbsp; ⏱️ {int(p2_data['Minutes']):,} Phút</h3>
        </div>
        """, unsafe_allow_html=True)
        
    tab1_radar, tab2_bars = st.tabs([
        "🕸️ Biểu Đồ Radar Đa Giác Kỹ Năng (Spider Chart)",
        "📋 So Sánh Cột & Thống Kê Chi Tiết"
    ])
    
    with tab1_radar:
        st.markdown("### 🕸️ Biểu Đồ Radar Kỹ Năng Đa Chiều (Spider Chart)")
        st.write("So sánh trực quan đa trục năng lực giữa hai cầu thủ theo chuẩn phân tích bóng đá chuyên nghiệp:")
        
        # Chuẩn hóa giá trị từ 0 đến 100 để vẽ radar đẹp
        categories = ['Dứt Điểm (Goals/90)', 'Kỳ Vọng (xG/90)', 'Kiến Tạo (Assists/90)', 'Tầm Nhìn (xA/90)', 'Số Cú Sút/90', 'Tạo Cơ Hội/90', 'Kỷ Luật Thi Đấu']
        
        # Scale to percentile/benchmark
        def scale_metric(val, max_v):
            return min(100, (val / max_v) * 100) if max_v > 0 else 0
            
        p1_radar_vals = [
            scale_metric(p1_data['G90'], 1.0),
            scale_metric(p1_data['xG90'], 1.0),
            scale_metric(p1_data['A90'], 0.5),
            scale_metric(p1_data['xA90'], 0.5),
            scale_metric(p1_data['Shots90'], 5.0),
            scale_metric(p1_data['KP90'], 3.5),
            p1_data['DisciplineScore']
        ]
        
        p2_radar_vals = [
            scale_metric(p2_data['G90'], 1.0),
            scale_metric(p2_data['xG90'], 1.0),
            scale_metric(p2_data['A90'], 0.5),
            scale_metric(p2_data['xA90'], 0.5),
            scale_metric(p2_data['Shots90'], 5.0),
            scale_metric(p2_data['KP90'], 3.5),
            p2_data['DisciplineScore']
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=p1_radar_vals + [p1_radar_vals[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=player1,
            line=dict(color='#8b5cf6', width=2),
            opacity=0.6
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=p2_radar_vals + [p2_radar_vals[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=player2,
            line=dict(color='#00ff87', width=2),
            opacity=0.6
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            title="<b>So Sánh Đa Giác Kỹ Năng Radar Spider Chart (Chuẩn Hóa Thang Điểm 100)</b>",
            height=500
        )
        st.plotly_chart(fig_radar, width='stretch')
        
    with tab2_bars:
        col_tb1, col_tb2 = st.columns(2)
        with col_tb1:
            st.markdown("### 📊 Biểu Đồ So Sánh Các Chỉ Số Hiệu Suất / 90 Phút")
            metrics_compare = ['G90', 'xG90', 'A90', 'xA90', 'Shots90', 'KP90']
            labels_compare = ['Bàn thắng/90', 'xG/90', 'Kiến tạo/90', 'xA/90', 'Cú sút/90', 'KeyPasses/90']
            
            comp_df = pd.DataFrame({
                'Chỉ số': labels_compare,
                player1: [p1_data[m] for m in metrics_compare],
                player2: [p2_data[m] for m in metrics_compare]
            })
            
            fig_bar_comp = go.Figure()
            fig_bar_comp.add_trace(go.Bar(
                y=comp_df['Chỉ số'], x=comp_df[player1], name=player1, orientation='h',
                marker_color='#8b5cf6',
                text=[f"<b>{v:.2f}</b>" for v in comp_df[player1]],
                textposition='auto'
            ))
            fig_bar_comp.add_trace(go.Bar(
                y=comp_df['Chỉ số'], x=comp_df[player2], name=player2, orientation='h',
                marker_color='#00ff87',
                text=[f"<b>{v:.2f}</b>" for v in comp_df[player2]],
                textposition='auto'
            ))
            fig_bar_comp.update_layout(barmode='group', height=420)
            st.plotly_chart(fig_bar_comp, width='stretch')
            
        with col_tb2:
            st.markdown("### 📋 Bảng Thống Kê So Sánh Chi Tiết")
            stat_table = pd.DataFrame({
                'Hạng Mục': ['Số phút thi đấu', 'Bàn thắng', 'Bàn thắng kỳ vọng (xG)', 'Hiệu số xG Diff', 'Kiến tạo', 'Kiến tạo kỳ vọng (xA)', 'Tổng cú sút', 'Đường chuyền quyết định', 'Thẻ vàng', 'Thẻ đỏ'],
                player1: [
                    f"{int(p1_data['Minutes']):,}",
                    f"{int(p1_data['Goals'])}",
                    f"{p1_data['xG']:.2f}",
                    f"{p1_data['Goals'] - p1_data['xG']:+.2f}",
                    f"{int(p1_data['Assists'])}",
                    f"{p1_data['xA']:.2f}",
                    f"{int(p1_data['Shots'])}",
                    f"{int(p1_data['KeyPasses'])}",
                    f"{int(p1_data['YellowCards'])}",
                    f"{int(p1_data['RedCards'])}"
                ],
                player2: [
                    f"{int(p2_data['Minutes']):,}",
                    f"{int(p2_data['Goals'])}",
                    f"{p2_data['xG']:.2f}",
                    f"{p2_data['Goals'] - p2_data['xG']:+.2f}",
                    f"{int(p2_data['Assists'])}",
                    f"{p2_data['xA']:.2f}",
                    f"{int(p2_data['Shots'])}",
                    f"{int(p2_data['KeyPasses'])}",
                    f"{int(p2_data['YellowCards'])}",
                    f"{int(p2_data['RedCards'])}"
                ]
            })
            st.table(stat_table.set_index('Hạng Mục'))

# ============================================================
# TRANG 5: AI MATCH PREDICTOR
# ============================================================
elif selected_page == "🔮 Trang 5: AI Match Predictor":
    st.markdown("""
    <div class="main-header">
        <h1>🔮 AI Match Predictor (Mô Phỏng Dự Đoán Trận Đấu EPL)</h1>
        <p>Mô hình Machine Learning Random Forest dự đoán xác suất Thắng - Hòa - Thua dựa trên phong độ trượt (Rolling Form)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Huấn luyện mô hình Random Forest trên Match Data
    @st.cache_resource
    def train_predictor():
        m_df = matches_df.copy().sort_values('Date').reset_index(drop=True)
        # Tạo team stats cho 5 trận gần nhất
        team_stats = {}
        rows = []
        for idx, row in m_df.iterrows():
            ht = row['HomeTeam']
            at = row['AwayTeam']
            
            h_form = team_stats.get(ht, [])
            a_form = team_stats.get(at, [])
            
            if len(h_form) >= 5 and len(a_form) >= 5:
                h_p = np.mean([x['Pts'] for x in h_form[-5:]])
                h_gf = np.mean([x['GF'] for x in h_form[-5:]])
                h_ga = np.mean([x['GA'] for x in h_form[-5:]])
                
                a_p = np.mean([x['Pts'] for x in a_form[-5:]])
                a_gf = np.mean([x['GF'] for x in a_form[-5:]])
                a_ga = np.mean([x['GA'] for x in a_form[-5:]])
                
                res_target = 0 if row['FTR'] == 'H' else (1 if row['FTR'] == 'D' else 2)
                rows.append({
                    'H_Pts5': h_p, 'H_GF5': h_gf, 'H_GA5': h_ga,
                    'A_Pts5': a_p, 'A_GF5': a_gf, 'A_GA5': a_ga,
                    'Target': res_target
                })
                
            # Update stats
            h_pts = 3 if row['FTR'] == 'H' else (1 if row['FTR'] == 'D' else 0)
            a_pts = 3 if row['FTR'] == 'A' else (1 if row['FTR'] == 'D' else 0)
            
            if ht not in team_stats: team_stats[ht] = []
            if at not in team_stats: team_stats[at] = []
            
            team_stats[ht].append({'Pts': h_pts, 'GF': row['FTHG'], 'GA': row['FTAG']})
            team_stats[at].append({'Pts': a_pts, 'GF': row['FTAG'], 'GA': row['FTHG']})
            
        feat_df = pd.DataFrame(rows)
        X = feat_df[['H_Pts5', 'H_GF5', 'H_GA5', 'A_Pts5', 'A_GF5', 'A_GA5']]
        y = feat_df['Target']
        
        clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        clf.fit(X, y)
        
        # Lưu lại phong độ hiện tại của các đội
        latest_team_stats = {t: stats[-5:] for t, stats in team_stats.items() if len(stats) >= 5}
        return clf, latest_team_stats
        
    clf, latest_stats = train_predictor()
    
    avail_teams = sorted(list(latest_stats.keys()))
    
    col_pr1, col_pr2 = st.columns(2)
    with col_pr1:
        home_team = st.selectbox("🏟️ Chọn Đội Chủ Nhà:", avail_teams, index=avail_teams.index("Arsenal") if "Arsenal" in avail_teams else 0)
    with col_pr2:
        away_team = st.selectbox("✈️ Chọn Đội Khách:", avail_teams, index=avail_teams.index("Chelsea") if "Chelsea" in avail_teams else min(1, len(avail_teams)-1))
        
    if home_team == away_team:
        st.warning("⚠️ Vui lòng chọn hai đội bóng khác nhau để dự đoán trận đấu!")
    else:
        h_s = latest_stats[home_team]
        a_s = latest_stats[away_team]
        
        h_pts5 = np.mean([x['Pts'] for x in h_s])
        h_gf5 = np.mean([x['GF'] for x in h_s])
        h_ga5 = np.mean([x['GA'] for x in h_s])
        
        a_pts5 = np.mean([x['Pts'] for x in a_s])
        a_gf5 = np.mean([x['GF'] for x in a_s])
        a_ga5 = np.mean([x['GA'] for x in a_s])
        
        feat_cols = ['H_Pts5', 'H_GF5', 'H_GA5', 'A_Pts5', 'A_GF5', 'A_GA5']
        input_feats = pd.DataFrame([[h_pts5, h_gf5, h_ga5, a_pts5, a_gf5, a_ga5]], columns=feat_cols)
        probs = clf.predict_proba(input_feats)[0] * 100
        
        tab1_pred, tab2_feat = st.tabs([
            "🔮 Kết Quả Dự Đoán & Xác Suất Trận Đấu",
            "🧠 Giải Thích Mô Hình & Trọng Số Đặc Trưng"
        ])
        
        with tab1_pred:
            st.markdown(f"### ⚔️ Dự Đoán Kết Quả: **{home_team}** vs **{away_team}**")
            
            prob_df = pd.DataFrame({
                'Kịch Bản': [f'{home_team} Thắng', 'Hòa', f'{away_team} Thắng'],
                'Xác Suất (%)': [probs[0], probs[1], probs[2]]
            })
            
            fig_prob = px.bar(
                prob_df, x='Xác Suất (%)', y='Kịch Bản', orientation='h',
                color='Kịch Bản',
                color_discrete_map={
                    f'{home_team} Thắng': '#2ecc71',
                    'Hòa': '#f39c12',
                    f'{away_team} Thắng': '#e74c3c'
                },
                text_auto='.1f'
            )
            fig_prob.update_traces(
                textposition='inside',
                textfont=dict(color='white', size=14, family='sans-serif')
            )
            fig_prob.update_layout(xaxis=dict(range=[0, 100]), height=300)
            st.plotly_chart(fig_prob, width='stretch')
            
            # Form comparison
            st.markdown("### 📋 So Sánh Phong Độ 5 Trận Gần Nhất")
            fc_df = pd.DataFrame({
                'Chỉ số phong độ 5 trận': ['Điểm số TB / trận', 'Bàn thắng TB / trận', 'Bàn thua TB / trận'],
                home_team: [f"{h_pts5:.2f}", f"{h_gf5:.2f}", f"{h_ga5:.2f}"],
                away_team: [f"{a_pts5:.2f}", f"{a_gf5:.2f}", f"{a_ga5:.2f}"]
            })
            st.table(fc_df.set_index('Chỉ số phong độ 5 trận'))
            
        with tab2_feat:
            st.markdown("### 🧠 Tầm Quan Trọng Của Các Yếu Tố (Feature Importance)")
            st.write("Mức độ đóng góp của từng chỉ số phong độ vào quyết định phân loại của mô hình Random Forest:")
            
            feat_names = ['Chủ Nhà - Điểm 5 trận', 'Chủ Nhà - Bàn thắng 5 trận', 'Chủ Nhà - Bàn thua 5 trận',
                          'Đội Khách - Điểm 5 trận', 'Đội Khách - Bàn thắng 5 trận', 'Đội Khách - Bàn thua 5 trận']
            fi_df = pd.DataFrame({
                'Đặc Trưng': feat_names,
                'Tầm Quan Trọng (%)': (clf.feature_importances_ * 100).round(1)
            }).sort_values('Tầm Quan Trọng (%)', ascending=True)
            
            fig_fi = px.bar(
                fi_df, x='Tầm Quan Trọng (%)', y='Đặc Trưng', orientation='h',
                color='Tầm Quan Trọng (%)',
                color_continuous_scale=[[0, '#8b5cf6'], [1, '#38003c']]
            )
            fig_fi.update_traces(texttemplate='<b>%{x:.1f}%</b>', textposition='outside')
            max_fi = max(fi_df['Tầm Quan Trọng (%)']) * 1.25 if len(fi_df) > 0 else 100
            fig_fi.update_layout(height=350, showlegend=False, xaxis=dict(range=[0, max_fi]))
            st.plotly_chart(fig_fi, width='stretch')
