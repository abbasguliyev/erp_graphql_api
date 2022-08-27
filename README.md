# kodazeCRM

## Install
git clone https://github.com/abbasguliyev/kodazeCRM.git \
cd kodazeCRM \
docker-compose build \
docker-compose run --rm web python3 manage.py migrate
docker-compose run --rm web python3 manage.py createsuperuser
## Run
docker-compose up