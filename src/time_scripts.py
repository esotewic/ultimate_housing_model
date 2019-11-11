from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from epiweeks import Week
from statsmodels.tools.eval_measures import rmse

# Dividing data set for further analysis
def forecasting_datasets_setup(master):
    master.CloseDate = master.CloseDate.apply(lambda x: pd.to_datetime(x))
    master = master[master['CloseDate']<'2019-09-30']
    master = master[master['CloseDate']>'2015-12-31']

    # create datasets of different property types
    sfr_master = master[master.PropertySubType=='Single Family Residence']
    condo_master = master[master.PropertySubType=='Condominium']
    town_master = master[master.PropertySubType=='Townhouse']

    # create dataset with only santa monica zipcodes
    sm_data = master[(master.PostalCode==90401)|
                     (master.PostalCode==90405)|
                     (master.PostalCode==90404)|
                     (master.PostalCode==90403)|
                     (master.PostalCode==90402)]

    # create dataset with only beverly hills zipcodes
    bh_data = master[(master.PostalCode==90210)|
                     (master.PostalCode==90212)]

    # create dataset with only silverlake zipcodes
    sl_data = master[(master.PostalCode==90039)|
                     (master.PostalCode==90026)]
    return master, sfr_master, condo_master, town_master, sm_data, bh_data, sl_data

# split into daily counts
def day_split_count(df):
    w = df[['CloseDate','ClosePrice']]
    w['ClosePrice'] = w['ClosePrice'].apply(lambda x: np.log(x))
    w['CloseDate']=pd.to_datetime(w.CloseDate).apply(lambda x: '{}-{}-{}'.format(x.year,x.month,x.day))
    w.rename(columns={'ClosePrice':'y','CloseDate':'ds'},inplace=True)
    w=w.groupby('ds').count()
    w.reset_index(inplace=True)
    w['ds'] = w['ds'].apply(lambda x: pd.to_datetime(x))
    return w

# split into weekly counts
def week_split_count(df):
    w = df[['CloseDate','ClosePrice']]
    w['week']=pd.to_datetime(w.CloseDate).apply(lambda x: '{}'.format(x.week))
    w['year']=pd.to_datetime(w.CloseDate).apply(lambda x: '{}'.format(x.year))
    ww = w[['week','year']]
    ww.week=ww.week.apply(int)
    ww.year=ww.year.apply(int)
    ww=ww[ww.week!=53]
    ww['enddate'] = ww.apply(lambda row: pd.to_datetime(Week(row.year, row.week, 'iso').enddate()),axis=1)
    w['ds'] = ww['enddate']
    w=w[['ds','ClosePrice']]
    w.rename(columns={'ClosePrice':'y'},inplace=True)
    w=w.groupby('ds').count()
    w.reset_index(inplace=True)
    w['ds'] = w['ds'].apply(lambda x: pd.to_datetime(x))
    return w

# split into monthly
def time_series_sale_count(df):
    ts = df[['CloseDate','ClosePrice']]
    ts.CloseDate = pd.to_datetime(ts.CloseDate).apply(lambda x: '{}-{}'.format(x.year,x.month))
    ts.CloseDate = pd.to_datetime(ts.CloseDate)
    ts = ts.groupby('CloseDate').count().sort_values('CloseDate')
    ts = ts.reset_index()
    ts.rename(columns={'CloseDate':'ds','ClosePrice':'y'},inplace=True)
    return ts

# fun time plot
def time_plot(df):
    sns.lineplot(x='ds',y='y',data=df)


# Run model and give scoring metric
def prophet_analysis(df,split,freq,changepoints=3):
    train = df.iloc[:split]
    test = df.iloc[split:]

    # m_eval = Prophet(growth='linear')
    m_eval = Prophet(
        growth='linear',
        n_changepoints=changepoints,
        changepoint_range=0.8,
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='additive',
        seasonality_prior_scale=20,
        changepoint_prior_scale=.5,
        mcmc_samples=0,
        interval_width=0.8,
        uncertainty_samples=500,
        ).add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        ).add_seasonality(
            name='yearly',
            period=365.25,
            fourier_order=20
        ).add_seasonality(
            name='quarterly',
            period=365.25/4,
            fourier_order=5,
            prior_scale=15)
    m_eval.fit(train)
    eval_future=m_eval.make_future_dataframe(periods=test.shape[0],freq=freq)
    eval_forecast=m_eval.predict(eval_future)

    fig,axs=plt.subplots(1,1,figsize=(15,4))
    ax1 = sns.lineplot(x='ds',y='yhat',data=eval_forecast,label='Predictions',legend='full')
    ax1 = sns.lineplot(x='ds',y='y',data=train,label='Train True',legend='full',linestyle='-.')
    ax1 = sns.lineplot(x='ds',y='y',data=test,label='Test True',legend='full')

    ax =m_eval.plot(eval_forecast)
    ax = add_changepoints_to_plot(fig.gca(),m_eval,eval_forecast)

    predictions = eval_forecast.iloc[-test.shape[0]:]['yhat'] #grab predictions to compare with test set
    print('MAPE = ' + str((abs(np.array(test.y)-predictions)/(np.array(test.y))).mean()))
    print('RMSE = ' + str(rmse(predictions,test['y'])))
    print('MEAN = ' + str(df.y.mean()))
    return




