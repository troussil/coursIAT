LOG=evince
TEX=cours

FIGSRC = $(wildcard fig/*.ipe)
FIGOBJ = $(FIGSRC:.ipe=.pdf)

all: fig slides

fig: $(FIGOBJ)

fig/%.pdf: fig/%.ipe
	ipetoipe -pdf $<

slides:
	pdflatex $(TEX).tex
	pdflatex $(TEX).tex

show:
	$(LOG) $(TEX).pdf

clean:
	rm -f *.log *.toc *.aux *.nav *.snm *.out *.bbl *.blg *.dvi
	rm -f *.backup *~
	rm -f $(FIGOBJ)

proper:	proper
	rm -f $(TEX).ps $(TEX).pdf
