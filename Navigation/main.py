import streamlit as st
from PIL import Image, ImageDraw
import config
from navigation import a_star
from location_finder import find_location
from mqtt_handler import start_mqtt, mqtt_data, stop_mqtt
import time

# Start MQTT Client
if 'mqtt_started' not in st.session_state:
    stop_mqtt()
    time.sleep(1)
    start_mqtt()
    st.session_state.mqtt_started = True

# Initialize session state
if 'current_location' not in st.session_state:
    st.session_state.current_location = None
if 'path' not in st.session_state:
    st.session_state.path = []
if 'dist' not in st.session_state:
    st.session_state.dist = 0
if 'navigating' not in st.session_state:
    st.session_state.navigating = False
if 'end_point' not in st.session_state:
    st.session_state.end_point = None

# Hide sidebar
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Page title
st.title("Indoor Navigation")

# Load image
map_image = Image.open('map.png')
goal_icon = Image.open('icon_goal.png').convert("RGBA")
beacon_icon = Image.open('icon_beacon.png').convert("RGBA")

# Dropdown options
locations = list(config.FULL_NAMES.keys())

# Select start and end points
start_point = st.selectbox("Select Starting Point:", locations, key='start')
end_point = st.selectbox("Select Destination:", [loc for loc in locations if loc != start_point], key='end')

start_point = config.FULL_NAMES[start_point]
end_point = config.FULL_NAMES[end_point]

# Create a toggle switch
toggle = st.checkbox("Show Beacons")

# Make a copy to draw
map_copy = map_image.copy()

# Functions to draw on the map
def draw_point(image, point_name, color='red'):
    draw = ImageDraw.Draw(image)
    x, y = config.COORDINATES[point_name]
    radius = 10
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)

def draw_path(image, path, color='blue'):
    draw = ImageDraw.Draw(image)
    for i in range(len(path) - 1):
        start = config.COORDINATES[path[i]]
        end = config.COORDINATES[path[i + 1]]
        # Check for special path points
        if (path[i], path[i + 1]) in config.PATH_POINTS:
            mid = config.PATH_POINTS[(path[i], path[i + 1])]
            draw.line((start, mid), fill=color, width=5)
            draw.line((mid, end), fill=color, width=5)
        elif (path[i + 1], path[i]) in config.PATH_POINTS:
            mid = config.PATH_POINTS[(path[i + 1], path[i])]
            draw.line((start, mid), fill=color, width=5)
            draw.line((mid, end), fill=color, width=5)
        else:
            draw.line((start, end), fill=color, width=5)

def overlay_image(map_img, overlay_img, point_name, diff_x=0, diff_y=0, overlay_size=(50, 50)):
    overlay_resized = overlay_img.resize(overlay_size)
    x, y = config.COORDINATES[point_name]
    position = (x+diff_x, y+diff_y)
    map_with_overlay = map_img.copy()
    map_with_overlay.paste(overlay_resized, position, overlay_resized)
    return map_with_overlay

# Find current location
if start_point == 'Current Location' or end_point == 'Current Location':
    if mqtt_data["RSSI1"] and mqtt_data["RSSI2"] and mqtt_data["RSSI3"]:
        st.session_state.current_location = find_location(mqtt_data["RSSI1"], mqtt_data["RSSI2"], mqtt_data["RSSI3"])
        st.write(f"Current Location: {st.session_state.current_location}")
    else:
        st.write("Waiting for current location data...")

# Show path
if start_point and end_point and start_point != end_point:
    if start_point == 'Current Location' and st.session_state.current_location:
        st.session_state.path, st.session_state.dist = a_star(st.session_state.current_location, end_point)
    elif end_point == 'Current Location' and st.session_state.current_location:
        st.session_state.path, st.session_state.dist = a_star(start_point, st.session_state.current_location)
    else:
        st.session_state.path, st.session_state.dist = a_star(start_point, end_point)

# Start navigation button
if start_point == 'Current Location' and st.session_state.path:
    if st.button("Start Navigation"):
        st.session_state.navigating = True
        st.session_state.end_point = end_point
        st.switch_page("pages/navigate.py")

# Toggle box
if toggle:
    draw_point(map_copy, 'Beacon1', '#2980b9')
    map_copy = overlay_image(map_copy, beacon_icon, 'Beacon1', -15, -50, (40,40))
    draw_point(map_copy, 'Beacon2', '#2980b9')
    map_copy = overlay_image(map_copy, beacon_icon, 'Beacon2', -20, 10, (40,40))
    draw_point(map_copy, 'Beacon3', '#2980b9')
    map_copy = overlay_image(map_copy, beacon_icon, 'Beacon3', -32, -50, (40,40))

if not st.session_state.navigating:
    if start_point == 'Current Location' and st.session_state.current_location:
        draw_point(map_copy, st.session_state.current_location, 'blue')
    else:
        draw_point(map_copy, start_point, 'blue')
    if st.session_state.path:
        draw_path(map_copy, st.session_state.path)

    if end_point == 'Current Location' and st.session_state.current_location:
        map_copy = overlay_image(map_copy, goal_icon, st.session_state.current_location)
    else:
        map_copy = overlay_image(map_copy, goal_icon, end_point, -25, -50)
st.image(map_copy, use_container_width=True)
st.write(f"Total Distance: {round(st.session_state.dist,2)} meters")
