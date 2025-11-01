import streamlit as st
import requests
import os
from datetime import datetime
import pandas as pd
from config import Config

# Page configuration
st.set_page_config(
    page_title="BHIV Candidate Portal",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize config
config = Config()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4e79;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .job-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
    .status-applied { color: #28a745; font-weight: bold; }
    .status-pending { color: #ffc107; font-weight: bold; }
    .status-rejected { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint, method="GET", data=None, headers=None):
    """Make API request to Gateway service"""
    try:
        url = f"{config.GATEWAY_URL}{endpoint}"
        default_headers = {"Authorization": f"Bearer {config.API_KEY}"}
        if headers:
            default_headers.update(headers)
        
        if method == "GET":
            response = requests.get(url, headers=default_headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=default_headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=default_headers, timeout=10)
        
        return response.json() if response.status_code == 200 else {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def login_page():
    """Candidate login/registration page"""
    st.markdown('<div class="main-header"><h1>🎯 BHIV Candidate Portal</h1><p>Your Gateway to Career Opportunities</p></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if email and password:
                    # Call candidate login API
                    login_data = {"email": email, "password": password}
                    result = make_api_request("/v1/candidate/login", "POST", login_data)
                    
                    if "error" not in result and result.get("success"):
                        st.session_state.candidate_logged_in = True
                        st.session_state.candidate_data = result.get("candidate", {})
                        st.session_state.candidate_token = result.get("token")
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(f"Login failed: {result.get('error', 'Invalid credentials')}")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="john.doe@example.com")
                phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")
            with col2:
                location = st.text_input("Location", placeholder="New York, NY")
                experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=0)
                password = st.text_input("Password", type="password")
            
            skills = st.text_area("Technical Skills", placeholder="Python, JavaScript, React, SQL...")
            education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD", "Other"])
            
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                if all([name, email, password]):
                    # Call candidate registration API
                    register_data = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "location": location,
                        "experience_years": experience,
                        "technical_skills": skills,
                        "education_level": education,
                        "password": password
                    }
                    result = make_api_request("/v1/candidate/register", "POST", register_data)
                    
                    if "error" not in result and result.get("success"):
                        st.success("Account created successfully! Please login.")
                        st.balloons()
                    else:
                        st.error(f"Registration failed: {result.get('error', 'Unknown error')}")
                else:
                    st.error("Please fill in required fields (Name, Email, Password)")

def dashboard_page():
    """Main candidate dashboard"""
    candidate = st.session_state.candidate_data
    
    # Header
    st.markdown(f'<div class="main-header"><h1>Welcome back, {candidate.get("name", "Candidate")}! 👋</h1><p>Manage your job applications and profile</p></div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150/1f4e79/white?text=BHIV", width=150)
        st.markdown(f"**{candidate.get('name', 'Candidate')}**")
        st.markdown(f"📧 {candidate.get('email', 'N/A')}")
        st.markdown(f"📍 {candidate.get('location', 'N/A')}")
        st.markdown(f"💼 {candidate.get('experience_years', 0)} years experience")
        
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💼 Job Search", "📋 My Applications", "👤 Profile"])
    
    with tab1:
        dashboard_overview()
    
    with tab2:
        job_search_page()
    
    with tab3:
        my_applications_page()
    
    with tab4:
        profile_management_page()

def dashboard_overview():
    """Dashboard overview with metrics"""
    st.subheader("📊 Your Dashboard Overview")
    
    # Get candidate applications
    candidate_id = st.session_state.candidate_data.get("id")
    applications = make_api_request(f"/v1/candidate/applications/{candidate_id}")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_apps = len(applications.get("applications", []))
        st.markdown(f'<div class="metric-card"><h3>{total_apps}</h3><p>Total Applications</p></div>', unsafe_allow_html=True)
    
    with col2:
        pending_apps = len([app for app in applications.get("applications", []) if app.get("status") == "applied"])
        st.markdown(f'<div class="metric-card"><h3>{pending_apps}</h3><p>Pending Review</p></div>', unsafe_allow_html=True)
    
    with col3:
        interviews = len([app for app in applications.get("applications", []) if app.get("status") == "interviewed"])
        st.markdown(f'<div class="metric-card"><h3>{interviews}</h3><p>Interviews</p></div>', unsafe_allow_html=True)
    
    with col4:
        offers = len([app for app in applications.get("applications", []) if app.get("status") == "offered"])
        st.markdown(f'<div class="metric-card"><h3>{offers}</h3><p>Job Offers</p></div>', unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    if applications.get("applications"):
        recent_apps = applications["applications"][:5]
        for app in recent_apps:
            status_class = f"status-{app.get('status', 'pending').lower()}"
            st.markdown(f"""
            <div class="job-card">
                <h4>{app.get('job_title', 'Unknown Position')}</h4>
                <p><strong>Company:</strong> {app.get('company', 'N/A')} | <strong>Status:</strong> <span class="{status_class}">{app.get('status', 'Pending').title()}</span></p>
                <p><strong>Applied:</strong> {app.get('applied_date', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No applications yet. Start by browsing available jobs!")

def job_search_page():
    """Job search and application page"""
    st.subheader("💼 Browse Available Jobs")
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search_skills = st.text_input("Skills", placeholder="Python, React, SQL...")
    with col2:
        search_location = st.text_input("Location", placeholder="New York, Remote...")
    with col3:
        min_experience = st.number_input("Min Experience (years)", min_value=0, value=0)
    
    # Get jobs
    jobs_data = make_api_request("/v1/jobs")
    jobs = jobs_data.get("jobs", [])
    
    # Filter jobs based on search criteria
    if search_skills or search_location or min_experience > 0:
        filtered_jobs = []
        for job in jobs:
            match = True
            if search_skills and search_skills.lower() not in job.get("requirements", "").lower():
                match = False
            if search_location and search_location.lower() not in job.get("location", "").lower():
                match = False
            if min_experience > 0:
                # Extract experience from requirements (simplified)
                job_exp = 0
                req = job.get("requirements", "").lower()
                if "senior" in req or "5+" in req:
                    job_exp = 5
                elif "mid" in req or "3+" in req:
                    job_exp = 3
                elif "junior" in req or "2+" in req:
                    job_exp = 2
                if job_exp < min_experience:
                    match = False
            if match:
                filtered_jobs.append(job)
        jobs = filtered_jobs
    
    st.write(f"Found {len(jobs)} jobs")
    
    # Display jobs
    for job in jobs:
        with st.expander(f"🏢 {job.get('title', 'Unknown')} - {job.get('department', 'N/A')}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Location:** {job.get('location', 'N/A')}")
                st.write(f"**Experience Level:** {job.get('experience_level', 'N/A')}")
                st.write(f"**Requirements:** {job.get('requirements', 'N/A')}")
                st.write(f"**Description:** {job.get('description', 'N/A')}")
                st.write(f"**Posted:** {job.get('created_at', 'N/A')}")
            
            with col2:
                if st.button(f"Apply Now", key=f"apply_{job.get('id')}", use_container_width=True):
                    # Apply for job
                    candidate_id = st.session_state.candidate_data.get("id")
                    application_data = {
                        "candidate_id": candidate_id,
                        "job_id": job.get("id"),
                        "cover_letter": "Applied through candidate portal"
                    }
                    result = make_api_request("/v1/candidate/apply", "POST", application_data)
                    
                    if "error" not in result and result.get("success"):
                        st.success("Application submitted successfully!")
                        st.rerun()
                    else:
                        st.error(f"Application failed: {result.get('error', 'Unknown error')}")

def my_applications_page():
    """View and manage applications"""
    st.subheader("📋 My Job Applications")
    
    candidate_id = st.session_state.candidate_data.get("id")
    applications_data = make_api_request(f"/v1/candidate/applications/{candidate_id}")
    applications = applications_data.get("applications", [])
    
    if not applications:
        st.info("You haven't applied to any jobs yet. Browse available positions to get started!")
        return
    
    # Applications table
    df_data = []
    for app in applications:
        df_data.append({
            "Job Title": app.get("job_title", "N/A"),
            "Company": app.get("company", "N/A"),
            "Status": app.get("status", "pending").title(),
            "Applied Date": app.get("applied_date", "N/A"),
            "Last Updated": app.get("updated_at", "N/A")
        })
    
    if df_data:
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    
    # Detailed view
    st.subheader("📄 Application Details")
    for app in applications:
        status_class = f"status-{app.get('status', 'pending').lower()}"
        
        with st.expander(f"{app.get('job_title', 'Unknown Position')} - {app.get('company', 'N/A')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Status:** {app.get('status', 'Pending').title()}")
                st.write(f"**Applied:** {app.get('applied_date', 'N/A')}")
                st.write(f"**Location:** {app.get('location', 'N/A')}")
            
            with col2:
                st.write(f"**Experience Required:** {app.get('experience_level', 'N/A')}")
                st.write(f"**Department:** {app.get('department', 'N/A')}")
                st.write(f"**Last Updated:** {app.get('updated_at', 'N/A')}")
            
            if app.get("interview_date"):
                st.info(f"🗓️ Interview scheduled for: {app.get('interview_date')}")
            
            if app.get("feedback"):
                st.success(f"💬 Feedback: {app.get('feedback')}")

def profile_management_page():
    """Manage candidate profile"""
    st.subheader("👤 Manage Your Profile")
    
    candidate = st.session_state.candidate_data
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=candidate.get("name", ""))
            email = st.text_input("Email", value=candidate.get("email", ""), disabled=True)
            phone = st.text_input("Phone", value=candidate.get("phone", ""))
            location = st.text_input("Location", value=candidate.get("location", ""))
        
        with col2:
            experience = st.number_input("Years of Experience", 
                                       min_value=0, max_value=50, 
                                       value=candidate.get("experience_years", 0))
            education = st.selectbox("Education Level", 
                                   ["High School", "Bachelor's", "Master's", "PhD", "Other"],
                                   index=0 if not candidate.get("education_level") else 
                                   ["High School", "Bachelor's", "Master's", "PhD", "Other"].index(candidate.get("education_level", "Bachelor's")))
            seniority = st.selectbox("Seniority Level",
                                   ["Junior", "Mid", "Senior", "Lead", "Principal"],
                                   index=0 if not candidate.get("seniority_level") else
                                   ["Junior", "Mid", "Senior", "Lead", "Principal"].index(candidate.get("seniority_level", "Junior")))
        
        skills = st.text_area("Technical Skills", 
                            value=candidate.get("technical_skills", ""),
                            placeholder="Python, JavaScript, React, SQL, AWS...")
        
        # Resume upload
        st.subheader("📄 Resume")
        uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'txt'])
        
        if st.form_submit_button("Update Profile", use_container_width=True):
            # Update profile data
            update_data = {
                "name": name,
                "phone": phone,
                "location": location,
                "experience_years": experience,
                "technical_skills": skills,
                "education_level": education,
                "seniority_level": seniority
            }
            
            candidate_id = candidate.get("id")
            result = make_api_request(f"/v1/candidate/profile/{candidate_id}", "PUT", update_data)
            
            if "error" not in result and result.get("success"):
                st.success("Profile updated successfully!")
                # Update session data
                st.session_state.candidate_data.update(update_data)
                st.rerun()
            else:
                st.error(f"Profile update failed: {result.get('error', 'Unknown error')}")

def main():
    """Main application logic"""
    # Check if candidate is logged in
    if not st.session_state.get("candidate_logged_in", False):
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
