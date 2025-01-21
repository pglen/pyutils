#!/usr/bin/env python3

import  os, sys, getopt, signal, select, socket, time, struct
import  random, stat, os.path, datetime, threading, subprocess
import  struct, io, traceback, hashlib, traceback, argparse
import codecs

base = os.path.dirname(os.path.realpath(__file__))

'''

 String quaruplet per test.  Input format is array of data.

    #   Context_string  Send_string     Expect_string   Find/Compare
    #   --------------  -----------     -------------   ------------
    #    for the user   what to test    what to expect  True if Find

'''

Version = "1.0.0"

def strdiff(expectx, actualx):

    ''' Rudimentary info on string differences '''

    strx = ""
    for cnt, bb in enumerate(expectx):
        #print("cnt", cnt, bb)
        if bb != actualx[cnt]:
            strx = "At pos: %d  [%s]" % (cnt,
                            str(expectx[cnt:cnt+5]))
            break
    return strx

def xdiff(actualx, expectx, findflag):

    ''' Compare values, display string in Color
        Sensitive to find flag.
    '''

    if findflag:
        #print("Find", str(expectx), str(actualx))
        if str(expectx) in str(actualx):
            return "\033[32;1mOK\033[0m"
        else:
            return"\033[31;1mERR\033[0m"

    else:
        if expectx == actualx:
            return "\033[32;1mOK\033[0m"
        else:
            return"\033[31;1mERR\033[0m"

def obtain_response(cmd):

    ''' Get output from command, if any '''

    comm = [0,]
    exec = cmd.split()
    if args.debug > 1:
        print("exec:", exec)

    if exec:
        try:
            ret = subprocess.Popen(exec, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            comm = ret.communicate()
            if args.outp:
                print(codecs.decode(comm[0]).replace("\\n", "\n"))
                sys.stdout.flush()
        except:
            print("Cannot communicate with:", exec, file=sys.stderr)
            print(sys.exc_info())

    return comm[0]

def send_expect(context, sendx, expectx, findflag):

    ''' Evaluate one SEND -- EXPECT sequence '''

    ret = obtain_response(sendx)
    if args.debug > 2:
        print("\033[32;1mGot: ", ret, "\033[0m")

    err = xdiff(ret, expectx, findflag)

    # If no context, we do not want any printing
    if context:
        print(context, "\t", err)

    if args.verbose:
        # On error tell us the expected result
        if ret != expectx:
            print("\033[34;1mGot:\033[0m\n", ret)

    if args.verbose > 1:
        if ret != expectx:
            print("\033[34;1mExpected:\033[0m\n", expectx)

    if args.verbose > 2:
        if ret != expectx:
            print("\033[34;1mDiff:\033[0m\n",
                strdiff(ret, expectx))
    return err

def mainloop():

    global args

    if args.test_cases:
        for fff in args.test_cases:
            try:
                with open(fff) as fp:
                    testx = fp.read()
            except:
                print("Cannot open file", "'" + fff  + "'", file=sys.stderr)
                args.errcnt += 100
                #sys.exit()
                continue
            #print("testx", testx)
            try:
                test_case_code = eval(testx)
            except:
                print("Error in", fff, sys.exc_info(), file=sys.stderr)
                args.errcnt += 1
                continue
            for aa in test_case_code:
                err = send_expect(aa[0], aa[1], aa[2], aa[3])
                #print("err", err)
                if "ERR" in err:
                    args.errcnt += 1

def mainfunct():

    global args

    parser = argparse.ArgumentParser(\
            description='Test send/expect by executing sub commands.')

    parser.add_argument("-V", '--version', dest='version',
                        default=0,  action='store_true',
                        help='Show version number')
    parser.add_argument("-v", '--verbose', dest='verbose',
                        default=0,  action='count',
                        help='increase verbocity (Default: none)')
    parser.add_argument("-d", '--debug', dest='debug',
                        default=0,  type=int, action='store',
                        help='Debug level. Default: off')
    parser.add_argument("-o", '--output', dest='outp',
                        default=0,  action='store_true',
                        help='Show communcation to program. Default: off')
    parser.add_argument("test_cases", nargs= "*",
                        help = "Test case file names to execute")

    args = parser.parse_args()
    #print(args)

    if args.version:
        print("Version: %s" % Version)
        sys.exit(0)

    if not args.test_cases:
        print("Must specify at least one test case file.")
        sys.exit(1)

    args.errcnt = 0
    mainloop()

if __name__ == "__main__":
    mainfunct()
    sys.exit(args.errcnt)

# EOF
