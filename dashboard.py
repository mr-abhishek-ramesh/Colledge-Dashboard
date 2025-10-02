import streamlit as st
import pandas as pd
import plotly.express as px
import os
import hashlib
import re
from datetime import datetime
from streamlit import rerun

# File paths for storing data
DEPARTMENTS_FILE = "departments.csv"
STUDENTS_FILE = "students.csv"
USERS_FILE = "users.csv"
AUDIT_LOG_FILE = "audit_log.csv"
CHANGE_LOG_FILE = "change_log.csv"
DELETION_REQUESTS_FILE = "deletion_requests.csv"

# ---------------- CUSTOM STYLING ---------------- #
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI Emoji', 'Apple Color Emoji', Roboto, sans-serif;
        background-color: #F8FAFC;
        color: #1E3A8A;
        text-shadow: none;
        transition: all 0.5s ease-in-out;
    }
    .stApp {
        background-color: #F8FAFC;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        animation: fadeIn 0.7s ease-in-out;
    }
    .stButton>button {
        background-color: #FFFFFF;
        color: #1E3A8A;
        text-shadow: none;
        border-radius: 24px;
        padding: 12px 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 16px;
        border: 1px solid #93C5FD;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        transition: all 0.3s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(75, 75, 75, 0.3);
        background-color: #DBEAFE;
    }
    .stButton>button:active::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(75, 75, 75, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: ripple 0.5s ease-out;
    }
    @keyframes ripple {
        0% { width: 0; height: 0; opacity: 0.5; }
        100% { width: 200px; height: 200px; opacity: 0; }
    }
    .logout-button>button {
        background-color: #FFFFFF;
        color: #1E3A8A;
        text-shadow: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        border: 1px solid #93C5FD;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        transition: all 0.3s ease-in-out;
    }
    .logout-button>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(75, 75, 75, 0.3);
        background-color: #DBEAFE;
    }
    .logout-button>button:active::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(75, 75, 75, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: ripple 0.5s ease-out;
    }
    .stTextInput>div>input {
        border-radius: 12px;
        border: 1px solid #93C5FD;
        padding: 12px;
        background-color: #FFFFFF;
        color: #1E3A8A;
        text-shadow: none;
        transition: all 0.3s ease-in-out;
    }
    .stTextInput>div>input:focus {
        border-color: #1E3A8A;
        box-shadow: 0 0 8px rgba(75, 75, 75, 0.3);
    }
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 1px solid #93C5FD;
        padding: 12px;
        background-color: #FFFFFF;
        color: #1E3A8A;
        text-shadow: none;
        transition: all 0.3s ease-in-out;
    }
    .stNumberInput>div>input {
        border-radius: 12px;
        border: 1px solid #93C5FD;
        padding: 12px;
        background-color: #FFFFFF;
        color: #1E3A8A;
        text-shadow: none;
        transition: all 0.3s ease-in-out;
    }
    .sidebar .sidebar-content {
        background-color: #F8FAFC;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        padding: 20px;
        color: #1E3A8A;
        text-shadow: none;
        animation: slideIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        background-color: #F8FAFC;
        transition: all 0.5s ease-in-out;
    }
    .stSuccess {
        background-color: #DBEAFE;
        color: #1E3A8A;
        text-shadow: none;
        border-radius: 12px;
        padding: 12px;
        font-weight: 600;
        border: 1px solid #93C5FD;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        animation: fadeIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    .stError {
        background-color: #DBEAFE;
        color: #1E3A8A;
        text-shadow: none;
        border-radius: 12px;
        padding: 12px;
        font-weight: 600;
        border: 1px solid #93C5FD;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        animation: fadeIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    .stWarning {
        background-color: #DBEAFE;
        color: #1E3A8A;
        text-shadow: none;
        border-radius: 12px;
        padding: 12px;
        font-weight: 600;
        border: 1px solid #93C5FD;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        animation: fadeIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 32px;
        color: #1E3A8A;
        text-shadow: none;
        animation: slideIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1E3A8A;
        text-shadow: none;
        animation: slideIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    .login-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: #3B82F6;
        text-shadow: none;
        margin-top: 8px;
        animation: fadeIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    @keyframes slideIn {
        0% { transform: translateY(20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .container {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        margin-bottom: 24px;
        transition: all 0.5s ease-in-out;
    }
    .container:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 10px rgba(75, 75, 75, 0.3);
    }
    .stExpander {
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(75, 75, 75, 0.2);
        background-color: #F8FAFC;
        color: #1E3A8A;
        text-shadow: none;
        transition: all 0.5s ease-in-out;
    }
    .stExpander:hover {
        box-shadow: 0 4px 10px rgba(75, 75, 75, 0.3);
    }
    .stPlotlyChart {
        animation: fadeIn 0.7s ease-in-out;
        transition: all 0.5s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- PASSWORD UTILS ---------------- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[@$!%*?&#]", password)
    )

def is_valid_login_id(login_id):
    """Validate login ID (alphanumeric, 4-20 characters)"""
    return bool(re.match(r"^[a-zA-Z0-9]{4,20}$", login_id))

def is_valid_phone(phone):
    """Enhanced phone validation: 10-15 digits after normalizing"""
    normalized = normalize_phone(phone)
    return bool(re.match(r"^\d{10,15}$", normalized)) and len(normalized) >= 10

def normalize_phone(phone):
    """Normalize phone by stripping + and returning as string"""
    if pd.isna(phone):
        return ""
    return re.sub(r"[^\d]", "", str(phone).lstrip('+'))  # Strip non-digits

# ---------------- INITIALIZATION ---------------- #
def initialize_data():
    if not os.path.exists(DEPARTMENTS_FILE):
        pd.DataFrame(columns=["dept_id", "dept_name"]).to_csv(DEPARTMENTS_FILE, index=False)
    if not os.path.exists(STUDENTS_FILE):
        pd.DataFrame(columns=["student_id", "name", "dept_id", "cgpa", "phone"]).to_csv(STUDENTS_FILE, index=False)
    if not os.path.exists(USERS_FILE):
        users_df = pd.DataFrame(columns=["login_id", "password", "dept_id", "role", "phone"])
        users_df.to_csv(USERS_FILE, index=False)
        admin_password = hash_password("admin008")
        admin_user = pd.DataFrame({
            "login_id": ["admin"],
            "password": [admin_password],
            "dept_id": ["ALL"],
            "role": ["author"],
            "phone": ["1234567890"]
        })
        admin_user.to_csv(USERS_FILE, index=False)
    else:
        users = pd.read_csv(USERS_FILE, dtype=str)
        if "identifier" in users.columns or "email" in users.columns or "phone" in users.columns:
            new_users = pd.DataFrame(columns=["login_id", "password", "dept_id", "role", "phone"])
            for _, row in users.iterrows():
                login_id = row.get("identifier", row.get("email", row.get("login_id", "")))
                if not login_id:
                    login_id = row.get("phone", "")
                new_users = pd.concat([new_users, pd.DataFrame({
                    "login_id": [login_id],
                    "password": [row.get("password", "")],
                    "dept_id": [row.get("dept_id", "ALL")],
                    "role": [row.get("role", "staff")],
                    "phone": [row.get("phone", "")]
                })], ignore_index=True)
            # Auto-fix admin login_id if migrated from old email
            if not new_users.empty and "admin@college.edu" in new_users["login_id"].values:
                new_users.loc[new_users["login_id"] == "admin@college.edu", "login_id"] = "admin"
            new_users.to_csv(USERS_FILE, index=False)
    if not os.path.exists(AUDIT_LOG_FILE):
        pd.DataFrame(columns=["login_id", "login_time", "logout_time", "usage_minutes"]).to_csv(AUDIT_LOG_FILE, index=False)
    if not os.path.exists(CHANGE_LOG_FILE):
        pd.DataFrame(columns=["timestamp", "login_id", "action", "student_id", "details"]).to_csv(CHANGE_LOG_FILE, index=False)
    if not os.path.exists(DELETION_REQUESTS_FILE):
        pd.DataFrame(columns=["timestamp", "staff_id", "student_id", "dept_id", "reason", "status"]).to_csv(DELETION_REQUESTS_FILE, index=False)

def load_data():
    try:
        departments = pd.read_csv(DEPARTMENTS_FILE, dtype={"dept_id": str})
        students = pd.read_csv(STUDENTS_FILE, dtype={"student_id": str, "dept_id": str})
    except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError):
        initialize_data()
        departments = pd.DataFrame(columns=["dept_id", "dept_name"])
        students = pd.DataFrame(columns=["student_id", "name", "dept_id", "cgpa", "phone"])
        st.warning("Data files initialized due to error or absence ⚠️")
    
    required_student_cols = ["student_id", "name", "dept_id", "cgpa", "phone"]
    for col in required_student_cols:
        if col not in students.columns:
            students[col] = ""
    
    required_dept_cols = ["dept_id", "dept_name"]
    for col in required_dept_cols:
        if col not in departments.columns:
            departments[col] = ""
    
    # Ensure CGPA is numeric and rounded to 1 decimal
    students["cgpa"] = pd.to_numeric(students["cgpa"], errors='coerce').fillna(0.0).round(1)
    
    return departments, students

def load_users():
    try:
        users = pd.read_csv(USERS_FILE, dtype=str)
        required_cols = ["login_id", "password", "dept_id", "role", "phone"]
        for col in required_cols:
            if col not in users.columns:
                users[col] = ""
        return users
    except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError):
        initialize_data()
        return pd.read_csv(USERS_FILE, dtype=str)

def load_audit_log():
    try:
        audit_log = pd.read_csv(AUDIT_LOG_FILE)
        required_cols = ["login_id", "login_time", "logout_time", "usage_minutes"]
        for col in required_cols:
            if col not in audit_log.columns:
                audit_log[col] = ""
        # Convert time columns to datetime if possible
        for col in ["login_time", "logout_time"]:
            if col in audit_log.columns:
                audit_log[col] = pd.to_datetime(audit_log[col], errors='coerce')
        return audit_log
    except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["login_id", "login_time", "logout_time", "usage_minutes"])

def load_change_log():
    try:
        change_log = pd.read_csv(CHANGE_LOG_FILE)
        required_cols = ["timestamp", "login_id", "action", "student_id", "details"]
        for col in required_cols:
            if col not in change_log.columns:
                change_log[col] = ""
        change_log["timestamp"] = pd.to_datetime(change_log["timestamp"], errors='coerce')
        return change_log
    except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["timestamp", "login_id", "action", "student_id", "details"])

