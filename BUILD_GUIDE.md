# HAR Inspector - Build Guide

This guide provides step-by-step instructions for building the HAR Inspector desktop application into a standalone executable.

## 📋 Prerequisites

### Required Software
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Comes with Python
- **PyInstaller**: Will be installed via requirements.txt

### Optional (for Windows Installer)
- **Inno Setup**: [Download Inno Setup](https://jrsoftware.org/isinfo.php) (Windows only)
- **UPX**: [Download UPX](https://upx.github.io/) for additional compression (optional)

## 🚀 Step-by-Step Build Process

### Step 1: Set Up Python Environment

It's recommended to use a virtual environment to keep dependencies isolated:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- customtkinter (UI framework)
- Pillow (image support)
- pyinstaller (build tool)

### Step 3: Test the Application

Before building, test that the application runs correctly:

```bash
python har_inspector.py
```

- Try loading a HAR file
- Test filtering and searching
- Try editing an entry
- Test exports (CSV and HAR)

### Step 4: Build the Executable

Run the build script:

```bash
python build.py
```

The build process will:
1. Clean previous builds
2. Analyze dependencies
3. Bundle Python and all required libraries
4. Create a single executable file
5. Place the result in the `dist/` folder

**Build time**: 2-5 minutes depending on your system

**Output location**:
- Windows: `dist/HARInspector.exe`
- Linux: `dist/HARInspector`
- Mac: `dist/HARInspector`

### Step 5: Test the Executable

Navigate to the `dist/` folder and run the executable:

**Windows:**
```bash
cd dist
HARInspector.exe
```

**Linux/Mac:**
```bash
cd dist
./HARInspector
```

Test all functionality to ensure everything works correctly.

## 📦 Creating an Installer (Windows)

### Using Inno Setup

1. **Install Inno Setup** from [jrsoftware.org](https://jrsoftware.org/isinfo.php)

2. **Open the installer script**:
   - Launch Inno Setup Compiler
   - Open `installer.iss`

3. **Compile the installer**:
   - Click "Build" → "Compile"
   - Or press F9

4. **Find your installer**:
   - Location: `installer_output/HAR-Inspector-Setup.exe`
   - This is a complete installer that can be distributed

5. **Test the installer**:
   - Run the installer
   - Install the application
   - Test all features
   - Uninstall to verify clean removal

### Customizing the Installer

Edit `installer.iss` to customize:
- App version number
- Publisher information
- Install location
- Start menu items
- Desktop shortcuts
- File associations

## 🎯 Optimizing Executable Size

### Current Size Expectations
- **Basic build**: 40-60 MB
- **With UPX**: 20-30 MB
- **Installer**: 25-35 MB

### Size Optimization Tips

1. **Use UPX Compression** (optional):
   ```bash
   # Install UPX and add to PATH
   # Rebuild with UPX enabled in build.py
   ```

2. **Clean Virtual Environment**:
   - Use a fresh venv with only required packages
   - Avoid installing development tools in the build environment

3. **Exclude Unnecessary Modules**:
   - The build script already excludes common large packages
   - Add more exclusions if you know they're not needed

4. **One-File vs One-Folder**:
   - Current: One-file (larger but simpler)
   - Alternative: One-folder (smaller initial size but multiple files)

## 🔧 Troubleshooting Build Issues

### Common Problems and Solutions

#### Problem: "ModuleNotFoundError" when running executable
**Solution**: Add missing modules to hidden-imports in `build.py`:
```python
'--hidden-import=module_name',
```

#### Problem: Executable is too large
**Solution**:
1. Use a clean virtual environment
2. Enable UPX compression
3. Switch to one-folder mode (edit build.py)

#### Problem: "Failed to execute script" error
**Solution**:
1. Test in non-windowed mode first (remove `--windowed`)
2. Check console output for error messages
3. Verify all data files are collected

#### Problem: CustomTkinter theme issues
**Solution**: Ensure data collection is enabled:
```python
'--collect-data=customtkinter',
```

#### Problem: Build fails on Linux/Mac
**Solution**:
- Install tkinter: `sudo apt-get install python3-tk` (Ubuntu/Debian)
- Install development tools: `sudo apt-get install python3-dev`

## 📝 Advanced Build Options

### Building for Different Platforms

**Windows on Windows**: Standard build works
**Linux on Linux**: Standard build works
**Mac on Mac**: May need code signing for distribution

**Cross-platform building**: Not recommended with PyInstaller
- Build on the target platform for best results
- Use CI/CD services (GitHub Actions) for multi-platform builds

### Debug Build

For debugging, create a console-enabled build:

```python
# In build.py, remove or comment out:
# '--windowed',
```

This will show a console window with error messages.

### Custom Icon

To add a custom application icon:

1. Create an icon file (Windows: .ico, Mac: .icns, Linux: .png)
2. Add to build.py:
   ```python
   '--icon=path/to/icon.ico',
   ```

## 🎨 Branding and Customization

### Application Metadata

Edit the following in `build.py`:
- Application name
- Version number
- Company name
- File description

### UI Customization

Edit `har_inspector.py`:
- Colors and theme
- Window size and layout
- Button text and icons
- Font sizes and families

## 📊 Size Comparison

| Configuration | Approximate Size |
|--------------|------------------|
| Python source code | < 1 MB |
| With dependencies | ~50 MB (venv) |
| PyInstaller (one-file) | 40-60 MB |
| PyInstaller + UPX | 20-30 MB |
| Inno Setup installer | 25-35 MB |

## ✅ Pre-Release Checklist

Before distributing your application:

- [ ] Test on a clean system without Python installed
- [ ] Verify all features work (file loading, editing, exporting)
- [ ] Test with various HAR files (small, large, different formats)
- [ ] Check error handling (invalid files, permissions)
- [ ] Verify installer creates proper shortcuts
- [ ] Test uninstaller removes all files
- [ ] Scan with antivirus (false positives are common with PyInstaller)
- [ ] Create version documentation
- [ ] Prepare release notes

## 🚀 Distribution

### Recommended Distribution Methods

1. **Direct Download**: Host the installer/executable on your website or GitHub Releases
2. **Microsoft Store**: Package as MSIX for Windows Store (additional work required)
3. **Chocolatey**: Create a Chocolatey package for Windows
4. **Snap/Flatpak**: Package for Linux app stores
5. **Homebrew**: Create a formula for macOS

### Signing Your Application

**Windows**: Use `signtool.exe` with a code signing certificate
**Mac**: Use `codesign` with an Apple Developer certificate
**Linux**: Generally not required, but GPG signing is available

## 📞 Support and Help

If you encounter issues:
1. Check the console output (debug build)
2. Review PyInstaller documentation
3. Search GitHub issues for similar problems
4. Create an issue with detailed error messages

## 📚 Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Python Packaging Guide](https://packaging.python.org/)

---

Built with ❤️ for the HAR Inspector community
