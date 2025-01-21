# misc pyutils

 These utils are developed out of suffering ... no more.

## Need to rename like this:

 figure001.txt --- figure100.txt image001.jpg -- image100.txt just do:

     ./bulkren.py -f figure*.txt  -o image

## Need to change "import sockets" to "import mysockets":

in every python file in the current dir just do:

    ./chall.py "import sockets" "import mysockets" *.py

   Not sure what to expect? Add the -t option for "test", so the program can
 show you what it would do.

## A nifty utility to test things.

 The test case file drives an send expect engine. The expect is then evaluated and
the result is printed in a green colored 'OK' or a red colored 'ERR'.

    ./testdrive.py testcase.txt

The test case file contains the test instructions, one line per test. The format:

    #   Context_string  Send_string     Expect_string   Find/Compare
    #   --------------  -----------     -------------   ------------
    #    for the user   what to test    what to expect  True if Find

### The output of test cases:

    Echo Command     	 OK
    Test ls          	 OK
    DF command       	 OK
    DF mregex        	 OK

## Summary:

| File          |          Description              |   Notes   |
| ------------- | --------------------------------  |  -------  |
|bulkren.py     |  Rename files in balk             |           |
|chall.py       |  Change string in maching files   |           |
|isnewer.py     |  Is file newer than reerence      |           |
|iterproj.py    |  Iterate current dir and subdirs  |           |
|pgdel.py       |  Delete by moving to temp dir     |           |
|pycomm.py      |  Extract comments                 |           |
|testdrive.py   |  Test executable by send / expect |           |
|README.md      |  This file                        |           |

// EOF
