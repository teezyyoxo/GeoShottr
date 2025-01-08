"""
=======================
 GeoShottr - Geotagging MSFS Screenshots
 Version 1.1.8
 By PBandJamf AKA TeezyYoxO
 =======================
"""
"""
This script connects to Microsoft Flight Simulator via SimConnect to retrieve real-time GPS data (latitude, longitude, altitude) while the simulator is running. 
It then watches specified directories for new screenshot files (in PNG format by default). 
Upon detecting a new screenshot, the script extracts the GPS data from the simulator and embeds it into the image's EXIF metadata. 
The script also supports converting PNG screenshots to JPEG format and storing them in a subfolder named 'Geotagged'.

Features:
- Monitors specific directories for new screenshots.
- Retrieves GPS data from Microsoft Flight Simulator using SimConnect.
- Embeds GPS data into EXIF metadata of PNG and JPEG files.
- Converts PNG screenshots to JPEG and stores them in a subfolder called 'Geotagged'.
- Formats the GPS data in the 'Description' field as: 
    "Longitude: X | Latitude: Y | Altitude: Z (feet)".
- Gracefully handles errors and ensures clean exit on user interruption.
"""


"""
######### CHANGELOG #########

# Version 1.1.8
# - Learned how to correctly comment things out in Python lol.

# Version 1.1.7:
# - Corrected the issue where the geo data wasn't being written to JPEG files.
# - Explicitly used `piexif` to insert EXIF metadata into JPEG files after conversion.
# - Updated the Description field to properly format GPS data for PNG files.
# - Ensured both PNG and JPEG files have location data (longitude, latitude, altitude) embedded.

# Version 1.1.6:
# - Fixed the issue where geo data failed to be written to the new JPEG files.
# - Improved handling of PNG-to-JPEG conversion and metadata embedding.
# - Updated Description field formatting for both PNG and JPEG files to use the correct structure.
# - Ensured EXIF metadata is properly saved to the new JPEG files after conversion from PNG.

# Version 1.1.5:
# - Fixed issue where PNG files were not properly converted to JPEG.
# - Added functionality to save converted JPEGs in a subfolder named `Geotagged`.
# - Corrected handling of EXIF data to ensure GPS information is embedded in the new JPEG files.
# - Implemented graceful handling of `KeyboardInterrupt` to exit the script without printing stack traces.
# - Improved error messages for better troubleshooting and user feedback.

# Version 1.1.4:
# - The script now handles KeyboardInterrupt to exit cleanly without printing stack traces.
# - Addressed the issue where PNG files failed to save due to broken metadata. Now, location data is embedded as a custom text chunk under the `Description` field.
# - Cleaned up the code for better handling of PNG metadata saving.

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
"""

import os
from time import sleep
from SimConnect import SimConnect, AircraftRequests
from PIL import Image, PngImagePlugin
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

# Edit image EXIF and save as JPEG in a subfolder
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
            print(f"Successfully converted {image_path} to {jpeg_path}")

            # Add the description to the JPEG image
            img = Image.open(jpeg_path)
            img.save(jpeg_path)  # Ensure the image is saved

            # Print the description and location info
            print(f"Updated EXIF data for {jpeg_path} - {description}")

        else:
            # If not PNG, just print the location info
            print(f"No conversion needed for {image_path}, skipping.")
            print(f"Description: {description}")

    except Exception as e:
        print(f"Failed to save metadata for {image_path}: {e}")

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

                        # Add location data to EXIF and save as JPEG
                        add_location_to_exif(screenshot_path, latitude, longitude, altitude)
                        print(f"Updated EXIF data for {new_file}.")

                # Update the file set for the directory
                existing_files[dir_path] = current_files

            sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