# train test split
def train_test_split_weekly_analysis(df,split,freq):
    train = df.iloc[:split]
    test = df.iloc[split:]
    # m_eval = Prophet(growth='linear')
    m_eval = Prophet(
        growth='linear',
        n_changepoints=3,
        changepoint_range=0.8,
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='additive',
        seasonality_prior_scale=20,
        changepoint_prior_scale=.5,
        mcmc_samples=0,
        interval_width=0.8,
        uncertainty_samples=500,
        ).add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        ).add_seasonality(
            name='yearly',
            period=365.25,
            fourier_order=20
        ).add_seasonality(
            name='quarterly',
            period=365.25/4,
            fourier_order=5,
            prior_scale=15)
    m_eval.fit(train)
    eval_future=m_eval.make_future_dataframe(periods=test.shape[0],freq=freq)
    eval_forecast=m_eval.predict(eval_future)

    fig,axs=plt.subplots(1,1,figsize=(15,4))
    ax1 = sns.lineplot(x='ds',y='yhat',data=eval_forecast,label='Predictions',legend='full')
    ax1 = sns.lineplot(x='ds',y='y',data=train,label='Train True',legend='full',linestyle='-.')
    ax1 = sns.lineplot(x='ds',y='y',data=test,label='Test True',legend='full',color='red')

#     fig =m_eval.plot(eval_forecast)
#     a = add_changepoints_to_plot(fig.gca(),m_eval,eval_forecast)

    predictions = eval_forecast.iloc[-test.shape[0]:]['yhat'] #grab predictions to compare with test set
    print('MAPE = ' + str((abs(np.array(test.y)-predictions)/(np.array(test.y))).mean()))
    print('RMSE = ' + str(rmse(predictions,test['y'])))
    print('MEAN = ' + str(df.y.mean()))
    return

#     fig =m_eval.plot(eval_forecast)
#     a = add_changepoints_to_plot(fig.gca(),m_eval,eval_forecast)

    predictions = eval_forecast.iloc[-test.shape[0]:]['yhat'] #grab predictions to compare with test set
    print('MAPE = ' + str((abs(np.array(test.y)-predictions)/(np.array(test.y))).mean()))
    print('RMSE = ' + str(rmse(predictions,test['y'])))
    print('MEAN = ' + str(df.y.mean()))
    return


# Put data into weekly increments
def week_split_count_close_price(df):
    w = df[['CloseDate','ClosePrice']]
    w['week']=pd.to_datetime(w.CloseDate).apply(lambda x: '{}'.format(x.week))
    w['year']=pd.to_datetime(w.CloseDate).apply(lambda x: '{}'.format(x.year))
    ww = w[['week','year']]
    ww.week=ww.week.apply(int)
    ww.year=ww.year.apply(int)
    ww=ww[ww.week!=53]
    ww['enddate'] = ww.apply(lambda row: pd.to_datetime(Week(row.year, row.week, 'iso').enddate()),axis=1)
    w['ds'] = ww['enddate']
    w=w[['ds','ClosePrice']]
    w.rename(columns={'ClosePrice':'y'},inplace=True)
    w=w.groupby('ds').count()
    w.reset_index(inplace=True)
    w['ds'] = w['ds'].apply(lambda x: pd.to_datetime(x))
    return w

# Find the average close price of each prop type
def week_split_avg_close_price(df):
    w = df[['CloseDate','ClosePrice']]
    w['week']=pd.to_datetime(w.CloseDate).apply(lambda x: '{}'.format(x.week))
    w['year']=pd.to_datetime(w.CloseDate).apply(lambda x: '{}'.format(x.year))
    ww = w[['week','year']]
    ww.week=ww.week.apply(int)
    ww.year=ww.year.apply(int)
    ww=ww[ww.week!=53]
    ww['enddate'] = ww.apply(lambda row: pd.to_datetime(Week(row.year, row.week, 'iso').enddate()),axis=1)
    w['ds'] = ww['enddate']
    w=w[['ds','ClosePrice']]
    w.rename(columns={'ClosePrice':'y'},inplace=True)
    w=w.groupby('ds').mean()
    w.reset_index(inplace=True)
    w['ds'] = w['ds'].apply(lambda x: pd.to_datetime(x))
    return w


def time_series_mean_data():
    ts = master[['CloseDate','ClosePrice']]
    ts.CloseDate = pd.to_datetime(ts.CloseDate).apply(lambda x: '{}-{}'.format(x.year,x.month))
    ts.CloseDate = pd.to_datetime(ts.CloseDate)
    ts = ts.groupby('CloseDate').mean().sort_values('CloseDate')
    ts = ts.reset_index()
    ts.rename(columns={'CloseDate':'ds','ClosePrice':'y'},inplace=True)
    return ts

def time_plot():
    fig,ax=plt.subplots(figsize=(10,6))
    sns.lineplot(x='ds',y='y',data=ts)
