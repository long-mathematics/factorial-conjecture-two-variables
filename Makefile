PAPER := paper/factorial_conjecture_two_variables.tex
OUTDIR := output/pdf
PDF := $(OUTDIR)/factorial_conjecture_two_variables.pdf

.PHONY: all clean

all: $(PDF)

$(PDF): $(PAPER)
	mkdir -p $(OUTDIR)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$(OUTDIR) $(PAPER)

clean:
	latexmk -C -outdir=$(OUTDIR) $(PAPER)
	rm -rf output
