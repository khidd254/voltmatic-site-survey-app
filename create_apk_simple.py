#!/usr/bin/env python3
"""
Simple APK creator - uses the most basic approach possible
Creates a working APK using minimal Android project structure
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """Run command and return success"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print("SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def create_simple_apk():
    """Create the simplest possible APK"""
    
    print("=== CREATING SIMPLE APK ===")
    
    # Environment setup
    android_home = os.environ.get('ANDROID_HOME', '/opt/android-sdk')
    build_tools = f"{android_home}/build-tools/30.0.3"
    platform = f"{android_home}/platforms/android-30/android.jar"
    
    print(f"Android Home: {android_home}")
    print(f"Build Tools: {build_tools}")
    
    # Create output directory
    os.makedirs("bin", exist_ok=True)
    
    # Create temporary working directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Working in: {temp_dir}")
        
        # Create basic Android project structure
        project_dir = Path(temp_dir) / "simple_app"
        project_dir.mkdir()
        
        # Create manifest
        manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.voltmatic.voltmaticapp"
    android:versionCode="1"
    android:versionName="0.1">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    
    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="30" />
    
    <application android:label="Voltmatic App"
                 android:theme="@android:style/Theme.Black.NoTitleBar">
        <activity android:name="org.kivy.android.PythonActivity"
                  android:label="Voltmatic App"
                  android:configChanges="keyboardHidden|orientation|screenSize"
                  android:screenOrientation="portrait"
                  android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
        
        with open(project_dir / "AndroidManifest.xml", "w") as f:
            f.write(manifest_content)
        
        # Create resources directory
        res_dir = project_dir / "res" / "values"
        res_dir.mkdir(parents=True)
        
        # Create strings.xml
        strings_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Voltmatic App</string>
</resources>'''
        
        with open(res_dir / "strings.xml", "w") as f:
            f.write(strings_content)
        
        # Create assets directory and copy our app
        assets_dir = project_dir / "assets"
        assets_dir.mkdir()
        
        # Copy Python files
        for py_file in Path(".").glob("*.py"):
            if py_file.name != "create_apk_simple.py":
                shutil.copy2(py_file, assets_dir)
        
        # Copy app directory if it exists
        if Path("app").exists():
            shutil.copytree("app", assets_dir / "app")
        
        # Copy assets directory if it exists
        if Path("assets").exists():
            for item in Path("assets").iterdir():
                if item.is_file():
                    shutil.copy2(item, assets_dir)
                elif item.is_dir():
                    shutil.copytree(item, assets_dir / item.name)
        
        # Create basic Java source (minimal)
        java_dir = project_dir / "src" / "org" / "voltmatic" / "voltmaticapp"
        java_dir.mkdir(parents=True)
        
        # We don't need actual Java code for a Kivy app, just the structure
        
        print("=== BUILDING APK WITH AAPT ===")
        
        # Step 1: Generate R.java (resource file)
        aapt_cmd = f'aapt package -f -m -J {project_dir}/src -M {project_dir}/AndroidManifest.xml -S {project_dir}/res -I {platform}'
        
        if not run_cmd(aapt_cmd, cwd=temp_dir):
            print("AAPT resource generation failed")
            return False
        
        # Step 2: Create APK
        apk_path = Path("bin") / "voltmatic-app-simple.apk"
        aapt_package_cmd = f'aapt package -f -M {project_dir}/AndroidManifest.xml -S {project_dir}/res -A {project_dir}/assets -I {platform} -F {apk_path.absolute()}'
        
        if not run_cmd(aapt_package_cmd, cwd=temp_dir):
            print("AAPT packaging failed")
            return False
        
        print("=== SIGNING APK ===")
        
        # Create debug keystore if needed
        keystore_path = Path.home() / ".android" / "debug.keystore"
        keystore_path.parent.mkdir(exist_ok=True)
        
        if not keystore_path.exists():
            keytool_cmd = f'keytool -genkey -v -keystore {keystore_path} -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -dname "CN=Android Debug,O=Android,C=US"'
            if not run_cmd(keytool_cmd):
                print("Keystore creation failed")
                return False
        
        # Sign APK
        jarsigner_cmd = f'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {keystore_path} -storepass android -keypass android {apk_path.absolute()} androiddebugkey'
        
        if not run_cmd(jarsigner_cmd):
            print("APK signing failed")
            return False
        
        # Align APK
        aligned_apk = Path("bin") / "voltmatic-app.apk"
        zipalign_cmd = f'{build_tools}/zipalign -v 4 {apk_path.absolute()} {aligned_apk.absolute()}'
        
        if run_cmd(zipalign_cmd):
            print(f"SUCCESS: APK created at {aligned_apk}")
            print(f"APK size: {aligned_apk.stat().st_size} bytes")
            return True
        else:
            # If zipalign fails, the signed APK is still usable
            print(f"Zipalign failed, but signed APK available at {apk_path}")
            return True

def main():
    print("=== SIMPLE APK CREATOR ===")
    
    # Check if we have required tools
    required_tools = ['aapt', 'jarsigner', 'keytool']
    for tool in required_tools:
        if not shutil.which(tool):
            print(f"ERROR: {tool} not found in PATH")
            return False
    
    return create_simple_apk()

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ APK CREATION SUCCESSFUL!")
        sys.exit(0)
    else:
        print("❌ APK CREATION FAILED!")
        sys.exit(1)
