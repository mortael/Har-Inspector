# HAR Inspector Desktop - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Python (if not already installed)
Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)

### 2. Run the Application

#### Windows
Double-click `run.bat` or open Command Prompt and run:
```cmd
run.bat
```

#### Linux/macOS
Open Terminal and run:
```bash
./run.sh
```

Or use Python directly:
```bash
python3 run.py
```

### 3. Use the Application
1. Click the upload area to select a HAR file
2. Browse and filter network entries
3. Click any entry to view details
4. Edit, export, or remove entries as needed

## 📖 Documentation

- **README_DESKTOP.md** - Full application documentation
- **BUILD_GUIDE.md** - How to build executables and installers
- **CONVERSION_SUMMARY.md** - Technical details about the conversion

## 🛠️ Building an Executable

### Quick Build
```bash
pip install pyinstaller
python build.py
```

The executable will be in `dist/HARInspector.exe` (Windows) or `dist/HARInspector` (Linux/Mac)

### Creating an Installer (Windows)
1. Build the executable (above)
2. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
3. Open `installer.iss` in Inno Setup
4. Click "Compile"
5. Find the installer in `installer_output/HAR-Inspector-Setup.exe`

## ✨ Key Features

- ✅ Load and parse HAR files
- ✅ Search and filter by URL and HTTP method
- ✅ View detailed request/response information
- ✅ Edit entries (URL, method, status, headers, body)
- ✅ Remove unwanted entries
- ✅ Export to CSV or modified HAR
- ✅ Dark theme UI
- ✅ 100% offline - complete privacy

## 🆘 Need Help?

### Common Issues

**Python not found?**
- Install Python 3.8+ from python.org
- Make sure "Add to PATH" is checked during installation

**Dependencies missing?**
```bash
pip install -r requirements.txt
```

**tkinter not found?** (Linux only)
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install python3-tkinter  # CentOS/RHEL
```

### More Information

See the full documentation in `README_DESKTOP.md` and `BUILD_GUIDE.md`

## 📦 Distribution

### Pre-built Executables
Coming soon - check GitHub Releases

### Manual Build
Follow the BUILD_GUIDE.md to create your own executable

## 🎯 What's Included

```
Har-Inspector/
├── har_inspector.py          # Main application (900+ lines)
├── run.py                    # Quick launcher with dependency checks
├── run.bat                   # Windows launcher
├── run.sh                    # Unix/Linux/Mac launcher
├── build.py                  # Build script for PyInstaller
├── installer.iss             # Inno Setup installer script
├── requirements.txt          # Python dependencies
├── README_DESKTOP.md         # Full documentation
├── BUILD_GUIDE.md            # Build instructions
└── CONVERSION_SUMMARY.md     # Conversion details
```

## 💡 Tips

1. **First Time Users**: Run `run.py` - it checks dependencies and guides you
2. **Developers**: Run `python har_inspector.py` directly after installing dependencies
3. **End Users**: Use the built executable (no Python needed)

## 🔒 Privacy

- All processing happens locally on your computer
- No internet connection required
- No data is sent to any server
- HAR files remain on your machine

## 📝 System Requirements

- **OS**: Windows 7+, Ubuntu 18.04+, macOS 10.13+
- **Python**: 3.8+ (for running from source)
- **RAM**: 512 MB minimum, 1 GB recommended
- **Disk**: 50-100 MB for executable

## 🎨 Screenshots

The application features:
- Modern dark theme interface
- Responsive layout
- Intuitive navigation
- Professional design

---

**Ready to start?** Just run `run.bat` (Windows) or `./run.sh` (Linux/Mac)!

For detailed instructions, see `README_DESKTOP.md`
