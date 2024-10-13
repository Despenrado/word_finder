## Runnig application:
```
uvicorn app.main:app --host 0.0.0.0 --port 8080
```
You can modify `app/utils/cache.py` to use another redis instance or disable it

## Runnig tests:
```
PYTHONPATH=. pytest 
```

## Docker
```
docker compose -f ./deployment/docker-compose.yml up --build
```
NGINX works on port `8081`

## Swagger
```
http://localhost:8080/docs
```
or when using docker
```
http://localhost:8081/docs
```

## Install and run pre-commit (see `add pre-commit` PR)
```
pip install pre-commit
pre-commit install
```