Sales and Inventory Analysis with Forecasting and Anomaly Detection

Project Overview
This project automates the analysis of sales and inventory data for Khen Enterprises, a fast-growing FMCG distributor. It integrates forecasting, anomaly detection, and visual reporting to drive data-informed decisions.

1.Business Problem
Khen Enterprises relied on manual spreadsheets to track sales performance and stock levels. This resulted in:

1.Delayed restocking of high-demand products
2.Overstocking of slow movers
3.Missed revenue trends
4.Time-consuming and error-prone reporting

3.Solution Summary
Built an automated pipeline and dashboard to:

-Load & clean sales/inventory data (CSV)
-Merge datasets via PRODUCTCODE
=Analyze trends and detect anomalies
=Forecast future sales using Prophet
-Visualize KPIs and insights in Power BI

4.Tools & Technologies
Component	Tool/Library

.Data Handling	pandas
.Date Processing	datetime
.Forecasting	Prophet
.Anomaly Detection	Z-Score (SciPy)
.Visualization	matplotlib, Power BI
.Automation	Python Scripting

5.Key Insights

a)Top Product Lines (by Quantity Sold)
Classic Cars (33,992 units)
Vintage Cars (21,069 units)

b)Monthly Sales Summary
-Highest: Nov 2004 –  1,089,048.01
−𝐿𝑜𝑤𝑒𝑠𝑡:𝐽𝑎𝑛2003–  129,753.60

c)Anomalies Detected
Nov 2003 and Nov 2004 flagged using Z-Score as high outliers.

d)Forecasted Sales (Prophet)
Month	Forecast	Range (95% CI)
Jun 2005	 382,589.80|  347,684.80 –  417,167.90
|𝑂𝑐𝑡2005|  1,205,186.00	1,167,811.00– 1,240,938.00

e)Power BI Dashboard
Interactive dashboard includes:

1.Monthly Sales Trend with Forecast
2.Anomaly Flags
3.Top Product Lines
4.Inventory vs. Sales Chart
5.Average Monthly Sales & KPI Cards
6.Region, ProductLine, and Date Filters



