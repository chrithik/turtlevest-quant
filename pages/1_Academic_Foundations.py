import streamlit as st

st.set_page_config(
    page_title="Open Source & Architecture | TurtleVest",
    page_icon="🎓",
    layout="wide"
)

# Custom Sidebar config is managed globally in config.toml

st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    h1, h2, h3 {
        color: #f8fafc !important;
    }
    .latex-box {
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# TOP NAVIGATION BAR
# ----------------------------------------------------
col_nav1, col_nav2, col_nav3, _ = st.columns([1.2, 1.6, 1.4, 3.8])
with col_nav1:
    st.page_link("app.py", label="Home Terminal", icon="🏠")
with col_nav2:
    st.page_link("pages/1_Academic_Foundations.py", label="Academic Foundations", icon="🎓")
with col_nav3:
    st.link_button("Download iOS App 📱", "https://apps.apple.com/us/app/turtlevest/id6746081109", use_container_width=True)

st.write("---")

st.title("🎓 Academic Thesis & Technical Foundations")
st.write(
    "TurtleVest is built on the belief that retail investors deserve the same analytical rigour "
    "as institutional desks. Below we document the core mathematical formulas, database structures, "
    "and pipeline schemas powering this site."
)

st.write("---")

# ----------------------------------------------------
# 1. CORE ALGORITHMIC EQUATIONS
# ----------------------------------------------------
st.header("🧮 Quantitative Frameworks & Ratios")

col_eq1, col_eq2 = st.columns(2)

with col_eq1:
    st.subheader("1. DuPont Return on Equity (ROE) Decomposition")
    st.write(
        "Standard ROE shows returns, but hides *how* they were generated. We decompose ROE into "
        "profitability, asset turnover, and financial leverage components to detect warning signs."
    )
    st.markdown("""
    <div class="latex-box">
    """, unsafe_allow_html=True)
    st.latex(r"ROE = \frac{\text{Net Income}}{\text{Revenue}} \times \frac{\text{Revenue}}{\text{Assets}} \times \frac{\text{Assets}}{\text{Equity}}")
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        "- **Net Profit Margin** (Operating Efficiency)\n"
        "- **Asset Turnover** (Asset Use Efficiency)\n"
        "- **Equity Multiplier** (Financial Leverage)"
    )

