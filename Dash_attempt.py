import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)

# Load data from the CSV file using the full path
file_path = r'C:\Users\alexb\OneDrive\Documents\Python Scripts\data_dashboard_app\combined_df.csv'
combined_df = pd.read_csv(file_path)

app.layout = html.Div([
    html.H1('Graph Page'),
    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(combined_df, x='Lap', y='Pace', title='Distance vs Pace')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)