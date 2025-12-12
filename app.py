import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime, timedelta, date
import hashlib
from html import escape
import difflib
from sqlalchemy.sql import text
import requests
import xml.etree.ElementTree as ET

# --- ENHANCED AI IMPORTS ---
import re

# --- UPDATED: Sentence Transformers Only ---
try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# --- 1. ENHANCED CSS FOR FINANCIAL AUTOMATION UI ---
def load_css():
    """Loads custom CSS for modern financial automation dashboard."""
    css = """
    <style>
        /* --- Modern Financial Dashboard Styling --- */
        @keyframes fadeIn {
            from { 
                opacity: 0; 
                transform: translateY(15px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        /* Apply animations to main content */
        div.st-emotion-cache-1r4qj8v, div.st-emotion-cache-1pezo1l, [data-testid="stAppViewContainer"] [data-testid="stVerticalBlock"] {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Main container styling - WIDER FOR WEB */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 95%;
        }
        
        /* --- Financial Dashboard Header --- */
        .dashboard-header {
            background: linear-gradient(135deg, #001f3f 0%, #003366 100%);
            padding: 2.5rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .dashboard-title {
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .dashboard-subtitle {
            font-size: 1.3rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        /* --- Metric Cards --- */
        .metric-card {
            background: white;
            padding: 1.8rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 1px solid #f0f0f0;
            text-align: center;
            transition: transform 0.3s ease;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: #333;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            font-size: 1rem;
            color: #666;
            font-weight: 500;
        }
        
        .metric-trend {
            font-size: 0.85rem;
            font-weight: 600;
            padding: 0.3rem 0.8rem;
            border-radius: 12px;
            display: inline-block;
        }
        
        .trend-up {
            background: #e8f5e8;
            color: #2e7d32;
        }
        
        .trend-down {
            background: #ffebee;
            color: #c62828;
        }
        
        /* --- Feature Cards --- */
        .feature-card {
            background: white;
            padding: 2.2rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #f0f0f0;
            height: 280px;
            transition: all 0.3s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }
        
        .feature-icon {
            font-size: 3.2rem;
            margin-bottom: 1.2rem;
            background: linear-gradient(135deg, #001f3f, #003366);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .feature-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 1.2rem;
        }
        
        .feature-description {
            color: #666;
            line-height: 1.6;
            font-size: 1rem;
        }
        
        /* --- Navigation Cards --- */
        .nav-card {
            background: white;
            padding: 1.8rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 1px solid #f0f0f0;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .nav-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            border-color: #001f3f;
        }

        .nav-icon {
            font-size: 2.8rem;
            margin-bottom: 1.2rem;
            color: #001f3f;
        }
        
        .nav-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 0.8rem;
        }
        
        .nav-description {
            color: #666;
            font-size: 0.95rem;
        }
        
        /* --- Process Steps --- */
        .process-steps {
            display: flex;
            justify-content: space-between;
            margin: 2.5rem 0;
            gap: 1.5rem;
        }
        
        .process-step {
            text-align: center;
            flex: 1;
            position: relative;
        }
        
        .step-number {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #001f3f, #003366);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.2rem;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        .step-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 0.8rem;
            font-size: 1.1rem;
        }
        
        .step-description {
            color: #666;
            font-size: 0.95rem;
        }
        
        /* --- Button Styling --- */
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
            padding: 0.85rem 2.2rem;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        
        .primary-button {
            background: linear-gradient(135deg, #001f3f, #003366);
            color: white;
            border: none;
        }

        .primary-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 31, 63, 0.4);
        }
        
        /* --- Data Upload Cards --- */
        .upload-card {
            background: white;
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 2px dashed #ddd;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .upload-card:hover {
            border-color: #001f3f;
            background: #f0f4f8;
        }

        .upload-icon {
            font-size: 3.5rem;
            color: #001f3f;
            margin-bottom: 1.2rem;
        }
        
        /* --- Status Indicators --- */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        .status-success {
            background: #e8f5e8;
            color: #2e7d32;
        }
        
        .status-warning {
            background: #fff3e0;
            color: #ef6c00;
        }
        
        .status-error {
            background: #ffebee;
            color: #c62828;
        }
        
        /* --- Progress Bars --- */
        .progress-container {
            background: #f0f0f0;
            border-radius: 10px;
            height: 10px;
            margin: 1.2rem 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(135deg, #001f3f, #003366);
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        /* --- WEB-SPECIFIC ADJUSTMENTS (Remove mobile optimizations) --- */
        .dashboard-title {
            font-size: 2.8rem;
        }
        
        .process-steps {
            flex-direction: row;
            gap: 1.5rem;
        }
        
        .metric-card {
            padding: 1.8rem;
        }
        
        .metric-value {
            font-size: 2.2rem;
        }
        
        /* --- Sidebar Styling - WIDER FOR WEB --- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
            border-right: 1px solid #e0e0e0;
            min-width: 300px !important;
            max-width: 350px !important;
        }
        
        .sidebar-header {
            padding: 2rem;
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 1.5rem;
        }
        
        .sidebar-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .sidebar-subtitle {
            font-size: 1rem;
            color: #666;
        }
        
        /* Sidebar buttons - larger for web */
        .sidebar-button {
            padding: 0.9rem 1.5rem !important;
            font-size: 1.05rem !important;
            margin: 0.3rem 0 !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        
        /* --- Form Styling - WIDER FOR WEB --- */
        .form-container {
            background: white;
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin: 1.5rem 0;
            max-width: 100%;
        }
        
        .form-title {
            font-size: 1.6rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 2rem;
        }
        
        /* --- Table Styling --- */
        .data-table {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        /* --- Color Scheme --- */
        :root {
            --primary-color: #001f3f;
            --secondary-color: #003366;
            --accent-color: #ffffff;
            --success-color: #2e7d32;
            --warning-color: #ef6c00;
            --error-color: #c62828;
        }
        
        /* --- Header Login Button --- */
        .header-login {
            position: absolute;
            top: 1.5rem;
            left: 1.5rem;
            z-index: 1000;
        }
        
        /* --- Professional Login Page Styles - WIDER FOR WEB --- */
        .login-container {
            max-width: 500px;
            margin: 3rem auto;
            padding: 3rem;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .login-logo {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #001f3f, #003366);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .login-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 0.8rem;
        }
        
        .login-subtitle {
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 2.5rem;
        }
        
        .security-badge {
            display: inline-flex;
            align-items: center;
            background: #e8f5e8;
            color: #2e7d32;
            padding: 0.7rem 1.5rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            margin: 0.8rem 0;
        }
        
        .sso-button {
            width: 100%;
            padding: 1rem;
            border: 2px solid #f0f0f0;
            border-radius: 12px;
            background: white;
            color: #333;
            font-weight: 500;
            margin: 0.7rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        
        .sso-button:hover {
            border-color: #001f3f;
            background: #f0f4f8;
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 2rem 0;
        }
        
        .divider::before, .divider::after {
            content: "";
            flex: 1;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .divider-text {
            padding: 0 1.5rem;
            color: #666;
            font-size: 1rem;
        }
        
        .login-footer {
            text-align: center;
            margin-top: 2.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #f0f0f0;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 1.2rem 0;
        }
        
        .footer-link {
            color: #666;
            text-decoration: none;
            font-size: 0.9rem;
        }
        
        .footer-link:hover {
            color: #001f3f;
        }
        
        .security-features {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.2rem 0;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            margin: 0.7rem 0;
            font-size: 0.9rem;
            color: #666;
        }
        
        .feature-icon-small {
            margin-right: 0.7rem;
            color: #2e7d32;
        }
        
        .captcha-container {
            background: #f9f9f9;
            border: 1px solid #e0e0f0;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1.2rem 0;
            text-align: center;
        }
        
        .last-login {
            background: #fff3e0;
            padding: 1rem;
            border-radius: 10px;
            margin: 1.2rem 0;
            font-size: 0.9rem;
            color: #ef6c00;
        }
        
        /* --- Compact Form Styling - WIDER FOR WEB --- */
        .compact-form {
            max-width: 500px;
            margin: 0 auto;
        }
        
        /* --- Data Editor Improvements for Web --- */
        .stDataEditor {
            font-size: 1rem !important;
        }
        
        /* --- Streamlit Native Element Overrides for Web --- */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            font-size: 1rem !important;
            padding: 0.8rem 1rem !important;
        }
        
        .stCheckbox label {
            font-size: 1rem !important;
        }
        
        /* --- Wider columns for web layouts --- */
        .stColumns {
            gap: 1.5rem;
        }
        
        /* --- Tab improvements for web --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem !important;
            font-size: 1rem !important;
        }
        
        /* --- Expand all streamlit components by default --- */
        .stExpander {
            border: 1px solid #e0e0f0;
            border-radius: 10px;
        }
        
        .stExpander details {
            background: white;
        }
        
        .stExpander summary {
            padding: 1rem 1.5rem;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        /* Force expanders to be open by default */
        .stExpander details[open] {
            background: white;
        }
        
        /* Make sure all content is visible */
        [data-testid="stExpander"] details[open] {
            background: white;
        }
        
        /* Ensure wide layout for all containers */
        .stApp {
            max-width: 100% !important;
        }
        
        /* Remove any max-width restrictions */
        .block-container {
            max-width: 100% !important;
            padding-left: 5% !important;
            padding-right: 5% !important;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 2. POLICY TEXT TEMPLATES ---
PRIVACY_POLICY_TEXT = """
## Privacy Policy
**Last Updated: November 6, 2025**
**Xml2Tally** ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our Dynamic Tally Converter application (the "Service").

### 1. Information We Collect
We may collect personal information from you in a variety of ways:
* **Personal Data:** When you register for an account, we collect your name, email address, phone number, and a hashed password.
* **Payment Data:** When you make your subscription payment, you are redirected to our payment processor, Razorpay. We do not store or collect your full payment card details. We only receive a payment confirmation ID, your email, and the amount paid.
* **Usage Data:** Information your browser sends when you use our Service (e.g., IP address, browser type).

### 2. How We Use Your Information
We use the information we collect to:
* Create and manage your account.
* Process your subscription payments.
* Provide you with the Tally conversion service.
* Notify you of your subscription status or trial expiry.
* Respond to your support requests.
* Monitor and analyze usage to improve our Service.

### 3. How We Protect Your Information
We use administrative, technical, and physical security measures to protect your personal information.
* All passwords are stored in a **hashed** format. We never store plain-text passwords.
* Our user database is secured.
* Payment processing is handled by Razorpay, a secure, PCI-compliant provider.

### 4. Data Sharing
We do not sell, trade, or rent your personal information to third parties. We may share information with:
* **Payment Processors:** With Razorpay, to process your payment.
* **Law Enforcement:** If required by law or to respond to valid legal processes.

### 5. Your Rights
You have the right to access, correct, or delete your personal information. Please contact us at <strong style="white-space: nowrap;">support@xml2tally.in</strong> to make such a request.

### 6. Contact Us
If you have any questions about this Privacy Policy, please contact us at:
<strong style="white-space: nowrap;">support@xml2tally.in</strong>
"""
TERMS_POLICY_TEXT = """
## Terms & Conditions
**Last Updated: November 6, 2025**
Please read these Terms and Conditions ("Terms") carefully before using the Dynamic Tally Converter (the "Service") operated by **Xml2Tally** ("us", "we", or "our").

### 1. Agreement to Terms
By creating an account and using our Service, you agree to be bound by these Terms. If you disagree with any part of the terms, you may not access the Service.

### 2. The Service
Our Service provides a tool to convert CSV or Excel files into a Tally-compatible XML format. You are responsible for the data you upload and for verifying the accuracy of the output XML before importing it into Tally. We are not responsible for any data loss, data corruption, or accounting errors that may result from using this tool.

### 3. Account Registration
* You must be 18 years or older to use this Service.
* You must provide accurate and complete information (Name, Email, Phone).
* You are responsible for safeguarding your password.

### 4. Subscription, Fees, and Free Trial
Access to the Service is provided on a subscription basis.
* **Free Trial:** Upon signing up, you receive a 30-day free trial with full access.
* **Monthly Subscription:** To continue service after your trial, you must purchase a **monthly subscription for ₹199 per month**.
* **Payment:** This fee is processed via our payment partner, Razorpay. Payment extends your account access by 30 days from its current expiry date.
* **Non-refundable:** All subscription fees are non-refundable, as a free trial is provided.

### 5. Limitation of Liability
The Service is provided "AS IS." **Xml2Tally** shall not be liable for any indirect, incidental, special, or consequential damages resulting from the use or inability to use the Service.

### 6. Termination
We may terminate or suspend your account immediately, without prior notice, for any breach of these Terms.

### 7. Contact Us
If you have any questions about these Terms, please contact us at:
**support@xml2tally.in**
"""
REFUND_POLICY_TEXT = """
## Refund & Cancellation Policy
**Last Updated: November 6, 2025**
### Our Policy
The Dynamic Tally Converter application offers a 30-day free trial, during which you can use all features of the service.
After the trial, the Service requires a **monthly subscription fee of ₹199** to maintain access.
**This ₹199 monthly fee is non-refundable.**

### Justification
We offer a 30-day, full-featured free trial, which we deem sufficient for you to evaluate the product. The fee is a recurring charge for continued access to the service. Because we provide the service immediately upon payment, we do not offer refunds for subscription periods.

### Failed Payments
If your payment fails but money is debited from your account, it is typically held by your bank or Razorpay. It will be automatically refunded to your original payment method within 5-7 business days. We do not receive this money.

### Account Activation Failure
If your payment was successful (you have a Payment ID) but your account access was not extended, **do not pay again**.
Please contact our support team immediately. We will manually verify your payment with Razorpay and activate your account.

