def generate_insights(df, forecast):
    """Generate AI-powered insights from data"""
    insights = []
    
    # 1. Trend Analysis
    daily = df.groupby('date')['sales'].sum()
    if len(daily) >= 2:
        first_half = daily.iloc[:len(daily)//2].mean()
        second_half = daily.iloc[len(daily)//2:].mean()
        change = ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
        
        if change > 10:
            insights.append(("🚀 Strong Growth", f"Sales surged by {change:.1f}%! Keep the momentum.", "success"))
        elif change > 0:
            insights.append(("📈 Positive Trend", f"Sales grew by {change:.1f}%. Steady progress!", "success"))
        elif change > -10:
            insights.append(("📊 Stable Period", f"Sales changed by {change:.1f}%. Consider promotions.", "info"))
        else:
            insights.append(("📉 Decline Alert", f"Sales dropped by {abs(change):.1f}%. Review strategy!", "warning"))
    
    # 2. Top Category
    if 'category' in df.columns:
        top_cat = df.groupby('category')['sales'].sum().idxmax()
        top_cat_val = df.groupby('category')['sales'].sum().max()
        insights.append(("🏆 Top Category", f"'{top_cat}' leads with ${top_cat_val:,.0f} in sales.", "success"))
    
    # 3. Top Region
    if 'region' in df.columns:
        top_reg = df.groupby('region')['sales'].sum().idxmax()
        insights.append(("🌟 Best Region", f"'{top_reg}' is your strongest market.", "success"))
    
    # 4. Forecast Insight
    avg_forecast = forecast['predicted_sales'].mean()
    avg_actual = df['sales'].mean()
    if avg_forecast > avg_actual * 1.05:
        insights.append(("🔮 Bright Future", "Forecasted sales above historical average!", "success"))
    elif avg_forecast < avg_actual * 0.95:
        insights.append(("⚠️ Forecast Warning", "Predicted sales below average. Take action!", "warning"))
    else:
        insights.append(("📊 Stable Forecast", "Predicted sales align with historical trends.", "info"))
    
    # 5. Best Day
    if len(daily) > 0:
        best_day = daily.idxmax()
        insights.append(("⭐ Record Day", f"Best sales on {best_day.strftime('%b %d, %Y')}.", "success"))
    
    return insights