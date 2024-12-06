

all: preconf tor

preconf:
	@apt install nginx -y
	@cp nginx.conf /etc/nginx/sites-available/default
	@systemctl restart nginx
	@cp website/index.html /var/www/html/index.nginx-debian.html

tor:
	@rm -rf /home/aartiges/tor_service
	@tor-instance-create mywebsite
	@cat torrc >> /etc/tor/instances/mywebsite/torrc
	@systemctl restart tor@mywebsite
	@sleep 10
	cat /run/tor-instances/mywebsite/data/hostname
