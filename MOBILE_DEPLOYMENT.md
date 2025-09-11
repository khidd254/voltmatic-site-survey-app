# Mobile Deployment Guide

## ⚠️ Windows Limitation
**Buildozer does not support Android builds on Windows** - it only supports iOS targets. For Android development on Windows, use the alternative methods below.

## Alternative Android Build Methods for Windows

### Method 1: WSL2 + Linux Environment (Recommended)
1. **Install WSL2** with Ubuntu:
   ```powershell
   wsl --install -d Ubuntu
   ```

2. **Inside WSL2**, install dependencies:
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   pip3 install --user --upgrade buildozer cython==0.29.33
   ```

3. **Copy project to WSL2**:
   ```bash
   cp -r /mnt/c/Users/user/CascadeProjects/android ~/voltmatic-android
   cd ~/voltmatic-android
   ```

4. **Build and deploy**:
   ```bash
   buildozer android debug deploy
   ```

### Method 2: Docker Container
1. **Create Dockerfile**:
   ```dockerfile
   FROM kivy/buildozer:latest
   WORKDIR /app
   COPY . /app
   RUN buildozer android debug
   ```

2. **Build with Docker**:
   ```bash
   docker build -t voltmatic-app .
   docker run -v ${PWD}:/app voltmatic-app
   ```

## Alternative Methods

### Method 1: Using Pydroid 3 (Easiest)
1. Install **Pydroid 3** from Google Play Store
2. Copy your project files to phone storage
3. Install required packages in Pydroid 3:
   ```python
   pip install kivy kivymd
   ```
4. Run `main.py` directly in Pydroid 3

### Method 2: Using Termux
1. Install **Termux** from F-Droid
2. Install Python and dependencies:
   ```bash
   pkg install python
   pip install kivy kivymd
   ```
3. Copy project files and run

## Troubleshooting

### Common Issues:
1. **Build fails**: Check Android SDK/NDK paths
2. **App crashes**: Check permissions in buildozer.spec
3. **Import errors**: Verify all dependencies in requirements

### Required Permissions:
- INTERNET (for future updates)
- WRITE_EXTERNAL_STORAGE (for database)
- READ_EXTERNAL_STORAGE (for assets)
- CALL_PHONE (for calling clients)
- READ_PHONE_STATE (for call functionality)

## Quick Test Method

**For immediate testing without building:**

1. Install **Pydroid 3** on your phone
2. Copy the entire project folder to your phone
3. Open Pydroid 3 and navigate to the project folder
4. Install dependencies:
   ```
   pip install kivy==2.3.1
   pip install kivymd==1.1.1
   ```
5. Run `main.py`

This should work immediately without any build process.
