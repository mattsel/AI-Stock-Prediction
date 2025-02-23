import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def train_model(stock_data):
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
    result_html = result_df[['Date', 'Actual', 'Predicted']].head().to_html(index=False)

    return result_html, mse, predictions.tolist(), target_test.tolist(), test_data['Date'].dt.strftime('%Y-%m-%d').tolist()
