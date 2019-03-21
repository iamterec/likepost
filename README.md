Run the automated bot:
```shell
docker-compose run --rm bot python bot.py
```

Run tests:
```shell
docker-compose exec api python -m pytest ./tests
```

For migrations:
```shell
docker-compose exec api python migrate.py db init
```
