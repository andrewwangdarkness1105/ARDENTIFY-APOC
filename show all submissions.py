import streamlit as st
import csv
import os
from PIL import Image

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



st.set_page_config(layout="wide")
st.title("All Submitted Artifacts")
st.subheader("View all contributions to ARDENTIFY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "../submissions.csv")

if not os.path.exists(CSV_FILE):
    st.warning("No submissions found yet.")
else:
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        st.info("No submissions yet.")
    else:
        for row in rows:
            st.markdown("---")
            st.write(f"**Timestamp:** {row.get('timestamp', '')}")
            st.write(f"**Name:** {row.get('name','')}")
            st.write(f"**Primary Contact:** {row.get('primary_contact','')}")
            st.write(f"**Secondary Contact:** {row.get('secondary_contact','')}")
            st.write(f"**Location / Digsite:** {row.get('location','')}")
            st.write(f"**Organisation:** {row.get('organisation','')}")
            st.write(f"**Prediction:** {row.get('prediction','')}")
            st.write(f"**Confidence:** {row.get('confidence','')}")

            # Show image if exists
            img_path = row.get('image_path', '')
            if img_path:
                full_path = os.path.join(BASE_DIR, "..", img_path)
                if os.path.exists(full_path):
                    st.image(full_path, use_container_width=True)
                else:
                    st.write("Image not found.")

# Optional: download CSV
with open(CSV_FILE, "rb") as f:
    st.download_button("Download all submissions", f.read(), "submissions.csv", "text/csv")
