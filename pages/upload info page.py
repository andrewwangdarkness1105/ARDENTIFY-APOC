import streamlit as st
from PIL import Image
import torch
import numpy as np
import cv2
import logging
import traceback
import csv
import os
from datetime import datetime

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



# ------------------ HIDE SIDEBAR ------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="stSidebarCollapsedControl"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ------------------ RIBBON ------------------
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
.block-container {padding-top: 100px;}
</style>
""", unsafe_allow_html=True)

# ---------------- CONFIG ----------------
MODEL_PATH = "/Users/andrewwang/Desktop/ancientartifact_model_v6.pt"
INPUT_SIZE = 64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "../submissions.csv")
IMAGE_DIR = os.path.join(BASE_DIR, "../uploaded_images")
os.makedirs(IMAGE_DIR, exist_ok=True)

logging.getLogger("ultralytics").setLevel(logging.WARNING)
logging.getLogger("torch").setLevel(logging.WARNING)

# ---------------- CLASS NAMES ----------------
class_names = {
    0: "Ankh", 1: "Arrowheads", 2: "Boomerang", 3: "Canopic Jar", 4: "Coins",
    5: "Papyrus", 6: "Pottery Shards", 7: "Scarab", 8: "Shields", 9: "Skull",
    10: "Sword", 11: "Tablet", 12: "Terracotta Statue",
}

# ---------------- DEVICE ----------------
def choose_device():
    if torch.backends.mps.is_available(): return "mps"
    if torch.cuda.is_available(): return "cuda"
    return "cpu"

# ---------------- ARTIFACT CLASSIFIER ----------------
class ArtifactClassifier:
    def __init__(self, model_path: str, device: str, input_size: int = 224):
        self.device = device
        self.input_size = input_size
        self.model = torch.jit.load(model_path, map_location=self.device)
        self.model.eval()
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def preprocess(self, frame: np.ndarray) -> torch.Tensor:
        resized = cv2.resize(frame, (self.input_size, self.input_size))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img = rgb.astype(np.float32) / 255.0
        img = (img - self.mean) / self.std
        img = np.transpose(img, (2, 0, 1))
        return torch.from_numpy(img).unsqueeze(0).to(self.device)

    def predict(self, frame: np.ndarray):
        inp = self.preprocess(frame)
        with torch.no_grad():
            out = self.model(inp)
        if isinstance(out, (list, tuple)): out = out[0]
        if isinstance(out, dict): out = list(out.values())[0]
        if out.dim() == 1: out = out.unsqueeze(0)
        probs = torch.softmax(out, dim=1)
        conf, idx = torch.max(probs, dim=1)
        return int(idx.item()), float(conf.item())

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    device = choose_device()
    return ArtifactClassifier(MODEL_PATH, device, INPUT_SIZE)

classifier = load_model()

# ---------------- SAVE FUNCTION ----------------
def save_submission(data, image_obj):
    # Save image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{data['name'].replace(' ', '_')}.png"
    image_path = os.path.join(IMAGE_DIR, filename)
    image_obj.save(image_path)
    data['image_path'] = os.path.relpath(image_path, BASE_DIR)

    # Save CSV
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists: writer.writeheader()
        writer.writerow(data)

# ---------------- SESSION STATE ----------------
if "submitted" not in st.session_state: st.session_state.submitted = False

# ---------------- UI ----------------
def show_thank_you():
    st.title("Thank you for contributing to ARDENTIFY.")
    st.subheader("Each upload counts.")
    if st.button("Upload Again"):
        st.session_state.submitted = False
        st.rerun()

def show_form():
    st.title("ARDENTIFY")
    st.subheader("Image upload")
    st.write("Upload image of artifact")

    File = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    class_name = None
    conf = None

    if File is not None:
        image = Image.open(File).convert("RGB")
        st.image(image, use_container_width=True)
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        try:
            idx, conf = classifier.predict(frame)
            class_name = class_names.get(idx, f"cls_{idx}")
            st.success(f"Prediction: {class_name}")
            st.write(f"Confidence: {conf*100:.2f}%")
        except Exception:
            st.error("Prediction failed")
            traceback.print_exc()

    # INPUT FIELDS
    name = st.text_input("Name", max_chars=45)
    primary_contact = st.text_input("Primary contact details", max_chars=45)
    secondary_contact = st.text_input("Secondary contact details")
    location = st.text_input("Country and address of digsite/find")
    organisation = st.text_input("Company/organisation")

    if st.button("Submit") and File is not None:
        submission = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "primary_contact": primary_contact,
            "secondary_contact": secondary_contact,
            "location": location,
            "organisation": organisation,
            "prediction": class_name if class_name else "None",
            "confidence": f"{conf*100:.2f}%" if conf else "N/A"
        }
        save_submission(submission, image)
        st.success(f"Saved submission to: {CSV_FILE}")
        st.session_state.submitted = True
        st.rerun()

# ---------------- MAIN ----------------
if st.session_state.submitted:
    show_thank_you()
else:
    show_form()
