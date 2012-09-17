#!/usr/bin/python
# Wei Guifeng, <guifengwei@gmail.com>
# -- coding: utf-8 --

import sys, os, argparse, string

def parse_argument():
    ''' argument parser'''
    p=argparse.ArgumentParser(description='example: %(prog)s --gene *.tab -o tssfile',
                            epilog="dependency: python2.7, zbed ")
    p.add_argument('-g','--gene',dest='genefile',metavar='Gene',type=str,
                    help="The GENE file. Format: GenePred")
    p.add_argument('-o','--output',dest='output',type=str, help=" the TSS output(sorted)")
    if len(sys.argv) == 1 :
        sys.exit(p.print_help())
    args=p.parse_args()
    return args

def main():
    ''' main scripts '''
    args = parse_argument()
    print "hello, python"


if __name__== "__main__":
    main()

