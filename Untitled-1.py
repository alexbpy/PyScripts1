import pandas as pd
import plotly.express as px
from flask import Flask, render_template
import plotly.offline as po


app = Flask(__name__)

# Load data from the CSV file using the full path
file_path = r'C:\Users\alexb\OneDrive\Documents\Python Scripts\data_dashboard_app\combined_df.csv'
combined_df = pd.read_csv(file_path)

@app.route('/')
def index():
    # Create a Plotly graph directly using the DataFrame
    graph1 = px.scatter(combined_df, x='Lap', y='Pace', title='Distance vs Pace')
    graph1_html = po.plot(graph1, output_type='div')
    return render_template('index.html', graph1=graph1_html)


if __name__ == '__main__':
    app.run(debug=True)

