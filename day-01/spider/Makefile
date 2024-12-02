
EXEC	=spider.py
ENV		=./venv

all: $(ENV) activate

$(ENV):
	pip3 install venv
	mkdir -p $(ENV)
	python3 -m venv $(ENV)

activate:
	@echo Do the following command:
	@echo source $(ENV)/bin/activate
	@echo pip3 install lxml
	@echo python3 $(EXEC)

