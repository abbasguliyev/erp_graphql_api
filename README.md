# kodazeCRM

## Install
git clone https://github.com/abbasguliyev/erp_graphql_api.git \
cd app \
docker-compose build \
docker-compose run --rm web python3 manage.py migrate
docker-compose run --rm web python3 manage.py createsuperuser
## Run
docker-compose up