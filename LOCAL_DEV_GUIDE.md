# ==============================================================================
# Quick Local Development Instructions
# ==============================================================================

## Current Status

✅ Dependencies installed in requirements.txt
✅ Settings configured for local development (SQLite3)
✅ Environment variables set in .env

## To Run Locally (Without Docker)

### Option 1: Use the Setup Script (Recommended)

```powershell
# Run the automated setup script
.\setup_local.ps1
```

### Option 2: Manual Setup

1. **Activate Virtual Environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies** (if not done already):
   ```powershell
   pip install -r requirements.txt
   ```

3. **Create Migrations**:
   ```powershell
   python manage.py makemigrations
   ```

4. **Apply Migrations**:
   ```powershell
   python manage.py migrate
   ```

5. **Start Server**:
   ```powershell
   python manage.py runserver
   ```

6. **Open Browser**:
   Navigate to: http://localhost:8000

---

## Testing the Hybrid Access System

### Test 1: Guest Mode (No Login)

Open your browser or use curl:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Where is the library?\"}"
```

Expected response:
```json
{
  "response": "LOCATION:...",
  "saved": false,
  "user": "guest"
}
```

### Test 2: Authenticated User (With Login)

1. **Register a user**:
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":\"2024-00001\",\"username\":\"testuser\",\"password\":\"TestPass123!\",\"email\":\"test@spus.edu.ph\"}"
```

2. **Login**:
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d "{\"username\":\"testuser\",\"password\":\"TestPass123!\"}"
```

3. **Send authenticated chat** (saved to database):
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d "{\"message\":\"What courses do you offer?\"}"
```

Expected response:
```json
{
  "response": "GENERAL INFORMATION:...",
  "saved": true,
  "user": "testuser"
}
```

4. **View chat history**:
```bash
curl -X GET http://localhost:8000/api/history \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## Current Configuration

**Database**: SQLite3 (local file at `db.sqlite3`)  
**Debug Mode**: Enabled (`DEBUG=True` in `.env`)  
**PostgreSQL**: Disabled for local dev (`USE_POSTGRES=false` in `.env`)

**Note**: When you switch to Docker deployment, set `USE_POSTGRES=true` in `.env`

---

## Troubleshooting

### Error: "No module named 'decouple'"

Make sure you're running commands inside the activated virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your prompt.

### Error: Database tables don't exist

Run migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Want to reset the database?

Delete `db.sqlite3` and run migrations again:
```powershell
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

---

## Next Steps

1. ✅ Run the local server
2. ✅ Test guest mode
3. ✅ Test authenticated mode
4. ⏳ Install Docker Desktop for production deployment
5. ⏳ Switch to PostgreSQL with `USE_POSTGRES=true`

**Good luck!** 🚀
