# HAR Inspector - Desktop Application

<div align="center">
  <h3>🔍 A Powerful Desktop Tool for Analyzing HTTP Archive Files</h3>
  <p>Inspect, filter, edit, and export HAR files with a modern, privacy-focused desktop application</p>
</div>

## ✨ Features

- **🔒 Privacy First**: All processing happens locally on your computer - no data is sent to any server
- **📊 Comprehensive Analysis**: View detailed information about network requests including headers, body, timings
- **🔎 Smart Filtering**: Search and filter by URL, HTTP method, status code
- **✏️ Edit Capabilities**: Modify request/response data, headers, and content
- **💾 Multiple Export Formats**: Export to CSV for analysis or save modified HAR files
- **🎨 Modern Dark UI**: Clean, professional interface built with CustomTkinter
- **⚡ Fast & Lightweight**: Efficient performance even with large HAR files

## 🚀 Quick Start

### Option 1: Run from Source

**Prerequisites**: Python 3.8 or higher

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python har_inspector.py
   ```

### Option 2: Build Executable

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the build script:
   ```bash
   python build.py
   ```
3. Find the executable in the `dist/` folder

## 📦 Building Installer

For creating a Windows installer (using Inno Setup):

1. Build the executable using the steps above
2. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
3. Create an installer script (see `installer.iss` template)
4. Compile with Inno Setup

For other platforms:
- **Linux**: Create a `.deb` or `.rpm` package, or use AppImage
- **macOS**: Use `py2app` or create a `.dmg` file

## 🎯 How to Use

### Loading a HAR File

1. Launch HAR Inspector
2. Click the upload area or use File → Open
3. Select your `.har` or `.json` file
4. The file will be parsed and displayed

### Viewing Network Requests

- **Browse entries**: Scroll through the list of network requests
- **Search**: Use the search box to filter by URL
- **Filter by method**: Select GET, POST, PUT, DELETE, etc. from the dropdown
- **Click any entry**: View detailed information in the right panel

### Editing Entries

1. Select an entry from the list
2. Click the "✏️ Edit Entry" button
3. Modify URL, method, status, headers, or content
4. Click "Save Changes"

### Exporting Data

- **Export CSV**: Click "📊 Export CSV" to create a spreadsheet with request data
- **Save HAR**: Click "💾 Save HAR" to export the modified HAR file

### Removing Entries

1. Select an entry
2. Click "🗑️ Remove" button
3. Confirm the deletion

## 📋 System Requirements

- **Windows**: Windows 7 or later (64-bit recommended)
- **Linux**: Ubuntu 18.04+, Debian 10+, or similar
- **macOS**: macOS 10.13+ (High Sierra or later)
- **RAM**: 512 MB minimum, 1 GB recommended
- **Disk Space**: 50-100 MB for executable

## 🔧 Dependencies

- **customtkinter**: Modern UI framework for Python
- **Pillow**: Image processing library (required by CustomTkinter)
- **tkinter**: Standard Python GUI library (included with Python)

## 🏗️ Project Structure

```
Har-Inspector/
├── har_inspector.py      # Main application file
├── requirements.txt      # Python dependencies
├── build.py             # Build script for creating executable
├── README_DESKTOP.md    # This file
└── dist/                # Built executables (after build)
```

## 🐛 Troubleshooting

### Application won't start
- Make sure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if tkinter is available: `python -c "import tkinter"`

### HAR file won't load
- Verify the file is valid JSON
- Ensure it has the correct HAR structure (`log.entries`)
- Try opening the file in a text editor to check for corruption

### Build errors
- Update PyInstaller: `pip install --upgrade pyinstaller`
- Clear the build cache: Delete `build/` and `dist/` folders
- Try running with admin/sudo permissions

## 📝 Tips for Creating Small Executables

The build script is optimized for size:

1. **UPX Compression**: Install [UPX](https://upx.github.io/) for additional compression (optional)
2. **Exclude modules**: The build script already excludes unnecessary packages
3. **One-file mode**: Uses `--onefile` for a single executable
4. **Virtual environment**: Build in a clean venv to avoid including unnecessary packages

Expected sizes:
- **Without UPX**: ~40-60 MB
- **With UPX**: ~20-30 MB

## 🔐 Security & Privacy

- **No telemetry**: No analytics or tracking
- **No network access**: Application runs entirely offline (except for loading files)
- **Local processing**: All HAR file processing happens on your machine
- **No cloud storage**: Files are never uploaded anywhere

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📧 Support

For issues, questions, or feedback, please open an issue on GitHub.

---

<div align="center">
  <p>Built with ❤️ using Python and CustomTkinter</p>
  <p>© 2026 HAR Inspector Desktop Edition</p>
</div>
