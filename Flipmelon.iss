#define MyAppName "Flipmelon"
#define MyAppVersion "1.0.8.9"
#define MyAppExeName "Flipmelon.exe"
[Setup]
AppId={{A45F9F5B-81F7-40F0-9F5B-94D9AF81E7C2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Flipmelon
DefaultDirName={localappdata}\Programs\Flipmelon
DefaultGroupName=Flipmelon
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED
SetupIconFile=flipmelon.ico
WizardImageFile=assets\installer-side.bmp
WizardSmallImageFile=assets\installer-small.bmp
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
; Experimental multi-file setup: avoids the temporary SetupLdr executable.
; MUST ship the .exe together with the generated .bin files.
UseSetupLdr=no
PrivilegesRequired=lowest
WizardStyle=modern
ArchitecturesAllowed=x64compatible
CloseApplications=yes
RestartApplications=no
SetupLogging=yes
[InstallDelete]
Type: files; Name: "{app}\AutoDock.exe"
Type: files; Name: "{autoprograms}\AutoDock.lnk"
Type: files; Name: "{autodesktop}\AutoDock.lnk"
Type: files; Name: "{userappdata}\Microsoft\Windows\Start Menu\Programs\Startup\AutoDock.vbs"
Type: files; Name: "{userappdata}\Microsoft\Windows\Start Menu\Programs\Startup\AutoDock.lnk"
[Files]
Source: "dist\Flipmelon\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
[Icons]
Name: "{autoprograms}\Flipmelon"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Flipmelon"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; Flags: checkedonce
[Run]
Filename: "{app}\{#MyAppExeName}"; Parameters: "--setup"; Description: "Abrir Flipmelon e configurar meu Android"; Flags: nowait postinstall skipifsilent
