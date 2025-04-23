import streamlit as st
from PIL import Image, ImageDraw

st.title("Find Coordinate")

map_path = "Map_beacon.png"
x = st.number_input("X", min_value=0, max_value=1200, value=250)
y = st.number_input("Y", min_value=0, max_value=1200, value=250)

if st.button("Confirm"):

    img = Image.open(map_path)
    draw = ImageDraw.Draw(img)

    radius = 10
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='green', outline='black')

    st.image(img, caption=f"Coordinate: ({x}, {y})", use_container_width=True)
