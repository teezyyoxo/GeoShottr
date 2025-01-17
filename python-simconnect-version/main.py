"""
=======================
 GeoShottr - Geotagging MSFS Screenshots
 Version 1.2.4 (current)
 By PBandJamf AKA TeezyYoxO
 =======================
"""

"""
######### CHANGELOG #########

# Version 1.2.6
# - Restored normal operation -- script now writes EXIF data to the down-converted JPEG again. Sorry about breaking that!
# - Back to square one with handling Super Resolution screenshots. Oy vey...

# Version 1.2.5
# - Fixed processing of super-resolution screenshots to handle both large and standard images effectively.
# - Added validation for PNG and other image types when using OpenCV for super-resolution images.
# - Reworked error handling during image loading and EXIF data insertion to avoid unexpected script failures.

# Version 1.2.4
# - Super-Resolution Support: Added OpenCV handling for "super-resolution" screenshots (e.g., 5120x2880 from NVIDIA overlay).
# - Updated EXIF geotagging: Enhanced EXIF update with GPS data (latitude, longitude, altitude).
# - Fallback on missing data: Skips EXIF update if location data is missing.
# - Improved logging for image loading issues and skipped screenshots.

# Version 1.2.3.3
# - Removed one line of extraneous console output.

# Version 1.2.3.2
# - Removed EXIF loading, assuming no EXIF data initially (for screenshots).
# - Created EXIF data from scratch with GPS coordinates, altitude, and description.
# - Simplified handling of PNG to JPEG conversion with EXIF insertion.
# - Ensured smoother workflow for screenshots without EXIF data.
# - Realized that the EXIF standard uses DMS and there is no way to get around it. A custom EXIF field with the converted value would work, but... kinda pointless.

# Version 1.2.3.1
# - Reverted to a previously working version of the script.
# - Improved EXIF data handling, especially when EXIF data is missing in newly created JPEG files.
# - Simplified the conversion of PNG files to JPEG with proper EXIF metadata addition.
# - Enhanced error handling during EXIF saving process.

# Version 1.2.3
# - Added error handling when EXIF data is missing in newly created JPEG files.
# - Now the script creates an empty EXIF structure if none exists and adds GPS data.
# - Improved robustness against missing or incomplete EXIF data during the metadata update process.
# - Ensured that GPS data is correctly embedded in JPEG files even when EXIF metadata is initially absent.

# Version 1.2.2
# - Fixed issue where EXIF metadata was being applied to the original PNG file instead of the new JPEG.
# - Ensured that EXIF metadata is updated only for the new JPEG file after PNG conversion.
# - Improved error handling for metadata saving to avoid issues with missing or invalid files.
# - Updated the script to handle PNG files with GPS data more effectively, preserving the original metadata.

# Version 1.2.1
# - Added decimal degree format for GPS coordinates in EXIF metadata (Latitude: 33.894074, Longitude: 141.540572).
# - Updated the script to handle GPS data in decimal format, making it compatible with modern mapping tools.
# - Fixed KeyboardInterrupt handling to allow graceful script termination when manually stopped.
# - Continued support for PNG to JPEG conversion, preserving EXIF metadata with decimal GPS values.

# Version 1.2.0
# - Improved GPS coordinate format by switching to decimal degrees for latitude and longitude in EXIF metadata.
# - Updated `create_gps_info` function to store GPS data in decimal degrees format, making it more compatible with modern tools.
# - Enhanced compatibility for iOS and mapping software that can read decimal degrees.
# - Ensured EXIF data now includes more easily accessible numeric latitude and longitude values (e.g., Latitude: 33.990744, Longitude: 141.216428).
# - Continued support for PNG to JPEG conversion, preserving metadata.

# Version 1.1.9
# - Integrated piexif for handling EXIF metadata in JPEG files.
# - Updated EXIF data handling to include proper GPS location and altitude information in JPEG files.
# - Ensured PNG to JPEG conversion maintains EXIF data.
# - Improved error handling for metadata saving.

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

"""
=======================
 GeoShottr - Geotagging MSFS Screenshots
 Version 1.2.5 (current)
 By PBandJamf AKA TeezyYoxO
 =======================
"""

## BEGIN! ##

import os
from time import sleep
from SimConnect import SimConnect, AircraftRequests
from PIL import Image
import piexif

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
            img.save(jpeg_path, exif=exif_bytes)
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

                        # Check for Super-Resolution images based on filename and size
                        if "Super-Resolution" in new_file or os.path.getsize(screenshot_path) > 10 * 1024 * 1024:
                            print(f"High-res image detected: {new_file}")
                        else:
                            print(f"Regular image detected: {new_file}")

                        # Get aircraft location data
                        latitude = aq.get("PLANE_LATITUDE")
                        longitude = aq.get("PLANE_LONGITUDE")
                        altitude = aq.get("PLANE_ALTITUDE")

                        print(f"New screenshot detected: {new_file}")
                        print(f"Path: {screenshot_path}")
                        print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")

                        # Add location data to EXIF and save as JPEG
                        add_location_to_exif(screenshot_path, latitude, longitude, altitude)

                # Update the file set for the directory
                existing_files[dir_path] = current_files

            sleep(1)

    except KeyboardInterrupt:
        print("Exiting gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
