import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import matplotlib.pyplot as plt

# Load environment variables from a .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Create a Flask app
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['MONGO_URI_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize PyMongo with your Flask application
mongo = PyMongo(app)
database = mongo.db['AI-Stock-Prediction']
collection = database['Stock-Collection']

# Function to fetch historical stock data for a given symbol from MongoDB
def get_stock_data_from_mongodb(symbol):
    # Connect to MongoDB and fetch data for the given symbol
    query = {'Name': symbol}
    stock_data = list(collection.find(query))

    # Convert the data to a Pandas DataFrame
    stock_df = pd.DataFrame(stock_data)

    return stock_df

@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = None

    if request.method == 'POST':
        selected_stock = request.form['stock_symbol']

        # Fetch historical stock data for the selected stock symbol from MongoDB
        stock_data = get_stock_data_from_mongodb(selected_stock)

        # Set Date to Datetime and sort values
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        stock_data = stock_data.sort_values(by='date')

        # Calculate the split date based on the 80% mark
        split_index = int(0.8 * len(stock_data))
        split_date = stock_data.iloc[split_index]['date']

        # Split the data into training and testing sets based on date
        train_data = stock_data[stock_data['date'] < split_date]
        test_data = stock_data[stock_data['date'] >= split_date]

        # Features and target for training set
        features_train = train_data[['open', 'high', 'low']]
        target_train = train_data['close']

        # Features and target for testing set
        features_test = test_data[['open', 'high', 'low']]
        target_test = test_data['close']

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
        result_df['date'] = test_data['date'].values

        # Plot the actual vs. predicted values with proper date formatting
        plt.figure(figsize=(10, 6))
        plt.plot(result_df['date'], result_df['Actual'], label='Actual')
        plt.plot(result_df['date'], result_df['Predicted'], label='Predicted')
        plt.title(f'Actual vs. Predicted Stock Prices for {selected_stock}')
        plt.xlabel('date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()

        result_html = result_df.head().to_html()

    return render_template('index.html', result_html=result_html)

if __name__ == '__main__':
    app.run(debug=True)
