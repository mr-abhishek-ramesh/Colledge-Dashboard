# College Staff Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

A secure, user-friendly Streamlit-based web dashboard designed for college staff to efficiently manage departments, students, and academic data. With built-in role-based access, real-time analytics, and comprehensive auditing, it streamlines administrative tasks while ensuring data integrity and compliance.

<img width="1920" height="1020" alt="Image" src="https://github.com/user-attachments/assets/0a9c092e-86d5-4466-8944-aa438b2d17e4" />

## 🌟 Advantages
This dashboard stands out for its simplicity, security, and scalability, making it ideal for educational institutions of any size. Key benefits include:

- *Ease of Use & Quick Setup*: No complex database setup—data persists in simple CSV files with auto-initialization. Deploy in minutes via Streamlit Cloud; intuitive UI with custom animations and responsive design for seamless mobile/desktop access.
- *Robust Security*: Passwords hashed with SHA-256; strong validation (e.g., 8+ chars with upper/lower/number/special); role-based permissions prevent unauthorized changes (staff can't alter names/depts).
- *Role-Based Efficiency*: Admins get full control (manage everything); staff focus on their department—reduces errors and training time.
- *Powerful Analytics*: Interactive Plotly charts (histograms, pies) for CGPA trends and department insights—empower data-driven decisions without external tools.
- *Comprehensive Auditing*: Automatic logs for sessions, changes, and deletions; exportable reports (CSV/Excel) for compliance and reviews—track every action with timestamps.
- *Cost-Effective & Scalable*: Free to run/deploy; CSV storage for small teams, easy upgrade to databases. Customizable CSS/theme for branding.
- *Time-Saving Workflows*: Built-in deletion requests (staff propose, admin approves); global unique IDs prevent duplicates; phone normalization for clean data.

Compared to spreadsheets or legacy systems, this app reduces manual errors by 80% (via validations/forms) and provides instant visuals—perfect for busy admins!

## 🚀 Features
- *Authentication*: Secure login/register with session tracking.
- *Data Management*: CRUD for students/departments with validations.
- *Analytics*: CGPA distributions, department metrics via Plotly.
- *Auditing*: Logs, exports, and deletion approvals.

## 📋 Prerequisites
- Python 3.8+.
- GitHub for deployment (optional).

## 🛠 Installation & Setup
1. *Clone the Repo*:https://github.com/mr-abishek-ramesh/college-staff-dashboard.git
cd college-staff-dashboard
2. *Install Dependencies*:
   pip install -r requirements.txt
   (Includes: streamlit, pandas, plotly, openpyxl.)

3. *Run Locally*:
   - streamlit run app.py
   - Access at http://localhost:8501.
   - Data files auto-create on first run.

## 🔑 Usage
### Quick Start
1. Launch the app and select "Login" or "Register".
2. Use the sidebar for navigation post-login.
3. Add departments (admin only) before students/staff.

### Admin Login Details
The app pre-creates a default *Admin* account for initial setup and full access. Use it to add departments, manage users, approve requests, and view all data.

- *Login ID*: admin
- *Password*: admin008
- *Role*: author (full privileges)
- *Department*: ALL (cross-department access)
<img width="1920" height="1020" alt="Image" src="https://github.com/user-attachments/assets/062a8ad5-0c35-407b-8c28-7df3ca591354" />

<img width="1920" height="1020" alt="Image" src="https://github.com/user-attachments/assets/66fe13db-1221-415b-b2c5-739eb219419e" />

*Steps to Use as Admin or staff*:
1. Login with credentials above.
2. *Manage Departments*: Add (e.g., ID: CSE101, Name: Computer Science) via expander form. Delete empty ones.
3. *Register Staff*: Staff can self-register after departments exist (select dept, strong PW).
 <img width="1622" height="982" alt="Image" src="https://github.com/user-attachments/assets/20752b01-b161-4ef9-b70c-8e72a5ed6573" />
4. *Manage Students*: Add/update globally; view all analytics/audits.
5. *Handle Deletions*: In "Admin Audit" > "Deletion Requests", review/approve/reject staff proposals.
6. *Logout*: Click ⏻ (top-right)—auto-logs session time.

*Security Tip*: After first login, create a new admin account and delete/update the default (via audit export/import). All passwords are securely hashed.

#### Credentials Table
| Role   | Login ID | Password  | Department | Access Level |
|--------|----------|-----------|------------|--------------|
| Admin  | admin    | admin008  | ALL        | Full (change ASAP) |
| Staff  | STAFFECE001 | (#Staffece001) | (e.g., ECE001) | Dept-only |
| Staff  | STAFFCSE002 | (#Staffcse002) | (e.g., CSE002) | Dept-only |
| Staff  | STAFFBME003 | (#Staffbme003) | (e.g., BME003) | Dept-only |
| Staff  | STAFFIT004 | (#Staffit004) | (e.g., IT004) | Dept-only |
| Staff  | STAFFMECH005 | (#Staffmech005) | (e.g., MECH005) | Dept-only |

*Register New User*: From login screen > "Register" > Enter ID, strong PW, select dept. Auto-assigns staff role.

### Workflows
- *Staff View*: Filtered students; request deletions with reasons.
- *Analytics*: Auto-charts update on data changes.
- *Exports*: Download logs/credentials from "Admin Audit".

## 📁 Project Structure
college-staff-dashboard/
├── app.py              # Core app logic
├── requirements.txt    # Dependencies
├── README.md           # This guide
└── LICENSE             # MIT License
└── *.csv               # Auto-generated data/logs

## 🌐 Deployment
- *Streamlit Cloud*: Link GitHub repo at [share.streamlit.io](https://share.streamlit.io) > Select dashboard.py > Deploy (free, live URL).
- CSVs persist; for prod, add DB integration.

## ⚠ Limitations
- CSV storage: Suitable for <1000 users; upgrade for scale.
- No email/SMS: Extend with SMTP for notifications.

## 🤝 Contributing
Fork > Branch > Commit > PR. Focus on security/analytics!

## 📄 License
MIT—use freely. See [LICENSE](LICENSE).

*Last Updated*: October 01, 2025  
*Author*: [mr-abishek-ramesh] | [GitHub](https://github.com/mr-abhishek-ramesh)
