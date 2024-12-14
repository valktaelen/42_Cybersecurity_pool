
re: down up

up:
	docker compose up -d --build
	@docker inspect -f '{{.Name}} {{range.NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_serv
	@docker inspect -f '{{.Name}} {{range.NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_client
	@docker inspect -f '{{.Name}} {{range.NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' inquisitor
	@echo docker exec -it inquisitor sh
	@echo python3 inquisitor.py $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_serv) $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{.MacAddress}}{{end}}' ftp_client)

down:
	docker compose down -v

logs:
	docker compose logs -f
