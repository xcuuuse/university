VERSION 4.00
Begin VB.Form frmMainWin 
   Caption         =   "Visual Map Tools Sample"
   ClientHeight    =   7770
   ClientLeft      =   1200
   ClientTop       =   2430
   ClientWidth     =   10545
   Height          =   8490
   Icon            =   "MainWin.frx":0000
   Left            =   1140
   LinkTopic       =   "Form1"
   ScaleHeight     =   7770
   ScaleWidth      =   10545
   Top             =   1770
   Width           =   10665
   WindowState     =   2  'Maximized
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
      _Version        =   65536
      _ExtentX        =   847
      _ExtentY        =   847
      _StockProps     =   0
      CancelError     =   -1  'True
      DialogTitle     =   "Open MapInfo Table"
   End
   Begin ComctlLib.ImageList imgsToolbar 
      Left            =   1200
      Top             =   840
      _Version        =   65536
      _ExtentX        =   1005
      _ExtentY        =   1005
      _StockProps     =   1
      ImageWidth      =   16
      ImageHeight     =   16
      MaskColor       =   12632256
      NumImages       =   6
      i1              =   "MainWin.frx":030A
      i2              =   "MainWin.frx":04C1
      i3              =   "MainWin.frx":0678
      i4              =   "MainWin.frx":082F
      i5              =   "MainWin.frx":09E6
      i6              =   "MainWin.frx":0B9D
   End
   Begin ComctlLib.Toolbar tbarMain 
      Align           =   1  'Align Top
      Height          =   390
      Left            =   0
      TabIndex        =   7
      Top             =   0
      Width           =   10545
      _Version        =   65536
      _ExtentX        =   18600
      _ExtentY        =   688
      _StockProps     =   96
      ImageList       =   "imgsToolbar"
      NumButtons      =   6
      i1              =   "MainWin.frx":0D54
      i2              =   "MainWin.frx":0F1D
      i3              =   "MainWin.frx":10CC
      i4              =   "MainWin.frx":127B
      i5              =   "MainWin.frx":142A
      i6              =   "MainWin.frx":15E1
      AlignSet        =   -1  'True
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
   Begin ComctlLib.TreeView tvwInfo 
      Height          =   3255
      Left            =   7200
      TabIndex        =   2
      Top             =   4560
      Width           =   3375
      _Version        =   65536
      _ExtentX        =   5953
      _ExtentY        =   5741
      _StockProps     =   196
      Appearance      =   1
      ImageList       =   ""
      LineStyle       =   1
      PathSeparator   =   "\"
      Style           =   6
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
Attribute VB_Creatable = False
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


