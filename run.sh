#!/bin/bash
echo "Running bot at $(date)"
source /app/container_env.sh
/usr/local/bin/python /app/hacktivity_monitor.py
echo "Finished at $(date)"

