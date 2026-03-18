import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title=os.getenv('DASHBOARD_TITLE', 'Pharma-CompIntel AI Insights'),
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

LATEST_FILE = os.getenv('LATEST_FILENAME', 'pharma_compintel_latest.csv')

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_list_field(val):
    if isinstance(val, list):
        return val
    if isinstance(val, str) and val.startswith('['):
        try:
            return json.loads(val.replace("'", '"'))
        except Exception:
            pass
    return [val] if val and val != 'Not Available' else ['Not Available']

def load_data():
    if not os.path.exists(LATEST_FILE):
        return pd.DataFrame()
    df = pd.read_csv(LATEST_FILE)
    return df

# ── CI Scoring ────────────────────────────────────────────────────────────────

def calculate_ci_scores(df):
    if df.empty:
        return {}
    phase_scores = {'Phase 3': 90, 'Phase 2': 70, 'Phase 1': 50,
                    'Pre-clinical': 30, 'Not Available': 20}

    def avg_list_len(col):
        counts = []
        for v in df[col].fillna('[]'):
            if isinstance(v, str) and v.startswith('['):
                try:
                    counts.append(len(json.loads(v.replace("'", '"'))))
                except Exception:
                    counts.append(0)
            else:
                counts.append(0)
        return sum(counts) / len(counts) if counts else 0

    clinical = sum(phase_scores.get(p, 20) for p in df['clinical_phase'].fillna('Not Available')) / len(df)
    market_caps = pd.to_numeric(df['market_cap'], errors='coerce').fillna(0)
    scores = {
        'Clinical Maturity': clinical,
        'Financial Stability': min(85, (market_caps.mean() / 1e9) * 10),
        'Pipeline Diversification': min(90, avg_list_len('pipeline') * 20),
        'Partnership Activity': min(80, avg_list_len('partnerships') * 25),
        'Regulatory Strength': min(95, avg_list_len('approved_products') * 30),
    }
    scores['Innovation Index'] = (scores['Clinical Maturity'] + scores['Pipeline Diversification']) / 2
    return scores

# ── Dashboard ─────────────────────────────────────────────────────────────────

