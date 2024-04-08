import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from scipy.interpolate import make_interp_spline
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import base64
import io
import dash_bootstrap_components as dbc
import dash_table


app = dash.Dash(__name__)


file_path = r'C:\Users\alexb\OneDrive\Documents\Python Scripts\data_dashboard_app\combined_df.csv'
combined_df = pd.read_csv(file_path)


# Get unique runner names
runners = combined_df['Name'].unique()

# Create traces for each runner
traces = []
for i, runner in enumerate(runners):
    runner_data = combined_df[combined_df['Name'] == runner]
    color = 'rgb(204, 204, 204)' if runner not in ['Top 25% Avg', 'Top 50% Avg', 'Top 75% Avg', 'Bottom 25% Avg'] else None
    trace = go.Scatter(
        x=runner_data['Lap'],
        y=runner_data['Pace'],
        mode='lines',
        name=runner,
        line=dict(color=color, width=0.25),
        opacity=0.35
    )
    traces.append(trace)


#FOR SPLICES


#VARIABLES
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

# Create the layout
layout = go.Layout(
    title='Pace per Lap for Each Runner',
    xaxis=dict(title='Lap', ticklen=1),
    yaxis=dict(title='Pace', range=[300, 850]),
    width=600,
    showlegend=False,
    legend=dict(x=0, y=1),
    plot_bgcolor='white',
    hovermode='closest'
)

# Create a list containing the existing traces and additional plots
combined_data = traces + [
    go.Scatter(x=x_new, y=smoothed_top_25, mode='lines', name='Top 25% Avg', line=dict(color='red', width=2.25)),
    go.Scatter(x=x_new, y=smoothed_top_50, mode='lines', name='Top 50% Avg', line=dict(color='green', width=2.25)),
    go.Scatter(x=x_new, y=smoothed_top_75, mode='lines', name='Top 75% Avg', line=dict(color='blue', width=2.25)),
    go.Scatter(x=x_new, y=smoothed_bottom_25, mode='lines', name='Bottom 25% Avg', line=dict(color='orange', width=2.25))
]



# Create the figure
figure = go.Figure(data=combined_data, layout=layout)



#####


# Create traces1 for each runner
traces1 = []
for i, runner in enumerate(runners):
    runner_data = combined_df[combined_df['Name'] == runner]
    color = 'rgb(204, 204, 204)' if runner not in ['Top 25% Avg', 'Top 50% Avg', 'Top 75% Avg', 'Bottom 25% Avg'] else None
    trace1 = go.Scatter(
        x=runner_data['Lap'],
        y=runner_data['HR'],
        mode='lines',
        name=runner,
        line=dict(color=color, width=0.25),
        opacity=0.35
    )
    traces1.append(trace1)


# Filter data for each quartile
top_25_data_1 = combined_df[combined_df['Total_Time'] <= quartile_10]
top_50_data_1 = combined_df[(combined_df['Total_Time'] >= quartile_10) & (combined_df['Total_Time'] <= quartile_40)]
top_75_data_1 = combined_df[(combined_df['Total_Time'] > quartile_40) & (combined_df['Total_Time'] <= quartile_70)]
bottom_25_data_1 = combined_df[combined_df['Total_Time'] >= quartile_70]


# Calculate average HR per lap for each quartile
average_top_25_1 = top_25_data_1.groupby('Lap')['HR'].mean()
average_top_50_1 = top_50_data_1.groupby('Lap')['HR'].mean()
average_top_75_1 = top_75_data_1.groupby('Lap')['HR'].mean()
average_bottom_25_1 = bottom_25_data_1.groupby('Lap')['HR'].mean()


# Define the x values for the spline interpolation
x_new = np.linspace(average_top_25_1.index.min(), average_top_25_1.index.max(), 300)

# Create spline objects for each quartile
spline_top_25 = make_interp_spline(average_top_25_1.index, average_top_25_1.values, k=3)
spline_top_50 = make_interp_spline(average_top_50_1.index, average_top_50_1.values, k=3)
spline_top_75 = make_interp_spline(average_top_75_1.index, average_top_75_1.values, k=3)
spline_bottom_25 = make_interp_spline(average_bottom_25_1.index, average_bottom_25_1.values, k=3)

