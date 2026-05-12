; Inno Setup script for Har Inspector Desktop
; Build the EXE first (see desktop/README.md), then compile this installer.

#define AppName "HAR Inspector"
#define AppExeName "HarInspector.exe"
#define AppVersion "0.1.0"
#define AppPublisher "HAR Inspector"

[Setup]
AppId={{E2A1B85B-4C3F-4D8E-93F1-0A56E5CFB2CC}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputBaseFilename=HarInspectorSetup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes

[Files]
Source: "..\\..\\dist\\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\\{#AppName}"; Filename: "{app}\\{#AppExeName}"
Name: "{autodesktop}\\{#AppName}"; Filename: "{app}\\{#AppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