def load_deletion_requests():
    try:
        requests = pd.read_csv(DELETION_REQUESTS_FILE)
        required_cols = ["timestamp", "staff_id", "student_id", "dept_id", "reason", "status"]
        for col in required_cols:
            if col not in requests.columns:
                requests[col] = ""
        requests["timestamp"] = pd.to_datetime(requests["timestamp"], errors='coerce')
        requests["status"] = requests["status"].fillna("pending")
        return requests
    except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["timestamp", "staff_id", "student_id", "dept_id", "reason", "status"])

def save_deletion_requests(requests):
    requests.to_csv(DELETION_REQUESTS_FILE, index=False)

def log_change(action, student_id, details):
    if st.session_state.current_user:
        timestamp = datetime.now()
        new_log = pd.DataFrame({
            "timestamp": [timestamp],
            "login_id": [st.session_state.current_user],
            "action": [action],
            "student_id": [student_id],
            "details": [details]
        })
        change_log = load_change_log()
        change_log = pd.concat([change_log, new_log], ignore_index=True)
        change_log.to_csv(CHANGE_LOG_FILE, index=False)

def request_deletion(student_id, reason=""):
    timestamp = datetime.now()
    new_request = pd.DataFrame({
        "timestamp": [timestamp],
        "staff_id": [st.session_state.current_user],
        "student_id": [student_id],
        "dept_id": [st.session_state.dept_id],
        "reason": [reason],
        "status": ["pending"]
    })
    requests = load_deletion_requests()
    requests = pd.concat([requests, new_request], ignore_index=True)
    save_deletion_requests(requests)
    log_change("deletion_request", student_id, f"Deletion request raised: {reason}")

