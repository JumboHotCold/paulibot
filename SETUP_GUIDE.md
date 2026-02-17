# PauliBot Setup and Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying PauliBot with PostgreSQL in Docker containers. Follow these instructions to set up the production-ready chatbot system for your thesis defense.

---

## Prerequisites

Before starting, ensure you have the following installed on your system:

1. **Docker Desktop** (Windows)
   - Download: https://www.docker.com/products/docker-desktop
   - Version: Latest stable release
   - Includes: Docker Engine + Docker Compose

2. **Git** (for version control)
   - Download: https://git-scm.com/download/win

3. **Python 3.11+** (optional, for local development without Docker)

---

## Installation Steps

### Step 1: Install Docker Desktop

1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Run the installer and follow the setup wizard
3. Restart your computer if prompted
4. Open Docker Desktop and wait for it to start
5. Verify installation:
   ```powershell
   docker --version
   docker compose version
   ```

### Step 2: Navigate to Project Directory

```powershell
cd c:\Dex\CAPSTONE\paulibot
```

### Step 3: Review Environment Variables

Open `.env` file and update the following:

```env
# IMPORTANT: Change these values for production!
POSTGRES_PASSWORD=YourSecurePasswordHere123!
DJANGO_SECRET_KEY=your-django-secret-key-generate-new-one
```

**Generate a new Django secret key:**
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Build and Start Docker Containers

```powershell
# Build and start all services
docker compose up -d --build

# Expected output:
# [+] Building ...
# [+] Running 3/3
#  ✔ Network paulibot_paulibot_network  Created
#  ✔ Container paulibot_postgres        Started
#  ✔ Container paulibot_web              Started
```

### Step 5: Verify Containers are Running

```powershell
docker compose ps

# Expected output:
# NAME                  STATUS    PORTS
# paulibot_postgres     Up        0.0.0.0:5432->5432/tcp
# paulibot_web          Up        0.0.0.0:8000->8000/tcp
```

### Step 6: Check Application Logs

```powershell
# View Django application logs
docker compose logs -f web

# You should see:
# "Applying migrations..."
# "Django version 4.2.x"
# "Starting gunicorn..."
# "Listening at: http://0.0.0.0:8000"
```

### Step 7: Create a Superuser (Admin Account)

```powershell
docker compose exec web python manage.py createsuperuser

# Follow the prompts:
# Student ID: ADMIN-001
# Username: admin
# Email: admin@spus.edu.ph
# Password: [enter secure password]
# Password (again): [confirm password]
```

### Step 8: Access the Application

Open your web browser and navigate to:
- **Main Application**: http://localhost:8000
- **Django Admin Panel**: http://localhost:8000/admin

---

## Using the Application

### For Authenticated Students

1. **Register a New Account**

   Send POST request to `/api/register`:
   
   ```bash
   curl -X POST http://localhost:8000/api/register \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": "2024-00001",
       "username": "juandelacruz",
       "password": "SecurePass123!",
       "email": "juan@spus.edu.ph",
       "first_name": "Juan",
       "last_name": "Dela Cruz"
     }'
   ```

2. **Login**

   Send POST request to `/api/login`:
   
   ```bash
   curl -X POST http://localhost:8000/api/login \
     -H "Content-Type: application/json" \
     -c cookies.txt \
     -d '{
       "username": "juandelacruz",
       "password": "SecurePass123!"
     }'
   ```

3. **Send Chat Message (Saved to Database)**

   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -b cookies.txt \
     -d '{
       "message": "Where is the library?"
     }'
   ```
   
   Response:
   ```json
   {
     "response": "LOCATION:\nName: Learning Resource Center...",
     "saved": true,
     "user": "juandelacruz"
   }
   ```

4. **View Chat History**

   ```bash
   curl -X GET http://localhost:8000/api/history \
     -H "Content-Type: application/json" \
     -b cookies.txt
   ```

### For Guest Visitors

**Send Chat Message (NOT Saved to Database)**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What courses do you offer?"
  }'
```

Response:
```json
{
  "response": "GENERAL INFORMATION:\nWe offer programs in...",
  "saved": false,
  "user": "guest"
}
```

**Key Difference**: Notice `"saved": false` - this message is NOT stored in the database.

---

## Database Verification

### View PostgreSQL Tables

