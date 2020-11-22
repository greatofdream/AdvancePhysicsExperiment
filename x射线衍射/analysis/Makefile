.PHONY: all hunhe
element:=Si NaCl_s NaCl_m Cu diamond graphene Mo hunhewu1 hunhewu2 base
all: $(element:%=../data/%/spectrum.png)
../data/%/spectrum.png: ../data/%/spec.txt ../data/%/spec.pid
	python -X utf8 spectrum.py -e $* -s $< -t $(wildcard ../data/$*/PDF*.txt) -p $(word 2,$^) -o $@ > $@.log
graphite: ../data/graphite/spec.png
../data/%/spec.png: ../data/%/spec.txt
	python -X utf8 spectrum.py -e $* -s $< -t $(wildcard ../data/$*/PDF*.txt) -p -o $@ > $@.log
.DELETE_ON_ERROR:
.SECONDARY: