

all: preconf tor

preconf:
	apt install nginx -y
	cp nginx.conf /etc/nginx/sites-available/default
	systemctl restart nginx
	cp website/index.html /var/www/html/index.nginx-debian.html

tor:
	rm -rf /home/aartiges/tor_service
	cp torrc /etc/tor/torrc
	chown root:root /etc/tor/torrc
	systemctl restart tor
	sleep 30
	cat /home/aartiges/tor_service/hostname
