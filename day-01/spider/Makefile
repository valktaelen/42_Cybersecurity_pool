
EXEC	=spider.py
ENV		=./venv
PIP		:= $(ENV)/bin/pip3

all: $(ENV) activate

$(ENV):
	mkdir -p $(ENV)
	python3 -m venv $(ENV)

activate:
	@echo source $(ENV)/bin/activate
	@echo $(PIP) install lxml
	@echo python3 $(EXEC)

