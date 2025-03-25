"""
Banking Customer Analytics Dashboard

A comprehensive banking customer analytics system with:
- Synthetic data generation
- Customer segmentation 
- Anomaly detection
- Personalized recommendations
- Interactive financial dashboard
"""

from .data_generation import generate_synthetic_banking_data
from .analytics import BankingCustomerAnalytics
from .visualization import (
    create_spending_profile,
    create_financial_health_radar,
    create_trend_projection
)
from .recommendations import BankingRecommendationEngine
from .dashboard import generate_dashboard

__all__ = [
    'generate_synthetic_banking_data',
    'BankingCustomerAnalytics',
    'create_spending_profile',
    'create_financial_health_radar',
    'create_trend_projection',
    'BankingRecommendationEngine',
    'generate_dashboard'
]

__version__ = '0.1.0'
