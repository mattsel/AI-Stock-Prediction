import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# User Input: Enter the CSV file name
user_stock = str(input("Enter your stock name: "))
csv_filename = 'csv/' + user_stock + '.csv'

# Load CSV Data
stock_data = pd.read_csv(csv_filename)

# Set Date to Datetime and sort valuess
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
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

# Print the actual and predicted values side by side
print(result_df.head())

# Plot the actual vs. predicted values with proper date formatting
plt.figure(figsize=(10, 6))
plt.plot(result_df['Date'], result_df['Actual'], label='Actual')
plt.plot(result_df['Date'], result_df['Predicted'], label='Predicted')
plt.title('Actual vs. Predicted Stock Prices')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

# Specify features for future dates
future_dates = pd.date_range(start=split_date + timedelta(days=1), end='2025-01-01', freq='B') 
future_features = pd.DataFrame({'Open': [your_open_value] * len(future_dates),
                                'High': [your_high_value] * len(future_dates),
                                'Low': [your_low_value] * len(future_dates)},
                               index=future_dates)

# Make predictions for future dates
future_predictions = model.predict(future_features)

# Create a DataFrame for future dates and predicted values
future_result_df = pd.DataFrame({'Date': future_dates, 'Predicted': future_predictions})

# Plot the actual vs. predicted values with proper date formatting
plt.figure(figsize=(10, 6))
plt.plot(result_df['Date'], result_df['Actual'], label='Actual')
plt.plot(result_df['Date'], result_df['Predicted'], label='Predicted (Test Set)')
plt.plot(future_result_df['Date'], future_result_df['Predicted'], label='Predicted (Future Dates)', linestyle='--')
plt.title('Actual vs. Predicted Stock Prices')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()