def main():
    st.title("🧬 Pharma-CompIntel AI Insights")
    st.markdown("*Automated Competitive Intelligence for Pharmaceutical & Biotech Companies*")

    df = load_data()

    if df.empty:
        st.warning("No data found. Run the fetcher first:")
        st.code("python nasdaq_fetcher.py")
        return

    # ── Sidebar filters
    st.sidebar.header("🔍 Filters")
    disease_areas = ['All'] + sorted(df['disease_area'].dropna().unique().tolist())
    phases = ['All'] + sorted(df['clinical_phase'].dropna().unique().tolist())
    countries = ['All'] + sorted(df['country'].dropna().unique().tolist())

    selected_disease = st.sidebar.selectbox("Disease Area", disease_areas)
    selected_phase = st.sidebar.selectbox("Clinical Phase", phases)
    selected_country = st.sidebar.selectbox("Country", countries)
    min_cap = st.sidebar.number_input("Min Market Cap (B$)", value=0.0, step=0.1)

    # ── Apply filters
    filtered = df.copy()
    if selected_disease != 'All':
        filtered = filtered[filtered['disease_area'] == selected_disease]
    if selected_phase != 'All':
        filtered = filtered[filtered['clinical_phase'] == selected_phase]
    if selected_country != 'All':
        filtered = filtered[filtered['country'] == selected_country]
    if min_cap > 0:
        filtered = filtered[pd.to_numeric(filtered['market_cap'], errors='coerce') >= min_cap * 1e9]

    # ── KPIs
    ci_scores = calculate_ci_scores(filtered)
    risk_index = sum(ci_scores.values()) / len(ci_scores) if ci_scores else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Companies", len(filtered))
    c2.metric("Active Trials", len(filtered[filtered['clinical_phase'].isin(['Phase 1', 'Phase 2', 'Phase 3'])]))
    c3.metric("Avg Market Cap", f"${pd.to_numeric(filtered['market_cap'], errors='coerce').mean() / 1e9:.1f}B")
    c4.metric("Risk Index", f"{risk_index:.0f}/100")

    # ── Forest plot
    st.subheader("📊 CI Domain Scores")
    if ci_scores:
        domains, values = list(ci_scores.keys()), list(ci_scores.values())
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[max(0, v - 10) for v in values] + [min(100, v + 10) for v in values][::-1],
            y=domains + domains[::-1],
            fill='toself', fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'), showlegend=False
        ))
        fig.add_trace(go.Scatter(x=values, y=domains, mode='markers',
                                 marker=dict(size=12, color='darkblue'), name='CI Score'))
        fig.add_vline(x=70, line_dash="dash", line_color="red", annotation_text="Industry Benchmark")
        fig.update_layout(xaxis_title="CI Score (0-100)", yaxis_title="CI Domains",
                          height=400, showlegend=False)
        st.plotly_chart(fig, width='stretch')

    # ── Company table — one row per disease
    st.subheader("🏢 Company Analysis")
    if not filtered.empty:
        expanded = []
        for _, row in filtered.iterrows():
            for disease in parse_list_field(row.get('diseases', 'Not Available')):
                expanded.append({
                    'Symbol': row['symbol'],
                    'Company': row['name'],
                    'Disease Area': row.get('disease_area', 'N/A'),
                    'Disease': disease,
                    'Clinical Phase': row.get('clinical_phase', 'N/A'),
                    'Lead Product': row.get('lead_product', 'N/A'),
                    'Market Cap (B$)': round(pd.to_numeric(row.get('market_cap', 0), errors='coerce') / 1e9, 2),
                    'Country': row.get('country', 'N/A'),
                    'Partnerships': row.get('partnerships', 'N/A'),
                })
        st.dataframe(pd.DataFrame(expanded), width='stretch')
        st.download_button("📥 Download Full Dataset", filtered.to_csv(index=False),
                           file_name=f"pharma_compintel_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv")

    # ── Charts
    st.subheader("📈 Market Analysis")
    c1, c2 = st.columns(2)
    with c1:
        phase_counts = filtered['clinical_phase'].value_counts()
        if not phase_counts.empty:
            st.plotly_chart(px.pie(values=phase_counts.values, names=phase_counts.index,
                                   title="Clinical Phase Distribution"), width='stretch')
    with c2:
        disease_counts = filtered['disease_area'].value_counts().head(10)
        if not disease_counts.empty:
            st.plotly_chart(px.bar(x=disease_counts.values, y=disease_counts.index,
                                   orientation='h', title="Top Disease Areas"), width='stretch')

    # ── Company profile detail
    st.subheader("🔬 Company Profiles")
    if not filtered.empty:
        selected = st.selectbox("Select Company", filtered['name'].tolist())
        if selected:
            c = filtered[filtered['name'] == selected].iloc[0]
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Symbol:** {c['symbol']}")
                st.write(f"**Disease Area:** {c.get('disease_area', 'N/A')}")
                st.write(f"**Clinical Phase:** {c.get('clinical_phase', 'N/A')}")
                st.write(f"**Lead Product:** {c.get('lead_product', 'N/A')}")
                st.write(f"**Technology:** {c.get('technology', 'N/A')}")
            with col2:
                st.write(f"**Market Cap:** ${pd.to_numeric(c.get('market_cap', 0), errors='coerce') / 1e9:.2f}B")
                st.write(f"**Country:** {c.get('country', 'N/A')}")
                st.write(f"**Website:** {c.get('website', 'N/A')}")
                st.markdown(f"[Pipeline Info]({c.get('pipeline_link', '#')})")
                st.markdown(f"[Clinical Trials]({c.get('clinical_trials_link', '#')})")
            st.write("**Company Profile:**")
            st.write(c.get('profile', 'N/A'))

if __name__ == "__main__":
    main()
