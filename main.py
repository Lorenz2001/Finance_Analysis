import yfinance as yf
import polars as pl
import warnings
import logging 

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


def get_tickers(option = "default", sectors = []):
    """
    Get the list of all the tickers of the stocks.
    Args:
        option (string): Option to get the list of tickers. Default is "default". Others are "wiki" and "sectors".
            - "default": Get the list of all the tickers of the stocks.
            - "wiki": Get the list of all the tickers of the stocks in S&P 500.
            - "sectors": Get the list of all the tickers of the stocks in the specified sectors.
        sectors (list): List of sectors for which the tickers are required. Default is empty list.
    
    Returns:
        list: List of all the tickers of the stocks.
    """
    if option == "default":    
        return yf.Tickers().tickers
    elif option == "wiki":
        # Download the list of S&P 500 companies from Wikipedia
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        table = pd.read_html(url)[0]  # Read the first table from the page
        tickers = table["Symbol"].tolist()  # Extract the tickers
        return tickers
    elif option == "sectors":
        #Check if the sectors are provided
        if len(sectors) == 0:
            warnings.warn("Please provide the sectors. The list passed in get_tickers() is empty.")
            logging.warning("The list passed in get_tickers() is empty.")
            return
        tickers = []
        for sector in sectors:
            stocks = yf.Ticker(sector)
            tickers.extend(stocks.tickers)
    else:
        raise ValueError("Invalid option. Please provide a valid option.")
    return tickers






def get_stock_data(ticker, period = "1d"):
    """
    Given a stock ticker, return the stock data for the given period.
    Args:
        main (string): ticker of the stock
        period (string): period for which the data is required

    Returns:
        float: L'importo totale dopo il periodo specificato.

    Example:
        >>> calcola_interesse(1000, 5, 2)
        1102.5
    """
    
    """
    Given a stock ticker, return the stock data for the given period.

    Parameters
    ----------
    ticker : str {AAPL, MSFT, ...}
        Ticker del titolo azionario.
        You can find the ticker of the stock from Yahoo Finance or with the function get_tickers().
    period : str, optional {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y" "max"}
        Period for which the data is required

    Raises
    ------
    ValueError
        If Ticker is not found or period is not valid.

    Returns
    -------
    pandas.DataFrame
        data

    Examples
    --------
    >>> set_livello("AAPL", "1d")
    This DataFrame contains the historical stock data, with columns typically including:

    Open: The opening price of the stock for each time period.
    High: The highest price of the stock during the time period.
    Low: The lowest price of the stock during the time period.
    Close: The closing price of the stock for each time period.
    Adj Close: The adjusted closing price, accounting for corporate actions like dividends and stock splits.
    Volume: The number of shares traded during the time period.
    
    """
    
    stock = yf.Ticker(ticker)
    data = stock.history(period= period)
    logging.info(f'data of {ticker} for {period} is fetched')
    return data





if __name__ == "__main__":

    # Get the data for the stock AAPL
    data = get_stock_data("AAPL", "max")
    print(data)