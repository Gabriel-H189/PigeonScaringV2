!include "MUI.nsh"

OutFile "PigeonScaringV2Setup.exe"
Name "Pigeon Scaring V2"
InstallDir $ProgramFiles\PigeonScaringV2
BrandingText "Gabriel Alonso-Holt"

!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_ICON "setup.ico"

!define MUI_WELCOMEPAGE_TEXT "Setup will guide you through the installation process of Pigeon Scaring V2.\n\nYou should close all other application before continuing.\n\nClick Next to continue and Cancel to exit the Setup Wizard."

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.rtf"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_DIRECTORY
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Main program"

    SetOutPath $INSTDIR

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2" "DisplayName" "PigeonScaringV2"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2" "DisplayVersion" "2.1.1"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2" "Publisher" "Gabriel Alonso-Holt"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2" "DisplayIcon" "$INSTDIR\Pigeon.ico"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2" "NoRepair" 1
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2" "UninstallString" "$INSTDIR\uninstall.exe"

    File PigeonScaringV2.exe
    File psv2cfg.ini
    File pigeon.png
    File icon.ico
    File psv2_log.txt

    CreateShortcut "$SMPROGRAMS\PigeonScaringV2.lnk" "$INSTDIR\PigeonScaringV2.exe"

    WriteUninstaller $INSTDIR\uninstall.exe

SectionEnd

Section "Gabriel's Pigeon Sound Pack"

    File /r media

SectionEnd

Section "Desktop shortcut"

    CreateShortcut "$DESKTOP\PigeonScaringV2.lnk" "$INSTDIR\PigeonScaringV2.exe"

SectionEnd

Section "Uninstall"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PigeonScaringV2"

    Delete $INSTDIR\PigeonScaringV2.exe
    Delete $INSTDIR\psv2cfg.ini
    Delete $INSTDIR\Pigeon.png
    Delete $INSTDIR\icon.ico
    Delete $INSTDIR\psv2_log.txt
    Delete $INSTDIR\media\pigeon.wav
    Delete $DESKTOP\PigeonScaringV2.lnk
    Delete $SMPROGRAMS\PigeonScaringV2.lnk
    RMDir /r $INSTDIR\media

    Delete $INSTDIR\uninstall.exe
    RMDir $INSTDIR

SectionEnd