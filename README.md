# Geoshottr

**Geoshottr** is a Python-based tool that automatically adds geolocation metadata (latitude, longitude, and altitude) to your Microsoft Flight Simulator screenshots. It detects screenshots saved by the game, retrieves geospatial data, and embeds the information into the images, so you can view them on a map or use them in photo apps that support geotagging.

---

## Features

- **Geolocation Tagging**: Adds latitude, longitude, and altitude metadata to screenshots.
- **PNG to JPEG Conversion**: Automatically converts PNG screenshots to JPEG format while preserving metadata.
- **Custom Folder Support**: Monitors one or more directories for new screenshots, with geotagging support.
- **EXIF Metadata**: Embeds GPS data into EXIF metadata (suitable for mapping applications like Google Photos and Apple Photos).
- **Clean Exit**: Handles interruptions gracefully without errors or incomplete file saves.

---

## Installation

### Prerequisites

- Python 3.x
- `pip` (Python package manager)

### Steps to Install

1. Clone the repository:
   ```bash
   git clone https://github.com/teezyyoxo/geoshottr.git`` 

2.  Navigate to the project folder:
    
    bash
    
    Copy code
    
    `cd geoshottr/python-simconnect-version` 
    
3.  Install required dependencies:
    
    bash
    
    Copy code
    
    `pip install -r requirements.txt` 
    
4.  (Optional) Set up an `.env` file to configure your screenshot directories:
    
    ini
    
    Copy code
    
    `SCREENSHOT_PATH_1="C:/path/to/screenshot/folder"
    SCREENSHOT_PATH_2="D:/another/folder"` 
    

----------

## Usage

1.  Ensure Microsoft Flight Simulator is running and taking screenshots.
    
2.  Run the script:
    
    bash
    
    Copy code
    
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

ini

Copy code

`SCREENSHOT_PATH_1="C:/Users/YourUsername/Documents/FS2020_Screenshots"
SCREENSHOT_PATH_2="E:/FlightSimScreenshots"` 

----------

## Changelog

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

----------

## License

This project is licensed under the MIT License - see the LICENSE file for details.
