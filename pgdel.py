#!/usr/bin/env python3

import os, sys

if sys.version_info[0] < 3:
    print("Python 2 is not supported as of 1/1/2020")
    sys.exit(1)

import getopt, signal, select, string, time, glob
import tarfile, subprocess, struct, platform, shutil, argparse

# ------------------------------------------------------------------------
# Globals

PNAME = "pgdel.py"
VERSION = "1.0.1"
tmptarg = "/tmp/pgdel"

''' Delete file by moving to temp '''

parser = argparse.ArgumentParser(prog=PNAME, description=\
                'Delete files by moving to /tmp directory.')
parser.add_argument("delname", nargs="+", help="File(s) to delete. Wildcard OK", action="append")
parser.add_argument("-v", '--verbose', dest='verbose',
                    default=0,  action='count',
                    help='verbosity on (default: off)')
parser.add_argument("-t", '--test', dest='test',
                    default=0,  action='count',
                    help='test what would be done (default: off)')
parser.add_argument("-V", '--version', dest='version',
                    default=0,  action='count',
                    help='Show version number.')

parser2 = argparse.ArgumentParser(prog="pgdel.py", description=\
                'Delete files by moving to /tmp directory.')
parser2.add_argument("-V", '--version', dest='version',
                    default=0,  action='count',
                    help='Show version number.')

def copydir(aa):

    ''' Recursively copy '''

    bb = aa
    if aa[0] == os.sep:
        #print("absolute --- turn to relative", aa)
        # if home component
        home = os.getenv("HOME")
        #print("home:", home)
        if aa[:len(home)] == home:
            bb = aa[len(home):]
        bb = "." + bb

    ttt = os.path.join(tmptarg, bb)
    try:
        if args.verbose > 1:
            print("moving", aa, ttt)
        if args.test:
            print("shutil.copytree" , aa, ttt)
        else:
            shutil.copytree(aa, ttt, dirs_exist_ok=True)
            shutil.rmtree(aa)
    except:
        for bb in range(2):
            fname2 = "%s_%d" % (ttt, bb)
            if not os.path.exists(fname2):
                break
        try:
            #print("ren", aa, fname2)
            if os.path.exists(fname2):
                shutil.rmtree(fname2)
                shutil.move(ttt, fname2)
        except:
            print("rename", sys.exc_info())

        if args.verbose > 1:
            print("Renaming:", ttt, "to", fname2)
        try:
            shutil.copytree(aa, ttt, dirs_exist_ok=True)
            shutil.rmtree(aa)
            #shutil.move(aa, tmptarg)
        except:
            print("move2", ttt, sys.exc_info())

def copyfile(aa):

    bb = aa
    if aa[0] == os.sep:
        #print("absolute --- turn to relative", aa)
        # if home component
        home = os.getenv("HOME")
        #print("home:", home)
        if aa[:len(home)] == home:
            bb = aa[len(home):]
        bb = "." + bb

    ttt = os.path.join(tmptarg, aa)
    if os.path.isfile(ttt):
        for bb in range(2):
            fname2 = "%s_%d" % (ttt, bb)
            if not os.path.exists(fname2):
                break
        try:
            if os.path.exists(fname2):
                os.remove(fname2)
            os.rename(ttt, fname2)
        except:
            print("File rename", sys.exc_info())
    try:
        if args.test:
            print("shutil.copytree" , aa, tmptarg)
        else:
            shutil.copy2(aa, tmptarg)
            os.remove(aa)
    except:
        print("copyfile", aa, ttt, sys.exc_info())

def mainfunct():

    if len(sys.argv) > 1 and sys.argv[1] == "-V":
        print(PNAME, "version", VERSION)
        sys.exit()

    global args
    args = parser.parse_args()
    #print(args);  sys.exit()

    if args.version:
        print("pgdel.py Version", version)
        sys.exit()

    if not os.path.isdir(tmptarg):
        os.mkdir(tmptarg)

    for arg in args.delname[0]:
        for aa in glob.glob(arg):
            if args.verbose > 1:
                print("processing:", aa)
            if not os.path.exists(aa):
                if args.verbose:
                    print("'" + aa + "'", "does not exist.")
                    continue

            if os.path.isfile(aa):
                copyfile(aa)
            else:
                copydir(aa)

if __name__ == '__main__':
    mainfunct()

# EOF