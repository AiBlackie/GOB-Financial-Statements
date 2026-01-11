Barbados Government Financial Statements Dashboard
https://img.shields.io/badge/Country-Barbados-blue?style=for-the-badge
https://img.shields.io/badge/Built%2520with-Streamlit-FF4B4B?style=for-the-badge
https://img.shields.io/badge/Python-3.8%252B-blue?style=for-the-badge
https://img.shields.io/badge/License-MIT-green?style=for-the-badge

📊 Overview
An interactive dashboard for analyzing the Barbados Government Financial Statements for the year ended March 31, 2023. This dashboard highlights the adverse audit opinion issued by the Auditor General and provides comprehensive financial analysis with interactive visualizations.

👥 Credits
Created by: Matthew Blackman
AI Assistant: DeepSeek AI by DeepSeek Company
Data Source: Auditor General's Report on Financial Statements, Government of Barbados

This dashboard was developed collaboratively with AI assistance from DeepSeek. The code structure, financial analysis logic, and interactive visualizations were created with the support of DeepSeek's AI capabilities, while the project direction, Barbados-specific financial insights, and implementation were led by Matthew Blackman.

🚀 Features
📈 Dashboard Sections
Executive Summary
· Adverse audit opinion warning and key findings
· High-level financial metrics
· Revenue vs Expenditure comparison
· Critical audit findings summary

Revenue Analysis
· Revenue composition by source
· Tax revenue performance breakdown
· Revenue variance analysis vs budget
· $2.43B tax receivables issue highlighted

Expenditure Analysis
· Expenditure composition visualization
· Major expense categories (personnel, debt service, grants)
· Budget vs actual performance analysis
· Debt service cost breakdown

Balance Sheet Analysis
· Assets vs liabilities overview
· Asset composition (current vs non-current)
· Key balance sheet items with year-over-year changes
· Net position calculation

Audit Findings
· Detailed adverse opinion analysis
· Material misstatements with severity ratings
· IPSAS compliance failures
· Remediation requirements

Debt Analysis
· Public debt structure visualization
· Domestic vs foreign debt breakdown
· Debt service costs and trends
· Debt sustainability metrics

SOE Transfers
· State-Owned Enterprise transfer analysis
· Top 10 SOE recipients
· Current vs capital transfers breakdown
· IPSAS consolidation violation highlighted

Performance Highlights
· Key performance indicators dashboard
· Year-over-year performance trends
· Interactive metrics cards
· Performance summary tables

🛠️ Installation
Prerequisites
Python 3.8 or higher

pip package manager

Step 1: Clone or Download
bash
git clone https://github.com/matthewblackman/barbados-financial-dashboard.git
cd barbados-financial-dashboard
Step 2: Install Dependencies
bash
pip install -r requirements.txt
If requirements.txt doesn't exist, install individually:

bash
pip install streamlit pandas plotly numpy
🚀 Quick Start
Running the Dashboard
bash
streamlit run barbados_government_financials_dashboard.py
The dashboard will open in your default browser at http://localhost:8501

Alternative: Run with Custom Port
bash
streamlit run barbados_government_financials_dashboard.py --server.port 8502
📁 Project Structure
text
barbados-financial-dashboard/
├── barbados_government_financials_dashboard.py  # Main dashboard application
├── requirements.txt                             # Python dependencies
├── README.md                                    # This file
├── LICENSE                                      # MIT License
└── .gitignore                                   # Git ignore file
🔧 Configuration
Customizing the Dashboard
Update Financial Data: Modify the load_financial_data() function to load from CSV/Excel files

Change Color Scheme: Update CSS variables in the custom CSS section

Add New Views: Extend the view_option selectbox and add corresponding sections

Data Sources
The dashboard uses financial data from the Auditor General's Report on Financial Statements for Barbados Government Financial Year 2022-2023.

🎯 Key Financial Insights
Critical Issues Highlighted
Adverse Audit Opinion - Financial statements don't present true/fair view

$719M Asset Discrepancy - Capital assets not reconciled

$2.43B Unverified Tax Receivables - Lack of supporting documentation

SOEs Not Consolidated - IPSAS violation

Pension Liabilities Omitted - Liabilities understated

Financial Performance
Total Revenue: $3.48B (2023) vs $2.70B (2022) - +28.9% growth

Total Expenditure: $3.59B (2023) vs $3.37B (2022) - +6.3% growth

Consolidated Fund Deficit: $110.9M (2023) vs $691.4M (2022) - Improvement

Total Public Debt: $14.93B (2023) vs $14.18B (2022) - +5.3% increase

📱 Usage Guide
Sidebar Controls
Select View: Choose from 8 different analysis views

Currency Format: Toggle between Millions, Billions, or full amounts

Comparative Period: Show/hide 2022 comparison data

Quick Stats: View key metrics at a glance

Interactive Features
Hover over charts for detailed values

Click on legend items to show/hide data series

Use dropdowns to filter data

Download charts as PNG images (right-click on charts)

🐛 Troubleshooting
Common Issues
Dashboard won't start

bash
# Check if Streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install --upgrade streamlit
Missing dependencies

bash
# Install all required packages
pip install streamlit pandas plotly numpy
Port already in use

bash
# Kill existing Streamlit processes
pkill -f streamlit

# Or run on different port
streamlit run your_script.py --server.port 8502
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📞 Contact & Support
Created by: Matthew Blackman
AI Assistance: DeepSeek AI
Government Contact: Auditor General's Office, Barbados
Technical Issues: Create an issue on GitHub repository

🙏 Acknowledgments
Primary Developer: Matthew Blackman

AI Assistant: DeepSeek AI by DeepSeek Company

Data Source: Auditor General of Barbados

Inspired by: Government financial transparency initiatives

Built with: Streamlit, Plotly, Pandas

Disclaimer: This dashboard is for analytical purposes only. Always refer to official government publications for authoritative financial information. The data presented is based on the Auditor General's report for the year ended March 31, 2023, and may be subject to updates and corrections.

Last Updated: January 11 2026
Dashboard Version: 2.0
Data Version: FY 2022-2023
Primary Developer: Matthew Blackman
AI Assistant: DeepSeek AI

