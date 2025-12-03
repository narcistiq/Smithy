## Backend setup:
cd backend

macOS / Linux:
python3 -m venv venv

source venv/bin/activate

Windows:
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

PostgreSQL init:

-- Create the database
CREATE DATABASE smithy;

-- Create a database user with password
CREATE USER smithy_admin WITH PASSWORD 'KnightsOTRT';

-- Give the user full access to the database
GRANT ALL PRIVILEGES ON DATABASE smithy TO smithy_admin;

--quit
\q

--The database may need to be reset if new items are added into the migration. If so run the commands:
cd backend

python manage.py migrate smithy zero

python manage.py migrate smithy

python manage.py runserver # to start the backend

--To open website, type into terminal:

cd frontend

python -m http.server 3000

--Access site with
http://localhost:3000/swe%20project.html


