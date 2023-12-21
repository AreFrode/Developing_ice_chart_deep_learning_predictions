import datetime

import seaborn as sns
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt, dates as mdates


def main():
    df = pd.read_csv("/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/CreateFigures/forecast_length_and_contour_resolve/weights_21021550.csv", index_col = 0)

    df.index = pd.to_datetime(df.index)

    one_day = pd.read_csv("/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/CreateFigures/forecast_length_and_contour_resolve/weights_08031256.csv", index_col = 0)
    one_day.index = pd.to_datetime(one_day.index)

    three_day = pd.read_csv("/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/CreateFigures/forecast_length_and_contour_resolve/weights_09031047.csv", index_col = 0)
    three_day.index = pd.to_datetime(three_day.index)

    columns={"target_length": "length", 'target_area1': 'area1', 'target_area2': 'area2', 'target_area3': 'area3', 'target_area4': 'area4', 'target_area5': 'area5', 'target_area6': 'area6'}
    target = df.loc[:, ['target_length', *[f'target_area{i}' for i in range(1,7)]]]
    target['name'] = '1Persistence'
    target = target.rename(columns = columns)

    columns={"forecast_length": "length", 'forecast_area1': 'area1', 'forecast_area2': 'area2', 'forecast_area3': 'area3', 'forecast_area4': 'area4', 'forecast_area5': 'area5', 'forecast_area6': 'area6'}
    forecast = df.loc[:, ['forecast_length', *[f'forecast_area{i}' for i in range(1,7)]]]
    forecast['name'] = 'porecast'
    forecast = forecast.rename(columns = columns)

    one_day_forecast = one_day.loc[:, ['forecast_length']]
    one_day_forecast['name'] = 'one'
    one_day_forecast = one_day_forecast.rename(columns = {"forecast_length": "length"})

    three_day_forecast = three_day.loc[:, ['forecast_length']]
    three_day_forecast['name'] = 'three'
    three_day_forecast = three_day_forecast.rename(columns = {"forecast_length": "length"})

    # bias = pd.DataFrame(forecast.loc[:, 'length'] - target.loc[:, 'length'], columns=['length'])
    
    cat = pd.concat([target, one_day_forecast, forecast, three_day_forecast])

    df_months = cat.groupby([pd.Grouper(freq = 'M'), 'name']).mean()
    df_months = df_months.reset_index(level=['name'])
    df_months.index = df_months.index.map(lambda x: x.replace(day = 1))
    
    # bias_months = bias.groupby(pd.Grouper(freq = 'M')).mean()
    # bias_months.index = bias_months.index.map(lambda x: x.replace(day = 1))


    locator = mdates.YearLocator()
    fmt = mdates.DateFormatter(fmt='%b\n%Y')
    
    minor_locator = mdates.MonthLocator()
    minor_fmt = mdates.DateFormatter(fmt = '%b')

    sns.set_theme()

    fig = plt.figure(figsize = (7.5, 7.5))
    ax = fig.add_subplot()

    line = sns.lineplot(data = df_months, x = df_months.index, y = 'length', hue='name', ax = ax, marker = 'o', color='k', markeredgewidth='1', markersize = '8', mec = None, ls = '--')

    ax.set_xlim([datetime.date(2021, 12, 2), datetime.date(2022, 12, 31)])
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)

    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_minor_formatter(minor_fmt)

    ax.grid(axis = 'x')

    ax.set_title('Sea ice edge length')
    ax.set_ylabel('Ice edge length [km]')
    ax.set_xlabel('Month')

    line.legend_.set_title(None)
    line.legend_.texts[0].set_text('Target')
    line.legend_.texts[1].set_text('One day lead time')
    line.legend_.texts[2].set_text('Two day lead time')
    line.legend_.texts[3].set_text('Three day lead time')

    # df_deep_learning = df_months.loc[df_months['name'] == 'Deep learning']
    # print(bias_months.mean())

    # for i in range(12):
        # ax.text(df_deep_learning.index[i], df_deep_learning['length'].iloc[i] + 150, f"{bias_months['length'].iloc[i]:.0f}")

    plt.savefig('ice_edge_length.pdf', dpi = 300)


if __name__  == "__main__":
    main()
