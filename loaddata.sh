#!/bin/bash
echo "Launching Data Load"
timedatectl
source /home/deployer1/envs/bokehdash352/bin/activate
cd /home/deployer1/BDESDash
python daily_build_table.py
deactivate
timedatectl
echo "done"