import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

def forecast_sales(df, periods=30):
    """Forecast future sales using Random Forest"""
    daily = df.groupby('date')['sales'].sum().reset_index()
    daily['day_num'] = np.arange(len(daily))
    
    # Add features
    daily['day_of_week'] = daily['date'].dt.dayofweek
    daily['month'] = daily['date'].dt.month
    daily['day'] = daily['date'].dt.day
    
    X = daily[['day_num', 'day_of_week', 'month', 'day']]
    y = daily['sales']
    
    model = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=10)
    model.fit(X, y)
    
    # Generate future data
    last_date = daily['date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods)
    
    future_df = pd.DataFrame({
        'date': future_dates,
        'day_num': np.arange(len(daily), len(daily) + periods),
        'day_of_week': future_dates.dayofweek,
        'month': future_dates.month,
        'day': future_dates.day
    })
    
    predictions = model.predict(future_df[['day_num', 'day_of_week', 'month', 'day']])
    
    forecast_df = pd.DataFrame({
        'date': future_dates,
        'predicted_sales': predictions.round(2)
    })
    
    return forecast_df, daily

def customer_segmentation(df):
    """Segment data by category"""
    if 'category' in df.columns:
        segments = df.groupby('category').agg(
            total_sales=('sales', 'sum'),
            avg_sales=('sales', 'mean'),
            total_orders=('sales', 'count')
        ).reset_index().sort_values('total_sales', ascending=False)
        return segments
    return None

def top_products(df, n=10):
    """Get top N products"""
    if 'product' in df.columns:
        return df.groupby('product')['sales'].sum().nlargest(n).reset_index()
    return None

def growth_rate(df):
    """Calculate sales growth rate"""
    daily = df.groupby('date')['sales'].sum()
    if len(daily) < 2:
        return 0
    first = daily.iloc[:len(daily)//2].mean()
    second = daily.iloc[len(daily)//2:].mean()
    return ((second - first) / first) * 100 if first > 0 else 0