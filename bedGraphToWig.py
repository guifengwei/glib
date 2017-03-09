#!/usr/bin/python
# Programmer: Guifeng Wei, <guifengwei@gmail.com>
#-- coding: utf-8 --
#Last-modified: 10 Jan 2017 13:03:54

import sys, os, argparse, string

def read_bedGraph(file=""):
    '''read the bedGraph into genome information '''
    for line in open(file, 'r'):
        if not line.startswith("#"):
            line = line.strip().split("\t")
            chri = line[0]
            span = int(line[2]) - int(line[1])
            start = int(line[1])
            print "variableStep chrom="+chri+" span="+str(span)
            print str(start)+"\t"+line[3]


if __name__ == "__main__":
    if len(sys.argv) <2:
        print "Usage: python this_script.py your_bedGraph"
    else:
        read_bedGraph(sys.argv[1])

