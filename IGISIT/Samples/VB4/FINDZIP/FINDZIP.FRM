VERSION 4.00
Begin VB.Form FindZipForm 
   Appearance      =   0  'Flat
   AutoRedraw      =   -1  'True
   BackColor       =   &H00C0C0C0&
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Find 5-Digit Zip Code"
   ClientHeight    =   5925
   ClientLeft      =   1170
   ClientTop       =   1980
   ClientWidth     =   8970
   BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
      Name            =   "MS Sans Serif"
      Size            =   8.25
      Charset         =   0
      Weight          =   700
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   ForeColor       =   &H80000008&
   Height          =   6615
   Left            =   1110
   LinkMode        =   1  'Source
   LinkTopic       =   "MainForm"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   5925
   ScaleWidth      =   8970
   Top             =   1350
   Width           =   9090
   Begin VB.PictureBox MapFrame 
      Appearance      =   0  'Flat
      AutoRedraw      =   -1  'True
      BackColor       =   &H80000005&
      ForeColor       =   &H80000008&
      Height          =   4935
      Left            =   1320
      ScaleHeight     =   4905
      ScaleWidth      =   7425
      TabIndex        =   5
      Top             =   840
      Width           =   7455
   End
   Begin VB.TextBox ZipCode 
      Appearance      =   0  'Flat
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   420
      Left            =   6240
      TabIndex        =   4
      Top             =   240
      Width           =   975
   End
   Begin Threed.SSCommand Query 
      Height          =   855
      Left            =   0
      TabIndex        =   7
      Top             =   3360
      Width           =   1095
      _Version        =   65536
      _ExtentX        =   1931
      _ExtentY        =   1508
      _StockProps     =   78
      Caption         =   "Query"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      AutoSize        =   2
      Picture         =   "FINDZIP.frx":0000
   End
   Begin Threed.SSCommand InfoTool 
      Height          =   855
      Left            =   0
      TabIndex        =   6
      Top             =   2520
      Width           =   1095
      _Version        =   65536
      _ExtentX        =   1931
      _ExtentY        =   1508
      _StockProps     =   78
      Caption         =   "InfoTool"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      AutoSize        =   2
      Picture         =   "FINDZIP.frx":031A
   End
   Begin Threed.SSCommand ZoomOut 
      Height          =   855
      Left            =   0
      TabIndex        =   2
      Top             =   1680
      Width           =   1095
      _Version        =   65536
      _ExtentX        =   1931
      _ExtentY        =   1508
      _StockProps     =   78
      Caption         =   "ZoomOut"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      AutoSize        =   2
      Picture         =   "FINDZIP.frx":0634
   End
   Begin Threed.SSCommand ZoomIn 
      Height          =   855
      Left            =   0
      TabIndex        =   1
      Top             =   840
      Width           =   1095
      _Version        =   65536
      _ExtentX        =   1931
      _ExtentY        =   1508
      _StockProps     =   78
      Caption         =   "ZoomIn"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      AutoSize        =   2
      Picture         =   "FINDZIP.frx":094E
   End
   Begin Threed.SSCommand Grabber 
      Height          =   855
      Left            =   0
      TabIndex        =   0
      Top             =   0
      Width           =   1095
      _Version        =   65536
      _ExtentX        =   1931
      _ExtentY        =   1508
      _StockProps     =   78
      Caption         =   "Grabber"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      AutoSize        =   2
      Picture         =   "FINDZIP.frx":0C68
   End
   Begin VB.Label Label1 
      Appearance      =   0  'Flat
      BackColor       =   &H00C0C0C0&
      Caption         =   "Type 5-digit zip-code to center map on:"
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H80000008&
      Height          =   375
      Left            =   1320
      TabIndex        =   3
      Top             =   240
      Width           =   4815
   End
   Begin VB.Menu MenuBar_File 
      Caption         =   "&File"
      Begin VB.Menu Menu_PrintForm 
         Caption         =   "&Print Form"
      End
      Begin VB.Menu Menu_PrintMap 
         Caption         =   "Print &Map"
      End
      Begin VB.Menu Menu_Sep1 
         Caption         =   "-"
      End
      Begin VB.Menu Menu_Exit 
         Caption         =   "E&xit"
      End
   End
   Begin VB.Menu MenuBar_Map 
      Caption         =   "&Map"
      Begin VB.Menu Menu_LayerControl 
         Caption         =   "&Layer Control..."
      End
      Begin VB.Menu Menu_CreateThematic 
         Caption         =   "Create &Thematic Map..."
      End
      Begin VB.Menu Menu_ViewEntire 
         Caption         =   "View &Entire Layer..."
      End
   End
