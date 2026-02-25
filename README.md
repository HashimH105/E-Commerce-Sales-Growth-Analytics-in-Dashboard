# E-Commerce Sales Growth Analytics Dashboard

**Project Title:** Overall Sales Analysis  
**GitHub:** https://github.com/HashimH105/E-Commerce-Sales-Growth-Analytics-in-Dashboard  
**Tableau Public Dashboard:** [https://public.tableau.com/app/profile/hashim.ebrahim/viz/OverallSalesAnalysisformyProject1withSQLandPython/Dashboard1?publish=yes]

End-to-end sales analytics project built to uncover growth drivers in an e-commerce dataset using the 80/20 rule.  
Pipeline: MySQL database → Python data generation + ETL + analysis (RFM, cohorts, forecasting) → Tableau interactive dashboard.

### Key Features & Insights
- Monthly sales trends with linear forecast  
- Revenue heatmap by Region vs Category  
- Top 10 products driving revenue  
- Summary KPI cards + clean metrics table  
- Action filters (click region/category/product → everything updates)  
- Business recommendations: target high-value regions, categories & customers for 15–25% potential uplift

### Tech Stack
- **Database**: MySQL (schema + generated Revenue column + indexes)  
- **Data Generation & Processing**: Python (pandas, matplotlib, seaborn, scikit-learn)  
  - Script: `sales_analytics.py`  
  - Jupyter Notebook: `Sales Analysis.ipynb` (recommended for interactive execution)  
- **Visualization**: Tableau Public – workbook named **Overall Sales analysis**  
- **Sample Data**: Generated via `generate_data.py` → `transactions_data.csv`

### Project Files
