import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Initialize NLTK
nltk.download('vader_lexicon', quiet=True)

class BankingCustomerAnalytics:
    def __init__(self, df):
        self.df = df.copy()
        self._preprocess_data()
        self._create_features()
        self._train_models()
        
    def _preprocess_data(self):
        """Data cleaning and preprocessing"""
        # Sentiment Analysis
        sia = SentimentIntensityAnalyzer()
        banking_lexicon = {
            'improvement': -0.5, 'excellent': 2.0, 'confusing': -1.5,
            'best': 1.8, 'better': 0.5, 'needs': -0.7, 'love': 1.5,
            'slow': -1.0, 'intuitive': 1.2, 'low': -0.8, 'great': 1.3
        }
        sia.lexicon.update(banking_lexicon)
        
        self.df['sentiment'] = self.df['feedback'].apply(lambda x: sia.polarity_scores(x)['compound'])
        self.df['sentiment_category'] = np.where(
            self.df['sentiment'] < -0.5, 'Negative',
            np.where(self.df['sentiment'] > 0.5, 'Positive', 'Neutral')
        )
        
        # Create product indicator columns
        all_products = set()
        for products in self.df['products_used']:
            all_products.update(products)
        
        for product in all_products:
            self.df[f'has_{product}'] = self.df['products_used'].apply(lambda x: product in x)
    
    def _create_features(self):
        """Create financial and behavioral features"""
        # Financial Health Metrics
        self.df['debt_to_income'] = (self.df['mortgage_balance'] + self.df['credit_card_balance']) / self.df['income']
        self.df['savings_ratio'] = self.df['savings_balance'] / self.df['income']
        self.df['investment_ratio'] = self.df['investment_balance'] / self.df['income']
        self.df['liquid_assets'] = self.df['checking_balance'] + self.df['savings_balance']
        self.df['total_assets'] = self.df['liquid_assets'] + self.df['investment_balance']
        self.df['net_worth'] = self.df['total_assets'] - (self.df['mortgage_balance'] + self.df['credit_card_balance'])
        
        # Behavioral Features
        self.df['digital_engagement_score'] = (
            self.df['app_logins'] * 0.5 + 
            self.df['social_posts'] * 0.3 + 
            self.df['rewards_claimed'] * 0.2
        )
        self.df['ecommerce_activity_score'] = (
            self.df['online_purchases'] * 0.6 + 
            self.df['mobile_payments'] * 0.4 - 
            self.df['abandoned_carts'] * 0.2
        )
        
        # Spending Categories
        spending_cols = ['groceries', 'dining', 'shopping', 'travel', 'luxury']
        self.df['total_spending'] = self.df[spending_cols].sum(axis=1)
        for col in spending_cols:
            self.df[f'{col}_ratio'] = self.df[col] / self.df['total_spending'].replace(0, 1)
        
        # Customer Lifetime Value (simplified)
        self.df['clv'] = (
            self.df['income'] * 0.05 +  # Revenue from interest/spread
            self.df['total_assets'] * 0.01 +  # Asset-based fees
            self.df['digital_engagement_score'] * 10  # Engagement multiplier
        )
    
    def _train_models(self):
        """Train machine learning models"""
        # Features for segmentation
        segment_features = [
            'income', 'credit_score', 'checking_balance',
            'savings_balance', 'online_purchases', 'app_logins',
            'investment_balance', 'digital_engagement_score',
            'ecommerce_activity_score', 'clv'
        ]
        
        # Scale features
        self.scaler = StandardScaler()
        scaled_features = self.scaler.fit_transform(self.df[segment_features].fillna(0))
        
        # Clustering
        self.kmeans = KMeans(n_clusters=5, random_state=42, n_init=20)
        self.df['segment'] = self.kmeans.fit_predict(scaled_features)
        
        # Name segments
        self.segment_names = {
            0: 'Mass Market',
            1: 'Digital Natives',
            2: 'Affluent Investors',
            3: 'Traditional Savers',
            4: 'High-Potential'
        }
        self.df['segment_name'] = self.df['segment'].map(self.segment_names)
        
        # Anomaly detection
        self.anomaly_detector = IsolationForest(contamination=0.05, random_state=42)
        self.df['anomaly_score'] = self.anomaly_detector.fit_predict(scaled_features)
        self.df['is_anomaly'] = self.df['anomaly_score'] == -1
        
    def get_product_recommendations(self, customer_id):
        """Get product recommendations based on similar customers"""
        # Implementation would go here
        return []
