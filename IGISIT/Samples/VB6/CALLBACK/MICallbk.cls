VERSION 1.0 CLASS
BEGIN
  MultiUse = 0   'False
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "MICallback"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = True
Option Explicit

Public Sub QueryTool(ByVal CmdStr As String)
    ReDim args(8) As String
    Dim start, pos, ndx, length As Integer
    Dim count As Integer
    Dim msg, Table, Row As String

    If (Left$(CmdStr, 3) <> "MI:") Then
        MsgBox "Unexpected callback: " & CmdStr
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
    
    'Args(1),Args(2) give the point where the user clicked
    count = Val(mapinfo.eval("SearchPoint(WindowID(1)," & args(1) & "," & args(2) & ")"))
    msg = ""
    For ndx = 1 To count
        Table = mapinfo.eval("SearchInfo(" & ndx & ",1)")
        Row = mapinfo.eval("SearchInfo(" & ndx & ",2)")
        mapinfo.do "Fetch Rec " & Row & " From " & Table
        msg = msg & mapinfo.eval(Table & ".col1") & " (" & Table & "@" & Row & ") "
    Next
    MsgBox msg
End Sub

Public Sub RunCommand(ByVal msg As String)
    Dim x As String

    x = InputBox$("Enter a command:", "Run Command", "note ""hello""")
    On Error GoTo handle_err
    mapinfo.do x
    On Error GoTo 0

    Exit Sub
handle_err:
'Debug.Print "      Err=" & Err.Number & " (" & Err.Description & ")"
'Debug.Print "    MIErr=" & mapinfo.LastErrorCode & " (" & mapinfo.LastErrorMessage & ")"
    MsgBox "Error " & mapinfo.LastErrorCode & " = " & mapinfo.LastErrorMessage
    Exit Sub
End Sub

Public Sub SelectQueryTool(ByVal msg As String)
    mapinfo.do "Run Menu Command ID 2001"
End Sub