with col_eq2:
    st.subheader("2. Altman Z-Score (Manufacturing/General Corporate)")
    st.markdown(
        "Predicts the probability that a firm will enter bankruptcy within two years. "
        "A Z-Score > <span style='color:#10b981; font-weight:bold;'>3.0</span> indicates 'Safe Zone'; "
        "< <span style='color:#ef4444; font-weight:bold;'>1.8</span> indicates 'Distress Zone'.",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="latex-box">
    """, unsafe_allow_html=True)
    st.latex(r"Z = 1.2 A + 1.4 B + 3.3 C + 0.6 D + 0.999 E")
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        "- **A**: Working Capital / Total Assets\n"
        "- **B**: Retained Earnings / Total Assets\n"
        "- **C**: EBIT / Total Assets\n"
        "- **D**: Market Value of Equity / Total Liabilities\n"
        "- **E**: Sales / Total Assets"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. PIOTROSKI F-SCORE CRITERIA
# ----------------------------------------------------
st.subheader("3. Piotroski F-Score (9-Point Fundamental Strength Check)")
st.write(
    "A binary scoring system assessing financial strength. The score goes from 0 to 9 based on "
    "meeting the following conditions year-over-year:"
)

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("### 📈 Profitability")
    st.markdown(
        "1. **Positive Net Income** (+1 if current year Net Income > 0)\n"
        "2. **Positive Return on Assets (ROA)** (+1 if current year ROA > 0)\n"
        "3. **Positive Cash Flow from Operations (CFO)** (+1 if CFO > 0)\n"
        "4. **Quality of Earnings** (+1 if CFO > Net Income)"
    )

with col_f2:
    st.markdown("### ⚖️ Leverage & Liquidity")
    st.markdown(
        "5. **Lower Debt Ratio** (+1 if long-term debt-to-assets decreased YoY)\n"
        "6. **Higher Current Ratio** (+1 if current ratio increased YoY)\n"
        "7. **No Share Dilution** (+1 if no new common shares were issued YoY)"
    )

with col_f3:
    st.markdown("### ⚙️ Operating Efficiency")
    st.markdown(
        "8. **Higher Gross Margin** (+1 if YoY Gross Margin percentage expanded)\n"
        "9. **Higher Asset Turnover** (+1 if YoY Asset Turnover ratio increased)"
    )


# ----------------------------------------------------
# 2. CREDIT RISK MODELING & REGULATORY FRAMEWORKS
# ----------------------------------------------------
st.markdown("---")
st.header("🏦 Credit Risk Modeling & Regulatory Frameworks")
st.write(
    "When assessing a corporate borrower's creditworthiness, quantitative analysts look at the intersection "
    "of balance-sheet distress models (micro-level risk) and banking regulatory capital frameworks (macro-level risk)."
)

col_cr1, col_cr2 = st.columns(2)

with col_cr1:
    st.subheader("A. Corporate Credit Assessment (Altman Z-Score)")
    st.write(
        "Lending institutions use the Altman Z-Score (defined in Section 1 above) as a primary quantitative input "
        "to gauge the borrower's default risk. By converting the resulting Z-Score index into a standardized "
        "credit rating (e.g., AAA, BB, CCC), risk management teams can map the index score to an empirical "
        "**Probability of Default (PD)** over a 1-year horizon."
    )
    st.markdown(
        "For example, a high Z-score (Safe Zone) maps to a low default probability, while a low Z-score (Distress Zone) "
        "triggers a high default probability. This PD rating serves as the foundational input for regulatory capital calculations."
    )

with col_cr2:
    st.subheader("B. Basel II Capital Accord (Regulatory Credit Risk)")
    st.write(
        "Under the Basel II framework, banks calculate the regulatory capital required to hold against credit risk. "
        "The core mathematical parameter is the **Expected Loss (EL)**, calculated as:"
    )
    st.latex(r"EL = PD \times LGD \times EAD")
    st.markdown(
        "- **Probability of Default (PD)**: The statistical likelihood of a borrower defaulting over a 1-year horizon "
        "(often modeled using financial health proxies like the Altman Z-Score).\n"
        "- **Loss Given Default (LGD)**: The percentage of the loan exposure lost if default occurs (calculated "
        "net of collateral liquidations).\n"
        "- **Exposure at Default (EAD)**: The gross dollar exposure outstanding when default happens."
    )

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📊 Applied Case Study: Corporate Borrowing Analysis")
st.write(
    "To demonstrate how these models interface, let's analyze a hypothetical corporate borrower seeking a "
    "**USD 10,000,000 credit facility** (Exposure at Default, or EAD):"
)

col_cs1, col_cs2 = st.columns(2)

with col_cs1:
    st.markdown("#### Step 1: Altman Z-Score Estimation")
    st.markdown(
        "Assuming a company with the following balance sheet metrics:\n"
        "- **Total Assets**: $50,000,000\n"
        "- **Total Liabilities**: $10,000,000\n"
        "- **Market Cap (Equity)**: $40,000,000\n"
        "- **Working Capital**: $5,000,000\n"
        "- **Retained Earnings**: $8,000,000\n"
        "- **EBIT**: $6,000,000\n"
        "- **Sales**: $20,000,000"
    )
    st.write("Calculating the five constituent ratios:")
    st.latex(r"X_1 = \frac{\text{Working Capital}}{\text{Total Assets}} = \frac{\$5,000,000}{\$50,000,000} = \mathbf{0.10}")
    st.latex(r"X_2 = \frac{\text{Retained Earnings}}{\text{Total Assets}} = \frac{\$8,000,000}{\$50,000,000} = \mathbf{0.16}")
    st.latex(r"X_3 = \frac{\text{EBIT}}{\text{Total Assets}} = \frac{\$6,000,000}{\$50,000,000} = \mathbf{0.12}")
    st.latex(r"X_4 = \frac{\text{Market Value of Equity}}{\text{Total Liabilities}} = \frac{\$40,000,000}{\$10,000,000} = \mathbf{4.00}")
    st.latex(r"X_5 = \frac{\text{Sales}}{\text{Total Assets}} = \frac{\$20,000,000}{\$50,000,000} = \mathbf{0.40}")
    st.write("Calculating the score:")
    st.latex(r"Z = 1.2(0.10) + 1.4(0.16) + 3.3(0.12) + 0.6(4.00) + 0.999(0.40) = \mathbf{3.54}")
    st.success("🟢 **Verdict**: Z-Score is **3.54**, placing the borrower securely in the **Safe Zone**.")

with col_cs2:
    st.markdown("#### Step 2: Basel II Expected Loss Calculation")
    st.markdown(
        "Using the credit rating derived from the borrower's high Z-Score, the lending bank models the risk parameters:\n"
        "- **Probability of Default (PD)** is modeled at a low **1.5%** (0.015).\n"
        "- The bank secures the loan against high-quality corporate real estate, reducing the **Loss Given Default (LGD)** to **30%** (0.30).\n"
        "- **Exposure at Default (EAD)** is the outstanding **$10,000,000** loan facility."
    )
    st.write("Calculating the Expected Loss:")
    st.latex(r"EL = 1.5\% \times 30\% \times \$10,000,000 = \mathbf{\$45,000}")
    st.info(
        "📈 **Bank Risk Outcome**: The bank models a statistical expected loss of only **$45,000** (0.45% of the total exposure), "
        "justifying credit extension at a lower prime rate."
    )

st.markdown("---")

# ----------------------------------------------------
# 3. PIPELINE SCHEMA
# ----------------------------------------------------
st.header("🔀 Data Pipeline & Architecture")
st.write("Our data scheduler is optimized to scrape, clean, calculate, and synthesize metrics autonomously:")

st.markdown("""
```text
+-----------------------+     +------------------------+     +-------------------------+
| SEC Edgar RSS Feed    |     | FMP Stable REST API    |     | Google Gemini API       |
| (Form 8-K debt scan)  |     | (Financial Statements) |     | (Catalyst Analysis)     |
+-----------+-----------+     +-----------+------------+     +------------+------------+
            |                             |                               |
            |                             v                               |
            |                 +-----------------------+                   |
            +---------------->| Python Data Parser    |<------------------+
                              | & Calculator Engine   |
                              +-----------+-----------+
                                          |
                                          v
                              +-----------------------+
                              | Postgres Database Log |
                              +-----------+-----------+
                                          |
                                          v
                              +-----------------------+
                              | Streamlit Dashboard   |
                              +-----------------------+
```
""")

st.subheader("🔒 SEC Scraper Rate Limits & User-Agent Compliance")
st.code("""
# Custom SEC Compliant headers used in scraping scripts:
headers = {
    "User-Agent": "TurtleVest Researcher student@turtlevest.com",
    "Accept-Encoding": "gzip, deflate"
}
""", language="python")

# ----------------------------------------------------
# 5. DISCLAIMER
# ----------------------------------------------------
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** All contents, metrics, tools, and reports on TurtleVest are built and presented "
    "purely for educational, research, and academic purposes. This application does not constitute professional financial, "
    "investment, tax, or legal advice. Under no circumstances should any metrics, charts, or summaries here be interpreted "
    "as a recommendation or solicitation to buy or sell securities. Past performance is not indicative of future results."
)


