import pandas as pd
import numpy as np
import seaborn as sns

from matplotlib import pyplot as plt

def main():
    PATH_GENERAL = '/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/nextsim_grid/'
    PATH_FIGURES = f"{PATH_GENERAL[:-13]}figures/thesis_figs/"

    ml = []
    ml.append(pd.read_csv(f"{PATH_GENERAL}lead_time_1/weights_08031256.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    ml.append(pd.read_csv(f"{PATH_GENERAL}lead_time_2/weights_21021550.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    ml.append(pd.read_csv(f"{PATH_GENERAL}lead_time_3/weights_09031047.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))

    pers = []
    pers.append(pd.read_csv(f"{PATH_GENERAL}lead_time_1/persistence.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    pers.append(pd.read_csv(f"{PATH_GENERAL}lead_time_2/persistence.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    pers.append(pd.read_csv(f"{PATH_GENERAL}lead_time_3/persistence.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))

    osi = []
    osi.append(pd.read_csv(f"{PATH_GENERAL}lead_time_1/osisaf.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    osi.append(pd.read_csv(f"{PATH_GENERAL}lead_time_2/osisaf.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    osi.append(pd.read_csv(f"{PATH_GENERAL}lead_time_3/osisaf.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))

    nextsim = []
    nextsim.append(pd.read_csv(f"{PATH_GENERAL}lead_time_1/nextsim.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    nextsim.append(pd.read_csv(f"{PATH_GENERAL}lead_time_2/nextsim.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))
    nextsim.append(pd.read_csv(f"{PATH_GENERAL}lead_time_3/nextsim.csv", index_col = 0, usecols = ['date', 'NIIEE_2']))

    tick_labels = ['1-day', '2-day', '3-day']

    common_dates = [pd.concat([ml[i], pers[i], osi[i], nextsim[i]], axis=1, join = 'inner').index.array for i in range(3)]

    for i in range(3):
        ml[i] = ml[i][ml[i].index.isin(common_dates[i])].mean()
        pers[i] = pers[i][pers[i].index.isin(common_dates[i])].mean()
        osi[i] = osi[i][osi[i].index.isin(common_dates[i])].mean()
        nextsim[i] = nextsim[i][nextsim[i].index.isin(common_dates[i])].mean()
    
    ml = np.array(ml).ravel()
    pers = np.array(pers).ravel()
    osi = np.array(osi).ravel()
    nextsim = np.array(nextsim).ravel()
    
    print(f"{ml=}")
    print(f"{np.diff(ml)=}")

    print(f"{pers=}")
    print(f"{np.diff(pers)=}")
    
    print(f"{osi=}")
    print(f"{np.diff(osi)=}")
    
    print(f"{nextsim=}")
    print(f"{np.diff(nextsim)=}")
    # print(np.mean(np.array(ml) / np.array(pers)))

    figname = f"{PATH_FIGURES}model_intercomparisson_leadtime_nextsim.pdf"


    sns.set_theme(context = 'poster')
    sns.set_palette(palette = 'deep')

    fig = plt.figure(figsize = (14, 11.5), constrained_layout = True)
    ax = fig.add_subplot()

 
    ax.plot(ml, '-o', label = 'Deep learning')
    ax.plot(pers, '-o', label = 'Persistence')
    ax.plot(osi, '-o', label = 'OSI SAF linear trend')
    ax.plot(nextsim, '-o', label = 'NeXtSIM')

    ax.set_xticks(np.arange(3), tick_labels)
    ax.set_title('Mean annual forecast error')
    ax.set_ylabel('Ice edge displacement error [km]')
    ax.set_xlabel('Lead time')
    ax.grid(axis = 'x')

    ax.legend()
    fig.savefig(f"{figname}", dpi = 300)


if __name__ == "__main__":
    main()
