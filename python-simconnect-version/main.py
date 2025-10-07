"""
=======================
 GeoShottr - Geotag your flightsim screenshots!
 By PBandJamf AKA TeezyYoxO
 =======================
"""



## BEGIN! ##
version = "1.7.5a"
import os
import sys
import time
from time import sleep
from SimConnect import SimConnect, AircraftRequests
from PIL import Image
import piexif
import pystray
from pystray import MenuItem as item
from threading import Thread, Event

# Add a global event flag for clean thread termination
stop_event = Event()
# this is the delay before writing the file to disk, to ensure all data is ready, to avoid the "image is truncated" error
# adjust this as needed
FILE_WRITE_DELAY_SECONDS = 3

# === Console Colors ===
RESET = "\033[0m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"

# Bugfix: Ensure that the script can handle missing or malformed data gracefully
def safe_format(value, fmt="{:.6f}", default="N/A"):
    try:
        return fmt.format(value)
    except (ValueError, TypeError):
        return default

# Helper function to get the correct path to bundled resources
def resource_path(relative_path):
    """ Get the correct path to a resource, whether running in a bundled exe or from source code. """
    try:
        # PyInstaller creates a temp folder for bundled resources
        base_path = sys._MEIPASS
    except Exception:
        # If not running from a bundled exe, use the current directory
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Function to convert to decimal degrees from DMS (degrees, minutes, seconds)
def convert_to_decimal_degrees(dms):
    degrees, minutes, seconds = dms
    return degrees + (minutes / 60) + (seconds / 3600)

# Function to create GPSInfo for EXIF
def create_gps_info(latitude, longitude, altitude):
    def convert_to_dms(value):
        d = int(value)
        m = int((value - d) * 60)
        s = (value - d - m / 60) * 3600
        return (d, m, s)

    lat_dms = convert_to_dms(abs(latitude))
    lon_dms = convert_to_dms(abs(longitude))

    # Convert DMS to decimal degrees for EXIF
    latitude_decimal = convert_to_decimal_degrees(lat_dms)
    longitude_decimal = convert_to_decimal_degrees(lon_dms)

    return {
        'GPSLatitude': [(lat_dms[0], 1), (lat_dms[1], 1), (int(lat_dms[2] * 10000), 10000)],
        'GPSLatitudeRef': 'N' if latitude >= 0 else 'S',
        'GPSLongitude': [(lon_dms[0], 1), (lon_dms[1], 1), (int(lon_dms[2] * 10000), 10000)],
        'GPSLongitudeRef': 'E' if longitude >= 0 else 'W',
        'GPSAltitude': (int(altitude * 100), 100),
        'GPSAltitudeRef': 0,  # Above sea level
        'GPSLatitudeDecimal': latitude_decimal,
        'GPSLongitudeDecimal': longitude_decimal
    }

# Edit image EXIF and save as JPEG in a subfolder, handle errors gracefully
def add_location_to_exif(image_path, latitude, longitude, altitude):
    img = Image.open(image_path)

    # Format the Description correctly
    description = f"Longitude: {longitude} | Latitude: {latitude} | Altitude: {altitude} (feet)"

    try:
        # Create subfolder "Geotagged" if it doesn't exist
        geotagged_folder = os.path.join(os.path.dirname(image_path), "Geotagged")
        os.makedirs(geotagged_folder, exist_ok=True)

        # Check if the image is PNG and convert to JPEG
        if img.format == 'PNG':
            # Create a new JPEG image in the Geotagged folder
            jpeg_path = os.path.join(geotagged_folder, os.path.basename(image_path).replace('.png', '.jpg'))
            img.convert('RGB').save(jpeg_path, 'JPEG')
            print(f"[✅ SAVED] JPEG created: {jpeg_path}")

            # Add the description to the JPEG image
            img = Image.open(jpeg_path)

            # Create a new EXIF structure as there's no existing EXIF
            exif_dict = {
                "0th": {piexif.ImageIFD.Make: "Microsoft Flight Simulator", piexif.ImageIFD.Model: "Screenshot"},
                "GPS": {}
            }

            # Add the GPS data to the EXIF
            gps_info = create_gps_info(latitude, longitude, altitude)
            exif_dict['GPS'] = {piexif.GPSIFD.GPSLatitude: gps_info['GPSLatitude'],
                                piexif.GPSIFD.GPSLongitude: gps_info['GPSLongitude'],
                                piexif.GPSIFD.GPSAltitude: gps_info['GPSAltitude'],
                                piexif.GPSIFD.GPSLatitudeRef: gps_info['GPSLatitudeRef'],
                                piexif.GPSIFD.GPSLongitudeRef: gps_info['GPSLongitudeRef']}

            # Convert EXIF data back to bytes and save the image
            exif_bytes = piexif.dump(exif_dict)
            img.save(jpeg_path, "JPEG", quality=100, optimize=False, subsampling=0, exif=exif_bytes)
            print(f"[🛰️  GEO] EXIF updated with location metadata.")

        else:
            # If not PNG, just print the location info
            print(f"No conversion needed for {image_path}, skipping.")
            print(f"Description: {description}")

    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Failed to save metadata for {image_path}: {e}")

