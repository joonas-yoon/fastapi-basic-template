# FastAPI basic template

FastAPI + JWT + MongoDB

## Set up

Create your own virtual environment, and install module dependencies:

```
pip install -r requirements.txt
```

## Run

To load ASGI app

```
uvicorn main:app --reload
```

The above command refers to:

- `main`: the file `main.py` (the Python "module").
- `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
- `--reload`: make the server restart after code changes. Only use for development.

## Directory

```
root/
├── configs
│   └── __init__.py
├── controllers
│   ├── auth.py
│   ├── db.py
│   └── users.py
├── crud
│   ├── base.py
│   └── user.py
├── models
│   ├── Auth.py
│   └── User.py
├── routes
│   ├── __init__.py
│   ├── auth.py
│   └── users.py
├── .env.dev
└── main.py
```

make your .env file as like:

```
DEBUG=true
SECRET_KEY=64965e9c9a7a903185a2fddffdaee41f5c4f245f1354dfb78ab629845b3129fd
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
USERPROFILE_DOC_TYPE=userprofile
DB_HOST=127.0.0.1:27017
DB_DATABASE=testdb
DB_URL=mongodb://${DB_HOST}/
```

you can get a string from this command: `openssl rand -hex 32`

## Docs

### Interactive API docs

http://127.0.0.1:8000/docs

You will see the automatic interactive API documentation (provided by Swagger UI)

### Generated API Docs

http://127.0.0.1:8000/redoc

You will see the alternative automatic documentation (provided by ReDoc)

## References

Documentation for FastAPI framework: https://fastapi.tiangolo.com/
