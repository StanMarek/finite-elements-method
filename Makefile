run:
	python3 src/main.py

clean:
	rm src/**/__pycache__/*  
	rm src/__pycache__/*  
	rm simulation_output/*
	rmdir src/**/__pycache__  
	rmdir src/__pycache__
	rmdir simulation_output
	