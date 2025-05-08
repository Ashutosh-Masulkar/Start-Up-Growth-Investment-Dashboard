#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import libraries
import pandas as pd
import plotly.express as px


# In[2]:


# Load dataset
df = pd.read_csv("startup_growth_investment_data.csv")


# In[3]:


# Display first few rows
df.head(100)


# In[4]:


# Get Info
df.info()


# In[5]:


# Get Summary Statistics
df.describe()


# In[6]:


# Check for missing values
missing_values = df.isnull().sum()
missing_values


# In[7]:


# Check for duplicate rows
duplicate_count = df.duplicated().sum()
duplicate_count

# If exist Drop them
df = df.drop_duplicates()


# In[8]:


# List of numerical columns to visualize
num_cols = ["Funding Rounds", "Investment Amount (USD)", "Valuation (USD)", "Number of Investors", "Growth Rate (%)"]

# Generate histograms for each numerical column
for col in num_cols:
    fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}", 
                       labels={col: col}, opacity=0.7, marginal="box")
    fig.show()


# In[1]:


import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Load and clean data
df = pd.read_csv("startup_growth_investment_data.csv")
df.columns = df.columns.str.strip()
df_clean = df.dropna(subset=['Country', 'Industry', 'Growth Rate (%)', 'Year Founded'])

# Options
countries = sorted(df['Country'].dropna().unique())
industries = sorted(df['Industry'].dropna().unique())

# Colors
pastel_palette = ['#1f2323', '#323433', '#3e4444', '#495251', '#5b5f61',
                  '#6f7b7e', '#8b989e', '#99a0a3', '#aab3b5', '#bcc4c6']

# Initialize Dash
app = Dash(__name__)
app.title = "Startup Growth Dashboard"

# Styles
card_style = {
    'backgroundColor': '#d6d4d2',
    'borderRadius': '12px',
    'padding': '20px',
    'marginBottom': '20px',
    'boxShadow': '0px 0px 8px rgba(0, 0, 0, 0.1)'
}
header_style = {'textAlign': 'center', 'color': '#333'}
input_style = {'width': '300px', 'margin': '10px auto', 'color': '#000'}
background_color = '#e3dede'
kpi_style = {
    'textAlign': 'center',
    'color': '#333',
    'backgroundColor': '#828181',
    'padding': '15px',
    'borderRadius': '8px',
    'boxShadow': '0px 0px 5px rgba(0,0,0,0.1)',
    'margin': '10px',
    'width': '30%',
    'display': 'inline-block'
}

