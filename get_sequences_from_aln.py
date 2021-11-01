#!/usr/bin/env python

import sys
from Bio import SeqIO
import os
import argparse

def main():
    options=argparse.ArgumentParser(sys.argv[0],
                        description='order sequences in alignments in Fasta format',
                        prefix_chars='-',
                        add_help=True,
                        epilog='Written by Chrispin Chaguza, Yale University, 2021')
    options.add_argument('-a',action='store',required=True,nargs=1,
                        metavar='in_align',dest='in_align',help='Input alignment file')
    options.add_argument('-l',action='store',required=True,nargs=1,
                        metavar='taxa_list',dest='taxa_list',help='File with the ordered sequence ids')
    options.add_argument('-o',action='store',required=True,nargs=1,
                        metavar='out_align',dest='out_align',help='Output file name')

    options=options.parse_args()

    infile=options.in_align[0:][0]
    outfile=options.out_align[0:][0]
    taxa_list=options.taxa_list[0:][0]

    in_align=[seq for seq in SeqIO.parse(infile,'fasta')]
    taxa_list=[seq_id.strip() for seq_id in open(taxa_list,'r')]
    seq_ids=[seq.id for seq in in_align]

    if len(set(seq_ids)&set(taxa_list))!=len(set(taxa_list)):
        sys.stdout.write('Warning: some sequences not found in alignment.\n')
    with open(outfile,'w') as out_handle:
        for taxon_id in taxa_list:
            for seq_id in in_align:
                if taxon_id==seq_id.id:
                    out_handle.write('>'+taxon_id+'\n')
                    out_handle.write(str(seq_id.seq)+'\n')
                    break
        for num,seq_id in enumerate(list(set(taxa_list)-set(seq_ids))):
            if num==0:
                sys.stdout.write("Sequences not found: "+seq_id+',')
                sys.stdout.flush()
            else:
                sys.stdout.write(seq_id+',')
                sys.stdout.flush()

                sys.stdout.write('\n')

if __name__=="__main__":
        main()
