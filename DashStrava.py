import dash
from dash import dcc
from dash import html
import pandas as pd
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import numpy as np



app = dash.Dash(__name__)


file_path = r'C:\Users\alexb\OneDrive\Documents\Python Scripts\data_dashboard_app\combined_df.csv'
combined_df = pd.read_csv(file_path)

# Calculate the quartiles
quartile_10 = combined_df['Total_Time'].quantile(0.10)
quartile_40 = combined_df['Total_Time'].quantile(0.40)
quartile_70 = combined_df['Total_Time'].quantile(0.70)

# Filter data for each quartile
top_25_data = combined_df[combined_df['Total_Time'] <= quartile_10]
top_50_data = combined_df[(combined_df['Total_Time'] >= quartile_10) & (combined_df['Total_Time'] <= quartile_40)]
top_75_data = combined_df[(combined_df['Total_Time'] > quartile_40) & (combined_df['Total_Time'] <= quartile_70)]
bottom_25_data = combined_df[combined_df['Total_Time'] >= quartile_70]

# Calculate average Pace per lap for each quartile
average_top_25 = top_25_data.groupby('Lap')['Pace'].mean()
average_top_50 = top_50_data.groupby('Lap')['Pace'].mean()
average_top_75 = top_75_data.groupby('Lap')['Pace'].mean()
average_bottom_25 = bottom_25_data.groupby('Lap')['Pace'].mean()

# Define the x values for the spline interpolation
x_new = np.linspace(average_top_25.index.min(), average_top_25.index.max(), 300)

# Create spline objects for each quartile
spline_top_25 = make_interp_spline(average_top_25.index, average_top_25.values, k=3)
spline_top_50 = make_interp_spline(average_top_50.index, average_top_50.values, k=3)
spline_top_75 = make_interp_spline(average_top_75.index, average_top_75.values, k=3)
spline_bottom_25 = make_interp_spline(average_bottom_25.index, average_bottom_25.values, k=3)

# Evaluate the spline functions at the new x values
smoothed_top_25 = spline_top_25(x_new)
smoothed_top_50 = spline_top_50(x_new)
smoothed_top_75 = spline_top_75(x_new)
smoothed_bottom_25 = spline_bottom_25(x_new)


average_data = pd.DataFrame(columns=['Name', 'Average_Pace', 'Average_HR'])



app.layout = html.Div(children=[
    html.H1('Strava Graphs'),
    dcc.Graph(id='pace-graph', figure={
        'data': [
            {'x': average_top_25.index, 'y': average_top_25.values, 'type': 'scatter', 'name': 'Top 25% Avg'},
            {'x': average_top_50.index, 'y': average_top_50.values, 'type': 'scatter', 'name': 'Top 50% Avg'},
            {'x': average_top_75.index, 'y': average_top_75.values, 'type': 'scatter', 'name': 'Top 75% Avg'},
            {'x': average_bottom_25.index, 'y': average_bottom_25.values, 'type': 'scatter', 'name': 'Bottom 25% Avg'},
        ],
        'layout': {
            'title': 'Pace per Lap for Each Runner',
            'xaxis': {'title': 'Lap'},
            'yaxis': {'title': 'Pace'},
            'ylim': [280, 700],
            'xlim': [1, 10],
            'grid': {'color': 'black', 'linestyle': '--', 'linewidth': 0.5},
            'legend': {'x': 0, 'y': 1}
        }
    }),
    dcc.Graph(id='hr-graph', figure={
        'data': [
            {'x': x_new, 'y': smoothed_top_25, 'type': 'scatter', 'name': 'Top 25% Avg'},
            {'x': x_new, 'y': smoothed_top_50, 'type': 'scatter', 'name': 'Top 50% Avg'},
            {'x': x_new, 'y': smoothed_top_75, 'type': 'scatter', 'name': 'Top 75% Avg'},
            {'x': x_new, 'y': smoothed_bottom_25, 'type': 'scatter', 'name': 'Bottom 25% Avg'}
        ],
        'layout': {
            'title': 'HR per Lap for Each Runner',
            'xaxis': {'title': 'Lap'},
            'yaxis': {'title': 'HR'},
            'ylim': [125, 200],
            'xlim': [1, 10],
            'grid': {'color': 'black', 'linestyle': '--', 'linewidth': 0.5},
            'legend': {'x': 0, 'y': 1}
        }
    }),
    dcc.Graph(id='average-graph', figure={
        'data': [
            {'x': average_data['Average_Pace'], 'y': average_data['Average_HR'], 'type': 'scatter', 'mode': 'markers'}
        ],
        'layout': {
            'title': 'Average Pace vs. Average HR',
            'xaxis': {'title': 'Average Pace (sec per mile)'},
            'yaxis': {'title': 'Average HR (bpm)'},
            'ylim': [100, 210],
            'grid': {'color': 'black', 'linestyle': '--', 'linewidth': 0.5},
            'legend': {'x': 0, 'y': 1}
        }
    })
])





if __name__ == '__main__':
    app.run_server(debug=True)