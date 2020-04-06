# dsa

## Homework 2
### Data Structures and Algorithms, September 2019

#### Imperial College Business School

In the first "main" part of the assignment, you'll practice your skills on looping, lists, and functions in the context of analysing stock prices. The second "honours" part involves more challenging computational puzzles.

There are four questions in the assignment.

The assignment is due on Monday 7 October.

Declaration
In submitting this assignment, you agree to the following declaration:

"I certify that my submission is entirely my own unaided work, and that I have read and complied with the College’s guidelines on plagiarism and referencing as set out on the College website.

I understand that the College may make use of plagiarism detection software and that my work may therefore be stored on a database and compared to others' work and other sources."

Where plagiarism is suspected, a formal investigation may be carried out under the College's disciplinary procedures. Plagiarism may result in penalties ranging from mark deduction to expulsion from the College.

Submission
You can find the skeleton code for the assignment in the file hw02.py.

When you're ready to submit the assignment, use the command

python ok --submit
You may submit more than once before the deadline; only the final submission will be graded.

Note. You can test your solutions with python ok commands as specified below. Note that these tests are not comprehensive and we may use different tests when grading your assignment. This means that passing all the tests before submitting does not guarantee a perfect grade. Be careful that your code works not just for a specific test case but in general.

Using OK
We use a program called OK for assignment feedback. You should have OK in the starter files downloaded for this assignment. To use OK to test a specified function, run the following command:

python ok -q function_name
By default, only tests that did not pass will show up. You can use the -v option to show all tests, including tests you have passed:

python ok -q function_name -v
Main part: Trading based on technical analysis
Some stock traders vouch for so-called "technical analysis": using mathematics and statistics to predict stock-price movements from historical data.

Others say that this is like driving a car by only looking at the rear-view mirror.

You will build a trading strategy based on technical analysis of stock prices and explore which group is right.

The technical analysis idea we'll study is using so-called moving-average strategies. A moving average is defined as follows. Consider a daily quoted time series of a stock price,  pt , eg the daily adjusted closing prices for the stock. An  n -step (or  n -lag) moving average is the average of the  n  last values of the price. More precisely, the  n -step moving average is defined as follows

MAn(t)=pt+pt−1+...+pt−(n−1)n.
 
The one-step MA is simply the current price:  MA1(t)=pt , and the two-step MA is the average of the current price and the previous day's price. Tf the moving average span  n  is short, the MA reacts quickly to any shocks to the stock price. If the span  n  is long, it reacts slowly. If the moving average spans the stock's entire period of existence, it is just the all-time average price.

The figure below shows an example of the Nasdaq index's development, along with two different moving averages. Notice how the two-step moving average follows the index more closely than the five-step one, which reacts to price changes more slowly and less strongly.

Nasdaq moving averages

A theory put forward by proponents for technical analysis has it that moving averages give an indication of the "momentum" of a price. In particular, by comparing two moving averages of different lengths, one should be able to infer that the momentum of a the stock is changing, giving a signal when to buy or sell the stock.

This comparison between two moving averages is done by finding so-called crossover points between different moving averages. This works as follows:

We keep track of two moving averages of different lengths: a shorter one (a lower lag  nL , eg  nL=2  in the figure) and a longer one (higher lag  nH , eg  nH=5  in the figure)
When the shorter MA "crosses" the longer one (it has been lower but becomes higher), this is a signal to buy the stock as it seems to be gaining momentum. In the figure, these points are the ones where the green line has been lower than the red line but then crosses it to become higher, eg around 29 June. More specifically, these are defined as follows. If for any time  t ,  MAnH(t−1)≥MAnL(t−1)  and  MAnL(t)>MAnH(t) , you should buy the stock.
Conversely, when the longer MA "crosses" the shorter one in the same way, this is a signal to sell the stock as it seems to be losing momentum. In the figure, these are the points in time where the red line has been lower than the green one, but then becomes higher, eg around 10 June.
Inspecting the figure, it looks like those dates may indeed have been good times to trade. But in general, can you make money based on such strategies? Your task is to evaluate this claim by writing a Python script that calculates two moving averages of a (historical) stock/index price, finds all the crossover points, and finally performs trades based on those points.

Some advocates of technical analysis claim, for example, that by looking at the 20-day and 50-day moving averages of a stock price, one can identify longer trends and benefit from them. Let's create a trading strategy to this idea.

Question 1: Moving average
Complete the function moving_average in hw02.py. The function should take as input a list of prices and the step  n , and return the  n -step moving average as a list, calculated using the formula above. We cannot calculate the moving average for the first  n−1  steps so these values in the list should be set to None. For example, a three-step moving average can only be calculated for the third price, so there would be two None values in the beginning of the list.

Please do not use Python libraries such as numpy or pandas for calculating moving averages (but you may want to use the sum function on a list).

You can test your function with

python ok -q moving_average -v
Question 2: Crossover points
Complete the function cross_overs in hw02.py. The function takes as input two lists (of moving averages of prices) and returns a list of their crossover points. Each item in the returned list is itself a list containing two integers: [time_index, higher_index], where

time_index is the index at which the crossover happens
higher_index indicates which moving average "crosses over", ie becomes higher at time_index. The value of higher_index should be 1 if this is the first list or 2 for the second list.
The moving averages as defined above will be lists with some None values in the beginning. Your function should start making comparisons at the point in time where both moving averages have numerical values instead of None-values as described above.

You can test your function with

python ok -q cross_overs -v
Question 3: Trading strategy
Complete the function make_trades in hw02.py. The function takes as input an initial cash position (a float), a list of prices, and a list of crossovers as described above. It uses these data to make trades at crossover points as follows.

Start out with initial cash position. Look for the first crossover with an indication to buy stock.
For any crossover [time_index, higher_index], assume that whenever higher_index == 1, this is an indication to buy, and 2 is an indication to sell at this time_index.
If at a given time_index is an indication to buy, AND you have a cash position, use all cash to buy stock at the current price. You will then hold stock only, and zero cash. You may assume that whenever a crossover happens, you're able to make a trade at the current day's price, without waiting for the next day.
If you hold stock, the value of your position fluctuates with the value of the stock price. You look for the next crossover which gives an indication to sell stock.
If there is an indication to sell AND you have a stock position, convert all stock to cash at the current stock price.
As a result, you will always either hold cash or hold stock, but never both. If you hold cash, the value of your position stays constant.
Assume you can buy fractional amounts of stocks, and there are no trading fees.
You can test your function with

python ok -q make_trades -v
"Honours" part: Problem-solving practice
NB: these exercises are more involved algorithm-design challenges. I recommend in each case starting with pen and paper and thinking about how to approach the problem with different inputs before starting to code.

Question 4: Palindromes
Complete the function palindrome in hw02.py. The function takes two arguments: an integer in string form, for example '1921', and an integer k, for example 2. The function returns the largest possible palindrome integer that one can find by changing at most k digits of the input number to any other digit 0-9. A palindrome is the same number read backwards.

For example, with at most two changes to 1921, the largest possible palindrome number is 1991 (with one change 2 -> 9). If we had three changes, we would get from 1921 to 9999, the highest possible integer value with four digits.

Note that test cases could have thousands of digits.

To test your function with ok, run

python ok -q palindrome -v
