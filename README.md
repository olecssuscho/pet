Just pet project where i was trainig back-end skills

git clone https://github.com/olecssuscho/pet.git

launch
docker-compose up --build

SECRET_KEY=
DATABASE_URL=
ALGORITHM=HS256

POST /user/register  — registration
POST /user/login     — login
GET  /task/get_all   — all tasks
POST /task/post      — create task
PUT  /task/put       — update task
DELETE /task/delete  — delete task

what i use
FastApi,SQLAlchemy,PostgreSQL,Alembic,Docker