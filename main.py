import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import timedelta

# CSV File inport
csv_filename = 's&p_5years.csv'  

# Load CSV Data
all_data = pd.read_csv(csv_filename)

# Ask user
selected_stock = str(input("Enter Stock Ticker Symbol: "))

# Filter data for the selected stock
stock_data = all_data[all_data['Name'] == selected_stock]

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

# Print the actual and predicted values side by side
print(result_df.head())

# Plot the actual vs. predicted values with proper date formatting
plt.figure(figsize=(10, 6))
plt.plot(result_df['date'], result_df['Actual'], label='Actual')
plt.plot(result_df['date'], result_df['Predicted'], label='Predicted')
plt.title(f'Actual vs. Predicted Stock Prices for {selected_stock}')
plt.xlabel('date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

# Specify features for future dates
future_dates = pd.date_range(start=split_date + timedelta(days=1), end='2025-01-01', freq='B') 
future_features = pd.DataFrame({'open': [your_open_value] * len(future_dates),
                                'high': [your_high_value] * len(future_dates),
                                'low': [your_low_value] * len(future_dates)},
                               index=future_dates)

# Make predictions for future dates
future_predictions = model.predict(future_features)

# Create a DataFrame for future dates and predicted values
future_result_df = pd.DataFrame({'date': future_dates, 'Predicted': future_predictions})

# Plot the actual vs. predicted values with proper date formatting
plt.figure(figsize=(10, 6))
plt.plot(result_df['date'], result_df['Actual'], label='Actual')
plt.plot(result_df['date'], result_df['Predicted'], label='Predicted (Test Set)')
plt.plot(future_result_df['date'], future_result_df['Predicted'], label='Predicted (Future Dates)', linestyle='--')
plt.title(f'Actual vs. Predicted Stock Prices for {selected_stock}')
plt.xlabel('date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
