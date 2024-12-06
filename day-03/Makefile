

all: preconf tor ssh

preconf:
	@apt install nginx -y
	@cp nginx.conf /etc/nginx/sites-available/default
	@systemctl restart nginx
	@cp index.html /var/www/html/index.nginx-debian.html

tor:
	@apt install tor torbrowser-launcher -y
	@rm -rf /home/aartiges/tor_service
	@tor-instance-create mywebsite
	@cat torrc >> /etc/tor/instances/mywebsite/torrc
	@systemctl restart tor@mywebsite
	@sleep 10
	cat /run/tor-instances/mywebsite/data/hostname

ssh:
	@apt install openssh-server -y
	@cat sshd_config > /etc/ssh/sshd_config
	@cat ssh.socket > /lib/systemd/system/ssh.socket
	@systemctl daemon-reload
	@systemctl restart ssh.socket
	@systemctl restart ssh.service
