import os
import time
import pandas as pd
from quart import Quart, render_template, request, redirect, url_for, jsonify
import redis.asyncio as redis
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import plotly.express as px
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CollectorRegistry

# Initialize Quart app
app = Quart(__name__, static_url_path='/static')

# Configure caching
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = os.getenv('REDIS_URL')

# Load data
df = pd.read_csv('data/sp_5years.csv')
df['Date'] = pd.to_datetime(df['Date'])

registry = CollectorRegistry()

# Metrics
request_counter = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'], registry=registry)
error_counter = Counter('http_errors_total', 'Total number of HTTP errors', ['method', 'endpoint'], registry=registry)
latency_histogram = Histogram('http_request_latency_seconds', 'Histogram of HTTP request latency', ['method', 'endpoint'], registry=registry)
health_check_gauge = Gauge('app_health', 'Health status of the application', registry=registry)

async def get_redis_client():
    client = redis.Redis.from_url(os.getenv('REDIS_URL'))
    return client

# Request timing middleware
@app.before_request
async def before_request():
    request.start_time = time.time()

@app.after_request
async def after_request(response):
    # Record metrics
    request_counter.labels(method=request.method, endpoint=request.path).inc()
    
    # Calculate and record latency
    latency = time.time() - request.start_time
    latency_histogram.labels(method=request.method, endpoint=request.path).observe(latency)
    
    return response

@app.errorhandler(Exception)
async def handle_exception(e):
    error_counter.labels(method=request.method, endpoint=request.path).inc()
    return jsonify({"error": "An error occurred"}), 500

# Endpoint to get all stock data
@app.route('/api/stocks', methods=['GET'])
async def get_all_data():
    client = await get_redis_client()
    try:
        data = await client.get('all_stock_data')
        if data is None:
            data = df.to_dict(orient='records')
            await client.set('all_stock_data', data, ex=300)
        return jsonify(data)
    except Exception as e:
        print(f"Error caching data: {e}")
        return jsonify({'error': 'Unable to retrieve data'}), 500
    finally:
        await client.aclose()

# Endpoint to filter by date
@app.route('/api/stocks/date', methods=['GET'])
async def get_data_by_date():
    date = request.args.get('date')
    if date:
        filtered_data = df[df['Date'] == date].to_dict(orient='records')
        if filtered_data:
            return jsonify(filtered_data)
        else:
            return jsonify({'error': 'No data for this date'})
    else:
        return jsonify({'error': 'Date parameter is missing'})

# Endpoint to get data through a range
@app.route('/api/stocks/range', methods=['GET'])
async def get_data_by_date_range():
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if start_date and end_date:
        filtered_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].to_dict(orient='records')
        if filtered_data:
            return jsonify(filtered_data)
        else:
            return jsonify({'error': 'No data for this date range'})
    else:
        return jsonify({'error': 'Start or end date parameter is missing'})

@app.route('/', methods=['GET', 'POST'])
async def index():
    error_message = None

    if request.method == 'POST':
        selected_stock = (await request.form)['stock_symbol']
        print(f"Submitted stock symbol: {selected_stock}")

        if selected_stock in df['Name'].values:
            return redirect(url_for('result', stock_symbol=selected_stock))
        else:
            error_message = "Invalid stock symbol entered. Please try again."
            print("Error: Invalid stock symbol.")

    return await render_template('index.html', error_message=error_message)

@app.route('/result/<stock_symbol>', methods=['GET'])
async def result(stock_symbol):
    result_html = None
    plot_div = None
    mse = None

    try:
        stock_data = df[df['Name'] == stock_symbol].sort_values(by='Date')
        split_index = int(0.8 * len(stock_data))
        split_date = stock_data.iloc[split_index]['Date']

        train_data = stock_data[stock_data['Date'] < split_date]
        test_data = stock_data[stock_data['Date'] >= split_date]

        features_train = train_data[['Open', 'High', 'Low']]
        target_train = train_data['Close']
        features_test = test_data[['Open', 'High', 'Low']]
        target_test = test_data['Close']

        model = LinearRegression()
        model.fit(features_train, target_train)

        predictions = model.predict(features_test)
        mse = mean_absolute_error(target_test, predictions)

        result_df = pd.DataFrame({'Actual': target_test, 'Predicted': predictions})
        result_df['Date'] = test_data['Date'].values

        fig = px.line(result_df, x='Date', y=['Actual', 'Predicted'], labels={'Value': 'Stock Price'})
        plot_div = fig.to_html(full_html=False)

        result_html = result_df.head().to_html()
    except Exception as e:
        print(f"Error in result function: {e}")
        return await render_template('index.html', error_message="Invalid stock symbol entered. Please try again.")

    return await render_template('result.html', result_html=result_html, plot_div=plot_div,
                                 mse=mse, selected_stock=stock_symbol)

@app.route('/health', methods=['GET'])
async def health_check():
    health_check_gauge.set(1)
    return jsonify({"status": "healthy"}), 200

@app.route('/metrics', methods=['GET'])
async def metrics():
    return generate_latest(registry), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