### Contact Us
For any payment-related issues or questions, please contact us at:
**support@xml2tally.in**
"""

# --- 3. USER AUTHENTICATION & DATABASE ---

def get_db_conn():
    if not os.path.exists("data"):
        os.makedirs("data")
    return st.connection("users_db", type="sql", url="sqlite:///data/users.db")

def hash_password(password):
    return hashlib.sha256(str(password).encode()).hexdigest()

def init_db(seed_admin=None, admin_password=None):
    """Initializes the database schema using st.connection.

    When enabled, seeds a default admin account (email "admin") using the
    password provided via ``admin_password`` or the ``ADMIN_DEFAULT_PASSWORD``
    environment variable (fallback: ``admin@2003``). Admin seeding can be
    disabled by passing ``seed_admin=False`` or setting the
    ``SEED_DEFAULT_ADMIN`` environment variable to a falsy value.
    """
    conn = get_db_conn()
    with conn.session as s:
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT,
                phone TEXT,
                password_hash TEXT,
                signup_date DATE,
                subscription_expiry_date DATE DEFAULT NULL 
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                email TEXT PRIMARY KEY,
                company_name TEXT,
                default_suspense_ledger TEXT,
                FOREIGN KEY (email) REFERENCES users (email)
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS journal_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                template_name TEXT,
                FOREIGN KEY (email) REFERENCES users (email),
                UNIQUE(email, template_name)
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS journal_template_fixed_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id INTEGER,
                csv_col TEXT,
                tally_ledger TEXT,
                type TEXT,
                FOREIGN KEY (template_id) REFERENCES journal_templates (id) ON DELETE CASCADE
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS journal_template_dynamic_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id INTEGER,
                ledger_name_col TEXT,
                amount_col TEXT,
                type TEXT,
                FOREIGN KEY (template_id) REFERENCES journal_templates (id) ON DELETE CASCADE
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS bank_ledger_master (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                ledger_name TEXT,
                FOREIGN KEY (email) REFERENCES users (email)
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS bank_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                keyword TEXT,
                mapped_ledger TEXT,
                FOREIGN KEY (email) REFERENCES users (email)
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS user_learned_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                narration_text TEXT,
                mapped_ledger TEXT,
                similarity_score REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 1,
                last_used DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (email) REFERENCES users (email),
                UNIQUE(email, narration_text)
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS tally_connection_settings (
                email TEXT PRIMARY KEY,
                tally_server_host TEXT DEFAULT 'localhost',
                tally_server_port INTEGER DEFAULT 9000,
                tally_company_name TEXT,
                enable_direct_sync BOOLEAN DEFAULT 0,
                enable_direct_push_bank BOOLEAN DEFAULT 0,
                enable_direct_push_journal BOOLEAN DEFAULT 0,
                sync_ledgers_on_load BOOLEAN DEFAULT 0,
                last_sync_date DATETIME,
                FOREIGN KEY (email) REFERENCES users (email)
            );
        '''))
        s.execute(text('''
            CREATE TABLE IF NOT EXISTS tally_synced_ledgers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                ledger_name TEXT,
                ledger_group TEXT,
                sync_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users (email),
                UNIQUE(email, ledger_name)
            );
        '''))

        # Add Admin User (seeded only when enabled)
        should_seed_admin = seed_admin
        if should_seed_admin is None:
            should_seed_admin = os.getenv("SEED_DEFAULT_ADMIN", "true").lower() in {"1", "true", "yes", "on"}

        if should_seed_admin:
            try:
                admin_pass = admin_password or os.getenv("ADMIN_DEFAULT_PASSWORD", "admin@2003")
                admin_pass_hash = hash_password(admin_pass)
                s.execute(text('''
                    INSERT OR IGNORE INTO users (email, name, phone, password_hash, signup_date, subscription_expiry_date)
                    VALUES (:email, :name, :phone, :pass_hash, DATE('now'), DATE('now', '+100 year'))
                '''), params=dict(
                    email="admin",
                    name="Administrator",
                    phone="0000000000",
                    pass_hash=admin_pass_hash
                ))
                s.commit()
            except Exception as e:
                print(f"Admin user creation: {e}")

def add_user_to_db(email, name, phone, password):
    """Adds a new user."""
    password_hash = hash_password(password)
    conn = get_db_conn()
    try:
        with conn.session as s:
            s.execute(text('''
                INSERT INTO users (email, name, phone, password_hash, signup_date)
                VALUES (:email, :name, :phone, :pass_hash, DATE('now'))
            '''), params=dict(
                email=email,
                name=name,
                phone=phone,
                pass_hash=password_hash
            ))
            s.commit()
        return True
    except Exception as e:
        print(f"User creation error: {e}")
        return False

def check_user_status(email, password):
    """Checks credentials and returns status."""
    try:
        password_hash = hash_password(password)
        conn = get_db_conn()
        with conn.session as s:
            user_data = s.execute(text('''
                SELECT signup_date, subscription_expiry_date FROM users
                WHERE email = :email AND password_hash = :pass_hash
            '''), params=dict(email=email, pass_hash=password_hash)).fetchone()

        if not user_data:
            return "INVALID"
    except Exception as e:
        print(f"Error checking user status: {e}")
        return "INVALID"

    today = date.today()
    
    sub_expiry_str = user_data[1]
    if sub_expiry_str:
        try:
            sub_expiry_date = datetime.strptime(sub_expiry_str, '%Y-%m-%d').date()
            if today <= sub_expiry_date:
                return "PAID"
        except ValueError:
            pass

    signup_date_str = user_data[0]
    if signup_date_str:
        try:
            signup_date = datetime.strptime(signup_date_str, '%Y-%m-%d').date()
            trial_expiry_date = signup_date + timedelta(days=30)
            if today <= trial_expiry_date:
                return "TRIAL"
        except ValueError:
            pass
            
    return "PENDING"

def activate_user_payment(email):
    """Adds 30 days of access to the user's account."""
    try:
        today = date.today()
        base_date = today
        conn = get_db_conn()
        with conn.session as s:
            user = s.execute(text('SELECT subscription_expiry_date FROM users WHERE email = :email'), params=dict(email=email)).fetchone()

            if not user:
                print(f"Warning: User {email} not found during payment activation")
                return False

            sub_expiry_str = user[0]

            if sub_expiry_str:
                try:
                    sub_expiry_date = datetime.strptime(sub_expiry_str, '%Y-%m-%d').date()
                    if sub_expiry_date > today:
                        base_date = sub_expiry_date
                except ValueError:
                    pass

            new_expiry_date = base_date + timedelta(days=30)

            s.execute(text('''
                UPDATE users SET subscription_expiry_date = :new_date WHERE email = :email
            '''), params=dict(new_date=new_expiry_date, email=email))
            s.commit()
            return True

    except Exception as e:
        print(f"Error activating payment for {email}: {e}")
        return False

def load_user_settings(email):
    """Loads all settings for the logged-in user from DB into session_state."""
    # Clear previous user data
    st.session_state.company_name = 'Xml2Tally (Default Co.)'
    st.session_state.journal_templates = {}
    st.session_state.ledger_master = ["Bank Suspense A/c (Default)"]
    st.session_state.bank_rules = []
    st.session_state.default_suspense_ledger = "Bank Suspense A/c (Default)"
    st.session_state.learned_mappings = {}
    
    conn = get_db_conn()
    with conn.session as s:
        # Load user preferences
        pref = s.execute(text('SELECT * FROM user_preferences WHERE email = :email'), params=dict(email=email)).fetchone()
        if pref:
            st.session_state.company_name = pref[1] if len(pref) > 1 and pref[1] else 'Xml2Tally (Default Co.)'
            st.session_state.default_suspense_ledger = pref[2] if len(pref) > 2 and pref[2] else "Bank Suspense A/c (Default)"
        
        # Load journal templates
        templates_db = s.execute(text('SELECT id, template_name FROM journal_templates WHERE email = :email'), params=dict(email=email)).fetchall()
        st.session_state.journal_templates = {r[1]: r[0] for r in templates_db}

        # Load ledger master
        ledger_master_db = s.execute(text('SELECT ledger_name FROM bank_ledger_master WHERE email = :email'), params=dict(email=email)).fetchall()
        if ledger_master_db:
            st.session_state.ledger_master = [r[0] for r in ledger_master_db]
        else:
            # For new users, start with default ledger only
            st.session_state.ledger_master = ["Bank Suspense A/c (Default)"]

        # Load bank rules
        bank_rules_db = s.execute(text('SELECT keyword, mapped_ledger FROM bank_rules WHERE email = :email'), params=dict(email=email)).fetchall()
        if bank_rules_db:
            st.session_state.bank_rules = [{'Narration Keyword': r[0], 'Mapped Ledger': r[1]} for r in bank_rules_db]
        else:
            st.session_state.bank_rules = []
            
        # Load learned mappings
        try:
            learned_mappings_db = s.execute(text('SELECT narration_text, mapped_ledger, similarity_score, usage_count FROM user_learned_mappings WHERE email = :email'), params=dict(email=email)).fetchall()
            st.session_state.learned_mappings = {r[0]: {'ledger': r[1], 'score': r[2], 'count': r[3]} for r in learned_mappings_db}
        except Exception as e:
            print(f"Error loading learned mappings: {e}")
            st.session_state.learned_mappings = {}

        # Load Tally connection settings
        try:
            tally_conn = s.execute(text('SELECT * FROM tally_connection_settings WHERE email = :email'), params=dict(email=email)).fetchone()
            if tally_conn:
                st.session_state.tally_server_host = tally_conn[1] if tally_conn[1] else "localhost"
                st.session_state.tally_server_port = tally_conn[2] if tally_conn[2] else 9000
                st.session_state.tally_company_name = tally_conn[3] if tally_conn[3] else ""
                st.session_state.enable_direct_sync = bool(tally_conn[4]) if tally_conn[4] is not None else False
                st.session_state.enable_direct_push_bank = bool(tally_conn[5]) if tally_conn[5] is not None else False
                st.session_state.enable_direct_push_journal = bool(tally_conn[6]) if tally_conn[6] is not None else False
                st.session_state.sync_ledgers_on_load = bool(tally_conn[7]) if tally_conn[7] is not None else False
        except Exception as e:
            print(f"Error loading Tally connection settings: {e}")
            # Set defaults if loading fails
            st.session_state.tally_server_host = "localhost"
            st.session_state.tally_server_port = 9000
            st.session_state.tally_company_name = ""
            st.session_state.enable_direct_sync = False
            st.session_state.enable_direct_push_bank = False
            st.session_state.enable_direct_push_journal = False
            st.session_state.sync_ledgers_on_load = False

        # Auto-sync ledgers if enabled
        if st.session_state.sync_ledgers_on_load and st.session_state.tally_company_name:
            try:
                success, message, count = sync_ledgers_from_tally(
                    st.session_state.tally_server_host,
                    st.session_state.tally_server_port,
                    st.session_state.tally_company_name,
                    email
                )
                if success:
                    # Load synced ledgers into ledger master
                    synced_ledgers = get_synced_ledgers(email)
                    if synced_ledgers:
                        st.session_state.ledger_master = [row[0] for row in synced_ledgers]
            except Exception as e:
                print(f"Auto-sync failed: {e}")

    st.session_state.settings_loaded = True

# --- 4. ENHANCED AI MAPPING WITHOUT OPENAI ---

