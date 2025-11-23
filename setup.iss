[Setup]
AppName=ClipOmnia
AppVersion=1.0
DefaultDirName={pf}\ClipOmnia
DefaultGroupName=ClipOmnia
OutputDir=dist_installer
OutputBaseFilename=ClipOmniaInstaller
;SetupIconFile=Icon.ico
Compression=lzma
SolidCompression=yes

[Files]
; Your PyInstaller executable
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

; All assets folder
Source: "src\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

; Optional: any other directories (components, utils) if needed
; Source: "src\components\*"; DestDir: "{app}\components"; Flags: ignoreversion recursesubdirs
; Source: "src\utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs

[Icons]
; Shortcut in Start Menu
Name: "{group}\ClipOmnia"; Filename: "{app}\main.exe"; IconFilename: "{app}\assets\Icon.ico"

; Optional: Desktop shortcut
Name: "{userdesktop}\ClipOmnia"; Filename: "{app}\main.exe"; IconFilename: "{app}\assets\Icon.ico"; Tasks: desktopicon

; Autostart shortcut
Name: "{userstartup}\ClipOmnia"; Filename: "{app}\main.exe"; IconFilename: "{app}\assets\Icon.ico"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

;[Registry]
; Run for current user
;Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
;    ValueType: string; ValueName: "ClipOmnia"; ValueData: """{app}\main.exe"""; Flags: uninsdeletevalue
