"""``snakemake`` file that runs entire analysis.

Written by Jesse Bloom."""


# Imports -----------------------------------------
import os
from os.path import join
import re


# Globals -----------------------------------------

# cell-gene matrices in this directory
CELLGENE_DIR = 'results/cellgenecounts'

# flu sequences in this directory
FLUSEQ_DIR = 'data/flu_sequences'

# PacBio subreads placed in this directory for analysis
SUBREADS_DIR = 'results/pacbio/subreads'

# PacBio CCS reads in this directory
CCS_DIR = 'results/pacbio/ccs'

# PacBio runs and subdirectory with initial subreads files
# are read from file.
PACBIO_RUNS_FILE = 'data/PacBio_runs.csv'
with open(PACBIO_RUNS_FILE) as f:
    PACBIO_RUNS = dict([line.strip().split(',') for line in f])

# paper in this directory
PAPER_DIR = 'paper'
PAPER = 'paper'

# get paper figures made by R and Python notebooks
with open(join(PAPER_DIR, PAPER) + '.tex') as f:
    paper_text = f.read()
# figs from monocle_analysis.ipynb in paper/figures/single_cell_figures
R_FIGS_SUBDIR = 'figures/single_cell_figures/'
R_FIGS = [
        join(PAPER_DIR, R_FIGS_SUBDIR, fig) for fig in re.findall(
        '\{[^\}]*' + R_FIGS_SUBDIR + '([^\}]+)\}',
        paper_text)
        ]
# figs from pacbio_analysis.ipynb in paper/figures/pacbio_single_cell_figures
PYTHON_FIGS_SUBDIR = 'figures/pacbio_single_cell_figures/'
PYTHON_FIGS = [
        join(PAPER_DIR, PYTHON_FIGS_SUBDIR, fig) for fig in re.findall(
        '\{[^\}]*' + PYTHON_FIGS_SUBDIR + '([^\}]+)\}',
        paper_text)
        ]


# Rules ------------------------------------------- 

rule make_paper:
    """Compile LaTex paper describing results."""
    input:
        join(PAPER_DIR, PAPER) + '.tex',
        R_FIGS,
        PYTHON_FIGS,
        join(PAPER_DIR, 'references.bib')
    output:
        join(PAPER_DIR, PAPER) + '.pdf'
    shell:
        """
        cd {PAPER_DIR}
        pdflatex {PAPER}
        bibtex {PAPER}
        pdflatex {PAPER}
        pdflatex {PAPER}
        cd ..
        """


rule analyze_IFN_vs_viral_mutations:
   """Analyze mutations associated with IFN and make paper figures."""
    input:
        join(CELLGENE_DIR, 'PacBio_annotated_merged_humanplusflu_cells.tsv'),
        join(CELLGENE_DIR, 'merged_humanplusflu_genes.tsv'),
        join(CELLGENE_DIR, 'merged_humanplusflu_matrix.mtx'),
        join(CELLGENE_DIR, 'merged_canine_cells.tsv'),
        join(CELLGENE_DIR, 'merged_canine_genes.tsv'),
        join(CELLGENE_DIR, 'merged_canine_matrix.mtx'),
        join(FLUSEQ_DIR, 'flu-wsn.fasta')
    output:
        R_FIGS
    shell:
        """
        jupyter nbconvert \
            --to notebook \
            --execute \
            --inplace \
            --ExecutePreprocessor.timeout=-1 \
            monocle_analysis.ipynb
        jupyter nbconvert monocle_analysis.ipynb --to html
        mv monocle_analysis.html {PAPER_DIR}/{R_FIGS_SUBDIR}
        """


rule call_PacBio_mutations:
    """Call mutations from PacBio CCSs and make some figures."""
    input:
        expand(join(CCS_DIR, '{pacbioRun}_ccs.bam'),
                pacbioRun=PACBIO_RUNS.keys()),
        join(CELLGENE_DIR, 'merged_humanplusflu_cells.tsv'),
        join(FLUSEQ_DIR, 'flu-wsn-mRNA.fasta'),
        join(FLUSEQ_DIR, 'flu-wsn-double-syn-mRNA.fasta'),
        join(FLUSEQ_DIR, 'flu-wsn.gb'),
        'data/images/10Xschematic.png'
    output:
        join(CELLGENE_DIR, 'PacBio_annotated_merged_humanplusflu_cells.tsv'),
        PYTHON_FIGS
    shell:
        """
        jupyter nbconvert \
            --to notebook \
            --execute \
            --inplace \
            --ExecutePreprocessor.timeout=-1 \
            pacbio_analysis.ipynb
        jupyter nbconvert pacbio_analysis.ipynb --to html
        mv pacbio_analysis.html {PAPER_DIR}/{PYTHON_FIGS_SUBDIR}
        """


rule get_PacBio_CCSs:
    """Build the PacBio CCSs."""
    input:
        join(SUBREADS_DIR, '{pacbioRun}.subreads.bam'),
    output:
        ccs_bam=join(CCS_DIR, '{pacbioRun}_ccs.bam'),
        ccs_report=join(CCS_DIR, '{pacbioRun}_report.csv'),
        ccs_log=join(CCS_DIR, '{pacbioRun}_log.txt')
    threads: 16
    shell:
        'ccs '
            '--minLength 50 '
            '--maxLength 5000 '
            '--minPasses 3 '
            '--minPredictedAccuracy 0.999 '
            '--logFile {output.ccs_log} '
            '--reportFile {output.ccs_report} '
            '--polish '
            '--numThreads {threads} '
            '{input} '
            '{output.ccs_bam}'


rule get_PacBio_subreads:
    """Get the PacBio subreads."""
    input:
        subreads=lambda wildcards: PACBIO_RUNS[wildcards.pacbioRun]
    output:
        subreads=join(SUBREADS_DIR, '{pacbioRun}.subreads.bam')
    run:
        os.symlink(input.subreads, output.subreads)
        

rule get_cellgene_matrix:
    """Build the cell-gene matrices with ``cellranger``."""
    input:
        join(FLUSEQ_DIR, 'flu-wsn.fasta'),
        join(FLUSEQ_DIR, 'flu-wsn.gtf'),
        join(FLUSEQ_DIR, 'flu-wsn-double-syn.fasta')
    output:
        join(CELLGENE_DIR, 'merged_humanplusflu_cells.tsv'),
        join(CELLGENE_DIR, 'merged_humanplusflu_genes.tsv'),
        join(CELLGENE_DIR, 'merged_humanplusflu_matrix.mtx'),
        join(CELLGENE_DIR, 'merged_canine_cells.tsv'),
        join(CELLGENE_DIR, 'merged_canine_genes.tsv'),
        join(CELLGENE_DIR, 'merged_canine_matrix.mtx')
    shell:
        'jupyter nbconvert '
            '--to notebook '
            '--execute '
            '--inplace '
            '--ExecutePreprocessor.timeout=-1 '
            'align_and_annotate.ipynb'
