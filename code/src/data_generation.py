import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_banking_data(num_customers=500):
    np.random.seed(42)
    random.seed(42)
    
    # US states with abbreviations
    us_states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
        'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'NewHampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
        'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    state_codes = list(us_states.keys())
    state_names = list(us_states.values())
    
    # Education levels
    education_levels = [
        'High School', 'Some College', 'Associate Degree', 
        "Bachelor's Degree", "Master's Degree", 'Doctorate', 'Professional Degree'
    ]
    
    # Common first and last names in the US
    first_names_male = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles']
    first_names_female = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    # Life stages with probabilities
    life_stages = ['young_professional', 'established_family', 'growing_family', 
                  'pre_retirement', 'retired', 'new_family', 'single_professional']
    life_stage_probs = [0.25, 0.2, 0.15, 0.1, 0.1, 0.1, 0.1]
    
    # Generate synthetic data
    customer_ids = range(1000, 1000 + num_customers)
    genders = np.random.choice(['Male', 'Female'], num_customers, p=[0.48, 0.52])
    ages = np.random.randint(18, 80, num_customers)
    incomes = np.round(np.random.lognormal(10.5, 0.35, num_customers), -3)
    credit_scores = np.random.normal(700, 50, num_customers).astype(int)
    credit_scores = np.clip(credit_scores, 300, 850)
    
    # Generate names based on gender
    names = []
    for gender in genders:
        if gender == 'Male':
            first = random.choice(first_names_male)
        else:
            first = random.choice(first_names_female)
        last = random.choice(last_names)
        names.append(f"{first} {last}")
    
    # Generate education levels correlated with age
    education = []
    for age in ages:
        if age < 22:
            edu = random.choice(['High School', 'Some College'])
        elif age < 30:
            edu = random.choice(['Some College', 'Associate Degree', "Bachelor's Degree"])
        elif age < 45:
            edu = random.choice(["Bachelor's Degree", "Master's Degree"])
        else:
            edu = random.choice(["Bachelor's Degree", "Master's Degree", 'Professional Degree', 'Doctorate'])
        education.append(edu)
    
    # Generate states with some concentration in populous states
    state_weights = [1.0] * len(state_codes)  # Base weights
    # Increase weight for populous states
    for i, code in enumerate(state_codes):
        if code in ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH']:
            state_weights[i] = 3.0
    state_weights = np.array(state_weights) / sum(state_weights)
    
    states = np.random.choice(state_codes, num_customers, p=state_weights)
    state_full_names = [us_states[code] for code in states]
    
    # Generate marital status correlated with age and life stage
    marital_status = []
    for age in ages:
        if age < 25:
            marital = random.choice(['Single', 'Single', 'Single', 'Married'])
        elif age < 40:
            marital = random.choice(['Single', 'Married', 'Married', 'Divorced'])
        else:
            marital = random.choice(['Married', 'Married', 'Divorced', 'Widowed'])
        marital_status.append(marital)
    
    # Generate number of children correlated with age and marital status
    num_children = []
    for age, marital in zip(ages, marital_status):
        if marital == 'Single':
            children = random.choices([0, 1, 2], weights=[0.8, 0.15, 0.05])[0]
        elif marital == 'Married':
            if age < 30:
                children = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2])[0]
            elif age < 45:
                children = random.choices([0, 1, 2, 3], weights=[0.2, 0.3, 0.3, 0.2])[0]
            else:
                children = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
        else:  # Divorced/Widowed
            children = random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1])[0]
        num_children.append(children)
    
    # Generate correlated financial data (existing code)
    checking_balances = np.round(incomes * np.random.uniform(0.05, 0.3, num_customers), 2)
    savings_balances = np.round(incomes * np.random.uniform(0.1, 2.0, num_customers), 2)
    investment_balances = np.where(
        incomes > 100000,
        np.round(incomes * np.random.uniform(0.5, 5.0, num_customers), 2),
        np.round(incomes * np.random.uniform(0, 0.5, num_customers), 2)
    )
    
    # Generate mortgage data correlated with age and income
    has_mortgage = (ages > 25) & (ages < 65) & (incomes > 50000)
    mortgage_balances = np.where(
        has_mortgage,
        np.round(incomes * np.random.uniform(2, 5, num_customers), 2),
        0
    )
    
    # Generate credit card balances
    credit_card_balances = np.round(incomes * np.random.uniform(0.02, 0.15, num_customers), 2)
    
    # Generate transaction categories as separate columns
    spending_categories = ['groceries', 'dining', 'shopping', 'bills', 
                         'investments', 'travel', 'gas', 'luxury', 'utilities']
    transaction_data = {
        cat: np.random.randint(0, 20, num_customers) for cat in spending_categories
    }
    
    # Generate social engagement
    social_data = {
        'app_logins': np.random.randint(10, 150, num_customers),
        'social_posts': np.random.randint(0, 10, num_customers),
        'rewards_claimed': np.random.randint(0, 5, num_customers),
        'customer_service_contacts': np.random.randint(0, 3, num_customers)
    }
    
    # Generate ecommerce activity
    ecommerce_data = {
        'online_purchases': np.random.randint(0, 20, num_customers),
        'mobile_payments': np.random.randint(0, 15, num_customers),
        'abandoned_carts': np.random.randint(0, 5, num_customers)
    }
    
    # Generate satisfaction metrics
    satisfaction_data = {
        'nps_score': np.random.randint(0, 11, num_customers),
        'csat': np.random.randint(1, 6, num_customers),
        'complaints': np.random.randint(0, 4, num_customers)
    }
    
    # Generate feedback comments
    feedback_options = [
        "The mobile app needs improvement for bill payments",
        "Excellent investment advisory services",
        "Mortgage payment process is confusing",
        "Best private banking experience ever",
        "Credit card rewards could be better",
        "Website navigation is intuitive and easy",
        "Customer service response times are too slow",
        "Love the new budgeting features in the app",
        "Interest rates on savings accounts are too low",
        "Would like more ATM locations in my area"
    ]
    
    # Generate products used
    product_options = ['checking', 'savings', 'mortgage', 'credit_card', 
                      'investment', 'auto_loan', 'student_loan', 'debit_card']
    
    def generate_products():
        num_products = random.randint(1, 6)
        return random.sample(product_options, num_products)
    
    # Create the DataFrame with enhanced demographic data
    data = {
        'customer_id': customer_ids,
        'name': names,
        'gender': genders,
        'age': ages,
        'education': education,
        'marital_status': marital_status,
        'num_children': num_children,
        'country': 'United States',
        'state': states,
        'state_name': state_full_names,
        'income': incomes,
        'credit_score': credit_scores,
        'checking_balance': checking_balances,
        'savings_balance': savings_balances,
        'mortgage_balance': mortgage_balances,
        'credit_card_balance': credit_card_balances,
        'investment_balance': investment_balances,
        'products_used': [generate_products() for _ in range(num_customers)],
        'feedback': random.choices(feedback_options, k=num_customers),
        'life_stage': np.random.choice(life_stages, num_customers, p=life_stage_probs)
    }
    
    # Add all the generated data
    data.update(transaction_data)
    data.update(social_data)
    data.update(ecommerce_data)
    data.update(satisfaction_data)
    
    return pd.DataFrame(data)
