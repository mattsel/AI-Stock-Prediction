# AI-Stock-Prediction

Within this program, the user can select a stock with an interactive interface and be presented with a stock prediction using a linear regression model. 
This program's data is held and maintained using MongoDB to sort collections and stock data.
This program was built using the following technologies: Python, MongoDB, Sklearn, Pandas, and Plotly.
My primary motivation for this project was to get a look into the realm of Artificial Intelligence as well as the use of non-relational databases.

To start, the application was defined with a function to handle stock data queries using with the help of the python library, PyMongo.

```python
# Function to fetch historical stock data for a given symbol from MongoDB
def get_stock_data_from_mongodb(symbol):
    query = {'Name': symbol}
    stock_data = list(collection.find(query))
    stock_df = pd.DataFrame(stock_data)
    return stock_df
```

After the user has made a query on a stock ticker symbol, the program will then utilize the data collected from the S&P 500 Index to split the data for training vs testing with an 80% ratio. 

```python
        # Set Date to Datetime and sort values
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        stock_data = stock_data.sort_values(by='date')

        # Calculate the split date based on the 80% mark
        split_index = int(0.8 * len(stock_data))
        split_date = stock_data.iloc[split_index]['date']

        # Split the data into training and testing sets based on date
        train_data = stock_data[stock_data['date'] < split_date]
        test_data = stock_data[stock_data['date'] >= split_date]
```

Once the data model has been split into a 20:80 ratio for training and testing data, the program will then create a LinearRegression instance with the help of sklearn, a Python artificial intelligence library.
Following the creation of the Linear Regression instance, the program will then pass through the features train and target train to create a prediction about the data.

```python
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
```

In order to justify the program's stock prediction, there must be some data visualization and statistical values to support the program hypothesis. To do this,
the program will then calculate the mean square error using sklearn's metrics library. This value will help to support that our program stock prediction is accurate. Essentially the lower the mean square error,
the more accurate the stock prediction is because of the minimal error involved in the predictions. Then both of the predicted and actual values are ploted to a chart to help visualize the data's accuracy

```python
# Evaluate the model
        mse = mean_squared_error(target_test, predictions)
        print(f"Mean Squared Error: {mse}")

        # Create a DataFrame for actual and predicted values
        result_df = pd.DataFrame({'Actual': target_test, 'Predicted': predictions})

        # Convert the numeric date values to datetime for visualization
        result_df['date'] = test_data['date'].values

        # Plot the actual vs. predicted values with Plotly
        fig = px.line(result_df, x='date', y=['Actual', 'Predicted'], labels={'Value': 'Stock Price'})
        plot_div = fig.to_html(full_html=False)
```

**Thanks for checking our my AI Stock Prediction Program**

