### THE SIMCONNECT VERSION IS THE ONLY FUNCTIONAL VERSION FOR RIGHT NOW :) --dev 16.1.24

# Geoshottr

**Geoshottr** is a Python-based tool that automatically adds geolocation metadata (latitude, longitude, and altitude) to your Microsoft Flight Simulator screenshots. It detects screenshots saved by the game, retrieves geospatial data, and embeds the information into the images, so you can view them on a map or use them in photo apps that support geotagging.

---

## Features

- **Geolocation Tagging**: Adds latitude, longitude, and altitude metadata to screenshots.
- **PNG to JPEG Conversion**: Automatically converts PNG screenshots to JPEG format while preserving metadata.
- **Custom Folder Support**: Monitors one or more directories for new screenshots, with geotagging support.
- **EXIF Metadata**: Embeds GPS data into EXIF metadata (suitable for mapping applications like Google Photos and Apple Photos).
- **Clean Exit**: Handles interruptions gracefully without errors or incomplete file saves.

# Planned upcoming features
- Executable + tray icon
- Automatic startup with sim – would love help with this!
---

## Installation

### Prerequisites

- Python 3.x
- `pip` (Python package manager)

### Steps to Install

1. Clone the repository:
   ```git clone https://github.com/teezyyoxo/geoshottr.git``` 

2.  Navigate to the project folder:   
    `cd geoshottr/python-simconnect-version` 
    
3.  Install required dependencies: 
    `pip install -r requirements.txt` 
    
4.  (Optional) Set up an `.env` file to configure your screenshot directories:
    - `SCREENSHOT_PATH_1="C:/path/to/screenshot/folder"`
    - `SCREENSHOT_PATH_2="D:/another/folder"`

## Usage

1.  Ensure Microsoft Flight Simulator is running and taking screenshots.
    
2.  Run the script:
    `python main.py` 
    
3.  The script will:
    -   Monitor specified screenshot directories for new images.
    -   Extract GPS data from Microsoft Flight Simulator (lat, long, altitude).
    -   Convert PNG screenshots to JPEG (if necessary) and save them in a subfolder `Geotagged`.
    -   Add EXIF geolocation metadata to the images.
4.  You should see the geotagged images in the designated folder, ready for mapping or use in photo apps.
    
----------

## Configuration

By default, the script monitors two directories:

-   `S:/MSFS Recordings/Microsoft Flight Simulator`
-   `C:/Users/YourUsername/Videos/Captures`

To customize these directories, create a `.env` file in the project root directory and set the paths using the variables `SCREENSHOT_PATH_1`, `SCREENSHOT_PATH_2`, etc.

Example `.env` file:

`SCREENSHOT_PATH_1="C:/Users/YourUsername/Documents/FS2020_Screenshots"
 SCREENSHOT_PATH_2="E:/FlightSimScreenshots"` 

----------

## Changelog

### Version 1.2.3.2

- Removed EXIF loading, assuming no EXIF data initially (for screenshots).
- Created EXIF data from scratch with GPS coordinates, altitude, and description.
- Simplified handling of PNG to JPEG conversion with EXIF insertion.
- Ensured smoother workflow for screenshots without EXIF data.
- Realized that the EXIF standard uses DMS and there is no way to get around it. A custom EXIF field with the converted value would work, but... kinda pointless.

### Version 1.2.3.1

- Reverted to a previously working version of the script.
- Improved EXIF data handling, especially when EXIF data is missing in newly created JPEG files.
- Simplified the conversion of PNG files to JPEG with proper EXIF metadata addition.
- Enhanced error handling during EXIF saving process.

### Version 1.2.3

- Added error handling when EXIF data is missing in newly created JPEG files.
- Now the script creates an empty EXIF structure if none exists and adds GPS data.
- Improved robustness against missing or incomplete EXIF data during the metadata update process.
- Ensured that GPS data is correctly embedded in JPEG files even when EXIF metadata is initially absent.

### Version 1.2.2

- Fixed issue where EXIF metadata was being applied to the original PNG file instead of the new JPEG.
- Ensured that EXIF metadata is updated only for the new JPEG file after PNG conversion.
- Improved error handling for metadata saving to avoid issues with missing or invalid files.
- Updated the script to handle PNG files with GPS data more effectively, preserving the original metadata.

### Version 1.2.1

- Added decimal degree format for GPS coordinates in EXIF metadata (Latitude: 33.894074, Longitude: 141.540572).
- Updated the script to handle GPS data in decimal format, making it compatible with modern mapping tools.
- Fixed KeyboardInterrupt handling to allow graceful script termination when manually stopped.
- Continued support for PNG to JPEG conversion, preserving EXIF metadata with decimal GPS values.