End
Attribute VB_Name = "FindZipForm"
Attribute VB_Creatable = False
Attribute VB_Exposed = False
Option Explicit

Dim mapinfo As Object
Dim mapid As Long
Dim legendid As Long

Private Sub DoLegendMaintence()
    'This routine is responsible for showing/hiding the legend
    'associated with the thematic map
    Dim bHasThematic As Integer
    Dim ndx, count As Integer

    bHasThematic = False
    count = Val(mapinfo.eval("MapperInfo(" & mapid & ",9)"))
    For ndx = 1 To count
        If (Val(mapinfo.eval("LayerInfo(" & mapid & "," & ndx & ",24)")) = 3) Then
            bHasThematic = True
            Exit For
        End If
    Next

    If (bHasThematic And legendid = 0) Then
        'create legend
        mapinfo.do "Set Next Document Parent WindowInfo(" & mapid & ",12) Style 1"
        mapinfo.do "Create Legend From Window " & mapid
        legendid = Val(mapinfo.eval("WindowID(0)"))
    ElseIf (Not bHasThematic And legendid <> 0) Then
        'destroy legend
        mapinfo.do "Close Window " & legendid
        legendid = 0
    End If
End Sub

Private Sub Form_LinkExecute(CmdStr As String, Cancel As Integer)
    ReDim args(8) As String
    Dim start, pos, ndx, length As Integer

    If (Left$(CmdStr, 3) <> "MI:") Then
        MsgBox "Unexpected LinkExecute: " & CmdStr
        Exit Sub
    End If

    args(8) = ""    'make sure we initialize this for later test
    ndx = 1
    start = 4
    length = Len(CmdStr)
    While (start < length)
        pos = InStr(start, CmdStr, ",")
        If (pos = 0) Then
            args(ndx) = Mid$(CmdStr, start, 32767)
            start = length
        Else
            args(ndx) = Mid$(CmdStr, start, pos - start)
            start = pos + 1
        End If
        ndx = ndx + 1
    Wend
    If (args(8) <> "") Then
        'CommandInfo(8) is the ID of the menu item we clicked
        'We use as the ID value the MapInfo menu command number
        'that we want to run when we get this event
        mapinfo.RunMenuCommand Val(args(8))
        Call DoLegendMaintence
    Else
        'Must have been tool callback
        MsgBox "You clicked at ( " & args(1) & " , " & args(2) & " )"
    End If
End Sub

