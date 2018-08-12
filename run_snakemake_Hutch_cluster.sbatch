#!/bin/bash
#SBATCH
#SBATCH -t 120:00:00
snakemake -j 10 --cluster "sbatch -p largenode -c 16 --mem=100000 -t 2-0" --latency-wait 30
