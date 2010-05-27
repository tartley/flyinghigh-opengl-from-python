
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries on the PATH


PACKAGE := flyinghigh
VERSION := `python -c "from ${PACKAGE}.version import version; print version"`
RUN = run.py

clean:
	rm -rf build dist tags pip-log.txt
	-find ${PACKAGE} bin -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

tags:
	ctags -R ${PACKAGE}
.PHONY: tags

stats:
	find ${PACKAGE} -name '*.py' | grep -v '/tests/' | xargs wc -l | sort -g
	find ${PACKAGE} -name '*.py' | grep '/tests/' | xargs wc -l | sort -g
.PHONY: stats

profile:
	python -O -m cProfile -o profile.out ${RUN}
	runsnake profile.out
.PHONY: profile

alltests:
	nosetests ${PACKAGE}
.PHONY: alltests

py2exe:
	rm -rf dist/${PACKAGE}
	python setup.py --quiet py2exe
.PHONY: py2exe

