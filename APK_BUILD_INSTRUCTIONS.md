# Voltmatic Energy Solutions - Android App

This is the Android application for Voltmatic Energy Solutions, built with Kivy and KivyMD.

## Building the APK

### Prerequisites

1. **GitHub Account** - To use GitHub Actions for building the APK
2. **Android Device** - For testing the APK (or use an emulator)
3. **Basic Git Knowledge** - To clone the repository and push changes

### Building with GitHub Actions

The easiest way to build the APK is using GitHub Actions:

1. **Fork this repository** to your GitHub account
2. **Enable GitHub Actions** in your forked repository
3. **Trigger a build** by pushing a commit or manually triggering the workflow:
   - Go to the "Actions" tab
   - Select "Build Android APK" workflow
   - Click "Run workflow"

4. **Download the APK** after the build completes:
   - Go to the completed workflow run
   - Download the "voltmatic-apk" artifact
   - Install on your Android device

### Building Locally (Advanced)

If you need to build locally, follow these steps:

1. **Set up a Linux environment** (WSL2, Linux VM, or native Linux)
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev libltdl-dev
   ```

3. **Install Buildozer**:
   ```bash
   pip install --user --upgrade buildozer==1.5.0 cython==0.29.33
   ```

4. **Build the APK**:
   ```bash
   # Initialize buildozer (only needed once)
   buildozer init
   
   # Build the APK
   buildozer -v android debug
   ```

5. **Find the APK** in the `bin/` directory

## Troubleshooting

### Common Build Issues

1. **Build fails with NDK errors**:
   - Make sure you're using NDK version 23b
   - Clean the build directory: `rm -rf .buildozer`

2. **APK crashes on launch**:
   - Check logcat for errors: `adb logcat | grep python`
   - Make sure all required permissions are in `buildozer.spec`

3. **Missing dependencies**:
   - Check the build log for missing Python packages
   - Add them to `requirements` in `buildozer.spec`

### GitHub Actions Specific

1. **Build fails with exit code 100**:
   - Check the build log in the Actions tab
   - Look for specific error messages about missing dependencies or configuration

2. **APK not generated**:
   - Check the build log for errors
   - Make sure the build completed successfully
   - Look for the APK in the workflow artifacts

## Deployment

### Testing the APK

1. Enable "Unknown Sources" in your Android settings
2. Install the APK using a file manager or adb:
   ```bash
   adb install -r bin/voltmaticsitesurvey-*-debug.apk
   ```

### Releasing to Production

1. Create a signed APK:
   - Set up keystore credentials in GitHub Secrets:
     - `P4A_RELEASE_KEYSTORE` - Base64 encoded keystore file
     - `P4A_RELEASE_KEYSTORE_PASSWD` - Keystore password
     - `P4A_RELEASE_KEYALIAS_PASSWD` - Key password
     - `P4A_RELEASE_KEYALIAS` - Key alias
   - Update `buildozer.spec` with your release settings
   - Trigger a release build in GitHub Actions

## Support

For issues and feature requests, please create an issue in the GitHub repository.
