import pytest
from src.data_generation import generate_synthetic_banking_data

def test_data_generation():
    df = generate_synthetic_banking_data(10)
    assert len(df) == 10
    assert 'customer_id' in df.columns
    assert 'name' in df.columns
    assert 'income' in df.columns