class EnhancedLedgerMapper:
    def __init__(self):
        self.model = None
        self.ledger_embeddings = None
        self.ledger_master = None
        self.initialized = False
        
    def initialize_model(self):
        """Initialize the sentence transformer model"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            st.warning("Sentence Transformers not available. Please install: pip install sentence-transformers")
            return False
            
        try:
            with st.spinner("Loading AI model for semantic matching..."):
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.initialized = True
                st.success("Semantic AI model loaded successfully!")
                return True
        except Exception as e:
            st.error(f"Failed to load AI model: {e}")
            return False
    
    def extract_name_from_end(self, narration):
        """Enhanced function to extract names from the end of narration - FOCUS ON LAST 50%"""
        if pd.isna(narration):
            return ""
            
        narration_str = str(narration).upper().strip()
        
        # If narration is short, use the whole thing
        if len(narration_str) <= 20:
            return narration_str
        
        # Focus on the last 50% of the narration - KEY ENHANCEMENT
        start_index = len(narration_str) // 2
        focus_part = narration_str[start_index:]
        
        # Remove common transaction patterns from the focused part
        patterns_to_remove = [
            r'UPI[-]?', r'TXN[-]?', r'REF[-]?', r'IMPS', r'NEFT', r'RTGS', 
            r'UTR?[\d]*', r'CHQ[\d]*', r'CHEQUE[\d]*', r'CREDIT\s*CARD', 
            r'DEBIT\s*CARD', r'ATM', r'IB[\d]*', r'\/', r'\\', r'TRF',
            r'TRANSFER', r'PAYMENT', r'RECEIPT', r'DEPOSIT', r'WITHDRAWAL',
            r'TO\s+', r'FROM\s+', r'BY\s+', r'VIA\s+', r'THROUGH\s+',
            r'BILL\s+NO', r'INVOICE\s+NO', r'REF\s+NO', r'ID\s+', r'TDS\s+',
            r'SALARY', r'PAYROLL', r'VENDOR', r'SUPPLIER', r'CLIENT', r'CUSTOMER',
            r'\d{2,}', r'[\(\)\{\}\[\]]', r'#\w+', r'FOR\s+', r'TOWARD\s+'
        ]
        
        for pattern in patterns_to_remove:
            focus_part = re.sub(pattern, '', focus_part, flags=re.IGNORECASE)
        
        # Remove extra spaces and special characters
        focus_part = re.sub(r'[^a-zA-Z0-9\s]', ' ', focus_part)
        focus_part = re.sub(r'\s+', ' ', focus_part).strip()
        
        # Look for name patterns (2-4 word sequences that look like names)
        words = focus_part.split()
        
        # Common name indicators
        name_indicators = ['MR', 'MRS', 'MS', 'SHRI', 'SMT', 'SRI', 'TO', 'BY']
        
        # Find potential name sequences
        potential_names = []
        
        # Look for sequences of 2-4 words that don't contain common transaction words
        transaction_words = ['BANK', 'ACCOUNT', 'CASH', 'CHEQUE', 'TRANSFER', 'PAYMENT']
        
        for i in range(len(words)):
            for length in [4, 3, 2]:  # Try longer sequences first
                if i + length <= len(words):
                    sequence = ' '.join(words[i:i+length])
                    # Check if this looks like a name (contains no transaction words and has reasonable length)
                    if (len(sequence) >= 3 and 
                        not any(tx_word in sequence for tx_word in transaction_words) and
                        any(word in name_indicators for word in words[i:i+length] if length > 1)):
                        potential_names.append(sequence)
        
        if potential_names:
            # Return the longest potential name
            return max(potential_names, key=len)
        
        # If no clear name pattern, return the last 3 words
        if len(words) >= 3:
            return ' '.join(words[-3:])
        elif words:
            return ' '.join(words)
        
        return focus_part
    
    def identify_person_or_company_name(self, narration):
        """Enhanced name identification focusing on employee, vendor, client names"""
        narration_str = str(narration).upper()
        
        # Keywords that indicate person/company names
        person_indicators = [
            'SALARY', 'PAYROLL', 'EMPLOYEE', 'STAFF', 'PAYMENT TO', 'PAID TO',
            'VENDOR', 'SUPPLIER', 'CONTRACTOR', 'SERVICE PROVIDER',
            'CLIENT', 'CUSTOMER', 'RECEIVED FROM', 'RECEIPT FROM',
            'MR ', 'MRS ', 'MS ', 'SHRI ', 'SMT ', 'SRI '
        ]
        
        # Extract name using the end-focused method
        extracted_name = self.extract_name_from_end(narration)
        
        # Check if this looks like a person/company transaction
        is_person_transaction = any(indicator in narration_str for indicator in person_indicators)
        
        return extracted_name, is_person_transaction
    
    def categorize_transaction(self, narration):
        """Enhanced transaction categorization"""
        narration_lower = str(narration).lower()
        
        # Enhanced expense categories with more keywords
        expense_keywords = {
            'salary': ['salary', 'payroll', 'wage', 'employee', 'staff', 'pay slip'],
            'food': ['zomato', 'swiggy', 'food', 'restaurant', 'cafe', 'pizza', 'burger', 'meal', 'dining'],
            'travel': ['uber', 'ola', 'rapido', 'travel', 'taxi', 'auto', 'fuel', 'petrol', 'diesel', 'transport'],
            'shopping': ['amazon', 'flipkart', 'myntra', 'shopping', 'store', 'market', 'purchase'],
            'utilities': ['electricity', 'water', 'gas', 'bill', 'mobile', 'phone', 'internet', 'broadband'],
            'entertainment': ['netflix', 'hotstar', 'movie', 'cinema', 'theatre', 'entertainment'],
            'healthcare': ['hospital', 'clinic', 'doctor', 'medical', 'pharmacy', 'medicine'],
            'education': ['school', 'college', 'tuition', 'course', 'book', 'education'],
            'vendor': ['vendor', 'supplier', 'contractor', 'service provider'],
            'client': ['client', 'customer', 'received from'],
        }
        
        for category, keywords in expense_keywords.items():
            for keyword in keywords:
                if keyword in narration_lower:
                    return category
        
        # Income categories
        income_keywords = ['salary', 'refund', 'interest', 'dividend', 'commission', 'revenue', 'income']
        for keyword in income_keywords:
            if keyword in narration_lower:
                return 'income'
                
        return 'other'
    
    def calculate_string_similarity(self, str1, str2):
        """Enhanced string similarity calculation"""
        str1 = str1.lower()
        str2 = str2.lower()
        
        if str1 == str2:
            return 1.0
        
        # Sequence matcher for better accuracy
        seq_matcher = difflib.SequenceMatcher(None, str1, str2)
        sequence_ratio = seq_matcher.ratio()
        
        # Word overlap similarity
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return sequence_ratio
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        word_ratio = len(intersection) / len(union) if union else 0
        
        # Combined score (weighted towards sequence matcher)
        return (sequence_ratio * 0.7) + (word_ratio * 0.3)
    
    def preprocess_narration(self, narration):
        """Enhanced preprocessing focusing on end of narration"""
        if pd.isna(narration):
            return ""
        
        narration_str = str(narration).upper()
        
        # Remove common transaction patterns and noise
        patterns_to_remove = [
            r'UPI[-]?', r'TXN[-]?', r'REF[-]?', r'IMPS', r'NEFT', r'RTGS', 
            r'UTR?[\d]*', r'CHQ[\d]*', r'CHEQUE[\d]*', r'CREDIT\s*CARD', 
            r'DEBIT\s*CARD', r'ATM', r'IB[\d]*', r'\/', r'\\', r'TRF',
            r'TRANSFER', r'PAYMENT', r'RECEIPT', r'DEPOSIT', r'WITHDRAWAL',
            r'TO\s+', r'FROM\s+', r'BY\s+', r'VIA\s+', r'THROUGH\s+',
            r'BILL\s+NO', r'INVOICE\s+NO', r'REF\s+NO', r'ID\s+', r'TDS\s+',
            r'\d{2,}', r'[\(\)\{\}\[\]]', r'#\w+'
        ]
        
        for pattern in patterns_to_remove:
            narration_str = re.sub(pattern, '', narration_str, flags=re.IGNORECASE)
        
        # Remove extra spaces and special characters, but keep meaningful words
        narration_str = re.sub(r'[^a-zA-Z0-9\s]', ' ', narration_str)
        narration_str = re.sub(r'\s+', ' ', narration_str).strip()

        return narration_str

    def build_ledger_keyword_index(self, ledger_master):
        """Prepare searchable keyword sets from ledger names"""
        noise_words = {
            'account', 'a/c', 'ac', 'ledger', 'bank', 'cash', 'general',
            'misc', 'miscellaneous', 'expense', 'expenses', 'and', '&'
        }

        keyword_synonyms = {
            'fuel': {'petrol', 'diesel', 'gas', 'cng'},
            'petrol': {'fuel', 'diesel', 'gas', 'cng'},
            'diesel': {'fuel', 'petrol', 'gas', 'cng'},
            'rent': {'lease'},
            'salary': {'payroll', 'wages', 'wage'},
            'travel': {'transport', 'conveyance'},
            'vendor': {'supplier', 'contractor'},
            'client': {'customer', 'debtor'},
            'gst': {'tax'},
            'tds': {'tax'},
        }

        ledger_index = []

        for ledger in ledger_master:
            clean_ledger = self.preprocess_narration(ledger)
            ledger_words = [word for word in clean_ledger.lower().split() if word and word not in noise_words]

            expanded_keywords = set(ledger_words)
            for word in ledger_words:
                expanded_keywords.update(keyword_synonyms.get(word, set()))

            ledger_index.append({
                'ledger': ledger,
                'clean': clean_ledger,
                'keywords': expanded_keywords
            })

        return ledger_index

    def ledger_name_focus_match(self, narration, ledger_master):
        """Prioritize matches that align closely with ledger names"""
        clean_narration = self.preprocess_narration(narration)
        narration_words = set(clean_narration.lower().split()) if clean_narration else set()

        if not narration_words or not ledger_master:
            return None, 0

        ledger_index = self.build_ledger_keyword_index(ledger_master)
        best_ledger = None
        best_score = 0

        for entry in ledger_index:
            overlap = narration_words.intersection(entry['keywords'])
            overlap_score = len(overlap) * 22  # Boost for strong keyword overlap

            name_similarity = self.calculate_string_similarity(clean_narration, entry['clean'])
            similarity_score = name_similarity * 60

            partial_bonus = 20 if entry['clean'] and entry['clean'] in clean_narration else 0

            combined_score = overlap_score + similarity_score + partial_bonus

            if combined_score > best_score and (overlap or name_similarity >= 0.55):
                best_score = combined_score
                best_ledger = entry['ledger']

        if best_ledger:
            return best_ledger, min(95, best_score)

        return None, 0
    
    def compute_ledger_embeddings(self, ledger_master):
        """Compute embeddings for the ledger master"""
        if not self.initialized or not ledger_master:
            return None
            
        try:
            processed_ledgers = [self.preprocess_narration(ledger) for ledger in ledger_master]
            self.ledger_embeddings = self.model.encode(processed_ledgers, convert_to_tensor=True)
            self.ledger_master = ledger_master
            return True
        except Exception as e:
            print(f"Error computing ledger embeddings: {e}")
            return False
    
    def semantic_similarity_match(self, narration, threshold=0.4):
        """Enhanced semantic similarity matching focusing on names"""
        if not self.initialized or self.ledger_embeddings is None:
            return None, 0
            
        try:
            # Use name extraction for better matching
            extracted_name, _ = self.identify_person_or_company_name(narration)
            if extracted_name:
                clean_narration = extracted_name
            else:
                clean_narration = self.preprocess_narration(narration)
            
            if not clean_narration:
                return None, 0
            
            narration_embedding = self.model.encode([clean_narration], convert_to_tensor=True)
            
            cosine_scores = util.cos_sim(narration_embedding, self.ledger_embeddings)[0]
            
            best_score, best_idx = torch.max(cosine_scores, dim=0)
            best_score = best_score.item()
            
            if best_score >= threshold:
                return self.ledger_master[best_idx], best_score * 100
            else:
                return None, best_score * 100
                
        except Exception as e:
            print(f"Semantic matching error: {e}")
            return None, 0
    
    def keyword_based_match(self, narration, ledger_master):
        """Enhanced keyword-based matching with focus on names"""
        if not narration or not ledger_master:
            return None, 0
        
        narration_str = str(narration).upper()
        clean_narration = self.preprocess_narration(narration_str)
        extracted_name, is_person_transaction = self.identify_person_or_company_name(narration)
        category = self.categorize_transaction(narration)
        
        # Strategy 1: Direct name matching (HIGHEST PRIORITY)
        if extracted_name and is_person_transaction:
            for ledger in ledger_master:
                clean_ledger = self.preprocess_narration(ledger)
                # Check if extracted name matches ledger name
                name_similarity = self.calculate_string_similarity(extracted_name, clean_ledger)
                if name_similarity > 0.6:  # Good name match
                    return ledger, min(95, name_similarity * 100)
                
                # Check for substring match
                if extracted_name in clean_ledger or clean_ledger in extracted_name:
                    return ledger, 90
        
        # Strategy 2: Category-based matching
        category_keywords = {
            'salary': ['salary', 'employee', 'payroll', 'staff'],
            'food': ['food', 'meal', 'restaurant', 'cafe', 'dining'],
            'travel': ['travel', 'transport', 'taxi', 'uber', 'fuel', 'conveyance'],
            'shopping': ['shopping', 'store', 'market', 'purchase', 'supplies'],
            'utilities': ['electricity', 'water', 'gas', 'utility', 'bill', 'telephone'],
            'entertainment': ['entertainment', 'movie', 'cinema', 'recreation'],
            'healthcare': ['medical', 'hospital', 'clinic', 'health', 'medicine'],
            'education': ['education', 'school', 'college', 'tuition', 'books'],
            'vendor': ['vendor', 'supplier', 'contractor', 'service'],
            'client': ['client', 'customer', 'debtor'],
            'income': ['salary', 'income', 'revenue', 'commission', 'interest']
        }
        
        if category in category_keywords:
            for keyword in category_keywords[category]:
                for ledger in ledger_master:
                    if keyword in ledger.lower():
                        return ledger, 80
        
        # Strategy 3: Direct substring match
        for ledger in ledger_master:
            clean_ledger = self.preprocess_narration(ledger)
            if clean_ledger and clean_ledger in clean_narration:
                return ledger, 85
        
        # Strategy 4: Word overlap matching
        narration_words = set(clean_narration.split())
        best_overlap = 0
        best_ledger = None
        
        for ledger in ledger_master:
            clean_ledger = self.preprocess_narration(ledger)
            if not clean_ledger:
                continue
                
            ledger_words = set(clean_ledger.split())
            overlap = narration_words.intersection(ledger_words)
            
            if overlap and len(overlap) > best_overlap:
                best_overlap = len(overlap)
                best_ledger = ledger
        
        if best_ledger and best_overlap >= 1:
            confidence = min(75, best_overlap * 30)
            return best_ledger, confidence
        
        # Strategy 5: Fuzzy matching
        close_matches = difflib.get_close_matches(clean_narration, ledger_master, n=1, cutoff=0.5)
        if close_matches:
            return close_matches[0], 65
        
        return None, 0

    def multi_strategy_match(self, narration, ledger_master, rules_config, suspense_ledger, learned_mappings):
        """Comprehensive multi-strategy matching with focus on names"""
        narration_str = str(narration)
        extracted_name, is_person_transaction = self.identify_person_or_company_name(narration)
        
        # Strategy 1: Exact learned mapping
        if narration_str in learned_mappings:
            return learned_mappings[narration_str]['ledger'], 95, "learned_exact"
            
        # Strategy 2: Smart rules
        for rule in rules_config:
            keyword = rule.get('Narration Keyword', '').lower()
            if keyword and keyword in narration_str.lower():
                return rule.get('Mapped Ledger'), 90, "rule"
        
        # Strategy 3: Similar learned mappings with enhanced similarity
        best_learned_score = 0
        best_learned_ledger = None
        
        for learned_narration, learned_data in learned_mappings.items():
            similarity = self.calculate_string_similarity(narration_str, learned_narration)
            boosted_score = similarity * 100 + (learned_data.get('count', 1) * 2) + (learned_data.get('score', 0) * 0.1)
            
            if boosted_score > best_learned_score and boosted_score >= 60:
                best_learned_score = boosted_score
                best_learned_ledger = learned_data['ledger']
        
        if best_learned_ledger:
            return best_learned_ledger, min(85, best_learned_score), "learned_similar"

        # Strategy 4: Enhanced keyword matching with name focus
        keyword_match, keyword_score = self.keyword_based_match(narration_str, ledger_master)
        if keyword_match and keyword_score >= 50:
            return keyword_match, keyword_score, "keyword_match"

        # Strategy 5: Match based on ledger-name keywords and overlaps
        ledger_focus_match, ledger_focus_score = self.ledger_name_focus_match(narration_str, ledger_master)
        if ledger_focus_match and ledger_focus_score >= 55:
            return ledger_focus_match, ledger_focus_score, "ledger_name_focus"

        # Strategy 6: Semantic AI matching
        if self.initialized:
            semantic_match, semantic_score = self.semantic_similarity_match(narration_str, threshold=0.3)
            if semantic_match and semantic_score >= 35:
                return semantic_match, semantic_score, "semantic_ai"

        # Strategy 7: Category-based fallback with name suggestion
        category = self.categorize_transaction(narration_str)
        category_ledgers = {
            'salary': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['salary', 'employee', 'staff'])],
            'food': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['food', 'meal', 'restaurant'])],
            'travel': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['travel', 'transport', 'fuel', 'conveyance'])],
            'shopping': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['purchase', 'expense', 'general', 'supplies'])],
            'utilities': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['electricity', 'water', 'utility', 'telephone'])],
            'vendor': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['vendor', 'supplier', 'contractor'])],
            'client': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['client', 'customer', 'debtor'])],
            'income': [ledger for ledger in ledger_master if any(word in ledger.lower() for word in ['salary', 'income', 'revenue'])]
        }
        
        if category in category_ledgers and category_ledgers[category]:
            return category_ledgers[category][0], 60, f"category_{category}"

        # Final fallback: If we extracted a name but couldn't match, create a suggestion
        if extracted_name and is_person_transaction:
            # Look for any ledger that might be related to the extracted name
            for ledger in ledger_master:
                if extracted_name.lower() in ledger.lower():
                    return ledger, 55, "name_fallback"

        # Ultimate fallback
        return suspense_ledger, 0, "default"

# Global instance of the enhanced mapper
ledger_mapper = EnhancedLedgerMapper()

def initialize_ai_model():
    """Initialize the AI model on app start"""
    if not ledger_mapper.initialized:
        return ledger_mapper.initialize_model()
    return ledger_mapper.initialized

def get_smart_suggestions(narrations_list, ledger_master, rules_config, suspense_ledger, learned_mappings):
    """
    Enhanced smart suggestions with focus on names at end of narration
    """
    best_matches = {}
    confidence_scores = {}
    match_types = {}
    
    initialize_ai_model()
    
    if ledger_mapper.initialized and (ledger_mapper.ledger_master != ledger_master or ledger_mapper.ledger_embeddings is None):
        ledger_mapper.compute_ledger_embeddings(ledger_master)
    
    # Filter out NaN values before processing to avoid dictionary key issues
    # (NaN != NaN in Python, so each NaN creates a separate key)
    valid_narrations = [n for n in narrations_list if pd.notna(n)]

    for narration in valid_narrations:
        narration_str = str(narration)

        # Use the comprehensive multi-strategy matching with name focus
        suggested_ledger, confidence, match_type = ledger_mapper.multi_strategy_match(
            narration_str, ledger_master, rules_config, suspense_ledger, learned_mappings
        )

        # Use string representation as key to ensure consistency
        best_matches[narration_str] = suggested_ledger
        confidence_scores[narration_str] = confidence
        match_types[narration_str] = match_type

    # Add a special handling for NaN values if they exist in the original list
    if len(valid_narrations) < len(narrations_list):
        # Use a special key for NaN values
        best_matches["__NaN__"] = suspense_ledger
        confidence_scores["__NaN__"] = 0
        match_types["__NaN__"] = "default"
            
    return best_matches, confidence_scores, match_types

def update_learned_mappings(email, narration, mapped_ledger, similarity_score=0):
    """Update learned mappings with enhanced scoring - automatically called when user maps ledgers"""
    conn = get_db_conn()
    with conn.session as s:
        try:
            existing = s.execute(text(
                'SELECT usage_count FROM user_learned_mappings WHERE email = :email AND narration_text = :narration'
            ), params=dict(email=email, narration=narration)).fetchone()

            # Initialize variables to avoid NameError
            base_score = max(similarity_score, 80)
            new_score = base_score

            if existing:
                new_count = existing[0] + 1
                # Enhanced scoring: combine similarity with usage count
                new_score = max(similarity_score, 75) + (new_count * 2)
                s.execute(text('''
                    UPDATE user_learned_mappings
                    SET usage_count = :count, similarity_score = :score, last_used = DATE('now')
                    WHERE email = :email AND narration_text = :narration
                '''), params=dict(email=email, narration=narration, count=new_count, score=min(new_score, 95)))
            else:
                s.execute(text('''
                    INSERT INTO user_learned_mappings (email, narration_text, mapped_ledger, similarity_score, usage_count)
                    VALUES (:email, :narration, :ledger, :score, 1)
                '''), params=dict(email=email, narration=narration, ledger=mapped_ledger, score=base_score))

            s.commit()

            # Update session state
            if narration not in st.session_state.learned_mappings:
                st.session_state.learned_mappings[narration] = {'ledger': mapped_ledger, 'score': base_score, 'count': 1}
            else:
                st.session_state.learned_mappings[narration]['count'] += 1
                st.session_state.learned_mappings[narration]['score'] = min(new_score, 95) if existing else base_score
                
        except Exception as e:
            print(f"Error updating learned mappings: {e}")

# --- AUTO MAPPING FUNCTIONS ---

def auto_map_ledgers_based_on_rules(narrations_list, ledger_master, rules_config, suspense_ledger, learned_mappings):
    """
    Automatically map ledgers based on smart rules and learned mappings
    Returns dictionary of {narration: mapped_ledger}
    """
    auto_mappings = {}

    # Filter out NaN values before processing to avoid dictionary key issues
    valid_narrations = [n for n in narrations_list if pd.notna(n)]

    for narration in valid_narrations:
        narration_str = str(narration)
        
        # Strategy 1: Exact learned mapping (highest priority)
        if narration_str in learned_mappings:
            auto_mappings[narration_str] = learned_mappings[narration_str]['ledger']
            continue
            
        # Strategy 2: Smart rules matching
        matched_by_rule = False
        for rule in rules_config:
            keyword = rule.get('Narration Keyword', '').lower()
            if keyword and keyword in narration_str.lower():
                auto_mappings[narration_str] = rule.get('Mapped Ledger')
                matched_by_rule = True
                break
        
        if matched_by_rule:
            continue
            
        # Strategy 3: Similar learned mappings
        best_similarity = 0
        best_learned_ledger = None
        
        for learned_narration, learned_data in learned_mappings.items():
            similarity = ledger_mapper.calculate_string_similarity(narration_str, learned_narration)
            if similarity > best_similarity and similarity >= 0.7:  # 70% similarity threshold
                best_similarity = similarity
                best_learned_ledger = learned_data['ledger']
        
        if best_learned_ledger:
            auto_mappings[narration_str] = best_learned_ledger
            continue
            
        # Strategy 4: Default to suspense ledger
        auto_mappings[narration_str] = suspense_ledger
    
    return auto_mappings

# --- 5. TALLY XML GENERATION FUNCTIONS ---

def create_tally_xml(df, fixed_ledger_config, dynamic_ledger_config, company_name, voucher_type, journal_mappings):
    xml_template = """<ENVELOPE>
 <HEADER>
  <TALLYREQUEST>Import Data</TALLYREQUEST>
 </HEADER>
 <BODY>
  <IMPORTDATA>
   <REQUESTDESC>
    <REPORTNAME>Vouchers</REPORTNAME>
    <STATICVARIABLES>
     <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
    </STATICVARIABLES>
   </REQUESTDESC>
   <REQUESTDATA>
{tally_messages}
   </REQUESTDATA>
  </IMPORTDATA>
 </BODY>