```powershell
# Access PostgreSQL shell
docker compose exec postgres psql -U paulibot_user -d paulibot_db

# Inside PostgreSQL shell:
\dt  # List all tables

# Expected tables:
# chatbot_customuser
# chatbot_chathistory
# django_session
# auth_* (Django authentication tables)
```

### Query User Data

```sql
-- View all registered users
SELECT id, student_id, username, email, date_joined
FROM chatbot_customuser;

-- Verify password is hashed
SELECT username, password
FROM chatbot_customuser
WHERE username = 'juandelacruz';

-- Expected output: password starts with "pbkdf2_sha256$..."
```

### Query Chat History

```sql
-- View all chat history
SELECT u.username, ch.message, ch.response, ch.timestamp
FROM chatbot_chathistory ch
JOIN chatbot_customuser u ON ch.user_id = u.id
ORDER BY ch.timestamp DESC;

-- Expected: Only authenticated user messages appear here
-- Guest messages should NOT appear
```

Exit PostgreSQL shell:
```sql
\q
```

---

## Stopping and Restarting the Application

### Stop Containers

```powershell
docker compose down

# This stops and removes containers but KEEPS your data
# (PostgreSQL data persists in the 'postgres_data' volume)
```

### Restart Containers

```powershell
docker compose up -d

# No need to rebuild unless code changes
```

### View Logs

```powershell
# All logs
docker compose logs -f

# Only web service logs
docker compose logs -f web

# Only postgres logs
docker compose logs -f postgres
```

---

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use:

**Option 1**: Stop the conflicting service

**Option 2**: Change ports in `docker-compose.yml`:
```yaml
services:
  web:
    ports:
      - "8001:8000"  # Change 8000 to 8001
  postgres:
    ports:
      - "5433:5432"  # Change 5432 to 5433
```

### Database Connection Error

If Django cannot connect to PostgreSQL:

1. Check if postgres container is running:
   ```powershell
   docker compose ps
   ```

2. Check postgres logs:
   ```powershell
   docker compose logs postgres
   ```

3. Verify environment variables in `.env`

### Migration Errors

If you encounter migration errors:

```powershell
# Delete and recreate migrations
docker compose exec web python manage.py migrate --run-syncdb

# OR start fresh with a new database:
docker compose down -v  # WARNING: This deletes ALL data
docker compose up -d --build
```

---

## For Thesis Defense Demonstration

### Prepare Demo Data

1. **Create Test Users**:
   - Student 1: student_id=2024-00001, username=student1
   - Student 2: student_id=2024-00002, username=student2

2. **Generate Chat History**:
   - Login as student1
   - Ask 3-5 questions (e.g., locations, staff, courses)
   - Logout and login again to show history persistence

3. **Demonstrate Guest Access**:
   - Open new incognito browser
   - Send chat messages without login
   - Show that history is NOT saved

### Key Talking Points

1. **Security**:
   - "Passwords are hashed using PBKDF2 with 600,000 iterations"
   - Show hashed password in database

2. **Hybrid Access**:
   - "Authenticated students: conversations saved for continuity"
   - "Guest visitors: transient sessions for privacy"

3. **Production Ready**:
   - "Docker containerization for reproducible deployment"
   - "PostgreSQL for scalable, production-grade data storage"
   - "Separated configuration via environment variables"

4. **Database Design**:
   - "Foreign key relationships between Users and ChatHistory"
   - "CASCADE delete ensures data integrity"
   - "Indexed timestamps for fast query performance"

---

## Backup and Export

### Backup PostgreSQL Database

```powershell
# Create backup
docker compose exec postgres pg_dump -U paulibot_user paulibot_db > backup.sql

# Restore from backup
docker compose exec -T postgres psql -U paulibot_user -d paulibot_db < backup.sql
```

### Export Chat History (CSV)

```powershell
docker compose exec postgres psql -U paulibot_user -d paulibot_db -c "\COPY (SELECT u.username, ch.message, ch.response, ch.timestamp FROM chatbot_chathistory ch JOIN chatbot_customuser u ON ch.user_id = u.id ORDER BY ch.timestamp) TO '/tmp/chat_history.csv' CSV HEADER"

docker compose cp postgres:/tmp/chat_history.csv ./chat_history.csv
```

---

## Next Steps

1. **Install Docker Desktop** (if not already done)
2. **Follow Steps 1-8** to deploy the application
3. **Test both user flows** (authenticated + guest)
4. **Prepare demo script** for thesis defense
5. **Create sample data** for demonstration

**Good luck with your thesis defense!** 🎓
