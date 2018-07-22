"""Make sequence and GTF files from Genbank plasmid maps."""


import re
import os
import glob
import itertools
import collections
import copy

import Bio.SeqIO
import Bio.Seq
import Bio.SeqRecord
import Bio.SeqFeature
import BCBio.GFF


def main():
    """Main body of script."""

    # flu genes
    gene_names = ['PB2', 'PB1', 'PA', 'HA', 'NP', 'NA', 'M', 'NS']

    # plus / minus synonymous viral barcodes
    viral_barcodes = ['', '-double-syn']

    # information used to identify features
    polyA = re.compile('A{5}') # run of at least 5 A nucleotides
    u12 = re.compile('AGC[GA]AAAGCAGG') # U12 with position 4 polymorphism
    u13 = re.compile('CCTTGTTTCTACT') # reverse of U13
    # Define introns removed to create NS2 and M2 as in Fig 3 of
    # http://mbio.asm.org/content/5/3/e00070-14.abstract
    mRNA_splice = {
            'M':re.compile('AAC(?P<intron>GTA[CT]GTTC[ACGT]+GAAAATTT[AG]CAG)[GA]C'),
            'NS':re.compile('CAG(?P<intron>GTAGA[CT]TG[ACGT]+C[CT]TC[TC][TCA]T[TG]CCAG)GA'),
            }

    genes = collections.defaultdict(list)

    for syntype, gene_short_name in itertools.product(viral_barcodes, gene_names):

        # read plasmid
        plasmidfile = glob.glob('*_pHW18*-{0}{1}.gb'.format(
                gene_short_name, syntype))
        assert len(plasmidfile) == 1, "not 1 map for {0}{1}".format(
                gene_short_name, syntype)
        plasmidfile = plasmidfile[0]
        plasmid = str(Bio.SeqIO.read(plasmidfile, 'genbank').seq)

        # get vRNA flanked by U12 / U13
        u12matches = list(u12.finditer(plasmid))
        assert len(u12matches) == 1, "Not exactly one U12 for {0}{1}".format(
                gene_short_name, syntype)
        u13matches = list(u13.finditer(plasmid))
        assert len(u13matches) == 1, "Not exactly one U13 for {0}{1}".format(
                gene_short_name, syntype)
        geneseq = plasmid[u12matches[0].start(0) : u13matches[0].end(0)]
        print("gene length {0} for {1}{2}".format(
                len(geneseq), gene_short_name, syntype))
        gene_name = "flu" + gene_short_name
        gene = Bio.SeqRecord.SeqRecord(Bio.Seq.Seq(geneseq), 
                id=gene_name,
                name=gene_name,
                description='{0} vRNA from plasmid {1}'.format(
                        gene_short_name, plasmidfile),
                features=[Bio.SeqFeature.SeqFeature(
                    Bio.SeqFeature.FeatureLocation(0, len(geneseq)),
                    id=gene_name,
                    type='gene',
                    strand=1,
                    qualifiers={
                        "source":"JesseBloom",
                        "gene_id":gene_name,
                        "gene_name":gene_name,
                        "gene_biotype":"gene",
                        },
                    )],
                )

        # Get mRNA flanked by one nt into u12 and polyA, see:
        # 5' end described: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4446424/
        # polyA described: https://www.ncbi.nlm.nih.gov/pubmed/7241649
        mrna_start = 1
        polyAmatches = list(polyA.finditer(geneseq))
        assert len(polyAmatches) >= 1, "Not at least one polyA for {0}{1}".format(
                gene_short_name, syntype)
        mrna_end = polyAmatches[-1].start(0)
        mrna_name = gene_name + {False:"", True:"1"}[gene_short_name in mRNA_splice]
        gene.features.append(
                Bio.SeqFeature.SeqFeature(
                    Bio.SeqFeature.FeatureLocation(mrna_start, mrna_end),
                    id=mrna_name,
                    type='mRNA',
                    strand=1,
                    qualifiers={
                        "source":"JesseBloom",
                        "gene_id":gene_name,
                        "gene_name":gene_name,
                        "transcript_id":mrna_name,
                        "gene_biotype":"mRNA",
                        },
                    )
                )

        # is there second splice form?
        if gene_short_name in mRNA_splice:
            intron = list(mRNA_splice[gene_short_name].finditer(geneseq))
            assert len(intron) == 1, "not exactly one intron for {0}{1}".format(
                    gene_short_name, syntype)
            intron_start = intron[0].start('intron')
            intron_end = intron[0].end('intron')
            mrna_name = gene_name + '2'
            gene.features.append(
                    Bio.SeqFeature.SeqFeature(
                        Bio.SeqFeature.CompoundLocation([
                            Bio.SeqFeature.FeatureLocation(
                                mrna_start, intron_start),
                            Bio.SeqFeature.FeatureLocation(
                                intron_end, mrna_end)
                            ]),
                        id=mrna_name,
                        type="mRNA",
                        strand=1,
                        qualifiers={
                            "source":"JesseBloom",
                            "gene_id":gene_name,
                            "gene_name":gene_name,
                            "transcript_id":mrna_name,
                            "gene_biotype":"mRNA",
                            },
                        )
                    )

        genes[syntype].append(gene)

    # now write output
    for syntype in viral_barcodes:

        genefile = 'flu-wsn{0}.fasta'.format(syntype)
        print("Writing {0} genes to {1}".format(len(genes[syntype]), genefile))
        Bio.SeqIO.write(genes[syntype], genefile, 'fasta')

        mrnas = [Bio.SeqRecord.SeqRecord(mrna.extract(gene).seq,
                    id=mrna.id, description='')
                for gene in genes[syntype]
                for mrna in gene.features if mrna.type == 'mRNA']
        mrnafile = 'flu-wsn{0}-mRNA.fasta'.format(syntype)
        print("Writing the {0} mRNAs to {1}".format(len(mrnas), mrnafile))
        Bio.SeqIO.write(mrnas, mrnafile, 'fasta')

        gtffile = os.path.splitext(genefile)[0] + '.gtf'
        print("Writing gene annotations to {0}\n".format(gtffile))
        just_genes = []
        for gene in genes[syntype]:
            just_gene = copy.deepcopy(gene)
            just_gene.features = just_gene.features[ : 1]
            just_genes.append(just_gene)
        with open(gtffile, 'w') as f:
            BCBio.GFF.write(just_genes, f)
        # Hacky conversion of GFF3 file to GTF, changing 9th column to
        # delimit qualifiers with spaces / quotes rather than equals sign.
        # Conversion is probably not robust to all qualifiers, but works here.
        with open(gtffile) as f:
            lines = f.readlines()
        newlines = []
        for line in lines:
            if line[0] == '#':
                newlines.append(line)
            else:
                entries = line.strip().split('\t')
                assert len(entries) == 9, str(len(entries)) + '\n' + line
                newqualifiers = []
                for qualifier in entries[-1].split(';'):
                    (key, value) = qualifier.split('=')
                    newqualifiers.append('{0} "{1}"'.format(key, value))
                entries[-1] = '; '.join(newqualifiers)
                newlines.append('\t'.join(entries) + '\n')
        with open(gtffile, 'w') as f:
            f.write(''.join(newlines))


# run the script
if __name__ == '__main__':
    main()

