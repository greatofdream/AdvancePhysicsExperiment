.PHONY: all
all: 1/Jacobi.h5 1/GS.h5 1/SOR.h5 1/SORbest.h5 1/iteration.png
1/%.h5: inputEquation.csv
	mkdir -p $(dir $@)
	python solveEquation.py -i 0 0 0 -e $< -m $* -o $@ -w 0.8 1 1.2 1.4 1.6 > $@.log
1/iteration.png: 1/Jacobi.h5 1/GS.h5 1/SOR.h5 1/SORbest.h5
	python comparePlot.py -i $^ -o $@ -w 0.8 1 1.2 1.4 1.6 > $@.log 2>&1
2/%100.h5:
	mkdir -p $(dir $@)
	python solveSparseEquation.py -n 100 -i 0 0 0 -m $* -o $@ > $@.log 2>&1
2/%10000.h5:
	mkdir -p $(dir $@)
	python solveSparseEquation.py -n 10000 -i 0 0 0 -m $* -o $@ > $@.log 2>&1
2/iteration%.png: 2/Jacobi%.h5 2/CG%.h5
	python compareSparsePlot.py -i $^ -o $@ > $@.log 2>&1
3/%.h5: inputEquation2.csv
	mkdir -p $(dir $@)
	python solveNoSymEquation.py -i 0 0 0 -e $< -m $* -o $@ > $@.log
3/iteration.png: 3/CG.h5
	python compareNoSymPlot.py -i $^ -o $@ > $@.log 2>&1
.DELETE_ON_ERROR: