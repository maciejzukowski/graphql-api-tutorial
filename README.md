# graphql-api-tutorial

Code for the tutorial [Zero to App Store in 1 day - Create a GraphQL API with Flask, SQLAlchemy, PostgreSQL](https://medium.com/@mzuk229/zero-to-app-store-in-1-day-create-a-graphql-api-with-flask-sqlalchemy-postgresql-28dffdea2dbb)

### Quick Start
Make sure you create a new postgres database first.  We'll connect to it with the environment variable DATABASE_URL.    

```
git clone git@github.com:maciejzukowski/graphql-api-tutorial.git
cd graphql-api-tutorial
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PORT=3001
export DATABASE_URL=postgres:///myapp
export SECRET_KEY=XXXGENERETATE_SECRET_KEYXXXX
alembic upgrade head
python app/server.py 
### Open http://127.0.0.1:3001/graphql to see the graphiql explorer
```
