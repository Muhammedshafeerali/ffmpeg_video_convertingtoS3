cd /home/ubuntu/myproject/deploymentcicd

# Pull the changes
git pull

# Makemigrations and migrate
myprojenv/bin/python manage.py makemigrations
myprojenv/bin/python manage.py migrate

# Collectstatic
myprojenv/bin/python manage.py collectstatic --noinput

# Restart gunicorn and reload nginx
systemctl restart gunicorn
systemctl reload nginx