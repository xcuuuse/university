VERSION 5.00
Begin VB.Form MainForm 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "OLE Callback Demonstration"
   ClientHeight    =   4470
   ClientLeft      =   1095
   ClientTop       =   1515
   ClientWidth     =   6855
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   4470
   ScaleWidth      =   6855
   ShowInTaskbar   =   0   'False
End
Attribute VB_Name = "MainForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub Form_Load()
    'Instantiate MapInfo
    Dim strfile As String
    Set mapinfo = CreateObject("MapInfo.Application")
    mapinfo.do "Set Application WIndow " & MainForm.hWnd
    'Instantiate OLE Automation callback object
    Set myCallback = New MICallback
    mapinfo.SetCallback myCallback
    'Initialize MapInfo the way we need
    mapinfo.do "Create Buttonpad ""Callback"" As Toolbutton ID 2001 DrawMode 34 Cursor 138 Calling OLE ""QueryTool"""
    mapinfo.do "Create Menu ""MapperShortcut"" ID 17 As " & _
                """Query Tool"" Calling OLE ""SelectQueryTool"", " & _
                """(-"", " & _
                """Grabber"" Calling 1702, " & _
                """Zoom-in"" Calling 1705, " & _
                """Zoom-out"" Calling 1706, " & _
                """(-"", " & _
                """MapBasic Statement..."" Calling OLE ""RunCommand"" "
    'Create a Map & select the query tool
    strfile = mapinfo.Eval("programdirectory$()")

   mapinfo.do "open table " & """" + strfile + "DATA\Tut_Data\Tut_Usa\USA\STATES.TAB" + """" + " Readonly Interactive"
   mapinfo.do "open table " & """" + strfile + "DATA\Tut_Data\Tut_Usa\USA\City_125.TAB" + """" + " Readonly Interactive "
   mapinfo.do "open table " & """" + strfile + "DATA\Tut_Data\Tut_Usa\USA\STATEcap.TAB" + """" + " Readonly Interactive "
    'mapinfo.do "Open Table ""States"" Interactive Open Table ""City_125"" Interactive Open Table ""StateCap"" Interactive"
    mapinfo.do "Set Next Document Parent " & MainForm.hWnd & " Style 1"
    mapinfo.do "Map from StateCap,City_125,States"
    mapinfo.do "Run Menu Command ID 2001"
End Sub

Private Sub Form_Unload(Cancel As Integer)
    mapinfo.SetCallback Nothing
    Set myCallback = Nothing
    Set mapinfo = Nothing
End Sub

