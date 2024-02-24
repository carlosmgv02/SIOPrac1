# SIO PRAC 1
## Authors
* Genís Martínez
* Carlos Martínez

## Setup
### 1. Start the database container
```bash
docker run --name postgreSIO -e POSTGRES_PASSWORD=sio_bd -e POSTGRES_DB=SIO_bd -d -p 5432:5432 postgres
```

### 2. Start the data processing
```bash
python3 main.py
```
