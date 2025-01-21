#!/usr/bin/env python

import os, sys, glob, string, time,  traceback, getopt, random
import subprocess, fnmatch, shlex

''' Iterate every python file in project '''

#sys.path.append('pyvcommon')

#import comline, support, pysyslog

version = "1.2.0"

conf = []
relarr = []
rel = "."
sumstr = ""

# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class
# This allows a lot of sub utils to have a common set of options.

class Config:

    def __init__(self, optarr):

        ddd = self.dupoptcheck(optarr)
        if ddd:
            raise ValueError("Duplicate options on comline.", ddd)

        global glsoptarr
        glsoptarr = optarr

        self.optarr = optarr
        self.verbose = False
        self.debug = False
        self.sess_key = ""

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            optletters += aa[0]
        #print( optletters    )
        # Create defaults:
        err = 0
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError as err:
            print( "Invalid option(s) on command line:", err)
            raise
            return ()
        except:
            print(sys.exc_info())

        #print( "opts", opts, "args", args)
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print( "match", aa, self.optarr[bb])
                    if len(self.optarr[bb][0]) > 1:
                        #print( "arg", self.optarr[bb][1], aa[1])
                        if self.optarr[bb][2] != None:
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print( "set", self.optarr[bb][1], self.optarr[bb][2])
                        if self.optarr[bb][2] != None:
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print( "call", self.optarr[bb][3])
                        if self.optarr[bb][3] != None:
                            self.optarr[bb][3]()
        return args

    def dupoptcheck(self, optarr):
        optdup = {}
        for bb in range(len(optarr)):
            kkk = optarr[bb][0][0]
            try:
                optdup[kkk] += 1
            except KeyError:
                optdup[kkk] = 1
            except:
                print(sys.exc_info())
        #print(optdup)
        found = False
        for cc in optdup.keys():
            if optdup[cc] > 1:
                #print("found dup", cc)
                found = cc
        return found


def gotfile(fname):

    global sumstr, conf

    #if conf.filter != "":
    #    if not conf.filter in fname:
    #        return

    basename = os.path.split(fname)[1]

    if conf.wild != "":
        #print(fname, conf.wild)
        if not fnmatch.fnmatch(basename, conf.wild):
            return

    if conf.exclude:
        for aa in conf.exclude:
            if fnmatch.fnmatch(basename, aa):
                return

    if conf.verbose:
        print ("file:", fname)

    eee = os.path.splitext(fname)
    #print(eee)

    # Filter non py files
    #if eee[1] != ".py":
    #    return

    # Filter extensions
    gotext = [".pyc", ".o", ".so", ".pem", ".pub", ]
    for aa in gotext:
        if aa == eee[1]:
            return

    # Filter common garbage names
    gotfname = ["__pycache__", "checksums", ]
    for bb in gotfname:
        if bb in fname:
            return

    if conf.sum:
        try:
            ret = subprocess.check_output(["sha256sum", fname])
            #print("ret", ret, end="")
        except:
            ret = "Cannot sum file: %s\n", fname
            print(ret)
        sumstr += ret.decode()  #+ b'\r\n'

    elif conf.xexec != "":
        xxx = shlex.split(conf.xexec)
        xxx.append(fname)
        if conf.verbose:
            print ("executing:", xxx)
        try:
            ret = subprocess.check_output(xxx)
            print(ret.decode(), end = "") #, end="")
        except subprocess.CalledProcessError as err:
            if conf.showret:
                ret = "Ret code of '%s %s' = %d" % \
                            (conf.xexec, fname, err.returncode)
                print(ret.decode())
        except:
            ret = "Cannot execute '%s' on: %s" % \
                        (conf.xexec, fname)
            print("dd", ret.decode())
    else:
        print (fname )

    #if ret.returncode:
    #    print ("camnnot exec", fname)

def listit():
    global rel

    arr = glob.glob(rel + "/*")
    #print(arr)

    for aa in arr:
        bb = rel + "/" + os.path.basename(aa)
        if not os.path.isdir(bb):
            gotfile(bb)

    for aa in arr:
        #print ("aa", aa)
        bb = rel + "/" +  os.path.basename(aa)
        if os.path.isdir(bb):
            #print  ("got dir", bb)

            was = False
            for cc in conf.excdir:
                #print("dirmtch", cc, os.path.basename(aa))
                if fnmatch.fnmatch(os.path.basename(aa), cc):
                    was = True
                    break
            if was:
                continue
            relarr.append(rel)
            rel += "/" + os.path.basename(aa)
            listit();
            rel = relarr.pop()

        else:
            #print  ("file", os.getcwd(), aa)
            #gotfile(rel + "/" + aa)
            pass

    # option, var_name, initial_val, function

# ------------------------------------------------------------------------
# Functions from command line

def phelp():

    print()
    print( "Usage: " + os.path.basename(sys.argv[0]) + " [options] startdir")
    print()
    print( "Execute options on every selected file in subtree. Default is to ")
    print( "print file names.")
    print()
    print( "Options:    -d level    - Debug level 0-10")
    print( "            -v          - Verbose, show file names.")
    print( "            -V          - Version.")
    print( "            -q          - Quiet.")
    print( "            -x exclude  - Exclude files.")
    print( "            -u excdir   - Exclude dir.")
    print( "            -w          - filter file names (wild card)")
    print( "            -e prog     - Execute prog on file.")
    print( "            -r          - Show prog exec exit code.")
    print( "            -m          - Generate SHA256 sum.")
    print( "            -h          - Show Help.")
    print()
    print("Use quotes for options with spaces.")
    print()
    sys.exit(0)


def pversion():
    print( os.path.basename(sys.argv[0]), "Version", version)
    sys.exit(0)

optarr = \
    ["d:",  "pgdebug",  0,      None],      \
    ["e:",  "xexec",    "",     None],      \
    ["x:",  "exclude",  "",     None],      \
    ["u:",  "excdir",   "",     None],      \
    ["w:",  "wild",     "",     None],      \
    ["v",   "verbose",  0,      None],      \
    ["r",   "showret",  0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     "x",    None],      \
    ["m",   "sum",      0,      None],      \
    ["s",   "showkey",  "",     None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \

conf = Config(optarr)

# ------------------------------------------------------------------------

def mainfunc():

    args = conf.comline(sys.argv[1:])

    if conf.verbose:
        print("args", args)

    if conf.debug > 4:
        print(conf)

    if len(args):
        os.chdir(args[0])

    if conf.exclude:
        conf.exclude = shlex.split(conf.exclude)
        print("exclude", conf.exclude)

    if conf.excdir:
        conf.excdir = shlex.split(conf.excdir)
        print("excdir", conf.excdir)

    listit()

    if conf.sum:
        print (sumstr, end="")

    #if conf.xexec != "":
    #    print ("xexec", conf.xexec)

if __name__ == '__main__':
    mainfunc()

# EOF