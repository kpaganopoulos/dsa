"""

Homework 2

"""

def moving_average(prices, n):
    """
    Calculates n-period moving average of a list of floats/integers.

    Parameters:
        prices: list of values (ordered in time),
        n: integer moving-average parameter

    Returns:
        list with None for the first n-1 values in prices and the appropriate moving average for the rest

    Example use:
    >>> ma = moving_average([2,3,4,5,8,5,4,3,2,1], 3)
    >>> [round(m, 2) if m is not None else None for m in ma]
    [None, None, 3.0, 4.0, 5.67, 6.0, 5.67, 4.0, 3.0, 2.0]
    >>> moving_average([2,3,4,5,8,5,4,3,2,1], 2)
    [None, 2.5, 3.5, 4.5, 6.5, 6.5, 4.5, 3.5, 2.5, 1.5]
    """    
    
    ma = []
    for i in range(len(prices)):
        if i < n - 1:
            ma.append(None) 
        else:
            ma.append(sum(prices[i-(n-1):i+1])/n)
    return ma


def cross_overs(prices1, prices2):
    """ 
    Identify cross-over indices for two equal-length lists of prices (here: moving averages)

    Parameters:
        prices1, prices2: lists of prices (ordered by time)

    Returns:
        list of crossover points

    Each item in the returned list is a list [time_index, higher_index], where:
        - time_index is the crossover time index (when it happends
        - higher_index indicates which price becomes higher at timeIndex: either 1 for first list or 2 for second list
    
    There are no crossovers before both price lists have values that are not None.
    You can start making comparisons from the point at which both have number values.
    
    Example use:
    >>> p1 = [1, 2, 4, 5]
    >>> p2 = [0, 2.5, 5, 3]
    >>> cross_overs(p1, p2)
    [[1, 2], [3, 1]]
    >>> p1 = [None, 2.5, 3.5, 4.5, 4.5, 3.5, 2.5, 1.5, 3.5, 3.5]
    >>> p2 = [None, None, 3.0, 4.0, 4.333333333333333, 4.0, 3.0, 2.0, 3.0, 2.6666666666666665]
    >>> cross_overs(p1, p2)
    [[5, 2], [8, 1]]
    """
    
    crossovers = []
    for i in range(1, len(prices2)): #len(prices1)==len(prices2)
        if prices1[i-1] is not None and prices2[i-1] is not None:
            if prices1[i-1] >= prices2[i-1] and prices2[i] > prices1[i]:
                crossovers.append([i, 2])
            elif prices2[i-1] >= prices1[i-1] and prices1[i] > prices2[i]:
                crossovers.append([i, 1])
    return crossovers


