# =======================
# MSFS Screenshot EXIF Updater
# Version 1.1.2
# By PBandJamf AKA TeezyYoxO
# =======================

# CHANGELOG #

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

    # Create GPS data
    gps_info = create_gps_info(latitude, longitude, altitude)

    # Look up the tag for GPSInfo in EXIF data
    gps_tag = TAGS.get('GPSInfo')

    # Convert the GPS data to a proper format for EXIF GPS
    gps_exif_data = {
        GPSTAGS['GPSLatitude']: gps_info['GPSLatitude'],
        GPSTAGS['GPSLatitudeRef']: gps_info['GPSLatitudeRef'],
        GPSTAGS['GPSLongitude']: gps_info['GPSLongitude'],
        GPSTAGS['GPSLongitudeRef']: gps_info['GPSLongitudeRef'],
        GPSTAGS['GPSAltitude']: gps_info['GPSAltitude'],
        GPSTAGS['GPSAltitudeRef']: gps_info['GPSAltitudeRef'],
    }

    # Check if GPS tag is valid
    if gps_tag is None:
        print("Could not find GPSInfo tag in EXIF.")
        return

    # Add GPS data to EXIF metadata
    if gps_tag in exif_data:
        exif_data[gps_tag] = gps_exif_data
    else:
        # If no GPS tag exists, create it and add the data
        exif_data[gps_tag] = gps_exif_data

    # Save updated EXIF data back to image
    try:
        img.save(image_path, exif=exif_data)
        print(f"Successfully updated EXIF data for {image_path}")
    except Exception as e:
        print(f"Failed to save EXIF data: {e}")

# Main function to retrieve data and update EXIF
def main():
    try:
        # Connect to MSFS SimConnect
        sm = SimConnect()
        aq = AircraftRequests(sm)

        print("Connected to Microsoft Flight Simulator.")

        # Specify folders to monitor
        screenshot_dirs = [
            r"S:\MSFS Recordings\Microsoft Flight Simulator",
            r"C:\Users\monte\Videos\Captures"
        ]
        print(f"Watching for screenshots in the following directories: {', '.join(screenshot_dirs)}")

        # Initialize tracking of existing files in each directory
        existing_files = {dir_path: set(os.listdir(dir_path)) for dir_path in screenshot_dirs}

        while True:
            for dir_path in screenshot_dirs:
                # Get current files in the directory
                current_files = set(os.listdir(dir_path))
                new_files = current_files - existing_files[dir_path]

                for new_file in new_files:
                    # Check if the file is a PNG and contains "Microsoft Flight Simulator"
                    if new_file.lower().endswith(".png") and "Microsoft Flight Simulator" in new_file:
                        screenshot_path = os.path.join(dir_path, new_file)

                        # Get aircraft location data
                        latitude = aq.get("PLANE_LATITUDE")
                        longitude = aq.get("PLANE_LONGITUDE")
                        altitude = aq.get("PLANE_ALTITUDE")

                        print(f"New screenshot detected: {new_file}")
                        print(f"Path: {screenshot_path}")
                        print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")

                        # Add location data to EXIF
                        add_location_to_exif(screenshot_path, latitude, longitude, altitude)
                        print(f"Updated EXIF data for {new_file}.")

                # Update the file set for the directory
                existing_files[dir_path] = current_files

            sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