# Main function to retrieve data and update EXIF
def main():
    try:
        # Connect to MSFS SimConnect
        sm = SimConnect()
        aq = AircraftRequests(sm)
        print("\n🛰️  GeoShottr initialized")
        print(f"Version: {version}")
        print("-----------------------------------------------------\n")
        print("{GREEN}[🛫 CONNECTED]{GREEN} Microsoft Flight Simulator detected.")

        # Specify folders to monitor
        screenshot_dirs = [
            r"C:\Users\monte\Videos\Captures",
            r"C:\Users\monte\Videos\NVIDIA\Microsoft Flight Simulator 2024",
            r"C:\Users\monte\Videos\NVIDIA\Microsoft Flight Simulator" # Updated path for MSFS screenshots
        ]
        print("[📂 MONITORING] Screenshot folders:")
        for path in screenshot_dirs:
            print(f"   • {path}")
            print("-----------------------------------------------------")
            print("Waiting for screenshots...")

        # Initialize tracking of existing files in each directory
        existing_files = {dir_path: set(os.listdir(dir_path)) for dir_path in screenshot_dirs}

        while not stop_event.is_set():  # Graceful exit condition
            for dir_path in screenshot_dirs:
                # Get current files in the directory
                current_files = set(os.listdir(dir_path))
                new_files = current_files - existing_files[dir_path]

                for new_file in new_files:
                    # Check if the file is a PNG and contains "Microsoft Flight Simulator"
                    if new_file.lower().endswith(".png") and "Microsoft Flight Simulator" in new_file:
                        screenshot_path = os.path.join(dir_path, new_file)

                        # Check for Super-Resolution images based on filename and size
                        if "Super-Resolution" in new_file or os.path.getsize(screenshot_path) > 10 * 1024 * 1024:
                            print(f"\n[🖼️  DETECTED] High-res screenshot: {new_file}")
                        else:
                            print(f"\n[🖼️  DETECTED] Screenshot: {new_file}")
                        # Try to get valid telemetry up to 5 times with short delay
                        max_attempts = 3
                        for attempt in range(max_attempts):
                            latitude = aq.get("PLANE_LATITUDE")
                            longitude = aq.get("PLANE_LONGITUDE")
                            altitude = aq.get("PLANE_ALTITUDE")
                            if None not in (latitude, longitude, altitude):
                                break
                            time.sleep(0.3)  # Wait briefly before retrying

                        if None in (latitude, longitude, altitude):
                            print(f"{RED}[ERROR]{RESET} One or more telemetry values are missing (Lat: {latitude}, Lon: {longitude}, Alt: {altitude}). Skipping.")
                            continue
                        print(f"[📍 LOCATION] Lat: {safe_format(latitude)} | Lon: {safe_format(longitude)} | Alt: {safe_format(altitude, '{:.0f}')} ft")
                        print(f"[📁 SOURCE]   {screenshot_path}")
                        time.sleep(FILE_WRITE_DELAY_SECONDS)

                        # Add location data to EXIF and save as JPEG
                        add_location_to_exif(screenshot_path, latitude, longitude, altitude)

                # Update the file set for the directory
                existing_files[dir_path] = current_files

            sleep(1)

    except KeyboardInterrupt:
        print("Exiting gracefully...")
        stop_event.set()  # Signal the thread to exit
    except Exception as e:
        print(f"{RED}[ERROR]{RED} An error occurred: {e}")

# Function to quit the application
def quit_action(icon, item):
    stop_event.set()  # Set the stop event to signal the thread to stop
    icon.stop()

# Function to run the system tray icon
def create_system_tray_icon():
    print("[📌 TRAY] Initializing system tray icon...")
    icon_image = Image.open(r"C:\Users\monte\Documents\GitHub\geoshottr\images\geoshottr.ico")
    icon = pystray.Icon("GeoShottr", icon_image, menu=pystray.Menu(
        item('Quit', quit_action)
    ))

    thread = Thread(target=main, daemon=True)
    thread.start()
    print("[🔄 THREAD] Screenshot monitoring started.")
    
    icon.run_detached()
    return icon

# handle application exit gracefully
if __name__ == "__main__":
    tray_icon = create_system_tray_icon()
    
    try:
        while not stop_event.is_set():
            sleep(1)
    except KeyboardInterrupt:
        print("\n[🔻 EXIT] Ctrl+C received. Stopping GeoShottr...")
        stop_event.set()
        tray_icon.stop()

