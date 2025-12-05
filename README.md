## Backend setup:
```bash
cd backend
```
macOS / Linux:  
```
python3 -m venv venv
source venv/bin/activate
```

Windows:  
```
python -m venv venv
venv\Scripts\activate
```
Cont.  
```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Create a .env file inside backend.  
1. Create a django secret key and name the variable `DJANGO_SECRETKEY` within the .env. Run the command below and define the variable using the output string.
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
2. Copy and paste into the .env: `DATABASE_URL=postgresql://postgres.jfzmxhnswjpofzfejniy:knightsoftheroundtable@aws-1-us-east-1.pooler.supabase.com:5432/postgres`

### PostgreSQL init:

Create the database  
```sql
CREATE DATABASE smithy;
```
Create a database user with password
```sql
CREATE USER smithy_admin WITH PASSWORD 'KnightsOTRT';
```

Give the user full access to the database
```sql
GRANT ALL PRIVILEGES ON DATABASE smithy TO smithy_admin;
```
Quit
```bash
\q
```
The database may need to be reset if new items are added into the migration. If so run the commands:
```bash
cd backend
python manage.py migrate smithy zero
python manage.py migrate smithy
python manage.py runserver # to start the backend
```

## Frontend Setup
To open website, type into terminal:
```bash
cd frontend
python -m http.server 3000
```
Access site with: `http://localhost:3000/swe%20project.html`  


