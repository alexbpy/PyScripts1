import pandas as pd
from scipy.interpolate import make_interp_spline
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np




file_path = r'C:\Users\alexb\OneDrive\Documents\Python Scripts\data_dashboard_app\combined_df.csv'
combined_df = pd.read_csv(file_path)


fig, axs = plt.subplots(3, 1, figsize=(8, 12))

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

# Get unique runner names
runners = combined_df['Name'].unique()

# Plot the line plot for each runner's Pace per lap
for i, runner in enumerate(runners):
    runner_data = combined_df[combined_df['Name'] == runner]
    color = (0.8, 0.8, 0.8) if runner not in ['Top 25% Avg', 'Top 50% Avg', 'Top 75% Avg', 'Bottom 25% Avg'] else None
    axs[0].plot(runner_data['Lap'], runner_data['Pace'], color=color, alpha=0.35, linewidth=0.25)


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



axs[0].plot(x_new, smoothed_top_25, color='red', linestyle='-', label='Top 25% Avg', linewidth=2.25)
axs[0].plot(x_new, smoothed_top_50, color='green', linestyle='-', label='Top 50% Avg', linewidth=2.25)
axs[0].plot(x_new, smoothed_top_75, color='blue', linestyle='-', label='Top 75% Avg', linewidth=2.25)
axs[0].plot(x_new, smoothed_bottom_25, color='orange', linestyle='-', label='Bottom 25% Avg', linewidth=2.25)
axs[0].set_xlabel('Lap')
axs[0].set_ylabel('Pace')
axs[0].set_title('Pace per Lap for Each Runner')
axs[0].set_ylim(280, 700)
axs[0].set_xlim(1, 10)
axs[0].grid(True, color='black', linestyle='--', linewidth=0.5)
axs[0].legend()


average_data = pd.DataFrame(columns=['Name', 'Average_Pace', 'Average_HR'])

# Get unique runner names
runners = combined_df['Name'].unique()

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


# Calculate the quartiles
quartile_10 = combined_df['Total_Time'].quantile(0.10)
quartile_40 = combined_df['Total_Time'].quantile(0.40)
quartile_70 = combined_df['Total_Time'].quantile(0.70)

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

# Get unique runner names
runners = combined_df['Name'].unique()

# Plot the line plot for each runner's HR per lap
for i, runner in enumerate(runners):
    runner_data = combined_df[combined_df['Name'] == runner]
    color = (0.8, 0.8, 0.8) if runner not in ['Top 25% Avg', 'Top 50% Avg', 'Top 75% Avg', 'Bottom 25% Avg'] else None
    axs[1].plot(runner_data['Lap'], runner_data['HR'], color=color, alpha=0.35, linewidth=0.25)


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


# Plot the second graph (HR per Lap)
axs[1].plot(x_new, smoothed_top_25, color='red', linestyle='-', label='Top 25% Avg', linewidth=2.25)
axs[1].plot(x_new, smoothed_top_50, color='green', linestyle='-', label='Top 50% Avg', linewidth=2.25)
axs[1].plot(x_new, smoothed_top_75, color='blue', linestyle='-', label='Top 75% Avg', linewidth=2.25)
axs[1].plot(x_new, smoothed_bottom_25, color='orange', linestyle='-', label='Bottom 25% Avg', linewidth=2.25)
axs[1].set_xlabel('Lap')
axs[1].set_ylabel('HR')
axs[1].set_title('HR per Lap for Each Runner')
axs[1].set_ylim(125, 200)
axs[1].set_xlim(1, 10)
axs[1].grid(True, color='black', linestyle='--', linewidth=0.5)
axs[1].legend()

# Plot the third graph (Average Pace per Lap)
axs[2].scatter(average_data['Average_Pace'], average_data['Average_HR'], marker='o')
axs[2].set_xlabel('Average Pace (sec per mile)')
axs[2].set_ylabel('Average HR (bpm)')
axs[2].set_title('Average Pace vs. Average HR')
axs[2].axvline(x=overall_average_pace, color='black', linestyle='-', linewidth='0.8')
axs[2].axhline(y=overall_average_hr, color='black', linestyle='-', linewidth='0.8')
axs[2].set_ylim(100, 210)
axs[2].grid(True)
axs[2].legend()

# Adjust the spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()