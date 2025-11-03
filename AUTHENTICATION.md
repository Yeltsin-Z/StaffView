# 🔐 StaffView Authentication Guide

StaffView now includes secure authentication to protect your regression comparison data.

## 📝 Default Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

### User Account  
- **Username**: `user`
- **Password**: `user123`

⚠️ **IMPORTANT**: Change these default passwords before deploying to production!

---

## 🎯 Features

✅ **Secure Password Hashing** - Uses werkzeug's `generate_password_hash`  
✅ **Session Management** - Secure session-based authentication  
✅ **Remember Me** - Stay logged in for 30 days  
✅ **Protected Routes** - All pages require authentication  
✅ **Beautiful Login UI** - Modern, responsive design  

---

## 🔧 How to Add/Modify Users

### Method 1: Edit app.py (Simple)

1. Open `app.py`
2. Find the `USERS` dictionary:

```python
USERS = {
    'admin': generate_password_hash('admin123'),
    'user': generate_password_hash('user123'),
}
```

3. Add or modify users:

```python
USERS = {
    'admin': generate_password_hash('your-secure-password'),
    'john': generate_password_hash('johns-password'),
    'jane': generate_password_hash('janes-password'),
}
```

4. Restart the application:

```bash
# Local development
python app.py

# Production (systemd)
sudo systemctl restart staffview
```

### Method 2: Generate Password Hash (Secure)

For better security, generate password hashes separately:

```python
# Run in Python shell
python3 -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
```

Then paste the hash into `app.py`:

```python
USERS = {
    'admin': 'pbkdf2:sha256:... (paste hash here)',
}
```

---

## 🌐 Production Configuration

### Set a Strong Secret Key

The secret key is used to sign session cookies. **Never use the default in production!**

#### Option 1: Environment Variable (Recommended)

```bash
# Generate a random secret key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Set as environment variable
export SECRET_KEY="your-generated-key-here"

# Or in systemd service file:
Environment="SECRET_KEY=your-generated-key-here"
```

#### Option 2: Edit app.py

```python
app.secret_key = 'your-very-secure-random-key-here'
```

### Enable HTTPS

Always use HTTPS in production to protect login credentials:

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

---

## 🚪 Session Management

### Session Duration

- **Default**: Session expires when browser closes
- **Remember Me**: Session lasts 30 days
- **Configurable**: Edit `app.permanent_session_lifetime` in `app.py`

### Logout

Users can logout by:
1. Clicking the "Logout" button (top right)
2. Visiting `/logout` directly
3. Clearing browser cookies

---

## 🛡️ Security Best Practices

### ✅ DO:

1. **Change default passwords** immediately
2. **Use strong passwords** (12+ characters, mixed case, numbers, symbols)
3. **Set unique SECRET_KEY** in production
4. **Use HTTPS** for all connections
5. **Limit login attempts** (consider adding rate limiting)
6. **Regular password updates** for users
7. **Audit user access** regularly

### ❌ DON'T:

1. ❌ Use default passwords in production
2. ❌ Share passwords between users
3. ❌ Commit passwords to git
4. ❌ Use HTTP in production
5. ❌ Share the SECRET_KEY

---

## 🔄 Upgrading to Database (Future)

For production use with many users, consider upgrading to a database:

### SQLite (Simple)

```python
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def create_users_table():
    conn = sqlite3.connect('staffview.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

def add_user(username, password, role='user'):
    conn = sqlite3.connect('staffview.db')
    password_hash = generate_password_hash(password)
    conn.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                 (username, password_hash, role))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('staffview.db')
    cursor = conn.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return check_password_hash(row[0], password)
    return False
```

### PostgreSQL (Enterprise)

For large deployments, use PostgreSQL with Flask-SQLAlchemy:

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

---

## 🔍 Troubleshooting

### Can't Login

1. **Check credentials** - Verify username and password
2. **Clear browser cache** - Sometimes old cookies cause issues
3. **Check logs** - `sudo journalctl -u staffview -f`
4. **Verify user exists** - Check USERS dict in `app.py`

### Session Expires Too Soon

Edit session lifetime in `app.py`:

```python
from datetime import timedelta

app.permanent_session_lifetime = timedelta(days=30)
```

### Forgot Password

Since passwords are hashed, you'll need to:

1. Generate new hash:
   ```python
   python3 -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('new-password'))"
   ```

2. Update in `app.py`:
   ```python
   USERS = {
       'admin': 'paste-new-hash-here',
   }
   ```

3. Restart application

---

## 📚 Related Documentation

- [AWS EC2 Deployment](AWS_EC2_DEPLOYMENT.md)
- [Main README](README.md)
- [Usage Guide](USAGE_GUIDE.md)

---

## 🆘 Support

Need help with authentication? Check:
1. Application logs: `sudo journalctl -u staffview -f`
2. Flask documentation: https://flask.palletsprojects.com/
3. Werkzeug security: https://werkzeug.palletsprojects.com/security/

---

**Stay secure! 🔒**

