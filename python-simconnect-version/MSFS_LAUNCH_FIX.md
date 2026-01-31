# GeoShottr MSFS Launch Fix

## Issues Identified

Your application was failing when launched by MSFS due to several issues:

### 1. **Hardcoded Icon Path** 
   - **Problem**: The code referenced `C:\Users\monte\Documents\GitHub\geoshottr\images\geoshottr.ico` directly
   - **Issue**: When running from the bundled executable, this path doesn't exist in the expected location
   - **Fix**: Now uses `resource_path("images/geoshottr.ico")` which correctly resolves from the bundled PyInstaller package

### 2. **Hardcoded Screenshot Directories**
   - **Problem**: Paths like `C:\Users\monte\Videos\Captures` were hardcoded
   - **Issue**: If MSFS launches the app with a different working directory or user context, it fails to find screenshots
   - **Fix**: Now dynamically constructs paths using `os.path.expanduser()` and validates they exist before monitoring

### 3. **No Error Visibility When Launched by MSFS**
   - **Problem**: When MSFS launches the executable, there's no console window to see error messages
   - **Issue**: Application silently fails without any way to diagnose what went wrong
   - **Fix**: Added file-based logging to `%APPDATA%\Local\GeoShottr\geoshottr_debug.log` so errors are captured

### 4. **No Permission Error Handling**
   - **Problem**: If a screenshot directory is inaccessible, the app would crash
   - **Issue**: MSFS may run with different permissions or directory access restrictions
   - **Fix**: Added try-catch blocks to gracefully handle permission errors

## Changes Made

### main.py
1. Added `LOG_FILE` constant pointing to: `~/AppData/Local/GeoShottr/geoshottr_debug.log`
2. Added `log_message()` function that writes to both console and file
3. Added `get_screenshot_directories()` function that:
   - Uses `os.path.expanduser()` for dynamic path resolution
   - Validates directories exist before returning them
   - Logs warnings if no directories are found
4. Updated `create_system_tray_icon()` to:
   - Use `resource_path()` for the icon file
   - Provide fallback icon if file cannot be loaded
5. Updated main loop to:
   - Use dynamic screenshot directories
   - Add try-catch blocks around directory operations
   - Log all errors to file for debugging

## How to Test

### Manual Launch (Existing Workflow - Should Still Work)
```cmd
cd C:\Users\monte\Documents\GitHub\GeoShottr\python-simconnect-version\dist
GeoShottr1.7.6.exe
```

### MSFS Integration
Keep your MSFS configuration as-is:
```
C:\Users\monte\Documents\GitHub\GeoShottr\python-simconnect-version\dist\GeoShottr1.7.6.exe
```

The app should now:
1. Show tray icon immediately
2. Begin monitoring screenshot directories
3. Process screenshots when detected

## Debugging

If issues persist, check the debug log:
```
%APPDATA%\Local\GeoShottr\geoshottr_debug.log
```

This file will show:
- Screenshot directories being monitored
- Permission errors
- SimConnect connection status
- File processing errors

## Rebuilding the Executable

When you're ready to rebuild with the fixed code:

```powershell
cd C:\Users\monte\Documents\GitHub\GeoShottr\python-simconnect-version
pyinstaller GeoShottr.spec
```

This will create a new `dist\GeoShottr1.7.6.exe` with all the fixes.

## Key Improvements
- ✅ No more hardcoded user-specific paths
- ✅ Robust error handling with file logging
- ✅ Dynamic resource loading for bundled files
- ✅ Graceful fallbacks when resources missing
- ✅ Better permission error detection
- ✅ Works with MSFS's process launch context
