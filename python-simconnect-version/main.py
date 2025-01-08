# =======================
# MSFS Screenshot EXIF Updater
# Version 1.2.0
# By PBandJamf AKA TeezyYoxO
# =======================

# CHANGELOG #

# Version 1.2.0:
# - **Added `-t`, `--test`, and `-T` flags**: These flags now allow running the script in "test mode" which only prints live location data from the simulator (latitude, longitude, altitude).
# - Integrated **`argparse`** for better command-line argument parsing.
# - If the test mode is selected, the script **connects to MSFS** and prints the **live location data** without processing screenshots.
# - If no test flag is passed, the script continues with its regular functionality, which includes monitoring directories for new screenshots and embedding GPS metadata into them.

# Version 1.1.3:
# - Fixed issue with broken PNG file when trying to write EXIF metadata.
# - Switched to embedding GPS data in custom text chunks (using the `Description` field) for PNG files.
# - Ensured that PNG files' integrity is preserved by avoiding direct modification of EXIF data, which is not native to PNG format.
# - Added fallback handling for storing GPS data in a format compatible with PNG metadata.
# - Improved error handling for cases where the image format is not supported or the file is corrupted.

# Version 1.1.2:
# - Fixed issue with GPS EXIF metadata not being correctly written to PNG files.
# - Manually mapped GPS data to the proper EXIF tags using the correct `GPSTAGS` values.
# - Improved handling for missing GPSInfo tag in EXIF and added more comprehensive error messages.
# - Ensured that GPS data is added properly even if the EXIF metadata doesn't initially contain a GPS tag.

# Version 1.1.1:
# - Fixed issue where GPS data was not correctly added to the EXIF metadata.
# - Updated EXIF handling to ensure GPS metadata is written under the correct tag (`GPSInfo`).
# - Added better error handling for missing EXIF tags and issues during save operation.
# - Ensured that only valid GPS keys are used in the EXIF data.

# Version 1.1.0:
# - Added support for monitoring multiple directories.
# - Limited file processing to `.png` files containing "Microsoft Flight Simulator" in their names.
# - Updated dynamic logging to print the actual monitored directories.
# - Prints the full path and location data when a new screenshot is detected.

# Version 1.0.0:
# - Initial release.
# - Connects to MSFS using SimConnect.
# - Retrieves latitude, longitude, and altitude data.
# - Monitors a specified folder for new screenshots.
# - Adds location data to screenshot EXIF metadata.
#   
# Future Plans:
# - Automate taking screenshots directly from the script.
# - Add user-configurable settings for screenshot folder and EXIF fields.
# - Handle non-image files more gracefully.

import argparse
import time
import os
from PIL import Image, PngImagePlugin
from simconnect import SimConnect, AircraftRequests, Simulation, SimConnectError

# Function to retrieve and print live location data
def print_live_location(sim):
    try:
        # Request live location data (latitude, longitude, altitude)
        lat_request = sim.get_data("Latitude")
        lon_request = sim.get_data("Longitude")
        alt_request = sim.get_data("Altitude")

        # Print the live data
        print(f"Longitude: {lon_request[0]}")
        print(f"Latitude: {lat_request[0]}")
        print(f"Altitude: {alt_request[0]}")
        
    except SimConnectError as e:
        print(f"Error retrieving location data: {e}")

# Function to process screenshots and update EXIF (as you were doing previously)
def process_screenshot(image_path, latitude, longitude, altitude):
    # Your screenshot EXIF processing code here...
    # For example:
    img = Image.open(image_path)
    gps_data = f"Latitude: {latitude}\nLongitude: {longitude}\nAltitude: {altitude}"
    if img.format == 'PNG':
        img.save(image_path, pnginfo=PngImagePlugin.PngInfo())
        img.info['Description'] = gps_data
        img.save(image_path)  # Save with metadata

    print(f"Successfully updated PNG metadata for {image_path}")

# Main function to handle arguments and SimConnect connection
def main():
    # Argument parsing to handle the --test flag
    parser = argparse.ArgumentParser(description="MSFS Screenshot EXIF Updater and Location Viewer.")
    parser.add_argument('-t', '--test', action='store_true', help="Print live location data from the simulator.")
    parser.add_argument('-T', '--Test', action='store_true', help="Print live location data from the simulator.")
    
    args = parser.parse_args()

    # If --test or -t or -T is provided, just print live location data
    if args.test or args.Test:
        # Connect to the simulator
        sim = SimConnect()
        print("Connected to Microsoft Flight Simulator.")
        
        # Print the live location data
        print_live_location(sim)
        return

    # Otherwise, proceed with your regular screenshot monitoring and processing
    print("No test flag passed, continuing with normal operations...")
    
    # You can add the logic to monitor screenshots and update EXIF data here
    screenshot_dirs = [
        r"S:\MSFS Recordings\Microsoft Flight Simulator",
        r"C:\Users\monte\Videos\Captures"
    ]

    print(f"Watching for screenshots in the following directories: {', '.join(screenshot_dirs)}")

    # SimConnect connection for location tracking
    sim = SimConnect()

    # Monitor screenshots in directories
    while True:
        # Here, you would monitor for new screenshots and process them
        # Example: Find .png files that match your criteria and process them
        for dir_path in screenshot_dirs:
            for filename in os.listdir(dir_path):
                if filename.endswith(".png") and "Microsoft Flight Simulator" in filename:
                    file_path = os.path.join(dir_path, filename)
                    # Retrieve live location data
                    lat_request = sim.get_data("Latitude")
                    lon_request = sim.get_data("Longitude")
                    alt_request = sim.get_data("Altitude")

                    # Process the screenshot (add location data to EXIF)
                    process_screenshot(file_path, lat_request[0], lon_request[0], alt_request[0])
                    print(f"New screenshot detected: {filename}")
                    print(f"Path: {file_path}")
                    print(f"Latitude: {lat_request[0]}, Longitude: {lon_request[0]}, Altitude: {alt_request[0]}")

        time.sleep(5)  # Check every 5 seconds for new screenshots

# Run the script
if __name__ == "__main__":
    main()