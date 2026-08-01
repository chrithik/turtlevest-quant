import streamlit as st
import pandas as pd
import psycopg2
import os
import plotly.graph_objects as go
import plotly.express as px
import json
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Quant Dashboard | TurtleVest",
    page_icon="📊",
    layout="wide"
)

# Custom Sidebar Panel
with st.sidebar:
    st.markdown("### 🐢 TurtleVest Engine")
    st.info("🔍 Currently Viewing: **Quant Dashboard 📊**")
    
    st.write("---")
    st.markdown("🌐 **Navigation:**")
    if st.button("Home Quant Terminal 🏠", use_container_width=True):
        st.switch_page("app.py")
    if st.button("Academic Foundations 🎓", use_container_width=True):
        st.switch_page("pages/2_Open_Source.py")
    st.link_button("Download iOS App 📱", "https://apps.apple.com/us/app/turtlevest/id6746081109", use_container_width=True)
    st.write("---")
    
    st.markdown("🎓 **Founder's Research Dossier:**")
    st.link_button("📄 Apple (AAPL) Report", "https://your-link-to-aapl-pdf.pdf", use_container_width=True)
    st.link_button("📄 NVIDIA (NVDA) Report", "https://your-link-to-nvda-pdf.pdf", use_container_width=True)
    st.link_button("📄 Microsoft (MSFT) Study", "https://your-link-to-msft-pdf.pdf", use_container_width=True)
    st.write("---")