Private Sub Form_Load()
Dim bUnableToCreateObj As Integer

    ' This code demonstrates how to structure an app that can be run
    ' with either MI Pro, or a MI Pro runtime as the OLE server.  Be sure
    ' to see the code below that creates a custom button using different
    ' approaches based on whether or not a runtime is in use.
    bUnableToCreateObj = False
    On Error GoTo cant_createApplicationObject
    Set mapinfo = CreateObject("MapInfo.Application")
    On Error GoTo 0

    If bUnableToCreateObj Then
        On Error GoTo cant_createRuntimeObject
        Set mapinfo = CreateObject("MapInfo.Runtime")
        On Error GoTo 0
    End If
    

    'indicate that we don't have a legend window
    legendid = 0

    'Initialize the application
    mapinfo.do "Set Application Window " & FindZipForm.hWnd
    mapinfo.do "Open Table ""STATES.TAB"" ReadOnly Interactive"
    mapinfo.do "Open Table ""US_ZIPS.TAB"" ReadOnly Interactive"

    'Disable the help subsystem - we don't support help in this application
    mapinfo.do "Set Window Help Off"

    'Disable the <Add...> control in the Layer Control dialog box
    mapinfo.do "Alter MapinfoDialog 1800 Control 12 Disable"

    'Make the Info tool parented to our form for when
    ' the user uses that tool
    mapinfo.do "Set Window Info Parent " & FindZipForm.hWnd
    mapinfo.do "Set Window Info ReadOnly"

    'Reprogram the map's shortcut menu (right-click on map)
    ' note well that we reprogram the Layer Control & Create Thematic
    ' to call us back via DDE so that we can do maintenence after these run
    mapinfo.do "Create Menu ""MapperShortcut"" ID 17 as ""&Layer Control..."" ID 801 calling DDE ""FindZip"",""MainForm"",""Create &Thematic Map..."" ID 307 calling DDE ""FindZip"",""MainForm"",""View &Entire Layer..."" calling 807"

    'Create our custom "Query" tool
    ' The positive case is true if the runtime is acting
    ' as the OLE server
    If mapinfo.eval("SystemInfo(4)") = "T" Then
        mapinfo.do "Create ButtonPad ID 3 As ToolButton Calling DDE ""FindZip"",""MainForm"" Cursor 128 DrawMode 34 ID 101"
    Else
        mapinfo.do "Alter ButtonPad ID 3 Add ToolButton Calling DDE ""FindZip"",""MainForm"" Cursor 128 DrawMode 34 ID 101"
    End If

    'Create the Map window
    mapinfo.do "Set Next Document Parent " & MapFrame.hWnd & " Style 1"
    mapinfo.do "Map From States"
    mapid = Val(mapinfo.eval("WindowID(0)"))
    mapinfo.do "Set Map Window " & mapid & " Center (-95.5,36.5) Zoom 3300"

    'Select the grabber tool as the active tool,
    mapinfo.RunMenuCommand 1702

    Exit Sub

cant_createApplicationObject:
    ' If we can't create the object using MapInfo Pro, we try to use the runtime
    bUnableToCreateObj = True
    Resume Next

cant_createRuntimeObject:
    ' If the attempt to create the runtime object also fails,
    ' we are done.
    MsgBox "Unable to CreateObject of MapInfo.Application"
    End
    

End Sub

Private Sub Grabber_Click()
    mapinfo.RunMenuCommand 1702
End Sub

Private Sub InfoTool_Click()
    mapinfo.RunMenuCommand 1707
End Sub

Private Sub Menu_CreateThematic_Click()
    mapinfo.RunMenuCommand 307
    Call DoLegendMaintence
End Sub

Private Sub Menu_Exit_Click()
    End 'Program
End Sub

Private Sub Menu_LayerControl_Click()
    mapinfo.RunMenuCommand 801
    Call DoLegendMaintence
End Sub

Private Sub Menu_PrintForm_Click()
    'Update picture on the form
    mapinfo.do "Save Window " & mapid & " As ""C:\MAP.WMF"" Type ""WMF"""
    MapFrame.Picture = LoadPicture("C:\MAP.WMF")
    'Now, print the form
    PrintForm
    Kill "C:\MAP.WMF"
End Sub

Private Sub Menu_PrintMap_Click()
    mapinfo.do "PrintWin"
End Sub

Private Sub Menu_ViewEntire_Click()
    mapinfo.RunMenuCommand 807
End Sub

Private Sub Query_Click()
    mapinfo.do "Run Menu Command ID 101"
End Sub

Private Sub ZipCode_Change()
    If (Len(ZipCode.Text) = 5) Then
        mapinfo.do "Find Using US_ZIPS(Zip_Code)"
        mapinfo.do "Find """ & ZipCode.Text & """"
        If (Val(mapinfo.eval("CommandInfo(3)")) >= 1) Then
            mapinfo.do "Set Map Window " & mapid & " Center(CommandInfo(1), CommandInfo(2)) Zoom 500"
        End If
    End If
End Sub

Private Sub ZoomIn_Click()
    mapinfo.RunMenuCommand 1705
End Sub

Private Sub ZoomOut_Click()
    mapinfo.RunMenuCommand 1706
End Sub

