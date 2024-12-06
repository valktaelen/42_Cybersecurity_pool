

preconf:
	apt install nginx -y
	cp nginx.conf /etc/nginx/sites-available/default
	systemctl restart nginx
	mkdir -p /home/aartiges/tor_service
	cp website/index.html /var/www/html/index.nginx-debian.html

tor:
	mkdir -p /home/aartiges/tor_service
	mv torrc /etc/tor/torrc
	systemctl restart tor
	sleep 30
	cat /home/aartiges/tor_service/hostname
