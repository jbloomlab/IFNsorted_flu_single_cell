"""Make FASTA and GTF files for vRNAs and mRNAs from Genbank plasmid maps."""


import re
import os
import glob
import Bio.SeqIO
import Bio.Seq
import Bio.SeqRecord
import Bio.SeqFeature
import BCBio.GFF


def main():
    """Main body of script."""
    polyA = re.compile('A{5}') # run of at least 5 A nucleotides
    u12 = re.compile('AGC[GA]AAAGCAGG') # U12 with position 4 polymorphism
    u13 = re.compile('CCTTGTTTCTACT') # reverse of U13
    segs = ['PB2', 'PB1', 'PA', 'HA', 'NP', 'NA', 'M', 'NS']
    # Define introns removed to create NS2 and M2 as in Fig 3 of
    # http://mbio.asm.org/content/5/3/e00070-14.abstract
    mRNA_splice = {
            'M':re.compile('AAC(?P<intron>GTA[CT]GTTC[ACGT]+GAAAATTT[AG]CAG)[GA]C'),
            'NS':re.compile('CAG(?P<intron>GTAGA[CT]TG[ACGT]+C[CT]TC[TC][TCA]T[TG]CCAG)GA'),
            }

    for syntype in ['', '-double-syn']:
        vrnas = []
        mrnas = []

        for seg in segs:

            # read plasmid
            fplasmid = glob.glob('*_pHW18*-{0}{1}.gb'.format(seg, syntype))
            assert len(fplasmid) == 1, "Didn't find 1 map for {0}{1}".format(
                    seg, syntype)
            fplasmid = fplasmid[0]
            plasmid = str(Bio.SeqIO.read(fplasmid, 'genbank').seq)

            # get vRNA flanked by U12 / U13
            u12matches = list(u12.finditer(plasmid))
            assert len(u12matches) == 1, "Not exactly one U12 for {0}{1}".format(
                    seg, syntype)
            u13matches = list(u13.finditer(plasmid))
            assert len(u13matches) == 1, "Not exactly one U13 for {0}{1}".format(
                    seg, syntype)
            vrnaseq = plasmid[u12matches[0].start(0) : u13matches[0].end(0)]
            print("vRNA of length {0} for {1}{2}".format(len(vrnaseq), seg, syntype))
            vrna = Bio.SeqRecord.SeqRecord(Bio.Seq.Seq(vrnaseq), 
                    id='flu' + seg + syntype,
                    description='{0} vRNA from plasmid {1}'.format(seg, fplasmid),
                    features=[Bio.SeqFeature.SeqFeature(
                        Bio.SeqFeature.FeatureLocation(0, len(vrnaseq)),
                        type='exon',
                        strand=1,
                        qualifiers={
                            "source":"JesseBloom",
                            "gene_id":'flu' + seg,
                            "transcript_id":'flu' + seg,
                            "gene_biotype":"vRNA",
                            },
                        )],
                    )
            vrnas.append(vrna)

            # Get mRNA flanked by one nt into u12 and polyA, see:
            # - 5' end described: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4446424/
            # - polyA described: https://www.ncbi.nlm.nih.gov/pubmed/7241649
            polyAmatches = list(polyA.finditer(vrnaseq))
            assert len(polyAmatches) >= 1, "Not at least one polyA for {0}{1}".format(
                    seg, syntype)
            mrnaseq = vrnaseq[1 : polyAmatches[-1].start(0)]
            if seg in mRNA_splice:
                intron = list(mRNA_splice[seg].finditer(mrnaseq))
                assert len(intron) == 1, "not exactly one intron for {0}{1}".format(
                        seg, syntype)
                mrna1_name = 'flu' + seg + '1' + syntype
                mrnas.append((mrna1_name, mrnaseq))
                print("mRNA of length {0} for {1}".format(len(mrnaseq), mrna1_name))
                mrna2_name = 'flu' + seg + '2' + syntype
                mrnaseq2 = (mrnaseq[ : intron[0].start('intron')] +
                            mrnaseq[intron[0].end('intron') : ])
                mrnas.append((mrna2_name, mrnaseq2))
                print("mRNA of length {0} for {1}".format(len(mrnaseq2), mrna2_name))
            else:
                mrna_name = 'flu' + seg + syntype
                mrnas.append((mrna_name, mrnaseq))
                print("mRNA of length {0} for {1}".format(len(mrnaseq), mrna_name))

        mrnafile = 'flu-wsn{0}-mRNA.fasta'.format(syntype)
        print("Writing the {0} mRNAs to {1}".format(len(mrnas), mrnafile))
        with open(mrnafile, 'w') as f:
            f.write('\n'.join('>{0}\n{1}'.format(*tup) for tup in mrnas))

        vrnafile = 'flu-wsn{0}.fasta'.format(syntype)
        print("Writing the {0} vRNAs to {1}".format(len(vrnas), vrnafile))
        Bio.SeqIO.write(vrnas, vrnafile, 'fasta')

        gtffile = os.path.splitext(vrnafile)[0] + '.gtf'
        print("Writing the vRNA annotations to {0}\n".format(gtffile))
        with open(gtffile, 'w') as f:
            BCBio.GFF.write(vrnas, f)
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

