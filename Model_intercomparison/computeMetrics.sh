#$ -S /bin/bash
#$ -l h_rt=24:00:00
#$ -q research-r8.q
#$ -l h_rss=8G
#$ -l mem_free=8G
#$ -wd /lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/logs/

# 'barents' / 'ml' / 'nextsim' / 'osisaf' / 'persistence'
forecast="persistence"

# 1 / 2 / 3
lead_time="3"

# 'nextsim' / 'amsr2'
target_grid="amsr2"

# If not forecast='ml', nothing happens
# weights="weights_08031256"
# weights="weights_21021550"
weights="weights_09031047"


# module use /modules/MET/centos7/GeneralModules
module use /modules/MET/rhel8/user-modules/

# module load Python-devel/3.8.7
module load Python/3.10.4

python3 /lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/commonData.py $target_grid
python3 /lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/computeMetrics.py $forecast $lead_time $target_grid $weights