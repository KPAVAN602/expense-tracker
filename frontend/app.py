import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# set_page_config MUST be the very first Streamlit command in the script
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)
#<----css Block----->
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #1B2A4A 0%, #3A5A7A 35%, #C9A08A 75%, #E8C9A8 100%);
    background-attachment: fixed;
}

/* Shrink the overall page padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* Glassmorphic form container - the "Ask anything" box look */
div[data-testid="stForm"] {
    background: rgba(20, 25, 40, 0.55);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 1.2rem 1.5rem;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    max-width: 480px;
    margin: 1rem auto 0.2rem auto;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Text inside the glass form should be light, since background is dark-ish */
div[data-testid="stForm"] label,
div[data-testid="stForm"] p {
    color: #F0F0F0 !important;
}

/* Inputs inside the glass card - subtle, not pure white */
div[data-testid="stForm"] input {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #F0F0F0 !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
}

/* Reduce space around the header text like "Login" */
div[data-testid="stForm"] h2,
div[data-testid="stForm"] h1 {
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
    padding: 0 !important;
}

/* Tighter spacing between every element on the page */
.element-container {
    margin-bottom: 0.2rem !important;
}

/* Tighter spacing specifically inside the form (label -> input -> button) */
div[data-testid="stForm"] .element-container {
    margin-bottom: 0.4rem !important;
}

/* Tighter gap after the form before the register/login prompt */
div[data-testid="stForm"] + div {
    margin-top: 0.2rem !important;
}

/* Metric cards - same glass treatment */
div[data-testid="stMetric"] {
    background: rgba(20, 25, 40, 0.45);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    padding: 1.2rem;
}
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricValue"] {
    color: #F0F0F0 !important;
}

/* Sidebar - dark glass panel */
section[data-testid="stSidebar"] {
    background: rgba(15, 20, 35, 0.7);
    backdrop-filter: blur(20px);
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: #F0F0F0 !important;
}

/* Headings - large, soft, centered like "Good morning, Pavan" */
h1 {
    color: #FFFFFF;
    font-weight: 600;
    text-align: center;
}

/* Rounded pill-style buttons, like Copilot's suggestion chips - default style */
.stButton button {
    background: rgba(255, 255, 255, 0.12);
    color: #F0F0F0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 24px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    backdrop-filter: blur(8px);
}
.stButton button:hover {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.35);
}

