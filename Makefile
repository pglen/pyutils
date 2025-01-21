# pyutils

all:
	echo Targets: copy docs

copy:
	cp -au *.py ~/pgbin

docs:
	echo Make docs

git:
	git add .
	git commit -m AutoCommit
	git push

# EOF