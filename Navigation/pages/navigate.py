import streamlit as st
from PIL import Image, ImageDraw
import time
import config
from navigation import a_star
from location_finder import find_location
from mqtt_handler import mqtt_data

st.title("Navigation Mode")

# Load the image
map_image = Image.open('Map.png')
goal_icon = Image.open('icon_goal.png').convert("RGBA")

# Ensure 'end_point' is set in session state, otherwise return to home page
if "end_point" not in st.session_state:
    st.error("No destination set. Please go back and select a destination.")
    st.switch_page("main.py")

# Ensure 'current_location' exists in session state, initialize if not set
if "current_location" not in st.session_state:
    st.session_state.current_location = None

# Check if a path exists in session state, otherwise return to home page
if "path" not in st.session_state or not st.session_state.path:
    st.error("No path found. Returning to home page...")
    st.switch_page("main.py")

end_point = st.session_state.end_point  # Destination point
last_current_location = None  # Keep track of the last known location

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

def overlay_image(map_img, overlay_img, point_name, overlay_size=(50, 50)):
    overlay_resized = overlay_img.resize(overlay_size)
    x, y = config.COORDINATES[point_name]
    position = (x-25, y-50)
    map_with_overlay = map_img.copy()
    map_with_overlay.paste(overlay_resized, position, overlay_resized)
    return map_with_overlay

# Placeholder for real-time map updates
map_placeholder = st.empty()

# Button to stop navigation and return to the main page
if st.button("End Navigation"):
    st.session_state.navigating = False
    st.switch_page("main.py")

# Navigation logic - continuously updates the map until the user reaches the destination
if st.session_state.navigating:
    if st.session_state.current_location:
        while st.session_state.current_location != end_point:
            # Check if the current location has changed
            if st.session_state.current_location != last_current_location:
                # Recalculate the path based on the new current location
                st.session_state.path, st.session_state.dist = a_star(st.session_state.current_location, end_point)

                # Create a copy of the map and update it with navigation info
                map_copy = map_image.copy()
                draw_point(map_copy, st.session_state.current_location, 'blue')  # Mark current location
                if st.session_state.path:
                    draw_path(map_copy, st.session_state.path)  # Draw updated path
                map_copy = overlay_image(map_copy, goal_icon, end_point) # Mark destination

                # Update the placeholder with the new map
                map_placeholder.image(map_copy, use_container_width=True)
                st.write(f"Total Distance: {round(st.session_state.dist, 2)} meters")

                # Store the last known location to detect changes
                last_current_location = st.session_state.current_location

            # Update the current location based on the latest RSSI values from MQTT
            st.session_state.current_location = find_location(mqtt_data["RSSI1"],mqtt_data["RSSI2"],mqtt_data["RSSI3"])

            # Delay before checking for new location updates
            time.sleep(2)
            st.rerun()  # Force Streamlit to refresh and update the UI dynamically

    # Display a success message once the destination is reached
    st.success("Arrived at Destination!")
    st.session_state.navigating = False
    time.sleep(2)
    st.switch_page("main.py")
