# E-Commerce Sales Growth Analytics Dashboard

**Project Title:** Overall Sales Analysis  
**GitHub Repository:** https://github.com/HashimH105/E-Commerce-Sales-Growth-Analytics-in-Dashboard  
**Tableau Public Dashboard:** [https://public.tableau.com/app/profile/hashim.ebrahim/viz/OverallSalesAnalysisformyProject1withSQLandPython/Dashboard1?publish=yes]

End-to-end sales analytics project for an e-commerce dataset using the 80/20 rule to uncover key growth drivers.  
The full pipeline includes MySQL storage, Python-based data generation + ETL + analysis (RFM, cohorts, forecasting), and an interactive Tableau dashboard.

### Key Features & Business Insights
- Monthly sales trends with linear 6-month forecast  
- Revenue heatmap by Region vs Category  
- Top 10 products driving the majority of revenue  
- KPI cards + clean summary metrics table  
- Action filters (click any region, category, or product → entire dashboard updates)  
- Actionable recommendations: Target high-value regions/categories/customers for 15–25% potential revenue uplift

### Tech Stack
- **Database**: MySQL (relational schema, generated Revenue column, indexes)  
- **Data Generation & ETL/Analysis**: Python (pandas, matplotlib, seaborn, scikit-learn)  
  - Plain script: `sales_analytics.py`  
  - Jupyter Notebook (recommended): `Sales Analysis.ipynb`  
- **Visualization & BI**: Tableau Public – workbook named **Overall Sales analysis**  
- **Input/Output Files**: CSV-based sample data and exported files for Tableau

### Project Files
├── database.sql                          # MySQL setup (database, table, indexes)
├── generate_data.py                      # Generates sample 1000-row e-commerce transactions
├── sales_analytics.py                    # Full ETL + RFM + cohort + forecast + CSV export
├── Sales Analysis.ipynb                  # Jupyter Notebook version (easier to run/debug)
├── transactions_data.csv                 # Sample input data (created by generate_data.py)
├── full_transactions_for_tableau.csv     # Clean, row-level data – primary file for Tableau
├── analytics_insights.csv                # Aggregated summaries (optional)
├── Overall Sales analysis.twbx           # Tableau workbook file
└── README.md                             # This file


