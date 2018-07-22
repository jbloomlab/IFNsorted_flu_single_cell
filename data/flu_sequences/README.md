# Sequences for the influenza strains

This directory contains the sequences for the wildtype and synonymously barcoded A/WSN/1933 (H1N1) influenza strains used in the study.

There are maps for the 8 plasmids (pHW181-PB2, ...) used to generate the wildtype virus and the 8 plasmids (pHW181-PB2-double-syn, ...) used to generate the synonymously barcoded virus. These are the Genbank plasmid maps from the Bloom lab plasmid logs.

The Python script [make_seqs_and_gtf.py](make_seqs_and_gtf.py) then makes sequence files and GTF files. 
These GTF files just annotate the entire viral RNAs with *gene_biotype* of *"gene"* for the full viral gene segment.
For the 3' end counting used by the Chromium, just annotating the gene segments is sufficient.
For the PacBio analysis, we want the mRNA.
We identify the genes as the regions flanked by U12 / U13, and the mRNAs as the second nucleotide of the reverse-complemented vRNA (this excludes the added snatched cap, see [Koppstein et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4446424/), but it's close enough for our purposes) up until the most 3' run of five `A` nucleotides in the positive sense direction (this is the polyA signal, see [Robertson et al](http://jvi.asm.org/content/38/1/157.full.pdf)).
We identify the NS1 / NS2 and M1 / M2 mRNAs using the splice junctions described in [Dubois et al](http://mbio.asm.org/content/5/3/e00070-14.abstract).

Running this Python script produces:
  - [flu-wsn.fasta](flu-wsn.fasta)
  - [flu-wsn.gtf](flu-wsn.gtf)
  - [flu-wsn-double-syn.fasta](flu-wsn-double-syn.fasta)
  - [flu-wsn-double-syn.gtf](flu-wsn-double-syn.gtf)
  - [flu-wsn-mRNA.fasta](flu-wsn-mRNA.fasta)
  - [flu-wsn-double-syn-mRNA.fasta](flu-wsn-double-syn-mRNA.fasta)