def process_deletion_request(request_idx, action):
    requests = load_deletion_requests()
    if request_idx < len(requests):
        req = requests.iloc[request_idx]
        if action == "accept":
            # Reload data to get current state
            departments, students = load_data()
            students = students[students["student_id"] != req["student_id"]]
            save_data(departments, students)
            log_change("delete", req["student_id"], f"Deletion accepted by admin: {req['reason']}")
            st.success(f"Student {req['student_id']} deleted successfully ✅")
        elif action == "reject":
            log_change("deletion_reject", req["student_id"], f"Deletion rejected: {req['reason']}")
            st.warning(f"Deletion request for {req['student_id']} rejected ⚠️")
        requests.loc[request_idx, "status"] = "accepted" if action == "accept" else "rejected"
        save_deletion_requests(requests)
        rerun()

def save_data(departments, students):
    with st.spinner("Saving data..."):
        departments.to_csv(DEPARTMENTS_FILE, index=False)
        students.to_csv(STUDENTS_FILE, index=False)
        # Update session state for persistence
        st.session_state.departments = departments
        st.session_state.students = students

def save_users(users):
    with st.spinner("Saving user data..."):
        users.to_csv(USERS_FILE, index=False)
        if not users.empty:
            users.to_excel("users_credentials.xlsx", index=False)

