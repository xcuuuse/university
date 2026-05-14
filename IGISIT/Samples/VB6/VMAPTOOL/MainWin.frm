VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "Comdlg32.ocx"
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "Comctl32.ocx"
Begin VB.Form frmMainWin 
   Caption         =   "Visual Map Tools Sample"
   ClientHeight    =   7770
   ClientLeft      =   1200
   ClientTop       =   2430
   ClientWidth     =   10545
   Icon            =   "MainWin.frx":0000
   LinkTopic       =   "Form1"
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   7770
   ScaleWidth      =   10545
   WindowState     =   2  'Maximized
   Begin ComctlLib.Toolbar tbarMain 
      Align           =   1  'Align Top
      Height          =   390
      Left            =   0
      TabIndex        =   7
      Top             =   0
      Width           =   10545
      _ExtentX        =   18600
      _ExtentY        =   688
      ButtonWidth     =   635
      ButtonHeight    =   582
      ImageList       =   "imgsToolbar"
      _Version        =   327682
      BeginProperty Buttons {0713E452-850A-101B-AFC0-4210102A8DA7} 
         NumButtons      =   6
         BeginProperty Button1 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "select"
            Object.ToolTipText     =   "Select Tool"
            Object.Tag             =   ""
            ImageIndex      =   1
            Style           =   2
            Value           =   1
         EndProperty
         BeginProperty Button2 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "grabber"
            Object.ToolTipText     =   "Grabber Tool"
            Object.Tag             =   ""
            ImageIndex      =   2
            Style           =   2
         EndProperty
         BeginProperty Button3 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "zoomin"
            Object.ToolTipText     =   "Zoom In Tool"
            Object.Tag             =   ""
            ImageIndex      =   3
            Style           =   2
         EndProperty
         BeginProperty Button4 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "zoomout"
            Object.ToolTipText     =   "Zoom Out Tool"
            Object.Tag             =   ""
            ImageIndex      =   4
            Style           =   2
         EndProperty
         BeginProperty Button5 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "info_pt"
            Object.ToolTipText     =   "Point Select Info Tool"
            Object.Tag             =   ""
            ImageIndex      =   5
            Style           =   2
         EndProperty
         BeginProperty Button6 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "info_rt"
            Object.ToolTipText     =   "Marquee Select Info Tool"
            Object.Tag             =   ""
            ImageIndex      =   6
            Style           =   2
         EndProperty
      EndProperty
   End
   Begin VB.ListBox lstLayers 
      Height          =   3375
      Left            =   7200
      TabIndex        =   1
      Top             =   600
      Width           =   3375
   End
   Begin VB.PictureBox picMapFrame 
      Height          =   5775
      Left            =   0
      ScaleHeight     =   381
      ScaleMode       =   3  'Pixel
      ScaleWidth      =   477
      TabIndex        =   0
      Top             =   1800
      Width           =   7215
      Begin VB.Label Label2 
         Caption         =   "Label2"
         Height          =   135
         Left            =   7200
         TabIndex        =   5
         Top             =   3960
         Width           =   15
      End
      Begin VB.Label Label1 
         Caption         =   "Label1"
         Height          =   255
         Left            =   7200
         TabIndex        =   3
         Top             =   0
         Width           =   15
      End
   End
   Begin MSComDlg.CommonDialog dlgOpenTable 
      Left            =   1920
      Top             =   840
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
      CancelError     =   -1  'True
      DialogTitle     =   "Open MapInfo Table"
   End
   Begin ComctlLib.TreeView tvwInfo 
      Height          =   3255
      Left            =   7200
      TabIndex        =   2
      Top             =   4560
      Width           =   3375
      _ExtentX        =   5953
      _ExtentY        =   5741
      _Version        =   327682
      LineStyle       =   1
      Style           =   6
      Appearance      =   1
   End
   Begin ComctlLib.ImageList imgsToolbar 
      Left            =   1200
      Top             =   840
      _ExtentX        =   1005
      _ExtentY        =   1005
      BackColor       =   -2147483633
      ImageWidth      =   16
      ImageHeight     =   16
      MaskColor       =   12632256
      _Version        =   327682
      BeginProperty Images {0713E8C2-850A-101B-AFC0-4210102A8DA7} 
         NumListImages   =   6
         BeginProperty ListImage1 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "MainWin.frx":030A
            Key             =   ""
         EndProperty
         BeginProperty ListImage2 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "MainWin.frx":041C
            Key             =   ""
         EndProperty
         BeginProperty ListImage3 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "MainWin.frx":052E
            Key             =   ""
         EndProperty
         BeginProperty ListImage4 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "MainWin.frx":0640
            Key             =   ""
         EndProperty
         BeginProperty ListImage5 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "MainWin.frx":0752
            Key             =   ""
         EndProperty
         BeginProperty ListImage6 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "MainWin.frx":0864
            Key             =   ""
         EndProperty
      EndProperty
   End
   Begin VB.Label lblInfo 
      Caption         =   "Info Tool Hits:"
      Height          =   255
      Left            =   7200
      TabIndex        =   6
      Top             =   4320
      Width           =   3375
   End
   Begin VB.Label lblLayers 
      Caption         =   "Layers:"
      Height          =   255
      Left            =   7200
      TabIndex        =   4
      Top             =   360
      Width           =   3375
   End
   Begin VB.Menu mnuFile 
      Caption         =   "&File"
      Begin VB.Menu mnuFileOpen 
         Caption         =   "&Open Table..."
         Shortcut        =   ^O
      End
      Begin VB.Menu mnuFileClose 
         Caption         =   "&Close Selected Layer"
      End
      Begin VB.Menu sep1 
         Caption         =   "-"
      End
      Begin VB.Menu mnuFileExit 
         Caption         =   "E&xit"
      End
   End