def make_trades(starting_cash, prices, crossovers):
    """
    Given an initial cash position, use a list of crossovers to make trades

    Parameters:
        starting_cash: initial cash position
        prices: list of prices (ordered by time)
        crossovers: list of crossover points on the prices

    Returns:
        list containing current value of trading position (either in stock value or cash) at each time index
    
    Assume each item crossovers[i] is a list [time_index, buy_index]
    Assume that buy_index = 1 means "buy"
    Assume that buy_index = 2 means "sell"

    We buy stock at any time_index where crossover's buy_index indicates 1, and sell at 2.
    In more detail:
        - We want to buy at time_index whenever buy_index = 1 and we currently hold a cash position
            - We buy at the stock price at time_index. We buy with the entire cash position we have and only hold stock
        - We want to sell at time_index when buy_index = 2 and we hold a stock position
            - We sell at the stock price at time_index. We sell our entire stock position and will only hold cash

    Whenever we trade, we buy with our entire cash position, or sell our entire stock position.
    We will therefore always hold either stock or cash, but never both.
    
    Assume we can hold fractional stock quantities, and there are no transaction fees.

    Example use:
    # In the first example, We start with cash 1.0.
    # We hold cash until we buy at index 1 at the price 4. We then hold 0.25 shares. 
    # After that, our portfolio is in stock, so its value fluctuates with the stock price.
    # As the stock price goes from 4 to 6, our portfolio value goes from 1.0 to 1.5.
    # This goes on until we sell at index 3 at the price 5. 
    # Then we hold cash again and the value of the portfolio does not change as it is in cash.
    >>> starting_cash = 1.0
    >>> prices = [2,4,6,5,1]
    >>> cos = [[1, 1], [3, 2]] # not real crossovers, just to illustrate portfolio value when trading
    >>> values = make_trades(starting_cash, prices, cos)
    >>> values 
    [1.0, 1.0, 1.5, 1.25, 1.25]
    >>> starting_cash = 1000.0
    >>> prices = [2,3,4,5,4,3,2,1,6,1,5,7,8,10,7,9]
    >>> cos = [[5, 2], [8, 1], [10, 2], [11, 1], [15, 2]]
    >>> values = make_trades(starting_cash, prices, cos)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 166.67, 833.33, 833.33, 952.38, 1190.48, 833.33, 1071.43]
    >>> prices =[38,21,20,13,7,14,22,23,27,23,44,26,48,32,48,60,70,40,34,35,33]
    >>> crossovers = [[7, 1], [19, 2]]
    >>> money = 100.0
    >>> values = make_trades(money, prices, crossovers)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 117.39, 100.0, 191.3, 113.04, 208.7, 139.13, 208.7, 260.87, 304.35, 173.91, 147.83, 152.17, 152.17]
    """
    import numpy as np
    current_value = []  
    stock_at = 0
    cash = starting_cash
    time_indexes = []
    for t in range(0, len(crossovers)):
        time_indexes.append(crossovers[t][0])
    time_indexes = np.array(time_indexes) # convert to numpy array
    buy_indexes = []
    for t in range(0, len(crossovers)):
        buy_indexes.append(crossovers[t][1])
    buy_indexes = np.array(buy_indexes) # convert to numpy array
    
    for i in range(0,len(prices)):
        if i==0: # we have no buy or sell at i = 0
            added_value = prices[i] 
            current_value.append(cash)  
            continue

        added_value = (prices[i] - prices[i-1])/prices[i-1]
        if (i == time_indexes).any(): # crossover point (buy or sell)
            if (buy_indexes[np.where(time_indexes == i)]) == 1: # buy
                stock_at = cash
                cash = 0 
                current_value.append(stock_at)                                                           
            else: # sell
                if stock_at == 0: # didn't buy at the past
                    cash = current_value[i-1] # i-1 because it didn't change
                    current_value.append(current_value[i-1])
                else: # buy at the past
                    cash = current_value[i-1] + current_value[i-1]*added_value
                    stock_at = 0
                    current_value.append(cash)
        else:
            if cash == 0: # a buy has occured in the past but not now (not sell because cash=0)          
                stock_at = current_value[i-1] + current_value[i-1]*added_value
                current_value.append(stock_at)
            else:
                current_value.append(cash) # a buy or sell has never occured                     
          
    return current_value


def palindrome(s, k):
    """
    Find highest-value palindrome from s with max k digit changes.
    
    Parameters:
        s - an integer in string format
        k - number of changes
        
    Returns:
        highest-value palindrome number in string format; 
        if creating a palindrome is not possible, returns the string 'Not possible.'
    
    Example use:
    >>> palindrome('1921', 2)
    '1991'
    >>> palindrome('1921', 3)
    '9999'
    >>> palindrome('11122', 1)
    'Not possible.'
    >>> palindrome('11119111', 4)
    '91199119'
    """
    
    my_s = []
    for i in range(len(s)):
        my_s.append(s[i]) 
    left_index = 0
    right_index = len(s) - 1
    while left_index < right_index:
        if s[left_index] != s[right_index]: # 1921 (2 --> 9)
            my_s[left_index] = max(s[left_index],s[right_index])
            my_s[right_index] = max(s[left_index],s[right_index])
            k -= 1
        left_index += 1
        right_index -= 1
    if k < 0:
        return 'Not possible.'

    left_index = 0
    right_index = len(s) - 1
    while left_index <= right_index:
        if left_index == right_index:
            if k > 0:
                my_s[left_index] = '9' # 19291
        if s[left_index] < '9':
            if k >= 2 and my_s[left_index] == s[left_index] and my_s[right_index] == s[right_index]: # 1231 (2,3 --> 9)
                my_s[left_index] = '9'
                my_s[right_index] = '9'
                k -= 2
            if k >= 1 and my_s[left_index] != s[left_index] and my_s[right_index] != s[right_index]: # 11119111
                my_s[left_index] = '9'
                my_s[right_index] = '9'
                k -= 1
        left_index += 1
        right_index -= 1

    return ''.join(my_s)
        


    
    
