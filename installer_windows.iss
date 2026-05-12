[Setup]
AppId={{D6AFA9B8-9A42-4D54-BB0D-8F2863CCED8A}
AppName=HAR Inspector
AppVersion=1.0.0
DefaultDirName={autopf}\HAR Inspector
DefaultGroupName=HAR Inspector
OutputDir=dist
OutputBaseFilename=har-inspector-setup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\har-inspector.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\HAR Inspector"; Filename: "{app}\har-inspector.exe"
Name: "{autodesktop}\HAR Inspector"; Filename: "{app}\har-inspector.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
