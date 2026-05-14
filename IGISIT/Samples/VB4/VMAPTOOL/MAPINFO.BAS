Attribute VB_Name = "MIBas"
'*********************************************************************************
'* The MoveWindow Windows API call is used to force MapInfo to resize the reparented
'* window when the user resizes the form. Note that the ScaleMode property of the
'* object ( PictureBox, Form, etc. ) whose hWnd has been assigned as the parent of
'* the MapInfo window ( using "Set Next Document Parent" ) must be set to "Pixels".
'*
Declare Function MoveWindow Lib "user32" (ByVal hwnd As Long, _
                                        ByVal x As Long, ByVal y As Long, _
                                        ByVal nWidth As Long, ByVal nHeight As Long, _
                                        ByVal bRepaint As Long) As Long

'*********************************************************************************
Public Const kPaneMargin = 50       '* margins around panes in main window

'*********************************************************************************
'* This type is used by this app's custom info tools
Type InfoToolHit
    Table As String
    column1 As String
End Type

'*********************************************************************************
Public MapInfo As Object            '* the object which will refer to MapInfo
Public theResponder As Object       '* the local object that MapInfo will send information back to

Public thereIsAMap As Boolean       '* keeps track of whether there is a map open
Public mapWinID As Long             '* the MapInfo Window ID of our map window
'*********************************************************************************
'
'   CloseSelectedLayer
'
'       This routine verifies that a valid, closeable table is selected
'       in the "Layers" listbox, and if so closes the table associated with
'       that layer.
'
'
'
'
'*********************************************************************************
Public Sub CloseSelectedLayer()
    Dim tabName As String
    Dim nLayers As Integer      '* number of layers in our map

    tabName = ""
'* check to see if a closeable layer is selected. Layer 0 = Cosmetic layer, which
'* is not closeable. -1 = nothing selected in the "Layers" listbox.
    With frmMainWin.lstLayers
        If .ListIndex > 0 Then
            tabName = .List(.ListIndex)     '* the listbox item  text is the table name
        End If
    End With

'* if a valid selection existed, close the table, and if it is the last layer in
'* our map, make sure the system is aware that the map no longer exists
    If tabName <> "" Then
        If thereIsAMap Then
        '* find out how many layers are in the map window
        '* mapbasic: nLayers = MapperInfo( mapWinID, MAPPER_INFO_LAYERS )
            nLayers = _
                CInt(MapInfo.Eval("MapperInfo(" & mapWinID & "," & MAPPER_INFO_LAYERS & ")"))

            MapInfo.Do "Close Table " & tabName     '* close the table

        '* if there was only one layer before we closed the table,
        '* then the map just went away. Reset the appropriate globals
        '* and update the layer list and toolbar.
       
            If nLayers = 1 Then
                thereIsAMap = False
                mapWinID = 0
                UpdateLayerList         '* update the "Layers" listbox
                UpdateMenuAndToolbar    '* Enable/Disable menus/toolbuttons
            End If

            '* clear the info tool.  MIResponder will clean up the Menu and Toolbar and the LayerList
            UpdateInfoClear
        End If
    End If
End Sub

'*********************************************************************************
'
'   OpenATable
'
'       This routine displays a common file open dialog, allowing the user to
'       select a file with the .TAB extension. It then opens this file in MapInfo,
'       verifies that it is mappable ( our app only handles mappable tables ), then
'       adds it to our map window. If the table is not mappable, the user is presented
'       with a message, and the table is closed.
'
'*********************************************************************************
Public Sub OpenATable()
    Dim theFile As String   '* the full path to the file
    Dim tabName As String   '* the MapInfo table alias for the file

