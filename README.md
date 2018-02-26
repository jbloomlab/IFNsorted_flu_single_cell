# Single-cell sequencing of IFN-sorted influenza-infected cells

## Overview
This is an analysis of single-cell mRNA sequencing of influenza-infected A549 cells that have been enriched for IFN+ cells.

Briefly, A549 cells were infected with A/WSN/1933 influenza virus at a relatively low MOI, aiming for about 30% infected by HA staining.
These A549 cells contained a sortable marker (LNGFRdel) under an IFNbeta promoter.
At 13-hours post-infection, the cells were sorted to enrich for IFN+ ones. 
These enriched IFN+ cells were mixed with some of the ones that did not sort as IFN+, and they were sequenced on the [Chromium 10X platform](https://www.10xgenomics.com/single-cell/).
A control sample infected with the same virus but not MACS sorted was collected and sequenced at 10 hours.

A modest number of non-infected MDCK (canine) cells were also included to enable assessment of mRNA leakage and lsysis.

The virus used was a mix of wildtype and virus with synonymous "barcodes" near the 3' end to help enable identification of co-infection, similar to the approach in [Russell et al (2018)][].
But whereas in that experiment that viral genomes were barcoded only at the end that gives the 3' end of the mRNA, in this experiment they were barcoded at both ends.

This study differs from [Russell et al (2018)][]:

  - The cells were enriched for IFN+, as that study found a very low rate of IFN+ cells.

  - The viral population was passaged at slightly less stringent MOI so it is a bit more IFN-inducing.

  - The MOI and timepoints are different.

  - The canine cells were included to better assess lysis / leakage.

## Publication and data
None at this time.

## Authors
Alistair Russell and [Jesse Bloom](https://research.fhcrc.org/bloom/en.html).

## Organization of analysis
The analysis is performed by a set of Jupyter notebooks that do the following.

### 1. Align and annotate 10X single-cell data to create cell-gene matrix
The Python notebook [align_and_annotate.ipynb][] demultiplexes and aligns the reads, annotates the flu synonymous barcodes, and generates the cell-gene matrix. It requires installation of [cellranger](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger), which performs the demultiplexing and alignment. It also uses custom Python and bash scripts found in the `./scripts/` subdirectory, and requires installation of a few common Python modules. The notebook describes the software versions used. The end result of this notebook is an annotated cell-gene matrix that is stored in `./results/cellgenecounts/`. There are separate matrices for the human cells with flu reads (*humanplusflu*) and the canine reads (*canine*):

    results/cellgenecounts//merged_canine_cells.tsv
    results/cellgenecounts//merged_canine_genes.tsv
    results/cellgenecounts//merged_canine_matrix.mtx
    results/cellgenecounts//merged_humanplusflu_cells.tsv
    results/cellgenecounts//merged_humanplusflu_genes.tsv
    results/cellgenecounts//merged_humanplusflu_matrix.mtx

### 2. Process annotated cell-gene matrix. 
The R notebook [monocle_analysis.ipynb][]

## Input data
The following input data is used by the analyses:

1. The BCL files that contain the deep sequencing data are on the Bloom lab `ngs` directory, and are linked to directly in [align_and_annotate.ipynb][].

2. [./data/flu_sequences/](./data/flu_sequences) contains the influenza genomes for both the wildtype A/WSN/1933 virus and the variants with double synonymous mutations barcoding the end of the mRNAs, as taken from the Bloom lab reverse-genetics plasmids used to grow these viruses.

## Results and Conclusions
The results from the analysis in each notebook are displayed and described in that notebook.

All output from the analyses are written to the `./results/` subdirectory.

[align_and_annotate.ipynb]: align_and_annotate.ipynb
[monocle_analysis.ipynb]: monocle_analysis.ipynb
[Monocle]: http://cole-trapnell-lab.github.io/monocle-release/
[Russell et al (2018)]: https://doi.org/10.7554/eLife.32303
