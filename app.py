import os
import random
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo, MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__, static_url_path='/static')
load_dotenv()

# Load the stock data from CSV
df = pd.read_csv('s&p_5years.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Endpoint to get all stock data
@app.route('/api/stocks', methods=['GET'])
def get_all_data():
    data = df.to_dict(orient='records')
    return jsonify(data)

# Endpoint to filter by date
@app.route('/api/stocks/date', methods=['GET'])
def get_data_by_date():
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
def get_data_by_date_range():
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
def index():
    error_message = None
    
    if request.method == 'POST':
        # Handle form submission and redirect to the result page
        selected_stock = request.form['stock_symbol']
        if selected_stock in df['Name'].values:  # Check if the entered stock symbol is valid
            return redirect(url_for('result', stock_symbol=selected_stock))
        else:
            error_message = "Invalid stock symbol entered. Please try again."

    return render_template('index.html', error_message=error_message)

@app.route('/result/<stock_symbol>', methods=['GET'])
def result(stock_symbol):
    result_html = None
    plot_div = None
    mse = None

    try:
        # Fetch historical stock data for the selected stock symbol from the DataFrame
        stock_data = df[df['Name'] == stock_symbol]

        # Set Date to Datetime and sort values
        stock_data = stock_data.sort_values(by='Date')

        # Calculate the split date based on the 80% mark
        split_index = int(0.8 * len(stock_data))
        split_date = stock_data.iloc[split_index]['Date']

        # Split the data into training and testing sets based on date
        train_data = stock_data[stock_data['Date'] < split_date]
        test_data = stock_data[stock_data['Date'] >= split_date]

        # Features and target for training set
        features_train = train_data[['Open', 'High', 'Low']]
        target_train = train_data['Close']

        # Features and target for testing set
        features_test = test_data[['Open', 'High', 'Low']]
        target_test = test_data['Close']

        # Train a simple linear regression model
        model = LinearRegression()
        model.fit(features_train, target_train)

        # Make predictions on the test set
        predictions = model.predict(features_test)

        # Evaluate the model
        mse = mean_squared_error(target_test, predictions)
        print(f"Mean Squared Error: {mse}")

        # Create a DataFrame for actual and predicted values
        result_df = pd.DataFrame({'Actual': target_test, 'Predicted': predictions})

        # Convert the numeric date values to datetime for visualization
        result_df['Date'] = test_data['Date'].values

        # Plot the actual vs. predicted values with Plotly
        fig = px.line(result_df, x='Date', y=['Actual', 'Predicted'], labels={'Value': 'Stock Price'})
        plot_div = fig.to_html(full_html=False)

        result_html = result_df.head().to_html()
    except Exception as e:
        print("Error:", e)
        return render_template('index.html', error_message="Invalid stock symbol entered. Please try again.")

    return render_template('result.html', result_html=result_html, plot_div=plot_div,
                           mse=mse, selected_stock=stock_symbol)

if __name__ == '__main__':
    app.run(debug=True)
