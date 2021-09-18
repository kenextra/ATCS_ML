import pandas as pd

Names = ["Manhattan", "LaGuardia", "JFK"]


def prepare_data(dt):
    dt_str = dt.strftime("%Y-%m-%d")
    pkt = pd.date_range(start=dt_str + ' 00:00:00', end=dt_str + ' 23:59:59', periods=72)
    dff = pd.DataFrame({'pickup_time': pkt})
    dff['pickup_time'] = pd.to_datetime(dff['pickup_time'].dt.strftime("%Y-%m-%d %H"))
    dff['location'] = Names * 24

    dff['timeofday'] = dff.pickup_time.dt.hour
    dff['dayofweek'] = dff.pickup_time.dt.day_name()
    dff['dayofmonth'] = dff.pickup_time.dt.day
    dff['dayofyear'] = dff.pickup_time.dt.dayofyear

    data = dff[['location', 'timeofday', 'dayofweek', 'dayofmonth', 'dayofyear']]
    return dff, data


def display_data(orig_data, predictions):
    orig_data['trip_count'] = predictions
    pickups = orig_data.groupby(by=['pickup_time', ], as_index=False, dropna=False, )['trip_count'].sum()
    pickups.columns = ['pickup_time', 'total_trip']
    pickups = pd.merge(left=orig_data, right=pickups, how='inner', on='pickup_time')
    pickups['fraction'] = pickups.trip_count / pickups.total_trip
    fractions = pickups.pivot(index='pickup_time', columns='location', values='fraction')
    fractions.columns = ['JFK', 'LaGuardia', 'Manhattan']
    return orig_data, fractions
