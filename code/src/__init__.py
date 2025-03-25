from src.data_generation import generate_synthetic_banking_data
from src.analytics import BankingCustomerAnalytics
from src.dashboard import generate_dashboard

# Generate data
bank_customers = generate_synthetic_banking_data(500)

# Analyze data
analytics = BankingCustomerAnalytics(bank_customers)

# Generate dashboard for customer 1001
generate_dashboard(1001, bank_customers, analytics)
