
EXEC	=spider.py
ENV		=./venv

all: $(ENV) activate

$(ENV):
	mkdir -p $(ENV)
	python3 -m venv $(ENV)

activate:
	@echo Do the following command:
	@echo source $(ENV)/bin/activate
	@echo pip3 install -r requirements.txt
	@echo python3 $(EXEC)

