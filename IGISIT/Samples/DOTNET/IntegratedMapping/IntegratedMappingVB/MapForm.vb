
Imports MapInfo
Imports System.IO
Imports System.Runtime.InteropServices


'
' A demonstration of how to do Integrated Mapping (the reparenting of a
' MapInfo Professional map window into other applications) using .Net 
'
Public Class MapForm
    Implements MapInfo.MiPro.Samples.IM.ICallbackNotify

    ' Strings displayed in a combobox, to let the user choose a map tool 
    Private _mapToolPan As String = "Pan"
    Private _mapToolSelect As String = "Select"
    Private _mapToolZoomIn As String = "Zoom In"
    Private _mapToolZoomOut As String = "Zoom Out"

    ' Id of the map window being reparented
    Private _mapWindowId As String = ""

    ' HWND of the window being reparented
    Private _hWnd As System.IntPtr

    ' Mapping of map tool names to tool command ids
    Private _toolIdMap As Dictionary(Of String, Integer)

    'ID of the custom OLE menu item on the map window's context menu
    Private Const _customItemId As UInteger = 10000

    ' Reference to the callbackobject 
    Private _callbackObject As MapInfo.MiPro.Samples.IM.MapInfoCallBack

    ' Store a reference to MapInfo Professional's COM interface
    Private _mapInfoApp As MapInfoApplication

    ' A File Open dialog that the user can use to open one or more .TAB files
    Private _openFileDlg As OpenFileDialog

    Private ReadOnly Property OpenDlg() As OpenFileDialog
        Get
            If _openFileDlg Is Nothing Then
                _openFileDlg = New OpenFileDialog()
                _openFileDlg.Filter = "MapInfo Tables (*.tab)|*.tab"
                _openFileDlg.Multiselect = True
                _openFileDlg.RestoreDirectory = False

                _openFileDlg.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)
            End If
            Return _openFileDlg
        End Get
    End Property

    Private ReadOnly Property MapInfoApp() As MapInfoApplication
        Get
            Return _mapInfoApp
        End Get
    End Property

    Public Sub New()
        InitializeComponent()

        InitializeMapToolCombobox()
    End Sub

    Private Sub MapForm_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load

        ' Create an instance of MapInfo Professional, silently/hidden 
        InitializeComObject()

        ' Add a custom item to the map window's context menu 
        AddMapperShortcutMenuitem()

    End Sub

    Private Sub MapForm_FormClosed(ByVal sender As System.Object, ByVal e As System.Windows.Forms.FormClosedEventArgs) Handles MyBase.FormClosed

        ' Unregister the callback object
        MapInfoApp.UnregisterCallback(_callbackObject)

    End Sub

    Private Sub MapForm_ResizeEnd(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.ResizeEnd

        ' The form has been resized. 
        If _mapWindowId <> "" Then
            ' Update the map to match the current size of the panel. 
            MoveWindow(_hWnd, 0, 0, Me.MapPanel.Width, Me.MapPanel.Height, False)
        End If

    End Sub

    ' Windows API function used for window resizing
    <DllImport("user32.dll")> _
Private Shared Function MoveWindow(ByVal hWnd As IntPtr, ByVal X As Integer, ByVal Y As Integer, ByVal nWidth As Integer, ByVal nHeight As Integer, ByVal bRepaint As Boolean) As Boolean
    End Function


    Private Sub ComboBoxMapTool_SelectionChangeCommitted(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles ComboBoxMapTool.SelectionChangeCommitted
        ' The user selected a different map tool from the combo box 

        ' Get the current combobox selection
        Dim selectedText As String = ComboBoxMapTool.SelectedItem.ToString()

        ' Get the command id
        Dim commandId As Integer = _toolIdMap(selectedText)

        ' Issue command to change the map tool
        Dim cmd As String = String.Format("Run Menu Command {0}", commandId)
        _mapInfoApp.Do(cmd)

    End Sub

    Private Sub OpenToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles OpenToolStripMenuItem.Click

        ' Prompt the user to open one or more TAB files
        If OpenDlg.ShowDialog(Me) = DialogResult.OK Then
            ' Close window and tables, if they exist
            If _mapWindowId <> "" Then
                CloseWindow(_mapWindowId)
                CloseAllTables()
                _mapWindowId = ""
            End If

            ' Create a new map
            NewMap(OpenDlg.FileNames)

            ' Enable the tool picker 
            ComboBoxMapTool.Enabled = True
        End If

    End Sub

    Private Sub AboutToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles AboutToolStripMenuItem.Click
        ' User chose Help > About 
        ShowMessage("Demonstration of integrated mapping, using Windows Forms.")
    End Sub

    Private Sub ExitToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles ExitToolStripMenuItem.Click
        ' User chose File > Exit 
        Me.Close()
    End Sub

    Private Sub ButtonZoomIn_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles ButtonZoomIn.Click
        ' The user clicked the Zoom In button 
        ZoomMap(0.5)

    End Sub

    Private Sub ButtonZoomOut_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles ButtonZoomOut.Click
        ' The user clicked the Zoom Out button 
        ZoomMap(2.0)

    End Sub

    Private Sub InitializeComObject()

        Dim cmd As String = String.Format("Set Application Window {0}", Me.Handle)

        ' Create the MapInfo Professional object
        _mapInfoApp = New MapInfoApplication()

        ' Set parent window for MapInfo Professional dialogs
        _mapInfoApp.Do(cmd)

        ' Create the callback object
        _callbackObject = New MapInfo.MiPro.Samples.IM.MapInfoCallBack(Me)

        ' Register the callback object with MapInfo Professional
        _mapInfoApp.RegisterCallback(_callbackObject)

    End Sub

    Private Sub InitializeMapToolCombobox()

        ' Set up the combo box that lets the user choose a map tool 
        ' Create the dictionary collection
        _toolIdMap = New Dictionary(Of String, Integer)()

        ' Add "Select" tool to combobox and dictionary
        Me.ComboBoxMapTool.Items.Add(_mapToolSelect)
        _toolIdMap.Add(_mapToolSelect, 1701)

        ' Add "Pan" tool to combobox and dictionary
        Me.ComboBoxMapTool.Items.Add(_mapToolPan)
        _toolIdMap.Add(_mapToolPan, 1702)

        ' Add "Zoom In" tool to combobox and dictionary
        Me.ComboBoxMapTool.Items.Add(_mapToolZoomIn)
        _toolIdMap.Add(_mapToolZoomIn, 1705)

        ' Add "Zoom Out" tool to combobox and dictionary
        Me.ComboBoxMapTool.Items.Add(_mapToolZoomOut)
        _toolIdMap.Add(_mapToolZoomOut, 1706)

        ' Set the combobox item to Select
        ComboBoxMapTool.SelectedIndex = 0
    End Sub

    Private Sub AddMapperShortcutMenuitem()
        ' Add a custom item to the Map window's context menu 
        ' Issue Alter Menu command, adding an OLE menuitem. 
        ' When the user chooses a custom OLE menuitem from the context menu,
        ' MapInfo Professional calls MapInfoCallback.MenuItemHandler,
        ' which in turn calls the OnMenuItemClick item below. 
        Dim cmd As String = String.Format("Alter Menu ""MapperShortcut"" Add ""Custom Item"" ID {0} calling OLE ""MenuItemHandler""", _customItemId)
        _mapInfoApp.Do(cmd)
    End Sub


    ' Given a list of .TAB filenames, open the tables and display them in a map
    Private Sub NewMap(ByVal tableList As String())
        Dim aliasList As String = ""
        Dim hWnd As Long

        ' Open each TAB file
        For Each tablepath As String In tableList
            ' Create alias string for the table
            Dim [alias] As String = Path.GetFileNameWithoutExtension(tablepath)
            [alias] = [alias].Replace(" ", "_")

            ' Open the table
            MapInfoApp.[Do]("Open table """ + tablepath + """ as " + [alias])

            ' Add new table's alias to the list
            If aliasList = "" Then
                aliasList += [alias]
            Else
                aliasList += ", " + [alias]
            End If
        Next

        ' Create map window, reparenting it to our map panel
        Dim cmd As String = String.Format("Set Next Document Parent {0} Style 1", Me.MapPanel.Handle)
        MapInfoApp.Do(cmd)
        MapInfoApp.Do("Map From " + aliasList)

        ' Save the ID of the newly created window
        _mapWindowId = MapInfoApp.Eval("WindowID(0)")

        ' Call WindowInfo with 12 (WIN_INFO_WND) to get the Windows HWND.
        ' If the user resizes the form, we need the HWND to update the map size.
        hWnd = Long.Parse(_mapInfoApp.Eval("WindowInfo(FrontWindow(),12)"))
        _hWnd = New System.IntPtr(hWnd)

        ' Now that there is a map, enable the Zoom In and Zoom Out buttons
        Me.ButtonZoomIn.Enabled = True
        Me.ButtonZoomOut.Enabled = True
    End Sub

    Private Sub CloseWindow(ByVal windowId As String)
        ' Close the window
        MapInfoApp.Do("Close window " + windowId)
    End Sub

    Private Sub CloseAllTables()
        MapInfoApp.Do("Close All")
    End Sub

    Public Sub ShowMessage(ByVal msg As String)
        MessageBox.Show(Me, msg)
    End Sub

    Private Sub ZoomMap(ByVal zoomFactor As Double)
        If _mapWindowId <> "" Then
            ' Call:  MapperInfo(id, MAPPER_INFO_DISTUNITS) 
            ' to get a units string such as "mi" or "km"
            Dim strUnit As String = MapInfoApp.Eval("MapperInfo( " + _mapWindowId + " , 12)")

            ' Call:  MapperInfo(id, MAPPER_INFO_ZOOM) 
            Dim dZoom As Double = [Double].Parse(MapInfoApp.Eval("MapperInfo( " + _mapWindowId + " , 1)"))

            dZoom *= zoomFactor
            dZoom = Math.Min(dZoom, 10000000)
            dZoom = Math.Max(dZoom, 0.0001)
            ' Apply the new zoom level with a statement of this form: 
            '     Set Map Window 123456 Zoom 123.456  Units "mi"  
            Dim cmd As String = String.Format("Set Map Window {0} Zoom {1} Units ""{2}""", _mapWindowId, dZoom, strUnit)
            MapInfoApp.Do(cmd)
        End If

    End Sub

#Region "ICallbackNotify Members"

    ' The method called when the user chooses the custom OLE menuitem.  
    Public Sub OnMenuItemClick(ByVal id As UInteger) Implements MapInfo.MiPro.Samples.IM.ICallbackNotify.OnMenuItemClick
        If id = _customItemId Then
            MessageBox.Show(Me, "Custom menu item was clicked.")
        End If
    End Sub


    ' The method called when the MapInfo Professional status bar text changes. 
    ' This can happen due to changes in the map view (zoom level) or selection, 
    ' or can happen because the user highlights an item on the map's context menu.
    Public Sub OnStatusBarTextChanged(ByVal text As String) Implements MapInfo.MiPro.Samples.IM.ICallbackNotify.OnStatusBarTextChanged

        Dim b As Boolean = StatusStrip1.InvokeRequired

        ' Replace any occurrences of "\t" (which can be included when the status bar
        ' is displaying map zoom etc.) with spaces.  
        ToolStripStatusLabel1.Text = text.Replace("" & Chr(9) & "", "        ")
    End Sub


    ' The method called when the map window changes, e.g. layers added.  
    Public Sub OnWindowContentsChanged(ByVal windowId As UInteger) Implements MapInfo.MiPro.Samples.IM.ICallbackNotify.OnWindowContentsChanged
        ' TODO:  If your application needs to respond to changes in the map 
        ' contents, add appropriate code here.   
    End Sub

#End Region


End Class