</ENVELOPE>"""
    tally_message_template = """
    <TALLYMESSAGE xmlns:UDF="TallyUDF">
     <VOUCHER VCHTYPE="{voucher_type}" ACTION="Create">
      <DATE>{date}</DATE>
      <VOUCHERTYPENAME>{voucher_type}</VOUCHERTYPENAME>
      <VOUCHERNUMBER>{voucher_number}</VOUCHERNUMBER>
      <NARRATION>{narration}</NARRATION>
      <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
      {ledger_entries}
     </VOUCHER>
    </TALLYMESSAGE>"""
    ledger_line_template = """
      <ALLLEDGERENTRIES.LIST>
       <LEDGERNAME>{ledger_name}</LEDGERNAME>
       <ISDEEMEDPOSITIVE>{is_positive}</ISDEEMEDPOSITIVE>
       <AMOUNT>{amount}</AMOUNT>
      </ALLLEDGERENTRIES.LIST>"""
    all_tally_messages = []
    
    mapping_dicts = {}
    for col_name, mapping_df in journal_mappings.items():
        mapping_dicts[col_name] = pd.Series(mapping_df['Mapped Ledger'].values, index=mapping_df['CSV Value']).to_dict()

    for index, row in df.iterrows():
        try:
            date_obj = pd.to_datetime(row['Date'], dayfirst=True)
            tally_date = date_obj.strftime('%Y%m%d')
            # Store tuples of (xml_string, transaction_type) for sorting
            ledger_entries_list = []

            # Handle voucher number - replace NaN with empty string
            voucher_number = str(row['Voucher Number']) if pd.notna(row['Voucher Number']) else ""

            for ledger in fixed_ledger_config:
                if ledger['CSV Column Name'] in row and pd.notna(row[ledger['CSV Column Name']]):
                    amount_val = round(float(row[ledger['CSV Column Name']]), 2)
                    if amount_val == 0: continue
                    is_positive_flag = "No" if ledger['Type (Debit/Credit)'] == 'Credit' else "Yes"
                    amount_for_xml = amount_val if ledger['Type (Debit/Credit)'] == 'Credit' else amount_val * -1
                    # XML escape ledger name
                    ledger_name_safe = escape(str(ledger['Tally Ledger Name']))
                    ledger_xml = ledger_line_template.format(
                        ledger_name=ledger_name_safe,
                        is_positive=is_positive_flag,
                        amount=amount_for_xml
                    )
                    # Store as tuple (xml, type) for sorting
                    ledger_entries_list.append((ledger_xml, ledger['Type (Debit/Credit)']))

            for dyn_ledger in dynamic_ledger_config:
                name_col = dyn_ledger['CSV Column for Ledger Name']
                amount_col = dyn_ledger['CSV Column for Amount']
                trans_type = dyn_ledger['Transaction Type']

                # Check if columns exist in the row
                if name_col not in row.index or amount_col not in row.index:
                    continue

                csv_value_as_ledger = row[name_col]

                # Skip if amount column has NaN or invalid value
                if pd.isna(row[amount_col]):
                    continue

                amount_from_col = round(float(row[amount_col]), 2)

                if pd.notna(csv_value_as_ledger) and str(csv_value_as_ledger).strip() != "" and amount_from_col != 0:

                    current_map = mapping_dicts.get(name_col, {})
                    # Convert to string to ensure hashable type for dictionary lookup
                    csv_value_str = str(csv_value_as_ledger)
                    final_ledger_name = current_map.get(csv_value_str, csv_value_str)

                    is_positive_flag = "No" if trans_type == 'Credit' else "Yes"
                    amount_for_xml = amount_from_col if trans_type == 'Credit' else amount_from_col * -1

                    # XML escape ledger name
                    ledger_name_safe = escape(str(final_ledger_name))

                    ledger_xml = ledger_line_template.format(
                        ledger_name=ledger_name_safe,
                        is_positive=is_positive_flag,
                        amount=amount_for_xml
                    )
                    # Store as tuple (xml, type) for sorting
                    ledger_entries_list.append((ledger_xml, trans_type))

            if ledger_entries_list:
                # Sort entries: Debit first (priority 0), Credit second (priority 1)
                ledger_entries_list.sort(key=lambda x: 0 if x[1] == 'Debit' else 1)
                # Extract only the XML strings
                sorted_ledger_xmls = [entry[0] for entry in ledger_entries_list]
                final_ledger_entries = "\n".join(sorted_ledger_xmls)
                # Safely get narration with proper type checking and XML escaping
                narration_raw = row.get('Narration', 'N/A')
                narration_safe = escape(str(narration_raw)) if pd.notna(narration_raw) else "N/A"

                all_tally_messages.append(tally_message_template.format(
                    voucher_type=voucher_type,
                    date=tally_date,
                    voucher_number=voucher_number,
                    narration=narration_safe,
                    ledger_entries=final_ledger_entries
                ))
        except Exception as e:
            st.error(f"Error processing row {index} ('{row.get('Narration', 'N/A')}'): {e}. Skipping row.")

    # XML escape company name before inserting into template
    company_name_safe = escape(str(company_name))

    return xml_template.format(
        company_name=company_name_safe,
        tally_messages="\n".join(all_tally_messages)
    )

def get_template_csv(fixed_ledger_config, dynamic_ledger_config):
    headers = ["Date", "Voucher Number", "Narration"]
    example_data = ["01-04-2024", "SJV-1", "Salary for April 2024"]
    for i, ledger in enumerate(fixed_ledger_config):
        headers.append(ledger['CSV Column Name'])
        example_data.append(str(1000 * (i+1)))
    for i, dyn_ledger in enumerate(dynamic_ledger_config):
        headers.append(dyn_ledger['CSV Column for Ledger Name'])
        example_data.append(f"Dynamic Ledger {i+1} Name")
        headers.append(dyn_ledger['CSV Column for Amount'])
        example_data.append(str(5000 * (i+1)))
    csv_headers = ",".join(headers) + "\n"
    csv_example = ",".join(example_data) + "\n"
    return csv_headers + csv_example

def get_bank_template_csv():
    """Generates the CSV template for bank statements."""
    headers = "Date,Narration,Debit,Credit\n"
    example_data = "01-04-2024,Rent Paid to Landlord,50000,0\n"
    example_data += "02-04-2024,Cash Deposit,0,100000\n"
    example_data += "05-04-2024,Amazon Office Supplies,15000,0\n"
    return headers + example_data

def create_bank_tally_xml(df, bank_ledger, company_name):
    """
    Generates Tally XML from a bank statement.
    Assumes the DataFrame *already* has a 'Mapped Ledger' column.
    """
    xml_template = """<ENVELOPE>
 <HEADER>
  <TALLYREQUEST>Import Data</TALLYREQUEST>
 </HEADER>
 <BODY>
  <IMPORTDATA>
   <REQUESTDESC>
    <REPORTNAME>Vouchers</REPORTNAME>
    <STATICVARIABLES>
     <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
    </STATICVARIABLES>
   </REQUESTDESC>
   <REQUESTDATA>
{tally_messages}
   </REQUESTDATA>
  </IMPORTDATA>
 </BODY>