# Evaluate the spline functions at the new x values
smoothed_top_25 = spline_top_25(x_new)
smoothed_top_50 = spline_top_50(x_new)
smoothed_top_75 = spline_top_75(x_new)
smoothed_bottom_25 = spline_bottom_25(x_new)


# Create the layout
layout1 = go.Layout(
    title='HR per Lap for Each Runner',
    xaxis=dict(title='Lap', ticklen=1),
    yaxis=dict(title='HR', range=[100,200]),
    width=200,
    showlegend=False,
    legend=dict(x=0, y=1),
    plot_bgcolor='white',
    hovermode='closest'
)


# Create a list containing the existing traces and additional plots
combined_data1 = traces1 + [
    go.Scatter(x=x_new, y=smoothed_top_25, mode='lines', name='Top 25% Avg', line=dict(color='red', width=2.25)),
    go.Scatter(x=x_new, y=smoothed_top_50, mode='lines', name='Top 50% Avg', line=dict(color='green', width=2.25)),
    go.Scatter(x=x_new, y=smoothed_top_75, mode='lines', name='Top 75% Avg', line=dict(color='blue', width=2.25)),
    go.Scatter(x=x_new, y=smoothed_bottom_25, mode='lines', name='Bottom 25% Avg', line=dict(color='orange', width=2.25))
]


figure1 = go.Figure(data=combined_data1, layout=layout1)

######


fig,ax = plt.subplots()


average_data = pd.DataFrame(columns=['Name', 'Average_Pace', 'Average_HR'])


# Plot the line plot for each runner's Pace per lap
for i, runner in enumerate(runners):
    runner_data = combined_df[combined_df['Name'] == runner]

    # Calculate the average pace and average HR for the runner
    average_pace = runner_data['Pace'].mean()
    average_hr = runner_data['HR'].mean()
    

    # Create a new DataFrame for the current runner
    runner_avg_data = pd.DataFrame({'Name': [runner], 'Average_Pace': [average_pace], 'Average_HR': [average_hr]})
    
    # Concatenate the runner's data with the average_data DataFrame
    average_data = pd.concat([average_data, runner_avg_data], ignore_index=True)


    overall_average_pace = average_data['Average_Pace'].mean()
    overall_average_hr = average_data['Average_HR'].mean()

average_data = average_data.dropna()


# Plot the third graph (Average Pace per Lap)
ax.scatter(average_data['Average_Pace'], average_data['Average_HR'], marker='o')
ax.set_xlabel('Average Pace (sec per mile)')
ax.set_ylabel('Average HR (bpm)')
ax.set_title('Average Pace vs. Average HR')
ax.axvline(x=overall_average_pace, color='black', linestyle='-', linewidth='0.8')
ax.axhline(y=overall_average_hr, color='black', linestyle='-', linewidth='0.8')
ax.set_ylim(100, 210)
ax.grid(True)

fig.savefig('fig.png')



# Convert the images to base64 strings
def fig_to_uri(in_fig, close_all=True, **save_args):
    out_img = io.BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

# Convert your matplotlib figures to base64 strings
fig_uri = fig_to_uri(fig)



# Define the app layout
# app.layout = html.Div(children=[
#     html.H1('Strava Graphs'),
#     dcc.Graph(id='pace-graph', figure=figure),
#     dcc.Graph(id='hr_graph', figure=figure1),
#     html.Img(src=fig_uri, style={'width': '80%', 'height': '400px'}),
# ])

app.layout = dbc.Container([
    html.H1('Strava Graphs', className='mb-2', style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='hr_graph', figure=figure1,style={'width': '50%', 'float': 'right', 'height': '580px'})
        ]),
        dbc.Col([
            # html.Img(src=fig_uri, style={'width': '100%', 'height': '400px'})
            html.Img(src=fig_uri,style={'width': '50%'})
        ])
    ],
    align='start'),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='pace_graph', figure=figure,style={'width': '100%'})
        ])
    ],align='end'),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in combined_df.columns],
                data=combined_df.to_dict('records'),
                page_size=10,  # we want the table to initially display 10 rows
                style_table={'overflowX': 'auto'}  # for horizontal scroll
            )
        ])
    ])
], fluid=False)
# Run the app
if __name__ == '__main__':
    app.run_server(port=8052, debug=True)
