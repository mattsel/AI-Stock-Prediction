# AI-Stock-Prediction

Within this program, the user can select a stock with an interactive interface and be presented with a stock prediction using a linear regression model. 
This program's data is held and maintained using MongoDB to sort collections and stock data.
This program was built using the following technologies: Python, MongoDB, Sklearn, Pandas, and Plotly.
My primary motivation for this project was to get a look into the realm of Artificial Intelligence as well as the use of non-relational databases.

Starting, the user can enter a stock's ticker symbol as input, which is then searched for using dictionaries and queries to aggregate the data appropriately.

<img width="364" alt="Screenshot 2024-05-04 at 8 09 39 PM" src="https://github.com/mattsel/AI-Stock-Prediction/assets/141775337/5989ccf8-57d9-4514-ad6f-6307e64d48af">


Following this, the program will then utilize the data collected from the S&P 500 Index to split the data for training vs testing with an 80% ratio. 

<img width="485" alt="Screenshot 2024-05-04 at 8 00 38 PM" src="https://github.com/mattsel/AI-Stock-Prediction/assets/141775337/a1547261-de56-48c3-8606-eca9c18e003a">


After allowing the program to both train and predict the values of the stock, the data is then aggregated to be visualized using plotly.

<img width="777" alt="Screenshot 2024-05-04 at 8 05 53 PM" src="https://github.com/mattsel/AI-Stock-Prediction/assets/141775337/4888a55f-a41a-42a3-afe1-342e30aeb42a">


With this addition, not only is the data displayed from the predicted values, but also the actual values of the stock's performance during this time. 
This is important because it allows the user to visualize the data, and they can also use the Mean Square Error of the stock prediction to justify this regression model's accuracy.

