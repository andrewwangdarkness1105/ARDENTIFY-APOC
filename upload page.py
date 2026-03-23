import streamlit as st
from PIL import Image

def first():  st.session_state = 0

def start():
    st.title("ARDENTIFY")
    st.subheader("Image upload")
    st.write("upload image of artifact")

def endpage():
    st.title("Thank you for contributing to the wider archeology community!!!")
    st.button("submit again", key=None, help=None, on_click=first(), args=None, kwargs=None, type="secondary", icon=None, disabled=False, use_container_width=None, width="content")

def main():
    start()
    File = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    if File is not None:
            image = Image.open(File)
            st.image(image, caption=None, width="content", use_column_width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=None)
            st.text_input("Name", value="", max_chars=45, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
            st.text_input("Primary contact details", value="", max_chars=45, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
            st.text_input("Secondary contact details", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")       
            st.text_input("Country and address of digsite/find", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
            st.text_input("Company/organisation", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
            end = st.button("Submit", key=None, help=None, on_click=None, args=None, kwargs=None, type="secondary", icon=None, disabled=False, use_container_width=None, width="content")  

main()

