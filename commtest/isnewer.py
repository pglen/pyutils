#!/usr/bin/env python3

import os, sys

#from optparse import OptionParser
from argparse import ArgumentParser

def     cmdline():

    parser = ArgumentParser()

    parser.add_argument('fnames', metavar='fname',  nargs='+',
                    help='The two file names to compare. [REF / SRC1 .. SRCN]')

    parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose",
                  help="print extended status messages to stdout")

    parser.add_argument("-q", "--quiet",
                  action="store_true", dest="quiet",
                  help="don't print status messages to stdout")

    parser.add_argument("-d", "--debug",
                  action="store_true", dest="debug",
                  help="print debug info")

    parser.add_argument("-e", "--echo",
                  action="store_true", dest="echo",
                  help="echo newer status to stdout")

    return parser

#
# use: isnewer.py oldfile newfile
#

def testage(clargs):

    if clargs.debug:
        print( "clargs", clargs); #exit()

    newer = 0

    # At least two files to be present
    if not os.path.isfile(clargs.fnames[0]):
        return 1

    if not os.path.isfile(clargs.fnames[1]):
        return 2

    try:
        if clargs.debug:
            for aa in clargs.fnames:
                print(aa, os.stat(aa).st_mtime,)

        ref = os.stat(clargs.fnames[0]).st_mtime
        for aa in clargs.fnames[1:]:
            if os.stat(aa).st_mtime > ref:
                newer |= 1
    except:
        if clargs.verbose or clargs.debug:
            print( "Exception on stat", sys.exc_info())
            newer = 2

    return newer

# -------------------------------------------------------------------

if __name__ == '__main__':

    parser = cmdline(); clargs = parser.parse_args()
    newer = testage(clargs)
    if  newer == 1:
        if clargs.verbose:
            print( "Newer")
        if clargs.echo:
            print("1")
        sys.exit(1)
    if  newer == 2:
        if clargs.verbose:
            print( "ERROR")
        if clargs.echo:
            print("2")
        sys.exit(2)
    else:
        if clargs.verbose:
            print( "Not Newer")
        if clargs.echo:
            print("0")
        sys.exit(0)

# EOF