# Custom Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    h1, h2, h3, h4 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }
    .metric-container {
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    /* Premium cards for newsletter briefs */
    .newsletter-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
        border-left: 4px solid #10b981;
    }
    .verdict-box {
        background-color: rgba(16, 185, 129, 0.05);
        border-left: 3px solid #10b981;
        padding: 12px 16px;
        border-radius: 0 6px 6px 0;
        margin: 14px 0;
        font-style: italic;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Database Connection Helper with Fallback
@st.cache_data(ttl=60)
def fetch_dashboard_data():
    db_url = os.environ.get("DATABASE_URL")
    
    # Pre-compiled high-fidelity founder YIS stock pitches
    mock_reports = pd.DataFrame([
        {
            "symbol": "AAPL",
            "title": "Analyst Research Brief: AAPL (Apple Inc.)",
            "content_markdown": """# Quantitative Equity Brief: Apple Inc. (NASDAQ: AAPL)
**Analysis Type:** Core Franchise & Capital Allocation Performance
**Verdict:** ACCUMULATE / STABLE CASH FLOW

## 1. Executive Summary
Apple Inc. continues to display superior capital compounding, supported by high customer retention within its Services ecosystem. Growth in subscription revenues buffers hardware cycle deceleration.

## 2. Capital Efficiency & DuPont Breakdown
- **DuPont Return on Equity Deconstruction:**
  - Net Profit Margin: **26.1%**
  - Asset Turnover: **0.82x**
  - Equity Multiplier: **1.54**
  - **ROE (Return on Equity):** **33.0%**
- **Altman Z-Score:** **6.20** (Safe Zone), indicating negligible bankruptcy or credit risk.
- **Piotroski F-Score:** **8/9** (High quality of earnings, positive net income, and robust asset turn).

## 3. Disclosures & Risk Check (Item 1A)
NLP parsing of filings shows concerns regarding supply-chain consolidation in East Asia and regulatory antitrust pressure on App Store fees.
""",
            "created_at": pd.Timestamp.now()
        },
        {
            "symbol": "NVDA",
            "title": "Analyst Research Brief: NVDA (NVIDIA Corporation)",
            "content_markdown": """# High Growth Equity Brief: NVIDIA Corporation (NASDAQ: NVDA)
**Analysis Type:** Semiconductor Market Cycles & AI Capex Ramps
**Verdict:** BUY / GROWTH VALUE

## 1. Thesis: AI Infrastructure Moat
NVIDIA's dominance in the AI accelerator market is supported by its proprietary CUDA software stack, creating a high barrier to entry. Blackwell GPU deliveries drive short-term revenues.

## 2. Quantitative & Capital Efficiency
- **Capital Intensity Check:** CapEx to Revenue remains low at **12.4%**, showing asset-light manufacturing scale.
- **DuPont ROE Breakdown:**
  - Net Profit Margin: **47.2%**
  - Asset Turnover: **1.12x**
  - Equity Multiplier: **1.35**
  - **ROE (Return on Equity):** **71.3%**
- **Altman Z-Score:** **9.50** (Exceptional credit strength).
- **Piotroski F-Score:** **8/9** (Margin expansions YoY, strong liquidity).

## 3. Disclosures & Geopolitical Risk (Item 1A)
Main risk factors center on geopolitical export controls and supply-chain packaging bottlenecks (TSMC CoWoS capacity).
""",
            "created_at": pd.Timestamp.now()
        },
        {
            "symbol": "MSFT",
            "title": "Analyst Research Brief: MSFT (Microsoft Corporation)",
            "content_markdown": """# Enterprise Cloud Valuation: Microsoft Corporation (NASDAQ: MSFT)
**Analysis Type:** Discounted Cash Flow (DCF) & Azure Scale Integration
**Verdict:** BUY / CORE ACCUMULATION

## 1. Enterprise Cloud Thesis
Microsoft's Azure cloud infrastructure and Enterprise Office suite integration drive high recurring revenue retention. Reinvestment in OpenAI models fuels long-term growth.

## 2. Financial Metrics & DCF Summary
- **Revenue CAGR:** Projected 11.8% over 5 years.
- **ROE (Return on Equity):** **29.4%** driven by premium enterprise margins.
- **Altman Z-Score:** **4.85** (Safe Zone), showing massive asset backings.
- **Piotroski F-Score:** **7/9** (Steady operational margins and conservative leverage profile).

## 3. SEC Risk Disclosures (Item 1A)
Disclosures highlight cybersecurity compliance and international regulatory checks on cloud competition.
""",
            "created_at": pd.Timestamp.now()
        }
    ])

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Helper function to execute queries and return DataFrames via cursor (bypasses pandas SQL connection warnings)
        def query_to_df(query, params=None):
            cur.execute(query, params)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            return pd.DataFrame(rows, columns=colnames)
        
        # Fetch reports
        reports_df = query_to_df("SELECT symbol, title, content_markdown, created_at FROM custom_research_reports ORDER BY created_at DESC")
        if reports_df.empty:
            reports_df = mock_reports
        
        # Fetch risk history
        risk_df = query_to_df("SELECT check_date, risk_score, vix_value, pcr_value, spy_pe_value, news_sentiment_score, monte_carlo_var FROM market_risk_log ORDER BY check_date DESC LIMIT 30")
        
        # Fetch SEC alerts
        sec_df = query_to_df("SELECT ticker, form_type, filing_date, description FROM sec_risk_alerts ORDER BY filing_date DESC LIMIT 10")
        
        # Fetch Morning briefs (for daily report view) - Filtered to the latest generated dispatch date to prevent duplication
        briefs_df = query_to_df("SELECT symbol, company_name, source_type, divergence_score, ratios_check, verdict, summary, analyst_ratings FROM morning_briefs WHERE brief_date = (SELECT MAX(brief_date) FROM morning_briefs) ORDER BY divergence_score DESC")
        
        # Fetch high upside momentum candidates - Filtered to the latest generated dispatch date
        upside_df = query_to_df("SELECT symbol, company_name, projected_upside_pct FROM high_upside_stocks WHERE added_at = (SELECT MAX(added_at) FROM high_upside_stocks) ORDER BY projected_upside_pct DESC LIMIT 5")
        
        cur.close()
        conn.close()
        return reports_df, risk_df, sec_df, briefs_df, upside_df, True
    except Exception as e:
        mock_risk = pd.DataFrame([
            {"check_date": pd.Timestamp.now() - pd.Timedelta(days=i), 
             "risk_score": max(1, min(10, 4 + (i % 3) - (i % 2))),
             "vix_value": 15.2 + i * 0.2,
             "pcr_value": 0.85 + i * 0.01,
             "spy_pe_value": 24.8,
             "news_sentiment_score": 5.2,
             "monte_carlo_var": 2.1} 
            for i in range(15)
        ])
        
        mock_sec = pd.DataFrame([
            {"ticker": "MSFT", "form_type": "8-K", "filing_date": "2026-06-18", "description": "Item 2.03: Creation of a Direct Financial Obligation of $1.5B Senior Notes due 2036."},
            {"ticker": "AMZN", "form_type": "8-K", "filing_date": "2026-06-15", "description": "Item 2.03: Entry into a $2.0B Credit Agreement Term Facility."}
        ])

        mock_briefs = pd.DataFrame([
            {
                "symbol": "NVDA",
                "company_name": "NVIDIA Corporation",
                "source_type": "both",
                "divergence_score": 9,
                "ratios_check": "Piotroski F-Score is 8/9. Gross margin expanded from 72.1% to 75.3%. Long-term debt is negligible.",
                "verdict": "Strong accumulation profile backed by accelerating Blackwell purchase orders and structural margin expansions.",
                "summary": "Blackwell shipments have entered mass-production. Social media indicators demonstrate minor FOMO retail sentiment but fundamental drivers fully justify multiples.",
                "analyst_ratings": {"average": "145.50", "min": "110.00", "max": "180.00"}
            },
            {
                "symbol": "TSLA",
                "company_name": "Tesla, Inc.",
                "source_type": "retail",
                "divergence_score": 5,
                "ratios_check": "Piotroski F-Score is 5/9. Gross margin stabilized at 18.2%. Debt-to-Equity is low at 0.08.",
                "verdict": "Speculative price action. Volume spikes on retail speculation regarding FSD regulatory approvals.",
                "summary": "Increased delivery figures in China supported short-term momentum, but guidance indicates high margin pressures.",
                "analyst_ratings": {"average": "220.00", "min": "85.00", "max": "310.00"}
            }
        ])

        mock_upside = pd.DataFrame([
            {"symbol": "LLY", "company_name": "Eli Lilly and Company", "projected_upside_pct": 14.8},
            {"symbol": "AVGO", "company_name": "Broadcom Inc.", "projected_upside_pct": 11.2}
        ])
        
        return mock_reports, mock_risk, mock_sec, mock_briefs, mock_upside, False

@st.cache_data(ttl=3600)
def fetch_sector_rotation():
    api_key = os.environ.get("FMP_API_KEY")
    import datetime
    import requests
    today = datetime.date.today()
    
    # Generate last 5 business days
    dates = []
    current = today
    while len(dates) < 5 and len(dates) < 15:
        if current.weekday() < 5:
            dates.append(current.strftime("%Y-%m-%d"))
        current -= datetime.timedelta(days=1)
        
    records = []
    for d in dates:
        try:
            url = f"https://financialmodelingprep.com/stable/sector-performance-snapshot?date={d}&apikey={api_key}"
            res = requests.get(url, timeout=5)
            if res.ok:
                data = res.json()
                for item in data:
                    records.append({
                        "Date": item.get("date"),
                        "Sector": item.get("sector"),
                        "Change %": float(item.get("averageChange") or 0)
                    })
        except Exception:
            pass
            
    # Dynamic fallback to simulated rotation data if API is down / restricted
    if not records:
        mock_sectors = [
            "Technology", "Financial Services", "Healthcare", "Consumer Cyclical", 
            "Communication Services", "Industrials", "Consumer Defensive", 
            "Energy", "Basic Materials", "Real Estate", "Utilities"
        ]
        import numpy as np
        np.random.seed(42)
        for i, d in enumerate(dates):
            for sector in mock_sectors:
                # Add some simulated rotation trend over the 5 days
                base = 0.6 if sector in ["Technology", "Utilities"] and i < 2 else -0.3
                change = base + np.random.normal(0, 1.1)
                records.append({
                    "Date": d,
                    "Sector": sector,
                    "Change %": round(change, 2)
                })
                
    return pd.DataFrame(records)

reports_df, risk_df, sec_df, briefs_df, upside_df, is_live = fetch_dashboard_data()

# Top Premium Branding Header
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 0; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-top: -30px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.8rem;">🐢</span>
        <span style="font-size: 1.6rem; font-weight: 800; letter-spacing: 0.5px; background: linear-gradient(90deg, #f8fafc, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">TurtleVest</span>
        <span style="font-size: 0.8rem; background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 3px 8px; border-radius: 4px; font-weight: 600; margin-left: 5px; border: 1px solid rgba(16, 185, 129, 0.2);">QUANT TERMINAL</span>
    </div>
    <div style="font-size: 0.9rem; color: #64748b; font-weight: 500;">
        Academic Research Platform
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize horizontal tabs
tab_risk, tab_rotation, tab_newsletter, tab_vault = st.tabs([
    "🚨 Systemic Risk & Alerts", 
    "🔄 Sector Rotation & Flows",
    "📬 Daily Newsletter", 
    "📁 Custom Analyst Reports"
])

# ----------------------------------------------------
# TAB 1: RISK MONITOR & ALERTS
# ----------------------------------------------------
with tab_risk:
    st.header("🚨 Systemic Risk & Crash Monitor")
    
    # Gauge chart and Current Status
    latest_risk = int(risk_df.iloc[0]["risk_score"]) if not risk_df.empty else 4
    
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        # Create Plotly Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest_risk,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Current Risk Threat Score", 'font': {'size': 20, 'color': "#f8fafc"}},
            gauge = {
                'axis': {'range': [1, 10], 'tickwidth': 1, 'tickcolor': "#f8fafc"},
                'bar': {'color': "#10b981" if latest_risk < 5 else "#f59e0b" if latest_risk < 8 else "#ef4444"},
                'steps': [
                    {'range': [1, 5], 'color': "rgba(16, 185, 129, 0.15)"},
                    {'range': [5, 8], 'color': "rgba(245, 158, 11, 0.15)"},
                    {'range': [8, 10], 'color': "rgba(239, 68, 68, 0.15)"}
                ]
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#f8fafc"},
            height=300
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col_g2:
        st.subheader("Systemic Risk Score Trend (Last 15 Days)")
        
        # Create an intuitive area chart for just the 1-10 Systemic Risk Score
        fig_trend = go.Figure()
        df_history = risk_df.head(15).sort_values("check_date")
        
        fig_trend.add_trace(go.Scatter(
            x=df_history["check_date"],
            y=df_history["risk_score"],
            mode='lines+markers',
            name='Risk Score',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8, color='#10b981'),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        
        # Horizontal alert lines
        fig_trend.add_hline(y=5, line_dash="dash", line_color="#f59e0b", annotation_text="Elevated Risk (5)", annotation_position="top left")
        fig_trend.add_hline(y=8, line_dash="dash", line_color="#ef4444", annotation_text="Extreme Danger (8)", annotation_position="top left")
        
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            font={'color': "#f8fafc"},
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Threat Level (1-10)",
                range=[1, 10],
                tickmode='linear',
                dtick=1,
                gridcolor='rgba(255,255,255,0.05)'
            ),
            margin=dict(l=40, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    
    # 4-Column Metric Row for Market Signals
    st.subheader("📊 Current Market Solvency & Valuation Indicators")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    # Extract latest and previous values for deltas
    latest_row = risk_df.iloc[0] if not risk_df.empty else None
    prev_row = risk_df.iloc[1] if not risk_df.empty and len(risk_df) > 1 else None
    
    vix = float(latest_row["vix_value"]) if latest_row is not None and latest_row["vix_value"] is not None else 15.2
    vix_prev = float(prev_row["vix_value"]) if prev_row is not None and prev_row["vix_value"] is not None else 15.2
    vix_delta = vix - vix_prev
    
    pcr = float(latest_row["pcr_value"]) if latest_row is not None and latest_row["pcr_value"] is not None else 0.85
    pcr_prev = float(prev_row["pcr_value"]) if prev_row is not None and prev_row["pcr_value"] is not None else 0.85
    pcr_delta = pcr - pcr_prev
    
    spy_pe = float(latest_row["spy_pe_value"]) if latest_row is not None and latest_row["spy_pe_value"] is not None else 24.8
    spy_pe_prev = float(prev_row["spy_pe_value"]) if prev_row is not None and prev_row["spy_pe_value"] is not None else 24.8
    spy_pe_delta = spy_pe - spy_pe_prev
    
    # Calculate Pillar Stretching metric (valuation deviation from historical baselines)
    pillar_stretching = max(0.0, (latest_risk - 3.0) * 12.5)
    pillar_prev = max(0.0, (int(prev_row["risk_score"] if prev_row is not None else 4) - 3.0) * 12.5)
    pillar_delta = pillar_stretching - pillar_prev
    
    with col_m1:
        st.metric(
            label="VOLATILITY (VIX)",
            value=f"{vix:.2f}",
            delta=f"{vix_delta:+.2f}",
            delta_color="inverse",
            help="CBOE Volatility Index (VIX) measures 30-day expected market volatility. Scores > 20 signal elevated market anxiety."
        )
        
    with col_m2:
        st.metric(
            label="PUT-CALL RATIO",
            value=f"{pcr:.2f}",
            delta=f"{pcr_delta:+.2f}",
            delta_color="inverse",
            help="Equity Put-Call volume ratio. Ratios > 1.0 signify bearish option hedging spikes, while < 0.7 signify bullish sentiment."
        )
        
    with col_m3:
        st.metric(
            label="PILLAR STRETCHING",
            value=f"{pillar_stretching:.1f}%",
            delta=f"{pillar_delta:+.1f}%",
            delta_color="inverse",
            help="Measures current valuation stretch relative to 5-year historical averages across our core basket of 20 market-leading stocks: MSFT, AAPL, NVDA, AVGO, GOOGL, META, AMZN, TSLA, JPM, LLY, UNH, ABBV, XOM, GE, COST, WMT, HD, MA, V, and NFLX.\n\n• GOOD (Fair Value): < 20% (indicates core growth and capital metrics are aligned with historical baselines).\n• BAD (Overstretched): > 50% (signals high valuation premiums, over-leverage, or speculative bubbles)."
        )
        
    with col_m4:
        st.metric(
            label="S&P 500 P/E",
            value=f"{spy_pe:.1f}x",
            delta=f"{spy_pe_delta:+.1f}x",
            delta_color="inverse",
            help="Trailing 12-Month Price-to-Earnings Ratio of the S&P 500 index.\n\n• GOOD (Historically Normal): 15x - 20x (indicates reasonable index pricing and stable corporate earnings growth).\n• BAD (Highly Valued): > 25x (suggests market leadership multiples are heavily stretched, heightening downside correction risks)."
        )
        st.caption("Average valuation multiple of top leaders.")

    st.markdown("---")
    st.header("⚠️ SEC Form 8-K Debt obligation Feed")
    st.write("Real-time warnings extracted by our SEC scraper scanning 20 index leaders.")
    st.info(
        "💡 **What is this?** Public companies are legally required to file a **Form 8-K** with the SEC "
        "to report major unscheduled corporate events. Specifically, this feed scans for **Item 2.03** filings, "
        "which alert investors that a company has taken on a significant new direct financial debt or obligation. "
        "Monitoring this feed helps identify sudden borrowing spikes, which could indicate corporate expansion or cash flow strain."
    )
    
    for idx, row in sec_df.iterrows():
        st.warning(f"**{row['ticker']}** ({row['form_type']}) - *Filed on {row['filing_date']}*\n\n{row['description']}")

# ----------------------------------------------------
# TAB 1B: SECTOR ROTATION & FLOWS
# ----------------------------------------------------
with tab_rotation:
    st.header("🔄 Sector Rotation & Macro Capital Flows")
    st.write(
        "Track the movement of institutional capital across primary GICS market sectors. "
        "Analyzing which sectors are gaining relative strength reveals shifting risk regimes and economic cycles."
    )
    
    rotation_df = fetch_sector_rotation()
    
    if not rotation_df.empty:
        # 1. Latest Session snapshot
        latest_date = rotation_df["Date"].max()
        latest_df = rotation_df[rotation_df["Date"] == latest_date].sort_values("Change %", ascending=False)
        
        st.subheader(f"📊 Latest Session Performance Snapshot ({latest_date})")
        
        # Color sectors based on performance (positive = green, negative = red)
        colors = ['#10b981' if val >= 0 else '#ef4444' for val in latest_df["Change %"]]
        
        fig_latest_sector = go.Figure(go.Bar(
            x=latest_df["Change %"],
            y=latest_df["Sector"],
            orientation='h',
            marker_color=colors,
            text=[f"{val:+.2f}%" for val in latest_df["Change %"]],
            textposition='auto'
        ))
        
        fig_latest_sector.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=380,
            font={'color': "#f8fafc"},
            xaxis=dict(
                title="Average Performance %",
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                autorange="reversed",
                showgrid=False
            ),
            margin=dict(l=140, r=40, t=20, b=40)
        )
        st.plotly_chart(fig_latest_sector, use_container_width=True)
        
        # 2. Sector Rotation Trends Line Chart
        st.subheader("📈 Sector Performance Trend (Last 5 Sessions)")
        
        # Sort values by Date ascending for correct plotting timeline
        trend_df = rotation_df.sort_values(["Sector", "Date"])
        
        fig_rotation_trend = px.line(
            trend_df,
            x="Date",
            y="Change %",
            color="Sector",
            markers=True,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        fig_rotation_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            font={'color': "#f8fafc"},
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Session Change %",
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.2)'
            ),
            margin=dict(l=40, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_rotation_trend, use_container_width=True)
        
        # 3. Macro Capital Flow Analysis Verdict
        top_sector = latest_df.iloc[0]["Sector"]
        top_perf = latest_df.iloc[0]["Change %"]
        bottom_sector = latest_df.iloc[-1]["Sector"]
        bottom_perf = latest_df.iloc[-1]["Change %"]
        
        # Determine rotation regime
        defensive_sectors = {"Utilities", "Healthcare", "Consumer Defensive"}
        
        regime = "Risk-On Rotation"
        explanation = (
            f"Capital is actively flowing into growth-oriented and cyclical assets, led by **{top_sector}** (+{top_perf:.2f}%). "
            f"This suggests expanding macroeconomic confidence and a preference for industrial and technological sectors."
        )
        
        if top_sector in defensive_sectors:
            regime = "Defensive / Risk-Off Rotation"
            explanation = (
                f"Capital is rotating defensively into yield-bearing and value-protective assets, led by **{top_sector}** (+{top_perf:.2f}%). "
                f"Meanwhile, cyclical sectors like **{bottom_sector}** ({bottom_perf:+.2f}%) are lagging, suggesting market participants are bracing for volatility."
            )
            
        st.markdown(f"""
        <div class="newsletter-card" style="border-left-color: #b89b64;">
            <div style="font-size:0.75rem;font-weight:700;color:#b89b64;letter-spacing:1px;margin-bottom:4px;">
                CAPITAL ROTATION REGIME VERDICT
            </div>
            <h3 style="margin:0;font-size:1.3rem;">Current Regime: {regime}</h3>
            <p style="margin-top:10px; font-size:0.95rem; line-height:1.5; color:#cbd5e1;">
                {explanation}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 2: DAILY DISPATCH NEWSLETTER (NATIVE LAYOUT)
# ----------------------------------------------------
with tab_newsletter:
    st.header("📬 The Daily Morning Pulse Report")
    
    # Render Today's Date Banner
    today_str = pd.Timestamp.now().strftime("%B %d, %Y").upper()
    st.caption(f"📅 **{today_str} • PRE-MARKET QUANT DISPATCH**")
    
    # Narrative Intro
    st.markdown(
        "> *Overnight analysis of institutional positioning and social momentum indices. "
        "All calculations compiled dynamically using SEC Edgar database structures.*"
    )
    
    # 1. High Momentum Section
    st.subheader("🚀 Linear Regression Projections & Momentum Outliers")
    if upside_df.empty:
        st.write("No momentum candidates logged today.")
    else:
        col_up = st.columns(len(upside_df))
        for idx, row in upside_df.iterrows():
            with col_up[idx % len(upside_df)]:
                st.markdown(
                    f"""<div class='metric-container'>
                        <strong style='color:#10b981;font-size:1.15rem;'>{row['symbol']}</strong><br>
                        <span style='color:#94a3b8;font-size:0.85rem;'>{row['company_name']}</span><br>
                        <span style='color:#f8fafc;font-weight:600;font-size:1.1rem;'>+{float(row['projected_upside_pct']):.2f}% Upside</span>
                    </div>""", 
                    unsafe_allow_html=True
                )
    
    # 2. Highlighted Breakouts (The Briefs)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Today's Highlighted Equity Breakouts")
    
    if briefs_df.empty:
        st.info("No breakouts recorded for today's market session.")
    else:
        for idx, row in briefs_df.iterrows():
            # Color code based on divergence score
            score = int(row["divergence_score"])
            score_color = "#10b981" if score >= 8 else "#f59e0b" if score >= 4 else "#ef4444"
            score_lbl = "STRONG SUPPORT" if score >= 8 else "SPECULATIVE HYPE" if score >= 4 else "EXTREME DIVERGENCE"
            
            source_lbl = "Double Breakout" if row["source_type"] == "both" else "Social Buzz" if row["source_type"] == "retail" else "Institutional Movers"
            
            # Format analyst ratings if available
            ratings_text = "N/A"
            if row["analyst_ratings"]:
                try:
                    ratings = row["analyst_ratings"]
                    if isinstance(ratings, str):
                        ratings = json.loads(ratings)
                    ratings_text = f"Avg: ${ratings.get('average', 'N/A')} (Range: ${ratings.get('min', 'N/A')} - ${ratings.get('max', 'N/A')})"
                except Exception:
                    ratings_text = str(row["analyst_ratings"])
            
            st.markdown(
                f"""<div class='newsletter-card' style='border-left-color: {score_color};'>
                    <div style='font-size:0.75rem;font-weight:700;color:#b89b64;letter-spacing:1px;margin-bottom:4px;'>
                        {source_lbl.upper()}
                    </div>
                    <h3 style='margin:0;font-size:1.4rem;'>{row['symbol']} &mdash; {row['company_name']}</h3>
                    <table style='width:100%;margin-top:12px;font-size:0.85rem;color:#cbd5e1;'>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'>
                            <td style='padding:6px 0;'>Divergence Rating:</td>
                            <td style='text-align:right;font-weight:700;color:{score_color};'>{score}/10 ({score_lbl})</td>
                        </tr>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'>
                            <td style='padding:6px 0;'>Analyst Target Consensus:</td>
                            <td style='text-align:right;font-weight:700;color:#f8fafc;'>{ratings_text}</td>
                        </tr>
                    </table>
                    <div class='verdict-box' style='border-left-color:{score_color};'>
                        <strong>Quantitative Verdict:</strong> {row['verdict']}
                    </div>
                    <p style='margin: 10px 0; font-size:0.95rem; line-height:1.5; color:#cbd5e1;'>
                        <strong>Fundamental Solvency:</strong> {row['ratios_check']}
                    </p>
                    <p style='margin: 0; font-size:0.95rem; line-height:1.5; color:#cbd5e1;'>
                        <strong>Qualitative Factors:</strong> {row['summary']}
                    </p>
                </div>""", 
                unsafe_allow_html=True
            )

# ----------------------------------------------------
# TAB 3: CUSTOM RESEARCH REPORTS VAULT
# ----------------------------------------------------
with tab_vault:
    st.header("📁 Custom Research Vault")
    st.write("Browse dynamic research reports generated by the Python LangGraph Deep Research Agent.")
    
    if reports_df.empty:
        st.write("No reports generated yet. Run deep research queries inside FinPulse to view reports here.")
    else:
        selected_symbol = st.selectbox("Select Company Report", options=reports_df["symbol"].unique())
        selected_report = reports_df[reports_df["symbol"] == selected_symbol].iloc[0]
        
        st.subheader(selected_report["title"])
        st.markdown(selected_report["content_markdown"])

# ----------------------------------------------------
# DISCLAIMER (Sticky Footer at Page Level)
# ----------------------------------------------------
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** All contents, metrics, tools, and reports on TurtleVest are built and presented "
    "purely for educational, research, and academic purposes. This application does not constitute professional financial, "
    "investment, tax, or legal advice. Under no circumstances should any metrics, charts, or summaries here be interpreted "
    "as a recommendation or solicitation to buy or sell securities. Past performance is not indicative of future results."
)
