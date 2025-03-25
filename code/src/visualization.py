import plotly.graph_objects as go
import plotly.express as px

def create_spending_profile(customer, spending_cols=None):
    """Create a spending profile visualization"""
    if spending_cols is None:
        spending_cols = ['groceries', 'dining', 'shopping', 'bills', 'travel']
    
    spending_data = {col: customer[col] for col in spending_cols if col in customer}
    
    if not spending_data:
        return None
    
    fig = go.Figure(go.Pie(
        labels=list(spending_data.keys()),
        values=list(spending_data.values()),
        hole=0.4,
        marker_colors=px.colors.qualitative.Pastel
    ))
    fig.update_layout(
        title="Monthly Spending Pattern",
        height=350,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    return fig

def create_financial_health_radar(customer):
    """Create a radar chart of financial health"""
    metrics = {
        'Debt-to-Income': min(1, customer['debt_to_income']),
        'Savings Ratio': min(1, customer['savings_ratio'] * 5),
        'Investment Ratio': min(1, customer['investment_ratio']),
        'Credit Score': customer['credit_score'] / 850,
        'Digital Engagement': customer['digital_engagement_score'] / 100
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        name='Your Metrics',
        line_color='#4E79A7'
    ))
    
    # Add benchmark values
    ideal_values = {
        'Debt-to-Income': 0.35,
        'Savings Ratio': 0.2 * 5,
        'Investment Ratio': 0.3,
        'Credit Score': 750/850,
        'Digital Engagement': 0.7
    }
    
    fig.add_trace(go.Scatterpolar(
        r=list(ideal_values.values()),
        theta=list(ideal_values.keys()),
        name='Ideal Benchmark',
        line_color='#59A14F'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Financial Health Radar Chart",
        height=350
    )
    
    return fig

def create_trend_projection(customer):
    """Create financial projections"""
    months = list(range(0, 13))
    
    # Project savings growth (5% annual return)
    current_savings = customer['savings_balance']
    savings_proj = [current_savings * (1.05)**(m/12) for m in months]
    
    # Project investment growth (7% annual return)
    current_investment = customer['investment_balance']
    investment_proj = [current_investment * (1.07)**(m/12) for m in months]
    
    # Project debt reduction
    current_debt = customer['mortgage_balance'] + customer['credit_card_balance']
    if current_debt > 0:
        annual_payment = customer['income'] * 0.15
        debt_proj = [max(0, current_debt - (annual_payment * m/12)) for m in months]
    else:
        debt_proj = [0] * len(months)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=savings_proj,
        mode='lines+markers',
        name='Savings',
        line=dict(color='#4E79A7', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=investment_proj,
        mode='lines+markers',
        name='Investments',
        line=dict(color='#59A14F', width=2)
    ))
    
    if current_debt > 0:
        fig.add_trace(go.Scatter(
            x=months,
            y=debt_proj,
            mode='lines+markers',
            name='Debt',
            line=dict(color='#E15759', width=2)
        ))
    
    fig.update_layout(
        title="12-Month Financial Projection",
        xaxis_title="Months",
        yaxis_title="Amount ($)",
        hovermode="x unified",
        height=350
    )
    
    return fig
