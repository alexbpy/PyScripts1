
import pandas as pd
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
from scipy.interpolate import make_interp_spline
from sklearn.linear_model import LinearRegression
import numpy as np
import base64
import plotly.graph_objects as go


#FILE PATH

file_path = r'C:\Users\alexb\OneDrive\Documents\Python Scripts\data_dashboard_app\combined_df.csv'
combined_df = pd.read_csv(file_path)

#INITIALISE DASH
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Get unique runner names
runners = combined_df['Name'].unique()

#MATPLOTLIB GRAPH CODE
fig, ax = plt.subplots()

#CALCULATE SLICES

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


# Create plots for each runner
for i, runner in enumerate(runners):
    runner_data = combined_df[combined_df['Name'] == runner]
    color = 'gray' if runner not in ['Top 25% Avg', 'Top 50% Avg', 'Top 75% Avg', 'Bottom 25% Avg'] else None
    ax.plot(runner_data['Lap'], runner_data['Pace'], label=runner, color=color, linewidth=0.25, alpha=0.35)


ax.plot(x_new, smoothed_top_25, color='red', linestyle='-', label='Top 25% Avg', linewidth=2.25)
ax.plot(x_new, smoothed_top_50, color='green', linestyle='-', label='Top 50% Avg', linewidth=2.25)
ax.plot(x_new, smoothed_top_75, color='blue', linestyle='-', label='Top 75% Avg', linewidth=2.25)
ax.plot(x_new, smoothed_bottom_25, color='orange', linestyle='-', label='Bottom 25% Avg', linewidth=2.25)
ax.set_xlabel('Lap')
ax.set_ylabel('Pace')
ax.set_title('Pace per Lap for Each Runner')
ax.set_ylim(280, 700)
ax.set_xlim(1, 10)
ax.grid(True, color='black', linestyle='--', linewidth=0.5)

# Set the plot title and axis labels
ax.set_title('Pace per Lap for Every Runner')
ax.set_xlabel('Lap')
ax.set_ylabel('Pace')

# Set the plot background color
ax.set_facecolor('white')


fig1,ax1 = plt.subplots()



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


# Create plots for each runner
for i, runner in enumerate(runners):
    runner_data = combined_df[combined_df['Name'] == runner]
    color = 'gray' if runner not in ['Top 25% Avg', 'Top 50% Avg', 'Top 75% Avg', 'Bottom 25% Avg'] else None
    ax1.plot(runner_data['Lap'], runner_data['HR'], label=runner, color=color, linewidth=0.25, alpha=0.35)



# Plot the second graph (HR per Lap)
ax1.plot(x_new, smoothed_top_25, color='red', linestyle='-', label='Top 25% Avg', linewidth=2.25)
ax1.plot(x_new, smoothed_top_50, color='green', linestyle='-', label='Top 50% Avg', linewidth=2.25)
ax1.plot(x_new, smoothed_top_75, color='blue', linestyle='-', label='Top 75% Avg', linewidth=2.25)
ax1.plot(x_new, smoothed_bottom_25, color='orange', linestyle='-', label='Bottom 25% Avg', linewidth=2.25)
ax1.set_xlabel('Lap')
ax1.set_ylabel('HR')
ax1.set_title('HR per Lap for Each Runner')
ax1.set_ylim(120, 200)
ax1.set_xlim(1, 10)
ax1.grid(True, color='black', linestyle='--', linewidth=0.5)

# Set the plot title and axis labels
ax1.set_title('HR per Lap for Every Runner')
ax1.set_xlabel('Lap')
ax1.set_ylabel('HR')

# Set the plot background color
ax1.set_facecolor('white')

fig2,ax2 = plt.subplots()


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
ax2.scatter(average_data['Average_Pace'], average_data['Average_HR'], marker='o')
ax2.set_xlabel('Average Pace (sec per mile)')
ax2.set_ylabel('Average HR (bpm)')
ax2.set_title('Average Pace vs. Average HR')
ax2.axvline(x=overall_average_pace, color='black', linestyle='-', linewidth='0.8')
ax2.axhline(y=overall_average_hr, color='black', linestyle='-', linewidth='0.8')
ax2.set_ylim(100, 210)
ax2.grid(True)


# def mpl_to_plotly(mpl_fig):
#     mpl_fig.canvas.draw()
#     mpl_image = np.frombuffer(mpl_fig.canvas.tostring_rgb(), dtype='uint8')
#     mpl_image = mpl_image.reshape(mpl_fig.canvas.get_width_height()[::-1] + (3,))
#     return go.Figure(data=go.Image(z=mpl_image))

# fig_plotly = mpl_to_plotly(fig)
# fig1_plotly = mpl_to_plotly(fig1)
# fig2_plotly = mpl_to_plotly(fig2)

#APP DETAILS
# app.layout = html.Div(children=[
#     html.H1('Strava Graphs'),
#     dcc.Graph(id='pace-graph', figure=fig_plotly,
#               style={'width': '80%', 'height': '800px', 'margin': 'auto'} ),
#     dcc.Graph(id='hr-graph', figure=fig1_plotly,
#               style={'width': '80%', 'height': '800px', 'margin': 'auto'} ),
#     dcc.Graph(id='av-graph', figure=fig2_plotly,
#               style={'width': '80%', 'height': '800px', 'margin': 'auto'} )
# ])

#APP DETAILS
# app.layout = html.Div(children=[
#     html.H1('Strava Graphs'),
#     dcc.Graph(id='pace-graph', figure=fig),
#     dcc.Graph(id='hr-graph', figure=fig1),
#     dcc.Graph(id='av-graph', figure=fig2)
# ])



import io
import urllib

# Convert matplotlib figure to PNG image
fig.savefig('fig.png')
fig1.savefig('fig1.png')
fig2.savefig('fig2.png')

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
fig1_uri = fig_to_uri(fig1)
fig2_uri = fig_to_uri(fig2)

# Use the base64 strings in your Dash app
app.layout = html.Div(children=[
    html.H1('Strava Graphs'),
    html.Img(src=fig_uri, style={'width': '80%', 'height': '400px'}),
    html.Img(src=fig1_uri, style={'width': '80%', 'height': '400px'}),
    html.Img(src=fig2_uri, style={'width': '80%', 'height': '400px'})
])


#RUN APP
if __name__ == '__main__':
    app.run_server(port=8056, debug=True)
