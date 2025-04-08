import pandas as pd
import plotly.graph_objects as go
import calendar
from datetime import datetime
from plotly.subplots import make_subplots
import math

def calculate_total_repayment(excel_path):
    """
    Calculate the total repayment obligation from Excel data

    Parameters:
    excel_path (str): Path to the Excel file containing repayment data

    Returns:
    float: Total repayment amount in Crore
    """
    try:
        # Read the Excel file
        df = pd.read_excel(excel_path)

        # Identify the value column
        value_column = None
        if 'Total Repayment' in df.columns:
            value_column = 'Total Repayment'
        elif 'value' in df.columns:
            value_column = 'value'
        else:
            # Find the first numeric column
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    value_column = col
                    break

        if value_column is None:
            raise ValueError("Could not find a numeric column in the Excel file")

        # Calculate the total
        total_repayment = df[value_column].sum()

        # Convert to Crore
        repayment_value = round(total_repayment, 2)

        return repayment_value

    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return 0





def annualAverageRepayment(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Convert 'Year' to datetime format
    df['Year'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract the calendar year
    df['Calendar Year'] = df['Year'].dt.year

    # Sum total repayment for each year
    yearly_totals = df.groupby('Calendar Year')['Total Repayment'].sum()

    # Calculate average of the yearly totals
    annual_average = round(yearly_totals.mean(), 2)

    return annual_average


import pandas as pd


def peakRepaymentPeriod(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Convert 'Year' column to datetime
    df['Year'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract calendar year
    df['Calendar Year'] = df['Year'].dt.year

    # Sum total repayment per year
    yearly_totals = df.groupby('Calendar Year')['Total Repayment'].sum()

    # Get the year with the highest repayment
    peak_year = yearly_totals.idxmax()
    peak_amount = round(yearly_totals.max(), 2)

    return peak_year, peak_amount





def averageYoYRepaymentGrowth(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert 'Year' column to datetime
    df['Year'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract calendar year
    df['Calendar Year'] = df['Year'].dt.year

    # Sum total repayment for each calendar year
    yearly_totals = df.groupby('Calendar Year')['Total Repayment'].sum().sort_index()

    # Calculate year-on-year percentage growth
    yoy_growth = yearly_totals.pct_change().dropna() * 100  # in percentage

    # Calculate average YoY growth
    average_growth = round(yoy_growth.mean(), 2)

    return average_growth





def yearlyRepaymentTrendChart(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)

    # Convert to datetime
    df['Year'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract calendar year
    df['Calendar Year'] = df['Year'].dt.year

    # Calculate total repayment per year
    yearly_totals = df.groupby('Calendar Year')['Total Repayment'].sum().sort_index()

    # Plotly figure
    fig = go.Figure()

    # Add trend line
    fig.add_trace(go.Scatter(
        x=yearly_totals.index,
        y=yearly_totals.values,
        mode='lines+markers+text',  # Added 'text' to show numbers on points
        line=dict(color='#1f77b4', width=3.5),
        marker=dict(size=9),
        hovertemplate='Year: %{x}<br>Total Repayment: %{y:.2f}<extra></extra>'
    ))

    # Style the chart
    fig.update_layout(
        height=360,  # Set the height of the figure
        width=1160,   # Set the width of the figure
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=14),
            dtick=1,  # Set the tick interval to 1 year
            tickvals=yearly_totals.index[::3]  # Show every 3rd year on the x-axis
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgrey',
            zeroline=False,
            tickfont=dict(size=14)
        ),
        plot_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background
        margin=dict(l=40, r=40, t=20, b=40)
    )

    return fig

def repaymentHeatmapByMonth(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert to datetime
    df['Date'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract year and month name
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month Name'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

    # Create pivot table: rows = Month, columns = Year, values = repayment
    pivot = df.pivot_table(
        index='Month Name',
        columns='Year',
        values='Total Repayment',
        aggfunc='sum'
    )

    # Ensure month order (Jan–Dec)
    month_order = list(calendar.month_abbr)[1:]
    pivot = pivot.reindex(month_order)

    # Plotly heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.astype(str).str[-2:],  # Format years to last two digits
        y=pivot.index,
        colorscale='Reds',
        hovertemplate='Month: %{y}<br>Year: %{x}<br>Repayment: %{z:.2f}<extra></extra>',
        colorbar=dict(title='Repayment'),
        showscale=True,
        xgap=2,  # small horizontal gap between years
        ygap=2  # small vertical gap between months
    ))

    # Apply minimal border effect using layout
    fig.update_layout(
        xaxis=dict(
            title='Repayment Years',  # Title for x-axis
            showgrid=False,
            tickfont=dict(size=12),
            ticks='outside',
            mirror=True,
            showline=True,
            linecolor='rgba(255, 255, 255, 0)',
            linewidth=1
        ),
        yaxis=dict(
            title='Month of Year',  # Title for y-axis
            showgrid=False,
            tickfont=dict(size=12),
            ticks='outside',
            mirror=True,
            showline=True,
            linecolor='rgba(255, 255, 255, 0)',
            linewidth=1
        ),
        plot_bgcolor='rgba(255, 255, 255, 0)',  # Set transparent background
        margin=dict(l=40, r=40, t=20, b=40)
    )

    return fig


def monthlyLineChartRepaymentChart(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract year and month
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Get list of unique years sorted
    all_years = sorted(df['Year'].unique())
    current_year = datetime.now().year
    default_year_index = all_years.index(current_year) if current_year in all_years else 0

    # Create traces for each year
    traces = []
    for i, year in enumerate(all_years):
        yearly_data = df[df['Year'] == year]
        monthly_totals = yearly_data.groupby('Month')['Total Repayment'].sum().reindex(range(1, 13), fill_value=0)
        month_names = [calendar.month_abbr[m] for m in monthly_totals.index]

        trace = go.Scatter(
            x=month_names,
            y=monthly_totals.values,
            mode='lines+markers+text',  # Added 'text' to show values on points
            name=str(year),
            visible=(i == default_year_index),  # Only the default year visible
            hovertemplate='Month: %{x}<br>Repayment: %{y:.2f}<extra></extra>',
            line=dict(width=3, color='#27548A'),  # Changed line color to orange
            marker=dict(size=8),
            text=[f'{value:.2f}' for value in monthly_totals.values],  # Show values rounded to two decimals
            textposition='top center'  # Position of the text
        )
        traces.append(trace)

    # Create dropdown buttons
    buttons = []
    for i, year in enumerate(all_years):
        visibility = [False] * len(all_years)
        visibility[i] = True
        buttons.append(dict(
            label=str(year),
            method='update',
            args=[{'visible': visibility},
                  {'title': f"Monthly Repayment Trend for {year}"}]
        ))

    # Create figure
    fig = go.Figure(data=traces)
    fig.update_layout(
        height=380,  # Set the height of the figure
        width=1160,  # Set the width of the figure
        updatemenus=[
            dict(
                buttons=buttons,
                direction='down',
                showactive=True,
                x=0.0,
                xanchor='left',
                y=1.15,
                yanchor='top'
            )
        ],
        xaxis=dict(
            title='Months of the Year',  # X-axis label
            showgrid=False,
            tickfont=dict(size=13)
        ),
        yaxis=dict(
            title='Amount in INR Cr',  # Y-axis label
            showgrid=True,
            gridcolor='lightgrey',
            zeroline=False,
            tickfont=dict(size=13)
        ),
        plot_bgcolor='rgba(255, 255, 255, 0)',
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig


def repaymentFluctuationChart(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract calendar year
    df['Year'] = df['Date'].dt.year

    # Aggregate total repayment per year
    yearly_totals = df.groupby('Year')['Total Repayment'].sum()

    # Calculate YoY growth (%)
    yoy_growth = yearly_totals.pct_change() * 100

    # Create bar chart with color based on growth direction
    colors = ['#2ca02c' if val >= 0 else '#d62728' for val in yoy_growth]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=yearly_totals.index.astype(str).str[-2:],  # Format years to last two digits
        y=yoy_growth.values,
        marker_color=colors,
        text=[f"{v:.2f}%" if pd.notnull(v) else "" for v in yoy_growth.values],
        textposition="outside",
        textfont=dict(color='black', size=14),  # Make text more visible and dark
        hovertemplate='Year: %{x}<br>Growth: %{y:.2f}%<extra></extra>'
    ))

    fig.update_layout(
        height=390,  # Set the height of the figure
        width=1140,  # Set the width of the figure
        xaxis=dict(title='Year', tickfont=dict(size=12)),
        yaxis=dict(title='', showticklabels=False),  # Remove y-axis title and labels
        plot_bgcolor='rgba(255, 255, 255, 0)',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig


import pandas as pd

def riskManagmentTable(file_path):
    # Read Excel
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Year'], format='%b-%y')

    # Extract Year and Month-Year string
    df['Year'] = df['Date'].dt.year
    df['Period'] = df['Date'].dt.strftime('%b-%y')

    # Calculate total repayment per year
    annual_totals = df.groupby('Year')['Total Repayment'].sum().to_dict()

    # Compute % of annual and assign risk
    def assess_risk(row):
        annual = annual_totals.get(row['Year'], 0)
        if annual == 0:
            return pd.Series([None, None])  # Skip rows with 0 annual
        percent = (row['Total Repayment'] / annual) * 100
        if percent >= 9:
            risk = 'High'
        elif percent >= 6:
            risk = 'Medium'
        else:
            risk = 'Low'
        return pd.Series([round(percent, 2), risk])

    df[['% of Annual', 'Risk Level']] = df.apply(assess_risk, axis=1)

    # Filter out rows where percentage is None (i.e., 0-annual years)
    df = df[df['% of Annual'].notnull()]

    # Final table with selected columns
    result = df[['Period', 'Total Repayment', '% of Annual', 'Risk Level']]
    result = result.sort_values(by='% of Annual', ascending=False).reset_index(drop=True)

    return result


def longTermRiskProfileChart(file_path):
    # Load data
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Year'], format='%b-%y')
    df['Year'] = df['Date'].dt.year

    # Total repayment per year
    yearly_totals = df.groupby('Year')['Total Repayment'].sum().reset_index()

    # Normalize for color intensity (optional)
    max_val = yearly_totals['Total Repayment'].max()
    min_val = yearly_totals['Total Repayment'].min()
    colors = yearly_totals['Total Repayment'].apply(
        lambda x: f'rgba(222,45,38,{0.3 + 0.7 * (x - min_val) / (max_val - min_val + 1e-6)})'
    )

    # Create bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly_totals['Year'].astype(str),
        y=yearly_totals['Total Repayment'],
        marker_color=colors,
        hovertemplate='Year: %{x}<br>Repayment: %{y:.2f}<extra></extra>',
        text=yearly_totals['Total Repayment'].round(2),
        textposition='outside'
    ))

    fig.update_layout(
        xaxis=dict(title='Year', tickfont=dict(size=12)),
        yaxis=dict(title='Total Repayment', tickfont=dict(size=12), gridcolor='lightgrey'),
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )

    return fig