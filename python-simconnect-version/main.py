# =======================
# MSFS Screenshot EXIF Updater
# Version 1.0.0
# By PBandJamf AKA TeezyYoxO
# =======================

# CHANGELOG #

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

import os
from time import sleep
from SimConnect import SimConnect, AircraftRequests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Function to create GPSInfo for EXIF
def create_gps_info(latitude, longitude, altitude):
    def convert_to_dms(value):
        d = int(value)
        m = int((value - d) * 60)
        s = (value - d - m / 60) * 3600
        return (d, m, s)

    lat_dms = convert_to_dms(abs(latitude))
    lon_dms = convert_to_dms(abs(longitude))

    return {
        'GPSLatitude': [(lat_dms[0], 1), (lat_dms[1], 1), (int(lat_dms[2] * 10000), 10000)],
        'GPSLatitudeRef': 'N' if latitude >= 0 else 'S',
        'GPSLongitude': [(lon_dms[0], 1), (lon_dms[1], 1), (int(lon_dms[2] * 10000), 10000)],
        'GPSLongitudeRef': 'E' if longitude >= 0 else 'W',
        'GPSAltitude': (int(altitude * 100), 100),
        'GPSAltitudeRef': 0  # Above sea level
    }

# Edit image EXIF
def add_location_to_exif(image_path, latitude, longitude, altitude):
    img = Image.open(image_path)
    exif_data = img.getexif()

    gps_info = create_gps_info(latitude, longitude, altitude)
    gps_tag = {TAGS[key]: key for key in TAGS}.get('GPSInfo')

    exif_data[gps_tag] = {
        GPSTAGS[key]: value for key, value in gps_info.items()
    }

    img.save(image_path, exif=exif_data)

# Main function to retrieve data and update EXIF
def main():
    try:
        # Connect to MSFS SimConnect
        sm = SimConnect()
        aq = AircraftRequests(sm)

        print("Connected to Microsoft Flight Simulator.")

        # Wait for screenshot to appear
        screenshot_dir = os.path.expanduser("~/Pictures")  # Adjust to your screenshot folder
        print(f"Watching for screenshots in {screenshot_dir}...")

        existing_files = set(os.listdir(screenshot_dir))

        while True:
            # Check for new screenshots
            current_files = set(os.listdir(screenshot_dir))
            new_files = current_files - existing_files

            if new_files:
                screenshot_file = list(new_files)[0]
                screenshot_path = os.path.join(screenshot_dir, screenshot_file)

                # Get aircraft location data
                latitude = aq.get("PLANE_LATITUDE")
                longitude = aq.get("PLANE_LONGITUDE")
                altitude = aq.get("PLANE_ALTITUDE")

                print(f"New screenshot detected: {screenshot_file}")
                print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")

                # Add location data to EXIF
                add_location_to_exif(screenshot_path, latitude, longitude, altitude)
                print(f"Updated EXIF data for {screenshot_file}.")

                # Update file set
                existing_files = current_files

            sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