# Layout
app.layout = html.Div(style={'backgroundColor': background_color, 'padding': '20px'}, children=[
    html.H1("📊 Startup Growth & Investment Dashboard", style=header_style),

    # KPIs
    html.Div([
        html.Div([
            html.H4("💰 Total Investment (USD)"),
            html.H2(f"{df['Investment Amount (USD)'].sum() / 1e9:.2f}B", style={'color': '#444'})
        ], style=kpi_style),
        html.Div([
            html.H4("🏢 Total Startups"),
            html.H2(df['Startup Name'].nunique(), style={'color': '#444'})
        ], style=kpi_style),
        html.Div([
            html.H4("📈 Avg. Valuation (USD)"),
            html.H2(f"{df['Valuation (USD)'].mean() / 1e9:.2f}B", style={'color': '#444'})
        ], style=kpi_style),
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    # Country-wise Insights
    html.Div([
        html.H3("🌎 Country-wise Startup Insights", style={'color': '#333', 'textAlign': 'center'}),
        dcc.Dropdown(
            id='insight-country',
            options=[{'label': c, 'value': c} for c in countries],
            value=countries[0],
            style=input_style
        ),
        html.Div([
            html.Div([
                html.P("📈 This chart shows how startup growth rate changed over time in the selected country.",
                       style={'textAlign': 'center', 'color': '#444'}),
                dcc.Graph(id='investment-trend')  # Growth over time here
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                html.P("📊 This chart displays the average growth rate of startups across industries in the selected country.",
                       style={'textAlign': 'center', 'color': '#444'}),
                dcc.Graph(id='sector-bar')
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ], style=card_style),

    # Top Countries by Investment
    html.Div([
        html.H3("🌍 Top 10 Countries by Total Investment", style={'color': '#333'}),
        html.P("Explore countries leading in startup investments by filtering industries.",
               style={'textAlign': 'center', 'color': '#444', 'fontSize': '13px', 'marginTop': '-10px'}),
        dcc.Checklist(
            id='industry-filter',
            options=[{'label': i, 'value': i} for i in industries],
            value=industries,
            labelStyle={
                'display': 'inline-block',
                'marginRight': '15px',
                'color': '#000',
                'fontSize': '16px',
                'fontWeight': '500'
            },
            inputStyle={
                "marginRight": "6px",
                "transform": "scale(1.3)",
                "accentColor": "#007BFF"
            },
            style={'textAlign': 'center', 'marginBottom': '10px'}
        ),
        dcc.Graph(id='top-countries-bar')
    ], style=card_style),

    # Treemap and Donut
    html.Div([
        html.Div([
            html.H3("📦 Startup Distribution & Valuation by Sector", style={'color': '#333'}),
            html.P("Switch between startup count and average valuation per sector.",
                   style={'textAlign': 'center', 'color': '#444', 'fontSize': '13px', 'marginTop': '-10px'}),
            dcc.Dropdown(
                id='treemap-country',
                options=[{'label': c, 'value': c} for c in countries],
                value=countries[0],
                style=input_style
            ),
            dcc.RadioItems(
                id='treemap-metric',
                options=[
                    {'label': '📊 Startup Count', 'value': 'count'},
                    {'label': '💵 Average Valuation', 'value': 'valuation'}
                ],
                value='count',
                labelStyle={'display': 'inline-block', 'marginRight': '15px'},
                style={'textAlign': 'center', 'marginBottom': '10px'}
            ),
            dcc.Graph(id='sector-treemap')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            html.H3("🥧 Sector-Wise Investment Share (By Year and Country)", style={'color': '#333'}),
            html.P("Visualizes sector-wise investment share for selected year and country.",
                   style={'textAlign': 'center', 'color': '#444', 'fontSize': '13px', 'marginTop': '-10px'}),
            html.Div([
                dcc.Slider(
                    id='year-slider',
                    min=2000,
                    max=2023,
                    step=1,
                    value=2023,
                    marks={y: str(y) for y in range(2000, 2024, 2)},
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': 'All Countries', 'value': 'All Countries'}] +
                            [{'label': c, 'value': c} for c in countries],
                    value='All Countries',
                    clearable=True,
                    searchable=True,
                    style={'width': '100%', 'color': '#000', 'marginTop': '10px'}
                )
            ]),
            dcc.Graph(id='sector-donut')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ], style=card_style)
])

# ==== Callbacks ====

@app.callback(
    Output('top-countries-bar', 'figure'),
    Input('industry-filter', 'value')
)
def update_top_countries(selected_industries):
    filtered = df[df['Industry'].isin(selected_industries)]
    grouped = filtered.groupby('Country')['Investment Amount (USD)'].sum().reset_index()
    grouped = grouped.sort_values(by='Investment Amount (USD)', ascending=False).head(10)

    fig = px.bar(grouped, x='Investment Amount (USD)', y='Country', orientation='h',
                 color='Country', color_discrete_sequence=pastel_palette)
    fig.update_layout(template='plotly_white', plot_bgcolor='#e3dede',
                      paper_bgcolor='#e3dede', showlegend=False,
                      title='Top 10 Countries by Total Investment')
    return fig

@app.callback(
    Output('investment-trend', 'figure'),
    Output('sector-bar', 'figure'),
    Input('insight-country', 'value')
)
def update_country_insights(selected_country):
    # 📈 Growth Rate Over Time
    growth_trend = df_clean[df_clean['Country'] == selected_country].groupby('Year Founded')['Growth Rate (%)'].mean().reset_index()
    fig_line = px.line(
        growth_trend,
        x='Year Founded',
        y='Growth Rate (%)',
        title=f"📈 Average Growth Rate Over Time – {selected_country}",
        markers=True,
        color_discrete_sequence=['#495251']
    )
    fig_line.update_layout(
        template='plotly_white',
        plot_bgcolor='#e3dede',
        paper_bgcolor='#e3dede',
        showlegend=False
    )

    # 📊 Growth Rate by Industry
    growth = df[df['Country'] == selected_country].dropna(subset=['Growth Rate (%)'])
    growth_grouped = growth.groupby('Industry')['Growth Rate (%)'].mean().reset_index()
    fig_bar = px.bar(growth_grouped.sort_values(by='Growth Rate (%)', ascending=False),
                     x='Industry', y='Growth Rate (%)',
                     color='Industry', color_discrete_sequence=pastel_palette)
    fig_bar.update_layout(
        template='plotly_white',
        plot_bgcolor='#e3dede',
        paper_bgcolor='#e3dede',
        title=f"Average Growth Rate by Industry – {selected_country}",
        showlegend=False
    )

    return fig_line, fig_bar

@app.callback(
    Output('sector-donut', 'figure'),
    Input('year-slider', 'value'),
    Input('country-dropdown', 'value')
)
def update_donut(selected_year, selected_country):
    filtered = df[df['Year Founded'] == selected_year]
    if selected_country != 'All Countries':
        filtered = filtered[filtered['Country'] == selected_country]
    grouped = filtered.groupby('Industry')['Investment Amount (USD)'].sum().reset_index()

    if grouped.empty:
        return px.pie(names=['No data'], values=[1], hole=0.4)

    fig = px.pie(grouped, names='Industry', values='Investment Amount (USD)',
                 hole=0.4, color_discrete_sequence=pastel_palette,
                 title=f"Sector Investment Share – {selected_year} in {selected_country}")
    fig.update_layout(template='plotly_white', plot_bgcolor='#e3dede', paper_bgcolor='#e3dede')
    return fig

@app.callback(
    Output('sector-treemap', 'figure'),
    Input('treemap-country', 'value'),
    Input('treemap-metric', 'value')
)
def update_treemap(selected_country, selected_metric):
    filtered = df[df['Country'] == selected_country].dropna(subset=['Valuation (USD)', 'Startup Name'])

    if selected_metric == 'count':
        grouped = filtered.groupby('Industry').agg({
            'Startup Name': 'count',
            'Valuation (USD)': 'mean'
        }).reset_index().rename(columns={'Startup Name': 'Startup Count'})

        if grouped.empty:
            return px.treemap(names=['No data'], values=[1], title='No data')

        fig = px.treemap(grouped, path=['Industry'], values='Startup Count',
                         color='Startup Count', color_continuous_scale=pastel_palette[::-1],
                         title=f"Startup Count by Sector – {selected_country}")
    else:
        grouped = filtered.groupby('Industry').agg({
            'Valuation (USD)': 'mean'
        }).reset_index()

        if grouped.empty:
            return px.treemap(names=['No data'], values=[1], title='No data')

        fig = px.treemap(grouped, path=['Industry'], values='Valuation (USD)',
                         color='Valuation (USD)', color_continuous_scale=pastel_palette[::-1],
                         title=f"Average Valuation by Sector – {selected_country}")

    fig.update_layout(template='plotly_white', plot_bgcolor='#e3dede', paper_bgcolor='#e3dede')
    return fig

print(f" Dashboard is running locally at: http://127.0.0.1:5555")
# Run the app
# Run
if __name__ == '__main__':
    app.run()



# In[ ]:




