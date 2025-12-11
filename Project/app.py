import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import create_users_table, register_user, verify_user
import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Social Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== FIXED CSS - WON'T BREAK INPUTS ==========
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Container for auth forms */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    
    .auth-container {
        background: white;
        border-radius: 16px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        padding: 40px;
        width: 100%;
        max-width: 440px;
    }
    
    /* Modern header */
    .dashboard-header {
        background: white;
        padding: 16px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,.08);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    /* Card styling */
    .analytics-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,.08);
        margin-bottom: 24px;
        border: 1px solid rgba(0,0,0,.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .analytics-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,.12);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,.05);
        border-top: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,.1);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom titles */
    .brand-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #2d3748;
        margin: 0 0 16px 0;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active { background-color: #48bb78; }
    .status-inactive { background-color: #e53e3e; }
    
    /* Activity timeline */
    .activity-item {
        padding: 12px 0;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
    }
    
    .activity-item:last-child {
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)
# ========== INITIALIZE SESSION STATE ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# ========== CREATE TABLES ==========
create_users_table()

# ========== MODERN HEADER ==========
def show_header():
    st.markdown("""
    <div class="main-header">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center;">
                <h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.5px;">Social Analytics</h1>
                <span style="margin-left: 12px; font-size: 22px;">📈</span>
            </div>
            <div style="color: rgba(255,255,255,0.9); font-weight: 500; font-size: 15px;">
                Real-time Social Media Insights
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)

# ========== AUTHENTICATION PAGES ==========
def show_login_register():
    """Show login or register form with modern design."""
    show_header()
    
    st.markdown("""
    <div class='auth-container'>
        <div style='text-align: center; margin-bottom: 30px;'>
            <div style='font-size: 32px; margin-bottom: 10px;'>📊</div>
            <h2 style='margin: 0; color: #2d3436; font-weight: 700;'>Welcome Back</h2>
            <p style='color: #636e72; margin-top: 8px;'>Sign in to access your analytics dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Sign In", "👤 Create Account"])
    
    with tab1:
        with st.form("login_form"):
            st.markdown("<div class='section-title'>Login to Your Account</div>", unsafe_allow_html=True)
            login_user = st.text_input("Username", placeholder="Enter your username")
            login_pass = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                login_submit = st.form_submit_button("Sign In", use_container_width=True)
            with col2:
                if st.form_submit_button("Forgot Password?", use_container_width=True):
                    st.info("Password reset feature would be implemented here")
            
            if login_submit:
                if not login_user or not login_pass:
                    st.error("Please enter both username and password")
                elif verify_user(login_user, login_pass):
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.session_state.user_data = {'login_time': datetime.datetime.now()}
                    st.success(f"Welcome back, {login_user}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            st.markdown("<div class='section-title'>Create New Account</div>", unsafe_allow_html=True)
            reg_user = st.text_input("Choose Username", placeholder="Enter unique username")
            reg_email = st.text_input("Email Address", placeholder="your.email@example.com")
            reg_pass = st.text_input("Create Password", type="password", placeholder="Minimum 8 characters")
            reg_pass_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            register_submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if register_submit:
                if not all([reg_user, reg_email, reg_pass, reg_pass_confirm]):
                    st.error("All fields are required")
                elif len(reg_pass) < 8:
                    st.error("Password must be at least 8 characters")
                elif reg_pass != reg_pass_confirm:
                    st.error("Passwords do not match")
                elif "@" not in reg_email or "." not in reg_email:
                    st.error("Please enter a valid email address")
                else:
                    if register_user(reg_user, reg_pass, reg_email):
                        st.success("Account created successfully! Please sign in.")
                    else:
                        st.error("Username already exists. Please choose another.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer note
    st.markdown("""
    <div style='text-align: center; color: #636e72; margin-top: 30px; font-size: 14px;'>
        <p>By continuing, you agree to our <a href='#' style='color: #667eea; text-decoration: none;'>Terms of Service</a> 
        and <a href='#' style='color: #667eea; text-decoration: none;'>Privacy Policy</a></p>
    </div>
    """, unsafe_allow_html=True)

# ========== DASHBOARD PAGE ==========
def main_dashboard():
    """Main analytics dashboard with modern design."""
    show_header()
    
    # User navigation bar
    st.markdown(f"""
    <div class='user-nav'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <span style='font-weight: 600; color: #2d3436;'>Welcome, {st.session_state.username}!</span>
                <span style='color: #636e72; font-size: 14px; margin-left: 15px;'>
                    Last login: {st.session_state.user_data.get('login_time', 'Today')}
                </span>
            </div>
            <div>
                <button onclick="window.location.reload()" style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 8px 20px;
                    border-radius: 6px;
                    font-weight: 500;
                    cursor: pointer;
                '>🔄 Refresh Data</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    with st.sidebar:
        st.markdown("### Account Settings")
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.metric("Active Users", "1,245", "+12%")
        st.metric("Engagement Rate", "4.8%", "+0.3%")
        st.metric("Response Time", "28m", "-5m")
    
    # ========== DASHBOARD CONTENT ==========
    st.markdown("<div class='page-title'>📊 Social Media Analytics Dashboard</div>", unsafe_allow_html=True)
    
    # Row 1: Key Metrics
    st.markdown("<div class='section-title'>Performance Overview</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 24px; color: #667eea;'>📱</div>
            <div style='font-size: 28px; font-weight: 700; color: #2d3436;'>12.5K</div>
            <div style='color: #636e72; font-size: 14px;'>Total Followers</div>
            <div style='color: #4CAF50; font-size: 12px; margin-top: 5px;'>▲ 8.2% from last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='border-left-color: #4CAF50;'>
            <div style='font-size: 24px; color: #4CAF50;'>👥</div>
            <div style='font-size: 28px; font-weight: 700; color: #2d3436;'>1,245</div>
            <div style='color: #636e72; font-size: 14px;'>Engaged Users</div>
            <div style='color: #4CAF50; font-size: 12px; margin-top: 5px;'>▲ 12.5% from last week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card' style='border-left-color: #FF9800;'>
            <div style='font-size: 24px; color: #FF9800;'>📈</div>
            <div style='font-size: 28px; font-weight: 700; color: #2d3436;'>4.8%</div>
            <div style='color: #636e72; font-size: 14px;'>Engagement Rate</div>
            <div style='color: #4CAF50; font-size: 12px; margin-top: 5px;'>▲ 0.8% from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card' style='border-left-color: #F44336;'>
            <div style='font-size: 24px; color: #F44336;'>⏱️</div>
            <div style='font-size: 28px; font-weight: 700; color: #2d3436;'>28m</div>
            <div style='color: #636e72; font-size: 14px;'>Avg. Response Time</div>
            <div style='color: #F44336; font-size: 12px; margin-top: 5px;'>▼ 12% faster</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Row 2: Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='analytics-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📱 Follower Growth Trend</div>", unsafe_allow_html=True)
        
        # Sample data for follower growth
        follower_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'Followers': [8500, 8900, 9200, 9500, 9800, 10100, 10500, 10900, 11200, 11500, 11800, 12500],
            'Target': [9000, 9200, 9400, 9700, 10000, 10300, 10600, 11000, 11300, 11700, 12000, 12500]
        })
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=follower_data['Month'], 
            y=follower_data['Followers'],
            mode='lines+markers',
            name='Actual Followers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        fig1.add_trace(go.Scatter(
            x=follower_data['Month'], 
            y=follower_data['Target'],
            mode='lines',
            name='Target',
            line=dict(color='#4CAF50', width=2, dash='dash')
        ))
        
        fig1.update_layout(
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='analytics-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>👥 Engagement by Platform</div>", unsafe_allow_html=True)
        
        # Sample data for platform engagement
        platform_data = pd.DataFrame({
            'Platform': ['Instagram', 'Twitter', 'Facebook', 'LinkedIn', 'TikTok'],
            'Engagement': [38, 22, 18, 12, 10],
            'Color': ['#E1306C', '#1DA1F2', '#1877F2', '#0077B5', '#000000']
        })
        
        fig2 = px.pie(
            platform_data, 
            values='Engagement', 
            names='Platform',
            color='Platform',
            color_discrete_map={
                'Instagram': '#E1306C',
                'Twitter': '#1DA1F2',
                'Facebook': '#1877F2',
                'LinkedIn': '#0077B5',
                'TikTok': '#000000'
            },
            hole=0.4
        )
        
        fig2.update_layout(
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=40, b=40)
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 3: Recent Activity
    st.markdown("<div class='section-title'>📋 Recent Social Activity</div>", unsafe_allow_html=True)
    st.markdown("<div class='analytics-card'>", unsafe_allow_html=True)
    
    activity_data = pd.DataFrame({
        'Time': ['2 min ago', '15 min ago', '1 hour ago', '3 hours ago', '5 hours ago'],
        'Platform': ['Twitter', 'Instagram', 'Facebook', 'LinkedIn', 'Twitter'],
        'Activity': ['New mention from @TechReview', 'Photo received 245 likes', 'Page liked by 12 new users', 'Connection request accepted', 'Tweet reached 1.2K impressions'],
        'Engagement': ['High', 'High', 'Medium', 'Low', 'High']
    })
    
    # Custom HTML table for better styling
    st.markdown("""
    <style>
        .activity-table {
            width: 100%;
            border-collapse: collapse;
        }
        .activity-table th {
            background-color: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #2d3436;
            border-bottom: 2px solid #eaeaea;
        }
        .activity-table td {
            padding: 12px;
            border-bottom: 1px solid #eaeaea;
        }
        .activity-table tr:hover {
            background-color: #f8f9fa;
        }
        .engagement-high { color: #4CAF50; font-weight: 600; }
        .engagement-medium { color: #FF9800; font-weight: 600; }
        .engagement-low { color: #F44336; font-weight: 600; }
    </style>
    
    <table class='activity-table'>
        <tr>
            <th>Time</th>
            <th>Platform</th>
            <th>Activity</th>
            <th>Engagement</th>
        </tr>
    """, unsafe_allow_html=True)
    
    for _, row in activity_data.iterrows():
        engagement_class = f"engagement-{row['Engagement'].lower()}"
        st.markdown(f"""
        <tr>
            <td>{row['Time']}</td>
            <td><strong>{row['Platform']}</strong></td>
            <td>{row['Activity']}</td>
            <td class='{engagement_class}'>{row['Engagement']}</td>
        </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("</table></div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #636e72; margin-top: 40px; padding: 20px; font-size: 14px; border-top: 1px solid #eaeaea;'>
        <p>Social Analytics Dashboard v2.0 • Data updates every 15 minutes</p>
        <p style='font-size: 12px; margin-top: 5px;'>
            Need help? <a href='#' style='color: #667eea; text-decoration: none;'>Contact Support</a> • 
            <a href='#' style='color: #667eea; text-decoration: none;'>Privacy Policy</a> • 
            <a href='#' style='color: #667eea; text-decoration: none;'>Terms of Service</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========== MAIN APP LOGIC ==========
if __name__ == "__main__":
    if st.session_state.logged_in:
        main_dashboard()
    else:
        show_login_register()