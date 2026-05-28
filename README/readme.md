# DevSync: Full-Stack SaaS Landing & User Portal

![Project Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)
![Flask](https://img.shields.io/badge/Flask-Framework-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue.svg)

## 📌 Project Overview

DevSync is a fully responsive, database-driven web application simulating a modern SaaS platform. It features a high-converting landing page, dynamic asynchronous form submissions, secure user authentication, and a protected internal dashboard.

This project was built to demonstrate complete full-stack architecture, moving from UI/UX design to backend routing, session state management, and secure relational database operations.

## 🚀 Core Features

- **Responsive UI/UX:** Built with modern CSS variables, Flexbox/Grid, and a dynamic sticky navigation bar.
- **Asynchronous Processing:** Lead generation forms submit via JavaScript `fetch` API for zero-reload interactions and custom Toast notifications.
- **Secure Authentication:** User portal utilizes `werkzeug.security` (PBKDF2 SHA256) for robust password hashing.
- **State Management:** Flask Sessions securely manage user login states, protecting dashboard routes from unauthorized access.
- **Simulated Checkout Flow:** Seamless routing from pricing tiers to payment capture, finalizing in database insertion.

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+), DOM Manipulation.
- **Backend:** Python, Flask Framework.
- **Database:** MySQL (via `mysql-connector-python`).
- **Security:** Werkzeug Password Hashing, Session Management.

## 🗄️ Database Schema

The application utilizes a local MySQL server with the following structure:

**1. `subscribers` Table** (Lead Generation)

- `id` (INT, Primary Key)
- `email` (VARCHAR, Unique)
- `created_at` (TIMESTAMP)

**2. `accounts` Table** (Secure Portal Access)

- `id` (INT, Primary Key)
- `email` (VARCHAR, Unique)
- `password_hash` (VARCHAR) - _Stores securely hashed strings, never plain text._
- `created_at` (TIMESTAMP)

## 💻 Local Setup Instructions

**1. Clone the repository:**
\`\`\`bash
git clone https://github.com/YourUsername/devsync-saas.git
cd devsync-saas
\`\`\`

**2. Install dependencies:**
\`\`\`bash
pip install flask mysql-connector-python werkzeug
\`\`\`

**3. Configure MySQL:**

- Ensure your local MySQL server is running.
- Update the `db_config` credentials in `app.py` with your local database username and password.
- Run the schema queries provided in `database_setup.sql` (or manually via MySQL Workbench).

**4. Run the application:**
\`\`\`bash
python app.py
\`\`\`

- Navigate to `http://127.0.0.1:5000` in your web browser.

---

_Developed by Shinde Mahesh as a demonstration of production-ready full-stack engineering._
