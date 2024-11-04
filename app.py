import os
import time
import pandas as pd
from quart import Quart, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import plotly.express as px
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry
from redis.asyncio import Redis
import pickle
import zlib

app = Quart(__name__, static_url_path='/static')

redis = Redis.from_url(os.getenv("REDIS_URL"), ssl_cert_reqs=None)
MONGODB_CONNECTION_STRING = os.getenv('CONNECTION_STRING')
mongo_client = MongoClient(MONGODB_CONNECTION_STRING)
mongo_db = mongo_client['SP500_Stocks']

registry = CollectorRegistry()
request_counter = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'], registry=registry)
error_counter = Counter('http_errors_total', 'Total number of HTTP errors', ['method', 'endpoint'], registry=registry)
latency_histogram = Histogram('http_request_latency_seconds', 'Histogram of HTTP request latency', ['method', 'endpoint'], registry=registry)

async def fetch_data_from_mongodb(stock_symbol):
    try:
        cached_data = await redis.get(stock_symbol)
        if cached_data:
            df = pickle.loads(zlib.decompress(cached_data))
            return df
        else:
            collection = mongo_db[stock_symbol]
            cursor = collection.find()
            df = pd.DataFrame(list(cursor))
            if not df.empty:
                compressed_df = zlib.compress(pickle.dumps(df))
                await redis.setex(stock_symbol, 60, compressed_df)
            else:
                print("No data found")
            return df
    except Exception as e:
        print(e)


@app.before_request
async def before_request():
    request.start_time = time.time()

@app.after_request
async def after_request(response):
    request_counter.labels(method=request.method, endpoint=request.path).inc()
    latency = time.time() - request.start_time
    latency_histogram.labels(method=request.method, endpoint=request.path).observe(latency)
    return response

@app.errorhandler(Exception)
async def handle_exception(e):
    error_counter.labels(method=request.method, endpoint=request.path).inc()
    return jsonify({"error": "An error occurred"}), 500

@app.route('/', methods=['GET', 'POST'])
async def index():
    error_message = None

    if request.method == 'POST':
        selected_stock = (await request.form)['stock_symbol']

        if selected_stock in mongo_db.list_collection_names():
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
        stock_data = await fetch_data_from_mongodb(stock_symbol)

        if stock_data.empty:
            return await render_template('index.html', error_message="No data found for the selected stock symbol.")

        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        stock_data = stock_data.sort_values(by='Date')

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
        result_df = pd.DataFrame({'Date': test_data['Date'].values, 'Actual': target_test, 'Predicted': predictions})

        fig = px.line(result_df, x='Date', y=['Actual', 'Predicted'], 
                      labels={'value': 'Stock Price', 'variable': 'Price Type'},
                      title=f'Stock Price Prediction for {stock_symbol}')
        plot_div = fig.to_html(full_html=False)

        result_html = result_df[['Date', 'Actual', 'Predicted']].head().to_html(index=False)

    except Exception as e:
        print(f"Error in result function: {e}")
        return await render_template('index.html', error_message="Invalid stock symbol entered. Please try again.")

    return await render_template('result.html', result_html=result_html, plot_div=plot_div,
                                 mse=mse, selected_stock=stock_symbol)

@app.route('/health', methods=['GET'])
async def health_check():
    status = {"status": "healthy"}
    try:
        mongo_client.server_info()
    except Exception as e:
        status['mongodb'] = {"status": "unhealthy", "error": str(e)}

    return jsonify(status), 200 if 'mongodb' not in status else 500

@app.route('/metrics', methods=['GET'])
async def metrics():
    return generate_latest(registry), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
