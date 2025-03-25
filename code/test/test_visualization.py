import pytest
import pandas as pd
import plotly.graph_objects as go
from src.visualization import (
    create_spending_profile,
    create_financial_health_radar,
    create_trend_projection
)

# Sample customer data for testing
@pytest.fixture
def sample_customer():
    return pd.Series({
        'customer_id': 1001,
        'groceries': 12,
        'dining': 8,
        'shopping': 15,
        'bills': 6,
        'travel': 4,
        'debt_to_income': 0.35,
        'savings_ratio': 0.2,
        'investment_ratio': 0.3,
        'credit_score': 725,
        'digital_engagement_score': 75,
        'income': 85000,
        'savings_balance': 15000,
        'investment_balance': 25000,
        'mortgage_balance': 200000,
        'credit_card_balance': 5000
    })

def test_create_spending_profile(sample_customer):
    """Test spending profile visualization"""
    # Test with default categories
    fig = create_spending_profile(sample_customer)
    
    assert isinstance(fig, go.Figure), "Should return a Plotly Figure"
    assert fig.layout.title.text == "Monthly Spending Pattern", "Incorrect title"
    assert len(fig.data[0].labels) == 5, "Should show 5 spending categories"
    assert sum(fig.data[0].values) > 0, "Spending values should be positive"
    
    # Test with custom categories
    custom_categories = ['groceries', 'dining', 'travel']
    fig_custom = create_spending_profile(sample_customer, custom_categories)
    assert len(fig_custom.data[0].labels) == 3, "Should show 3 custom categories"

def test_create_financial_health_radar(sample_customer):
    """Test financial health radar chart"""
    fig = create_financial_health_radar(sample_customer)
    
    assert isinstance(fig, go.Figure), "Should return a Plotly Figure"
    assert fig.layout.title.text == "Financial Health Radar Chart", "Incorrect title"
    assert len(fig.data) == 2, "Should have 2 traces (customer + benchmark)"
    
    # Check metrics are properly scaled
    customer_trace = fig.data[0]
    assert max(customer_trace.r) <= 1, "Values should be normalized to 0-1 range"
    assert 'Debt-to-Income' in customer_trace.theta, "Missing key metric"

def test_create_trend_projection(sample_customer):
    """Test financial trend projection"""
    fig = create_trend_projection(sample_customer)
    
    assert isinstance(fig, go.Figure), "Should return a Plotly Figure"
    assert fig.layout.title.text == "12-Month Financial Projection", "Incorrect title"
    
    # Should have at least 2 traces (savings + investments)
    assert len(fig.data) >= 2, "Should show at least two financial trends"
    
    # Check projections make mathematical sense
    savings_proj = fig.data[0].y
    assert savings_proj[0] == sample_customer['savings_balance'], "Should start with current balance"
    assert savings_proj[-1] > savings_proj[0], "Savings should grow over time"

def test_edge_cases():
    """Test visualization functions with edge cases"""
    # Test with minimal customer data
    minimal_customer = pd.Series({
        'groceries': 1,
        'dining': 1,
        'debt_to_income': 0,
        'savings_ratio': 0,
        'investment_ratio': 0,
        'credit_score': 300,
        'digital_engagement_score': 0,
        'income': 10000,
        'savings_balance': 0,
        'investment_balance': 0,
        'mortgage_balance': 0,
        'credit_card_balance': 0
    })
    
    # All functions should handle minimal data without errors
    assert create_spending_profile(minimal_customer) is not None
    assert create_financial_health_radar(minimal_customer) is not None
    assert create_trend_projection(minimal_customer) is not None
    
    # Test with missing spending categories
    with pytest.raises(KeyError):
        create_spending_profile(pd.Series({}), ['nonexistent_category'])