/* Override: "Login here" button specifically - black background */
.st-key-login_here_btn button {
    background-color: #000000 !important;
    color: #F0F0F0 !important;
    border: none !important;
    border-radius: 24px !important;
}
.st-key-login_here_btn button:hover {
    background-color: #1A1A1A !important;
}
</style>
""", unsafe_allow_html=True)
API_BASE =  "https://expense-tracker-2-nfwk.onrender.com"

st.title("Expense Tracker 💰")

# Initialize once
if 'token' not in st.session_state:
    st.session_state['token'] = None


def get_expenses(headers):
    response = requests.get(f"{API_BASE}/expenses", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def prepare_df(expenses):
    df = pd.DataFrame(expenses)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["month"] = df["created_at"].dt.strftime("%Y-%m")
    return df
# ============================================================
# LOGGED OUT: show login/register, nothing else
# ============================================================
if st.session_state['token'] is None:
 
    if 'auth_view' not in st.session_state:
        st.session_state['auth_view'] = 'login'   # default view
 
    # ---------------- LOGIN VIEW ----------------#
    if st.session_state['auth_view'] == 'login':
        with st.form("Login_Page"):
            st.header("Login")
            Email = st.text_input("Email")
            Password = st.text_input("Password", type="password")
            Login = st.form_submit_button("Login")
 
            if Login:
                response = requests.post(f"{API_BASE}/api/auth/Login",
                                          json={"Email": Email, "Password": Password})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state['token'] = data['access_token']
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password")
 
        st.markdown(
            "<p style='text-align:center; color:#F0F0F0; max-width:480px; margin:0.2rem auto;'>Don't have an account?</p>",
            unsafe_allow_html=True
        )
        _, mid, _ = st.columns([1.5, 1, 1.5])
        with mid:
            if st.button("Register here", key="login_here_btn",use_container_width=True):
                st.session_state['auth_view'] = 'register'
                st.rerun()
 
    # ---------------- REGISTER VIEW ----------------
    else:
        with st.form("Register_form"):
            st.header("Register")
            Name = st.text_input("Enter Your name")
            Email_reg = st.text_input("Enter your email")
            Password_reg = st.text_input("Password", type="password")
            register = st.form_submit_button("Register")
 
            if register:
                response = requests.post(f"{API_BASE}/api/auth/Register",
                                          json={"Name": Name, "Email": Email_reg, "Password": Password_reg})
                if response.status_code in [200, 201]:
                    st.success("User registered successfully — you can now log in.")
                    st.session_state['auth_view'] = 'login'
                    st.rerun()
                else:
                    st.error("Registration failed")
                    st.write(response.text)

        st.markdown(
        "<p style='text-align:center; color:#F0F0F0; max-width:480px; margin:0.2rem auto;'>Already have an account?</p>",
        unsafe_allow_html=True
    )
        _, mid, _ = st.columns([1.5, 1, 1.5])
        with mid:
            if st.button("Login here", key="login_here_btn",use_container_width=True):     
                st.session_state['auth_view'] = 'login'
                st.rerun()
# ============================================================
# LOGGED IN: sidebar navigation + all expense features
# ============================================================
else:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    st.sidebar.title("Menu")
    option = st.sidebar.selectbox(
        "Choose an option",
        [
            "Dashboard",
            "Add Expense",
            "View Expense",
            "Update Expense",
            "Delete Expense",
            "About"
        ],
        key="nav_option"
    )

    if st.sidebar.button("Logout"):
        st.session_state['token'] = None
        st.rerun()

    # ---------------- Dashboard ----------------
    if option == "Dashboard":
        st.header("Dashboard 📊")
        st.subheader("Welcome To Dashboard 👋")
 
        expenses = get_expenses(headers)
        if expenses:
            df = prepare_df(expenses)                # <-- use the helper here
            total_amount = df["amount"].sum()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Expenses", len(df))
            with col2:
                st.metric("Total Amount", f"₹{total_amount:.2f}")
 
            summary = df.groupby("category", as_index=False)["amount"].sum()
 
            pie_fig = px.pie(summary, names="category", values="amount",
                             title="Expense share by category")
            bar_fig = px.bar(summary, x="category", y="amount", color="category",
                             title="Total spent by category", text_auto=True,
                             labels={"amount": "Amount (₹)", "category": "Category"})
            bar_fig.update_layout(showlegend=False)
 
            chart_col1, chart_col2 = st.columns(2)
            chart_col1.plotly_chart(pie_fig, use_container_width="stretch")
            chart_col2.plotly_chart(bar_fig, use_container_width="stretch")
 
            # --- Line chart: spending over time (all months) ---
            monthly = (
                df.dropna(subset=["month"])
                .groupby("month", as_index=False)["amount"].sum()
                .sort_values("month")
            )

            if not monthly.empty:
                trend_fig = go.Figure()
                trend_fig.add_trace(go.Bar(
                    x=monthly["month"],
                    y=monthly["amount"],
                    marker=dict(
                        color="#4FD1A5",
                        line=dict(color="#F0F0F0", width=0.5)
                    ),
                    text=monthly["amount"].apply(lambda x: f"₹{x:,.0f}"),
                    textposition="outside",
                    textfont=dict(color="#F0F0F0"),
                    hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>"
                ))
                trend_fig.update_layout(
                    title=dict(text="Monthly Spending Trend", font=dict(size=20, color="#F0F0F0")),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#F0F0F0"),
                    xaxis=dict(showgrid=False, color="#F0F0F0"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="#F0F0F0", title="Amount (₹)"),
                    margin=dict(l=20, r=20, t=60, b=40),
                    bargap=0.4,   # thinner bars look better with few data points, avoids a bulky look
                )
                st.plotly_chart(trend_fig, use_container_width=True,width="stretch" )


                st.subheader("🧾 Recent expenses")
                st.dataframe(df, use_container_width="stretch")
 
        else:
            st.info("No expenses found yet — add one to get started.")

    # ---------------- Add Expense ----------------
    elif option == "Add Expense":
        with st.form("add_expense_form"):
            st.header("Add Expense")
            title = st.text_input("Enter expense item")
            category = st.selectbox("Select category",
                                     ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"],
                                     key="add_cat")
            amount = st.number_input("Enter Amount (₹)", min_value=0.0)
            Add_expense = st.form_submit_button("Add Expense")

            if Add_expense:
                expense = {"category": category, "title": title, "amount": amount}
                response = requests.post(f"{API_BASE}/expenses", json=expense, headers=headers)
                if response.status_code == 201:
                    st.success("Expense added successfully")
                else:
                    st.error("Failed to add expense")
                    st.write(response.text)

    # ---------------- View Expenses ----------------
    elif option == "View Expense":
        st.header("View Expenses 🔎")
        expenses = get_expenses(headers)
 
        if not expenses:
            st.info("No expenses found.")
        else:
            df = prepare_df(expenses)
            # --- Filter controls ---
            col1, col2 = st.columns(2)
            with col1:
                title_search = st.text_input("Search by title", key="filter_title")
            with col2:
                categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
                category_filter = st.selectbox("Filter by category", categories, key="filter_cat")
 
            col3, col4 = st.columns(2)
            with col3:
                min_amt = float(df["amount"].min())
                max_amt = float(df["amount"].max())
                amount_range = st.slider(
                    "Total amount range (₹)",
                    min_value=min_amt, max_value=max_amt,
                    value=(min_amt, max_amt),
                    key="filter_amount"
                )
            with col4:
                valid_dates = df["created_at"].dropna()
                if not valid_dates.empty:
                    min_date = valid_dates.min().date()
                    max_date = valid_dates.max().date()
                    date_range = st.date_input(
                        "Date range",
                        value=(min_date, max_date),
                        min_value=min_date, max_value=max_date,
                        key="filter_date"
                    )
                else:
                    date_range = None
                    st.write("No dates available to filter by")
 
            # --- Apply filters ---
            filtered = df.copy()
 
            if title_search:
                filtered = filtered[filtered["title"].str.contains(title_search, case=False, na=False)]
 
            if category_filter != "All":
                filtered = filtered[filtered["category"] == category_filter]
 
            filtered = filtered[
                (filtered["amount"] >= amount_range[0]) &
                (filtered["amount"] <= amount_range[1])
            ]
 
            if date_range and isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                filtered = filtered[
                    (filtered["created_at"].dt.date >= start_date) &
                    (filtered["created_at"].dt.date <= end_date)
                ]
 
            st.divider()
            st.subheader(f"Results: {len(filtered)} expense(s)")
 
            if not filtered.empty:
                st.metric("Total (filtered)", f"₹{filtered['amount'].sum():.2f}")
                st.dataframe(filtered, use_container_width=True)
            else:
                st.warning("No expenses match these filters.")
 

    # ---------------- Update Complete Expense (PUT) ----------------
    elif option == "Update Expense":
        with st.form("put_expense_form"):
            st.header("Update Expense")
            expense_id = st.number_input("Expense id", min_value=1, step=1, key="put_id")
            category = st.selectbox("Select Category",
                                     ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"],
                                     key="put_cat")
            title = st.text_input("Enter expense item", key="put_title")
            amount = st.number_input("New Amount (₹)", min_value=0.0, key="put_amount")
            update_expense = st.form_submit_button("Update Expense")

            if update_expense:
                update_data = {"category": category, "title": title, "amount": amount}
                response = requests.put(f"{API_BASE}/expenses/{int(expense_id)}",
                                         json=update_data, headers=headers)
                if response.status_code == 200:
                    st.success("Expense fully updated")
                else:
                    st.error("Failed to update  expense")
                    st.write(response.text)

    # ---------------- Delete Expense ----------------
    elif option == "Delete Expense":
        with st.form("delete_expense"):
            st.header("Delete Expense")
            expense_id = st.number_input("Enter Expense ID to delete", min_value=1, step=1)
            delete_expense = st.form_submit_button("Delete Expense")

            if delete_expense:
                response = requests.delete(f"{API_BASE}/expenses/{int(expense_id)}", headers=headers)
                if response.status_code == 200:
                    st.success("Expense deleted successfully")
                else:
                    st.error("Failed to delete expense")
                    st.write(response.text)
        # ---------------- About ----------------
    elif option == "About":
        st.markdown("""
        <div style="
            background: rgba(20, 25, 40, 0.55);
            backdrop-filter: blur(16px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 2rem 2.5rem;
            max-width: 600px;
            margin: 1rem auto;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        ">
            <h2 style="color:#F0F0F0; margin-top:0;">About This Project</h2>
            <p style="color:#C9CDD3; font-size:1.05rem;">A secure full-stack expense tracker that helps you add, track, and analyze your spending — built with Flask, MySQL, and Streamlit.</p>
            <hr style="border-color: rgba(255,255,255,0.15); margin: 1rem 0;">
            <p style="color:#F0F0F0;"><b>🎯 Purpose</b><br>
            Most people don't track their spending until it's already a problem — receipts pile up, 
            expenses blend together, and by month-end it's hard to say where the money actually went. 
            This project was built to change that: a simple, secure space to log expenses as they happen 
        and see your spending patterns clearly, so budgeting feels less like guesswork.</p>
        <hr style="border-color: rgba(255,255,255,0.15); margin: 1rem 0;">
            <p style="color:#F0F0F0;"><b>👤 Developer</b><br>Pavan Kalyan K</p>
            <p style="color:#F0F0F0;"><b>🛠️ Tech Stack</b><br>Python · Flask · MySQL · Streamlit · JWT Authentication</p>
            <p style="color:#F0F0F0;"><b>✨ Features</b></p>
            <ul style="color:#C9CDD3; line-height:1.8;">
                <li>Secure login &amp; registration</li>
                <li>Add, view, update, and delete expenses</li>
                <li>Category-wise spending breakdown</li>
                <li>Monthly spending trend visualization</li>
            </ul>
            <hr style="border-color: rgba(255,255,255,0.15); margin: 1rem 0;">
            <p style="color:#F0F0F0;">
                📧 <a href="mailto:kpavankalyan648@gmail.com" style="color:#4FD1A5;">kpavankalyan648@gmail.com</a><br>
                🔗 <a href="https://github.com/KPAVAN602" style="color:#4FD1A5;" target="_blank">GitHub</a>
                &nbsp;|&nbsp;
                <a href="https://linkedin.com/in/komkonipavan" style="color:#4FD1A5;" target="_blank">LinkedIn</a>
            </p>
        </div>
        """, unsafe_allow_html=True)