import os
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

# Custom CSS giao diện Premier League hiện đại
st.markdown("""
<style>
    /* Gradient Header */
    .main-header {
        background: linear-gradient(135deg, #38003c 0%, #00ff87 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #e0e0e0;
        margin-top: 6px;
        font-size: 1.05rem;
    }
    
    /* Card số liệu */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38003c;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DỮ LIỆU CÓ CACHING & DỰ PHÒNG ĐƯỜNG DẪN ĐA NỀN TẢNG
# ============================================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Các vị trí tiềm năng chứa file dữ liệu
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
        Ứng dụng cần 2 tệp dữ liệu sau để hoạt động:
        - `data/processed/matches_clean.csv`
        - `data/processed/players_clean.csv`
        
        **Cách khắc phục:**
        1. Đảm bảo thư mục `data/` trong repo đã được tải về đầy đủ.
        2. Nếu chưa có thư mục `data/processed/`, hãy mở và chạy file `EPL_Data_Analysis.ipynb` để tự động làm sạch và xuất dữ liệu.
        3. Khởi chạy lại dashboard từ thư mục gốc của repository:
           ```bash
           streamlit run dashboard/app.py
           ```
        """)
        st.stop()
    
    matches_df = pd.read_csv(matches_path)
    players_df = pd.read_csv(players_path)
    
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
            "📊 Tổng Quan & Lịch Sử EPL",
            "🏆 Hiệu Suất Câu Lạc Bộ",
            "👟 Phân Tích Cầu Thủ & xG",
            "⚔️ So Sánh Đối Đầu Cầu Thủ",
            "🔮 Dự Đoán Kết Quả Trận Đấu"
        ]
    )
    
    st.markdown("---")
    st.markdown("""
    **Thông tin đề tài:**
    - **Match Data:** 20 mùa giải (7,601 trận)
    - **Player Data:** 11 mùa giải (5,887 cầu thủ)
    - **Nguồn:** Football-Data & Understat
    """)

