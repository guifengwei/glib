#!/usr/bin/python
# Wei Guifeng, <guifengwei@gmail.com>
# -- coding: utf-8 --

import sys
from zbed import GenePred

def main():
    ''' '''
    fh = open(sys.argv[1],'r')
    for line in fh:
        if not line.startswith("#"):
            line=line.strip().split("\t")
            a= GenePred(line)
            seq = a.get_cdna_seq(fn="/usr/people/bioc1387/Project/UCSCTools/genome_2bit/mm10.2bit")
            print ">"+a.id
            print seq

if __name__=="__main__":
    if len(sys.argv)==1:
        print >>sys.stderr,"# usage: python xGenePred_GetSeq.py genetab.txt"
    else:
        main()
