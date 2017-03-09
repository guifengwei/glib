#!/usr/bin/python
# Programmer: Guifeng Wei, <guifengwei@gmail.com>
#-- coding: utf-8 --
#Last-modified: 07 May 2016 22:08:14

import sys, os, argparse, string
import pysam


def main():
    ''' main scripts '''
    bamfilename = sys.argv[1]
    samfile = pysam.AlignmentFile(bamfilename, 'rb')
    OutSamfileName = bamfilename.strip('.bam')
    outsamfile = pysam.AlignmentFile(OutSamfileName+'.f.bam', 'wb', template=samfile)
    for row in samfile:
        # mate_pair 1
        if not (row.flag & 0x0004):
            n = outsamfile.write(row)
    print >>sys.stderr, '## Split done !'
    outsamfile.close()

    
if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print ' Usage: python Filtering_Unmapped_ReadsPair.py ChIP-seq.bam'
    elif sys.argv[1][-4:] != '.bam':
        print ' Usage: python Filtering_Unmapped_ReadsPair.py ChIP-seq.bam'
    else:
        main()

