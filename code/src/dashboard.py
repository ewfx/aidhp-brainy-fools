from IPython.display import display, HTML
from .visualization import create_spending_profile, create_financial_health_radar, create_trend_projection
from .recommendations import BankingRecommendationEngine

def generate_dashboard(customer_id, bank_customers, analytics):
    """Generate customer dashboard"""
    try:
        customer = bank_customers[bank_customers['customer_id'] == customer_id].iloc[0]
    except IndexError:
        display(HTML("""<div style="color: red; padding: 20px; border: 1px solid red;">
                      Customer not found</div>"""))
        return
    
    # Get recommendations
    recommendation_engine = BankingRecommendationEngine(analytics)
    recommendations = recommendation_engine.generate_recommendations(customer_id)
    
    # Determine life stage icon
    life_stage_icons = {
        'young_professional': '👔',
        'established_family': '👨‍👩‍👧‍👦',
        'growing_family': '👪',
        'pre_retirement': '🏖️',
        'retired': '🧓',
        'new_family': '👶',
        'single_professional': '💼'
    }
    
    # Header with enhanced demographic information and visual elements
    display(HTML(f"""
    <div style="background: linear-gradient(135deg, #1a2980, #26d0ce); 
        padding: 25px; border-radius: 10px; color: white; margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); position: relative; overflow: hidden;">
        
        <!-- Decorative elements -->
        <div style="position: absolute; right: 20px; top: 20px; opacity: 0.1;">
            <svg width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <!-- Left Section - Customer Identity -->
            <div style="flex: 1; padding-right: 20px;">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="background: rgba(255,255,255,0.2); width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 24px;">
                        {'👨' if customer['gender'] == 'Male' else '👩'}
                    </div>
                    <div>
                        <h1 style="margin: 0 0 5px 0; font-size: 28px;">{customer['name']}</h1>
                        <div style="font-size: 14px; display: flex; align-items: center; gap: 10px;">
                            <span>ID: {customer_id}</span>
                            <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px;">
                                {customer['state']}
                            </span>
                        </div>
                    </div>
                </div>
                
                <!-- Demographic Details Grid -->
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                    <div style="background: rgba(255,255,255,0.1); padding: 8px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">AGE</div>
                        <div style="font-size: 16px; font-weight: bold;">{customer['age']}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 8px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">GENDER</div>
                        <div style="font-size: 16px; font-weight: bold;">{customer['gender']}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 8px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">CHILDREN</div>
                        <div style="font-size: 16px; font-weight: bold;">{customer['num_children']} {'👶' * customer['num_children'] if customer['num_children'] > 0 else '—'}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 8px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">EDUCATION</div>
                        <div style="font-size: 16px; font-weight: bold;">{customer['education'].split()[0]}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 8px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">MARITAL</div>
                        <div style="font-size: 16px; font-weight: bold;">{customer['marital_status'][0]}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 8px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">LOCATION</div>
                        <div style="font-size: 16px; font-weight: bold;">{customer['state_name'].split()[0] if len(customer['state_name'].split()) > 1 else customer['state_name']}</div>
                    </div>
                </div>
            </div>
            
            <!-- Center Divider -->
            <div style="width: 1px; height: 120px; background: rgba(255,255,255,0.3); margin: 0 20px;"></div>
            
            <!-- Right Section - Financial Summary -->
            <div style="flex: 1; padding-left: 20px;">
                <!-- Segment Card -->
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                        <span style="font-size: 24px;">{life_stage_icons.get(customer['life_stage'], '👤')}</span>
                        <div>
                            <div style="font-size: 16px; font-weight: bold;">{customer['segment_name']}</div>
                            <div style="font-size: 12px; opacity: 0.9;">{customer['life_stage'].replace('_', ' ').title()}</div>
                        </div>
                    </div>
                </div>
                
                <!-- Financial Stats -->
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                    <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">INCOME</div>
                        <div style="font-size: 18px; font-weight: bold;">${customer['income']/1000:.0f}K</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">CREDIT SCORE</div>
                        <div style="font-size: 18px; font-weight: bold; color: {'#006400' if customer['credit_score'] > 700 else '#FFC107' if customer['credit_score'] > 600 else '#F44336'}">
                            {customer['credit_score']}
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">NET WORTH</div>
                        <div style="font-size: 18px; font-weight: bold;">${customer['net_worth']/1000:.0f}K</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px;">
                        <div style="font-size: 11px; opacity: 0.8;">CLV [Customer Lifetime Value]</div>
                        <div style="font-size: 18px; font-weight: bold;">${customer['clv']/1000:.0f}K</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """))
    
    # First Row - Financial Overview
    display(HTML("<h3 style='color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px;'>Financial Overview</h3>"))
    
    # Create and show visualizations
    spending_cols = ['groceries', 'dining', 'shopping', 'bills', 'travel']
    spending_fig = create_spending_profile(customer, spending_cols)
    if spending_fig:
        spending_fig.show()
    
    health_fig = create_financial_health_radar(customer)
    health_fig.show()
    
    # Second Row - Projections
    display(HTML("<h3 style='color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px;'>Financial Projections</h3>"))
    trend_fig = create_trend_projection(customer)
    trend_fig.show()
    
    # Third Row - Customer Insights
    display(HTML("<h3 style='color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px;'>Customer Insights</h3>"))
    
    # Get primary spending category
    spending_cols = ['groceries', 'dining', 'shopping', 'bills', 'travel']
    primary_spending = max(spending_cols, key=lambda x: customer.get(x, 0))
    
    insights_html = f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px;">
        <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="margin-top: 0; color: #0d47a1; border-bottom: 1px solid #bbdefb; padding-bottom: 8px;">Financial Snapshot</h4>
            <p><strong>Total Assets:</strong> ${customer['total_assets']:,.0f}</p>
            <p><strong>Liquid Assets:</strong> ${customer['liquid_assets']:,.0f}</p>
            <p><strong>Total Debt:</strong> ${customer['mortgage_balance'] + customer['credit_card_balance']:,.0f}</p>
            <p><strong>Debt-to-Income:</strong> {customer['debt_to_income']:.2f} {'🚩' if customer['debt_to_income'] > 0.4 else ''}</p>
        </div>
        
        <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="margin-top: 0; color: #2e7d32; border-bottom: 1px solid #c8e6c9; padding-bottom: 8px;">Behavioral Insights</h4>
            <p><strong>Digital Engagement:</strong> {customer['digital_engagement_score']:.1f}/100</p>
            <p><strong>E-commerce Activity:</strong> {customer['ecommerce_activity_score']:.1f}/100</p>
            <p><strong>Primary Spending:</strong> {primary_spending.title()}</p>
            <p><strong>Products Used:</strong> {len(customer['products_used'])} of 8</p>
        </div>
        
        <div style="background: #fff3e0; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="margin-top: 0; color: #e65100; border-bottom: 1px solid #ffe0b2; padding-bottom: 8px;">Customer Experience</h4>
            <p><strong>NPS Score:</strong> {customer['nps_score']}/10 {'⭐' * int(customer['nps_score'])}</p>
            <p><strong>Sentiment:</strong> <span style="color: {'#F44336' if customer['sentiment_category'] == 'Negative' else '#FFC107' if customer['sentiment_category'] == 'Neutral' else '#4CAF50'}">
                {customer['sentiment_category']}</span></p>
            <p><strong>Feedback:</strong> "{customer['feedback']}"</p>
            <p><strong>Anomaly Detection:</strong> {'⚠️ Flagged' if customer['is_anomaly'] else '✅ Normal'}</p>
        </div>
    </div>
    """
    display(HTML(insights_html))
    
    # Recommendations section remains the same...
    if recommendations:
        display(HTML("<h3 style='color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px;'>Personalized Recommendations</h3>"))
        
        def create_rec_card(title, recs, icon, color):
            if recs:
                return f"""
                <div style="background: {color}08; border-left: 4px solid {color}; padding: 15px; border-radius: 5px; margin-bottom: 15px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <h4 style="margin-top: 0; color: {color}; display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 20px;">{icon}</span> {title}
                    </h4>
                    <ul style="padding-left: 20px; margin-bottom: 0;">{''.join(f'<li style="margin-bottom: 8px;">{rec}</li>' for rec in recs)}</ul>
                </div>
                """
            return ""
        
        rec_html = "<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;'>"
        
        rec_html += create_rec_card(
            "Financial Products", 
            recommendations['financial_products'], 
            "💰", "#2196F3"
        )
        rec_html += create_rec_card(
            "Digital Services", 
            recommendations['digital_services'], 
            "📱", "#4CAF50"
        )
        rec_html += create_rec_card(
            "Wealth Management", 
            recommendations['wealth_management'], 
            "📈", "#9C27B0"
        )
        rec_html += create_rec_card(
            "Credit Optimization", 
            recommendations['credit_optimization'], 
            "💳", "#FF9800"
        )
        rec_html += create_rec_card(
            "Financial Education", 
            recommendations['financial_education'], 
            "🎓", "#00BCD4"
        )
        rec_html += create_rec_card(
            "Banking Habits", 
            recommendations['banking_habits'], 
            "🔄", "#607D8B"
        )
        
        # Alerts at the bottom spanning full width
        if recommendations['alerts']:
            rec_html += f"""
            <div style="grid-column: span 2; background: #ffebee; border-left: 4px solid #f44336; 
                        padding: 15px; border-radius: 5px; margin-top: 10px;">
                <h4 style="margin-top: 0; color: #f44336; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 20px;">⚠️</span> Important Alerts
                </h4>
                <ul style="padding-left: 20px; margin-bottom: 0;">{''.join(f'<li style="margin-bottom: 8px; color: #b71c1c;">{rec}</li>' for rec in recommendations['alerts'])}</ul>
            </div>
            """
        
        rec_html += "</div>"
        display(HTML(rec_html))
