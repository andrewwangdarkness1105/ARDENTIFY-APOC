import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- Hide sidebar ---
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="stSidebarCollapsedControl"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- Ribbon style ---
st.markdown("""
<style>
.ribbon-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background-color: rgba(255, 75, 75, 0.9);
    display: flex;
    align-items: center;
    padding-left: 20px;
    z-index: 9999;
}

/* Push content down */
.block-container {
    padding-top: 100px;
}
</style>
""", unsafe_allow_html=True)

# --- Ribbon buttons (aligned horizontally) ---
col1, col2, col3, col4, _ = st.columns([1,1,1,1,1])

with col1:
    if st.button("Home"):
        st.switch_page("index.py")

with col2:
    if st.button("About Us"):
        st.switch_page("pages/about us page.py")

with col3:
    if st.button("Upload Artifact"):
        st.switch_page("pages/upload info page.py")

with col4:
    if st.button("All Artifacts"):
        st.switch_page("pages/show all submissions.py")

# --- MAIN CONTENT ---
st.title("ARDENTIFY")
st.write("Welcome to the artifact scanner.")
