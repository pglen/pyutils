#!/usr/bin/python

# A simpler version of comment extractor

import os, sys, string, re, argparse

#if len(sys.argv) <= 1:
#    print("Extract comments from files.")
#    print("Use: pycomm.py file(s)");
#    sys.exit(0);

# Regular expressions to search for:

rexn   = re.compile("(.*///////)|(.*//[!/])");
rexall = re.compile(".*//[\<\>]");

rexbeg = re.compile(" *//.*\{");
rexend = re.compile(" *//.*\}");

rexcodebeg = re.compile(" *//.*\[");
rexcodeend = re.compile(" *//.*\]");

bsend = re.compile(".*\\\\$");

rexname = re.compile(".*\\\\name ");
rexdesc = re.compile(".*\\\\desc ");
rexfile = re.compile(".*\\\\file ");
rexparm = re.compile(".*\\\\parm ");
rexretu = re.compile(".*\\\\retu ");
rexfunc = re.compile(".*\\\\func ");

def mainloop():

    for aa in args.files:

        if args.verbose:
            print("Extracting:", aa)
        #continue

        fpi = open(aa, "r")
        fpo = open(aa + ".html", "w")

        cb = 0; bf = 0; bhead = 0

        #print("<h1>Project: %s" % os.path.basename(aa) + "</h1>", file=fpo)

        stash = ""

        for aaa in fpi:
            bbb2 = aaa.replace("\r", "");
            bbb = bbb2.replace("\n", "");

            if stash != "":
                rrr = rexn.match(bbb)
                if rrr:
                    bbb = stash + bbb[rrr.end():];
                else:
                    bbb = stash

            #if bbb == "":
            #    continue

            if bsend.match(bbb):
                #print ("backslash at end, ");
                stash = bbb[:-1]
                continue
            else:
                stash = ""

            if rexall.match(bbb):
                print("%s<br>" % bbb, file=fpo)
                continue

            if rexend.match(bbb):
                bf = 0
            else:
                if bf:
                    #print("bf line: '%s'" % bbb)
                    rmx3 = rexn.match(bbb)
                    if rmx3:
                        print("%s" % bbb[rmx3.end():] + "<br>", file=fpo)
                else:
                    if not rexbeg.match(bbb) and not rexend.match(bbb):
                        rmx = rexn.match(bbb)
                        if rmx:
                            got = 0
                            rmx2 = rexname.match(bbb)
                            if rmx2:
                                print("<h3>Name: %s" % bbb[rmx2.end():]+"</h3>", file=fpo)
                                got = 1

                            rmx2 = rexfile.match(bbb)
                            if rmx2:
                                print("<h2>File: %s" % bbb[rmx2.end():] + "</h2>", file=fpo)
                                got = 1

                            rmx2 = rexdesc.match(bbb)
                            if rmx2:
                                print("Description: %s" % bbb[rmx2.end():] + "<br>", file=fpo)
                                got = 1
                            rmx2 = rexparm.match(bbb)
                            if rmx2:
                                print("Parameters: %s" % bbb[rmx2.end():] + "<br>", file=fpo)
                                got = 1
                            rmx2 = rexretu.match(bbb)
                            if rmx2:
                                print("Return: %s" % bbb[rmx2.end():] + "<br>", file=fpo)
                                got = 1
                            rmx2 = rexfunc.match(bbb)
                            if rmx2:
                                print("<b>Function: %s" % bbb[rmx2.end():] + "</b><br>", file=fpo)
                                got = 1
                            if got == 0:
                                print("%s" % bbb[rmx.end():] + "<br>", file=fpo)

            if rexbeg.match(bbb):
                bf = 1

            if rexcodeend.match(bbb):
                cb = 0

            if cb:
                print("%s" % bbb + "<br>", file=fpo)

            if rexcodebeg.match(bbb):
                cb = 1

# ------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Extract comments from files.')

parser.add_argument("-v", '--verbose', dest='verbose',
                    default=0,  action='count',
                    help='verbocity on (default: off)')

parser.add_argument("-d", '--debug', dest='debug',
                    default=0,  type=int, action='store',
                    help='Debug level')

parser.add_argument("-t", '--test', dest='testx',
                    default=0,  action='store_true',
                    help='Test what would be done.')

parser.add_argument(dest='files', nargs="*",
                    default=0,  type=str, action='store',
                    help='File names.')

# ------------------------------------------------------------------------

def mainfunct():

    global args
    args = parser.parse_args()
    #print(args)
    mainloop()

if __name__ == "__main__":
    mainfunct()

# EOF
