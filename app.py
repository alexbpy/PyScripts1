from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(r'C:\Users\alexb\OneDrive\Documents\Python Scripts\templates\index.html')

@app.route('/update_table', methods=['POST'])
def update_table():
    line_id = int(request.form['line_id'])
    x_data = np.linspace(0, 10, 100)
    y_data = np.sin(x_data) if line_id == 1 else np.cos(x_data)

    data = [{'x': x, 'y': y} for x, y in zip(x_data, y_data)]

    return {'data': data}

if __name__ == '__main__':
    app.run(debug=True)
 