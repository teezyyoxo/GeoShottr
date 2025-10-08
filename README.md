### THE PYTHON-SIMCONNECT VERSION IS THE ONLY FUNCTIONAL VERSION FOR RIGHT NOW :) --dev 3Mar2025

# Geoshottr

**Geoshottr** is a Python-based tool that automatically adds geolocation metadata (latitude, longitude, and altitude) to your Microsoft Flight Simulator screenshots. It detects screenshots saved by the game, retrieves aircraft location data, and embeds the information into the images, so you can view them on a map or use them in photo apps that support geotagging.

---

## Features

- **Geolocation Tagging**: Adds latitude, longitude, and altitude metadata to screenshots.
- **PNG to JPEG Conversion**: Automatically converts PNG screenshots to JPEG format while preserving metadata.
- **Custom Folder Support**: Monitors one or more directories for new screenshots, with geotagging support.
- **EXIF Metadata**: Embeds GPS data into EXIF metadata (suitable for mapping applications like Google Photos and Apple Photos).
- **Clean Exit**: Handles interruptions gracefully without errors or incomplete file saves.

# Planned upcoming features
## Future Plans:
- Automate taking screenshots directly from the script.
- Create/add a UI (initially, will be a System Tray icon, but would ultimately like to integrate directly into the sim's in-flight toolbar to initiate the whole process of the script, but I am satisfied with how it works for now).
- ~~Executable + tray icon~~ *in-development*
- Automatic startup with sim – would love help with this!
- Figure out a way to preserve image quality when converting down from the uncompressed PNG to JPEG (or a completely different approach to this whole issue).
- Add user-configurable settings for screenshot folder and EXIF fields, either in the in-game UI, a "verify settings" dialog box that is produced at launch, or something from the System Tray. Possibly via tray icon?
- Optimize, optimize, optimize.
- Handle non-PNG files more gracefully.
- Actual support for NVIDIA's "Super Resolution" screenshots.
- NVIDIA Capture SDK integration for closer-to-native screenshot handling.
- Full-resolution geotagged screenshots; currently, the script converts the full-res to JPEG. See "how it works" for more info.
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

 To compile the .exe yourself, run the following command:
`py -3 -m PyInstaller --onefile --noconsole --icon 'images\geoshottr.ico' --name GeoShottr main.py`

----------

## How does it work?

~~Simple.~~
The script runs in the background, monitoring the specified folders for new screenshots from the sim.
It actively reads data lat/long/alt directly from SimConnect.
When a screenshot is taken, the script "catches" it.
The "captured" screenshot (PNG, which *does not* have EXIF support) is then converted to a JPEG (which *does* have EXIF support).
Because the python-simconnect version (along with the current executable) utilizes the PIL ("Pillow") module for doing this, the output file is usually noticeably lower in quality as it has less color depth than the original. 
If you know of a better way to do this, please submit an Issue or PR, because I would love to improve this for everyone. I love my full-res screenshots (#SimPhotographer), but I'm beginning to appreciate seeing a map with receipts of my past flights much more than knowing I can color-grade the original.

Let's work together? :D

## Changelog
All version history/changes can be found in Changelog.md.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
