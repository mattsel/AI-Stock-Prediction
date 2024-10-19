import os
import pandas as pd
from quart import Quart, render_template, request, redirect, url_for, jsonify
import redis.asyncio as redis
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import plotly.express as px

# Initialize Quart app
app = Quart(__name__, static_url_path='/static')

# Configure caching
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = os.getenv('REDIS_URL')

# Load data
df = pd.read_csv('data/sp_5years.csv')
df['Date'] = pd.to_datetime(df['Date'])

async def get_redis_client():
    client = redis.Redis.from_url(os.getenv('REDIS_URL'))
    return client

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
        # Makes 80 / 20 Split
        split_index = int(0.8 * len(stock_data))
        split_date = stock_data.iloc[split_index]['Date']

        train_data = stock_data[stock_data['Date'] < split_date]
        test_data = stock_data[stock_data['Date'] >= split_date]

        # Seperate models
        features_train = train_data[['Open', 'High', 'Low']]
        target_train = train_data['Close']
        features_test = test_data[['Open', 'High', 'Low']]
        target_test = test_data['Close']

        # Train the model
        model = LinearRegression()
        model.fit(features_train, target_train)

        # Predictions and evaluation
        predictions = model.predict(features_test)
        mse = mean_absolute_error(target_test, predictions)

        result_df = pd.DataFrame({'Actual': target_test, 'Predicted': predictions})
        result_df['Date'] = test_data['Date'].values

        # Plotting
        fig = px.line(result_df, x='Date', y=['Actual', 'Predicted'], labels={'Value': 'Stock Price'})
        plot_div = fig.to_html(full_html=False)

        result_html = result_df.head().to_html()
    except Exception as e:
        print(f"Error in result function: {e}")
        return await render_template('index.html', error_message="Invalid stock symbol entered. Please try again.")

    return await render_template('result.html', result_html=result_html, plot_div=plot_div,
                                 mse=mse, selected_stock=stock_symbol)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