End
Attribute VB_Name = "frmMainWin"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False


Private Sub Form_Load()
    InitializeMapInfoConnection         '* setup MapInfo to work with us
End Sub

Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    ShutdownMapInfoConnection       '* cleanly disconnect from MapInfo
End Sub
Private Sub Form_Resize()
    Dim hPane As Long       '* Right edge of map frame
    Dim vPane As Long       '* Boundary between the ListBox & the TreeView
    Dim mapHWnd As Long     '* the hWnd of the mapper window in MapInfo.

'* only do the resize logic if the window was not minimized.
    If frmMainWin.WindowState <> 1 Then

    '* first, make sure the window wasn't made too small:
        If frmMainWin.WindowState <> 2 Then
            If frmMainWin.ScaleHeight <= (tbarMain.Height + lblLayers.Height + lblInfo.Height) Then
                frmMainWin.Width = 5445
                frmMainWin.Height = 3615
            End If
        End If

'* The basic logic here is that the PictureBox is 2/3 the width of the entire form,
'* minus a small border width defined by the constant kBorder (defined in MapInfo.bas)
'* The "Layers" listbox and "Info Tool" TreeView each take up 1/2 the height of
'* the remaining 1/3 of the form.
        hPane = 2 * frmMainWin.ScaleWidth / 3
        vPane = tbarMain.Height + (frmMainWin.ScaleHeight - tbarMain.Height) / 2
    
        picMapFrame.Left = kPaneMargin
        picMapFrame.Top = tbarMain.Height + kPaneMargin
        picMapFrame.Width = hPane - 2 * kPaneMargin
        picMapFrame.Height = frmMainWin.ScaleHeight - tbarMain.Height - 2 * kPaneMargin
    
        lblLayers.Left = hPane + kPaneMargin
        lblLayers.Top = tbarMain.Height + kPaneMargin
        lblLayers.Width = frmMainWin.ScaleWidth - hPane - 2 * kPaneMargin
    
        lstLayers.Left = hPane + kPaneMargin
        lstLayers.Top = tbarMain.Height + lblLayers.Height + kPaneMargin
        lstLayers.Width = frmMainWin.ScaleWidth - hPane - 2 * kPaneMargin
        lstLayers.Height = vPane - lblLayers.Height - tbarMain.Height - 2 * kPaneMargin
    
        lblInfo.Left = hPane + kPaneMargin
        lblInfo.Top = vPane + kPaneMargin
        lblInfo.Width = frmMainWin.ScaleWidth - hPane - 2 * kPaneMargin
    
        tvwInfo.Left = hPane + kPaneMargin
        tvwInfo.Top = vPane + lblInfo.Height + kPaneMargin
        tvwInfo.Width = frmMainWin.ScaleWidth - hPane - 2 * kPaneMargin
        tvwInfo.Height = (frmMainWin.ScaleHeight - vPane) - lblInfo.Height - 2 * kPaneMargin
    
    '* Now, if a map is open, tell MapInfo to resize it to fit the new picture frame.
    '* for the call to the Windows API function "MoveWindow()" to work, the "ScaleMode"
    '* property of the PictureBox into which the map window has been reparented must be
    '* set to "Pixels".
        If thereIsAMap Then
            mapHWnd = CLng(MapInfo.Eval("WindowInfo(" & mapWinID & "," & WIN_INFO_WND & ")"))
    
            MoveWindow mapHWnd, 0, 0, picMapFrame.ScaleWidth, picMapFrame.ScaleHeight, 0
        End If
    End If
End Sub


Private Sub lstLayers_Click()
    UpdateMenuAndToolbar    '* when the user clicks in the "Layers" list box, the "Close" menu
                            '* item may become disabled, so we make sure it and alll other menu
                            '* items are properly enabled/disabled
End Sub

Private Sub mnuFileClose_Click()
    CloseSelectedLayer
End Sub

Private Sub mnuFileExit_Click()
    End     '* the Form's QueryUnload event handler will make sure we cleanly exit
End Sub

Private Sub mnuFileOpen_Click()
    OpenATable
End Sub

Public Sub tbarMain_ButtonClick(ByVal Button As Button)
    Select Case Button.Key
        Case "select"
            MapInfo.RunMenuCommand M_TOOLS_SELECTOR     '* make MapInfo's select tool active
        Case "grabber"
            MapInfo.RunMenuCommand M_TOOLS_RECENTER     '* make MapInfo's grabber tool active
        Case "zoomin"
            MapInfo.RunMenuCommand M_TOOLS_EXPAND       '* make MapInfo's zoom in tool active
        Case "zoomout"
            MapInfo.RunMenuCommand M_TOOLS_SHRINK       '* make MapInfo's zoom in tool active
        Case "info_pt"
            MapInfo.Do "Run Menu Command ID 2001"       '* make our first custom tool active
        Case "info_rt"
            MapInfo.Do "Run Menu Command ID 2002"       '* make our second custom tool active
    End Select
End Sub

Private Sub tvwInfo_BeforeLabelEdit(Cancel As Integer)
    Cancel = 1      '* cancel the action so the user can't edit the fields in the control
End Sub


