# Banking Customer Analytics Dashboard

A comprehensive banking customer analytics system with synthetic data generation, customer segmentation, anomaly detection, and personalized recommendations.

## Features

- Synthetic customer data generation with realistic financial and demographic attributes
- Customer segmentation using K-means clustering
- Anomaly detection with Isolation Forest
- Personalized product recommendations
- Interactive financial dashboard with visualizations

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install requirements: `pip install -r requirements.txt`

## Usage

Run the dashboard with:
```python
from src.dashboard import generate_dashboard
generate_dashboard(1001)  # Replace with desired customer ID
