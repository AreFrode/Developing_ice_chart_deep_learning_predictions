import pandas as pd
import glob

# from seaborn import apionly as sns
from matplotlib import pyplot as plt
import seaborn as sns

path_1km = "/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/ForecastValidation/lead_time_2/"

files_1km = glob.glob(f"{path_1km}20*/**/*.csv")

df = pd.concat((pd.read_csv(f, index_col='date') for f in files_1km))
df.index = pd.to_datetime(df.index)
df = df.sort_index()
df_m = df.resample('M').mean()

path_10km = "/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/ForecastValidation/lead_time_2/persistence_10km.csv"
df_10 = pd.read_csv(path_10km, index_col = 'date')
df_10.index = pd.to_datetime(df_10.index)
df_10_m = df_10.resample('M').mean()

sns.set_theme(context='talk')
fig, ax = plt.subplots(figsize = (10,6))
df_m['NIIEE_2'].plot(ax = ax, color = 'r')

df_10_m['NIIEE_2'].plot(ax = ax, color = 'b')
ax.set_ylabel('Ice edge displacement error [km]')

ax.xaxis.grid(False)

ax.legend(['nIIEE 1km resolution', 'nIIEE 10km resolution'])

fig.savefig("/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/ForecastValidation/Forecasts/figures/nIIEE_compare.pdf")
