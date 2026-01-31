# GeoShottr MSFS Integration - Complete Fix Summary

## What Was Wrong

Your GeoShottr executable works when launched manually via CMD or Run prompt, but fails when MSFS launches it because:

1. **Hardcoded file paths** - The icon path and screenshot directories were hardcoded to your specific user directory
2. **No error visibility** - When MSFS launches the app, there's no console window to see what's failing
3. **Working directory differences** - Manual launch vs MSFS launch may use different working directories
4. **Missing error handling** - Permission issues would crash the app instead of gracefully continuing

## What Was Fixed

### Code Changes (main.py)

1. **Dynamic Path Resolution**
   - Screenshot directories now use `os.path.expanduser()` instead of hardcoded paths
   - Icon path now uses the `resource_path()` function to work with PyInstaller's bundled resources
   - Paths are validated before use

2. **File-Based Logging**
   - Added `LOG_FILE` pointing to `%APPDATA%\Local\GeoShottr\geoshottr_debug.log`
   - New `log_message()` function writes to both console AND file
   - When launched by MSFS (no console), errors are captured to the log file

3. **Dynamic Directory Detection**
   - New `get_screenshot_directories()` function:
     - Checks common NVIDIA and Windows capture locations
     - Returns only directories that actually exist
     - Logs warnings if no directories found

4. **Robust Error Handling**
   - Try-catch blocks around directory operations
   - Handles permission errors gracefully
   - Provides fallback icon if image file is missing
   - Continues operation even if some features fail

## Files Modified

- **main.py** - Core application logic with all the fixes above
- **GeoShottr.spec** - Already correct (includes images folder and icon)

## Files Added

- **MSFS_LAUNCH_FIX.md** - Detailed documentation of the changes
- **diagnostic.py** - Utility script to verify your setup

## Next Steps

### 1. Verify the Setup (Optional but Recommended)
```powershell
cd C:\Users\monte\Documents\GitHub\GeoShottr\python-simconnect-version
python diagnostic.py
```

This will check:
- ✅ Screenshot directories exist and are readable
- ✅ Icon file can be found
- ✅ Log directory is writable
- ✅ SimConnect is installed

### 2. Rebuild the Executable
```powershell
cd C:\Users\monte\Documents\GitHub\GeoShottr\python-simconnect-version
pyinstaller GeoShottr.spec
```

The new executable will be at:
```
C:\Users\monte\Documents\GitHub\GeoShottr\python-simconnect-version\dist\GeoShottr1.7.6.exe
```

### 3. Test Manual Launch (Should Still Work)
```powershell
C:\Users\monte\Documents\GitHub\GeoShottr\python-simconnect-version\dist\GeoShottr1.7.6.exe
```

You should see:
- Startup message in console
- Tray icon appears
- "Waiting for screenshots" message

### 4. Test MSFS Integration
Launch MSFS as normal. The app should:
- Show tray icon immediately
- Begin monitoring screenshot directories
- Process screenshots when you take them

## Debugging If Issues Persist

If something still doesn't work, check the debug log:

**Windows Explorer:**
```
%APPDATA%\Local\GeoShottr\geoshottr_debug.log
```

**Or from PowerShell:**
```powershell
Get-Content "$env:APPDATA\Local\GeoShottr\geoshottr_debug.log" -Tail 50
```

The log will show:
- Directories being monitored
- Connection attempts to MSFS
- Permission errors
- File processing details
- Any other errors

## Key Improvements

| Issue | Before | After |
|-------|--------|-------|
| Icon loading | Hardcoded path fails | Uses `resource_path()`, has fallback |
| Screenshot dirs | Hardcoded paths | Dynamic `os.path.expanduser()` |
| Error visibility | Silent failure | Logged to file |
| Permission errors | Crashes app | Logged and continues |
| User paths | Only works for monte | Works for any user |

## Technical Details

### Why This Works with MSFS

When MSFS launches your executable:
- It may use a different working directory
- It may run with different user context or permissions
- There's no console window to show errors
- The application must be self-contained and self-diagnosing

The fixes address all of these:
- Paths are absolute and user-independent (using `os.path.expanduser()`)
- All errors are logged to a file that persists regardless of console
- Resources are properly bundled and located with `resource_path()`
- Errors don't crash the app; they're logged and processing continues

## Questions?

The [MSFS_LAUNCH_FIX.md](MSFS_LAUNCH_FIX.md) file has more technical details.

The [diagnostic.py](diagnostic.py) script can verify your environment is set up correctly.

Good luck with GeoShottr! 🛰️
