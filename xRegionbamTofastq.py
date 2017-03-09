#!/usr/bin/python
# Programmer: Wei Guifeng, <guifengwei@gmail.com>
#-- coding: utf-8 --
#Last-modified: 11 Jul 2014 15:54:35

import sys, os, argparse, string

def parse_argument():
    ''' argument parser '''
    p=argparse.ArgumentParser(description='example: %(prog)s --bam *.bam --bed *.bed --library pe --name', 
                              epilog=" dependency: samtools ")
    p.add_argument('--bed', dest='bed', metavar='bed',required=True, type=str, help="The region file. format: bed")
    p.add_argument('--bam', dest='bam', metavar='bam',type=str, required=True, help="The input bamfile. format: bam")
    p.add_argument('--library', dest='library', metavar='se|pe', type=str, choices=["se",'pe'], default="se", help="The library type, se represents single-end reads and pe represents paired-end read (Default: se)")
    p.add_argument('--name', dest="name", metavar='name', default="temp", type=str, help="the name for queried fastq file(default: temp)")
    if len(sys.argv) == 1 :
        sys.exit(p.print_help())
    args=p.parse_args()
    return args

def main():
    ''' main scripts '''
    args = parse_argument()
    print >>sys.stderr, '\n# Using Samtools to fetch the alignment in the bed region'
    os.system("samtools view -L %s %s > temp_bam" %(args.bed, args.bam) )
    if args.library == 'se':
        print >>sys.stderr, "# Processing the single-end library"
        f = open(args.name + "_output.se.fastq", 'w')
        for line in open("temp_bam", 'r'):
            if not line.startswith("#") or not line.startswith("@"):
                line = line.strip().split("\t")
                fqid, fqseq, fq_qual = line[0], line[9], line[10]
                print >>f, "{0}\n{1}\n{2}\n{3}".format("@"+fqid, fqseq, "+", fq_qual)
        f.close()
        print >>sys.stderr, "# Success! Output is :", args.name+"_output.se.fastq "
    elif args.library == 'pe':
        print >>sys.stderr, "# Processing the paried-end library"
        
        rd1 = open(args.name + "_output.pe.rd1.fastq", 'w')
        rd2 = open(args.name + "_output.pe.rd2.fastq", 'w')
        for line in open("temp_bam", 'r'):
            if not line.startswith("#") or not line.startswith("@"):
                line = line.strip().split("\t")
                fqid, flag, fqseq, fq_qual = line[0], line[1], line[9], line[10]
                if int(flag) & 64: # 64 means read is first mate
                    print >>rd1, "{0}\n{1}\n{2}\n{3}".format("@"+fqid+"/1", fqseq, "+", fq_qual)
                elif int(flag) & 128: # 128 means read is second mate
                    print >>rd2, "{0}\n{1}\n{2}\n{3}".format("@"+fqid+"/2", fqseq, "+", fq_qual)
                else:
                    pass
        rd1.close()
        rd2.close()
        print >>sys.stderr, "# Success! Output is :", args.name+"_output.pe.rd1/2.fastq"
    else:
        print >>sys.stderr, '# library error '
    os.system("rm temp_bam")

if __name__ == "__main__":
    main()

