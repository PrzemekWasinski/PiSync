#!/bin/bash

#Config
NAS="/mnt/the_vault/ComputerScience"
SSD="/mnt/ssd/ComputerScience"
LOG="$HOME/sync_projects.log"

#Check if NAS is reachable
if ping -c 1 -W 1 192.168.0.68 >/dev/null 2>&1; then
    mkdir -p "$SSD"

    #Start
    echo "Starting sync from NAS to SSD" | tee -a "$LOG"

    #Rsync
    rsync -aH --whole-file --progress "$NAS/" "$SSD/"

    #End
    echo "Sync completed" | tee -a "$LOG"
else
    echo "NAS not reachable skipping sync" | tee -a "$LOG"
fi
