PAPER := paper/factorial_conjecture_two_variables.tex
OUTDIR := output/pdf
PDF := $(OUTDIR)/factorial_conjecture_two_variables.pdf
LOG := $(OUTDIR)/factorial_conjecture_two_variables.log
LATEXMK ?= latexmk

.PHONY: all test check snapshot snapshot-check clean

all:
	mkdir -p $(OUTDIR)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -outdir=$(OUTDIR) $(PAPER)
	python3 scripts/check_latex_log.py $(LOG)

test:
	mkdir -p verification
	python3 scripts/verify_degree6.py
	python3 scripts/verify_identities.py
	python3 scripts/verify_supplementary.py
	python3 -m unittest discover -s scripts -p 'test_*.py' -v

snapshot: all
	python3 scripts/check_pdf_snapshot.py --write

snapshot-check:
	python3 scripts/check_pdf_snapshot.py --check

check: test all snapshot-check

clean:
	$(LATEXMK) -C -outdir=$(OUTDIR) $(PAPER)
	rm -rf output
