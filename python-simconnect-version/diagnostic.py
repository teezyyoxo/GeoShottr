#!/usr/bin/env python3
"""
Quick diagnostic script to verify GeoShottr can find all required resources
when launched from the executable.
"""

import os
import sys
from pathlib import Path

def check_screenshot_dirs():
    """Check if screenshot directories are accessible"""
    print("=" * 60)
    print("SCREENSHOT DIRECTORY CHECK")
    print("=" * 60)
    
    potential_dirs = [
        os.path.expanduser("~/Videos/Captures"),
        os.path.expanduser("~/Videos/NVIDIA/Microsoft Flight Simulator 2024"),
        os.path.expanduser("~/Videos/NVIDIA/Microsoft Flight Simulator"),
    ]
    
    print(f"\nUsername: {os.getenv('USERNAME')}")
    print(f"Home directory: {os.path.expanduser('~')}\n")
    
    for dir_path in potential_dirs:
        exists = os.path.isdir(dir_path)
        accessible = os.access(dir_path, os.R_OK) if exists else False
        status = "✅ EXISTS & READABLE" if accessible else "❌ NOT FOUND or NOT READABLE" if not exists else "⚠️  EXISTS but NOT READABLE"
        print(f"  {status}: {dir_path}")
    
    print()

def check_icon_file():
    """Check if the icon file can be loaded"""
    print("=" * 60)
    print("ICON FILE CHECK")
    print("=" * 60)
    
    # Try the bundled path first (as it would be from the exe)
    bundled_path = os.path.join(os.path.dirname(__file__), "images", "geoshottr.ico")
    
    # Try the source path
    source_path = os.path.expanduser("~/Documents/GitHub/geoshottr/images/geoshottr.ico")
    
    print(f"\nBundled path: {bundled_path}")
    print(f"  Exists: {os.path.isfile(bundled_path)}")
    
    print(f"\nSource path: {source_path}")
    print(f"  Exists: {os.path.isfile(source_path)}")
    
    print()

def check_log_directory():
    """Check if log directory is writable"""
    print("=" * 60)
    print("LOG DIRECTORY CHECK")
    print("=" * 60)
    
    log_dir = os.path.expanduser("~/AppData/Local/GeoShottr")
    
    print(f"\nLog directory: {log_dir}")
    print(f"  Exists: {os.path.isdir(log_dir)}")
    
    if os.path.isdir(log_dir):
        writable = os.access(log_dir, os.W_OK)
        print(f"  Writable: {writable}")
    else:
        print(f"  Will be created on first run")
    
    print()

def check_simconnect():
    """Check if SimConnect can be imported"""
    print("=" * 60)
    print("SIMCONNECT IMPORT CHECK")
    print("=" * 60)
    
    try:
        from SimConnect import SimConnect, AircraftRequests
        print("\n✅ SimConnect module found and imported successfully")
    except ImportError as e:
        print(f"\n❌ Could not import SimConnect: {e}")
    
    print()

if __name__ == "__main__":
    print("\n")
    print("🔧 GeoShottr Diagnostic Check")
    print("=" * 60)
    print(f"Current directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    print()
    
    check_screenshot_dirs()
    check_icon_file()
    check_log_directory()
    check_simconnect()
    
    print("=" * 60)
    print("Diagnostic check complete!")
    print("=" * 60)
