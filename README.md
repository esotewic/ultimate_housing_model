# Machine Learning Regression on Multiple Listing Services Data
ML Home Price Predictive Model on Santa Monica Housing Data

## Premise:
- Buying a home is difficult - hard to understand
- Everyone needs it - you probably know someone who owns a house
- If you own a home or when you do own a home - one of your biggest assets
- Expensive - mortgage and downpayment
- Expensive - Real Estate Agents
- Investment opportunity

## Data:
Data pulled from the MLS(multiple listing services). Data cleaned and extracted into a separate file:
westcoastbestcoast.csv, clean_master.csv

## Objective:
Develop an algorithm to estimate the value of homes in the greater Los Angeles area based on features provided by the MLS.
Find if there is a correlation in the state of the economy and home prices.
Evaluate if the time of year, winter or summer, has an impact on the house prices.
Quantify the effect of certain characteristics of a home have on prices.

## Process:
- Clean Data and EDA
- Feature Engineering
- Train Model
- Evaluate Model

## EDA
- There is a clear correlation between the size and price of the house
<img src="https://github.com/esotewic/ultimate_housing_model/blob/master/pictures/property_features_pairplot.png">

- Also there are definitive characteristics in the types of propertys and locations

<img src="https://github.com/esotewic/ultimate_housing_model/blob/master/pictures/livingarea_boxplot.png">

- Single Family Homes exhibit a unique behavior when comparing the living areas

<img src="https://github.com/esotewic/ultimate_housing_model/blob/master/pictures/livingarea_lmplot.png">

- Also geographical location exhibits some unique characteristics. Different neighborhoods seem to yield different sale prices.

<img src="https://github.com/esotewic/ultimate_housing_model/blob/master/pictures/sale_price_boxplot_by_zip_code.png">

## Feature Engineering
3 different features were engineered from the CloseDate:
- Age
- Bond10Year
- Winter vs Summer

Create a heatmap to check for multicolinearity:

<img src="https://github.com/esotewic/ultimate_housing_model/blob/master/pictures/date_features_heatmap.png">

# Machine Learning Regression Models
- Linear Regression
- Random Forests
- Gradient Boost 

Linear Regression returned an R2 score of .802
Random Forests returned an R2 score of .805
Gradient Boost returned an R2 score of .865
Neural Net returned an R2 score of .744
