#!/usr/bin/env python

import sys, os, readline, shutil, shlex, fnmatch, re, argparse

#print("bulkrename", "from", sys.argv[1], "to", sys.argv[2])

parser = argparse.ArgumentParser(description='Bulk rename files.')

parser.add_argument("-v", '--verbose', dest='verbose',
                    default=0,  action='count',
                    help='verbocity on (default: off)')

parser.add_argument("-d", '--debug', dest='debug',
                    default=0,  type=int, action='store',
                    help='Debug level')

parser.add_argument("-t", '--test', dest='testx',
                    default=0,  action='store_true',
                    help='Test what would be done.')

parser.add_argument("-f", '--from', dest='frox',
                    default=0,  type=str, action='store',
                    help='File name from.')

parser.add_argument("-o", '--to', dest='tox',
                    default=0,  type=str, action='store',
                    help='File name to.')

# ------------------------------------------------------------------------

def     mainloop():

    if not args.frox:
        print("Must specify from regex (-f)")
        sys.exit()

    if not args.tox:
        print("Must specify to regex (-o)")
        sys.exit()

    xx = re.compile(args.frox)

    lll = os.listdir(".")

    for aa in lll:
        #if fnmatch.fnmatch(aa, sys.argv[1]):
        #if regexfnmatch.fnmatch(aa, sys.argv[1]):
        mm = xx.match(aa)
        if mm:
            sss = mm.span()
            nnn = aa[:sss[0]] + \
                        args.tox + aa[sss[1]:]

            if args.verbose:
                print("from:", aa, "to", nnn)
            if not args.testx:
                os.rename(aa, nnn)

version = "1.0.0"

def mainfunct():

    global args
    args = parser.parse_args()
    #print(args)
    mainloop()

if __name__ == "__main__":
    mainfunct()

# EOF
