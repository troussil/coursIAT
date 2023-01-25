TEX=doc.tex
BIB= #refs.bib
PDF=$(TEX:.tex=.pdf)

FIGSRC = $(wildcard *.ipe)
FIGOBJ = $(FIGSRC:.ipe=.pdf)

###################################################

all:  fig ${PDF}

fig: $(FIGOBJ)

%.pdf: %.ipe
	ipetoipe -pdf $<

${PDF}: ${TEX} ${BIB}
	pdflatex  ${TEX}
	# bibtex `basename -s .tex ${TEX}`
	# pdflatex  ${TEX}
	pdflatex  ${TEX}

clean:
	-rm -f ${PDF} *.bak *.blg *.bbl *.out *.aux *~ *.log $(FIGOBJ)

distclean:
	-rm -rf *.pdf *.ps *~ *.log *.bak *.out *.aux *.tar *.tar.gz *.dvi 
