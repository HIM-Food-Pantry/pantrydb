## Production
Have docker-machine create a new server or use the following to set up a generic server.
 `docker-machine create \
  --driver generic \
  --generic-ip-address=203.0.113.81 \
  --generic-ssh-key ~/.ssh/id_rsa \
  him-pantry`
  
Activate the docker-machine
```docker-machine env him-pantry```

Create directory for Postgres conf and data dir, and Python Logs
```mkdir /him_database && cd /him_database && mkdir ./django ./postgres ./nginx ./nginx-gen```

Build the docker image using docker-compose
```docker-compose build```

Use the following to bring up the Postgres, Django and Nginx up and running preferably locally.
```docker-compose up```
Will run them detached
```docker-compose up -d```


### Running manage.py commands

To create super users or other administrative activie is usign the following command to get into bash.
```docker exec -it django /bin/sh```

```docker exec -it django python3 manage.py migrate```

```docker exec -it django python3 manage.py createsuperuser```

```docker exec -it django python3 manage.py```

### Running Tests
Start the server
```docker-compose up -d```
Run the Tests
```docker-compose -f docker-compose.test.yml run django test```

 
Get the docker-machine ip and set it as an enviormental variable
export DOCKER_MACHINE_IP=$(docker-machine ip)

sed -e "s/DOCKER_MACHINE_IP/$(docker-machine ip default)/g" ../deploy/docker-compose.test.yml | docker-compose --file - up


https://docs.docker.com/v1.5/compose/cli/#run