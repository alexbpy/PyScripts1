import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
import io
import base64


app = Flask(__name__)

# Load data from the CSV file using the full path
file_path = r'C:\Users\alexb\OneDrive\Documents\Python Scripts\data_dashboard_app\combined_df.csv'
combined_df = pd.read_csv(file_path)


@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/plot')
def plot():
    # Create a Matplotlib scatter plot using the DataFrame
    fig, ax = plt.subplots()
    ax.scatter(combined_df['Lap'], combined_df['Pace'])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Pace')
    ax.set_title('Distance vs Pace')

    # Convert the plot to an image
    image = io.BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)
    plot_url = base64.b64encode(image.getvalue()).decode()

    return render_template('index1.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)