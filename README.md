## How to run this
To run this application you need to have Docker and Docker Compose installed.

Rename:
*  *`db/.env_example`*  file to *`.env`*
*  *`celery/config/secret_example.py`* file to *`secret.py`*
*  *`likepost/config/secret_example.py`* file to *`secret.py`*

Migrate the database with:
```shell
docker-compose exec api python migrate.py db init
docker-compose exec api python migrate.py db migrate
docker-compose exec api python migrate.py db upgrade
```

Then you can run the application with:
```shell
docker-compose up
```

Run the automated bot:
```shell
docker-compose run --rm bot python bot.py
```

Run tests:
```shell
docker-compose exec api python -m pytest ./tests
```


### Clearbit enrichment and emailhunter
To use clearbit.com/enrichment and emailhunter:<br/>
*  Fill API keys in *`celery/config/secret.py`*
*  Than change `USE_CLEARBIT` and `USE_EMAILHUNTER` variables to *`True`* in *`likepost/config/general.py`*
