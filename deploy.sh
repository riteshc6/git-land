#! /bin/bash
sudo apt update
sudo apt install python3-pip
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo apt install redis
sudo apt install nginx
pip3 install gunicorn
sudo bash -c 'cat > \.env <<EOF
DATABASE_URL='postgresql://postgres:postgres@youtube.clejaeyrxoaa.ap-south-1.rds.amazonaws.com'
EOF'
sudo bash -c 'cat >  /etc/nginx/conf.d/virtual.conf <<EOF
server {
    listen       80;
    server_name  13.233.31.67;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
client_max_body_size 20M;
EOF'
sudo service nginx restart
python manage.py migrate
sudo bash -c 'cat > /etc/systemd/system/git-land.service <<EOF
[Unit]
Description=GitLand web application
After=network.target

[Service]
User=gitlab
WorkingDirectory=/home/gitlab/git-land
ExecStart=/home/gitlab/git-land/venv/bin/gunicorn -b 0.0.0.0:80 -w 4 mysite.wsgi:application
Environment=DATABASE_URL=postgresql://postgres:postgres@youtube.clejaeyrxoaa.ap-south-1.rds.amazonaws.com
Restart=always

[Install]
WantedBy=multi-user.target
EOF'
sudo systemctl daemon-reload
sudo systemctl start git-land
sudo bash -c 'cat > /etc/systemd/system/celery.service << EOF
[Unit]
Description=Gitland task worker
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/gitlab/git-land
ExecStart=/home/gitlab/git-land/venv/bin/celery -A mysite worker -l info
Environment=DATABASE_URL=postgresql://postgres:postgres@youtube.clejaeyrxoaa.ap-south-1.rds.amazonaws.com
Restart=always

[Install]
WantedBy=multi-user.target
EOF'
sudo systemctl daemon-reload
sudo systemctl start celery
