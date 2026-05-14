; CLW file contains information for the MFC ClassWizard

[General Info]
Version=1
LastClass=CFindzipApp
LastTemplate=CDialog
NewFileInclude1=#include "stdafx.h"
NewFileInclude2=#include "findzip.h"
ODLFile=findzip.odl
LastPage=0

ClassCount=6
Class1=CFindzipApp
Class2=CFindzipDoc
Class3=CFindzipView
Class4=CMainFrame

ResourceCount=3
Resource1=IDD_ABOUTBOX
Resource2=IDR_MAINFRAME
Class5=CAboutDlg
Class6=CFindZipDlg
Resource3=IDD_FINDZIP

[CLS:CFindzipApp]
Type=0
HeaderFile=findzip.h
ImplementationFile=findzip.cpp
Filter=N
BaseClass=CWinApp
VirtualFilter=AC
LastObject=CFindzipApp

[CLS:CFindzipDoc]
Type=0
HeaderFile=findzdoc.h
ImplementationFile=findzdoc.cpp
Filter=N
VirtualFilter=DC
LastObject=CFindzipDoc

[CLS:CFindzipView]
Type=0
HeaderFile=findzvw.h
ImplementationFile=findzvw.cpp
Filter=C
LastObject=ID_FILE_PRINTMAP
VirtualFilter=VWC

[CLS:CMainFrame]
Type=0
HeaderFile=mainfrm.h
ImplementationFile=mainfrm.cpp
Filter=T
LastObject=ID_MAP_LAYERCONTROL



[CLS:CAboutDlg]
Type=0
HeaderFile=findzip.cpp
ImplementationFile=findzip.cpp
Filter=D
VirtualFilter=dWC
LastObject=CAboutDlg

[DLG:IDD_ABOUTBOX]
Type=1
Class=CAboutDlg
ControlCount=4
Control1=IDC_STATIC,static,1342177283
Control2=IDC_STATIC,static,1342308352
Control3=IDC_STATIC,static,1342308352
Control4=IDOK,button,1342373889

[MNU:IDR_MAINFRAME]
Type=1
Class=CMainFrame
Command1=ID_FILE_PRINTMAP
Command2=ID_APP_EXIT
Command3=ID_VIEW_TOOLBAR
Command4=ID_VIEW_STATUS_BAR
Command5=ID_MAP_LAYERCONTROL
Command6=ID_MAP_CREATETHEME
Command7=ID_MAP_VIEWENTIRELAYER
Command8=ID_TOOLBAR_FINDZIP
Command9=ID_APP_ABOUT
CommandCount=9

[ACL:IDR_MAINFRAME]
Type=1
Class=CMainFrame
Command1=ID_EDIT_COPY
Command2=ID_MAP_LAYERCONTROL
Command3=ID_FILE_NEW
Command4=ID_FILE_OPEN
Command5=ID_FILE_SAVE
Command6=ID_EDIT_PASTE
Command7=ID_EDIT_UNDO
Command8=ID_EDIT_CUT
Command9=ID_NEXT_PANE
Command10=ID_PREV_PANE
Command11=ID_EDIT_COPY
Command12=ID_EDIT_PASTE
Command13=ID_EDIT_CUT
Command14=ID_EDIT_UNDO
CommandCount=14

[DLG:IDD_FINDZIP]
Type=1
Class=CFindZipDlg
ControlCount=4
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_STATIC,static,1342308352
Control4=IDC_ZIP,edit,1350631552

[CLS:CFindZipDlg]
Type=0
HeaderFile=fzipdlg.h
ImplementationFile=fzipdlg.cpp
Filter=D
LastObject=CFindZipDlg
VirtualFilter=dWC

