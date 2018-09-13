# Key citations for paper

Here are some key background citations on topics related to the paper.

## IFN induction by flu

[Velthuis et al (2018)](https://www.biorxiv.org/content/early/2018/08/06/385716):
Shows that mini-viral RNAs are a major IFN antagonist, and that the level of their production varies markedly between avian and human strains. 
They show that PB2 mutations can modulate IFN induction by mini-viral mRNAs, and also that a PB1 mutation affects the level of IFN induction.

[Wu et al (2014)](https://jvi.asm.org/content/88/17/10157.short):
Passaged influenza +/- IFN and looked for mutations that arose in IFN- conditions taht conferred IFN sensitivity.
Showed that a variety of NS point mutations can do this.
One of the mutations that they validated only caused an amino-acid substitution in NS2, but most caused amino-acid substitutions in NS1.
Note that they screened for mutations that conferred IFN sensitivity, not mutations that induced IFN!
Main relevant point for us is simply that there are lots of NS mutations that alter IFN sensitivity.

[Du et al (2018)](http://science.sciencemag.org/content/359/6373/290):
Passaged influenza in absence of IFN and then found mutations that increase IFN sensitivity.
In addition to mutations in NS1, they validate mutations in PB2 and M1 that increase IFN sensitivity and (in combination) IFN induction.
Main relevant point for us is just that there are point mutations in NS1 and PB2 and/or M1 that alter IFN induction.

[Perez-Cidoncha (2014)](https://jvi.asm.org/content/88/9/4632.short):
Passaged virus +/-IFN, and then identified mutations that arose.
They identify viruses with mutations throughout the genomes that induce more IFN.
The experiments are somewhat confounded by the fact that they never use reverse genetics to specifically validate that any given mutation actually causes more IFN induction when introduced in an isogenic background in a controlled fashion--but nonetheless, the implication of their results as a whole are that mutations in a variety of genes other than NS1 could be associated with IFN induction.

[Killip et al (2017)](https://doi.org/10.1099/jgv.0.000687):
Uses an A549 reporter cell line to show that only a low percentage (<= 1%) of cells infected with a "wildtype" viral stock induce IFN.
They also perform infections with NS1-deficient virus and show that although it induces IFN much more, still less than half of cells infected with the NS1-deficient virus induce IFN.

[Weber et al (2013)](https://www.sciencedirect.com/science/article/pii/S1931312813000437):
Argues that incoming RNPs induce IFN via RIG-I independent of transcription.
Although there experiments use cycloheximide, which I would expect to only block **secondary** transcription.

[Weber et al (2015)](https://www.sciencedirect.com/science/article/pii/S1931312815000256):
Shows that mutation at 627K in PB2 affects IFN induction.
Also argues that incoming vRNPs induce IFN.
I have not read carefully enough to have an opinion on whether this is the case or not.

[Killip et al (2014)](https://jvi.asm.org/content/88/8/3942.short):
Argues that activation of IFN by influenza requires primary transcription: it's blocked by actinomycin D, but not cycloheximide.

[Kalfass et al (2013)](https://jvi.asm.org/content/87/12/6925.short):
Infect IFNb reporter mice with wildtype or NS1-deficient influenza.
At 24 and 48 hours, no and only a small fraction of flu+ cells were IFN+ on infection with wildtype virus, respectively.
Infection with the NS1-deficient virus clearly induces more IFN globally in the mice, but they don't present data that I can understand that shows exactly how much more commonly cells are IFN+ on infection with the NS1-deficient virus.

[Tapia et al (2013)](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1003703):
Shows that appearance of defective viral genomes (internal deletions in polymerase genes) appeared in mice after a few days, coincident with IFN expression.

[Baum et al (2010)](http://www.pnas.org/content/107/37/16303.short):
Suggests RIG-I preferentially binds shorter internally deleted influenza segments.

[Boergeling et al (2015)](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1004924):
Shows that the truncated PB2 protein in an internal deletion virus induces more IFN.

[Dimmock and Easton (2015)](http://www.mdpi.com/1999-4915/7/7/2796):
Reviews a cloned defective interfering influenza RNA that induces more IFN.

[Sjaastad et al (2018)](http://www.pnas.org/content/early/2018/08/29/1807516115):
Uses reporter viruses to look at heterogeneity and IFN induction of single-cycle flu in mice.
Argues for specific ISG signatures in cells with more flu, although this is done at the bulk level so could be confounded by cell type, etc.
Definitely shows that priming of IFN by one infection changes tropism of cells infected in a second infection shortly thereafter.

## Single-cell virus mRNA-seq

[Russell et al (2018)](https://elifesciences.org/articles/32303):
Our original single-cell transcriptomics of influenza-infected cells.
Showed lots of heterogeneity in mRNA production among cells, and very rare IFN induction.

[Zanini et al (2018)](https://elifesciences.org/articles/32942):
Single-cell transcriptomics of dengue and Zika infected cells.
Cells sorted into 384-well plates and a custom primer used to capture the non-polyA viral RNA.
They sequenced to great depth (400,000 per cell).
Up to 25% of reads virus derived.
Identified host genes correlated with viral burden, some of which differed between Zika and dengue.
They then validated that some of the genes correlated with viral burden were pro- or anti-viral.

[Zanini et al (2018b)](https://www.biorxiv.org/content/early/2018/08/09/388181):
Single-cell RNA-seq on cells isolated from dengue-infected individuals. 
They identify cellular genes (especially ISGs) upregulated in a cell-type specific fashion on patients who get severe disease.
Dengue RNA is relatively rare in cells, and only reaches 1% (compared to 25% in their earlier cell culture study).
The reads also covered the entire viral genome for one sample allowing them to call the viral sequence in one patient, although this appears to be done at the consensus-across-cells level.

[Steuerman et al (2018)](https://www.biorxiv.org/content/early/2018/08/09/388181):
They perform single-cell mRNA-seq on cells from influenza-infected mice.
They do this in wildtype mice and IRF7-KO mice.
They show that all cell types (immune and non-immune) are virus infected, although the viral loads are much lower in immune cells than epithelial ones.
There is lots of ISG expression, although a re-analysis of their data shows that IFN expression isn't very common.
An interesting aspect of this study is that they sequence to very low depth. 
I'm not clear if this is simply a choice based on economizing sequencing depth, or is due to some constrain in their mRNA capture efficiency.

[Saikia et al (2018)](https://www.biorxiv.org/content/early/2018/08/28/328328):
Modifies DropSeq by ligating a custom primer onto the polyA, and uses this to perform targeted capture of viral transcripts at the same time as standard polyA transcriptomics. 
Uses it to get full sequence of a viral gene in rheovirus infected cells.

## PacBio-related references
[Gupta et al (2018)](https://www.biorxiv.org/content/early/2018/07/08/364950):
Performed PacBio sequencing to obtain splice isoforms of genes from 10X single-cell transcriptomic libraries of mouse brain cells.
Provides combined transcriptomic and splicing information.

[Laird Smith et al (2016)](https://academic.oup.com/ve/article/2/2/vew018/2797613), [Eren et al (2017)](https://doi.org/10.1101/230474), and [Rogers et al (2015)](https://mbio.asm.org/content/6/2/e02464-14.short) appear to be good example papers for using PacBio to get full-length sequence of viral genes at the **bulk** (non-single-cell level).

## Stochasticity in IFN induction

[Shalek et al (2013)](https://www.nature.com/articles/nature12172) and [Shalek et al (2014)](https://doi.org/10.1038/nature13437):
IFN induction is stochastic even when stimulated with a synthetic ligand.

[Bhushal et al (2017)](https://www.ncbi.nlm.nih.gov/pubmed/28659914):
Show stochastic induction of type I and III IFN, dependent on part on epigenetic state.

[Wimmers et al (2018)](https://www.nature.com/articles/s41467-018-05784-3):
Shows that only a fraction pDCs stochastically activate IFN.


##Effect of ribavirin on influenza

[C, Schiktussek (1976)](https://www.ncbi.nlm.nih.gov/pubmed/1275709) Original report on the inhibition of influenza RNA synthesis with virazole (ribavirin).

[Vanderlinden et al (2016)](https://aac.asm.org/content/60/11/6679) Comparison of inhibitory effects of favirpiravir and ribavirin. Shows polymerase inhibition at high doses of ribavirin.

[Reuther et al (2015)](https://www.nature.com/articles/srep11346) Generation of reporter virus demonstrates the suppression of influenza polymerase activity at high doses of ribavirin. 


