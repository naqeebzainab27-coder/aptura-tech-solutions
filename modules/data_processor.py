import pandas as pd
import numpy as np

def load_data(file):
    """Load CSV file into a DataFrame"""
    df = pd.read_csv(file)
    return df

def clean_data(df):
    """Clean and prepare the data"""
    df = df.drop_duplicates()
    df = df.dropna()
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        df = df.sort_values('date').reset_index(drop=True)
    
    # Ensure numeric columns
    for col in ['quantity', 'price', 'sales']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna()
    return df

def get_kpis(df):
    """Calculate Key Performance Indicators"""
    kpis = {
        'total_sales': df['sales'].sum() if 'sales' in df.columns else 0,
        'avg_sales': df['sales'].mean() if 'sales' in df.columns else 0,
        'max_sales': df['sales'].max() if 'sales' in df.columns else 0,
        'total_orders': len(df),
        'unique_products': df['product'].nunique() if 'product' in df.columns else 0,
        'unique_regions': df['region'].nunique() if 'region' in df.columns else 0,
        'unique_categories': df['category'].nunique() if 'category' in df.columns else 0,
    }
    return kpis

def get_summary_stats(df):
    """Get statistical summary"""
    return df.describe()