# ============================================================
# TRANG 1: TỔNG QUAN & LỊCH SỬ EPL
# ============================================================
if selected_page == "📊 Tổng Quan & Lịch Sử EPL":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Tổng Quan & Xu Hướng Lịch Sử Ngoại Hạng Anh</h1>
        <p>Phân tích dữ liệu 20 mùa giải Ngoại hạng Anh (2005/06 - 2024/25) với hơn 7,600 trận đấu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bộ lọc mùa giải
    all_seasons = sorted(matches_df['Season'].unique())
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        selected_seasons = st.multiselect(
            "Lọc Mùa Giải:",
            options=all_seasons,
            default=all_seasons,
            help="Chọn một hoặc nhiều mùa giải để phân tích"
        )
    
    if not selected_seasons:
        st.warning("Vui lòng chọn ít nhất một mùa giải!")
        st.stop()
        
    filtered_matches = matches_df[matches_df['Season'].isin(selected_seasons)].copy()
    
    # Top KPI Metrics Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(filtered_matches):,}</div><div class="metric-label">Tổng Số Trận</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{filtered_matches['TotalGoals'].sum():,}</div><div class="metric-label">Tổng Bàn Thắng</div></div>""", unsafe_allow_html=True)
    with c3:
        avg_g = filtered_matches['TotalGoals'].mean()
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{avg_g:.2f}</div><div class="metric-label">Bàn Thắng TB / Trận</div></div>""", unsafe_allow_html=True)
    with c4:
        home_win_pct = (filtered_matches['FTR'] == 'H').mean() * 100
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{home_win_pct:.1f}%</div><div class="metric-label">Tỷ Lệ Chủ Nhà Thắng</div></div>""", unsafe_allow_html=True)
    with c5:
        avg_shots = filtered_matches['TotalShots'].mean()
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{avg_shots:.1f}</div><div class="metric-label">Cú Sút TB / Trận</div></div>""", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Biểu đồ xu hướng bàn thắng qua các mùa
    season_summary = filtered_matches.groupby('Season').agg(
        TotalGoals=('TotalGoals', 'sum'),
        AvgGoals=('TotalGoals', 'mean'),
        AvgShots=('TotalShots', 'mean'),
        AvgSoT=('TotalShotsOnTarget', 'mean')
    ).reset_index().sort_values('Season')
    
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        fig_goals = go.Figure()
        fig_goals.add_trace(go.Bar(
            x=season_summary['Season'], y=season_summary['TotalGoals'],
            name='Tổng bàn thắng', marker_color='#38003c', opacity=0.8
        ))
        fig_goals.add_trace(go.Scatter(
            x=season_summary['Season'], y=season_summary['AvgGoals'],
            name='Bàn thắng TB / trận', yaxis='y2', line=dict(color='#e74c3c', width=3), mode='lines+markers'
        ))
        fig_goals.update_layout(
            title='<b>Xu Hướng Bàn Thắng Qua Các Mùa Giải EPL</b>',
            yaxis=dict(title='Tổng số bàn thắng'),
            yaxis2=dict(title='Bàn thắng TB / trận', overlaying='y', side='right'),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.6)'),
            hovermode='x unified',
            height=400,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig_goals, use_container_width=True)
        
    with col_chart2:
        # Donut chart kết quả trận đấu
        res_counts = filtered_matches['FTR'].map({'H': 'Chủ Nhà Thắng', 'D': 'Hòa', 'A': 'Đội Khách Thắng'}).value_counts()
        fig_pie = px.pie(
            values=res_counts.values,
            names=res_counts.index,
            title='<b>Tỷ Lệ Kết Quả Trận Đấu (Home Win / Draw / Away Win)</b>',
            hole=0.45,
            color=res_counts.index,
            color_discrete_map={'Chủ Nhà Thắng': '#2ecc71', 'Hòa': '#f39c12', 'Đội Khách Thắng': '#e74c3c'}
        )
        fig_pie.update_layout(height=400, margin=dict(l=20, r=20, t=60, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    # Phân tích sâu về Lợi thế sân nhà & Tác động của COVID-19
    st.markdown("### 🏟️ Phân Tích Lợi Thế Sân Nhà & Tác Động Giai Đoạn COVID-19")
    home_adv_season = filtered_matches.groupby(['Season', 'FTR']).size().unstack(fill_value=0)
    home_adv_season['Total'] = home_adv_season.sum(axis=1)
    home_adv_season['HomeWinRate'] = (home_adv_season['H'] / home_adv_season['Total']) * 100
    home_adv_season['DrawRate'] = (home_adv_season['D'] / home_adv_season['Total']) * 100
    home_adv_season['AwayWinRate'] = (home_adv_season['A'] / home_adv_season['Total']) * 100
    
    fig_adv = px.line(
        home_adv_season.reset_index(),
        x='Season',
        y=['HomeWinRate', 'DrawRate', 'AwayWinRate'],
        labels={'value': 'Tỷ lệ (%)', 'variable': 'Kết quả', 'Season': 'Mùa giải'},
        title='<b>Biến Động Tỷ Lệ Thắng Sân Nhà vs Sân Khách (Lưu ý mùa dịch COVID 2020-21)</b>',
        color_discrete_map={'HomeWinRate': '#2ecc71', 'DrawRate': '#f39c12', 'AwayWinRate': '#e74c3c'}
    )
    fig_adv.add_vrect(
        x0='2020-2021', x1='2020-2021',
        fillcolor="yellow", opacity=0.3, line_width=0,
        annotation_text="COVID-19 (Không khán giả)", annotation_position="top left"
    )
    fig_adv.update_layout(height=380, hovermode='x unified')
    st.plotly_chart(fig_adv, use_container_width=True)

# ============================================================
# TRANG 2: HIỆU SUẤT CÂU LẠC BỘ & BẢNG XẾP HẠNG
# ============================================================
elif selected_page == "🏆 Hiệu Suất Câu Lạc Bộ":
    st.markdown("""
    <div class="main-header">
        <h1>🏆 Hiệu Suất Câu Lạc Bộ & Bảng Tổng Sắp</h1>
        <p>Bảng xếp hạng, số liệu thống kê bàn thắng, cú sút và tỷ lệ chuyển hóa cơ hội của các CLB</p>
    </div>
    """, unsafe_allow_html=True)
    
    mode = st.radio("Chế độ xem:", ["Toàn bộ 20 mùa giải lịch sử (2005 - 2025)", "Xem theo từng mùa giải cụ thể"], horizontal=True)
    
    if mode == "Xem theo từng mùa giải cụ thể":
        chosen_season = st.selectbox("Chọn mùa giải:", sorted(matches_df['Season'].unique(), reverse=True))
        data_to_use = matches_df[matches_df['Season'] == chosen_season].copy()
    else:
        data_to_use = matches_df.copy()
        
    # Tính bảng xếp hạng
    home_stats = data_to_use[['HomeTeam', 'FTHG', 'FTAG', 'FTR', 'HS', 'HST']].copy()
    home_stats.columns = ['Team', 'GF', 'GA', 'FTR', 'Shots', 'SoT']
    home_stats['W'] = (home_stats['FTR'] == 'H').astype(int)
    home_stats['D'] = (home_stats['FTR'] == 'D').astype(int)
    home_stats['L'] = (home_stats['FTR'] == 'A').astype(int)
    
    away_stats = data_to_use[['AwayTeam', 'FTAG', 'FTHG', 'FTR', 'AS', 'AST']].copy()
    away_stats.columns = ['Team', 'GF', 'GA', 'FTR', 'Shots', 'SoT']
    away_stats['W'] = (away_stats['FTR'] == 'A').astype(int)
    away_stats['D'] = (away_stats['FTR'] == 'D').astype(int)
    away_stats['L'] = (away_stats['FTR'] == 'H').astype(int)
    
    combined = pd.concat([home_stats, away_stats], ignore_index=True)
    
    standings = combined.groupby('Team').agg(
        MP=('GF', 'count'),
        W=('W', 'sum'),
        D=('D', 'sum'),
        L=('L', 'sum'),
        GF=('GF', 'sum'),
        GA=('GA', 'sum'),
        Shots=('Shots', 'sum'),
        SoT=('SoT', 'sum')
    ).reset_index()
    
    standings['GD'] = standings['GF'] - standings['GA']
    standings['Pts'] = standings['W'] * 3 + standings['D']
    standings['WinRate'] = (standings['W'] / standings['MP']) * 100
    standings['ShotAccuracy'] = np.where(standings['Shots'] > 0, (standings['SoT'] / standings['Shots']) * 100, 0)
    standings['ConversionRate'] = np.where(standings['Shots'] > 0, (standings['GF'] / standings['Shots']) * 100, 0)
    
    standings = standings.sort_values(['Pts', 'GD', 'GF'], ascending=False).reset_index(drop=True)
    standings.index += 1
    
    col_tbl, col_bars = st.columns([3, 2])
    
    with col_tbl:
        st.markdown("### 📋 Bảng Xếp Hạng & Chỉ Số Kỹ Thuật")
        st.dataframe(
            standings[['Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'WinRate', 'ConversionRate']].style.format({
                'WinRate': '{:.1f}%',
                'ConversionRate': '{:.1f}%'
            }).background_gradient(subset=['Pts', 'GD'], cmap='Purples'),
            height=480,
            use_container_width=True
        )
        
    with col_bars:
        st.markdown("### 🎯 Top CLB Ghi Bàn & Tỷ Lệ Chuyển Hóa")
        top_scorers_club = standings.sort_values('GF', ascending=False).head(8)
        fig_clubs = px.bar(
            top_scorers_club,
            x='GF', y='Team',
            orientation='h',
            title='<b>Top 8 CLB Ghi Nhiều Bàn Thắng Nhất</b>',
            color='ConversionRate',
            color_continuous_scale='Viridis',
            labels={'GF': 'Số bàn thắng', 'ConversionRate': 'Tỷ lệ chuyển hóa (%)'}
        )
        fig_clubs.update_layout(yaxis={'categoryorder': 'total ascending'}, height=480)
        st.plotly_chart(fig_clubs, use_container_width=True)
        
    # So sánh trực tiếp nhóm "Big Six"
    st.markdown("### ⚔️ So Sánh Trực Tiếp Nhóm \"Big Six\"")
    big_six = ['Manchester City', 'Manchester United', 'Liverpool', 'Arsenal', 'Chelsea', 'Tottenham']
    b6_df = standings[standings['Team'].isin(big_six)].sort_values('Pts', ascending=False)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        fig_b6_pts = px.bar(
            b6_df, x='Team', y='Pts',
            title='<b>Tổng Điểm Tích Lũy Nhóm Big Six</b>',
            color='Team',
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        st.plotly_chart(fig_b6_pts, use_container_width=True)
    with col_b2:
        fig_b6_eff = px.scatter(
            b6_df, x='ShotAccuracy', y='ConversionRate',
            size='GF', color='Team', text='Team',
            title='<b>Độ Chính Xác Sút vs Tỷ Lệ Chuyển Hóa Cơ Hội (Big Six)</b>',
            labels={'ShotAccuracy': 'Sút trúng đích (%)', 'ConversionRate': 'Chuyển hóa bàn thắng (%)'}
        )
        fig_b6_eff.update_traces(textposition='top center')
        st.plotly_chart(fig_b6_eff, use_container_width=True)

# ============================================================
# TRANG 3: PHÂN TÍCH CẦU THỦ CHUYÊN SÂU & xG
# ============================================================
elif selected_page == "👟 Phân Tích Cầu Thủ & xG":
    st.markdown("""
    <div class="main-header">
        <h1>👟 Phân Tích Cầu Thủ Chuyên Sâu & Bàn Thắng Kỳ Vọng (xG)</h1>
        <p>Kho dữ liệu hơn 5,800 cầu thủ qua 11 mùa giải với các chỉ số hiệu suất tiên tiến: xG, xA, Per 90 metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bộ lọc cầu thủ
    c_f1, c_f2, c_f3, c_f4 = st.columns(4)
    with c_f1:
        p_seasons = ["Tất cả các mùa (Tổng hợp sự nghiệp)"] + sorted(players_df['Season'].unique().tolist(), reverse=True)
        chosen_p_season = st.selectbox("Mùa giải:", p_seasons)
    with c_f2:
        p_clubs = ["Tất cả CLB"] + sorted(players_df['Club'].dropna().unique().tolist())
        chosen_club = st.selectbox("Câu lạc bộ:", p_clubs)
    with c_f3:
        p_positions = ["Tất cả vị trí", "Forward", "Midfielder", "Defender", "Goalkeeper"]
        chosen_pos = st.selectbox("Vị trí:", p_positions)
    with c_f4:
        min_minutes = st.slider("Số phút thi đấu tối thiểu:", 0, 3000, 900, step=100)
        
    # Xử lý lọc dữ liệu
    if chosen_p_season == "Tất cả các mùa (Tổng hợp sự nghiệp)":
        p_filtered = players_df.groupby('Player').agg(
            Club=('Club', lambda x: x.mode()[0] if not x.empty else 'Unknown'),
            PositionGroup=('PositionGroup', lambda x: x.mode()[0] if not x.empty else 'Forward'),
            Appearances=('Appearances', 'sum'),
            Minutes=('Minutes', 'sum'),
            Goals=('Goals', 'sum'),
            Assists=('Assists', 'sum'),
            Shots=('Shots', 'sum'),
            KeyPasses=('KeyPasses', 'sum'),
            xG=('xG', 'sum'),
            xA=('xA', 'sum')
        ).reset_index()
    else:
        p_filtered = players_df[players_df['Season'] == chosen_p_season].copy()
        
    if chosen_club != "Tất cả CLB":
        p_filtered = p_filtered[p_filtered['Club'] == chosen_club]
    if chosen_pos != "Tất cả vị trí":
        p_filtered = p_filtered[p_filtered['PositionGroup'] == chosen_pos]
        
    p_filtered = p_filtered[p_filtered['Minutes'] >= min_minutes].copy()
    
    # Tính Per 90 metrics
    p_filtered['GoalsPer90'] = np.where(p_filtered['Minutes'] > 0, (p_filtered['Goals'] / p_filtered['Minutes']) * 90, 0)
    p_filtered['AssistsPer90'] = np.where(p_filtered['Minutes'] > 0, (p_filtered['Assists'] / p_filtered['Minutes']) * 90, 0)
    p_filtered['xG_Diff'] = p_filtered['Goals'] - p_filtered['xG'] # > 0: Overperform
    
    # Top KPI Metrics Cầu thủ
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(p_filtered):,}</div><div class="metric-label">Số Lượng Cầu Thủ Đạt Chuẩn</div></div>""", unsafe_allow_html=True)
    with c2:
        top_scorer_name = p_filtered.sort_values('Goals', ascending=False).iloc[0]['Player'] if len(p_filtered) > 0 else 'N/A'
        top_scorer_goals = p_filtered.sort_values('Goals', ascending=False).iloc[0]['Goals'] if len(p_filtered) > 0 else 0
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{int(top_scorer_goals)} ({top_scorer_name})</div><div class="metric-label">Vua Phá Lưới</div></div>""", unsafe_allow_html=True)
    with c3:
        top_ast_name = p_filtered.sort_values('Assists', ascending=False).iloc[0]['Player'] if len(p_filtered) > 0 else 'N/A'
        top_ast_val = p_filtered.sort_values('Assists', ascending=False).iloc[0]['Assists'] if len(p_filtered) > 0 else 0
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{int(top_ast_val)} ({top_ast_name})</div><div class="metric-label">Vua Kiến Tạo</div></div>""", unsafe_allow_html=True)
    with c4:
        top_p90 = p_filtered.sort_values('GoalsPer90', ascending=False).iloc[0] if len(p_filtered) > 0 else None
        p90_text = f"{top_p90['GoalsPer90']:.2f} ({top_p90['Player']})" if top_p90 is not None else 'N/A'
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{p90_text}</div><div class="metric-label">Hiệu Suất / 90 Phút Cao Nhất</div></div>""", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Biểu đồ Scatter: Bàn Thắng Thực Tế vs xG
    st.markdown("### 🎯 Phân Tích Độ Hiệu Quả Dứt Điểm: Bàn Thắng Thực Tế vs Bàn Thắng Kỳ Vọng (xG)")
    fig_scatter = px.scatter(
        p_filtered,
        x='xG', y='Goals',
        size='Shots',
        color='PositionGroup',
        hover_name='Player',
        hover_data=['Club', 'Minutes', 'GoalsPer90', 'xG_Diff'],
        title='<b>Bàn Thắng Thực Tế (Goals) vs Bàn Thắng Kỳ Vọng (xG) | Đường đỏ: Goals = xG</b>',
        labels={'xG': 'Bàn thắng kỳ vọng (xG)', 'Goals': 'Bàn thắng thực tế (Goals)'},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    # Đường xG = Goals
    max_axis = max(p_filtered['Goals'].max() if len(p_filtered)>0 else 10, p_filtered['xG'].max() if len(p_filtered)>0 else 10) + 2
    fig_scatter.add_shape(
        type='line', line=dict(dash='dash', color='red', width=2),
        x0=0, x1=max_axis, y0=0, y1=max_axis
    )
    fig_scatter.update_layout(height=520)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Bảng xếp hạng chi tiết
    st.markdown("### 📊 Bảng Xếp Hạng Chi Tiết Cầu Thủ")
    st.dataframe(
        p_filtered[['Player', 'Club', 'PositionGroup', 'Minutes', 'Goals', 'Assists', 'GoalsPer90', 'Shots', 'xG', 'xA', 'xG_Diff']]
        .sort_values('Goals', ascending=False)
        .style.format({
            'GoalsPer90': '{:.2f}',
            'xG': '{:.2f}',
            'xA': '{:.2f}',
            'xG_Diff': '{:+.2f}'
        }).background_gradient(subset=['Goals', 'xG_Diff'], cmap='RdYlGn'),
        height=380,
        use_container_width=True
    )

# ============================================================
# TRANG 4: SO SÁNH ĐỐI ĐẦU CẦU THỦ
# ============================================================
elif selected_page == "⚔️ So Sánh Đối Đầu Cầu Thủ":
    st.markdown("""
    <div class="main-header">
        <h1>⚔️ So Sánh Đối Đầu Cầu Thủ (Head-to-Head)</h1>
        <p>Chọn bất kỳ 2 cầu thủ để so sánh trực diện các chỉ số chuyên môn trong toàn bộ sự nghiệp tại EPL</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tổng hợp sự nghiệp
    career = players_df.groupby('Player').agg(
        Club=('Club', lambda x: ', '.join(sorted(x.unique()))),
        PositionGroup=('PositionGroup', lambda x: x.mode()[0] if not x.empty else 'Forward'),
        Seasons=('Season', 'nunique'),
        Minutes=('Minutes', 'sum'),
        Goals=('Goals', 'sum'),
        Assists=('Assists', 'sum'),
        Shots=('Shots', 'sum'),
        KeyPasses=('KeyPasses', 'sum'),
        xG=('xG', 'sum'),
        xA=('xA', 'sum')
    ).reset_index()
    
    career['GoalsPer90'] = np.where(career['Minutes'] > 0, (career['Goals'] / career['Minutes']) * 90, 0)
    career['AssistsPer90'] = np.where(career['Minutes'] > 0, (career['Assists'] / career['Minutes']) * 90, 0)
    career['ShotsPer90'] = np.where(career['Minutes'] > 0, (career['Shots'] / career['Minutes']) * 90, 0)
    career['ConversionRate'] = np.where(career['Shots'] > 0, (career['Goals'] / career['Shots']) * 100, 0)
    
    # Danh sách cầu thủ có thi đấu
    player_list = sorted(career[career['Minutes'] >= 1000]['Player'].unique())
    
    c_sel1, c_sel2 = st.columns(2)
    with c_sel1:
        default_p1 = 'Harry Kane' if 'Harry Kane' in player_list else player_list[0]
        player1 = st.selectbox("Chọn Cầu Thủ 1:", player_list, index=player_list.index(default_p1))
    with c_sel2:
        default_p2 = 'Mohamed Salah' if 'Mohamed Salah' in player_list else player_list[1]
        player2 = st.selectbox("Chọn Cầu Thủ 2:", player_list, index=player_list.index(default_p2))
        
    p1_data = career[career['Player'] == player1].iloc[0]
    p2_data = career[career['Player'] == player2].iloc[0]
    
    # Profile cards
    cp1, cp2 = st.columns(2)
    with cp1:
        st.markdown(f"""
        <div style="background:#f1f5f9; padding:16px; border-radius:10px; border-left:6px solid #38003c;">
            <h3 style="margin:0; color:#38003c;">{player1}</h3>
            <p style="margin:4px 0; color:#64748b;"><b>CLB:</b> {p1_data['Club']} | <b>Vị trí:</b> {p1_data['PositionGroup']}</p>
            <p style="margin:0; color:#64748b;"><b>Số mùa giải thi đấu:</b> {p1_data['Seasons']} | <b>Số phút:</b> {p1_data['Minutes']:,} phút</p>
        </div>
        """, unsafe_allow_html=True)
    with cp2:
        st.markdown(f"""
        <div style="background:#f1f5f9; padding:16px; border-radius:10px; border-left:6px solid #00ff87;">
            <h3 style="margin:0; color:#0284c7;">{player2}</h3>
            <p style="margin:4px 0; color:#64748b;"><b>CLB:</b> {p2_data['Club']} | <b>Vị trí:</b> {p2_data['PositionGroup']}</p>
            <p style="margin:0; color:#64748b;"><b>Số mùa giải thi đấu:</b> {p2_data['Seasons']} | <b>Số phút:</b> {p2_data['Minutes']:,} phút</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Biểu đồ cột đối chiếu các chỉ số
    metrics_to_compare = [
        ('Bàn Thắng (Goals)', 'Goals'),
        ('Kiến Tạo (Assists)', 'Assists'),
        ('Bàn Thắng / 90 Phút', 'GoalsPer90'),
        ('Kiến Tạo / 90 Phút', 'AssistsPer90'),
        ('Cú Sút / 90 Phút', 'ShotsPer90'),
        ('Tỷ Lệ Chuyển Hóa (%)', 'ConversionRate'),
        ('Bàn Thắng Kỳ Vọng (xG)', 'xG'),
        ('Kiến Tạo Kỳ Vọng (xA)', 'xA')
    ]
    
    comp_df = pd.DataFrame([
        {'Chỉ số': label, player1: p1_data[col], player2: p2_data[col]}
        for label, col in metrics_to_compare
    ])
    
    col_chart_comp, col_table_comp = st.columns([3, 2])
    
    with col_chart_comp:
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=comp_df['Chỉ số'], y=comp_df[player1], name=player1, marker_color='#38003c'))
        fig_comp.add_trace(go.Bar(x=comp_df['Chỉ số'], y=comp_df[player2], name=player2, marker_color='#00ff87'))
        fig_comp.update_layout(
            title=f'<b>Đối Đầu Trực Tiếp: {player1} vs {player2}</b>',
            barmode='group',
            height=460,
            hovermode='x unified'
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
    with col_table_comp:
        st.markdown("### 📋 Bảng Thống Kê So Sánh")
        st.table(comp_df.set_index('Chỉ số').style.format('{:.2f}'))

# ============================================================
# TRANG 5: DỰ ĐOÁN KẾT QUẢ TRẬN ĐẤU (AI MATCH PREDICTOR)
# ============================================================
elif selected_page == "🔮 Dự Đoán Kết Quả Trận Đấu":
    st.markdown("""
    <div class="main-header">
        <h1>🔮 AI Match Predictor: Mô Phỏng Dự Đoán Trận Đấu</h1>
        <p>Ứng dụng mô hình Random Forest huấn luyện trên 20 năm dữ liệu phong độ để dự báo xác suất Thắng / Hòa / Thua</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Train nhanh model Random Forest
    @st.cache_resource
    def train_prediction_model():
        # Xây dựng bảng rolling features
        team_matches = []
        for idx, row in matches_df.iterrows():
            team_matches.append({
                'match_id': idx, 'Date': row['Date'], 'Team': row['HomeTeam'], 'IsHome': 1,
                'GoalsFor': row['FTHG'], 'GoalsAgainst': row['FTAG'],
                'Shots': row['HS'], 'ShotsOnTarget': row['HST'],
                'Points': 3 if row['FTR'] == 'H' else (1 if row['FTR'] == 'D' else 0),
                'Win': 1 if row['FTR'] == 'H' else 0
            })
            team_matches.append({
                'match_id': idx, 'Date': row['Date'], 'Team': row['AwayTeam'], 'IsHome': 0,
                'GoalsFor': row['FTAG'], 'GoalsAgainst': row['FTHG'],
                'Shots': row['AS'], 'ShotsOnTarget': row['AST'],
                'Points': 3 if row['FTR'] == 'A' else (1 if row['FTR'] == 'D' else 0),
                'Win': 1 if row['FTR'] == 'A' else 0
            })
        tm_df = pd.DataFrame(team_matches).sort_values(['Date', 'match_id']).reset_index(drop=True)
        
        team_rolling = []
        for team, group in tm_df.groupby('Team'):
            g = group.copy()
            g['Rolling_GF_5'] = g['GoalsFor'].shift(1).rolling(5, min_periods=3).mean()
            g['Rolling_GA_5'] = g['GoalsAgainst'].shift(1).rolling(5, min_periods=3).mean()
            g['Rolling_Pts_5'] = g['Points'].shift(1).rolling(5, min_periods=3).sum()
            g['Rolling_Shots_5'] = g['Shots'].shift(1).rolling(5, min_periods=3).mean()
            g['Rolling_SoT_5'] = g['ShotsOnTarget'].shift(1).rolling(5, min_periods=3).mean()
            g['Cum_WinRate'] = g['Win'].shift(1).expanding(min_periods=5).mean()
            team_rolling.append(g)
            
        feat_all = pd.concat(team_rolling, ignore_index=True)
        
        stat_cols = ['Rolling_GF_5', 'Rolling_GA_5', 'Rolling_Pts_5', 'Rolling_Shots_5', 'Rolling_SoT_5', 'Cum_WinRate']
        home_f = feat_all[feat_all['IsHome'] == 1][['match_id'] + stat_cols]
        home_f.columns = ['match_id'] + ['Home_' + c for c in stat_cols]
        
        away_f = feat_all[feat_all['IsHome'] == 0][['match_id'] + stat_cols]
        away_f.columns = ['match_id'] + ['Away_' + c for c in stat_cols]
        
        ml_df = matches_df.reset_index().rename(columns={'index': 'match_id'})
        ml_df = ml_df.merge(home_f, on='match_id').merge(away_f, on='match_id')
        
        f_cols = [
            'Home_Rolling_GF_5', 'Home_Rolling_GA_5', 'Home_Rolling_Pts_5', 'Home_Rolling_Shots_5', 'Home_Rolling_SoT_5', 'Home_Cum_WinRate',
            'Away_Rolling_GF_5', 'Away_Rolling_GA_5', 'Away_Rolling_Pts_5', 'Away_Rolling_Shots_5', 'Away_Rolling_SoT_5', 'Away_Cum_WinRate'
        ]
        
        clean = ml_df.dropna(subset=f_cols).copy()
        clean['Target'] = clean['FTR'].map({'A': 0, 'D': 1, 'H': 2})
        
        rf = RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42)
        rf.fit(clean[f_cols], clean['Target'])
        
        # Lưu lại phong độ gần nhất của từng đội
        latest_team_stats = {}
        for team, group in tm_df.groupby('Team'):
            last_matches = group.tail(5)
            cum_win = group['Win'].mean()
            latest_team_stats[team] = {
                'Rolling_GF_5': last_matches['GoalsFor'].mean(),
                'Rolling_GA_5': last_matches['GoalsAgainst'].mean(),
                'Rolling_Pts_5': last_matches['Points'].sum(),
                'Rolling_Shots_5': last_matches['Shots'].mean(),
                'Rolling_SoT_5': last_matches['ShotsOnTarget'].mean(),
                'Cum_WinRate': cum_win
            }
            
        return rf, latest_team_stats, f_cols
    
    with st.spinner("Đang tải mô hình Machine Learning..."):
        model, latest_stats, f_cols = train_prediction_model()
        
    teams_available = sorted(list(latest_stats.keys()))
    
    st.markdown("### ⚽ Chọn Cặp Đấu Cần Dự Đoán:")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        home_team = st.selectbox("Đội Chủ Nhà (Home Team):", teams_available, index=teams_available.index('Arsenal') if 'Arsenal' in teams_available else 0)
    with col_t2:
        away_options = [t for t in teams_available if t != home_team]
        away_team = st.selectbox("Đội Khách (Away Team):", away_options, index=away_options.index('Chelsea') if 'Chelsea' in away_options else 0)
        
    # Tạo vector đặc trưng
    h_s = latest_stats[home_team]
    a_s = latest_stats[away_team]
    
    input_vector = np.array([[
        h_s['Rolling_GF_5'], h_s['Rolling_GA_5'], h_s['Rolling_Pts_5'], h_s['Rolling_Shots_5'], h_s['Rolling_SoT_5'], h_s['Cum_WinRate'],
        a_s['Rolling_GF_5'], a_s['Rolling_GA_5'], a_s['Rolling_Pts_5'], a_s['Rolling_Shots_5'], a_s['Rolling_SoT_5'], a_s['Cum_WinRate']
    ]])
    
    probs = model.predict_proba(input_vector)[0] # [P(Away), P(Draw), P(Home)]
    p_away = probs[0] * 100
    p_draw = probs[1] * 100
    p_home = probs[2] * 100
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hiển thị xác suất
    st.markdown("### 📊 Kết Quả Dự Báo Xác Suất Từ AI:")
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 5px solid #2ecc71;">
            <div class="metric-value" style="color:#2ecc71;">{p_home:.1f}%</div>
            <div class="metric-label">{home_team} Thắng (Home Win)</div>
        </div>
        """, unsafe_allow_html=True)
    with c_p2:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 5px solid #f39c12;">
            <div class="metric-value" style="color:#f39c12;">{p_draw:.1f}%</div>
            <div class="metric-label">Hòa (Draw)</div>
        </div>
        """, unsafe_allow_html=True)
    with c_p3:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 5px solid #e74c3c;">
            <div class="metric-value" style="color:#e74c3c;">{p_away:.1f}%</div>
            <div class="metric-label">{away_team} Thắng (Away Win)</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Biểu đồ Gauge / Bar xác suất
    fig_prob = go.Figure(go.Bar(
        x=[p_home, p_draw, p_away],
        y=[f'{home_team} Thắng', 'Hòa', f'{away_team} Thắng'],
        orientation='h',
        marker_color=['#2ecc71', '#f39c12', '#e74c3c'],
        text=[f'{p_home:.1f}%', f'{p_draw:.1f}%', f'{p_away:.1f}%'],
        textposition='auto'
    ))
    fig_prob.update_layout(
        title='<b>Phân Bố Xác Suất Kết Quả Trận Đấu</b>',
        xaxis=dict(title='Xác suất (%)', range=[0, 100]),
        height=320
    )
    st.plotly_chart(fig_prob, use_container_width=True)
    
    # Bảng so sánh phong độ 5 trận gần nhất
    st.markdown("### 📋 So Sánh Phong Độ Gần Nhất Trước Trận:")
    form_comparison = pd.DataFrame({
        'Chỉ số phong độ gần nhất': [
            'Điểm số 5 trận gần nhất',
            'Bàn thắng TB / trận (5 trận)',
            'Bàn thua TB / trận (5 trận)',
            'Cú sút TB / trận (5 trận)',
            'Sút trúng đích TB / trận (5 trận)',
            'Tỷ lệ thắng tích lũy toàn giải'
        ],
        home_team: [
            f"{h_s['Rolling_Pts_5']:.0f} điểm",
            f"{h_s['Rolling_GF_5']:.2f}",
            f"{h_s['Rolling_GA_5']:.2f}",
            f"{h_s['Rolling_Shots_5']:.1f}",
            f"{h_s['Rolling_SoT_5']:.1f}",
            f"{h_s['Cum_WinRate']*100:.1f}%"
        ],
        away_team: [
            f"{a_s['Rolling_Pts_5']:.0f} điểm",
            f"{a_s['Rolling_GF_5']:.2f}",
            f"{a_s['Rolling_GA_5']:.2f}",
            f"{a_s['Rolling_Shots_5']:.1f}",
            f"{a_s['Rolling_SoT_5']:.1f}",
            f"{a_s['Cum_WinRate']*100:.1f}%"
        ]
    })
    st.table(form_comparison.set_index('Chỉ số phong độ gần nhất'))