def log_session_end():
    if "login_time" in st.session_state and st.session_state.current_user:
        logout_time = datetime.now()
        duration = (logout_time - st.session_state.login_time).total_seconds() / 60
        new_log = pd.DataFrame({
            "login_id": [st.session_state.current_user],
            "login_time": [st.session_state.login_time],
            "logout_time": [logout_time],
            "usage_minutes": [round(duration, 2)]
        })
        audit_log = load_audit_log()
        audit_log = pd.concat([audit_log, new_log], ignore_index=True)
        audit_log.to_csv(AUDIT_LOG_FILE, index=False)

def generate_student_id(dept_id, students):
    """Generate next student ID for the department, e.g., CS1001, CS1002"""
    existing = students[students["dept_id"] == dept_id]
    count = len(existing)
    next_num = 1000 + count + 1
    return f"{dept_id}{next_num}"

@st.cache_data
def compute_dept_stats(students, departments):
    """Cached computation for department stats"""
    dept_stats = students.groupby("dept_id").agg({
        'cgpa': 'mean',
        'student_id': 'count'
    }).reset_index()
    dept_stats.columns = ['dept_id', 'avg_cgpa', 'student_count']
    dept_stats = dept_stats.merge(departments[["dept_id", "dept_name"]], on="dept_id", how="left")
    dept_stats["dept_name"] = dept_stats["dept_name"].fillna("Unknown")
    return dept_stats

# ---------------- APP START ---------------- #
initialize_data()

# Session state persistence for data
if 'departments' not in st.session_state:
    st.session_state.departments, st.session_state.students = load_data()
departments = st.session_state.departments
students = st.session_state.students

users = load_users()

# Session state
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "dept_id" not in st.session_state:
    st.session_state.dept_id = None
if "login_time" not in st.session_state:
    st.session_state.login_time = None