### Version 1.2.0

- Improved GPS coordinate format by switching to decimal degrees for latitude and longitude in EXIF metadata.
- Updated `create_gps_info` function to store GPS data in decimal degrees format, making it more compatible with modern tools.
- Enhanced compatibility for iOS and mapping software that can read decimal degrees.
- Ensured EXIF data now includes more easily accessible numeric latitude and longitude values (e.g., Latitude: 33.990744, Longitude: 141.216428).
- Continued support for PNG to JPEG conversion, preserving metadata.

### Version 1.1.9

- Integrated piexif for handling EXIF metadata in JPEG files.
- Updated EXIF data handling to include proper GPS location and altitude information in JPEG files.
- Ensured PNG to JPEG conversion maintains EXIF data.
- Improved error handling for metadata saving.
- Learned how to correctly comment things out in Python lol.



### Version 1.1.8:

-   Added support for an `.env` file to declare screenshot directories.
-   Implemented `png` to `jpeg` conversion with embedded EXIF metadata in the JPEG files.
-   Improved geolocation metadata formatting in the `Description` field: `Longitude: X | Latitude: Y | Altitude: Z (feet)`.

### Version 1.1.7:

-   Fixed issues where GPS metadata wasn't being embedded in JPEG files.
-   Refined error handling and logging to improve feedback during script execution.

### Version 1.1.6:

-   Added geotagging support for both PNG and JPEG files.
-   Resolved issues with missing geolocation data in images.

### Version 1.1.5:

-   Fixed issue where PNG files were not properly converted to JPEG.
-   Added functionality to save converted JPEGs in a subfolder named `Geotagged`.
-   Corrected handling of EXIF data to ensure GPS information is embedded in the new JPEG files.
-   Implemented graceful handling of `KeyboardInterrupt` to exit the script without printing stack traces.

### Version 1.1.4:

- The script now handles KeyboardInterrupt to exit cleanly without printing stack traces.
- Addressed the issue where PNG files failed to save due to broken metadata. Now, location data is embedded as a custom text chunk under the `Description` field.
- Cleaned up the code for better handling of PNG metadata saving.

### Version 1.1.3:

- Fixed issue with broken PNG file when trying to write EXIF metadata.
- Switched to embedding GPS data in custom text chunks (using the `Description` field) for PNG files.
- Ensured that PNG files' integrity is preserved by avoiding direct modification of EXIF data, which is not native to PNG format.
- Added fallback handling for storing GPS data in a format compatible with PNG metadata.
- Improved error handling for cases where the image format is not supported or the file is corrupted.

### Version 1.1.2:

- Fixed issue with GPS EXIF metadata not being correctly written to PNG files.
- Manually mapped GPS data to the proper EXIF tags using the correct `GPSTAGS` values.
- Improved handling for missing GPSInfo tag in EXIF and added more comprehensive error messages.
- Ensured that GPS data is added properly even if the EXIF metadata doesn't initially contain a GPS tag.

### Version 1.1.1:

- Fixed issue where GPS data was not correctly added to the EXIF metadata.
- Updated EXIF handling to ensure GPS metadata is written under the correct tag (`GPSInfo`).
- Added better error handling for missing EXIF tags and issues during save operation.
- Ensured that only valid GPS keys are used in the EXIF data.

### Version 1.1.0:

- Added support for monitoring multiple directories.
- Limited file processing to `.png` files containing "Microsoft Flight Simulator" in their names.
- Updated dynamic logging to print the actual monitored directories.
- Prints the full path and location data when a new screenshot is detected.

### Version 1.0.0:

- Initial release.
- Connects to MSFS using SimConnect.
- Retrieves latitude, longitude, and altitude data.
- Monitors a specified folder for new screenshots.
- Adds location data to screenshot EXIF metadata. 

## Future Plans:
- Automate taking screenshots directly from the script.
- Create/add a UI (initially, will be a System Tray icon, but would ultimately like to integrate directly into the sim's in-flight toolbar to initiate the whole process of the script, but I am satisfied with how it works for now)
- Figure out a way to preserve image quality when converting down from the uncompressed PNG to JPEG (or a completely different approach to this whole issue)
- Add user-configurable settings for screenshot folder and EXIF fields, either in the in-game UI, a "verify settings" dialog box that is produced at launch, or something from the System Tray.
- Optimize, optimize, optimize.

----------

## License

This project is licensed under the MIT License - see the LICENSE file for details.
