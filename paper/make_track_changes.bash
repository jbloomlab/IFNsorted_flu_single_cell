#!/bin/bash

# make track changes version of manuscript

latexdiff paper_orig_submission.tex paper.tex > track_changes.tex
pdflatex track_changes
bibtex track_changes
pdflatex track_changes
pdflatex track_changes
