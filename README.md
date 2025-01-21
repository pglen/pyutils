# misc pyutils

 These utils are developed out od suffering ... no more. Need to rename
 figure001.txt --- figure100.txt image001.jpg -- image100.txt just do:

     ./bulkren.py -f figure*.txt  -o image

 need to change "import sockets" to "import mysockets" in every python file
 in the current dir just do:

    ./chall.py "import sockets" "import mysockets" *.py

   Not sure what to expect? Add the -t option for "test", so the program can
 show you what it would do.

| File                    Description                   Notes   |
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
