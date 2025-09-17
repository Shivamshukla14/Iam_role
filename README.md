# MTC-structured Django scaffold

This repo contains a minimal Django 4.2 project with an Azure-SSO-ready login page and a protected dashboard.

## Features
- Login page (50/50 split): dummy username/password form + active "Sign in with Microsoft" button (stubbed)
- SSO stub: clicking the Microsoft button logs in a fabricated user and redirects to the dashboard
- Dashboard page with top bar (Logout) and two tabs
- Modular templates (`base.html`, partials, per-app templates) and a basic dark theme CSS

## Quickstart (Windows, cmd.exe)

1. Create and activate a virtual environment:

```cmd
cd proj
py -3 -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```cmd
pip install -r requirements.txt
```

3. Initialize the database and run the server:

```cmd
python manage.py migrate
python manage.py runserver
```

4. Open http://127.0.0.1:8000/ — you'll be redirected to `/accounts/login/`.
   - Click "Sign in with Microsoft" to use the stubbed SSO and land on the dashboard.
   - The username/password form is disabled and will always show an error if submitted.

## Project structure
```
proj/
  manage.py
  requirements.txt
  mtcsite/
    settings.py, urls.py, asgi.py, wsgi.py
  accounts/
    apps.py, urls.py, views.py, templates/accounts/login.html
  dashboard/
    apps.py, urls.py, views.py, templates/dashboard/index.html
  templates/
    base.html, partials/topbar.html
  static/
    css/app.css
    img/company-logo.svg
```

## Next steps for real Azure AD SSO

Replace the stub with a real OpenID Connect client. Two common options:

- MSAL for Python + custom auth views
- `social-auth-app-django` with the Azure AD OIDC backend

Key items you'll need to configure:
- Azure AD App Registration (client ID, tenant, redirect URI `http://localhost:8000/accounts/sso/callback/`)
- OIDC scopes and claims (email, name)
- State/nonce protection and token validation
- Mapping claims to Django users (create-or-update on login)

We can wire this when ready.
