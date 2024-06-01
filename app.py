from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load JSON data
with open('./static/data/sales_forecast.json') as f:
    sales_data = json.load(f)

# Convert JSON data to DataFrame for plotting
data = []
for store, dates in sales_data.items():
    for date, sales in dates.items():
        data.append({'Store': store, 'Date': pd.to_datetime(date, format='%d-%m-%y'), 'Sales': sales})

df = pd.DataFrame(data)

def format_sales(sales):
    sales = int(sales)
    if sales >= 1_000_000:
        return f'{sales / 1_000_000:.1f}M'
    elif sales >= 1_000:
        return f'{sales / 1_000:.1f}K'
    else:
        return str(sales)

@app.route('/')
def index():
    stores = list(sales_data.keys())
    return render_template('index.html', stores=stores)

@app.route('/get_dates', methods=['POST'])
def get_dates():
    store = request.form['store']
    dates = list(sales_data[store].keys())
    return jsonify(dates)

@app.route('/get_sales', methods=['POST'])
def get_sales():
    store = request.form['store']
    date = request.form['date']
    sales = sales_data[store][date]
    formatted_sales = format_sales(sales)
    return jsonify(formatted_sales)

@app.route('/plot')
def plot():
    # Create the line plot
    fig = px.line(df, x='Date', y='Sales', color='Store', title='Weekly Sales per Store')
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('plot.html', graph_html=graph_html)


