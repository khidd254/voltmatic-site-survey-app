[app]

# (str) Title of your application
title = Voltmatic App

# (str) Package name
package.name = voltmaticapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.voltmatic

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow==9.5.0,requests==2.28.2,python-dateutil==2.8.2,plyer==2.1.0,pyjnius==1.4.2,android

# Orientation and display
orientation = portrait
fullscreen = 0

# Android specific
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 30
android.minapi = 21
android.ndk = 25.2.9519653
android.ndk_path = /opt/android-sdk/ndk/25.2.9519653
android.sdk_path = /opt/android-sdk
android.private_storage = True
android.accept_sdk_license = True

# Build tools configuration
android.gradle_dependencies = 
android.add_compile_options = 
android.add_gradle_repositories = 
android.gradle_repositories = google(), mavenCentral()

# Kivy configuration
android.entrypoint = org.kivy.android.PythonActivity
android.enable_androidx = True
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