'* First, display a common file dialog to open a table
    On Error GoTo userCancelled     '* hitting cancel in the dlg is handled as an error

    frmMainWin.dlgOpenTable.Filter = "MapInfo Tables (*.tab)|*.tab"
    frmMainWin.dlgOpenTable.FilterIndex = 1

    frmMainWin.dlgOpenTable.ShowOpen    '* display the dialog

    theFile = frmMainWin.dlgOpenTable.filename  '* get the file selected by the user
    tabName = MapInfo.Eval("PathToTableName$( """ & theFile & """ )")       '* get table alias
    MapInfo.Do "Open Table """ & theFile & """ as " & tabName       '* open the table
    MapInfo.Do "Set Table " & tabName & " ReadOnly"                 '* make it ReadOnly

'* now, make sure the table is mappable, otherwise, display a msg and close the table
    If MapInfo.Eval("TableInfo(" & tabName & "," & TAB_INFO_MAPPABLE & ")") = "F" Then
        MsgBox "This table is not mappable. I can only open mappable tables."
        MapInfo.Do "Close Table " & tabName
        Exit Sub
    End If

'* if the table is mappable, add it to the current map OR create a new map
    If thereIsAMap Then
    '* there's already a map. Add this new layer to the existing map
        MapInfo.Do "Add Map Layer " & tabName
    Else
    '* no map yet. Create a new one, reparented into our picture box
        MapInfo.Do "Set Next Document Parent " & frmMainWin.picMapFrame.hwnd & " Style 1"
        MapInfo.Do "Map From " & tabName
        mapWinID = CLng(MapInfo.Eval("FrontWindow()"))
        thereIsAMap = True
    End If

'* we don't need to include UpdateLayerList or UpdateMenuAndToolbar here because they will
'* get called by the WindowContentsChanged() method in the MIResponder object which was set
'* with MapInfo's "SetCallback" method in the "InitializeMapInfoConnection" subroutine.
    UpdateInfoClear

    Exit Sub

'* handle the user cancelling the dialog as an error condition ( the "CancelError" property
'* of the common dialog control must be set to True! )
userCancelled:
    Exit Sub
End Sub
'*********************************************************************************
'
'   ShutdownMapInfoConnection
'
'       This routine makes sure we exit cleanly. It is called by the QueryUnload
'       handler of our main form. Basically, since we have given MapInfo a
'       reference to an OLE object in our app ( of class MIResponder ), this has
'       incremented the reference count on our object to 1. This VB app cannot
'       exit cleanly until this reference count is decremented back to 0. We do
'       this by setting MapInfo's callback to the VB keyword "Nothing", which
'       represents a NULL object variable.
'
'*********************************************************************************
Public Sub ShutdownMapInfoConnection()

'* first, if the MapInfo object exists, we must reset its callback object
'* to a null object ( the VB keyword "Nothing" ), otherwise the VB app will
'* not exit because the reference count on this object will still be greater
'* than 0.
    If Not (MapInfo Is Nothing) Then
        MapInfo.SetCallback Nothing
    End If

'* Now, just for completeness, remove our reference to MapInfo and
'* to the responder
    Set MapInfo = Nothing
    Set theResponder = Nothing
End Sub
'*********************************************************************************
'
'   UpdateInfoByPoint
'
'       This routine accepts x & y coordinates from the map, and performs a
'       point hit test ( using the mapbasic routines "SearchPoint" and "SearchInfo" ),
'       then fills in the Info Tool TreeView control with a list of all the records
'       in all selectable layers of the map that were detected as "Hits"
'
'*********************************************************************************
Public Sub UpdateInfoByPoint(ByVal x As Double, ByVal y As Double)
    Dim nHits As Long
    Dim myHits() As InfoToolHit
    Dim recNum As Long
    Dim i As Long

    If thereIsAMap Then
    '* first, get the number of "Hits" using the MB function "SearchPoint"
    '* mapbasic: nHits = SearchPoint( mapWinID, x, y )
        nHits = CLng(MapInfo.Eval("SearchPoint(" & mapWinID & "," & x & "," & y & ")"))

        With frmMainWin.tvwInfo
        '* clear out any previous info tool hits
            .Nodes.Clear
            If nHits = 0 Then
            '* there were no hits: disable the TreeView control
                .Nodes.Add , , "noinfo", "< No Records >"
                .Enabled = False
            Else
            '* there were hits: scan through them using "SearchInfo", then add them to
            '* the TreeView control, and make sure the TreeView is enabled
                ReDim myHits(nHits)
                For i = 1 To nHits
                    myHits(i).Table = MapInfo.Eval("SearchInfo(" & i & "," & SEARCH_INFO_TABLE & ")")
                    recNum = CLng(MapInfo.Eval("SearchInfo(" & i & "," & SEARCH_INFO_ROW & ")"))
                    MapInfo.Do "Fetch Rec " & recNum & " from " & myHits(i).Table
                    myHits(i).column1 = MapInfo.Eval(myHits(i).Table & ".col1")

                '* attempt to create the parent node containing the table name.
                '* If it already exists, an error will occur and we do nothing
                '* in the error handler
                    On Error GoTo errPointParentExists
                    .Nodes.Add , , myHits(i).Table, myHits(i).Table
                    .Nodes(myHits(i).Table).Expanded = True
                    On Error GoTo 0
                '* now, create the child, containing the first field of each "Hit" record
                    .Nodes.Add myHits(i).Table, tvwChild, "child" & i, myHits(i).column1
                Next
            '* make sure the TreeView control is enabled.
                .Enabled = True
            End If
        End With
    Else
    '* if there was no map, disable the control. This should never happen, since this
    '* routine can only get called when a map is open, but we put it here for completeness.
        frmMainWin.tvwInfo.Nodes.Clear
        frmMainWin.tvwInfo.Nodes.Add , , "notab", "< No Map >"
        frmMainWin.tvwInfo.Enabled = False
    End If

    Exit Sub

errPointParentExists:
    '* if node exists, do nothing
    Resume Next
End Sub
'*********************************************************************************
'
'   UpdateInfoByRect
'
'       This routine accepts x,y,x2,y2 coordinates from the map, and performs a
'       rectangle hit test ( using the mapbasic routines "SearchRect" and "SearchInfo" ),
'       then fills in the Info Tool TreeView control with a list of all the records
'       in all selectable layers of the map that were detected as "Hits"
'
'*********************************************************************************
Public Sub UpdateInfoByRect(ByVal x As Double, ByVal y As Double, _
                            ByVal x2 As Double, ByVal y2 As Double)
    Dim nHits As Long
    Dim myHits() As InfoToolHit
    Dim recNum As Long
    Dim i As Long

    If thereIsAMap Then
    '* first, determine the number of "Hits" within the specified rectangle
    '* mapbasic: nHits = SearchRect( mapWinID, x, y, x2, y2 )
        nHits = _
            CLng(MapInfo.Eval("SearchRect(" & mapWinID & "," & x & "," & y & _
                                "," & x2 & "," & y2 & ")"))

        With frmMainWin.tvwInfo
        '* clear the TreeView control
            .Nodes.Clear
            If nHits = 0 Then
            '* there were no hits. disable the TreeView
                .Nodes.Add , , "noinfo", "< No Records >"
                .Enabled = False
            Else
            '* there were hits: scan through them using "SearchInfo", then add them to
            '* the TreeView control, and make sure the TreeView is enabled
                ReDim myHits(nHits)
                For i = 1 To nHits
                    myHits(i).Table = MapInfo.Eval("SearchInfo(" & i & "," & SEARCH_INFO_TABLE & ")")
                    recNum = CLng(MapInfo.Eval("SearchInfo(" & i & "," & SEARCH_INFO_ROW & ")"))
                    MapInfo.Do "Fetch Rec " & recNum & " from " & myHits(i).Table
                    myHits(i).column1 = MapInfo.Eval(myHits(i).Table & ".col1")

                '* attempt to create the parent node containing the table name.
                '* If it already exists, an error will occur and we do nothing
                '* in the error handler
                    On Error GoTo errRectParentExists
                    .Nodes.Add , , myHits(i).Table, myHits(i).Table
                    .Nodes(myHits(i).Table).Expanded = True
                    On Error GoTo 0
                '* now, create the child, containing the first field of each "Hit" record
                    .Nodes.Add myHits(i).Table, tvwChild, "child" & i, myHits(i).column1
                Next
            '* make sure the TreeView control is enabled
                .Enabled = True
            End If
        End With
    Else
    '* if there was no map, disable the control. This should never happen, since this
    '* routine can only get called when a map is open, but we put it here for completeness.
        frmMainWin.tvwInfo.Nodes.Clear
        frmMainWin.tvwInfo.Nodes.Add , , "notab", "< No Map >"
        frmMainWin.tvwInfo.Enabled = False
    End If

    Exit Sub

errRectParentExists:
    '* if node exists, do nothing
    Resume Next
End Sub

'*********************************************************************************
'   UpdateInfoClear
'       This routine simply clears the Info Tool TreeView of any previous
'       results.
'*********************************************************************************
Public Sub UpdateInfoClear()
    frmMainWin.tvwInfo.Nodes.Clear
End Sub

'*********************************************************************************
'
'   UpdateLayerList
'
'       This routine gets a list of the layers in the current map ( if one
'       exists ), and displays the list in the "Layers" listbox.
'
'*********************************************************************************
Public Sub UpdateLayerList()
    Dim winType As Integer      '* type of frontmost window in MapInfo
    Dim nLayers As Integer      '* number of layers in map window
    Dim layerName As String     '* the name of each layer
    Dim i As Integer

    frmMainWin.lstLayers.Clear  '* blank out the list

    If Not thereIsAMap Then                               '* is a map window open?
    '* no map is open, disable the layer list control.
        frmMainWin.lstLayers.AddItem "< No Map >"
        frmMainWin.lstLayers.Enabled = False
    Else
    '* a map was open. Get a list of its layers & fill the listbox control
    '*
    '* check to make sure the ID actually represents a map. It should not be possible for
    '* it to be anything other than a map, but we place this here for robustness.
    '* mapbasic: winType = WindowInfo( mapWinID, WIN_INFO_TYPE )
        winType = CInt(MapInfo.Eval("WindowInfo(" & mapWinID & "," & WIN_INFO_TYPE & ")"))

        If winType <> WIN_MAPPER Then               '* is the current window a map?
            frmMainWin.lstLayers.AddItem "< No Map >"
            frmMainWin.lstLayers.Enabled = False
        Else
        '* get the number of layers in the map window
        '* mapbasic: nLayers = MapperInfo( mapWinID, MAPPER_INFO_LAYERS )
            nLayers = _
                CInt(MapInfo.Eval("MapperInfo(" & mapWinID & "," & MAPPER_INFO_LAYERS & ")"))

            For i = 0 To nLayers
            '* get the name of each layer, and insert them into the layer list box
            '* mapbasic: layerName = LayerInfo( mapWinID, i, LAYER_INFO_NAME )
                layerName = _
                    MapInfo.Eval("LayerInfo(" & mapWinID & "," & i & "," & LAYER_INFO_NAME & ")")
                frmMainWin.lstLayers.AddItem layerName
            Next
            frmMainWin.lstLayers.Enabled = True
        End If
    End If
End Sub

'*********************************************************************************
'
'   InitializeMapInfoConnection
'
'       This routine establishes an instance of MapInfo in the background
'       for us to communicate with. It also establishes a local instance of
'       an object of the class "MIResponder" ( defined in this project ), which
'       will be used for MapInfo to communicate back to our application.
'
'       Also here, we create the shortcut menu and the "invisible" toolbuttons
'       within MapInfo which will be used by our custom application.
'
'*********************************************************************************
Public Sub InitializeMapInfoConnection()

'* First, establish an instance of MapInfo to communicate with
    Set MapInfo = CreateObject("MapInfo.Application")

'* Now, make sure all MI's dialogs will appear as children of our main window
    MapInfo.Do "Set Application Window " & frmMainWin.hwnd

'* Now, create an instance of "MIResponder" class defined by this VB app
'* to allow MapInfo to communicate information back to the VB app.
    Set theResponder = New MIResponder
    MapInfo.SetCallback theResponder

'* Now, set the mapper shortcut to do some stuff...
    MapInfo.Do "Create Menu ""TitleBarMenu"" As " & _
                """!+Current Zoom"" ID 1101 Calling OLE ""HandleMenuSelection"", " & _
                """!Current Scale"" ID 1102 Calling OLE ""HandleMenuSelection"", " & _
                """!Cursor Location"" ID 1103 Calling OLE ""HandleMenuSelection"""
    MapInfo.Do "Create Menu ""MapperShortcut"" ID 17 As " & _
                """Layer Control..."" ID 1001 Calling OLE ""HandleMenuSelection"", " & _
                """Title Bar Display"" As ""TitleBarMenu"", " & _
                """(-"", " & _
                """Open Table..."" ID 1002 Calling OLE ""HandleMenuSelection"", " & _
                """Close Selected Layer"" ID 1003 Calling OLE ""HandleMenuSelection"""

'* Now, create our custom tools. This is done by creating a MapInfo ButtonPad with
'* custom ToolButtons. These toolbuttons will never be directly visible to the
'* user, but can be made the active tool in response to some action in the VB app's
'* UI, for example clicking a button on a ToolBar implemented in VB, as we will do
'* here.
'*  note: DrawMode 34 = single point drawmode, DrawMode 32 = marquee (rectangle) drawmmode
    MapInfo.Do "Create ButtonPad ""Custom Tools"" As " & _
                "ToolButton ID 2001 DrawMode 34 Calling OLE ""HandleToolButton"" " & _
                "ToolButton ID 2002 DrawMode 32 Calling OLE ""HandleToolButton"""

'* initialize some other useful stuff
    thereIsAMap = False                     '* initially, there is no map window
    mapWinID = 0                            '* a window ID of 0 means no window
    MapInfo.RunMenuCommand M_TOOLS_SELECTOR '* make MapInfo's select tool active
    UpdateLayerList
    UpdateInfoClear
    UpdateMenuAndToolbar
End Sub
'************************************************************************
'
'   UpdateMenuAndToolbar
'
'       This routine appropriately enables and disables all menu items
'       and Toolbar buttons based on the current state of the system
'************************************************************************
Public Sub UpdateMenuAndToolbar()
    With frmMainWin
        
        If thereIsAMap Then
        '* a map is open. Enable "Close Layer" only if a selection exists in the layer list box
            If .lstLayers.ListIndex < 1 Then
                .mnuFileClose.Enabled = False   '* map is open, but no tables selected
                MapInfo.Do "Alter Menu Item ID 1003 Disable"    '* disable item in shortcut menu
            Else
                .mnuFileClose.Enabled = True    '* map is open, table is selected
                MapInfo.Do "Alter Menu Item ID 1003 Enable"     '* enable item in shortcut menu
            End If

        '* a map is open. Enable all of the buttons in the Toolbar
            If Not .tbarMain.Buttons("select").Enabled Then
            '* if the "select" button is becoming enabled ( ie - a new map just opened ),
            '* make sure the select tool is the active tool
                .tbarMain.Buttons("select").Enabled = True
                .tbarMain.Buttons("select").Value = tbrPressed
            End If
            .tbarMain.Buttons("select").Enabled = True
            .tbarMain.Buttons("grabber").Enabled = True
            .tbarMain.Buttons("zoomin").Enabled = True
            .tbarMain.Buttons("zoomout").Enabled = True
            .tbarMain.Buttons("info_pt").Enabled = True
            .tbarMain.Buttons("info_rt").Enabled = True
        Else
        '* no map is open. Disable the "Close Layer" menu item
            .mnuFileClose.Enabled = False

        '* no map is open. Make sure select tool is active, disable all Toolbar buttons
            MapInfo.RunMenuCommand M_TOOLS_SELECTOR
            .tbarMain.Buttons("select").Enabled = False
            .tbarMain.Buttons("grabber").Enabled = False
            .tbarMain.Buttons("zoomin").Enabled = False
            .tbarMain.Buttons("zoomout").Enabled = False
            .tbarMain.Buttons("info_pt").Enabled = False
            .tbarMain.Buttons("info_rt").Enabled = False
        End If
    
    End With
End Sub


