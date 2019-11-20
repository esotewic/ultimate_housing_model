# Supervised Machine Learning on Multiple Listing Services Data
ML Home Price Predictive Model on Santa Monica Housing Data

# Premise:
- Buying a home is difficult - hard to understand
- Everyone needs it - you probably know someone who owns a house
- If you own a home or when you do own a home - one of your biggest assets
- Expensive - mortgage and downpayment
- Expensive - Real Estate Agents
- Investment opportunity

# Data:
Data pulled from the MLS(multiple listing services). Data cleaned and extracted into a separate file:
westcoastbestcoast.csv, clean_master.csv

# Objective:
Develop an algorithm to estimate the value of homes in the greater Los Angeles area based on features provided by the MLS.
Find if there is a correlation in the state of the economy and home prices.
Evaluate if the time of year, winter or summer, has an impact on the house prices.
Quantify the effect of certain characteristics of a home have on prices.

# Process:
-Clean Data and EDA
-Feature Engineering
-Train Model
-Evaluate Model


The real estate market is exposed to many fluctuations in prices because of existing
correlations with many variables, some of which cannot be controlled or might even be unknown.
Housing prices can increase rapidly (or in some cases, also drop very fast), yet the numerous listings
available online where houses are sold or rented are not likely to be updated that often.

In other cases, some individuals might be interested in
deliberately setting a price below the market price in order to sell the home faster, for various reasons.

The application is
formally implemented as a regression problem that tries to estimate the market price of a house
given features retrieved from public online listings.

Several machine learning algorithms have been tested

Attending to the figure, we can see some common patterns

Most important factors
driving the value of a house are the size and the location, but there are many other variables that are
often taken into account when determining its value:most notably living area


With such a high variability and unpredictable factors (e.g., one neighborhood deemed better
or more fashionable than others), it is likely that the price of some assets will deviate from its
expected value. When the actual price is much less than the expected value, we could be dealing
with an investment opportunity: an asset that could generate immediate profit if sold soon after its
purchase.

There can be a number of reasons motivating the existence of these investment opportunities,
from which two can be easily identified. The first one can occur when the seller publishes the
advertisement in some online listing. In that case, it could occur that the seller ignored the actual value
of the house. More likely, the house has remained published in the listing for some time, during which
its value has risen (because of global or local trends) but the seller has not updated its value. In the second case, the asset price can be deliberately set lower than its expected value with the intention of it
be sold fast, for example if the seller needs the money.

Whichever the case, investment opportunities in real estate exist and can be identified. In this
paper, we aim at using machine learning techniques to identify such opportunities, by determining
whether the price of an asset is smaller than its estimated value.
