# Changelog

Version 1.7.6
- Consolidated monitoring output: screenshot directories are listed once under a single header instead of repeating "Waiting for screenshots..." for each directory.
- Colorized the labels for clearer console output.
- Extracted monitor thread startup into `start_monitoring_thread()` for sanity, I guess.
- Added `CAMERA_MODEL` EXIF tag for converted JPEGs (sets Camera Model to "iPhone 19 Pro Max" by default -- because, why not?)
- Improved SimConnect telemetry handling: the monitor will handle I/O errors more gracefully and attempt reconnects instead of spamming the console with repeated low-level errors.
- Minor console output and formatting tweaks.

 Version 1.7.5
- Modified console output to use colorized labels for better readability. Further modifications to come.

 Version 1.7.4
- Improved telemetry reliability by retrying data requests up to 3 times with a short delay.
- Enhanced console logging for telemetry fetch attempts and error reporting.
- Maintained maximum JPEG quality when saving converted screenshots.
- Minor code cleanup and robustness improvements around EXIF metadata writing.

 Version 1.7.3
 - Fixed rare script crash when telemetry values are None.
 - Added safe formatting for missing GPS values.

 Version 1.7.2
 - Colorized error log label.

 Version 1.7.1
 - Added timeout for file write operations to avoid "image is truncated" errors.

 Version 1.7
 - Updated screenshot paths.
 - Corrected exit behavior (ctrl+c now works properly).
 - Prettified console output (just a little bit).

 Version 1.6.1.3
 - Updated executable to include the added debugging.

 Version 1.6.1.2 (hopefully this versioning makes sense by now)
 - Added some debugging; the actual operations are not running when the executable is run standalone.

 Version 1.5.1.2 (script v1.5 + executable v1.2)
 - Corrected path definition to images/icons and such for executable.
 - Added path for X-Plane screenshots to screenshot_dirs.

 Version 1.4.1.1 (script v1.4 + executable v1.1)
 - Attempted to fix issue of script not terminating with ctrl+c in console, but am getting nowhere. 
 - Both the script and executable both work beautifully as-is.
 - Onward and upward from here on out.

 Version 1.3a1.0 (script v1.3a + executable v1.0)
 - Adjusted the thread function call to main instead of one that is nonexistent.

 Version 1.3.1.0 (script v1.3 + executable v1.0 = en juntos "v1.3.1.0")
 - Added System Tray integration using PyStray.
 - Script now runs in a separate thread (for more herspers).
 - Right-click menu in the System Tray allows for graceful exit.
 - System Tray icon supports custom icons (icon_image var).

 Version 1.2.6
 - Restored normal operation -- script now writes EXIF data to the down-converted JPEG again. Sorry about breaking that!
 - Back to square one with handling Super Resolution screenshots. Oy vey...

 Version 1.2.5
 - Fixed processing of super-resolution screenshots to handle both large and standard images effectively.
 - Added validation for PNG and other image types when using OpenCV for super-resolution images.
 - Reworked error handling during image loading and EXIF data insertion to avoid unexpected script failures.

 Version 1.2.4
 - Super-Resolution Support: Added OpenCV handling for "super-resolution" screenshots (e.g., 5120x2880 from NVIDIA overlay).
 - Updated EXIF geotagging: Enhanced EXIF update with GPS data (latitude, longitude, altitude).
 - Fallback on missing data: Skips EXIF update if location data is missing.
 - Improved logging for image loading issues and skipped screenshots.

 Version 1.2.3.3
 - Removed one line of extraneous console output.

 Version 1.2.3.2
 - Removed EXIF loading, assuming no EXIF data initially (for screenshots).
 - Created EXIF data from scratch with GPS coordinates, altitude, and description.
 - Simplified handling of PNG to JPEG conversion with EXIF insertion.
 - Ensured smoother workflow for screenshots without EXIF data.
 - Realized that the EXIF standard uses DMS and there is no way to get around it. A custom EXIF field with the converted value would work, but... kinda pointless.

 Version 1.2.3.1
 - Reverted to a previously working version of the script.
 - Improved EXIF data handling, especially when EXIF data is missing in newly created JPEG files.
 - Simplified the conversion of PNG files to JPEG with proper EXIF metadata addition.
 - Enhanced error handling during EXIF saving process.

 Version 1.2.3
 - Added error handling when EXIF data is missing in newly created JPEG files.
 - Now the script creates an empty EXIF structure if none exists and adds GPS data.
 - Improved robustness against missing or incomplete EXIF data during the metadata update process.
 - Ensured that GPS data is correctly embedded in JPEG files even when EXIF metadata is initially absent.

 Version 1.2.2
 - Fixed issue where EXIF metadata was being applied to the original PNG file instead of the new JPEG.
 - Ensured that EXIF metadata is updated only for the new JPEG file after PNG conversion.
 - Improved error handling for metadata saving to avoid issues with missing or invalid files.
 - Updated the script to handle PNG files with GPS data more effectively, preserving the original metadata.

 Version 1.2.1
 - Added decimal degree format for GPS coordinates in EXIF metadata (Latitude: 33.894074, Longitude: 141.540572).
 - Updated the script to handle GPS data in decimal format, making it compatible with modern mapping tools.
 - Fixed KeyboardInterrupt handling to allow graceful script termination when manually stopped.
 - Continued support for PNG to JPEG conversion, preserving EXIF metadata with decimal GPS values.

 Version 1.2.0
 - Improved GPS coordinate format by switching to decimal degrees for latitude and longitude in EXIF metadata.
 - Updated `create_gps_info` function to store GPS data in decimal degrees format, making it more compatible with modern tools.
 - Enhanced compatibility for iOS and mapping software that can read decimal degrees.
 - Ensured EXIF data now includes more easily accessible numeric latitude and longitude values (e.g., Latitude: 33.990744, Longitude: 141.216428).
 - Continued support for PNG to JPEG conversion, preserving metadata.

 Version 1.1.9
 - Integrated piexif for handling EXIF metadata in JPEG files.
 - Updated EXIF data handling to include proper GPS location and altitude information in JPEG files.
 - Ensured PNG to JPEG conversion maintains EXIF data.
 - Improved error handling for metadata saving.

 Version 1.1.8
 - Learned how to correctly comment things out in Python lol.

 Version 1.1.7:
 - Corrected the issue where the geo data wasn't being written to JPEG files.
 - Explicitly used `piexif` to insert EXIF metadata into JPEG files after conversion.
 - Updated the Description field to properly format GPS data for PNG files.
 - Ensured both PNG and JPEG files have location data (longitude, latitude, altitude) embedded.

 Version 1.1.6:
 - Fixed the issue where geo data failed to be written to the new JPEG files.
 - Improved handling of PNG-to-JPEG conversion and metadata embedding.
 - Updated Description field formatting for both PNG and JPEG files to use the correct structure.
 - Ensured EXIF metadata is properly saved to the new JPEG files after conversion from PNG.

 Version 1.1.5:
 - Fixed issue where PNG files were not properly converted to JPEG.
 - Added functionality to save converted JPEGs in a subfolder named `Geotagged`.
 - Corrected handling of EXIF data to ensure GPS information is embedded in the new JPEG files.
 - Implemented graceful handling of `KeyboardInterrupt` to exit the script without printing stack traces.
 - Improved error messages for better troubleshooting and user feedback.

 Version 1.1.4:
 - The script now handles KeyboardInterrupt to exit cleanly without printing stack traces.
 - Addressed the issue where PNG files failed to save due to broken metadata. Now, location data is embedded as a custom text chunk under the `Description` field.
 - Cleaned up the code for better handling of PNG metadata saving.

 Version 1.1.3:
 - Fixed issue with broken PNG file when trying to write EXIF metadata.
 - Switched to embedding GPS data in custom text chunks (using the `Description` field) for PNG files.
 - Ensured that PNG files' integrity is preserved by avoiding direct modification of EXIF data, which is not native to PNG format.
 - Added fallback handling for storing GPS data in a format compatible with PNG metadata.
 - Improved error handling for cases where the image format is not supported or the file is corrupted.

 Version 1.1.2:
 - Fixed issue with GPS EXIF metadata not being correctly written to PNG files.
 - Manually mapped GPS data to the proper EXIF tags using the correct `GPSTAGS` values.
 - Improved handling for missing GPSInfo tag in EXIF and added more comprehensive error messages.
 - Ensured that GPS data is added properly even if the EXIF metadata doesn't initially contain a GPS tag.

 Version 1.1.1:
 - Fixed issue where GPS data was not correctly added to the EXIF metadata.
 - Updated EXIF handling to ensure GPS metadata is written under the correct tag (`GPSInfo`).
 - Added better error handling for missing EXIF tags and issues during save operation.
 - Ensured that only valid GPS keys are used in the EXIF data.

 Version 1.1.0:
 - Added support for monitoring multiple directories.
 - Limited file processing to `.png` files containing "Microsoft Flight Simulator" in their names.
 - Updated dynamic logging to print the actual monitored directories.
 - Prints the full path and location data when a new screenshot is detected.

 Version 1.0.0:
 - Initial release.
 - Connects to MSFS using SimConnect.
 - Retrieves latitude, longitude, and altitude data.
 - Monitors a specified folder for new screenshots.
 - Adds location data to screenshot EXIF metadata.
   