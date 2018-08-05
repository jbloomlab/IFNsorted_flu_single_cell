"""``snakemake`` file that runs entire analysis.

Written by Jesse Bloom."""


# Imports -----------------------------------------
import shutil
from os.path import join


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
PACBIO_RUNS_FILE = 'data/PacBio_runs.tsv'
with open(PACBIO_RUNS_FILE) as f:
    PACBIO_RUNS = dict([line.strip().split('\t') for line in f])


# Rules ------------------------------------------- 

rule all:
    input:
        join(CELLGENE_DIR, 'PacBio_annotated_merged_humanplusflu_cells.tsv')
    

rule call_PacBio_mutations:
    """Call viral mutations from PacBio CCSs."""
    input:
        expand(os.path.join(CCS_DIR, '{pacbioRun}_ccs.bam'),
                pacbioRun=PACBIO_RUNS.keys()),
        join(CELLGENE_DIR, 'merged_humanplusflu_cells.tsv'),
        join(FLUSEQ_DIR, 'flu-wsn-mRNA.fasta'),
        join(FLUSEQ_DIR, 'flu-wsn-double-syn-mRNA.fasta'),
        join(FLUSEQ_DIR, 'flu-wsn.gb'),
        'data/images/10Xschematic.png'
    output:
        join(CELLGENE_DIR, 'PacBio_annotated_merged_humanplusflu_cells.tsv')
    shell:
        'jupyter nbconvert '
            '--to notebook '
            '--execute '
            '--inplace '
            '--ExecutePreprocessor.timeout=-1 '
            'pacbio_analysis.ipynb'


rule get_PacBio_CCSs:
    """Build the PacBio CCSs."""
    input:
        join(SUBREADS_DIR, '{pacbioRun}.subreads.bam'),
    output:
        ccs_bam=os.path.join(CCS_DIR, '{pacbioRun}_ccs.bam'),
        ccs_report=os.path.join(CCS_DIR, '{pacbioRun}_report.csv'),
        ccs_log=os.path.join(CCS_DIR, '{pacbioRun}_log.txt')
    threads: 16
    shell:
        'ccs '
            '--minLength 50 '
            '--maxLength 5000 '
            '--minPasses 3 '
            '--minPredictedAccuracy 0.999 '
            '--logFile {output.ccs_log}_log.txt '
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
        shutil.copy(input.subreads, output.subreads)
        

rule get_cellgene_matrix:
    """Build the cell-gene matrices with ``cellranger``."""
    input:
        join(FLUSEQ_DIR, 'flu-wsn.fasta'),
        join(FLUSEQ_DIR, 'flu-wsn-double-syn.fasta')
    output:
        join(CELLGENE_DIR, 'merged_humanplusflu_genes.tsv'),
        join(CELLGENE_DIR, 'merged_humanplusflu_cells.tsv'),
        join(CELLGENE_DIR, 'merged_humanplusflu_matrix.mtx'),
        join(CELLGENE_DIR, 'merged_canine_genes.tsv'),
        join(CELLGENE_DIR, 'merged_canine_cells.tsv'),
        join(CELLGENE_DIR, 'merged_canine_matrix.mtx')
    shell:
        'jupyter nbconvert '
            '--to notebook '
            '--execute '
            '--inplace '
            '--ExecutePreprocessor.timeout=-1 '
            'align_and_annotate.ipynb'