# ---------------- AUTHENTICATION ---------------- #
if not st.session_state.authentication_status:
    with st.container():
        st.markdown("<h1>College Staff Dashboard</h1>", unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Manage Your Academic Data</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("### Quick Actions")
            choice = st.radio("Select Action", ["Login", "Register"], horizontal=False, key="auth_choice")
        with col2:
            if choice == "Login":
                st.subheader("🔑 Staff Login")
                with st.form("login_form"):
                    login_id = st.text_input("Login ID", placeholder="Enter your login ID (e.g., admin)", help="Use your registered login ID")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    submit = st.form_submit_button("Login", use_container_width=True)
                    
                    if submit:
                        if not login_id or not password:
                            st.error("Please enter both login ID and password ❌")
                        else:
                            hashed = hash_password(password)
                            match = users[(users["login_id"] == login_id) & (users["password"] == hashed)]
                            if not match.empty:
                                st.session_state.authentication_status = True
                                st.session_state.current_user = login_id
                                st.session_state.role = match["role"].iloc[0]
                                st.session_state.dept_id = match["dept_id"].iloc[0]
                                st.session_state.login_time = datetime.now()
                                st.success("Login successful! ✅")
                                rerun()
                            else:
                                st.error("Invalid login ID or password. Please try again. ❌")
            
            else:
                with st.form("register_form"):
                    st.subheader("📝 Register New Staff Account")
                    login_id = st.text_input(
                        "Login ID",
                        placeholder="e.g., johndoe123",
                        help="Enter a unique login ID (alphanumeric, 4-20 characters)"
                    )
                    password = st.text_input("Choose Password", type="password", placeholder="Enter a strong password")
                    dept_id = st.selectbox("Department", departments["dept_id"] if not departments.empty else ["No Departments Available"], key="reg_dept")
                    submit = st.form_submit_button("Register", use_container_width=True)
                    if submit:
                        if not login_id:
                            st.error("Please provide a login ID ❌")
                        elif not is_valid_login_id(login_id):
                            st.error("Login ID must be 4-20 characters and alphanumeric ❌")
                        elif login_id in users["login_id"].values:
                            st.error("This login ID is already registered ❌")
                        elif not is_strong_password(password):
                            st.error("Password must be at least 8 characters and include uppercase, lowercase, number, and special character ⚠️")
                        elif dept_id == "No Departments Available":
                            st.error("No departments available. Please contact admin to add departments. ⚠️")
                        else:
                            new_user = pd.DataFrame({
                                "login_id": [login_id],
                                "password": [hash_password(password)],
                                "dept_id": [dept_id],
                                "role": ["staff"],
                                "phone": [""]
                            })
                            users = pd.concat([users, new_user], ignore_index=True)
                            save_users(users)
                            st.success("Account created successfully! Please login with your credentials. ✅")
else:
    # Unique Logout Button
    st.markdown('<div class="logout-button">', unsafe_allow_html=True)
    if st.button("⏻", key="logout"):
        log_session_end()
        # Clear only auth-related session state
        for key in ["authentication_status", "current_user", "role", "dept_id", "login_time"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.authentication_status = False
        rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("### 🎓 Staff Dashboard")
    st.sidebar.success(f"Logged in as {st.session_state.current_user} ({st.session_state.role})")
    if st.session_state.login_time:
        session_duration = (datetime.now() - st.session_state.login_time).total_seconds() / 60
        st.sidebar.info(f"Session Time: {round(session_duration, 2)} minutes")
    if st.session_state.role == "author":
        requests = load_deletion_requests()
        pending = requests[requests["status"] == "pending"]
        if not pending.empty:
            st.sidebar.warning(f"🔔 {len(pending)} Pending Deletion Requests!")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")
    options = ["Manage Students", "Analytics Dashboard"]
    if st.session_state.role == "author":
        options = ["Manage Departments", "Manage Students", "Analytics Dashboard", "Admin Audit"]
    option = st.sidebar.selectbox("Select Option", options, format_func=lambda x: f"📌 {x}", key="nav_select")

    # Main Content
    st.markdown("<h1>College Staff Dashboard</h1>", unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Streamline department and student management with powerful analytics.</div>', unsafe_allow_html=True)

    # ---------------- MANAGE DEPARTMENTS ---------------- #
    if option == "Manage Departments" and st.session_state.role == "author":
        with st.container():
            st.header("🏛 Manage Departments")
            with st.expander("Add New Department", expanded=True):
                with st.form("dept_form"):
                    dept_id = st.text_input("Department ID", placeholder="e.g., CSE101")
                    dept_name = st.text_input("Department Name", placeholder="e.g., Computer Science")
                    submit = st.form_submit_button("➕ Add Department")
                    if submit:
                        if dept_id and dept_name:
                            if dept_id not in departments["dept_id"].values:
                                new_dept = pd.DataFrame({"dept_id": [dept_id], "dept_name": [dept_name]})
                                departments = pd.concat([departments, new_dept], ignore_index=True)
                                save_data(departments, students)
                                st.success("Department added successfully ✅")
                                rerun()
                            else:
                                st.error("Department ID already exists ❌")
                        else:
                            st.error("All fields required ⚠️")

            st.subheader("📋 Department List")
            st.dataframe(departments, use_container_width=True)

            with st.expander("Delete Department"):
                dept_to_delete = st.selectbox("Select Department to Delete", departments["dept_id"], key="delete_dept")
                if st.button("🗑 Delete Department"):
                    if dept_to_delete in students["dept_id"].values:
                        st.error("Cannot delete department with enrolled students ❌")
                    else:
                        departments = departments[departments["dept_id"] != dept_to_delete]
                        save_data(departments, students)
                        st.success("Department deleted successfully ✅")
                        rerun()

    # ---------------- MANAGE STUDENTS ---------------- #
    if option == "Manage Students":
        with st.container():
            st.header("👩‍🎓 Manage Students")
            if st.session_state.role == "author":
                filtered_students = students
            else:
                filtered_students = students[students["dept_id"] == st.session_state.dept_id]

            with st.expander("Add/Update Student", expanded=True):
                with st.form("student_form"):
                    student_id = st.text_input("Student ID (optional - auto-generate if blank, e.g., CS1001)", placeholder="Leave blank for auto-generation")
                    name = st.text_input("Name", placeholder="e.g., John Doe")
                    if st.session_state.role == "author":
                        dept_options = departments["dept_id"].tolist() if not departments.empty else ["NO_DEPT_AVAILABLE"]
                        dept_id = st.selectbox("Department", dept_options, key="student_dept")
                    else:
                        dept_id = st.session_state.dept_id
                        st.text_input("Department", value=dept_id, disabled=True)
                    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
                    phone = st.text_input("Phone", placeholder="e.g., +919876543210 or 9876543210", help="10-15 digits only")
                    submit = st.form_submit_button("➕ Add/Update Student")
                    if submit:
                        # Enhanced security: Role-based dept check
                        if st.session_state.role != "author" and dept_id != st.session_state.dept_id:
                            st.error("Access denied: Cannot change department ❌")
                            st.stop()
                        
                        if not name or dept_id == "NO_DEPT_AVAILABLE" or pd.isna(cgpa) or not phone:
                            st.error("All fields required (except optional Student ID) ⚠️")
                        elif not is_valid_phone(phone):
                            st.error("Invalid phone number. Use 10-15 digits only ❌")
                        else:
                            # Handle auto-generation if student_id blank
                            if not student_id:
                                student_id = generate_student_id(dept_id, students)
                                st.info(f"Auto-generated Student ID: {student_id}")
                            
                            if student_id in students["student_id"].values:
                                if student_id not in filtered_students["student_id"].values:
                                    st.error("Student ID already exists in another department. IDs must be unique globally. ❌")
                                else:
                                    # Check for name change or dept change only for non-admin
                                    existing = students[students["student_id"] == student_id].iloc[0]
                                    old_name = existing["name"]
                                    old_dept = existing["dept_id"]
                                    old_cgpa = existing["cgpa"]
                                    old_phone = existing["phone"]
                                    if st.session_state.role != "author" and (old_name != name or old_dept != dept_id):
                                        st.error("Cannot change student name or department. Delete and re-add if needed. ❌")
                                    existing_name = students[(students["dept_id"] == dept_id) & (students["name"] == name) & (students["student_id"] != student_id)]
                                    if not existing_name.empty:
                                        st.error(f"Student name '{name}' already exists in department {dept_id} ❌")
                                    # Log changes
                                    changes = []
                                    if old_name != name:
                                        changes.append(f"Name: {old_name} -> {name}")
                                    if old_dept != dept_id:
                                        changes.append(f"Dept: {old_dept} -> {dept_id}")
                                    if old_cgpa != cgpa:
                                        changes.append(f"CGPA: {old_cgpa} -> {cgpa}")
                                    if old_phone != phone:
                                        changes.append(f"Phone: {old_phone} -> {phone}")
                                    details = "; ".join(changes) if changes else "No changes"
                                    students.loc[students["student_id"] == student_id, ["name", "dept_id", "cgpa", "phone"]] = [name, dept_id, round(cgpa, 1), normalize_phone(phone)]
                                    save_data(departments, students)
                                    log_change("update", student_id, details)
                                    st.success("Student updated successfully ✅")
                            else:
                                existing_name = students[(students["dept_id"] == dept_id) & (students["name"] == name)]
                                if not existing_name.empty:
                                    st.error(f"Student name '{name}' already exists in department {dept_id} ❌")
                                else:
                                    new_student = pd.DataFrame({
                                        "student_id": [student_id],
                                        "name": [name],
                                        "dept_id": [dept_id],
                                        "cgpa": [round(cgpa, 1)],
                                        "phone": [normalize_phone(phone)]
                                    })
                                    students = pd.concat([students, new_student], ignore_index=True)
                                    save_data(departments, students)
                                    details = f"New student: Name={name}, Dept={dept_id}, CGPA={cgpa}, Phone={phone}"
                                    log_change("add", student_id, details)
                                    st.success("Student added successfully ✅")

            st.subheader("📋 Student List")
            st.dataframe(filtered_students, use_container_width=True)

            with st.expander("Delete Student"):
                student_to_delete = st.selectbox("Select Student to Delete", filtered_students["student_id"], key="delete_student")
                if st.session_state.role == "author":
                    if st.button("🗑 Delete Student"):
                        log_change("delete", student_to_delete, "Student deleted by admin")
                        students = students[students["student_id"] != student_to_delete]
                        save_data(departments, students)
                        st.success("Student deleted successfully ✅")
                        rerun()
                else:
                    reason = st.text_area("Reason for Deletion (optional)", placeholder="Enter reason for deletion request...")
                    if st.button("📤 Request Delete"):
                        request_deletion(student_to_delete, reason)
                        st.success("Deletion request raised to admin! ✅")

    # ---------------- ANALYTICS ---------------- #
    if option == "Analytics Dashboard":
        with st.container():
            st.header("📊 Analytics Dashboard")
            if st.session_state.role == "author":
                filtered_students = students
            else:
                filtered_students = students[students["dept_id"] == st.session_state.dept_id]

            if not filtered_students.empty:
                st.subheader("📈 CGPA Distribution")
                fig = px.histogram(filtered_students, x="cgpa", nbins=20, title="CGPA Distribution", color_discrete_sequence=["#1E3A8A"])
                fig.update_layout(
                    plot_bgcolor="#F8FAFC",
                    paper_bgcolor="#F8FAFC",
                    font=dict(family="Inter", size=12, color="#1E3A8A"),
                    xaxis=dict(gridcolor="#93C5FD"),
                    yaxis=dict(gridcolor="#93C5FD")
                )
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("🥧 Department Performance")
                dept_stats = compute_dept_stats(students, departments)
                if st.session_state.role != "author":
                    dept_stats = dept_stats[dept_stats["dept_id"] == st.session_state.dept_id]
                if not dept_stats.empty:
                    total_students = dept_stats["student_count"].sum()
                    dept_stats["weighted_percentage"] = (dept_stats["student_count"] / total_students * 100).round(2)
                    fig = px.pie(
                        dept_stats,
                        values="weighted_percentage",
                        names="dept_name",
                        title="Department Student Distribution (%)",
                        color_discrete_sequence=["#1E3A8A", "#3B82F6", "#93C5FD", "#DBEAFE"]
                    )
                    fig.update_layout(
                        font=dict(family="Inter", size=12, color="#1E3A8A"),
                        plot_bgcolor="#F8FAFC",
                        paper_bgcolor="#F8FAFC"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No valid CGPA data available for analysis ⚠️")

                st.subheader("🥧 Overall GPA Metrics")
                avg_cgpa = filtered_students["cgpa"].mean()
                percentage = (avg_cgpa / 10) * 100 if not pd.isna(avg_cgpa) else 0
                title = "Overall College GPA" if st.session_state.role == "author" else "Department GPA"
                data = pd.DataFrame({
                    "Category": ["Achieved", "Remaining"],
                    "Percentage": [percentage, 100 - percentage]
                })
                fig = px.pie(
                    data,
                    values="Percentage",
                    names="Category",
                    title=f"{title} out of 100%",
                    color_discrete_sequence=["#1E3A8A", "#DBEAFE"]
                )
                fig.update_layout(
                    font=dict(family="Inter", size=12, color="#1E3A8A"),
                    plot_bgcolor="#F8FAFC",
                    paper_bgcolor="#F8FAFC"
                )
                st.plotly_chart(fig, use_container_width=True)

                if st.session_state.role == "author":
                    st.subheader("🥧 Department-wise GPA")
                    dept_avg = students.groupby("dept_id")["cgpa"].mean().reset_index()
                    dept_avg = dept_avg.merge(departments[["dept_id", "dept_name"]], on="dept_id", how="left")
                    dept_avg["dept_name"] = dept_avg["dept_name"].fillna("Unknown")
                    if not dept_avg.empty:
                        for _, row in dept_avg.iterrows():
                            percentage = (row["cgpa"] / 10) * 100 if not pd.isna(row["cgpa"]) else 0
                            data = pd.DataFrame({
                                "Category": ["Achieved", "Remaining"],
                                "Percentage": [percentage, 100 - percentage]
                            })
                            st.markdown(f"**{row['dept_name']} (ID: {row['dept_id']})**")
                            fig = px.pie(
                                data,
                                values="Percentage",
                                names="Category",
                                title=f"Average CGPA → {percentage:.2f}%",
                                hole=0.4,
                                color_discrete_sequence=["#1E3A8A", "#DBEAFE"]
                            )
                            fig.update_layout(
                                font=dict(family="Inter", size=12, color="#1E3A8A"),
                                plot_bgcolor="#F8FAFC",
                                paper_bgcolor="#F8FAFC"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No department data available for analysis ⚠️")
            else:
                st.warning("No student data available for analysis ⚠️")

    # ---------------- ADMIN AUDIT ---------------- #
    if option == "Admin Audit" and st.session_state.role == "author":
        with st.container():
            st.header("🔍 Admin Audit")
            users = load_users()
            st.subheader("🔑 User Credentials")
            st.dataframe(users, use_container_width=True)

            if os.path.exists("users_credentials.xlsx"):
                with open("users_credentials.xlsx", "rb") as f:
                    st.download_button(
                        "📥 Download Credentials",
                        data=f.read(),
                        file_name="users_credentials.xlsx",
                        key="download_credentials"
                    )
            else:
                st.warning("Credentials file not available ⚠️")

            # ---------------- CREATE NEW STAFF ACCOUNT ---------------- #
            with st.expander("➕ Create New Staff Account"):
                with st.form("admin_create_user_form"):
                    new_login_id = st.text_input("New Login ID", placeholder="e.g., newstaff123")
                    new_password = st.text_input("New Password", type="password", placeholder="Enter a strong password")
                    new_dept_id = st.selectbox("Department", ["ALL"] + departments["dept_id"].tolist() if not departments.empty else ["ALL"])
                    new_role = st.selectbox("Role", ["staff", "author"])
                    new_phone = st.text_input("Phone (optional)", placeholder="e.g., 9876543210")
                    create_submit = st.form_submit_button("Create Staff Account")
                    if create_submit:
                        if not new_login_id or not new_password:
                            st.error("Login ID and Password required ❌")
                        elif not is_valid_login_id(new_login_id):
                            st.error("Login ID must be 4-20 alphanumeric characters ❌")
                        elif new_login_id in users["login_id"].values:
                            st.error("Login ID already exists ❌")
                        elif not is_strong_password(new_password):
                            st.error("Password must be strong (8+ chars, upper, lower, number, special) ⚠️")
                        else:
                            new_user = pd.DataFrame({
                                "login_id": [new_login_id],
                                "password": [hash_password(new_password)],
                                "dept_id": [new_dept_id],
                                "role": [new_role],
                                "phone": [normalize_phone(new_phone) or ""]
                            })
                            users = pd.concat([users, new_user], ignore_index=True)
                            save_users(users)
                            st.success(f"New staff account '{new_login_id}' created successfully! ✅")
                            rerun()

            # ---------------- CHANGE PASSWORD ---------------- #
            with st.expander("🔑 Change User Password"):
                if len(users) > 0:
                    available_users = users[users["login_id"] != st.session_state.current_user]["login_id"].tolist()
                    if not available_users:
                        st.warning("No other users available to change password ⚠️")
                    else:
                        user_to_change = st.selectbox("Select User", available_users, key="change_user")
                        with st.form("change_password_form"):
                            new_password = st.text_input("New Password", type="password", placeholder="Enter new strong password")
                            confirm_password = st.text_input("Confirm New Password", type="password", placeholder="Confirm new password")
                            change_submit = st.form_submit_button("Update Password")
                            if change_submit:
                                if new_password != confirm_password:
                                    st.error("Passwords do not match ❌")
                                elif not is_strong_password(new_password):
                                    st.error("Password must be strong (8+ chars, upper, lower, number, special) ⚠️")
                                else:
                                    users.loc[users["login_id"] == user_to_change, "password"] = hash_password(new_password)
                                    save_users(users)
                                    st.success(f"Password for '{user_to_change}' updated successfully! ✅")
                                    rerun()
                else:
                    st.warning("No users available ⚠️")

            # ---------------- DELETE USER ---------------- #
            with st.expander("🗑 Delete User Account"):
                if len(users) > 1:  # Ensure at least admin remains
                    available_users = users[users["login_id"] != st.session_state.current_user]["login_id"].tolist()
                    user_to_delete = st.selectbox("Select User to Delete", available_users, key="delete_user")
                    if st.button("🗑 Delete User"):
                        users = users[users["login_id"] != user_to_delete]
                        save_users(users)
                        st.success(f"User {user_to_delete} deleted successfully ✅")
                        rerun()
                else:
                    st.warning("Cannot delete the last user account ⚠️")

            st.markdown("---")
            st.subheader("📊 Login Audit Log")
            audit_log = load_audit_log()
            if not audit_log.empty:
                st.dataframe(audit_log, use_container_width=True)
                st.download_button(
                    "📥 Download Audit Log",
                    data=audit_log.to_csv(index=False).encode(),
                    file_name="audit_log.csv",
                    key="download_audit"
                )
            else:
                st.info("No audit logs available yet. 📝")

            st.markdown("---")
            st.subheader("📝 Change Log")
            change_log = load_change_log()
            if not change_log.empty:
                st.dataframe(change_log, use_container_width=True)
                st.download_button(
                    "📥 Download Change Log",
                    data=change_log.to_csv(index=False).encode(),
                    file_name="change_log.csv",
                    key="download_change_log"
                )
            else:
                st.info("No change logs available yet. 📝")

            st.markdown("---")
            st.subheader("🗑 Deletion Requests")
            requests = load_deletion_requests()
            if not requests.empty:
                pending_requests = requests[requests["status"] == "pending"]
                if not pending_requests.empty:
                    st.subheader("Pending Requests")
                    for idx, row in pending_requests.iterrows():
                        with st.expander(f"Request {idx}: Student {row['student_id']} by {row['staff_id']} ({row['dept_id']}) - {row['timestamp']}"):
                            st.write(f"**Reason:** {row['reason']}")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"✅ Accept {idx}", key=f"accept_{idx}"):
                                    process_deletion_request(idx, "accept")
                            with col2:
                                if st.button(f"❌ Reject {idx}", key=f"reject_{idx}"):
                                    process_deletion_request(idx, "reject")
                processed_requests = requests[requests["status"] != "pending"]
                if not processed_requests.empty:
                    st.subheader("Processed Requests")
                    st.dataframe(processed_requests, use_container_width=True)
                st.download_button(
                    "📥 Download All Requests",
                    data=requests.to_csv(index=False).encode(),
                    file_name="deletion_requests.csv",
                    key="download_requests"
                )
            else:
                st.info("No deletion requests available yet. 📝")

            st.markdown("---")
            st.markdown(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")