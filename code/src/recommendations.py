class BankingRecommendationEngine:
    def __init__(self, analytics):
        self.analytics = analytics
        self.product_info = {
            'checking': {'desc': "Basic checking account", 'benefit': "No fees"},
            'savings': {'desc': "High-yield savings", 'benefit': "2.5% APY"},
            'mortgage': {'desc': "Home loan", 'benefit': "Low rates"},
            'credit_card': {'desc': "Rewards card", 'benefit': "Cash back"},
            'investment': {'desc': "Investment account", 'benefit': "Grow wealth"},
            'auto_loan': {'desc': "Car financing", 'benefit': "Competitive rates"},
            'student_loan': {'desc': "Student loan", 'benefit': "Refinancing options"},
            'debit_card': {'desc': "Debit card", 'benefit': "Easy access"}
        }
    
    def generate_recommendations(self, customer_id):
        """Generate personalized recommendations"""
        try:
            customer = self.analytics.df[self.analytics.df['customer_id'] == customer_id].iloc[0]
            segment_data = self.analytics.df[self.analytics.df['segment'] == customer['segment']]
            
            recommendations = {
                'financial_products': self._get_product_recs(customer),
                'digital_services': self._get_digital_recs(customer, segment_data),
                'wealth_management': self._get_wealth_recs(customer),
                'credit_optimization': self._get_credit_recs(customer),
                'financial_education': self._get_life_stage_recs(customer),
                'banking_habits': self._get_habit_recs(customer),
                'alerts': self._get_alerts(customer, segment_data)
            }
            
            return recommendations
        except IndexError:
            print(f"Customer {customer_id} not found")
            return None
    
    def _get_product_recs(self, customer):
        """Recommend products customer doesn't have"""
        current_products = customer['products_used']
        return [
            f"{self.product_info[p]['desc']}: {self.product_info[p]['benefit']}"
            for p in self.product_info
            if p not in current_products
        ][:3]  # Limit to top 3
    
    def _get_digital_recs(self, customer, segment_data):
        """Digital service recommendations"""
        recs = []
        if customer['app_logins'] < segment_data['app_logins'].median():
            recs.append("Enable push notifications to increase app engagement")
        if customer['mobile_payments'] < 5:
            recs.append("Try our mobile payment feature for faster checkouts")
        return recs
    
    def _get_wealth_recs(self, customer):
        """Wealth management recommendations"""
        recs = []
        if customer['investment_balance'] < 10000 and customer['age'] < 50:
            recs.append("Start investing with as little as $100 in our starter portfolio")
        if customer['investment_balance'] > 50000:
            recs.append("Schedule a consultation with our wealth management team")
        return recs
    
    def _get_credit_recs(self, customer):
        """Credit optimization recommendations"""
        recs = []
        if customer['credit_card_balance'] > 5000:
            recs.append("Consider a balance transfer to reduce interest payments")
        if customer['credit_score'] < 700:
            recs.append("Credit building program available to help improve your score")
        return recs
    
    def _get_life_stage_recs(self, customer):
        """Life stage specific recommendations"""
        stage = customer['life_stage']
        if stage == 'young_professional':
            return ["Start retirement savings early", "Build credit history"]
        elif stage == 'established_family':
            return ["College savings plans", "Home equity options"]
        elif stage == 'retired':
            return ["Required Minimum Distribution calculator", "Estate planning guide"]
        else:
            return ["Financial wellness checkup"]
    
    def _get_habit_recs(self, customer):
        """Banking habit recommendations"""
        recs = []
        if customer['checking_balance'] > 10000:
            recs.append("Move excess cash to savings to earn more interest")
        if customer['debt_to_income'] > 0.4:
            recs.append("Debt consolidation options available")
        return recs
    
    def _get_alerts(self, customer, segment_data):
        """Financial alerts"""
        alerts = []
        if customer['is_anomaly']:
            alerts.append("Unusual activity detected - please verify your transactions")
        if customer['debt_to_income'] > 0.5:
            alerts.append("High debt-to-income ratio - consider debt counseling")
        return alerts
