# Calculate percent flu-infected cells IFN+

Analyzes flow cytometry data to calculate the percent of flu-infected cells that are IFN+.
Also uses Uninfected negative control and Sendai-infected positive control.

Subdirectory [2018-09-07_flow_data](2018-09-07_flow_data) has Alistair's flow data after FlowJo processing.

The Python Jupyter notebook [analyze_flow.ipynb](analyze_flow.ipynb) processes these data to create the plot [flow_plot.pdf](flow_plot.pdf) and the file [ifn_stats.csv](ifn_stats.csv).

The R Jupter notebook [analyze_IFNpercent.ipynb](analyze_IFNpercent.ipynb) uses [ifn_stats.csv](ifn_stats.csv) to make a simple summary plot [ifn_percent.pdf](ifn_percent.pdf).
