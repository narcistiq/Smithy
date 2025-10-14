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