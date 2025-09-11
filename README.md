# Voltmatic Energy Solutions - Site Survey App

A professional Android application for conducting solar site surveys, built with Python and Kivy.

## Features

- **Modern, Professional UI** - Clean and intuitive interface designed for field technicians
- **Site Survey Management** - Create, view, and manage site surveys
- **Client Management** - Store and manage client information
- **Reports** - Generate detailed survey reports
- **Offline Capable** - Work without an internet connection
- **Cross-Platform** - Runs on Android, Windows, and other platforms

## Requirements

- Python 3.7+
- Kivy 2.0.0+
- KivyMD 1.0.0+
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd android
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download and prepare assets:
   ```bash
   python download_assets.py
   ```

## Running the App

### On Desktop
```bash
python main.py
```

### On Android
1. Install Buildozer:
   ```bash
   pip install buildozer
   pip install cython==0.29.33
   ```

2. Initialize buildozer:
   ```bash
   buildozer init
   ```

3. Build the APK:
   ```bash
   buildozer -v android debug
   ```

## Project Structure

```
.
├── app/                      # Application code
│   ├── screens/             # Screen definitions
│   ├── widgets/             # Custom widgets
│   └── theme/               # Theme and styling
├── assets/                  # Static assets
│   ├── images/              # Image files
│   └── icons/               # Icon files
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Kivy](https://kivy.org/) - The framework used
- [KivyMD](https://kivymd.readthedocs.io/) - Material Design components
- [Voltmatic Energy Solutions](https://voltmaticenergysolutions.co.ke/) - For the opportunity
