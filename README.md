# EC2 x FastAPI

Leveraging Supervisor + Gunicorn + Nginx to deploy persistent apps/microservices on AWS EC2

### Provision EC2

* AMI: Ubuntu 24.04/22.04 Server (64-bit)
* Allow HTTPS/HTTP traffic from the internet

### EC2 Setup

SSH into your EC2 machine and configure

```
$ sudo apt update && sudo apt install supervisor nginx python3-venv -y
$ sudo systemctl enable supervisor
$ sudo systemctl start supervisor

$ git clone https://github.com/athletedecoded/ec2-fastapi.git
$ cd ec2-fastapi

$ touch .env # set your env vars
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

$ uvicorn main:app
$ curl http://localhost:8000/health # {"ping":"pong"}
```

### Configure Gunicorn

```
$ mkdir run
$ chmod u+x gunicorn_start
```

### Configure Supervisor

```
$ mkdir logs
$ sudo cp supervisor.conf /etc/supervisor/conf.d/app.conf

$ sudo supervisorctl reread # app: available
$ sudo supervisorctl update # app: added process group
$ sudo supervisorctl status app # STARTING

# Wait 1-2 mins
$ sudo supervisorctl status app # RUNNING   pid 41838, uptime 0:00:08
```

### Configure NGINX

Update your `server_name` in `nginx.conf`

```
$ sudo cp nginx.conf /etc/nginx/sites-available/app
$ sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
$ sudo nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
$ sudo systemctl restart nginx
```

### Permissions

```
$ sudo usermod -aG ubuntu www-data
```

### Test App

```
$ curl //ec2-XX-XXX-XXX-XXX.compute-1.amazonaws.com/health # {"ping":"pong"}
```

You should now be able to navigate to your http:// EC2 endpoint and see the Hello, World! landing page.

### Code changes

After code changes you need to restart supervisor

```
sudo supervisorctl restart app
```

---

### References

* [How to Securely Deploy a FastAPI app with NGINX and Gunicorn](https://dylancastillo.co/posts/fastapi-nginx-gunicorn.html)