#!/usr/bin/env python3
"""
Direct APK builder - bypasses buildozer completely
Uses python-for-android (p4a) directly to build APK
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run command and return success status"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("=== DIRECT APK BUILDER - BYPASSING BUILDOZER ===")
    
    # Install p4a directly
    print("Installing python-for-android...")
    if not run_command("pip install python-for-android"):
        print("Failed to install p4a")
        return False
    
    # Set up environment
    android_home = os.environ.get('ANDROID_HOME', '/opt/android-sdk')
    android_ndk = os.environ.get('ANDROID_NDK_HOME', f'{android_home}/ndk/25.2.9519653')
    
    print(f"ANDROID_HOME: {android_home}")
    print(f"ANDROID_NDK_HOME: {android_ndk}")
    
    # Create output directory
    os.makedirs("bin", exist_ok=True)
    
    # Build with p4a directly
    requirements = "python3,kivy==2.1.0,kivymd==1.1.1,pillow==9.5.0,requests==2.28.2,python-dateutil==2.8.2,plyer==2.1.0,pyjnius==1.4.2,android"
    
    p4a_cmd = f"""
    p4a apk --private . --package=org.voltmatic.voltmaticapp --name="Voltmatic App" --version=0.1 \
    --bootstrap=sdl2 --requirements={requirements} \
    --permission INTERNET --permission WRITE_EXTERNAL_STORAGE --permission READ_EXTERNAL_STORAGE \
    --permission ACCESS_NETWORK_STATE --permission ACCESS_WIFI_STATE \
    --arch=arm64-v8a --arch=armeabi-v7a \
    --sdk-dir={android_home} --ndk-dir={android_ndk} \
    --android-api=30 --ndk-api=21 \
    --orientation=portrait \
    --release
    """.strip().replace('\n', ' ')
    
    print("Building APK with p4a...")
    if run_command(p4a_cmd):
        print("P4A build successful!")
        
        # Find generated APK
        apk_files = list(Path(".").glob("**/*.apk"))
        if apk_files:
            apk_file = apk_files[0]
            shutil.copy(apk_file, "bin/voltmatic-app-p4a.apk")
            print(f"APK copied to bin/voltmatic-app-p4a.apk")
            print(f"APK size: {os.path.getsize('bin/voltmatic-app-p4a.apk')} bytes")
            return True
        else:
            print("P4A build completed but no APK found")
    else:
        print("P4A build failed")
    
    # Try debug build if release failed
    debug_cmd = p4a_cmd.replace("--release", "--debug")
    print("Trying debug build...")
    if run_command(debug_cmd):
        apk_files = list(Path(".").glob("**/*.apk"))
        if apk_files:
            apk_file = apk_files[0]
            shutil.copy(apk_file, "bin/voltmatic-app-p4a-debug.apk")
            print(f"Debug APK created: bin/voltmatic-app-p4a-debug.apk")
            return True
    
    print("All direct build attempts failed")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
