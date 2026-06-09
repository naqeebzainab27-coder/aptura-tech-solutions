import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

NEON_COLORS = ['#00f2fe', '#a855f7', '#4facfe', '#f093fb', '#f5576c', '#43e97b', '#fa709a', '#fee140']

def common_layout(fig, title):
    """Apply common futuristic layout"""
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='#00f2fe'), x=0.5),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(10,10,31,0.3)',
        font=dict(color='white', family='Arial'),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def plot_sales_trend(daily):
    """Beautiful sales trend with neon glow"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily['date'], y=daily['sales'],
        mode='lines+markers',
        line=dict(color='#00f2fe', width=3, shape='spline'),
        marker=dict(size=8, color='#a855f7', line=dict(width=2, color='#00f2fe')),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 254, 0.15)',
        name='Sales',
        hovertemplate='<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>'
    ))
    return common_layout(fig, '📈 Sales Trend Over Time')

def plot_forecast(daily, forecast):
    """Combined historical + forecast chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily['date'], y=daily['sales'],
        mode='lines', name='Historical',
        line=dict(color='#00f2fe', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 254, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast['date'], y=forecast['predicted_sales'],
        mode='lines+markers', name='Forecast',
        line=dict(color='#a855f7', width=4, dash='dash'),
        marker=dict(size=6, color='#f093fb')
    ))
    
    return common_layout(fig, '🔮 AI Sales Forecast')

def plot_category_pie(df):
    """Donut chart for categories"""
    cat_sales = df.groupby('category')['sales'].sum().reset_index()
    fig = go.Figure(data=[go.Pie(
        labels=cat_sales['category'],
        values=cat_sales['sales'],
        hole=0.6,
        marker=dict(colors=NEON_COLORS, line=dict(color='#0a0a1f', width=3)),
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    return common_layout(fig, '🛍️ Sales Distribution by Category')

def plot_region_bar(df):
    """Horizontal bar chart for regions"""
    reg_sales = df.groupby('region')['sales'].sum().reset_index().sort_values('sales')
    fig = go.Figure(data=[go.Bar(
        x=reg_sales['sales'], y=reg_sales['region'],
        orientation='h',
        marker=dict(
            color=reg_sales['sales'],
            colorscale=[[0, '#00f2fe'], [0.5, '#4facfe'], [1, '#a855f7']],
            line=dict(color='#ffffff', width=1)
        ),
        text=reg_sales['sales'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>'
    )])
    return common_layout(fig, '🌍 Sales by Region')

def plot_heatmap(df):
    """Sales heatmap by weekday and month"""
    df_copy = df.copy()
    df_copy['month'] = df_copy['date'].dt.month_name()
    df_copy['weekday'] = df_copy['date'].dt.day_name()
    
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = df_copy.pivot_table(index='weekday', columns='month', values='sales', aggfunc='sum').reindex(weekday_order)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=[[0, '#0a0a1f'], [0.5, '#4facfe'], [1, '#f093fb']],
        hovertemplate='<b>%{y} - %{x}</b><br>Sales: $%{z:,.0f}<extra></extra>'
    ))
    return common_layout(fig, '🔥 Sales Heatmap (Weekday × Month)')

def plot_top_products(df, n=10):
    """Top products bar chart"""
    top = df.groupby('product')['sales'].sum().nlargest(n).reset_index().sort_values('sales')
    fig = go.Figure(data=[go.Bar(
        x=top['sales'], y=top['product'],
        orientation='h',
        marker=dict(color=top['sales'], colorscale='Plasma'),
        text=top['sales'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    )])
    return common_layout(fig, f'🏆 Top {n} Products')

def plot_monthly_sales(df):
    """Monthly sales bar chart"""
    df_copy = df.copy()
    df_copy['month_year'] = df_copy['date'].dt.to_period('M').astype(str)
    monthly = df_copy.groupby('month_year')['sales'].sum().reset_index()
    
    fig = go.Figure(data=[go.Bar(
        x=monthly['month_year'], y=monthly['sales'],
        marker=dict(
            color=monthly['sales'],
            colorscale=[[0, '#00f2fe'], [1, '#a855f7']],
            line=dict(color='white', width=1)
        ),
        text=monthly['sales'].apply(lambda x: f'${x/1000:.1f}K'),
        textposition='outside'
    )])
    return common_layout(fig, '📅 Monthly Sales Performance')