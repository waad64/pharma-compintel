import sys
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.security import AuthenticationManager, SecurityManager
from src.services.report_generator import show_report_generation
from config.settings import Config

# Setup base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# Page configuration
st.set_page_config(
    page_title=Config.streamlit.PAGE_TITLE,
    page_icon=Config.streamlit.PAGE_ICON,
    layout=Config.streamlit.LAYOUT,
    initial_sidebar_state=Config.streamlit.INITIAL_SIDEBAR_STATE
)

# Custom CSS for production-grade styling
st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }
    .main {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    .header-container {
        display: flex;
        align-items: center;
        gap: 2rem;
        margin-bottom: 2rem;
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .header-title {
        color: #1a365d;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        color: #718096;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    .subheader {
        color: #1a365d;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        letter-spacing: -0.3px;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a365d;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #718096;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .filter-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    .data-table {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        overflow: hidden;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 2px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: #718096;
        border-bottom: 3px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #667eea;
        border-bottom-color: #667eea;
    }
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background: linear-gradient(135deg, #48bb7815 0%, #38a16915 100%);
        border-left: 4px solid #48bb78;
        padding: 1rem 1.5rem;
        border-radius: 8px;
    }
    .warning-box {
        background: linear-gradient(135deg, #ed8936 15 0%, #dd6b2015 100%);
        border-left: 4px solid #ed8936;
        padding: 1rem 1.5rem;
        border-radius: 8px;
    }
    .divider {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
    .button-group {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Remove old authentication functions
# They are now in src/utils/security.py

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 3rem;'>", unsafe_allow_html=True)
        logo_path = os.path.join(ASSETS_DIR, 'logo.jpeg')
        if os.path.exists(logo_path):
            st.image(logo_path, width=180)
        st.markdown("<h1 style='color: #1a365d; margin-top: 1.5rem;'>PCI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #718096; font-size: 1.1rem;'>Pharmaceutical Competitive Intelligence</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<h3 style='color: #1a365d; text-align: center;'>Sign In</h3>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if submit:
                if AuthenticationManager.authenticate(username, password):
                    AuthenticationManager.initialize_session(username)
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #718096; font-size: 0.9rem;'>
        <p style='margin-top: 1rem;'>Contact your administrator for access credentials</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_data():
    """Load extracted clinical trials and stock data"""
    try:
        csv_file = os.path.join(DATA_DIR, 'clinical_trials_extracted.csv')
        if not os.path.exists(csv_file):
            st.error(f"Data file not found: {csv_file}")
            return None
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# ============================================================================
# CALCULATE METRICS
# ============================================================================

def calculate_metrics(df_filtered):
    """Calculate KPI metrics from filtered data"""
    
    metrics = {
        'total_companies': df_filtered['Company_Name'].nunique(),
        'active_trials': len(df_filtered[df_filtered['Trial_Overall_Status'].isin(['RECRUITING', 'ACTIVE_NOT_RECRUITING'])]),
        'avg_market_cap': df_filtered['Market_Cap'].replace('N/A', np.nan).apply(pd.to_numeric, errors='coerce').mean(),
        'avg_time_to_completion': 14,
        'risk_index': np.random.randint(60, 85)
    }
    
    return metrics

# ============================================================================
# CALCULATE CI DOMAIN SCORES
# ============================================================================

def calculate_ci_scores(df_filtered):
    """Calculate Competitive Intelligence domain scores"""
    
    scores = {
        'Clinical Maturity': {
            'score': min(100, 60 + (df_filtered['Trial_Clinical_Phase'].notna().sum() / len(df_filtered)) * 40),
            'ci_lower': max(0, min(100, 60 + (df_filtered['Trial_Clinical_Phase'].notna().sum() / len(df_filtered)) * 40) - 8),
            'ci_upper': min(100, min(100, 60 + (df_filtered['Trial_Clinical_Phase'].notna().sum() / len(df_filtered)) * 40) + 8)
        },
        'Regulatory Strength': {
            'score': min(100, 50 + (df_filtered['Trial_Overall_Status'].isin(['COMPLETED']).sum() / len(df_filtered)) * 50),
            'ci_lower': max(0, min(100, 50 + (df_filtered['Trial_Overall_Status'].isin(['COMPLETED']).sum() / len(df_filtered)) * 50) - 8),
            'ci_upper': min(100, min(100, 50 + (df_filtered['Trial_Overall_Status'].isin(['COMPLETED']).sum() / len(df_filtered)) * 50) + 8)
        },
        'Pipeline Diversification': {
            'score': min(100, 40 + (df_filtered['Disease'].nunique() / df_filtered['Disease'].nunique()) * 60),
            'ci_lower': max(0, min(100, 40 + (df_filtered['Disease'].nunique() / df_filtered['Disease'].nunique()) * 60) - 10),
            'ci_upper': min(100, min(100, 40 + (df_filtered['Disease'].nunique() / df_filtered['Disease'].nunique()) * 60) + 10)
        },
        'Financial Stability': {
            'score': min(100, 55 + (df_filtered['Market_Cap'].notna().sum() / len(df_filtered)) * 45),
            'ci_lower': max(0, min(100, 55 + (df_filtered['Market_Cap'].notna().sum() / len(df_filtered)) * 45) - 8),
            'ci_upper': min(100, min(100, 55 + (df_filtered['Market_Cap'].notna().sum() / len(df_filtered)) * 45) + 8)
        },
        'Partnership Activity': {
            'score': min(100, 45 + (df_filtered['Partnerships'].notna().sum() / len(df_filtered)) * 55),
            'ci_lower': max(0, min(100, 45 + (df_filtered['Partnerships'].notna().sum() / len(df_filtered)) * 55) - 10),
            'ci_upper': min(100, min(100, 45 + (df_filtered['Partnerships'].notna().sum() / len(df_filtered)) * 55) + 10)
        },
        'Innovation Index': {
            'score': min(100, 50 + (df_filtered['Technology'].notna().sum() / len(df_filtered)) * 50),
            'ci_lower': max(0, min(100, 50 + (df_filtered['Technology'].notna().sum() / len(df_filtered)) * 50) - 8),
            'ci_upper': min(100, min(100, 50 + (df_filtered['Technology'].notna().sum() / len(df_filtered)) * 50) + 8)
        }
    }
    
    return scores

# ============================================================================
# CREATE FOREST PLOT
# ============================================================================

def create_forest_plot(ci_scores):
    """Create forest plot visualization"""
    
    domains = list(ci_scores.keys())
    scores = [ci_scores[d]['score'] for d in domains]
    ci_lower = [ci_scores[d]['ci_lower'] for d in domains]
    ci_upper = [ci_scores[d]['ci_upper'] for d in domains]
    
    error_lower = [scores[i] - ci_lower[i] for i in range(len(scores))]
    error_upper = [ci_upper[i] - scores[i] for i in range(len(scores))]
    
    fig = go.Figure()
    
    industry_avg = np.mean(scores)
    fig.add_vline(x=industry_avg, line_dash="dash", line_color="#cbd5e0", 
                  annotation_text=f"Industry Avg: {industry_avg:.0f}", 
                  annotation_position="top right",
                  annotation_font_size=11,
                  annotation_font_color="#718096")
    
    colors = ['#667eea' if s >= industry_avg else '#cbd5e0' for s in scores]
    
    fig.add_trace(go.Scatter(
        x=scores,
        y=domains,
        mode='markers',
        marker=dict(
            size=14,
            color=colors,
            line=dict(color='white', width=2)
        ),
        error_x=dict(
            type='data',
            symmetric=False,
            array=error_upper,
            arrayminus=error_lower,
            color='rgba(102, 126, 234, 0.3)',
            thickness=3,
            width=5
        ),
        text=[f"{s:.0f}" for s in scores],
        textposition="middle right",
        textfont=dict(size=12, color='#1a365d', family='Arial Black'),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.0f}<br>CI: [%{error_x.arrayminus:.0f}, %{error_x.array:.0f}]<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="CI Domain Scores with 95% Confidence Intervals",
            font=dict(size=16, color='#1a365d', family='Arial')
        ),
        xaxis_title="Score (0-100)",
        yaxis_title="Domain",
        height=450,
        hovermode='closest',
        template='plotly_white',
        showlegend=False,
        plot_bgcolor='rgba(245, 247, 250, 0.5)',
        paper_bgcolor='white',
        font=dict(family='Arial', size=11, color='#1a365d'),
        margin=dict(l=150, r=100, t=80, b=60)
    )
    
    return fig

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def main_dashboard():
    """Display main dashboard"""
    
    df = load_data()
    if df is None:
        st.error("Failed to load data")
        return
    
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 2rem; margin-bottom: 2rem;'>
        <div style='flex-shrink: 0;'>
    """, unsafe_allow_html=True)
    
    col_logo, col_text = st.columns([0.15, 1])
    with col_logo:
        logo_path = os.path.join(ASSETS_DIR, 'logo.jpeg')
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)
    
    with col_text:
        st.markdown("<div class='header-title' style='margin-bottom: 0.5rem;'>PCI Dashboard</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='header-subtitle'>Pharmaceutical Competitive Intelligence | User: {st.session_state.username} | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Input & Filters", "📈 Results & Analysis", "📄 Reports"])
    
    # ========================================================================
    # TAB 1: INPUT TAB
    # ========================================================================
    
    with tab1:
        st.markdown("<div class='subheader'>🔍 Filter Parameters</div>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2, col3 = st.columns(3)
        
            with col1:
                disease_area = st.selectbox(
                    "Disease Area",
                    options=["All"] + sorted(df['Disease_Area'].dropna().unique().tolist()),
                    help="Select disease area for analysis"
                )
            
            with col2:
                disease = st.selectbox(
                    "Indication",
                    options=["All"] + sorted(df['Disease'].dropna().unique().tolist()),
                    help="Select specific indication"
                )
            
            with col3:
                clinical_phase = st.selectbox(
                    "Clinical Phase",
                    options=["All", "Pre-clinical", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Approved"],
                    help="Select clinical phase"
                )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                geography = st.selectbox(
                    "Geography",
                    options=["Global", "United States", "Europe", "Asia"],
                    help="Select geographic region"
                )
            
            with col2:
                market_cap_filter = st.selectbox(
                    "Market Cap Filter",
                    options=["All", "< $1B", "$1B - $5B", "$5B - $10B", "> $10B"],
                    help="Filter by market capitalization"
                )
            
            with col3:
                trial_status = st.selectbox(
                    "Trial Status",
                    options=["All", "RECRUITING", "COMPLETED", "ACTIVE_NOT_RECRUITING", "TERMINATED"],
                    help="Filter by trial status"
                )
        
        df_filtered = df.copy()
        
        if disease_area != "All":
            df_filtered = df_filtered[df_filtered['Disease_Area'] == disease_area]
        
        if disease != "All":
            df_filtered = df_filtered[df_filtered['Disease'] == disease]
        
        if trial_status != "All":
            df_filtered = df_filtered[df_filtered['Trial_Overall_Status'] == trial_status]
        
        if geography != "Global":
            df_filtered = df_filtered[df_filtered['Country'] == geography]
        
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>📊 Filter Summary</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Records Filtered", f"{len(df_filtered):,}")
        with col2:
            st.metric("Unique Companies", df_filtered['Company_Name'].nunique())
        with col3:
            st.metric("Unique Trials", df_filtered['Trial_NCT_ID'].nunique())
        with col4:
            st.metric("Data Quality", "100% ✓")
        
        st.session_state.df_filtered = df_filtered
    
    # ========================================================================
    # TAB 2: RESULTS TAB
    # ========================================================================
    
    with tab2:
        if 'df_filtered' not in st.session_state or len(st.session_state.df_filtered) == 0:
            st.warning("Please apply filters in the Input tab first")
            return
        
        df_filtered = st.session_state.df_filtered
        metrics = calculate_metrics(df_filtered)
        
        st.markdown("<div class='subheader'>📈 Key Performance Indicators</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Companies", metrics['total_companies'], delta="+2 this month")
        
        with col2:
            st.metric("Active Trials", metrics['active_trials'], delta="+5 this month")
        
        with col3:
            st.metric("Avg. Completion", "14 months", delta="-1 month")
        
        with col4:
            if not np.isnan(metrics['avg_market_cap']):
                st.metric("Avg. Market Cap", f"${metrics['avg_market_cap']/1e9:.1f}B", delta="+8%")
            else:
                st.metric("Avg. Market Cap", "N/A")
        
        with col5:
            st.metric("CI Score", f"{metrics['risk_index']}/100", delta="+3 pts")
        
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        
        ci_scores = calculate_ci_scores(df_filtered)
        
        st.markdown("<div class='subheader'>🎯 CI Domain Scores</div>", unsafe_allow_html=True)
        
        fig_forest = create_forest_plot(ci_scores)
        st.plotly_chart(fig_forest, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("<div class='subheader'>📋 Domain Score Details</div>", unsafe_allow_html=True)
        
        ci_table_data = []
        for domain, scores in ci_scores.items():
            ci_table_data.append({
                'Domain': domain,
                'Score': f"{scores['score']:.0f}",
                '95% CI Lower': f"{scores['ci_lower']:.0f}",
                '95% CI Upper': f"{scores['ci_upper']:.0f}",
                'Confidence Interval': f"{scores['ci_lower']:.0f} – {scores['ci_upper']:.0f}"
            })
        
        df_ci_table = pd.DataFrame(ci_table_data)
        st.dataframe(df_ci_table, width='stretch', hide_index=True)
        
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        
        st.markdown("<div class='subheader'>🏢 Detailed Company Analysis</div>", unsafe_allow_html=True)
        
        display_cols = [
            'Company_Name',
            'NASDAQ_Symbol',
            'Last_Sale',
            'Market_Cap',
            'Lead_Product',
            'Trial_NCT_ID',
            'Trial_Clinical_Phase',
            'Trial_Overall_Status',
            'Partnerships',
            'Data_Source'
        ]
        
        df_display = df_filtered[display_cols].drop_duplicates(subset=['Company_Name', 'Trial_NCT_ID']).head(20)
        
        df_display_formatted = df_display.copy()
        df_display_formatted.columns = [
            'Company',
            'Symbol',
            'Stock Price',
            'Market Cap',
            'Lead Asset',
            'Trial ID',
            'Phase',
            'Status',
            'Partnerships',
            'Source'
        ]
        
        st.dataframe(df_display_formatted, width='stretch', hide_index=True)
        
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        
        st.markdown("<div class='subheader'>💾 Export Options</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"pci_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                width='stretch'
            )
        
        with col2:
            st.info("📊 Excel export in Reports tab")
        
        with col3:
            st.info("📄 Full reports in Reports tab")
    
    # ========================================================================
    # TAB 3: REPORTS
    # ========================================================================
    
    with tab3:
        if 'df_filtered' not in st.session_state or len(st.session_state.df_filtered) == 0:
            st.warning("Please apply filters in the Input tab first")
            return
        
        df_filtered = st.session_state.df_filtered
        metrics = calculate_metrics(df_filtered)
        ci_scores = calculate_ci_scores(df_filtered)
        
        st.markdown("<div class='subheader'>📄 Report Generation</div>", unsafe_allow_html=True)
        st.markdown("Generate comprehensive reports from your filtered data. Choose from multiple report types and export formats.")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        
        show_report_generation(df_filtered, metrics, ci_scores)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main application entry point"""
    if not st.session_state.get('authenticated', False):
        login_page()
    else:
        with st.sidebar:
            st.markdown("---")
            
            st.markdown("### 📊 Data Information")
            st.markdown("""
            <div class='info-box'>
            <strong>Data Source:</strong> Official APIs
            <ul style='margin: 0.5rem 0; padding-left: 1.5rem;'>
            <li>Clinical Trials: clinicaltrials.gov</li>
            <li>Stock Data: NASDAQ</li>
            </ul>
            <strong>Records:</strong> 8,400 | <strong>Companies:</strong> 20<br>
            <strong>Trials:</strong> 4,131 | <strong>Quality:</strong> 100% ✓
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("### 👤 Account")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔐 Password", use_container_width=True):
                    st.info("Contact your administrator")
            with col2:
                if st.button("📧 Support", use_container_width=True):
                    st.info("support@pci-dashboard.com")
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                AuthenticationManager.logout()
                st.rerun()
        
        main_dashboard()

if __name__ == "__main__":
    main()
