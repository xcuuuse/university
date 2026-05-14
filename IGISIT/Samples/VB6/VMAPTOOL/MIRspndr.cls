VERSION 1.0 CLASS
BEGIN
  MultiUse = 0   'False
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "MIResponder"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = True
'********************************************************************************
'   GetField
'
'       Purpose: returns the Nth field from a delimited string
'
'       Arguments:
'           theStr - the delimited string
'           delimiter - a string indicating the field delimiter character(s)
'           whichField - an integer indicating which field is desired.
'                        i.e. - 1 = the first field, etc.
'
'       Returns:
'           a string representing the field indicated by whichField, or a
'           zero-length string ( "" ) if the field was not found.
'
'********************************************************************************
Private Function GetField(ByVal theStr As String, _
                            ByVal delimiter As String, _
                            ByVal whichField As Integer) As String
    Dim i As Integer
    Dim startPos As Integer
    Dim argCount As Integer
    Dim tmpStr, result As String

'* if the input string was null, or they asked for a field # less than 1,
'* return an empty string as the result
    If Len(theStr) = 0 Or whichField < 1 Then
        GetField = ""
        Exit Function
    End If

'* loop through til we get the field we want. If the string contains fewer
'* fields than the field number requested, a zero-length string is returned.
    argCount = 0
    tmpStr = theStr
    While InStr(tmpStr, delimiter) > 0 And argCount < whichField
        argCount = argCount + 1
        result = Left$(tmpStr, InStr(tmpStr, delimiter) - 1)
        tmpStr = Mid$(tmpStr, InStr(tmpStr, delimiter) + 1)
    Wend

'* if we dropped out of the while loop because InStr() returned 0, and
'* we haven't gotten to the desired field yet, take one more step in case
'* we are actually looking for the last field in the string.
    If argCount < whichField Then
        argCount = argCount + 1
        result = tmpStr
    End If

'* if we found our field, argCount will equal whichField. return the
'* result string, otherwise, return a zero-length string
    If argCount = whichField Then
        GetField = result
    Else
        GetField = ""
    End If
End Function
'********************************************************************************
'
'   HandleMenuSelection
'
'       This method is called by the items on the custom MapperShortcut menu
'       created in MapInfo in the "InitializeMapInfoConnection" routine. This
'       routine determines which menu item was selected, then performs the
'       appropriate action.
'
'********************************************************************************
Public Sub HandleMenuSelection(ByVal CommandInfoStr As String)
    Dim whichItem As Integer

'* first, verify that the message did, in fact, come from MapInfo
'* ( the string will begin with "MI:" if it did ). If it did come
'* from MapInfo, strip off the "MI:" prefix:
    If Left$(CommandInfoStr, 3) = "MI:" Then
        CommandInfoStr = Mid$(CommandInfoStr, 4, 9999)  '* strip off the "MI:"
    Else
        Exit Sub   '* msg did not come from MapInfo. Ignore it.
    End If

'* determine which menu item was selected by parsing out the correct field
'* from the comma delimited "CommandInfoStr"
    whichItem = CInt(GetField(CommandInfoStr, ",", CMD_INFO_MENUITEM))

    Select Case whichItem
        Case 1001   '* Bring up MapInfo's layer control dialog
            If thereIsAMap Then
            '* disable the "Add" and "Remove" buttons in the layer control dlg first
                MapInfo.Do "Alter MapInfoDialog 1800 Control 12 Disable"
                MapInfo.Do "Alter MapInfoDialog 1800 Control 13 Disable"
                MapInfo.RunMenuCommand M_MAP_LAYER_CONTROL  '* display the MapInfo's layer control dlg
            End If
        Case 1002   '* Open another table into the map window
            OpenATable
        Case 1003   '* close the currently selected table
            CloseSelectedLayer
    '* "Title Bar Display" sub menu items:
        Case 1101   '* Display the current zoom in the title bar
            If thereIsAMap Then MapInfo.Do "Set Map Display Zoom"
            MapInfo.Do "Alter Menu Item ID 1101 Check"
            MapInfo.Do "Alter Menu Item ID 1102 UnCheck"
            MapInfo.Do "Alter Menu Item ID 1103 UnCheck"
        Case 1102   '* Display the current scale in the title bar
            If thereIsAMap Then MapInfo.Do "Set Map Display Scale"
            MapInfo.Do "Alter Menu Item ID 1101 UnCheck"
            MapInfo.Do "Alter Menu Item ID 1102 Check"
            MapInfo.Do "Alter Menu Item ID 1103 UnCheck"
        Case 1103   '* display the cursor location in the title bar
            If thereIsAMap Then MapInfo.Do "Set Map Display Position"
            MapInfo.Do "Alter Menu Item ID 1101 UnCheck"
            MapInfo.Do "Alter Menu Item ID 1102 UnCheck"
            MapInfo.Do "Alter Menu Item ID 1103 Check"
    End Select
