<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# HAR Inspector - Network Archive Tool

A powerful tool to inspect, filter, edit, and convert HTTP Archive (HAR) files. Available as both a web application and a desktop application.

## 🎯 Choose Your Version

### 🖥️ Desktop Application (Recommended)

A standalone Python desktop application with a modern GUI.

**Features:**
- ✅ Complete offline operation - maximum privacy
- ✅ No installation required (use pre-built executable)
- ✅ Native OS integration
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Modern dark theme UI

**Quick Start:**
```bash
# Run from source
python3 run.py

# Or use the launcher scripts
./run.sh          # Linux/Mac
run.bat           # Windows
```

**📖 Documentation:** See [README_DESKTOP.md](README_DESKTOP.md) and [QUICKSTART.md](QUICKSTART.md)

### 🌐 Web Application

A React-based web application that runs in your browser.

**Quick Start:**

**Prerequisites:** Node.js

1. Install dependencies:
   ```bash
   npm install
   ```
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   ```bash
   npm run dev
   ```

View in AI Studio: https://ai.studio/apps/5a5a1cae-77d2-4b56-8675-e6c9be4344db

## 📋 Features

Both versions include:

- 📁 Load and parse HAR files
- 🔍 Search and filter network requests
- 📊 View detailed request/response information
- ✏️ Edit entries (URL, method, status, headers, body)
- 🗑️ Remove unwanted entries
- 💾 Export to CSV or modified HAR files
- 🔒 Privacy-focused (client-side/offline processing)

## 🚀 Building Desktop Executable

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed instructions.

Quick build:
```bash
pip install pyinstaller
python build.py
```

Output: `dist/HARInspector.exe` (Windows) or `dist/HARInspector` (Linux/Mac)

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide for desktop app
- [README_DESKTOP.md](README_DESKTOP.md) - Desktop app documentation
- [BUILD_GUIDE.md](BUILD_GUIDE.md) - Building executables and installers
- [CONVERSION_SUMMARY.md](CONVERSION_SUMMARY.md) - Web to desktop conversion details

## 📝 License

Apache License 2.0

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

© 2026 HAR Inspector. Built for developers.
