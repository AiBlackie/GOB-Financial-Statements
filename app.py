"""
Barbados Government Financial Statements 2023 Dashboard
=====================================================

A comprehensive dashboard for analyzing the Barbados Government Financial 
Statements for year ended March 31, 2023, with focus on the adverse audit opinion.

This dashboard visualizes financial data from the Auditor General's report,
highlighting material misstatements, compliance issues, and financial performance.

Version: 2.0
Date: April 2, 2025
"""

# ============================================================================
# IMPORTS
# ============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Barbados Government Financial Statements 2023",
    page_icon="🇧🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
st.markdown("""
<style>
:root {
    --bb-blue: #00267F;
    --bb-gold: #FFC726;
    --bb-black: #000000;
}

/* Header Styles */
.main-header {
    font-size: 2.5rem;
    color: var(--bb-blue);
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(90deg, var(--bb-blue) 0%, var(--bb-gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-header {
    font-size: 1.8rem;
    color: var(--bb-blue);
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 3px solid var(--bb-gold);
    padding-bottom: 0.5rem;
}

.section-header {
    font-size: 1.3rem;
    color: var(--bb-blue);
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

/* Card Styles */
.financial-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-left: 4px solid var(--bb-blue);
}

.adverse-opinion {
    background: linear-gradient(135deg, #fee 0%, #fff5f5 100%);
    border-left: 4px solid #DC2626;
}

.qualified-item {
    background: linear-gradient(135deg, #fff7e6 0%, #fff3cd 100%);
    border-left: 4px solid #F59E0B;
}

.material-misstatement {
    background: linear-gradient(135deg, #f0f7ff 0%, #e6f7ff 100%);
    border-left: 4px solid #3B82F6;
}

/* UI Elements */
.bb-badge {
    background-color: var(--bb-gold);
    color: var(--bb-blue);
    padding: 4px 12px;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: bold;
    display: inline-block;
    margin-right: 5px;
}

.financial-value {
    font-size: 1.3rem;
    font-weight: bold;
    color: var(--bb-blue);
}

.financial-label {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 5px;
}

.flag-container {
    text-align: center;
    padding: 15px;
    border-radius: 10px;
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
    border: 2px solid #00267F;
    box-shadow: 0 4px 6px rgba(0, 38, 127, 0.1);
}

.quick-stats-box {
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    text-align: center;
}

.quick-stats-value {
    font-size: 2rem;
    font-weight: bold;
    color: var(--bb-blue);
}

.quick-stats-label {
    font-size: 0.9rem;
    color: #666;
    margin-top: 5px;
}

/* Color coding for financial metrics */
.revenue-positive { color: #10B981; font-weight: bold; }
.revenue-negative { color: #DC2626; font-weight: bold; }
.revenue-neutral { color: #6B7280; font-weight: bold; }

.expenditure-high { color: #DC2626; font-weight: bold; }
.expenditure-medium { color: #F59E0B; font-weight: bold; }
.expenditure-low { color: #10B981; font-weight: bold; }

.debt-high { color: #DC2626; font-weight: bold; }
.debt-medium { color: #F59E0B; font-weight: bold; }
.debt-low { color: #10B981; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================
@st.cache_data
def load_financial_data():
    """
    Load and prepare financial data from the PDF report.
    
    Returns:
        dict: Dictionary containing all financial data as DataFrames
    """
    # Financial Performance Data
    financial_performance = pd.DataFrame({
        'Category': [
            'Taxation', 'Goods and Services', 'Income and Profits', 
            'Property Taxes', 'International Trade', 'Other Taxes',
            'Levies, Fees and Fines', 'Special Receipts', 'Other Revenue', 'Grants'
        ],
        'Revised_Budget_2023': [
            2977381493, 1463856504, 1024520055, 227384934, 241200000,
            20420000, 69614799, 2312561, 164208584, 25700000
        ],
        'Actual_2023': [
            3209934907, 1628078161, 1068849288, 240517833, 250253724,
            22235902, 83376897, 1905632, 170882782, 20000000
        ],
        'Actual_2022': [
            2587338338, 1257284226, 861692875, 223959932, 231008360,
            13392945, -39531402, -90224420, 153071264, 0
        ]
    })
    
    # Calculate variances
    financial_performance['Variance_2023'] = (
        financial_performance['Actual_2023'] - financial_performance['Revised_Budget_2023']
    )
    financial_performance['Variance_Pct_2023'] = (
        financial_performance['Variance_2023'] / financial_performance['Revised_Budget_2023']
    ) * 100
    financial_performance['YoY_Growth'] = (
        financial_performance['Actual_2023'] - financial_performance['Actual_2022']
    )
    financial_performance['YoY_Growth_Pct'] = (
        financial_performance['YoY_Growth'] / financial_performance['Actual_2022'].abs()
    ) * 100
    
    # Expenditure Data
    expenditure_data = pd.DataFrame({
        'Category': [
            'Payroll and Employee Benefits', 'Goods and Services', 'Depreciation',
            'Bad Debt Expense', 'Retiring Benefits and Allowances',
            'Grants and Other Current Transfers', 'Other Statutory Expenditure',
            'Capital Transfers', 'Debt Service'
        ],
        'Revised_Budget_2023': [
            915064501, 655380977, 54000000, 989555, 387655291,
            675353637, 1970000, 281518344, 691711905
        ],
        'Actual_2023': [
            863924381, 545212668, 49626566, 68281611, 333644842,
            910661649, 4554557, 241950953, 568277615
        ],
        'Actual_2022': [
            828005895, 653615712, 43277406, 9880606, 340245554,
            831432691, 7489232, 268894435, 391453035
        ]
    })
    
    # Calculate expenditure variances
    expenditure_data['Variance_2023'] = (
        expenditure_data['Actual_2023'] - expenditure_data['Revised_Budget_2023']
    )
    expenditure_data['Variance_Pct_2023'] = (
        expenditure_data['Variance_2023'] / expenditure_data['Revised_Budget_2023']
    ) * 100
    
    # Statement of Financial Position Data
    balance_sheet = pd.DataFrame({
        'Category': [
            'Current Assets', 'Financial Assets', 'Cash on Hand', 'Bank',
            'Tax Receivables (Net)', 'Other Receivables (Net)', 'Restricted cash',
            'Non-Current Assets', 'Financial Assets', 'Sinking Fund Assets',
            'Investments', 'Non Financial Assets', 'Land', 'Other capital assets (Net)'
        ],
        'Actual_Mar_23': [
            3735288225, 3734618402, 152830846, 759489160, 2428696065,
            254774883, 138827448, 4337385833, 609280459, 60998391,
            529021234, 3728105374, 1445313783, 2282791591
        ],
        'Actual_Mar_22': [
            3476483879, 3475932368, 101071094, 620329896, 2384625679,
            231248217, 138657482, 4077323452, 439248332, 30094107,
            381209361, 3638075120, 1443906209, 2194168911
        ]
    })
    
    # Liabilities Data
    liabilities_data = pd.DataFrame({
        'Category': [
            'Current Liabilities', 'Overdraft Facility', 'Accounts Payable',
            'Refunds Payable', 'Pension Liability', 'Deposits', 'Treasury Bills',
            'Current Portion of Long term debt', 'Long-term Liabilities',
            'Government Securities', 'Other Local Debt',
            'Loans from International Financial Institutions',
            'Loans from Other Governments', 'Other Foreign Debt'
        ],
        'Actual_Mar_23': [
            2131488223, 167110481, 82010933, 530063724, 5573965, 170086214,
            495103750, 661885235, 12799271087, 8572467834, 101315000,
            3194580072, 376309795, 416416319
        ],
        'Actual_Mar_22': [
            1877339098, 214985000, 33894156, 522864905, 5382182, 163215273,
            495103750, 408361016, 12306018215, 8781379378, 101315000,
            2795720352, 312635489, 178010652
        ]
    })
    
    # Adverse Opinion Details
    adverse_opinion_items = [
        {
            'Issue': 'Other Capital Assets Discrepancy',
            'Amount': 719000000,
            'Description': 'Difference of $719 million between amounts reported vs subsidiary records',
            'Impact': 'Overstated Assets',
            'Severity': 'High'
        },
        {
            'Issue': 'Cash Overstatement',
            'Amount': 115000000,
            'Description': 'Cash overstated by $115 million',
            'Impact': 'Overstated Current Assets',
            'Severity': 'High'
        },
        {
            'Issue': 'Financial Investments Overstatement',
            'Amount': 147000000,
            'Description': 'Financial investments overstated by $147 million',
            'Impact': 'Overstated Investments',
            'Severity': 'High'
        },
        {
            'Issue': 'Pension Liabilities Omitted',
            'Amount': 'Not Quantified',
            'Description': 'Pension and employee benefits liability not included',
            'Impact': 'Understated Liabilities',
            'Severity': 'Critical'
        },
        {
            'Issue': 'Tax Receivables Unverified',
            'Amount': 2430000000,
            'Description': '$2.43 billion tax receivables could not be confirmed',
            'Impact': 'Overstated Receivables',
            'Severity': 'Critical'
        },
        {
            'Issue': 'Bad Debt Expenses Unverified',
            'Amount': 68280000,
            'Description': '$68.28 million bad debt expenses could not be confirmed',
            'Impact': 'Potential Overstated Expenses',
            'Severity': 'Medium'
        },
        {
            'Issue': 'Non-Consolidation of SOEs',
            'Amount': 'Not Quantified',
            'Description': 'State-owned entities not consolidated as required by IPSAS',
            'Impact': 'Incomplete Financial Statements',
            'Severity': 'Critical'
        }
    ]
    
    # Tax Revenue Breakdown
    tax_revenue_details = pd.DataFrame({
        'Tax_Type': [
            'Income and Profits - Individuals', 'Income and Profits - Corporation',
            'Withholding Tax', 'VAT (Net)', 'Excise Duty', 'Highway Revenue',
            'Other Goods & Services', 'Land Tax (Net)', 'Property Transfer Tax',
            'Import Duties (Net)', 'Stamp Duty'
        ],
        'Actual_2023': [
            545610497, 485674857, 37563935, 1156630063, 251622393,
            16612103, 203213603, 211157762, 29360071, 250253724, 22235902
        ],
        'Actual_2022': [
            429779367, 394168620, 37744944, 874397904, 204941594,
            15628435, 162416302, 203072475, 20887457, 231002875, 13392945
        ],
        'Growth_Amount': [
            115831130, 91506237, -181009, 282232159, 46680799,
            983668, 40797301, 8085287, 8472614, 19250849, 8842957
        ],
        'Growth_Pct': [
            26.95, 23.22, -0.48, 32.28, 22.78, 6.29,
            25.13, 3.98, 40.58, 8.33, 66.04
        ]
    })
    
    # Debt Structure
    debt_structure = pd.DataFrame({
        'Debt_Type': [
            'Local Loans Act', 'External Loans Act', 'Caribbean Development Bank',
            'Inter American Development Bank', 'Special Loans Act', 'Treasury Bills',
            'Savings Bond Act', 'International Monetary Fund',
            'Latin American Development Bank', 'Ways & Means (Overdraft)'
        ],
        'Amount_2023': [
            7745270000, 1061170000, 483540000, 1814760000, 890940000,
            495100000, 32230000, 548410000, 357430000, 167150000
        ],
        'Amount_2022': [
            7871410000, 1061170000, 469380000, 1499660000, 810080000,
            495100000, 47290000, 464770000, 340600000, 214990000
        ],
        'Change': [
            -126140000, 0, 14160000, 315100000, 80860000,
            0, -15060000, 83640000, 16830000, -47840000
        ]
    })
    
    # State-Owned Enterprise Transfers
    soe_transfers = pd.DataFrame({
        'Entity': [
            'Queen Elizabeth Hospital', 'Barbados Defence Force', 'Transport Board',
            'National Housing Corporation', 'Barbados Agricultural Management',
            'Sanitation Service Authority', 'Barbados Tourism Investment',
            'National Sports Council', 'Barbados Investment and Development Corp',
            'Urban Development Commission'
        ],
        'Current_Transfers': [
            133664857.68, 69932639.00, 46023613.00, 16851610.11, 38984952.00,
            4452630.00, 3516575.00, 16443141.43, 9852282.00, 5370098.22
        ],
        'Capital_Transfers': [
            8800000.00, 1547900.00, 750000.00, 29450000.00, 5000000.00,
            6000000.00, 91200000.00, 19919939.00, 8387000.00, 10716031.00
        ],
        'Total': [
            142464857.68, 71480539.00, 46773613.00, 46301610.11, 43984952.00,
            10452630.00, 94716575.00, 36363080.43, 18219282.00, 15086129.22
        ]
    })
    
    return {
        'financial_performance': financial_performance,
        'expenditure_data': expenditure_data,
        'balance_sheet': balance_sheet,
        'liabilities_data': liabilities_data,
        'adverse_opinion_items': pd.DataFrame(adverse_opinion_items),
        'tax_revenue_details': tax_revenue_details,
        'debt_structure': debt_structure,
        'soe_transfers': soe_transfers
    }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def calculate_key_metrics():
    """
    Calculate key financial metrics from the loaded data.
    
    Returns:
        dict: Dictionary of key financial metrics
    """
    # Total Revenue
    total_revenue_2023 = financial_data['financial_performance']['Actual_2023'].sum()
    total_revenue_2022 = financial_data['financial_performance']['Actual_2022'].sum()
    revenue_growth = total_revenue_2023 - total_revenue_2022
    revenue_growth_pct = (revenue_growth / total_revenue_2022) * 100 if total_revenue_2022 != 0 else 0
    
    # Total Expenditure
    total_expenditure_2023 = financial_data['expenditure_data']['Actual_2023'].sum()
    total_expenditure_2022 = financial_data['expenditure_data']['Actual_2022'].sum()
    
    # Deficit/Surplus
    deficit_2023 = total_revenue_2023 - total_expenditure_2023
    deficit_2022 = total_revenue_2022 - total_expenditure_2022
    
    # Total Assets
    total_assets_2023 = (
        financial_data['balance_sheet']['Actual_Mar_23'].iloc[0] + 
        financial_data['balance_sheet']['Actual_Mar_23'].iloc[7]
    )
    total_assets_2022 = (
        financial_data['balance_sheet']['Actual_Mar_22'].iloc[0] + 
        financial_data['balance_sheet']['Actual_Mar_22'].iloc[7]
    )
    
    # Total Liabilities
    total_liabilities_2023 = (
        financial_data['liabilities_data']['Actual_Mar_23'].iloc[0] + 
        financial_data['liabilities_data']['Actual_Mar_23'].iloc[8]
    )
    total_liabilities_2022 = (
        financial_data['liabilities_data']['Actual_Mar_22'].iloc[0] + 
        financial_data['liabilities_data']['Actual_Mar_22'].iloc[8]
    )
    
    # Net Debt
    net_debt_2023 = total_liabilities_2023 - (
        financial_data['balance_sheet']['Actual_Mar_23'].iloc[0] + 
        financial_data['balance_sheet']['Actual_Mar_23'].iloc[1]
    )
    net_debt_2022 = total_liabilities_2022 - (
        financial_data['balance_sheet']['Actual_Mar_22'].iloc[0] + 
        financial_data['balance_sheet']['Actual_Mar_22'].iloc[1]
    )
    
    # Tax Receivables (Major Issue)
    tax_receivables_2023 = financial_data['balance_sheet'][
        financial_data['balance_sheet']['Category'] == 'Tax Receivables (Net)'
    ]['Actual_Mar_23'].values[0]
    tax_receivables_2022 = financial_data['balance_sheet'][
        financial_data['balance_sheet']['Category'] == 'Tax Receivables (Net)'
    ]['Actual_Mar_22'].values[0]
    
    return {
        'total_revenue_2023': total_revenue_2023,
        'total_revenue_2022': total_revenue_2022,
        'revenue_growth': revenue_growth,
        'revenue_growth_pct': revenue_growth_pct,
        'total_expenditure_2023': total_expenditure_2023,
        'total_expenditure_2022': total_expenditure_2022,
        'deficit_2023': deficit_2023,
        'deficit_2022': deficit_2022,
        'total_assets_2023': total_assets_2023,
        'total_assets_2022': total_assets_2022,
        'total_liabilities_2023': total_liabilities_2023,
        'total_liabilities_2022': total_liabilities_2022,
        'net_debt_2023': net_debt_2023,
        'net_debt_2022': net_debt_2022,
        'tax_receivables_2023': tax_receivables_2023,
        'tax_receivables_2022': tax_receivables_2022
    }

# ============================================================================
# DATA INITIALIZATION
# ============================================================================
financial_data = load_financial_data()
metrics = calculate_key_metrics()

# ============================================================================
# HEADER SECTION
# ============================================================================
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(
        '<div class="main-header">Barbados Government Financial Statements 2023</div>',
        unsafe_allow_html=True
    )
    st.markdown("**Audited Financial Statements for Year Ended March 31, 2023 • Adverse Audit Opinion Issued**")
    st.caption("Prepared by Accountant General • Audited by Auditor General of Barbados")

with col2:
    st.markdown("""
    <div class="flag-container">
        <div style="font-size: 4rem; line-height: 1; margin-bottom: 10px;">🇧🇧</div>
        <div style="font-weight: bold; color: #00267F; font-size: 1.3rem;">Government of Barbados</div>
        <div style="font-size: 0.9rem; color: #666; font-weight: bold;">Financial Statements</div>
        <div style="font-size: 0.7rem; color: #999; margin-top: 5px;">Year Ended March 31, 2023</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.caption(f"**Report Date:** {datetime.now().strftime('%B %d, %Y')}")
    st.caption(f"**Financial Year:** April 1, 2022 - March 31, 2023")
    st.caption("**Audit Opinion:** ❌ Adverse")
    st.caption("**Dashboard Version:** 2.0")

st.markdown("---")

# ============================================================================
# SIDEBAR - FILTERS & PERFORMANCE HIGHLIGHTS
# ============================================================================
with st.sidebar:
    st.header("📊 Financial Analysis Filters")
    
    # Display Options
    st.subheader("Display Options")
    view_option = st.selectbox(
        "Select View",
        [
            "Executive Summary", "Revenue Analysis", "Expenditure Analysis",
            "Balance Sheet", "Audit Findings", "Debt Analysis", 
            "SOE Transfers", "Performance Highlights"
        ]
    )
    
    # Currency Format
    st.subheader("Currency Format")
    currency_format = st.selectbox(
        "Display values as",
        ["Millions (BBD $M)", "Billions (BBD $B)", "Full Amount (BBD $)"]
    )
    
    # Comparative Period
    st.subheader("Comparative Period")
    show_comparative = st.checkbox("Show 2022 Comparison", value=True)
    
    st.markdown("---")
    
    # Performance Highlights in Sidebar
    st.subheader("📈 Performance Highlights")
    
    # Revenue Growth
    st.markdown(f"""
    <div class="financial-card">
        <div class="financial-label">Revenue Growth:</div>
        <div class="financial-value">${metrics['revenue_growth']/1e6:,.0f}M</div>
        <div>{metrics['revenue_growth_pct']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tax Collection
    tax_collection = financial_data['financial_performance'].loc[0, 'Actual_2023']
    st.markdown(f"""
    <div class="financial-card">
        <div class="financial-label">Tax Collection:</div>
        <div class="financial-value">${tax_collection/1e9:,.2f}B</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Debt Service
    debt_service = financial_data['expenditure_data'].loc[8, 'Actual_2023']
    st.markdown(f"""
    <div class="financial-card">
        <div class="financial-label">Debt Service:</div>
        <div class="financial-value">${debt_service/1e6:,.0f}M</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Capital Transfers
    capital_transfers = financial_data['expenditure_data'].loc[7, 'Actual_2023']
    st.markdown(f"""
    <div class="financial-card">
        <div class="financial-label">Capital Transfers:</div>
        <div class="financial-value">${capital_transfers/1e6:,.0f}M</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data Source
    st.markdown("**Data Source:**")
    st.caption("Auditor General's Report on Financial Statements")
    st.caption("Government of Barbados")
    st.caption("Financial Year 2022-2023")

# ============================================================================
# QUICK STATS OVERVIEW
# ============================================================================
st.markdown("### 📈 Financial Overview")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    # Total Revenue
    if currency_format == "Millions (BBD $M)":
        value = f"${metrics['total_revenue_2023']/1e6:,.1f}M"
    elif currency_format == "Billions (BBD $B)":
        value = f"${metrics['total_revenue_2023']/1e9:,.2f}B"
    else:
        value = f"${metrics['total_revenue_2023']:,.0f}"
    
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value">{value}</div>
        <div class="quick-stats-label">Total Revenue 2023</div>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    # Deficit/Surplus
    deficit_color = "#DC2626" if metrics['deficit_2023'] < 0 else "#10B981"
    
    if currency_format == "Millions (BBD $M)":
        deficit_value = f"${abs(metrics['deficit_2023'])/1e6:,.1f}M"
    elif currency_format == "Billions (BBD $B)":
        deficit_value = f"${abs(metrics['deficit_2023'])/1e9:,.2f}B"
    else:
        deficit_value = f"${abs(metrics['deficit_2023']):,.0f}"
    
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value" style="color: {deficit_color}">
            {deficit_value}
        </div>
        <div class="quick-stats-label">{"Deficit" if metrics['deficit_2023'] < 0 else "Surplus"} 2023</div>
    </div>
    """, unsafe_allow_html=True)

with col_s3:
    # Total Liabilities
    if currency_format in ["Billions (BBD $B)", "Millions (BBD $M)"]:
        debt_value = f"${metrics['total_liabilities_2023']/1e9:,.2f}B"
    else:
        debt_value = f"${metrics['total_liabilities_2023']:,.0f}"
    
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value" style="color: #DC2626;">{debt_value}</div>
        <div class="quick-stats-label">Total Liabilities</div>
    </div>
    """, unsafe_allow_html=True)

with col_s4:
    # Audit Issues Count
    st.markdown(f"""
    <div class="quick-stats-box">
        <div class="quick-stats-value">{len(financial_data['adverse_opinion_items'])}</div>
        <div class="quick-stats-label">Audit Issues</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# VIEW SELECTION
# ============================================================================

if view_option == "Executive Summary":
    # Executive Summary View
    st.markdown('<div class="sub-header">Executive Summary - Adverse Audit Opinion</div>', unsafe_allow_html=True)
    
    # Warning about Adverse Opinion
    with st.container():
        st.markdown("""
        <div class="financial-card adverse-opinion">
            <h3 style="color: #DC2626; margin-top: 0;">⚠️ ADVERSE AUDIT OPINION ISSUED</h3>
            <p><strong>Auditor General's Conclusion:</strong> The accompanying financial statements do <strong>NOT</strong> give a true and fair view of the financial position of the Government of Barbados as at March 31, 2023.</p>
            <p><strong>Reason:</strong> Significant material misstatements and non-compliance with International Public Sector Accounting Standards (IPSAS).</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Financial Metrics
    st.markdown('<div class="section-header">Key Financial Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if metrics['total_revenue_2023'] >= 1e9:
            revenue_value = f"${metrics['total_revenue_2023']/1e9:,.2f}B"
        else:
            revenue_value = f"${metrics['total_revenue_2023']/1e6:,.1f}M"
        st.metric(
            "Total Revenue", 
            revenue_value, 
            f"{metrics['revenue_growth_pct']:.1f}% vs 2022",
            help="Total government revenue for financial year 2022-2023"
        )
    
    with col2:
        expenditure_value = f"${metrics['total_expenditure_2023']/1e9:,.2f}B"
        st.metric(
            "Total Expenditure", 
            expenditure_value,
            f"${(metrics['total_expenditure_2023'] - metrics['total_expenditure_2022'])/1e9:,.2f}B",
            help="Total government expenditure for financial year 2022-2023"
        )
    
    with col3:
        deficit_color = "inverse" if metrics['deficit_2023'] < 0 else "normal"
        deficit_value = f"${abs(metrics['deficit_2023'])/1e9:,.2f}B"
        st.metric(
            "Consolidated Fund Deficit",
            deficit_value,
            f"${(abs(metrics['deficit_2023']) - abs(metrics['deficit_2022']))/1e9:+.2f}B",
            delta_color=deficit_color,
            help="Deficit after including annex operations"
        )
    
    with col4:
        debt_value = f"${metrics['total_liabilities_2023']/1e9:,.2f}B"
        debt_growth = (
            (metrics['total_liabilities_2023'] - metrics['total_liabilities_2022']) / 
            metrics['total_liabilities_2022']
        ) * 100 if metrics['total_liabilities_2022'] != 0 else 0
        st.metric(
            "Total Public Debt",
            debt_value,
            f"{debt_growth:.1f}%",
            delta_color="inverse",
            help="Total government liabilities as at March 31, 2023"
        )
    
    # Revenue vs Expenditure Chart
    st.markdown('<div class="section-header">Revenue vs Expenditure Trend</div>', unsafe_allow_html=True)
    
    trend_data = pd.DataFrame({
        'Year': ['2022', '2023'],
        'Revenue': [metrics['total_revenue_2022'], metrics['total_revenue_2023']],
        'Expenditure': [metrics['total_expenditure_2022'], metrics['total_expenditure_2023']],
        'Deficit': [abs(metrics['deficit_2022']), abs(metrics['deficit_2023'])]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Revenue',
        x=trend_data['Year'],
        y=trend_data['Revenue'],
        marker_color='#00267F',
        text=[f'${x/1e9:.2f}B' for x in trend_data['Revenue']],
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        name='Expenditure',
        x=trend_data['Year'],
        y=trend_data['Expenditure'],
        marker_color='#DC2626',
        text=[f'${x/1e9:.2f}B' for x in trend_data['Expenditure']],
        textposition='auto'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Revenue vs Expenditure Comparison (2022-2023)',
        yaxis_title='Amount (BBD $)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Critical Audit Findings
    st.markdown('<div class="section-header">Critical Audit Findings Requiring Immediate Attention</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Asset Management Issues
        st.markdown("""
        <div class="financial-card qualified-item">
            <h4 style="color: #D97706; margin-top: 0;">🏛️ Asset Management Issues</h4>
            <p><strong>$719M Discrepancy</strong> in Other Capital Assets</p>
            <p><strong>$115M Cash Overstatement</strong> in Treasury accounts</p>
            <p><strong>$147M Investments Overstatement</strong></p>
            <p><strong>Fixed Asset Register</strong> not reconciled</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Revenue Recognition Issues
        st.markdown("""
        <div class="financial-card material-misstatement">
            <h4 style="color: #1D4ED8; margin-top: 0;">💰 Revenue Recognition Issues</h4>
            <p><strong>$2.43B Tax Receivables</strong> unverified</p>
            <p><strong>$68.3M Bad Debt Expense</strong> not confirmed</p>
            <p><strong>Historical cost issues</strong> with asset valuation</p>
            <p><strong>Measurement uncertainty</strong> in tax accruals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Financial Reporting Failures
        st.markdown("""
        <div class="financial-card adverse-opinion">
            <h4 style="color: #DC2626; margin-top: 0;">📊 Financial Reporting Failures</h4>
            <p><strong>State-Owned Entities NOT consolidated</strong> (IPSAS violation)</p>
            <p><strong>Pension liabilities OMITTED</strong> from balance sheet</p>
            <p><strong>No consolidated financial statements</strong></p>
            <p><strong>15+ year bank reconciliation backlog</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance Highlights
        st.markdown(f"""
        <div class="financial-card">
            <h4 style="color: #00267F; margin-top: 0;">📈 Performance Highlights</h4>
            <p><strong>Revenue Growth:</strong> ${metrics['revenue_growth']/1e6:,.0f}M (+{metrics['revenue_growth_pct']:.1f}%)</p>
            <p><strong>Tax Collection:</strong> ${financial_data['financial_performance'].loc[0, 'Actual_2023']/1e9:,.2f}B</p>
            <p><strong>Debt Service:</strong> ${financial_data['expenditure_data'].loc[8, 'Actual_2023']/1e6:,.0f}M</p>
            <p><strong>Capital Transfers:</strong> ${financial_data['expenditure_data'].loc[7, 'Actual_2023']/1e6:,.0f}M</p>
        </div>
        """, unsafe_allow_html=True)

elif view_option == "Revenue Analysis":
    # Revenue Analysis View
    st.markdown('<div class="sub-header">Revenue Analysis & Tax Performance</div>', unsafe_allow_html=True)
    
    # Revenue Composition
    st.markdown('<div class="section-header">Revenue Composition 2023</div>', unsafe_allow_html=True)
    
    revenue_composition = financial_data['financial_performance'].copy()
    fig = px.pie(
        revenue_composition, 
        values='Actual_2023', 
        names='Category',
        title='Revenue Composition by Source (2023)',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # Tax Revenue Details
    st.markdown('<div class="section-header">Tax Revenue Performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 Tax Revenue Sources
        top_taxes = financial_data['tax_revenue_details'].nlargest(5, 'Actual_2023')
        fig = px.bar(
            top_taxes, 
            x='Tax_Type', 
            y='Actual_2023', 
            title='Top 5 Tax Revenue Sources (2023)',
            color='Growth_Pct', 
            color_continuous_scale='Blues',
            text=[f'${x/1e6:.0f}M' for x in top_taxes['Actual_2023']]
        )
        fig.update_layout(yaxis_title='Amount (BBD $)', xaxis_title='Tax Type')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tax Revenue Growth
        fig = px.bar(
            financial_data['tax_revenue_details'], 
            x='Tax_Type', 
            y='Growth_Pct', 
            title='Tax Revenue Growth (2022 to 2023)',
            color='Growth_Pct', 
            color_continuous_scale='RdYlGn',
            text=[f'{x:.1f}%' for x in financial_data['tax_revenue_details']['Growth_Pct']]
        )
        fig.update_layout(yaxis_title='Growth Percentage (%)', xaxis_title='Tax Type')
        st.plotly_chart(fig, use_container_width=True)
    
    # Revenue Performance Table
    st.markdown('<div class="section-header">Revenue Performance Details</div>', unsafe_allow_html=True)
    
    display_df = financial_data['financial_performance'][[
        'Category', 'Revised_Budget_2023', 'Actual_2023', 
        'Variance_2023', 'Variance_Pct_2023'
    ]].copy()
    
    # Format the DataFrame
    display_df['Revised_Budget_2023'] = display_df['Revised_Budget_2023'].apply(lambda x: f"${x/1e6:,.1f}M")
    display_df['Actual_2023'] = display_df['Actual_2023'].apply(lambda x: f"${x/1e6:,.1f}M")
    display_df['Variance_2023'] = display_df['Variance_2023'].apply(lambda x: f"${x/1e6:+,.1f}M")
    display_df['Variance_Pct_2023'] = display_df['Variance_Pct_2023'].apply(lambda x: f"{x:+.1f}%")
    
    display_df.columns = [
        'Revenue Category', 'Revised Budget', 'Actual 2023', 
        'Variance', 'Variance %'
    ]
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Tax Receivables Issue
    st.markdown('<div class="section-header">⚠️ Critical Issue: Unverified Tax Receivables</div>', unsafe_allow_html=True)
    
    st.warning(f"""
    **$2.43 Billion Tax Receivables Could Not Be Verified**
    
    - **Amount Unverified:** ${metrics['tax_receivables_2023']/1e9:,.2f}B (as at March 31, 2023)
    - **Year-over-Year Change:** ${(metrics['tax_receivables_2023'] - metrics['tax_receivables_2022'])/1e6:,.0f}M
    - **Percentage of Total Assets:** {(metrics['tax_receivables_2023']/metrics['total_assets_2023']*100):.1f}%
    
    **Auditor's Note:** "Tax Receivables of $2.43 billion... could not be confirmed because of the absence of sufficient supporting documentation."
    """)

elif view_option == "Expenditure Analysis":
    # Expenditure Analysis View
    st.markdown('<div class="sub-header">Government Expenditure Analysis</div>', unsafe_allow_html=True)
    
    # Expenditure Composition
    st.markdown('<div class="section-header">Expenditure Composition 2023</div>', unsafe_allow_html=True)
    
    expenditure_composition = financial_data['expenditure_data'].copy()
    fig = px.pie(
        expenditure_composition, 
        values='Actual_2023', 
        names='Category',
        title='Expenditure Composition by Category (2023)',
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # Major Expenditure Categories
    st.markdown('<div class="section-header">Major Expenditure Categories</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Personnel Costs
        personnel_costs = expenditure_composition[
            expenditure_composition['Category'].isin([
                'Payroll and Employee Benefits', 
                'Retiring Benefits and Allowances'
            ])
        ]
        total_personnel = personnel_costs['Actual_2023'].sum()
        
        st.markdown(f"""
        <div class="financial-card">
            <h4 style="color: #00267F; margin-top: 0;">👥 Personnel Costs</h4>
            <div class="financial-value">${total_personnel/1e6:,.0f}M</div>
            <div class="financial-label">Total Payroll & Benefits</div>
            <p><strong>Payroll:</strong> ${personnel_costs.iloc[0]['Actual_2023']/1e6:,.0f}M</p>
            <p><strong>Retiring Benefits:</strong> ${personnel_costs.iloc[1]['Actual_2023']/1e6:,.0f}M</p>
            <p><strong>% of Total Expenditure:</strong> {(total_personnel/metrics['total_expenditure_2023']*100):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Grants and Transfers
        grants = expenditure_composition[
            expenditure_composition['Category'] == 'Grants and Other Current Transfers'
        ]
        
        capital_transfers = expenditure_composition[
            expenditure_composition['Category'] == 'Capital Transfers'
        ]
        
        st.markdown(f"""
        <div class="financial-card">
            <h4 style="color: #00267F; margin-top: 0;">🏛️ Grants & Transfers</h4>
            <div class="financial-value">${grants.iloc[0]['Actual_2023']/1e6:,.0f}M</div>
            <div class="financial-label">Current Transfers</div>
            <p><strong>Capital Transfers:</strong> ${capital_transfers.iloc[0]['Actual_2023']/1e6:,.0f}M</p>
            <p><strong>Total Transfers:</strong> ${(grants.iloc[0]['Actual_2023'] + capital_transfers.iloc[0]['Actual_2023'])/1e6:,.0f}M</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Debt Service
        debt_service = expenditure_composition[
            expenditure_composition['Category'] == 'Debt Service'
        ]
        
        st.markdown(f"""
        <div class="financial-card">
            <h4 style="color: #DC2626; margin-top: 0;">💳 Debt Service</h4>
            <div class="financial-value">${debt_service.iloc[0]['Actual_2023']/1e6:,.0f}M</div>
            <div class="financial-label">Interest & Loan Expenses</div>
            <p><strong>Interest Expense:</strong> ${financial_data['expenditure_data'].iloc[8]['Actual_2023']/1e6:,.0f}M</p>
            <p><strong>% of Revenue:</strong> {(debt_service.iloc[0]['Actual_2023']/metrics['total_revenue_2023']*100):.1f}%</p>
            <p><strong>Year-over-Year:</strong> +${(debt_service.iloc[0]['Actual_2023'] - financial_data['expenditure_data'].iloc[8]['Actual_2022'])/1e6:,.0f}M</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Operating Expenses
        operating = expenditure_composition[
            expenditure_composition['Category'].isin([
                'Goods and Services', 
                'Depreciation', 
                'Bad Debt Expense'
            ])
        ]
        total_operating = operating['Actual_2023'].sum()
        
        st.markdown(f"""
        <div class="financial-card">
            <h4 style="color: #00267F; margin-top: 0;">⚙️ Operating Expenses</h4>
            <div class="financial-value">${total_operating/1e6:,.0f}M</div>
            <div class="financial-label">Goods, Services & Depreciation</div>
            <p><strong>Goods & Services:</strong> ${operating.iloc[0]['Actual_2023']/1e6:,.0f}M</p>
            <p><strong>Depreciation:</strong> ${operating.iloc[1]['Actual_2023']/1e6:,.0f}M</p>
            <p><strong>Bad Debt Expense:</strong> ${operating.iloc[2]['Actual_2023']/1e6:,.0f}M</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Expenditure Performance Table
    st.markdown('<div class="section-header">Expenditure Performance vs Budget</div>', unsafe_allow_html=True)
    
    exp_display_df = financial_data['expenditure_data'][[
        'Category', 'Revised_Budget_2023', 'Actual_2023', 
        'Variance_2023', 'Variance_Pct_2023'
    ]].copy()
    
    # Format the DataFrame
    exp_display_df['Revised_Budget_2023'] = exp_display_df['Revised_Budget_2023'].apply(lambda x: f"${x/1e6:,.1f}M")
    exp_display_df['Actual_2023'] = exp_display_df['Actual_2023'].apply(lambda x: f"${x/1e6:,.1f}M")
    exp_display_df['Variance_2023'] = exp_display_df['Variance_2023'].apply(lambda x: f"${x/1e6:+,.1f}M")
    exp_display_df['Variance_Pct_2023'] = exp_display_df['Variance_Pct_2023'].apply(lambda x: f"{x:+.1f}%")
    
    exp_display_df.columns = [
        'Expenditure Category', 'Revised Budget', 'Actual 2023', 
        'Variance', 'Variance %'
    ]
    
    st.dataframe(exp_display_df, use_container_width=True, height=400)

elif view_option == "Balance Sheet":
    # Balance Sheet View
    st.markdown('<div class="sub-header">Statement of Financial Position Analysis</div>', unsafe_allow_html=True)
    
    # Assets vs Liabilities Overview
    st.markdown('<div class="section-header">Assets vs Liabilities Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Assets", 
            f"${metrics['total_assets_2023']/1e9:,.2f}B", 
            f"${(metrics['total_assets_2023'] - metrics['total_assets_2022'])/1e9:+.2f}B"
        )
    
    with col2:
        st.metric(
            "Total Liabilities", 
            f"${metrics['total_liabilities_2023']/1e9:,.2f}B", 
            f"${(metrics['total_liabilities_2023'] - metrics['total_liabilities_2022'])/1e9:+.2f}B"
        )
    
    with col3:
        net_position = metrics['total_assets_2023'] - metrics['total_liabilities_2023']
        net_position_prev = metrics['total_assets_2022'] - metrics['total_liabilities_2022']
        change = net_position - net_position_prev
        
        st.metric(
            "Net Position", 
            f"${net_position/1e9:,.2f}B", 
            f"${change/1e9:+.2f}B", 
            delta_color="normal" if net_position >= 0 else "inverse"
        )
    
    # Asset Composition
    st.markdown('<div class="section-header">Asset Composition (March 31, 2023)</div>', unsafe_allow_html=True)
    
    asset_data = financial_data['balance_sheet'].copy()
    
    # Group assets
    current_assets = asset_data[asset_data['Category'] == 'Current Assets']['Actual_Mar_23'].values[0]
    non_current_assets = asset_data[asset_data['Category'] == 'Non-Current Assets']['Actual_Mar_23'].values[0]
    
    fig = go.Figure(data=[go.Pie(
        labels=['Current Assets', 'Non-Current Assets'],
        values=[current_assets, non_current_assets],
        hole=.3,
        marker_colors=['#3B82F6', '#1D4ED8']
    )])
    fig.update_layout(title='Asset Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Key Asset Items
    st.markdown('<div class="section-header">Key Asset Items</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        key_assets = asset_data[asset_data['Category'].isin([
            'Cash on Hand', 'Bank', 'Tax Receivables (Net)', 
            'Investments', 'Land'
        ])]
        
        for _, row in key_assets.iterrows():
            value = f"${row['Actual_Mar_23']/1e6:,.0f}M"
            prev_value = f"${row['Actual_Mar_22']/1e6:,.0f}M"
            change = row['Actual_Mar_23'] - row['Actual_Mar_22']
            change_pct = (change / row['Actual_Mar_22']) * 100 if row['Actual_Mar_22'] != 0 else 0
            
            st.markdown(f"""
            <div class="financial-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{row['Category']}</strong><br>
                        <small style="color: #666;">2023: {value} | 2022: {prev_value}</small>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {'#10B981' if change >= 0 else '#DC2626'}; font-weight: bold;">
                            {change/1e6:+.0f}M
                        </div>
                        <small style="color: #666;">{change_pct:+.1f}%</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Liabilities Breakdown
        liabilities = financial_data['liabilities_data']
        key_liabilities = liabilities[liabilities['Category'].isin([
            'Current Liabilities', 'Long-term Liabilities', 
            'Government Securities', 'Loans from International Financial Institutions'
        ])]
        
        for _, row in key_liabilities.iterrows():
            if row['Actual_Mar_23'] >= 1e9:
                value = f"${row['Actual_Mar_23']/1e9:,.2f}B"
                prev_value = f"${row['Actual_Mar_22']/1e9:,.2f}B"
            else:
                value = f"${row['Actual_Mar_23']/1e6:,.0f}M"
                prev_value = f"${row['Actual_Mar_22']/1e6:,.0f}M"
            
            change = row['Actual_Mar_23'] - row['Actual_Mar_22']
            change_pct = (change / row['Actual_Mar_22']) * 100 if row['Actual_Mar_22'] != 0 else 0
            
            st.markdown(f"""
            <div class="financial-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{row['Category']}</strong><br>
                        <small style="color: #666;">2023: {value} | 2022: {prev_value}</small>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {'#DC2626' if change >= 0 else '#10B981'}; font-weight: bold;">
                            {change/1e9:+.2f}B
                        </div>
                        <small style="color: #666;">{change_pct:+.1f}%</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif view_option == "Audit Findings":
    # Audit Findings View
    st.markdown('<div class="sub-header">Audit Findings & Material Misstatements</div>', unsafe_allow_html=True)
    
    # Adverse Opinion Summary
    with st.container():
        st.markdown("""
        <div class="financial-card adverse-opinion">
            <h3 style="color: #DC2626; margin-top: 0;">❌ ADVERSE AUDIT OPINION - KEY FINDINGS</h3>
            <p><strong>Basis for Adverse Opinion (Extract from Auditor General's Report):</strong></p>
            <p>"The total for Other Capital Assets could not be confirmed because of a difference of $719 million between the amounts reported in the financial statements compared with the corresponding figures listed in the subsidiary records. Cash and Financial Investments listed in the financial statements were overstated by $115 million and $147 million respectively. In addition, the liability for pensions and employee benefits were not included in the Statement of Financial Position and the accounts of the State-owned Entities were not consolidated into the financial statements as required by the International Public Sector Accounting Standards (IPSAS). Also, Tax Receivables of $2.43 billion and Bad Debt Expenses of $68.28 million could not be confirmed because of the absence of sufficient supporting documentation."</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Material Misstatements
    st.markdown('<div class="section-header">Material Misstatements Identified</div>', unsafe_allow_html=True)
    
    for _, item in financial_data['adverse_opinion_items'].iterrows():
        severity_color = {
            'Critical': '#DC2626',
            'High': '#F59E0B',
            'Medium': '#3B82F6',
            'Low': '#10B981'
        }.get(item['Severity'], '#666')
        
        if isinstance(item['Amount'], (int, float)):
            amount_display = f"${item['Amount']/1e6:,.0f}M"
        else:
            amount_display = item['Amount']
        
        st.markdown(f"""
        <div class="financial-card" style="border-left-color: {severity_color};">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4 style="margin-top: 0; color: {severity_color};">{item['Issue']}</h4>
                    <p><strong>Amount:</strong> {amount_display}</p>
                    <p><strong>Impact:</strong> {item['Impact']}</p>
                    <p><strong>Description:</strong> {item['Description']}</p>
                </div>
                <div style="background-color: {severity_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">
                    {item['Severity']} Severity
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # IPSAS Compliance Issues
    st.markdown('<div class="section-header">IPSAS Compliance Failures</div>', unsafe_allow_html=True)
    
    ipsas_issues = [
        {
            'Requirement': 'Consolidation of State-Owned Entities',
            'Status': '❌ NOT COMPLIANT',
            'Impact': 'Financial statements incomplete and misleading',
            'Remediation': 'Require full consolidation of all SOEs'
        },
        {
            'Requirement': 'Recognition of Pension Liabilities',
            'Status': '❌ NOT COMPLIANT',
            'Impact': 'Liabilities understated by unquantified amount',
            'Remediation': 'Actuarial valuation and proper accounting'
        },
        {
            'Requirement': 'Asset Valuation and Verification',
            'Status': '⚠️ PARTIALLY COMPLIANT',
            'Impact': 'Assets potentially overstated by $981M+',
            'Remediation': 'Complete asset register reconciliation'
        },
        {
            'Requirement': 'Revenue Recognition (Tax Receivables)',
            'Status': '❌ NOT COMPLIANT',
            'Impact': '$2.43B receivables unverified',
            'Remediation': 'Documentation and verification procedures'
        }
    ]
    
    for issue in ipsas_issues:
        status_color = '#DC2626' if 'NOT' in issue['Status'] else '#F59E0B'
        
        st.markdown(f"""
        <div class="financial-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h5 style="margin-top: 0;">{issue['Requirement']}</h5>
                    <p><strong>Status:</strong> <span style="color: {status_color};">{issue['Status']}</span></p>
                    <p><strong>Impact:</strong> {issue['Impact']}</p>
                    <p><strong>Remediation Required:</strong> {issue['Remediation']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif view_option == "Debt Analysis":
    # Debt Analysis View
    st.markdown('<div class="sub-header">Public Debt Analysis</div>', unsafe_allow_html=True)
    
    # Debt Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        debt_ratio = (metrics['total_liabilities_2023'] / metrics['total_assets_2023']) * 100
        st.metric(
            "Total Public Debt", 
            f"${metrics['total_liabilities_2023']/1e9:,.2f}B", 
            f"{debt_ratio:.1f}% of Assets"
        )
    
    with col2:
        net_debt_change = metrics['net_debt_2023'] - metrics['net_debt_2022']
        st.metric(
            "Net Debt Position", 
            f"${metrics['net_debt_2023']/1e9:,.2f}B", 
            f"${net_debt_change/1e9:+.2f}B"
        )
    
    with col3:
        debt_service_ratio = (
            financial_data['expenditure_data'].loc[8, 'Actual_2023'] / 
            metrics['total_revenue_2023']
        ) * 100
        st.metric(
            "Debt Service to Revenue", 
            f"{debt_service_ratio:.1f}%", 
            f"${financial_data['expenditure_data'].loc[8, 'Actual_2023']/1e6:,.0f}M"
        )
    
    # Debt Structure Visualization
    st.markdown('<div class="section-header">Public Debt Structure</div>', unsafe_allow_html=True)
    
    debt_data = financial_data['debt_structure'].copy()
    fig = px.bar(
        debt_data, 
        x='Debt_Type', 
        y='Amount_2023', 
        title='Public Debt by Type (2023)',
        color='Amount_2023', 
        color_continuous_scale='Reds',
        text=[f'${x/1e9:.2f}B' for x in debt_data['Amount_2023']]
    )
    fig.update_layout(yaxis_title='Amount (BBD $)', xaxis_title='Debt Type')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Debt Composition
    st.markdown('<div class="section-header">Debt Composition Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Domestic vs Foreign Debt
        domestic_debt_types = [
            'Local Loans Act', 'Treasury Bills', 
            'Savings Bond Act', 'Ways & Means (Overdraft)'
        ]
        
        domestic_debt = debt_data[
            debt_data['Debt_Type'].isin(domestic_debt_types)
        ]['Amount_2023'].sum()
        
        foreign_debt = debt_data[
            ~debt_data['Debt_Type'].isin(domestic_debt_types)
        ]['Amount_2023'].sum()
        
        fig = px.pie(
            names=['Domestic Debt', 'Foreign Debt'],
            values=[domestic_debt, foreign_debt],
            title='Domestic vs Foreign Debt',
            color_discrete_sequence=['#00267F', '#FFC726']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Debt Changes
        fig = px.bar(
            debt_data, 
            x='Debt_Type', 
            y='Change', 
            title='Debt Changes (2022 to 2023)',
            color='Change', 
            color_continuous_scale='RdYlGn_r',
            text=[f'${x/1e6:+.0f}M' for x in debt_data['Change']]
        )
        fig.update_layout(yaxis_title='Change (BBD $)', xaxis_title='Debt Type')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Debt Repayment Schedule
    st.markdown('<div class="section-header">Debt Service Analysis</div>', unsafe_allow_html=True)
    
    debt_service = {
        'Category': [
            'Interest Expense - Domestic', 'Interest Expense - Foreign', 
            'Total Interest', 'Expenses of Loans', 'Total Debt Service'
        ],
        'Amount_2023': [372283237, 182429845, 554713083, 13564532, 568277615],
        'Amount_2022': [258748956, 125213222, 383962718, 7490317, 391453035]
    }
    
    debt_service_df = pd.DataFrame(debt_service)
    debt_service_df['Growth'] = debt_service_df['Amount_2023'] - debt_service_df['Amount_2022']
    debt_service_df['Growth_Pct'] = (
        debt_service_df['Growth'] / debt_service_df['Amount_2022']
    ) * 100
    
    for _, row in debt_service_df.iterrows():
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            st.write(f"**{row['Category']}**")
        
        with col2:
            st.write(f"${row['Amount_2023']/1e6:,.0f}M")
        
        with col3:
            growth_color = '#DC2626' if row['Growth'] > 0 else '#10B981'
            st.write(
                f"<span style='color: {growth_color}'>"
                f"{row['Growth']/1e6:+.0f}M ({row['Growth_Pct']:+.1f}%)"
                f"</span>", 
                unsafe_allow_html=True
            )

elif view_option == "SOE Transfers":
    # SOE Transfers View
    st.markdown('<div class="sub-header">State-Owned Enterprise Transfers</div>', unsafe_allow_html=True)
    
    # Total Transfers
    total_transfers = financial_data['soe_transfers']['Total'].sum()
    st.info(
        f"**Total Transfers to State-Owned Entities (2022-2023):** "
        f"${total_transfers/1e6:,.0f}M"
    )
    
    # SOE Transfers Visualization
    st.markdown('<div class="section-header">Top 10 SOE Transfers</div>', unsafe_allow_html=True)
    
    top_soes = financial_data['soe_transfers'].nlargest(10, 'Total')
    fig = px.bar(
        top_soes, 
        x='Entity', 
        y='Total', 
        title='Top 10 State-Owned Enterprise Transfers',
        color='Total', 
        color_continuous_scale='Blues',
        text=[f'${x/1e6:.0f}M' for x in top_soes['Total']]
    )
    fig.update_layout(yaxis_title='Total Transfers (BBD $)', xaxis_title='State-Owned Entity')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Current vs Capital Transfers
    st.markdown('<div class="section-header">Current vs Capital Transfers</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_current = financial_data['soe_transfers']['Current_Transfers'].sum()
        total_capital = financial_data['soe_transfers']['Capital_Transfers'].sum()
        
        fig = px.pie(
            names=['Current Transfers', 'Capital Transfers'],
            values=[total_current, total_capital],
            title='Current vs Capital Transfers',
            color_discrete_sequence=['#3B82F6', '#1D4ED8']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # SOE Transfer Details Table
        display_soes = financial_data['soe_transfers'].copy()
        
        # Format the DataFrame
        display_soes['Current_Transfers'] = display_soes['Current_Transfers'].apply(
            lambda x: f"${x/1e6:,.1f}M"
        )
        display_soes['Capital_Transfers'] = display_soes['Capital_Transfers'].apply(
            lambda x: f"${x/1e6:,.1f}M"
        )
        display_soes['Total'] = display_soes['Total'].apply(
            lambda x: f"${x/1e6:,.1f}M"
        )
        
        display_soes.columns = [
            'State-Owned Entity', 'Current Transfers', 
            'Capital Transfers', 'Total Transfers'
        ]
        
        st.dataframe(display_soes, use_container_width=True, height=400)
    
    # Audit Issue: Non-Consolidation of SOEs
    st.markdown('<div class="section-header">⚠️ Critical Audit Issue: SOE Non-Consolidation</div>', unsafe_allow_html=True)
    
    st.error(f"""
    **IPSAS VIOLATION: State-Owned Entities NOT Consolidated**
    
    **Auditor General's Finding:** "The accounts of the State-owned Entities were not consolidated into the financial statements as required by the International Public Sector Accounting Standards (IPSAS)."
    
    **Impact:**
    - Financial statements are **incomplete and misleading**
    - **${total_transfers/1e6:,.0f}M in transfers** not properly accounted for
    - True financial position of Government **cannot be determined**
    - **Material misstatement** in financial reporting
    
    **Required Action:** Immediate consolidation of all State-Owned Entities into government financial statements.
    """)

elif view_option == "Performance Highlights":
    # Performance Highlights View
    st.markdown('<div class="sub-header">Performance Highlights</div>', unsafe_allow_html=True)
    
    # Performance Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Revenue Growth
        revenue_growth_color = '#10B981' if metrics['revenue_growth'] > 0 else '#DC2626'
        
        st.markdown(f"""
        <div class="financial-card">
            <div class="financial-label">Revenue Growth</div>
            <div class="financial-value">${metrics['revenue_growth']/1e6:,.0f}M</div>
            <div style="color: {revenue_growth_color}; font-weight: bold;">
                {metrics['revenue_growth_pct']:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Tax Collection
        tax_collection = financial_data['financial_performance'].loc[0, 'Actual_2023']
        tax_variance = financial_data['financial_performance'].loc[0, 'Variance_2023']
        
        st.markdown(f"""
        <div class="financial-card">
            <div class="financial-label">Tax Collection</div>
            <div class="financial-value">${tax_collection/1e9:,.2f}B</div>
            <div style="color: #666; font-size: 0.9rem;">
                vs Budget: ${tax_variance/1e6:+.0f}M
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Debt Service
        debt_service = financial_data['expenditure_data'].loc[8, 'Actual_2023']
        debt_service_2022 = financial_data['expenditure_data'].loc[8, 'Actual_2022']
        debt_growth = debt_service - debt_service_2022
        debt_growth_color = '#DC2626' if debt_growth > 0 else '#10B981'
        
        st.markdown(f"""
        <div class="financial-card">
            <div class="financial-label">Debt Service</div>
            <div class="financial-value">${debt_service/1e6:,.0f}M</div>
            <div style="color: {debt_growth_color}; font-weight: bold;">
                {debt_growth/1e6:+.0f}M
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Capital Transfers
        capital_transfers = financial_data['expenditure_data'].loc[7, 'Actual_2023']
        capital_2022 = financial_data['expenditure_data'].loc[7, 'Actual_2022']
        capital_change = capital_transfers - capital_2022
        capital_change_color = '#10B981' if capital_change < 0 else '#DC2626'
        
        st.markdown(f"""
        <div class="financial-card">
            <div class="financial-label">Capital Transfers</div>
            <div class="financial-value">${capital_transfers/1e6:,.0f}M</div>
            <div style="color: {capital_change_color}; font-weight: bold;">
                {capital_change/1e6:+.0f}M
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Performance Table
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    performance_data = [
        {
            'Metric': 'Total Revenue',
            '2023': metrics['total_revenue_2023'],
            '2022': metrics['total_revenue_2022'],
            'Change': metrics['revenue_growth'],
            'Change %': metrics['revenue_growth_pct']
        },
        {
            'Metric': 'Tax Revenue',
            '2023': financial_data['financial_performance'].loc[0, 'Actual_2023'],
            '2022': financial_data['financial_performance'].loc[0, 'Actual_2022'],
            'Change': (
                financial_data['financial_performance'].loc[0, 'Actual_2023'] - 
                financial_data['financial_performance'].loc[0, 'Actual_2022']
            ),
            'Change %': (
                (financial_data['financial_performance'].loc[0, 'Actual_2023'] - 
                 financial_data['financial_performance'].loc[0, 'Actual_2022']) / 
                financial_data['financial_performance'].loc[0, 'Actual_2022']
            ) * 100
        },
        {
            'Metric': 'Total Expenditure',
            '2023': metrics['total_expenditure_2023'],
            '2022': metrics['total_expenditure_2022'],
            'Change': metrics['total_expenditure_2023'] - metrics['total_expenditure_2022'],
            'Change %': (
                (metrics['total_expenditure_2023'] - metrics['total_expenditure_2022']) / 
                metrics['total_expenditure_2022']
            ) * 100
        },
        {
            'Metric': 'Debt Service',
            '2023': financial_data['expenditure_data'].loc[8, 'Actual_2023'],
            '2022': financial_data['expenditure_data'].loc[8, 'Actual_2022'],
            'Change': (
                financial_data['expenditure_data'].loc[8, 'Actual_2023'] - 
                financial_data['expenditure_data'].loc[8, 'Actual_2022']
            ),
            'Change %': (
                (financial_data['expenditure_data'].loc[8, 'Actual_2023'] - 
                 financial_data['expenditure_data'].loc[8, 'Actual_2022']) / 
                financial_data['expenditure_data'].loc[8, 'Actual_2022']
            ) * 100
        },
        {
            'Metric': 'Net Deficit',
            '2023': metrics['deficit_2023'],
            '2022': metrics['deficit_2022'],
            'Change': metrics['deficit_2023'] - metrics['deficit_2022'],
            'Change %': (
                (metrics['deficit_2023'] - metrics['deficit_2022']) / 
                abs(metrics['deficit_2022'])
            ) * 100 if metrics['deficit_2022'] != 0 else 0
        }
    ]
    
    perf_df = pd.DataFrame(performance_data)
    
    # Format the DataFrame for display
    display_perf_df = perf_df.copy()
    display_perf_df['2023'] = display_perf_df['2023'].apply(lambda x: f"${x/1e6:,.1f}M")
    display_perf_df['2022'] = display_perf_df['2022'].apply(lambda x: f"${x/1e6:,.1f}M")
    display_perf_df['Change'] = display_perf_df['Change'].apply(lambda x: f"${x/1e6:+,.1f}M")
    display_perf_df['Change %'] = display_perf_df['Change %'].apply(lambda x: f"{x:+.1f}%")
    
    st.dataframe(display_perf_df, use_container_width=True)
    
    # Performance Trends Visualization
    st.markdown('<div class="section-header">Performance Trends</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    # Add bars for 2022 and 2023
    fig.add_trace(go.Bar(
        name='2022',
        x=perf_df['Metric'],
        y=perf_df['2022'],
        marker_color='#3B82F6',
        text=[f'${x/1e6:.0f}M' for x in perf_df['2022']],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='2023',
        x=perf_df['Metric'],
        y=perf_df['2023'],
        marker_color='#00267F',
        text=[f'${x/1e6:.0f}M' for x in perf_df['2023']],
        textposition='auto'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Key Performance Indicators (2022 vs 2023)',
        yaxis_title='Amount (BBD $)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 20px;">
        <p style="font-weight: bold; color: var(--bb-blue);">Government of Barbados Financial Statements</p>
        <p>Financial Year Ended March 31, 2023 • Audited by Auditor General of Barbados</p>
        <p>📞 Tel: (246) 535-4254 • ✉️ Email: audit@bao.gov.bb</p>
        <p style="margin-top: 20px; font-size: 0.8rem;">
            Data Source: Auditor General's Report on Financial Statements • 
            Dashboard Version 2.0 • Generated: {datetime.now().strftime('%B %d, %Y')}
        </p>
        <p style="font-size: 0.7rem; color: #999;">
            ⚠️ This dashboard highlights material misstatements and adverse audit opinion
        </p>
    </div>
    """, unsafe_allow_html=True)