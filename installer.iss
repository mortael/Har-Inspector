; HAR Inspector Installer Script for Inno Setup
; This script creates a professional Windows installer

#define MyAppName "HAR Inspector"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "HAR Inspector Team"
#define MyAppURL "https://github.com/mortael/Har-Inspector"
#define MyAppExeName "HARInspector.exe"

[Setup]
; Basic app information
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; Uncomment the following line to run in non-administrative install mode
; PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer_output
OutputBaseFilename=HAR-Inspector-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; Installer size optimization
DisableDirPage=auto
DisableProgramGroupPage=auto

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; The executable from PyInstaller dist folder
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Add README
Source: "README_DESKTOP.md"; DestDir: "{app}"; DestName: "README.txt"; Flags: ignoreversion
; Add example HAR file if you have one
; Source: "examples\sample.har"; DestDir: "{app}\examples"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