</ENVELOPE>"""
    voucher_template = """
    <TALLYMESSAGE xmlns:UDF="TallyUDF">
     <VOUCHER VCHTYPE="{voucher_type}" ACTION="Create">
      <DATE>{date}</DATE>
      <VOUCHERTYPENAME>{voucher_type}</VOUCHERTYPENAME>
      <NARRATION>{narration}</NARRATION>
      <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
      {ledger_entries}
     </VOUCHER>
    </TALLYMESSAGE>"""

    ledger_entry_template = """
      <ALLLEDGERENTRIES.LIST>
       <LEDGERNAME>{ledger_name}</LEDGERNAME>
       <ISDEEMEDPOSITIVE>{is_positive}</ISDEEMEDPOSITIVE>
       <AMOUNT>{amount}</AMOUNT>
      </ALLLEDGERENTRIES.LIST>"""
    all_tally_messages = []
    for index, row in df.iterrows():
        narration = "N/A"  # Initialize before try block to avoid NameError in exception handler
        try:
            date_obj = pd.to_datetime(row['Date'], dayfirst=True)
            tally_date = date_obj.strftime('%Y%m%d')
            narration = str(row['Narration'])
            debit = round(float(row['Debit']), 2)
            credit = round(float(row['Credit']), 2)

            mapped_ledger = row['Mapped Ledger']

            if debit > 0:
                voucher_type = "Payment"
                bank_amount = debit
                contra_amount = debit * -1
                is_bank_positive = "No"
                is_contra_positive = "Yes"
            elif credit > 0:
                voucher_type = "Receipt"
                bank_amount = credit * -1
                contra_amount = credit
                is_bank_positive = "Yes"
                is_contra_positive = "No"
            else:
                continue
            # XML escape narration and ledger names
            narration_safe = escape(str(narration)) if pd.notna(narration) else "N/A"
            bank_ledger_safe = escape(str(bank_ledger))
            mapped_ledger_safe = escape(str(mapped_ledger))

            # Create ledger entries list with tuples (xml, is_debit_flag)
            ledger_list = []

            # Bank ledger entry
            bank_entry_xml = ledger_entry_template.format(
                ledger_name=bank_ledger_safe,
                is_positive=is_bank_positive,
                amount=bank_amount
            )
            # is_bank_positive="Yes" means debit
            ledger_list.append((bank_entry_xml, is_bank_positive == "Yes"))

            # Contra ledger entry
            contra_entry_xml = ledger_entry_template.format(
                ledger_name=mapped_ledger_safe,
                is_positive=is_contra_positive,
                amount=contra_amount
            )
            # is_contra_positive="Yes" means debit
            ledger_list.append((contra_entry_xml, is_contra_positive == "Yes"))

            # Sort: Debit entries (True) first, Credit entries (False) second
            ledger_list.sort(key=lambda x: not x[1])  # not x[1] puts True before False

            # Extract sorted XML strings
            sorted_ledger_entries = "\n".join([entry[0] for entry in ledger_list])

            all_tally_messages.append(
                voucher_template.format(
                    voucher_type=voucher_type,
                    date=tally_date,
                    narration=narration_safe,
                    ledger_entries=sorted_ledger_entries
                )
            )
        except Exception as e:
            st.error(f"Error processing row {index} ('{narration}'): {e}. Skipping row.")

    # XML escape company name before inserting into template
    company_name_safe = escape(str(company_name))

    return xml_template.format(
        company_name=company_name_safe,
        tally_messages="\n".join(all_tally_messages)
    )

def sync_ledgers_from_tally(host, port, company_name, email):
    """
    Fetches ledger list from Tally and stores in database.
    Returns tuple (success: bool, message: str, ledger_count: int)
    """
    try:
        # Construct Tally XML request to get all ledgers
        tally_request = f'''
        <ENVELOPE>
            <HEADER>
                <VERSION>1</VERSION>
                <TALLYREQUEST>Export</TALLYREQUEST>
                <TYPE>Collection</TYPE>
                <ID>List of Ledgers</ID>
            </HEADER>
            <BODY>
                <DESC>
                    <STATICVARIABLES>
                        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                        <SVCURRENTCOMPANY>{escape(company_name)}</SVCURRENTCOMPANY>
                    </STATICVARIABLES>
                    <TDL>
                        <TDLMESSAGE>
                            <COLLECTION NAME="MyLedgers" ISMODIFY="No" ISFIXED="No">
                                <TYPE>Ledger</TYPE>
                                <FETCH>Name, Parent</FETCH>
                            </COLLECTION>
                        </TDLMESSAGE>
                    </TDL>
                </DESC>
            </BODY>
        </ENVELOPE>
        '''

        # Send request to Tally
        url = f"http://{host}:{port}"
        headers = {'Content-Type': 'text/xml'}

        response = requests.post(url, data=tally_request, headers=headers, timeout=10)

        if response.status_code != 200:
            return False, f"Tally server returned error: {response.status_code}", 0

        # Parse XML response
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            return False, f"Failed to parse Tally response: {str(e)}", 0

        # Extract ledgers from response
        ledgers = []

        # Look for LEDGER elements in the response
        for ledger_elem in root.findall('.//LEDGER'):
            name_elem = ledger_elem.find('.//NAME')
            parent_elem = ledger_elem.find('.//PARENT')

            if name_elem is not None and name_elem.text:
                ledger_name = name_elem.text.strip()
                ledger_group = parent_elem.text.strip() if parent_elem is not None and parent_elem.text else "Unknown"
                ledgers.append((ledger_name, ledger_group))

        if not ledgers:
            return False, "No ledgers found in Tally response. Please check company name and Tally configuration.", 0

        # Store ledgers in database
        conn = get_db_conn()
        with conn.session as s:
            # Clear existing ledgers for this user
            s.execute(text('DELETE FROM tally_synced_ledgers WHERE email = :email'),
                     params={'email': email})

            # Insert new ledgers
            for ledger_name, ledger_group in ledgers:
                s.execute(text('''
                    INSERT OR REPLACE INTO tally_synced_ledgers (email, ledger_name, ledger_group)
                    VALUES (:email, :ledger_name, :ledger_group)
                '''), params={
                    'email': email,
                    'ledger_name': ledger_name,
                    'ledger_group': ledger_group
                })

            # Update last sync date
            s.execute(text('''
                UPDATE tally_connection_settings
                SET last_sync_date = :sync_date
                WHERE email = :email
            '''), params={
                'email': email,
                'sync_date': datetime.now()
            })

            s.commit()

        return True, f"Successfully synced {len(ledgers)} ledgers from Tally", len(ledgers)

    except requests.exceptions.ConnectionError:
        return False, f"Could not connect to Tally server at {host}:{port}. Please ensure Tally is running with web server enabled.", 0
    except requests.exceptions.Timeout:
        return False, "Connection to Tally server timed out. Please try again.", 0
    except Exception as e:
        return False, f"Error syncing ledgers: {str(e)}", 0

def push_vouchers_to_tally(xml_data, host, port):
    """
    Pushes vouchers directly to Tally server via HTTP POST.
    Returns tuple (success: bool, message: str, voucher_count: int)
    """
    try:
        # Send XML data to Tally server
        url = f"http://{host}:{port}"
        headers = {'Content-Type': 'text/xml'}

        response = requests.post(url, data=xml_data, headers=headers, timeout=30)

        if response.status_code != 200:
            return False, f"Tally server returned error: {response.status_code}", 0

        # Count how many vouchers we attempted to send
        vouchers_sent = xml_data.count('<TALLYMESSAGE')

        # Parse response to check for errors and actual success
        try:
            root = ET.fromstring(response.text)

            # Log the response for debugging (to console/logs)
            st.write("### 🔍 Tally Response Debug Info")
            st.text(response.text[:2000])  # Show first 2000 chars of response

            # Check for general ERROR element
            error_elem = root.find('.//ERROR')
            if error_elem is not None and error_elem.text and error_elem.text.strip():
                return False, f"Tally import error: {error_elem.text}", 0

            # Check for LINEERROR elements (per-voucher errors)
            line_errors = root.findall('.//LINEERROR')
            if line_errors:
                error_details = []
                for idx, err in enumerate(line_errors[:5], 1):  # Show first 5 errors
                    error_details.append(f"  {idx}. {err.text}")
                error_msg = "Tally rejected vouchers with errors:\n" + "\n".join(error_details)
                if len(line_errors) > 5:
                    error_msg += f"\n  ... and {len(line_errors) - 5} more errors"
                return False, error_msg, 0

            # Check for CREATED count in response (Tally's confirmation)
            created_elem = root.find('.//CREATED')
            if created_elem is not None and created_elem.text:
                try:
                    created_count = int(created_elem.text)
                    if created_count == 0:
                        return False, "Tally accepted the request but created 0 vouchers. Please check:\n- Company name is correct\n- All ledger names exist in Tally\n- Voucher numbers are not duplicates", 0
                    elif created_count < vouchers_sent:
                        return False, f"⚠️ Partial success: {created_count} out of {vouchers_sent} vouchers created. Some vouchers may have validation errors.", created_count
                    else:
                        return True, f"✅ Successfully created {created_count} vouchers in Tally", created_count
                except ValueError:
                    pass

            # Check for LASTVCHID (indicates successful voucher creation)
            last_vch_id = root.find('.//LASTVCHID')
            if last_vch_id is not None and last_vch_id.text:
                return True, f"Successfully pushed {vouchers_sent} vouchers to Tally (Last Voucher ID: {last_vch_id.text})", vouchers_sent

            # If response has IMPORTRESULT with status
            import_result = root.find('.//IMPORTRESULT')
            if import_result is not None:
                status = import_result.find('.//STATUS')
                if status is not None and status.text:
                    if status.text.upper() == 'SUCCESS':
                        return True, f"Successfully pushed {vouchers_sent} vouchers to Tally", vouchers_sent
                    else:
                        return False, f"Tally import status: {status.text}", 0

            # If we got HTTP 200 but can't find success indicators, this is suspicious
            return False, f"⚠️ Uncertain result: Tally returned HTTP 200 but no confirmation of voucher creation. Response may not contain expected elements. Please check Tally manually.", 0

        except ET.ParseError as parse_err:
            # If we can't parse the response, show it to user for debugging
            return False, f"Could not parse Tally response. Raw response:\n{response.text[:500]}\n\nParse error: {str(parse_err)}", 0

    except requests.exceptions.ConnectionError:
        return False, f"Could not connect to Tally server at {host}:{port}. Please ensure Tally is running with web server enabled.", 0
    except requests.exceptions.Timeout:
        return False, "Connection to Tally server timed out. Please try again.", 0
    except Exception as e:
        return False, f"Error pushing vouchers to Tally: {str(e)}", 0

def fetch_companies_from_tally(host, port):
    """
    Fetches list of company names from Tally server.
    Returns tuple (success: bool, message: str, companies: list)
    """
    try:
        # Construct Tally XML request to get all companies
        tally_request = '''
        <ENVELOPE>
            <HEADER>
                <VERSION>1</VERSION>
                <TALLYREQUEST>Export</TALLYREQUEST>
                <TYPE>Data</TYPE>
                <ID>ListOfCompanies</ID>
            </HEADER>
            <BODY>
                <DESC>
                    <STATICVARIABLES>
                        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    </STATICVARIABLES>
                    <TDL>
                        <TDLMESSAGE>
                            <REPORT NAME="ListOfCompanies">
                                <FORMS>List</FORMS>
                                <FORM>List</FORM>
                            </REPORT>
                            <FORM NAME="List">
                                <TOPPARTS>List</TOPPARTS>
                                <PART>List</PART>
                            </FORM>
                            <PART NAME="List">
                                <TOPLINES>CompanyList</TOPLINES>
                                <LINE>CompanyList</LINE>
                                <REPEAT>CompanyList : Company</REPEAT>
                                <SCROLLED>Vertical</SCROLLED>
                            </PART>
                            <LINE NAME="CompanyList">
                                <FIELD>CompanyName</FIELD>
                            </LINE>
                            <FIELD NAME="CompanyName">
                                <SET>$Name</SET>
                            </FIELD>
                            <COLLECTION NAME="Company">
                                <TYPE>Company</TYPE>
                            </COLLECTION>
                        </TDLMESSAGE>
                    </TDL>
                </DESC>
            </BODY>
        </ENVELOPE>
        '''

        # Send request to Tally
        url = f"http://{host}:{port}"
        headers = {'Content-Type': 'text/xml'}

        response = requests.post(url, data=tally_request, headers=headers, timeout=10)

        if response.status_code != 200:
            return False, f"Tally server returned error: {response.status_code}", []

        # Parse XML response to extract company names
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            return False, f"Failed to parse Tally response: {str(e)}", []

        # Extract company names from response
        companies = []

        # Try multiple possible XML paths for company names
        for company_elem in root.findall('.//COMPANYNAME'):
            if company_elem.text:
                companies.append(company_elem.text.strip())

        # Alternative path - check for NAME elements under COMPANY
        if not companies:
            for company_elem in root.findall('.//COMPANY'):
                name_elem = company_elem.find('.//NAME')
                if name_elem is not None and name_elem.text:
                    companies.append(name_elem.text.strip())

        # Another alternative - direct NAME elements
        if not companies:
            for name_elem in root.findall('.//NAME'):
                if name_elem.text and name_elem.text.strip():
                    companies.append(name_elem.text.strip())

        # Remove duplicates while preserving order
        companies = list(dict.fromkeys(companies))

        if not companies:
            return False, "No companies found on Tally server. Please ensure Tally is running and companies are loaded.", []

        return True, f"Successfully detected {len(companies)} company(ies) from Tally", companies

    except requests.exceptions.ConnectionError:
        return False, f"Could not connect to Tally server at {host}:{port}. Please ensure Tally is running with web server enabled.", []
    except requests.exceptions.Timeout:
        return False, "Connection to Tally server timed out. Please try again.", []
    except Exception as e:
        return False, f"Error fetching companies: {str(e)}", []

def get_synced_ledgers(email):
    """Retrieves synced ledgers from database for the given user."""
    conn = get_db_conn()
    with conn.session as s:
        result = s.execute(text('''
            SELECT ledger_name, ledger_group, sync_date
            FROM tally_synced_ledgers
            WHERE email = :email
            ORDER BY ledger_name
        '''), params={'email': email})
        return result.fetchall()

# --- 6. Page Configuration ---
st.set_page_config(
    page_title="Xml2Tally - Financial Automation Platform",
    layout="wide",  # Changed to "wide" for more space
    initial_sidebar_state="expanded"  # Changed to "expanded" - THIS IS THE KEY CHANGE
)

load_css()

# --- 7. Session State Initialization ---
if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False
if "current_view" not in st.session_state: 
    st.session_state.current_view = "main" 
if "email" not in st.session_state: 
    st.session_state.email = "default"
if "settings_loaded" not in st.session_state: 
    st.session_state.settings_loaded = False 
if "company_name" not in st.session_state:
    st.session_state.company_name = 'Xml2Tally (Default Co.)'
if "journal_templates" not in st.session_state:
    st.session_state.journal_templates = {}
if "ledger_master" not in st.session_state:
    st.session_state.ledger_master = ["Bank Suspense A/c (Default)"]
if "bank_rules" not in st.session_state:
    st.session_state.bank_rules = []
if "default_suspense_ledger" not in st.session_state:
    st.session_state.default_suspense_ledger = "Bank Suspense A/c (Default)"
if "journal_mappings" not in st.session_state:
    st.session_state.journal_mappings = {}
if "learned_mappings" not in st.session_state:
    st.session_state.learned_mappings = {}
if "ai_initialized" not in st.session_state:
    st.session_state.ai_initialized = False
if "tally_server_host" not in st.session_state:
    st.session_state.tally_server_host = "localhost"
if "tally_server_port" not in st.session_state:
    st.session_state.tally_server_port = 9000
if "tally_company_name" not in st.session_state:
    st.session_state.tally_company_name = ""
if "detected_companies" not in st.session_state:
    st.session_state.detected_companies = []
if "enable_direct_sync" not in st.session_state:
    st.session_state.enable_direct_sync = False
if "enable_direct_push_bank" not in st.session_state:
    st.session_state.enable_direct_push_bank = False
if "enable_direct_push_journal" not in st.session_state:
    st.session_state.enable_direct_push_journal = False
if "sync_ledgers_on_load" not in st.session_state:
    st.session_state.sync_ledgers_on_load = False
if "tally_simple_mode" not in st.session_state:
    st.session_state.tally_simple_mode = True
if "tally_simple_profile" not in st.session_state:
    st.session_state.tally_simple_profile = "Download XML files only"

# --- 8. ENHANCED PAGE RENDERING FUNCTIONS FOR FINANCIAL AUTOMATION ---

def render_login_page():
    """Simple login page"""
    st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <div class="login-title">Welcome Back</div>
                <div class="login-subtitle">Sign in to your Financial Automation Platform</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("Login to Your Account")
            
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button("Sign In", use_container_width=True)
            with col2:
                if st.form_submit_button("Create Account", use_container_width=True, type="secondary"):
                    st.session_state.current_view = "signup"
                    st.rerun()
            
            if login_button:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    status = check_user_status(email, password)
                    if status == "INVALID":
                        st.error("Invalid email or password")
                    elif status == "PENDING":
                        st.error("Your trial has expired. Please subscribe to continue.")
                    else:
                        # Clear previous user data and load new user data
                        st.session_state.logged_in = True
                        st.session_state.email = email
                        st.session_state.current_view = "dashboard"
                        st.session_state.settings_loaded = False
                        st.success("Login successful!")
                        st.rerun()
        
        st.markdown("---")

def render_signup_page():
    """Simple signup page"""
    st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <div class="login-title">Create Account</div>
                <div class="login-subtitle">Start your 30-day free trial with full features</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("signup_form"):
            st.subheader("Create Your Account")
            
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email Address", placeholder="Enter your email")
            phone = st.text_input("Phone Number", placeholder="Enter your phone number")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            # Terms agreement
            col1, col2 = st.columns([1, 4])
            with col1:
                agree_terms = st.checkbox("", value=False)
            with col2:
                st.markdown("I agree to the [Terms & Conditions](#) and [Privacy Policy](#)")
            
            col1, col2 = st.columns(2)
            with col1:
                signup_button = st.form_submit_button("Start Free Trial", use_container_width=True, type="primary")
            with col2:
                if st.form_submit_button("← Back to Login", use_container_width=True, type="secondary"):
                    st.session_state.current_view = "login"
                    st.rerun()
            
            if signup_button:
                if not all([name, email, phone, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif not agree_terms:
                    st.error("Please agree to the Terms & Conditions")
                else:
                    # Check if user already exists
                    conn = get_db_conn()
                    with conn.session as s:
                        existing_user = s.execute(text('SELECT email FROM users WHERE email = :email'),
                                               params=dict(email=email)).fetchone()

                    if existing_user:
                        st.error("An account with this email already exists")
                    else:
                        # Create new user
                        if add_user_to_db(email, name, phone, password):
                            st.success("Account created successfully! Starting your 30-day free trial...")

                            # Auto-login after successful signup
                            st.session_state.logged_in = True
                            st.session_state.email = email
                            st.session_state.current_view = "dashboard"
                            st.session_state.settings_loaded = False
                            st.rerun()
                        else:
                            st.error("Error creating account. Please try again.")
        
        st.markdown("---")
        
        # Benefits of signing up
        st.markdown("""
            <div style="text-align: center;">
                <h4>What's Included in Your Free Trial:</h4>
                <p>• Full access to all features<br>
                • 30 days of unlimited conversions<br>
                • AI-powered ledger mapping<br>
                • Premium support</p>
            </div>
        """, unsafe_allow_html=True)

def render_main_page():
    """Enhanced main page with financial automation dashboard"""

    # Header Section
    st.markdown("""
        <div class="dashboard-header">
            <div class="dashboard-title">Financial Automation Platform</div>
            <div class="dashboard-subtitle">Automate your Tally data entry with AI-powered accuracy</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom: 1.5rem;">
            <span class="status-indicator status-success">Bank & journal ready</span>
            <span class="status-indicator status-warning">Human review built-in</span>
            <span class="status-indicator status-success">Export-ready XML files</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Conversion Accuracy</div>
                <div class="metric-value">98.7%</div>
                <div class="metric-trend trend-up">Consistently improving</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Time Saved</div>
                <div class="metric-value">4h/day</div>
                <div class="metric-trend trend-up">Teams report 85% faster closes</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Active Workspaces</div>
                <div class="metric-value">1,247</div>
                <div class="metric-trend trend-up">Growing weekly</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Ledger Coverage</div>
                <div class="metric-value">99.2%</div>
                <div class="metric-trend trend-up">Mapping confidence</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Features Section
    st.markdown("## Core Financial Automation Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🏦</div>
                <div class="feature-title">Smart Bank Reconciliation</div>
                <div class="feature-description">
                    Automatically match bank transactions with Tally ledgers using advanced AI.
                    Reduce reconciliation time from hours to minutes with built-in exception cues.
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📑</div>
                <div class="feature-title">Journal Automation</div>
                <div class="feature-description">
                    Convert CSV/Excel journals to Tally XML with intelligent ledger mapping.
                    Perfect for payroll, invoices, and expense tracking with reusable templates.
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Streamlined Data Entry</div>
                <div class="feature-description">
                    Automated data processing with template management.
                    Eliminate manual entry errors and keep teams aligned with guided reviews.
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Guided experience
    st.markdown("## Your workspace at a glance")
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        st.markdown(
            """
            <div class="nav-card">
                <div class="nav-icon">🧭</div>
                <div class="nav-title">Guided Bank Workflows</div>
                <div class="nav-description">Upload statements, review AI matches, and finalize reconciliations with fewer clicks.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with exp_col2:
        st.markdown(
            """
            <div class="nav-card">
                <div class="nav-icon">🧾</div>
                <div class="nav-title">Bulk Journal Uploads</div>
                <div class="nav-description">Standardize monthly imports with saved templates and automated ledger suggestions.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # How It Works Section
    st.markdown("## How Financial Automation Works")

    st.markdown(
        """
        <div class="process-steps">
            <div class="process-step">
                <div class="step-number">1</div>
                <div class="step-title">Upload Your Data</div>
                <div class="step-description">CSV, Excel, or bank statements</div>
            </div>
            <div class="process-step">
                <div class="step-number">2</div>
                <div class="step-title">AI-Powered Mapping</div>
                <div class="step-description">Smart ledger matching</div>
            </div>
            <div class="process-step">
                <div class="step-number">3</div>
                <div class="step-title">Review & Adjust</div>
                <div class="step-description">Visual verification tools</div>
            </div>
            <div class="process-step">
                <div class="step-number">4</div>
                <div class="step-title">Export to Tally</div>
                <div class="step-description">Ready-to-import XML</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # CTA Section with Login/Signup
    st.markdown(
        """
        <div style="text-align: center; padding: 3rem 1rem;">
            <h2 style="color: #333; margin-bottom: 1rem;">Ready to transform your accounting workflow?</h2>
            <p style="color: #666; margin-bottom: 1.5rem; font-size: 1.05rem;">
                Start with guided flows or jump straight into conversions with your existing templates.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        auth_col1, auth_col2 = st.columns(2)
        with auth_col1:
            if st.button("Sign In", use_container_width=True, type="primary"):
                st.session_state.current_view = "login"
                st.rerun()
        with auth_col2:
            if st.button("Start Free Trial", use_container_width=True):
                st.session_state.current_view = "signup"
                st.rerun()

        st.markdown(
            """
            <div style="margin-top: 1.2rem; color: #4a5568; font-size: 0.95rem; text-align: center;">
                No setup required • Works with existing Tally ledgers • Support team on standby
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Footer
    st.markdown("---")
    render_policy_footer(centered=True)

def render_policy_footer(centered=False):
    if centered:
        c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
        with c2:
            if st.button("Privacy Policy", type="secondary", use_container_width=True):
                st.session_state.current_view = "privacy"
                st.rerun()
        with c3:
            if st.button("Terms & Conditions", type="secondary", use_container_width=True):
                st.session_state.current_view = "terms"
                st.rerun()
        with c4:
            if st.button("Refund Policy", type="secondary", use_container_width=True):
                st.session_state.current_view = "refund"
                st.rerun()
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Privacy Policy", use_container_width=True, type="secondary"):
                st.session_state.current_view = "privacy"
                st.rerun()
        with col2:
            if st.button("Terms & Conditions", use_container_width=True, type="secondary"):
                st.session_state.current_view = "terms"
                st.rerun()
        with col3:
            if st.button("Refund Policy", use_container_width=True, type="secondary"):
                st.session_state.current_view = "refund"
                st.rerun()

def render_privacy_policy_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Privacy Policy")
        col_a, col_b = st.columns([1,1])
        with col_a:
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.current_view = "main"
                st.rerun()
        st.markdown(PRIVACY_POLICY_TEXT, unsafe_allow_html=True)
        st.divider()

def render_terms_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Terms & Conditions")
        col_a, col_b = st.columns([1,1])
        with col_a:
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.current_view = "main"
                st.rerun()
        st.markdown(TERMS_POLICY_TEXT, unsafe_allow_html=True)
        st.divider()

def render_refund_policy_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Refund & Cancellation Policy")
        col_a, col_b = st.columns([1,1])
        with col_a:
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.current_view = "main"
                st.rerun()
        st.markdown(REFUND_POLICY_TEXT, unsafe_allow_html=True)
        st.divider()

def render_dashboard_page():
    """Enhanced dashboard for financial automation"""
    
    # Dashboard Header
    st.markdown(f"""
        <div class="dashboard-header">
            <div class="dashboard-title">Financial Automation Dashboard</div>
            <div class="dashboard-subtitle">Welcome to Xml2Tally</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Get actual values for display
    active_templates = len(st.session_state.journal_templates)
    ledgers_available = len(st.session_state.ledger_master)
    smart_rules = len(st.session_state.bank_rules)
    ai_learnings = len(st.session_state.learned_mappings)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Active Templates</div>
                <div class="metric-value">{active_templates}</div>
                <div class="status-indicator status-success">Ready</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Ledgers Available</div>
                <div class="metric-value">{ledgers_available}</div>
                <div class="status-indicator status-success">Loaded</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Smart Rules</div>
                <div class="metric-value">{smart_rules}</div>
                <div class="status-indicator status-success">Active</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AI Learnings</div>
                <div class="metric-value">{ai_learnings}</div>
                <div class="status-indicator status-success">Growing</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation Cards
    st.markdown("## Automation Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏦 Bank Reconciliation\n\nAutomatically match bank statements with Tally ledgers", 
                    use_container_width=True, help="Convert bank statements to Tally XML"):
            st.session_state.current_view = "bank_converter"
            st.rerun()
    
    with col2:
        if st.button("Journal Automation\n\nConvert CSV/Excel journals to Tally XML format", 
                    use_container_width=True, help="Process journal entries to Tally XML"):
            st.session_state.current_view = "journal_converter"
            st.rerun()
    
    with col3:
        if st.button("Settings & Configuration\n\nManage templates, ledgers, and automation rules", 
                    use_container_width=True, help="Configure your automation settings"):
            st.session_state.current_view = "settings"
            st.rerun()
    
    st.markdown("---")
    
    # Recent Activity & Quick Actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quick Actions")
        
        if st.button("Upload Bank Statement", use_container_width=True):
            st.session_state.current_view = "bank_converter"
            st.rerun()
            
        if st.button("Process Journal Entry", use_container_width=True):
            st.session_state.current_view = "journal_converter"
            st.rerun()
            
        if st.button("Configure Smart Rules", use_container_width=True):
            st.session_state.current_view = "settings"
            st.rerun()
    
    with col2:
        st.subheader("System Status")
        
        # AI Status
        ai_status = "🟢 Active" if ledger_mapper.initialized else "🟡 Limited"
        st.write(f"**AI Mapping Engine:** {ai_status}")
        
        # Template Status
        template_status = "🟢 Ready" if st.session_state.journal_templates else "🟡 Setup Required"
        st.write(f"**Templates:** {template_status}")
        
        # Ledger Status
        ledger_status = "🟢 Loaded" if len(st.session_state.ledger_master) > 1 else "🟡 Setup Required"
        st.write(f"**Ledger Master:** {ledger_status}")
        
        # Rules Status
        rules_status = "🟢 Active" if st.session_state.bank_rules else "🟡 Recommended"
        st.write(f"**Smart Rules:** {rules_status}")

def render_journal_converter_page():
    """Enhanced journal converter page"""
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1>Journal Automation</h1>
            <p style="color: #666; font-size: 1.1rem;">Convert CSV/Excel journals to Tally XML with intelligent mapping</p>
        </div>
    """, unsafe_allow_html=True)

    # Use tally_company_name if direct push is enabled, otherwise use company_name
    enable_direct_push = st.session_state.get('enable_direct_push_journal', False)
    tally_company_name = st.session_state.get('tally_company_name', '')
    company_name = st.session_state.get('company_name', 'Xml2Tally (Default Co.)')

    # If direct push is enabled and tally_company_name is set, use it; otherwise fall back to company_name
    if enable_direct_push and tally_company_name:
        company_name = tally_company_name

    rules_config = st.session_state.get('bank_rules', [])
    ledger_master = st.session_state.get('ledger_master', ["Bank Suspense A/c (Default)"])
    suspense_ledger = st.session_state.get('default_suspense_ledger', "Bank Suspense A/c (Default)")
    journal_templates = st.session_state.get('journal_templates', {})
    learned_mappings = st.session_state.get('learned_mappings', {})

    if not ledger_master or ledger_master == ["Bank Suspense A/c (Default)"]:
        st.warning("""
            **Setup Required**: Please upload your **Ledger Master** in the **Settings** page before using this tool.
            
            This ensures accurate mapping of your journal entries to the correct Tally accounts.
        """)
        if st.button("Go to Settings", use_container_width=True):
            st.session_state.current_view = "settings"
            st.rerun()
        st.stop()
        
    if not journal_templates:
        st.warning("""
            **Setup Required**: Please create at least one **Journal Template** in the **Settings** page.
            
            Templates define how your CSV/Excel data maps to Tally ledger structure.
        """)
        if st.button("Go to Settings", use_container_width=True):
            st.session_state.current_view = "settings"
            st.rerun()
        st.stop()

    # Process Steps
    st.markdown("""
        <div class="process-steps">
            <div class="process-step">
                <div class="step-number">1</div>
                <div class="step-title">Select Template</div>
                <div class="step-description">Choose your journal format</div>
            </div>
            <div class="process-step">
                <div class="step-number">2</div>
                <div class="step-title">Upload Data</div>
                <div class="step-description">CSV or Excel file</div>
            </div>
            <div class="process-step">
                <div class="step-number">3</div>
                <div class="step-title">AI Mapping</div>
                <div class="step-description">Automatic ledger matching</div>
            </div>
            <div class="process-step">
                <div class="step-number">4</div>
                <div class="step-title">Export XML</div>
                <div class="step-description">Ready for Tally</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 1: Template Selection
    st.subheader("1. Select Journal Template")
    template_name_list = ["<Select a Template>"] + list(journal_templates.keys())
    selected_template_name = st.selectbox("Choose your journal template:", template_name_list)

    if selected_template_name == "<Select a Template>":
        st.info("Select a template to define how your journal data should be processed.")
        st.stop()

    template_id = journal_templates[selected_template_name]
    conn = get_db_conn()
    with conn.session as s:
        fixed_rules_db = s.execute(text('SELECT csv_col, tally_ledger, type FROM journal_template_fixed_rules WHERE template_id = :id'), params=dict(id=template_id)).fetchall()
        fixed_rules = [{'CSV Column Name': r[0], 'Tally Ledger Name': r[1], 'Type (Debit/Credit)': r[2]} for r in fixed_rules_db]
        
        dynamic_rules_db = s.execute(text('SELECT ledger_name_col, amount_col, type FROM journal_template_dynamic_rules WHERE template_id = :id'), params=dict(id=template_id)).fetchall()
        dynamic_rules = [{'CSV Column for Ledger Name': r[0], 'CSV Column for Amount': r[1], 'Transaction Type': r[2]} for r in dynamic_rules_db]
    
    # Step 2: Voucher Type
    st.subheader("2. Select Voucher Type")
    voucher_type = st.selectbox(
        "Which Tally Voucher Type are you importing?",
        ("Journal", "Sales", "Purchase", "Payment", "Receipt", "Credit Note", "Debit Note", "Contra"),
        key="journal_voucher_type"
    )
    
    st.divider()
    
    # Step 3: Download Template
    st.subheader("3. Download Template (Optional)")
    st.write("Use this template to ensure your data is in the correct format.")
    st.download_button(
        label=f"📥 Download {selected_template_name}_Template.csv",
        data=get_template_csv(fixed_rules, dynamic_rules),
        file_name=f"{selected_template_name}_Template.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.divider()
    
    # Step 4: Upload and Process
    st.subheader("4. Upload and Process Journal")
    
    st.markdown("""
        <div class="upload-card">
            <div class="upload-icon">📤</div>
            <h3>Upload Your Journal File</h3>
            <p>Supported formats: CSV, Excel (.xlsx)</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your journal file",
        type=["csv", "xlsx"],
        key="journal_uploader",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        try:
            # Process file
            df = pd.read_csv(uploaded_file, encoding='latin1') if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            
            st.success(f"File processed successfully! Found {len(df)} journal entries.")
            
            st.divider()
            
            # Step 5: AI Mapping
            st.subheader("5. AI-Powered Ledger Mapping")
            st.write("We'll automatically suggest mappings for dynamic columns in your template.")
            
            edited_mappings = {}

            with st.spinner("Analyzing data with AI..."):
                for rule in dynamic_rules:
                    name_col = rule['CSV Column for Ledger Name']
                    if name_col not in df.columns:
                        st.error(f"Column '{name_col}' not found in your file. Please check your template settings.")
                        continue
                    
                    st.markdown(f"#### Mapping for: `{name_col}`")
                    
                    unique_values = df[name_col].dropna().unique()
                    
                    suggestions_map, confidence_scores, match_types = get_smart_suggestions(
                        unique_values,
                        ledger_master,
                        rules_config,
                        suspense_ledger,
                        learned_mappings
                    )

                    # SIMPLIFIED: Removed confidence and match type columns
                    mapping_data = []
                    for val in unique_values:
                        # Convert to string for dictionary lookup (get_smart_suggestions returns string keys)
                        val_str = str(val) if pd.notna(val) else "__NaN__"
                        suggestion = suggestions_map.get(val_str, suspense_ledger)
                        mapping_data.append({
                            "CSV Value": val,
                            "Mapped Ledger": suggestion
                        })
                    
                    mapping_df = pd.DataFrame(mapping_data)
                    
                    # Add Auto-Map button for this column
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"Found {len(mapping_df)} unique values to map. Please review and adjust if needed.")
                    with col2:
                        if st.button(f"Auto Map {name_col}", key=f"auto_map_{name_col}", use_container_width=True):
                            # Apply auto-mapping based on rules and learned mappings
                            auto_mappings = auto_map_ledgers_based_on_rules(
                                unique_values,
                                ledger_master,
                                rules_config,
                                suspense_ledger,
                                learned_mappings
                            )
                            
                            # Update the mapping dataframe with auto-mappings
                            for idx, row in mapping_df.iterrows():
                                csv_value = str(row['CSV Value'])
                                if csv_value in auto_mappings and auto_mappings[csv_value] != suspense_ledger:
                                    mapping_df.at[idx, 'Mapped Ledger'] = auto_mappings[csv_value]
                            
                            st.success(f"Auto-mapped {name_col} column!")
                            st.rerun()
                    
                    # SIMPLIFIED: Removed confidence summary display
                    
                    # SIMPLIFIED: Removed confidence and match type columns from data editor
                    edited_df = st.data_editor(
                        mapping_df,
                        column_config={
                            "CSV Value": st.column_config.TextColumn("CSV Value", disabled=True),
                            "Mapped Ledger": st.column_config.SelectboxColumn(
                                "Tally Ledger",
                                options=ledger_master,
                                required=True,
                            )
                        },
                        use_container_width=True,
                        hide_index=True,
                        key=f"editor_{name_col}"
                    )
                    edited_mappings[name_col] = edited_df
            
            st.divider()

            # Final Actions
            # Check if direct push is enabled
            enable_direct_push = st.session_state.get('enable_direct_push_journal', False)

            if enable_direct_push:
                # Show Direct Push button as primary action
                if st.button(f"🚀 Direct Push to Tally", type="primary", use_container_width=True):
                    # Automatically learn from user mappings
                    learned_count = 0
                    for col_name, mapping_df in edited_mappings.items():
                        for _index, row in mapping_df.iterrows():
                            csv_value = row['CSV Value']
                            mapped_ledger = row['Mapped Ledger']

                            if mapped_ledger != suspense_ledger:
                                confidence = 90
                                update_learned_mappings(
                                    st.session_state.email,
                                    csv_value,
                                    mapped_ledger,
                                    confidence
                                )
                                learned_count += 1

                    if learned_count > 0:
                        st.success(f"🧠 AI learned from {learned_count} mappings for future use!")

                    with st.spinner("Pushing vouchers to Tally..."):
                        xml_data = create_tally_xml(
                            df,
                            fixed_rules,
                            dynamic_rules,
                            company_name,
                            voucher_type,
                            edited_mappings
                        )

                        success, message, count = push_vouchers_to_tally(
                            xml_data,
                            st.session_state.tally_server_host,
                            st.session_state.tally_server_port
                        )

                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

                    # Provide XML download for debugging
                    st.download_button(
                        label="📥 Download Sent XML (for debugging)",
                        data=xml_data,
                        file_name=f"tally_{voucher_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
                        mime="text/xml",
                        help="Download the exact XML that was sent to Tally for debugging"
                    )

                # Show Download XML as secondary option
                if st.button(f"📥 Download {voucher_type} XML (Backup)", use_container_width=True):
                    # Automatically learn from user mappings
                    learned_count = 0
                    for col_name, mapping_df in edited_mappings.items():
                        for _index, row in mapping_df.iterrows():
                            csv_value = row['CSV Value']
                            mapped_ledger = row['Mapped Ledger']

                            if mapped_ledger != suspense_ledger:
                                confidence = 90
                                update_learned_mappings(
                                    st.session_state.email,
                                    csv_value,
                                    mapped_ledger,
                                    confidence
                                )
                                learned_count += 1

                    if learned_count > 0:
                        st.success(f"🧠 AI learned from {learned_count} mappings for future use!")

                    with st.spinner("Generating Tally XML..."):
                        xml_data = create_tally_xml(
                            df,
                            fixed_rules,
                            dynamic_rules,
                            company_name,
                            voucher_type,
                            edited_mappings
                        )

                    st.success("Tally XML generated successfully!")
                    st.download_button(
                        label=f"📥 Download {voucher_type}Vouchers.xml",
                        data=xml_data,
                        file_name=f"{voucher_type}Vouchers.xml",
                        mime="application/xml",
                        use_container_width=True
                    )
            else:
                # Show only Generate XML button when direct push is disabled
                if st.button(f"Convert to Tally {voucher_type} XML", type="primary", use_container_width=True):
                    # Automatically learn from user mappings when they generate XML
                    learned_count = 0
                    for col_name, mapping_df in edited_mappings.items():
                        for _index, row in mapping_df.iterrows():
                            csv_value = row['CSV Value']
                            mapped_ledger = row['Mapped Ledger']

                            if mapped_ledger != suspense_ledger:
                                confidence = 90  # Default high confidence for manual mappings
                                update_learned_mappings(
                                    st.session_state.email,
                                    csv_value,
                                    mapped_ledger,
                                    confidence
                                )
                                learned_count += 1

                    if learned_count > 0:
                        st.success(f"🧠 AI learned from {learned_count} mappings for future use!")

                    with st.spinner("Generating Tally XML..."):
                        xml_data = create_tally_xml(
                            df,
                            fixed_rules,
                            dynamic_rules,
                            company_name,
                            voucher_type,
                            edited_mappings
                        )

                    st.success("Tally XML generated successfully!")
                    st.download_button(
                        label=f"📥 Download {voucher_type}Vouchers.xml",
                        data=xml_data,
                        file_name=f"{voucher_type}Vouchers.xml",
                        mime="application/xml",
                        use_container_width=True
                    )
                    
        except Exception as e:
            st.error(f"Error processing file: {e}")

def render_bank_converter_page():
    """Simplified bank converter page with auto-mapping"""
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1>🏦 Bank Reconciliation</h1>
            <p style="color: #666; font-size: 1.1rem;">Convert bank statements to Tally XML format</p>
        </div>
    """, unsafe_allow_html=True)

    # Use tally_company_name if direct push is enabled, otherwise use company_name
    enable_direct_push = st.session_state.get('enable_direct_push_bank', False)
    tally_company_name = st.session_state.get('tally_company_name', '')
    company_name = st.session_state.get('company_name', 'Xml2Tally (Default Co.)')

    # If direct push is enabled and tally_company_name is set, use it; otherwise fall back to company_name
    if enable_direct_push and tally_company_name:
        company_name = tally_company_name

    ledger_master = st.session_state.get('ledger_master', [])
    if not ledger_master:
        synced_ledgers = get_synced_ledgers(st.session_state.email)
        ledger_master = [row[0] for row in synced_ledgers] if synced_ledgers else []

    if not ledger_master:
        ledger_master = ["Bank Suspense A/c (Default)"]

    rules_config = st.session_state.get('bank_rules', [])
    learned_mappings = st.session_state.get('learned_mappings', {})

    suspense_ledger_options = ledger_master.copy()
    current_suspense = st.session_state.get('default_suspense_ledger', "Bank Suspense A/c (Default)")
    if current_suspense not in suspense_ledger_options:
        suspense_ledger_options = [current_suspense] + suspense_ledger_options

    suspense_index = suspense_ledger_options.index(current_suspense) if current_suspense in suspense_ledger_options else 0

    st.subheader("Suspense Ledger for Unmapped Bank Entries")
    st.caption("Select which ledger should receive transactions that cannot be auto-mapped during bank sync.")
    selected_suspense_ledger = st.selectbox(
        "Choose suspense ledger (synced from Tally):",
        options=suspense_ledger_options,
        index=suspense_index,
        key="bank_page_suspense_ledger",
        help="Pick the Tally ledger to use for unmatched bank transactions."
    )

    if selected_suspense_ledger != st.session_state.get('default_suspense_ledger'):
        st.session_state.default_suspense_ledger = selected_suspense_ledger

    if st.button("Save suspense ledger preference", type="secondary", use_container_width=True):
        try:
            conn = get_db_conn()
            with conn.session as s:
                s.execute(text('''
                    INSERT INTO user_preferences (email, default_suspense_ledger)
                    VALUES (:email, :suspense)
                    ON CONFLICT(email) DO UPDATE SET default_suspense_ledger = :suspense
                '''), params=dict(email=st.session_state.email, suspense=selected_suspense_ledger))
                s.commit()
            st.success("Suspense ledger preference saved for future sessions.")
        except Exception as e:
            st.error(f"Failed to save suspense ledger preference: {e}")

    suspense_ledger = selected_suspense_ledger

    if suspense_ledger == "Bank Suspense A/c (Default)":
        st.warning("Consider selecting a suspense ledger synced from Tally to improve mapping accuracy.")
    
    # Process Steps
    st.markdown("""
        <div class="process-steps">
            <div class="process-step">
                <div class="step-number">1</div>
                <div class="step-title">Select Bank</div>
                <div class="step-description">Choose Tally ledger</div>
            </div>
            <div class="process-step">
                <div class="step-number">2</div>
                <div class="step-title">Upload Statement</div>
                <div class="step-description">CSV or Excel format</div>
            </div>
            <div class="process-step">
                <div class="step-number">3</div>
                <div class="step-title">Map Transactions</div>
                <div class="step-description">Assign ledgers manually or automatically</div>
            </div>
            <div class="process-step">
                <div class="step-number">4</div>
                <div class="step-title">Export & Import</div>
                <div class="step-description">Ready for Tally</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 1: Bank Selection
    st.subheader("1. Select Bank Account")
    bank_ledger = st.selectbox(
        "Which Tally ledger represents this bank account?",
        options=ledger_master
    )
    
    st.divider()
    
    # Step 2: Download Template
    st.subheader("2. Download Template (Optional)")
    st.write("Use this template to ensure your bank statement is in the correct format.")
    st.download_button(
        label="📥 Download Bank Statement Template",
        data=get_bank_template_csv(),
        file_name="Bank_Statement_Template.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.divider()
    
    # Step 3: Upload and Process
    st.subheader("3. Upload Bank Statement")
    
    st.markdown("""
        <div class="upload-card">
            <div class="upload-icon">🏦</div>
            <h3>Upload Your Bank Statement</h3>
            <p>Supported formats: CSV, Excel (.xlsx)</p>
            <p style="font-size: 0.9rem; color: #666;">Required columns: Date, Narration, Debit, Credit</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your bank statement file",
        type=["csv", "xlsx"],
        key="bank_uploader",
        label_visibility="collapsed"
    )
    
    if uploaded_file and bank_ledger:
        try:
            # Process file
            df = pd.read_csv(uploaded_file, encoding='latin1') if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            df.columns = [str(c).strip().title() for c in df.columns] 
            
            # Validate required columns
            for col in ['Date', 'Narration', 'Debit', 'Credit']:
                if col not in df.columns:
                    st.error(f"Required column '{col}' not found in file. Please use the template.")
                    st.stop()
            
            # Convert numeric columns
            for col in ['Debit', 'Credit']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            # Set default ledger for all transactions
            df['Mapped Ledger'] = suspense_ledger
            
            st.success(f"Bank statement processed! {len(df)} transactions ready for mapping.")
            
            st.divider()
            
            # Step 4: Mapping Section with Auto-Map Button
            st.subheader("4. Map Transactions to Ledgers")
            
            # Auto-map button
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.info("""
                **Smart Mapping:**
                - Uses your smart rules and learned mappings
                - Automatically suggests ledgers based on previous decisions
                - Updates only unmapped transactions by default
                """)
            
            with col2:
                overwrite_existing = st.checkbox("Overwrite existing mappings", value=False, 
                                               help="If checked, will replace ALL mappings. If unchecked, only updates suspense ledger mappings.")
            
            with col3:
                if st.button("Auto Map Ledgers", use_container_width=True, type="secondary"):
                    with st.spinner("Applying smart rules and learned mappings..."):
                        # Get unique narrations for auto-mapping
                        unique_narrations = df['Narration'].unique()
                        
                        # Get auto-mappings based on rules and learned patterns
                        auto_mappings = auto_map_ledgers_based_on_rules(
                            unique_narrations,
                            ledger_master,
                            rules_config,
                            suspense_ledger,
                            learned_mappings
                        )
                        
                        # Apply auto-mappings to dataframe
                        updated_count = 0
                        for idx, row in df.iterrows():
                            narration = str(row['Narration'])
                            current_ledger = row['Mapped Ledger']
                            
                            # Apply auto-mapping based on user preference
                            if overwrite_existing or current_ledger == suspense_ledger:
                                auto_ledger = auto_mappings.get(narration, suspense_ledger)
                                if auto_ledger != suspense_ledger:  # Only update if we found a better match
                                    df.at[idx, 'Mapped Ledger'] = auto_ledger
                                    updated_count += 1
                        
                        st.success(f"Auto-mapped {updated_count} transactions!")
                        
                        # Show mapping statistics
                        if updated_count > 0:
                            mapping_sources = {}
                            for narration in unique_narrations:
                                auto_ledger = auto_mappings.get(str(narration), suspense_ledger)
                                if auto_ledger != suspense_ledger:
                                    # Determine mapping source
                                    if str(narration) in learned_mappings:
                                        source = "Learned Mapping"
                                    else:
                                        source = "Smart Rule"
                                    mapping_sources[source] = mapping_sources.get(source, 0) + 1
                            
                            if mapping_sources:
                                st.info(f"**Mapping Sources:** {', '.join([f'{k}: {v}' for k, v in mapping_sources.items()])}")

            st.info("""
            **Manual Mapping Instructions:**
            - For each transaction, select the appropriate Tally ledger from the dropdown
            - Use the default suspense ledger for transactions you're unsure about
            - The AI will automatically learn from your mappings for future suggestions
            """)

            # Data editor for manual mapping
            st.write(f"Mapping {len(df)} transactions. Select the correct ledger for each transaction:")
            
            edited_df = st.data_editor(
                df[['Date', 'Narration', 'Debit', 'Credit', 'Mapped Ledger']],
                column_config={
                    "Mapped Ledger": st.column_config.SelectboxColumn(
                        "Mapped Ledger",
                        help="Select the Tally ledger for this transaction",
                        options=ledger_master,
                        required=True,
                    )
                },
                use_container_width=True,
                hide_index=True,
                num_rows="dynamic",
                key="bank_mapping_editor"
            )

            st.divider()

            # Final Actions
            # Check if direct push is enabled
            enable_direct_push = st.session_state.get('enable_direct_push_bank', False)

            if enable_direct_push:
                # Show Direct Push button as primary action
                if st.button("🚀 Direct Push to Tally", type="primary", use_container_width=True):
                    # Automatically learn from user mappings
                    learned_count = 0
                    for index, row in edited_df.iterrows():
                        narration = str(row['Narration'])
                        mapped_ledger = row['Mapped Ledger']

                        if mapped_ledger != suspense_ledger:
                            update_learned_mappings(
                                st.session_state.email,
                                narration,
                                mapped_ledger,
                                90
                            )
                            learned_count += 1

                    if learned_count > 0:
                        st.success(f"🧠 AI learned from {learned_count} mappings for future suggestions!")

                    with st.spinner("Pushing bank vouchers to Tally..."):
                        xml_data = create_bank_tally_xml(
                            edited_df,
                            bank_ledger,
                            company_name
                        )

                        success, message, count = push_vouchers_to_tally(
                            xml_data,
                            st.session_state.tally_server_host,
                            st.session_state.tally_server_port
                        )

                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

                    # Provide XML download for debugging
                    st.download_button(
                        label="📥 Download Sent XML (for debugging)",
                        data=xml_data,
                        file_name=f"tally_bank_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
                        mime="text/xml",
                        help="Download the exact XML that was sent to Tally for debugging"
                    )

                # Show Download XML as secondary option
                if st.button("📥 Download Bank XML (Backup)", use_container_width=True):
                    # Automatically learn from user mappings
                    learned_count = 0
                    for index, row in edited_df.iterrows():
                        narration = str(row['Narration'])
                        mapped_ledger = row['Mapped Ledger']

                        if mapped_ledger != suspense_ledger:
                            update_learned_mappings(
                                st.session_state.email,
                                narration,
                                mapped_ledger,
                                90
                            )
                            learned_count += 1

                    if learned_count > 0:
                        st.success(f"🧠 AI learned from {learned_count} mappings for future suggestions!")

                    with st.spinner("Generating Tally XML..."):
                        xml_data = create_bank_tally_xml(
                            edited_df,
                            bank_ledger,
                            company_name
                        )

                    st.success("Tally XML generated successfully!")
                    st.download_button(
                        label="📥 Download BankVouchers.xml",
                        data=xml_data,
                        file_name="BankVouchers.xml",
                        mime="application/xml",
                        use_container_width=True
                    )
            else:
                # Show only Generate XML button when direct push is disabled
                if st.button("Generate Tally XML", type="primary", use_container_width=True):
                    # Automatically learn from user mappings when they generate XML
                    learned_count = 0
                    for index, row in edited_df.iterrows():
                        narration = str(row['Narration'])
                        mapped_ledger = row['Mapped Ledger']

                        if mapped_ledger != suspense_ledger:
                            update_learned_mappings(
                                st.session_state.email,
                                narration,
                                mapped_ledger,
                                90  # High confidence for manual mappings
                            )
                            learned_count += 1

                    if learned_count > 0:
                        st.success(f"🧠 AI learned from {learned_count} mappings for future suggestions!")

                    with st.spinner("Generating Tally XML..."):
                        xml_data = create_bank_tally_xml(
                            edited_df,
                            bank_ledger,
                            company_name
                        )

                    st.success("Tally XML generated successfully!")
                    st.download_button(
                        label="📥 Download BankVouchers.xml",
                        data=xml_data,
                        file_name="BankVouchers.xml",
                        mime="application/xml",
                        use_container_width=True
                    )
                    
        except Exception as e:
            st.error(f"Error processing bank statement: {e}")

def render_settings_page():
    """Enhanced settings page"""
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1>Settings & Configuration</h1>
            <p style="color: #666; font-size: 1.1rem;">Configure your financial automation settings</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Company", "Journals", "AI Settings", "Tally Integration"])

    with tab1:
        st.subheader("Company Settings")
        
        with st.container():
            st.text_input(
                "Tally Company Name:", 
                value=st.session_state.company_name,
                key="company_name_input",
                help="This name must exactly match your company name in Tally."
            )
            
            if st.button("Save Company Settings", use_container_width=True):
                conn = get_db_conn()
                with conn.session as s:
                    s.execute(text('''
                        INSERT INTO user_preferences (email, company_name) VALUES (:email, :name)
                        ON CONFLICT(email) DO UPDATE SET company_name = :name
                    '''), params=dict(email=st.session_state.email, name=st.session_state.company_name_input))
                    s.commit()
                st.session_state.company_name = st.session_state.company_name_input
                st.success("Company name saved successfully!")

    with tab2:
        st.subheader("Journal Template Manager")
        
        template_names = list(st.session_state.journal_templates.keys())
        selected_template_name = st.selectbox("Select a template to edit:", ["<Create New Template>"] + template_names)
        
        new_template_name = st.text_input("Or create a new template:")
        
        template_id = None
        fixed_rules = []
        dynamic_rules = []

        if selected_template_name != "<Create New Template>":
            template_id = st.session_state.journal_templates[selected_template_name]
            conn = get_db_conn()
            with conn.session as s:
                fixed_rules_db = s.execute(text('SELECT csv_col, tally_ledger, type FROM journal_template_fixed_rules WHERE template_id = :id'), params=dict(id=template_id)).fetchall()
                fixed_rules = [{'CSV Column Name': r[0], 'Tally Ledger Name': r[1], 'Type (Debit/Credit)': r[2]} for r in fixed_rules_db]
                
                dynamic_rules_db = s.execute(text('SELECT ledger_name_col, amount_col, type FROM journal_template_dynamic_rules WHERE template_id = :id'), params=dict(id=template_id)).fetchall()
                dynamic_rules = [{'CSV Column for Ledger Name': r[0], 'CSV Column for Amount': r[1], 'Transaction Type': r[2]} for r in dynamic_rules_db]
        
        st.divider()
        
        # Fixed Ledgers
        st.subheader("Fixed Ledger Columns")
        st.write("Define columns that always map to specific Tally ledgers.")
        
        if not fixed_rules:
            fixed_rules = [{'CSV Column Name': '', 'Tally Ledger Name': '', 'Type (Debit/Credit)': 'Debit'}]
        
        fixed_df = pd.DataFrame(fixed_rules)
        
        edited_fixed_df = st.data_editor(
            fixed_df,
            num_rows="dynamic",
            column_config={
                "CSV Column Name": st.column_config.TextColumn(
                    "CSV Column Name", 
                    help="Name of the column in your CSV file",
                    required=True
                ),
                "Tally Ledger Name": st.column_config.TextColumn(
                    "Tally Ledger Name",
                    help="Fixed Tally ledger name for this column",
                    required=True
                ),
                "Type (Debit/Credit)": st.column_config.SelectboxColumn(
                    "Type",
                    help="Debit or Credit for this ledger",
                    options=["Debit", "Credit"],
                    required=True
                )
            },
            use_container_width=True,
            key="journal_fixed_editor"
        )
        
        st.divider()
        
        # Dynamic Ledgers
        st.subheader("Dynamic Ledger Columns")
        st.write("Define columns where each value needs individual ledger mapping.")
        
        if not dynamic_rules:
            dynamic_rules = [{'CSV Column for Ledger Name': '', 'CSV Column for Amount': '', 'Transaction Type': 'Debit'}]
        
        dynamic_df = pd.DataFrame(dynamic_rules)
        
        edited_dynamic_df = st.data_editor(
            dynamic_df,
            num_rows="dynamic",
            column_config={
                "CSV Column for Ledger Name": st.column_config.TextColumn(
                    "Ledger Name Column",
                    help="CSV column containing values to be mapped to ledgers",
                    required=True
                ),
                "CSV Column for Amount": st.column_config.TextColumn(
                    "Amount Column", 
                    help="CSV column containing amounts",
                    required=True
                ),
                "Transaction Type": st.column_config.SelectboxColumn(
                    "Transaction Type",
                    help="Debit or Credit for these entries",
                    options=["Debit", "Credit"],
                    required=True
                )
            },
            use_container_width=True,
            key="journal_dynamic_editor"
        )
        
        # Save Template
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Template", type="primary", use_container_width=True):
                save_name = new_template_name if new_template_name else selected_template_name
                if not save_name or save_name == "<Create New Template>":
                    st.error("Please enter a name for your template.")
                else:
                    # Validate and save
                    fixed_to_save = edited_fixed_df.to_dict('records')
                    dynamic_to_save = edited_dynamic_df.to_dict('records')
                    
                    conn = get_db_conn()
                    with conn.session as s:
                        try:
                            s.execute(text('INSERT INTO journal_templates (email, template_name) VALUES (:email, :name)'),
                                      params=dict(email=st.session_state.email, name=save_name))
                            s.commit()
                        except Exception as e:
                            # Template may already exist, continue to retrieve it
                            print(f"Note: Template may already exist: {e}")

                        template_id_res = s.execute(text('SELECT id FROM journal_templates WHERE email = :email AND template_name = :name'),
                                                 params=dict(email=st.session_state.email, name=save_name)).fetchone()

                        if not template_id_res:
                            st.error("Failed to create or find template. Please try again.")
                            return

                        template_id = template_id_res[0]
                        
                        # Update rules
                        s.execute(text('DELETE FROM journal_template_fixed_rules WHERE template_id = :id'), params=dict(id=template_id))
                        s.execute(text('DELETE FROM journal_template_dynamic_rules WHERE template_id = :id'), params=dict(id=template_id))
                        
                        for rule in fixed_to_save:
                            s.execute(text('''
                                INSERT INTO journal_template_fixed_rules (template_id, csv_col, tally_ledger, type) 
                                VALUES (:id, :csv, :tally, :type)
                            '''), params=dict(id=template_id, csv=rule['CSV Column Name'], tally=rule['Tally Ledger Name'], type=rule['Type (Debit/Credit)']))
                        
                        for rule in dynamic_to_save:
                            s.execute(text('''
                                INSERT INTO journal_template_dynamic_rules (template_id, ledger_name_col, amount_col, type) 
                                VALUES (:id, :name_col, :amt_col, :type)
                            '''), params=dict(id=template_id, name_col=rule['CSV Column for Ledger Name'], amt_col=rule['CSV Column for Amount'], type=rule['Transaction Type']))
                        
                        s.commit()
                    
                    st.session_state.settings_loaded = False
                    st.success(f"Template '{save_name}' saved successfully!")
                    st.rerun()

        with col2:
            if selected_template_name != "<Create New Template>":
                if st.button("Delete Template", type="secondary", use_container_width=True):
                    conn = get_db_conn()
                    with conn.session as s:
                        s.execute(text('DELETE FROM journal_templates WHERE id = :id'), params=dict(id=template_id))
                        s.commit()
                    st.session_state.settings_loaded = False
                    st.success(f"Template '{selected_template_name}' deleted.")
                    st.rerun()

    with tab3:
        st.subheader("AI Learning & Configuration")
        
        # AI Status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### AI Status")
            if ledger_mapper.initialized:
                st.success("Semantic AI: ACTIVE")
                st.write("AI model is ready for intelligent ledger mapping.")
            else:
                st.warning("Semantic AI: NOT AVAILABLE")
                st.write("Install sentence-transformers for enhanced AI features.")
            
            if st.button("Initialize AI Models", use_container_width=True):
                if initialize_ai_model():
                    st.success("AI models initialized successfully!")
                    st.rerun()
                else:
                    st.error("Failed to initialize AI models.")

        with col2:
            st.markdown("#### Performance")
            if st.session_state.learned_mappings:
                learned_count = len(st.session_state.learned_mappings)
                st.metric("Learned Mappings", learned_count)
                st.write("AI has learned from your previous corrections.")
            else:
                st.info("No learned mappings yet. AI will learn as you map transactions.")
        
        st.divider()
        
        # Learned Mappings Management
        st.markdown("#### Learned Mappings")
        st.info("""
        **🤖 Smart Learning Feature:**
        - AI automatically learns from your manual mappings in both Journal and Bank converters
        - Each time you map a ledger to a narration or CSV value, the AI remembers it
        - Future suggestions will be more accurate based on your previous decisions
        - No need to manually save learnings - it happens automatically!
        """)
        
        if st.session_state.learned_mappings:
            learned_data = []
            for narration, data in st.session_state.learned_mappings.items():
                learned_data.append({
                    'Narration': narration,
                    'Mapped Ledger': data['ledger'],
                    'Usage Count': data['count'],
                    'Confidence Score': f"{data['score']}%"
                })
            
            learned_df = pd.DataFrame(learned_data)
            st.dataframe(learned_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📤 Export Learned Data", use_container_width=True):
                    csv = learned_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="learned_mappings.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col2:
                if st.button("Clear All Learned Data", type="secondary", use_container_width=True):
                    conn = get_db_conn()
                    with conn.session as s:
                        s.execute(text('DELETE FROM user_learned_mappings WHERE email = :email'), 
                                params=dict(email=st.session_state.email))
                        s.commit()
                    st.session_state.settings_loaded = False
                    st.success("All learned mappings cleared!")
                    st.rerun()
        else:
            st.info("No learned mappings yet. The AI will start learning automatically as you map transactions in the Journal and Bank converters.")

    with tab4:
        st.subheader("Tally Direct Integration")
        st.markdown("""
            <div style="background-color: #e8f4f8; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                <p style="margin: 0; color: #1e3a8a;">
                    Configure direct integration with Tally for real-time sync and push capabilities.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Auto-detect companies on tab load if connection settings exist
        if 'auto_detected_companies' not in st.session_state:
            st.session_state.auto_detected_companies = False

        if (not st.session_state.auto_detected_companies and
            st.session_state.tally_server_host and
            st.session_state.tally_server_port):
            with st.spinner("Detecting companies from Tally server..."):
                success, message, companies = fetch_companies_from_tally(
                    st.session_state.tally_server_host,
                    st.session_state.tally_server_port
                )
                if success and companies:
                    st.session_state.detected_companies = companies
                    st.session_state.auto_detected_companies = True

        st.markdown("#### Tally Server Connection")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(
                "Tally Server Host:",
                value=st.session_state.tally_server_host,
                key="tally_host_input",
                help="Enter the IP address or hostname of your Tally server (default: localhost)"
            )
        with col2:
            st.number_input(
                "Tally Server Port:",
                value=st.session_state.tally_server_port,
                key="tally_port_input",
                min_value=1,
                max_value=65535,
                help="Enter the port number for Tally ODBC connection (default: 9000)"
            )

        # Company selection - use dropdown if companies are detected, otherwise show text input
        if st.session_state.detected_companies:
            # Add "Manual Entry" option to allow custom input
            company_options = [""] + st.session_state.detected_companies + ["-- Manual Entry --"]

            selected_company = st.selectbox(
                "Tally Company Name (for Direct Sync):",
                options=company_options,
                index=company_options.index(st.session_state.tally_company_name) if st.session_state.tally_company_name in company_options else 0,
                key="tally_company_select",
                help="Select your Tally company name from detected companies. If you don't see your company, click 'Test Connection' to refresh the list."
            )

            # If "Manual Entry" is selected, show text input
            if selected_company == "-- Manual Entry --":
                st.session_state.tally_company_name = st.text_input(
                    "Enter Company Name Manually:",
                    value=st.session_state.tally_company_name if st.session_state.tally_company_name != "-- Manual Entry --" else "",
                    key="tally_company_manual_input",
                    help="Enter your Tally company name manually"
                )
            else:
                st.session_state.tally_company_name = selected_company
        else:
            # No companies detected yet - show text input with info message
            st.text_input(
                "Tally Company Name (for Direct Sync):",
                value=st.session_state.tally_company_name,
                key="tally_company_input",
                help="Enter your Tally company name or click 'Test Connection' to auto-detect from Tally"
            )
            st.info("💡 Click 'Test Connection' to auto-detect company names from Tally server")

        st.divider()

        st.markdown("#### Setup mode")
        st.session_state.tally_simple_mode = st.checkbox(
            "Use simplified Tally setup (recommended)",
            value=st.session_state.tally_simple_mode,
            help="Toggle to switch between a single-choice setup and detailed advanced controls"
        )

        if st.session_state.tally_simple_mode:
            profile_options = [
                "Download XML files only",
                "Auto-sync ledgers and push vouchers",
            ]
            profile_help = {
                "Download XML files only": "Keeps everything manual. You download files and import them into Tally yourself.",
                "Auto-sync ledgers and push vouchers": "Turn on automatic ledger sync plus direct push for both Bank and Journal vouchers.",
            }

            selected_profile = st.radio(
                "Pick a quick setup",
                options=profile_options,
                index=profile_options.index(st.session_state.tally_simple_profile)
                if st.session_state.tally_simple_profile in profile_options
                else 0,
                key="tally_simple_profile",
                help="Choose the level of automation you want. You can still switch to advanced controls anytime."
            )

            presets = {
                "Download XML files only": {
                    "sync": False,
                    "sync_on_load": False,
                    "push_bank": False,
                    "push_journal": False,
                    "summary": "Manual mode selected. We'll only prepare XML downloads for you.",
                },
                "Auto-sync ledgers and push vouchers": {
                    "sync": True,
                    "sync_on_load": True,
                    "push_bank": True,
                    "push_journal": True,
                    "summary": "Full automation enabled. Ledgers sync automatically and vouchers push directly to Tally.",
                },
            }

            preset = presets[selected_profile]
            st.session_state.direct_sync_checkbox = preset["sync"]
            st.session_state.sync_on_load_checkbox = preset["sync_on_load"]
            st.session_state.direct_push_bank_checkbox = preset["push_bank"]
            st.session_state.direct_push_journal_checkbox = preset["push_journal"]

            st.success(preset["summary"])
            st.caption(profile_help[selected_profile])
        else:
            with st.expander("Advanced Tally controls", expanded=True):
                st.markdown("#### Direct Sync Settings")
                st.checkbox(
                    "Enable direct sync of Tally ledgers",
                    value=st.session_state.enable_direct_sync,
                    key="direct_sync_checkbox",
                    help="When enabled, ledgers will be automatically synced from Tally when you load the application"
                )

                st.checkbox(
                    "Sync ledgers on application load",
                    value=st.session_state.sync_ledgers_on_load,
                    key="sync_on_load_checkbox",
                    help="Automatically sync ledgers from Tally each time you log in"
                )

                st.divider()

                st.markdown("#### Direct Push Settings")
                st.markdown("Enable direct push to automatically send vouchers to Tally instead of downloading XML files.")

                col1, col2 = st.columns(2)
                with col1:
                    st.checkbox(
                        "Enable direct push for Bank vouchers",
                        value=st.session_state.enable_direct_push_bank,
                        key="direct_push_bank_checkbox",
                        help="When enabled, bank reconciliation vouchers will be pushed directly to Tally"
                    )
                with col2:
                    st.checkbox(
                        "Enable direct push for Journal vouchers",
                        value=st.session_state.enable_direct_push_journal,
                        key="direct_push_journal_checkbox",
                        help="When enabled, journal vouchers will be pushed directly to Tally"
                    )

        st.divider()

        st.markdown("#### Bank Suspense Ledger")
        st.write("Choose which ledger should receive unmatched bank transactions during Tally sync.")

        ledger_options = st.session_state.get('ledger_master', [])
        if not ledger_options:
            synced_ledgers = get_synced_ledgers(st.session_state.email)
            ledger_options = [row[0] for row in synced_ledgers] if synced_ledgers else []

        if not ledger_options:
            ledger_options = ["Bank Suspense A/c (Default)"]

        current_suspense = st.session_state.get('default_suspense_ledger', "Bank Suspense A/c (Default)")
        if current_suspense not in ledger_options:
            ledger_options = [current_suspense] + ledger_options

        suspense_index = ledger_options.index(current_suspense) if current_suspense in ledger_options else 0

        st.selectbox(
            "Suspense ledger for bank sync:",
            options=ledger_options,
            index=suspense_index,
            key="tally_suspense_ledger",
            help="This ledger will be used when bank entries cannot be auto-mapped."
        )

        st.divider()

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            if st.button("Save Tally Integration Settings", type="primary", use_container_width=True):
                # Get company name from appropriate source (dropdown or text input)
                company_name = st.session_state.tally_company_name
                if not st.session_state.detected_companies and 'tally_company_input' in st.session_state:
                    company_name = st.session_state.tally_company_input

                selected_suspense = st.session_state.get('tally_suspense_ledger', st.session_state.default_suspense_ledger)

                conn = get_db_conn()
                with conn.session as s:
                    s.execute(text('''
                        INSERT INTO tally_connection_settings
                        (email, tally_server_host, tally_server_port, tally_company_name,
                         enable_direct_sync, enable_direct_push_bank, enable_direct_push_journal,
                         sync_ledgers_on_load, last_sync_date)
                        VALUES (:email, :host, :port, :company, :sync, :push_bank, :push_journal, :sync_on_load, CURRENT_TIMESTAMP)
                        ON CONFLICT(email) DO UPDATE SET
                            tally_server_host = :host,
                            tally_server_port = :port,
                            tally_company_name = :company,
                            enable_direct_sync = :sync,
                            enable_direct_push_bank = :push_bank,
                            enable_direct_push_journal = :push_journal,
                            sync_ledgers_on_load = :sync_on_load,
                            last_sync_date = CURRENT_TIMESTAMP
                    '''), params=dict(
                        email=st.session_state.email,
                        host=st.session_state.tally_host_input,
                        port=st.session_state.tally_port_input,
                        company=company_name,
                        sync=st.session_state.direct_sync_checkbox,
                        push_bank=st.session_state.direct_push_bank_checkbox,
                        push_journal=st.session_state.direct_push_journal_checkbox,
                        sync_on_load=st.session_state.sync_on_load_checkbox
                    ))

                    s.execute(text('''
                        INSERT INTO user_preferences (email, default_suspense_ledger)
                        VALUES (:email, :suspense)
                        ON CONFLICT(email) DO UPDATE SET default_suspense_ledger = :suspense
                    '''), params=dict(email=st.session_state.email, suspense=selected_suspense))
                    s.commit()

                # Update session state with saved values
                st.session_state.tally_server_host = st.session_state.tally_host_input
                st.session_state.tally_server_port = st.session_state.tally_port_input
                st.session_state.tally_company_name = company_name
                st.session_state.enable_direct_sync = st.session_state.direct_sync_checkbox
                st.session_state.enable_direct_push_bank = st.session_state.direct_push_bank_checkbox
                st.session_state.enable_direct_push_journal = st.session_state.direct_push_journal_checkbox
                st.session_state.sync_ledgers_on_load = st.session_state.sync_on_load_checkbox
                st.session_state.default_suspense_ledger = selected_suspense

                st.success("Tally integration settings saved successfully!")

        with col2:
            if st.button("Test Connection", use_container_width=True, help="Click to refresh company list from Tally"):
                # Reset auto-detection flag to allow fresh detection
                st.session_state.auto_detected_companies = False
                with st.spinner("Testing connection and detecting companies..."):
                    success, message, companies = fetch_companies_from_tally(
                        st.session_state.tally_host_input,
                        st.session_state.tally_port_input
                    )
                    if success:
                        st.session_state.detected_companies = companies
                        st.session_state.auto_detected_companies = True
                        st.success(message)
                        if companies:
                            st.info(f"📋 Detected companies: {', '.join(companies)}")
                            # Auto-select first company if none selected
                            if not st.session_state.tally_company_name and companies:
                                st.session_state.tally_company_name = companies[0]
                        st.rerun()
                    else:
                        st.error(message)

        with col3:
            if st.button("Sync Ledgers Now", use_container_width=True, type="secondary"):
                if not st.session_state.tally_company_name:
                    st.error("Please enter Tally Company Name and save settings first!")
                else:
                    with st.spinner("Syncing ledgers from Tally..."):
                        success, message, count = sync_ledgers_from_tally(
                            st.session_state.tally_server_host,
                            st.session_state.tally_server_port,
                            st.session_state.tally_company_name,
                            st.session_state.email
                        )
                        if success:
                            st.success(message)
                            # Update ledger master with synced ledgers
                            synced_ledgers = get_synced_ledgers(st.session_state.email)
                            if synced_ledgers:
                                st.session_state.ledger_master = [row[0] for row in synced_ledgers]
                            st.rerun()
                        else:
                            st.error(message)

        st.divider()

        # Display synced ledgers information
        st.markdown("#### Synced Ledgers from Tally")

        # Get last sync date
        conn = get_db_conn()
        with conn.session as s:
            result = s.execute(text('''
                SELECT last_sync_date FROM tally_connection_settings WHERE email = :email
            '''), params={'email': st.session_state.email})
            row = result.fetchone()
            last_sync = row[0] if row and row[0] else None

        col1, col2 = st.columns(2)
        with col1:
            synced_ledgers = get_synced_ledgers(st.session_state.email)
            if synced_ledgers:
                st.metric("Total Synced Ledgers", len(synced_ledgers))
            else:
                st.metric("Total Synced Ledgers", 0)

        with col2:
            if last_sync:
                st.metric("Last Sync", last_sync.strftime("%Y-%m-%d %H:%M:%S") if isinstance(last_sync, datetime) else str(last_sync))
            else:
                st.metric("Last Sync", "Never")

        # Display synced ledgers in a table
        if synced_ledgers:
            st.markdown("##### Ledger List")
            ledgers_df = pd.DataFrame(synced_ledgers, columns=['Ledger Name', 'Group', 'Sync Date'])

            # Add search filter
            search_term = st.text_input("Search Ledgers:", placeholder="Type to filter ledgers...", key="ledger_search")

            if search_term:
                ledgers_df = ledgers_df[ledgers_df['Ledger Name'].str.contains(search_term, case=False, na=False)]

            st.dataframe(
                ledgers_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Ledger Name": st.column_config.TextColumn("Ledger Name", width="medium"),
                    "Group": st.column_config.TextColumn("Group", width="small"),
                    "Sync Date": st.column_config.DatetimeColumn("Synced On", width="small")
                },
                hide_index=True
            )

            # Export synced ledgers
            if st.button("Export Synced Ledgers to CSV", use_container_width=True):
                csv = ledgers_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"tally_ledgers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No ledgers synced yet. Click 'Sync Ledgers Now' to fetch ledgers from Tally.")

def logout():
    st.session_state.logged_in = False
    st.session_state.current_view = "main" 
    st.session_state.email = "default"
    st.session_state.settings_loaded = False 
    st.rerun()

# --- 9. Main App Router ---
init_db()

# Initialize AI model when the app starts
if not st.session_state.ai_initialized:
    if initialize_ai_model():
        st.session_state.ai_initialized = True

if not st.session_state.logged_in:
    if st.session_state.current_view == "main":
        render_main_page()
    elif st.session_state.current_view == "login":
        render_login_page()
    elif st.session_state.current_view == "signup":
        render_signup_page()
    elif st.session_state.current_view == "privacy":
        render_privacy_policy_page()
    elif st.session_state.current_view == "terms":
        render_terms_page()
    elif st.session_state.current_view == "refund":
        render_refund_policy_page()
    else:
        render_main_page()
else:
    if not st.session_state.settings_loaded:
        load_user_settings(st.session_state.email)
    
    # Enhanced Sidebar - WIDER FOR WEB USERS
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-header">
                <div class="sidebar-title">Xml2Tally</div>
                <div class="sidebar-subtitle">Financial Automation</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Navigation")
        
        # Sidebar navigation with larger buttons for web
        nav_cols = st.columns(1)
        with nav_cols[0]:
            if st.button("Dashboard", use_container_width=True, key="sidebar_dashboard"):
                st.session_state.current_view = "dashboard"
                st.rerun()
                
            if st.button("Bank Reconciliation", use_container_width=True, key="sidebar_bank"):
                st.session_state.current_view = "bank_converter"
                st.rerun()
                
            if st.button("Journal Automation", use_container_width=True, key="sidebar_journal"):
                st.session_state.current_view = "journal_converter"
                st.rerun()
                
            if st.button("Settings", use_container_width=True, key="sidebar_settings"):
                st.session_state.current_view = "settings"
                st.rerun()

        st.divider()
        
        # User info and logout
        st.markdown(f"**User:** {st.session_state.email}")
        if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
            logout()
            st.rerun()
    
    # Route to appropriate page
    if st.session_state.current_view == "dashboard":
        render_dashboard_page()
    elif st.session_state.current_view == "bank_converter":
        render_bank_converter_page()
    elif st.session_state.current_view == "journal_converter":
        render_journal_converter_page()
    elif st.session_state.current_view == "settings":
        render_settings_page()
