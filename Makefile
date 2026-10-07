PAPER := paper/factorial_conjecture_two_variables.tex
OUTDIR := output/pdf
PDF := $(OUTDIR)/factorial_conjecture_two_variables.pdf

.PHONY: all test clean

all: $(PDF)

$(PDF): $(PAPER)
	mkdir -p $(OUTDIR)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$(OUTDIR) $(PAPER)

test:
	mkdir -p verification
	python3 scripts/verify_degree6.py
	python3 scripts/verify_identities.py

clean:
	latexmk -C -outdir=$(OUTDIR) $(PAPER)
	rm -rf output
