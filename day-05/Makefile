
EXEC	= stockholm.py
ENV		= ./venv
SHELL := /bin/bash

all: $(ENV) activate

$(ENV):
#	python3 -m pip install virtualenv
	mkdir -p $(ENV)
	python3 -m venv $(ENV)

activate:
	source $(ENV)/bin/activate && pip3 install -r requirements.txt
	@echo Do the following command:
	@echo source $(ENV)/bin/activate
	@echo python3 $(EXEC)