End Sub
'********************************************************************************
'
'   HandleToolButton
'
'       This method is called when the custom tools defined in MapInfo
'       in the "InitializeMapInfoConnection" are used in the map window.
'       This method determines which tool was used ( a point select tool,
'       and a rectangle select tool ), and performs the appropriate action
'
'********************************************************************************
Public Sub HandleToolButton(ByVal CommandInfoStr As String)
    Dim whichButton As Integer
    Dim x As Double
    Dim y As Double
    Dim x2 As Double
    Dim y2 As Double
    Dim nHits As Long

'* first, verify that the message did, in fact, come from MapInfo
'* ( the string will begin with "MI:" if it did ). If it did come
'* from MapInfo, strip off the "MI:" prefix:
    If Left$(CommandInfoStr, 3) = "MI:" Then
        CommandInfoStr = Mid$(CommandInfoStr, 4, 9999)  '* strip off the "MI:"
    Else
        Exit Sub   '* msg did not come from MapInfo. Ignore it.
    End If

'* determine which tool was used
    whichButton = CInt(GetField(CommandInfoStr, ",", CMD_INFO_TOOLBTN))

    Select Case whichButton
        Case 2001   '* the point info tool
            x = CDbl(GetField(CommandInfoStr, ",", CMD_INFO_X))     '* get x and y
            y = CDbl(GetField(CommandInfoStr, ",", CMD_INFO_Y))     '* from CommandInfo
            UpdateInfoByPoint x, y                          '* Update contents of TreeView
        Case 2002   '* the marquee (rectangle) info tool
            x = CDbl(GetField(CommandInfoStr, ",", CMD_INFO_X))     '* get x, y and
            y = CDbl(GetField(CommandInfoStr, ",", CMD_INFO_Y))     '* x2, y2 from
            x2 = CDbl(GetField(CommandInfoStr, ",", CMD_INFO_X2))   '* CommandInfo
            y2 = CDbl(GetField(CommandInfoStr, ",", CMD_INFO_Y2))
            UpdateInfoByRect x, y, x2, y2                   '* Update contents of TreeView
    End Select
End Sub
'**********************************************************************
'
'   SetStatusText
'
'       This is a standard method that MapInfo looks for in its Callback
'       object. If MapInfo finds this method in the Callback object, it
'       will get called automatically every time the text in MapInfo's
'       status bar text changes. The string passed in is a tab-delimited
'       string containing each of the status bar "Fields", i.e. - the
'       first field is the zoom, scale, or cursor location, the second field
'       is the editable layer, etc.
'
'       In the case of our sample, we just append the first field (the zoom,
'       scale, or cursor position ) to the title of the form window
'
'**********************************************************************
Public Sub SetStatusText(ByVal statusText As String)
    Dim newText As String

    newText = GetField(statusText, vbTab, 1)        '* get first field in tab-delimited string

    If newText = "" Then
        frmMainWin.Caption = "Visual Map Tools Sample"
    Else
        frmMainWin.Caption = "Visual Map Tools Sample : " & newText '* append it to form title
    End If
End Sub
'************************************************************************************
'
'   WindowContentsChanged
'
'       This is a standard method that MapInfo will look for in its Callback
'       object. If this routine exists, it will get called whenever the contents
'       of a window changes, such as a layer being removed, etc.
'
'       In the case of this sample app, we simply make sure that our layer list
'       and Menu/Toolbar are up to date.
'
'************************************************************************************
Public Sub WindowContentsChanged(ByVal winID As Long)
'* if the window that changed is in fact our map window, we update the controls in
'* our VB application
    If winID = mapWinID Then
        UpdateLayerList     '* make sure the layer list is up to date
        UpdateMenuAndToolbar    '* make sure menu & toolbar are properly activated
    End If
End Sub


