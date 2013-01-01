import commands
import time


for i in range(10000):
	b=commands.getoutput('bibtex Main.aux')
	print b
	a=commands.getoutput('pdflatex Main.tex')
	print a
	time.sleep(20)
	c=commands.getoutput('clear')
