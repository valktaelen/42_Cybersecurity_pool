
COMPOSE_DEV=docker-compose-dev.yml
COMPOSE=docker-compose.yml

re_dev: down_dev up_dev

re: down up

up:
	docker compose -f $(COMPOSE) up -d --build
	@$(MAKE) infos

down:
	docker compose -f $(COMPOSE) down -v

logs:
	docker compose -f $(COMPOSE) logs -f

up_dev:
	docker compose -f $(COMPOSE_DEV) up -d --build
	@$(MAKE) infos

down_dev:
	docker compose -f $(COMPOSE_DEV) down -v

logs_dev:
	docker compose -f $(COMPOSE_DEV) logs -f

infos:
	@docker inspect -f '{{.Name}} {{range.NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_serv
	@docker inspect -f '{{.Name}} {{range.NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_client
	@docker inspect -f '{{.Name}} {{range.NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' inquisitor
	@echo docker exec -it inquisitor sh
	@echo python3 inquisitor.py $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_serv) $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_client)
