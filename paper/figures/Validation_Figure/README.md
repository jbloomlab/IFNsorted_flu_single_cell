# Validation of mutations associated with IFN

Analyzes flow cytometry and and associated data on how mutations affect IFN induction.

Subdirectory [flow](flow) has Alistair's flow data after FlowJo processing.

The Python Jupyter notebook [analyze_flow.ipynb](analyze_flow.ipynb) processes these data to create plots of the flow cytometry data and write summary stats.
The plots are [SNP_flow_plot.pdf](SNP_flow_plot.pdf) and [del_flow_plot.pdf](del_flow_plot.pdf).
The summary stats are in [ifn_stats.csv](ifn_stats.csv).

The R Jupter notebook [analyze_IFNpercent.ipynb](analyze_IFNpercent.ipynb) uses the summary stats to make a simple summary plot of percent IFN+.
It also analyzes the qPCR data for the deletion-mutant experiment.
