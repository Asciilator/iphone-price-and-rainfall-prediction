import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import yfinance as yf

# Load Nvidia Stock Data
def load_data(ticker="NVDA", start_date="2022-01-01", end_date="2023-01-01"):
    """
    Load stock data from Yahoo Finance for a specified ticker and date range.

    Args:
        ticker (str, optional): The stock ticker symbol to load data for. Defaults to "NVDA".
        start_date (str, optional): The start date for the data (in "YYYY-MM-DD" format). Defaults to "2022-01-01".
        end_date (str, optional): The end date for the data (in "YYYY-MM-DD" format). Defaults to "2023-01-01".

    Returns:
        pd.DataFrame: A pandas DataFrame containing the stock data with 'Date' as index.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['Date'] = stock_data.index
    return stock_data

# Or alternatively, after running the data-retrieval.py file, you can load its resulting CSV file to load the Nvidia Stock Data 

# def load_finance_data_from_csv(filepath):
    """
    Load stock data from a CSV file and parse the 'Date' column as the index.

    Args:
        filepath (str): The file path of the CSV file containing the stock data.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the stock data with 'Date' as index, and columns such as 'Open', 'Close', 'High', 'Low', etc.
    """
#     stock_data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
#     return stock_data

# Load your CSV file according to your filepath and display the data
#     csv_file_path = r'C:\Users\yusuf\OneDrive\LST\Derde jaar\Y3Q1\Signals and systems with python\Python project\Nvidia-stock-price-prediction\nvidia_stock_data.csv'  # Replace with the path to your file
#     stock_data = load_finance_data_from_csv(csv_file_path)


# Display the first few rows of the stock data to show that you actually obtained the data
stock_data = load_data()
print("First few rows of the obtained stock data\n", stock_data.head())

# Moving Average Model
def moving_average_prediction(data, window=5):
    """
    Compute the moving average for the closing prices of the stock over a specified window size.

    Args:
        data (pd.DataFrame): DataFrame containing stock price data with a 'Close' column.
        window (int, optional): The window size for calculating the moving average. Defaults to 5.

    Returns:
        pd.DataFrame: Updated DataFrame with a new column 'Moving_Avg' for the moving average of the 'Close' prices.
    """
    data['Moving_Avg'] = data['Close'].rolling(window=window).mean()
    return data

# Linear Regression Model
def linear_regression_prediction(data):
    """
    Apply a linear regression model to predict stock prices based on the number of days.

    Args:
        data (pd.DataFrame): DataFrame containing stock price data with a 'Close' column.

    Returns:
        pd.DataFrame: Updated DataFrame with a new column 'Linear_Regression_Pred' for predicted stock prices.
    """
    # Prepare the data
    data['Days'] = np.arange(len(data))  # Use the number of days as a feature
    X = data[['Days']]
    y = data['Close']
    
    # Split into training and test set (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict on test set
    y_pred = model.predict(X_test)

    # Evaluate performance using Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Linear Regression Mean Squared Error: {mse}")

    # Add predictions to the data frame
    data['Linear_Regression_Pred'] = np.nan
    data.loc[X_test.index, 'Linear_Regression_Pred'] = y_pred

    return data

# Visualize the Predictions
def visualize_predictions(data):
    """
    Visualize actual stock prices, moving average predictions, and linear regression predictions.

    Args:
        data (pd.DataFrame): DataFrame containing stock price data along with prediction columns.

    Displays:
        Matplotlib Plot: A line plot showing actual prices, moving average, and linear regression predictions.
    """
    plt.figure(figsize=(14, 7))
    
    # Plot actual prices
    plt.plot(data['Date'], data['Close'], label="Actual Prices", color='blue')

    # Plot moving average predictions
    plt.plot(data['Date'], data['Moving_Avg'], label=f"Moving Average (window=5)", color='green')

    # Plot linear regression predictions
    plt.plot(data['Date'], data['Linear_Regression_Pred'], label="Linear Regression Prediction", color='red')

    plt.title("Nvidia Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)

    # Save the plot to your working directory as a PNG file
    plt.savefig("nvidia_stock_price_prediction.png")

    # Display the plot
    plt.show()

# Main function to run everything
def main():
    """
    The main function that orchestrates the stock price prediction process:
    
    1. Load stock data from Yahoo Finance.
    2. Perform moving average prediction.
    3. Perform linear regression prediction.
    4. Visualize the predictions.
    """
    # Load data
    stock_data = load_data()

    # Moving average prediction
    stock_data = moving_average_prediction(stock_data)

    # Linear regression prediction
    stock_data = linear_regression_prediction(stock_data)

    # Visualize the predictions
    visualize_predictions(stock_data)

if __name__ == "__main__":
    main()
