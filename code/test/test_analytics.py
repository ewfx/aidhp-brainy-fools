import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from src.analytics import BankingCustomerAnalytics
from src.data_generation import generate_synthetic_banking_data

@pytest.fixture
def sample_data():
    """Generate a small synthetic dataset for testing"""
    return generate_synthetic_banking_data(50)  # Small dataset for faster tests

@pytest.fixture
def analytics_instance(sample_data):
    """Create an instance of BankingCustomerAnalytics with sample data"""
    return BankingCustomerAnalytics(sample_data)

def test_initialization(analytics_instance):
    """Test that the analytics class initializes correctly"""
    assert isinstance(analytics_instance.df, pd.DataFrame)
    assert not analytics_instance.df.empty
    assert 'sentiment' in analytics_instance.df.columns
    assert 'segment' in analytics_instance.df.columns

def test_preprocessing(analytics_instance):
    """Test data preprocessing steps"""
    df = analytics_instance.df
    
    # Test sentiment analysis
    assert all(df['sentiment'].between(-1, 1))
    assert set(df['sentiment_category'].unique()) == {'Negative', 'Neutral', 'Positive'}
    
    # Test product indicator columns
    assert any(col.startswith('has_') for col in df.columns)
    for product in ['checking', 'savings', 'credit_card']:
        assert f'has_{product}' in df.columns

def test_feature_creation(analytics_instance):
    """Test feature engineering"""
    df = analytics_instance.df
    
    # Test financial ratios
    assert all(df['debt_to_income'] >= 0)
    assert all(df['savings_ratio'] >= 0)
    assert all(df['investment_ratio'] >= 0)
    
    # Test calculated fields
    assert all(df['net_worth'] == 
               df['total_assets'] - (df['mortgage_balance'] + df['credit_card_balance']))
    
    # Test behavioral scores
    assert all(df['digital_engagement_score'].between(0, 100))
    assert all(df['ecommerce_activity_score'] >= 0)

def test_model_training(analytics_instance):
    """Test machine learning models"""
    # Test clustering
    assert set(analytics_instance.df['segment'].unique()) == {0, 1, 2, 3, 4}
    assert all(analytics_instance.df['segment_name'].isin(
        ['Mass Market', 'Digital Natives', 'Affluent Investors', 
         'Traditional Savers', 'High-Potential']))
    
    # Test anomaly detection
    assert 'is_anomaly' in analytics_instance.df.columns
    assert analytics_instance.df['is_anomaly'].dtype == bool
    assert 0 < analytics_instance.df['is_anomaly'].mean() < 0.2  # Rough check for anomaly rate

def test_scaler_fitted(analytics_instance):
    """Test that the scaler was properly fitted"""
    assert isinstance(analytics_instance.scaler, StandardScaler)
    assert hasattr(analytics_instance.scaler, 'mean_')  # Verify scaler was fitted
    assert hasattr(analytics_instance.scaler, 'scale_')

def test_empty_data():
    """Test handling of empty DataFrames"""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError):
        BankingCustomerAnalytics(empty_df)

def test_missing_columns():
    """Test handling of DataFrames with missing required columns"""
    incomplete_df = pd.DataFrame({
        'income': [50000],
        'credit_score': [700]
    })
    with pytest.raises(KeyError):
        BankingCustomerAnalytics(incomplete_df)

def test_product_recommendations(analytics_instance):
    """Test product recommendations method"""
    # Test with valid customer ID
    valid_id = analytics_instance.df['customer_id'].iloc[0]
    recs = analytics_instance.get_product_recommendations(valid_id)
    assert isinstance(recs, list)
    
    # Test with invalid customer ID
    invalid_id = 9999
    recs = analytics_instance.get_product_recommendations(invalid_id)
    assert recs == []

def test_segment_distribution(analytics_instance):
    """Test that segments are reasonably distributed"""
    segment_counts = analytics_instance.df['segment_name'].value_counts(normalize=True)
    for segment in ['Mass Market', 'Digital Natives', 'Affluent Investors']:
        assert 0.1 < segment_counts[segment] < 0.5  # No segment should dominate

def test_numeric_features(analytics_instance):
    """Test that all features for clustering are numeric"""
    numeric_cols = [
        'income', 'credit_score', 'checking_balance',
        'savings_balance', 'online_purchases', 'app_logins',
        'investment_balance', 'digital_engagement_score',
        'ecommerce_activity_score', 'clv'
    ]
    for col in numeric_cols:
        assert pd.api.types.is_numeric_dtype(analytics_instance.df[col])
