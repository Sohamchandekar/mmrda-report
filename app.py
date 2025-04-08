from flask import Flask, render_template
import pandas as pd
import os
from plotly.io import to_html



from plotly.io import to_html

from static.functions import *

app = Flask(__name__)





@app.route('/')
def index():
    # Path to the Excel file (relative to the app.py file)
    excel_path = os.path.join('static', 'data', 'repayment_data.xlsx')

    # Calculate total repayment if file exists
    if os.path.exists(excel_path):
        repayment_amount = calculate_total_repayment(excel_path)
        annual_average_amount  = annualAverageRepayment(excel_path)
        peak_year, peak_amount = peakRepaymentPeriod(excel_path)
        repayment_growth_percentage = averageYoYRepaymentGrowth(excel_path)



        # GRAPHS
        trend_chart = yearlyRepaymentTrendChart(excel_path)
        trend_chart_html = to_html(trend_chart, full_html= False)

        repayment_heatmap = repaymentHeatmapByMonth(excel_path)
        repayment_heatmap_html = to_html(repayment_heatmap, full_html= False)

        monthly_repayment_chart = monthlyLineChartRepaymentChart(excel_path)
        monthly_repayment_chart_html = to_html(monthly_repayment_chart, full_html = False)

        repayment_fluctuation_bar_chart = repaymentFluctuationChart(excel_path)
        repayment_fluctuation_bar_chart_html = to_html(repayment_fluctuation_bar_chart, full_html= False)

        ##########################################################################

        risk_table = riskManagmentTable(excel_path)
        risk_table_html = risk_table.to_html(index=False, classes='table table-bordered', float_format='%.2f')

        long_term_risk = longTermRiskProfileChart(excel_path)
        long_term_risk_html = to_html(long_term_risk, full_html= False)



    else:
        formatted_total = "₹0.00 Crore (Excel file not found)"
        print(f"Warning: Excel file not found at {excel_path}")

    # Render the template with the calculated value
    return render_template('index.html',
                           total_repayment=repayment_amount,
                           annual_average_amount = annual_average_amount,
                           peak_year = peak_year, peak_amount=peak_amount,
                           repayment_growth_percentage = repayment_growth_percentage,

                           trend_chart_html = trend_chart_html,
                           repayment_heatmap_html = repayment_heatmap_html,

                           monthly_repayment_chart_html = monthly_repayment_chart_html,
                           repayment_fluctuation_bar_chart_html = repayment_fluctuation_bar_chart_html,

                           risk_table_html = risk_table_html,
                           long_term_risk_html = long_term_risk_html)


if __name__ == '__main__':
    # Create folders if they don't exist
    os.makedirs(os.path.join('static', 'data'), exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    # Run the Flask app
    app.run(debug=True)