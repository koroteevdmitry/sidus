# Test task for Sidus

1. For run docker container with project use command:
```bash
1. cat docker-compose.env.example > .env
2. docker-compose up -d --build
4. docker-compose exec web alembic upgrade head
3. Check http://localhost:8000 or docker-compose ps if something wrong
```

2. For run project without docker use command:
```bash
1. cd app/requrements
2. pip install -r development.txt
3. cd app/core && cat .env.example > .env
4. run alembic upgrade head
5. start server.py
6. start celery worker by command: celery worker --app=worker.celery