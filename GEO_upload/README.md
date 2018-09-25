# Upload data to GEO

This directory contains the code that uploads the data to the [GEO database](https://www.ncbi.nlm.nih.gov/geo/) according to the [instructions here](https://www.ncbi.nlm.nih.gov/geo/info/seq.html#metadata).

The steps are:

 1. The current GEO metadata Excel document was downloaded [from here](https://www.ncbi.nlm.nih.gov/geo/info/examples/seq_template_v2.1.xls). This document was then manually converted from `*.xls` to `*.xlsx` format and manually filled with all information about the experiment and the name of the processed and raw data files. In addition, the example spreadsheets in the document were removed. However, the MD5 checksums were **not** added. This manually filled Excel document was saved as [metadata_template.xlsx](metadata_template.xlsx).

 2. The Jupyter notebook [submit_to_GEO.ipynb](submit_to_GEO.ipynb) was created to add the MD5 checksums, collect the files into a subdirectory, and submit them to GEO. That notebook is well documented, so see it for detailed explanations. It creates the file [metadata.xlsx](metadata.xlsx), which is a version of [metadata_template.xlsx](metadata_template.xlsx) with all of the MD5 checksums added. It then performs the FTP upload. See the notebook for details.


