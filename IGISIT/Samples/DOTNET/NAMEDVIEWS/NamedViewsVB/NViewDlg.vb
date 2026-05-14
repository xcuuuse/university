Imports System
Imports System.Windows.Forms
Imports System.Threading
Imports System.Xml
Imports System.Drawing
Imports System.IO
Imports System.Runtime.InteropServices 

Namespace MISamples
    Public Partial Class NViewDlg 
        Inherits UserControl
        ' some string in xml file 
        Private Const STR_NAME As String = "Name"
        Private Const STR_ROOT As String = "root"
        Private Const STR_DIALOG As String = "Dialog"
        Private Const STR_NAMEDVIEWS As String = "NamedViews"
        Private Const STR_VIEWS As String = "Views"
        Private Const STR_PATH_DIALOG As String = "/NamedViews/Dialog"
        Private Const STR_PATH_ROOT_FOLDER As String = "/NamedViews/Views"
        Private Const STR_LEFT As String = "Left"
        Private Const STR_TOP As String = "Top"
        Private Const STR_WIDTH As String = "Width"
        Private Const STR_HEIGHT As String = "Height"



        ' The controller class which uses this dialog class ensures 
        ' * a single instance of this dialog class. However different 
        ' * running instance of MapInfo Professional will have their 
        ' * own copy of dll. To make sure that read/write from/to xml 
        ' * file which is going to be a single file on the disk, is 
        ' * smooth and we have the synchronized access to the xml file, 
        ' * the Mutexes will be used. 
        ' 

        Private mut As Mutex = Nothing
        Private Const mutexName As String = "MISamples.NamedView"
        ' Name of the mutex 
        Private sXMLFile As String = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData) + "\MapInfo\MapInfo\nviews.xml"
        Private bTreeChanged As Boolean = False
        ' a flag indicating that tree contents have been changed 
        ' since last write to xml file 
        Private dragPrevNode As TreeNode = Nothing
        ' previous drag over node 
        'private TreeNode dragSelNode = null; // current drag over node 
        Private dialogLeft As Integer, dialogTop As Integer, dialogWidth As Integer, dialogHeight As Integer
        ' flag indicating whether it is the first time the form is being loaded
        Dim firstLoad As Boolean = True
        Private _controller As Controller  ' represents the window that owns this dialog (main MI Pro window)


        ''' <summary> 
        ''' Construction 
        ''' </summary> 
        Public Sub New()
            InitializeComponent()
            mut = New Mutex(False, mutexName)
        End Sub

        ''' <summary>
        ''' Parameterised Construction
        ''' <param name="controller"></param>
        ''' </summary>
        Public Sub New(ByVal controller As Controller)
            Me.New()
            _controller = controller
        End Sub




#Region "[DIALOG EVENT HANDLERS]"
        ''' <summary> 
        ''' Named View dialog Load event handler 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub NViewDlg_Load(ByVal sender As Object, ByVal e As EventArgs) Handles MyBase.Load

            If firstLoad = True Then
                firstLoad = False

                LoadTreeFromFile(sXMLFile)
                UpdateButtons()

                If dialogWidth >= Me.MinimumSize.Width AndAlso dialogWidth <= Screen.PrimaryScreen.WorkingArea.Width Then
                    Me.Width = dialogWidth
                End If
                If dialogHeight >= Me.MinimumSize.Height AndAlso dialogHeight <= Screen.PrimaryScreen.WorkingArea.Height Then
                    Me.Height = dialogHeight
                End If
                If dialogLeft > -Me.Width AndAlso dialogLeft < Screen.PrimaryScreen.WorkingArea.Width Then
                    Me.Left = dialogLeft
                End If
                If dialogTop > -Me.Top AndAlso dialogTop < Screen.PrimaryScreen.WorkingArea.Height Then
                    Me.Top = dialogTop
                End If
            End If
        End Sub
        ' This call to the WIN32 API function SetFocus is used in NViewDlg_FormClosing below
        <DllImport("User32.dll")> _
        Private Shared Function SetFocus(ByVal hWnd As IntPtr)
        End Function




#End Region


#Region "[TREEVIEW EVENT HANDLERS]"

        ''' <summary> 
        ''' Begins drag operation 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_ItemDrag(ByVal sender As Object, ByVal e As ItemDragEventArgs) Handles tvwNamedViews.ItemDrag
            tvwNamedViews.SelectedNode = DirectCast(e.Item, TreeNode)
            DoDragDrop(e.Item, DragDropEffects.Move)
        End Sub

        ''' <summary> 
        ''' Displays the drop target during a drag operation 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_DragOver(ByVal sender As Object, ByVal e As DragEventArgs) Handles tvwNamedViews.DragOver
            ' Change any previous node back 
            If dragPrevNode IsNot Nothing Then
                dragPrevNode.BackColor = Color.Empty
                dragPrevNode.ForeColor = Color.Empty
            End If

            ' Get the node from the mouse position, colour it 
            Dim pt As Point = DirectCast(sender, TreeView).PointToClient(New Point(e.X, e.Y))
            Dim tNode As TreeNode = DirectCast(sender, TreeView).GetNodeAt(pt)
            tNode.BackColor = SystemColors.Highlight
            tNode.ForeColor = SystemColors.HighlightText

            dragPrevNode = tNode

        End Sub

        Private Sub tvwNamedViews_DragLeave(ByVal sender As Object, ByVal e As EventArgs) Handles tvwNamedViews.DragLeave
            ' Change any previous node back 
            If dragPrevNode IsNot Nothing Then
                dragPrevNode.BackColor = SystemColors.Highlight
                dragPrevNode.ForeColor = SystemColors.HighlightText
            End If

        End Sub

        ''' <summary> 
        ''' Continues the drag operation 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_DragEnter(ByVal sender As Object, ByVal e As DragEventArgs) Handles tvwNamedViews.DragEnter
            e.Effect = DragDropEffects.Move

            dragPrevNode = Nothing
            'dragSelNode = null; 
        End Sub

        ''' <summary>
        ''' This event is generated when user drops a node
        ''' on another node. This handler completes the drag/drop operation.
        ''' </summary>
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_DragDrop(ByVal sender As Object, ByVal e As DragEventArgs) Handles tvwNamedViews.DragDrop
            ' Change any previous node back 
            If dragPrevNode IsNot Nothing Then
                dragPrevNode.BackColor = Color.Empty
                dragPrevNode.ForeColor = Color.Empty
                dragPrevNode = Nothing
            End If

            Dim dragNode As TreeNode

            If e.Data.GetDataPresent("System.Windows.Forms.TreeNode", False) Then

                Dim dropIndex As Integer = -1
                Dim newNode As TreeNode

                ' Get the node where the item has been dropped 
                Dim pt As Point = DirectCast(sender, TreeView).PointToClient(New Point(e.X, e.Y))
                Dim dropNode As TreeNode = DirectCast(sender, TreeView).GetNodeAt(pt)

                ' Get the node that is being dragged 
                dragNode = DirectCast(e.Data.GetData("System.Windows.Forms.TreeNode"), TreeNode)
                If Not TreeNodeUtil.IsViewNode(dragNode) Then
                    dragNode.Collapse()
                    dragNode.ImageIndex = 1
                End If

                If dropNode IsNot Nothing Then
                    ' If a node has been dropped on a view node use its parent as drop target 
                    If TreeNodeUtil.IsViewNode(dropNode) Then
                        ' Dropped a node onto a View node.  Move the node-being-dropped 
                        ' into the spot occupied by the drop target node. 
                        If (dropNode.Parent IsNot Nothing) Then
                            ' User dropped onto a node that is inside a folder. 
                            ' Get the index number of the target node, 
                            ' indicating the position within the folder. 
                            dropIndex = dropNode.Parent.Nodes.IndexOf(dropNode)
                        Else
                            ' The view node that we are dropping onto does not have a 
                            ' parent node, so it must be at the root level of the tree.
                            dropIndex = tvwNamedViews.Nodes.IndexOf(dropNode)
                        End If

                        dropNode = dropNode.Parent
                    Else
                        ' Dropped a node onto a Folder node.  Move the node-being-dropped 
                        ' into the top of the folder.  
                        dropIndex = 0
                    End If
                End If

                ' If the drop node is null add dragged node as the top level node 
                If dropNode Is Nothing Then
                    newNode = DirectCast(dragNode.Clone(), TreeNode)
                    If dropIndex >= 0 Then
                        tvwNamedViews.Nodes.Insert(dropIndex, newNode)
                    Else
                        tvwNamedViews.Nodes.Add(newNode)
                    End If
                    bTreeChanged = True
                ElseIf Not dropNode.Equals(dragNode) Then

                    ' else check if drag and drop nodes are different 
                    ' Do not allow a node to be dropped on a child/grand child 
                    If TreeNodeUtil.ContainsNode(dragNode, dropNode) Then
                        MessageBox.Show(My.Resources.ERR_INVALID_DROP, My.Resources.ERR_INVALID_DROP_MSG_TITLE, MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
                        Return
                    End If

                    newNode = DirectCast(dragNode.Clone(), TreeNode)
                    If dropIndex >= 0 Then
                        dropNode.Nodes.Insert(dropIndex, newNode)
                    Else
                        dropNode.Nodes.Add(newNode)
                    End If

                    dropNode.Expand()
                    dropNode.ImageIndex = 0
                    dropNode.SelectedImageIndex = 0
                    bTreeChanged = True
                Else
                    Return
                End If

                'Remove the dragged node 
                Dim dragNodeParent As TreeNode = dragNode.Parent
                dragNode.Remove()
                If dragNodeParent IsNot Nothing Then
                    If dragNodeParent.Nodes.Count = 0 Then
                        dragNodeParent.Collapse()
                        dragNodeParent.ImageIndex = 1
                        dragNodeParent.SelectedImageIndex = 1

                    End If
                End If

                ' Make sure the node that the user dragged is selected 
                tvwNamedViews.SelectedNode = newNode

            End If
        End Sub

        ''' <summary> 
        ''' Handles renaming of a tree node 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_AfterLabelEdit(ByVal sender As Object, ByVal e As NodeLabelEditEventArgs) Handles tvwNamedViews.AfterLabelEdit
            If e.Label Is Nothing AndAlso e.Node.Text.Length = 0 Then
                e.Node.Remove()
                Return
            End If

            If e.Label IsNot Nothing Then
                If e.Label.Length > 0 Then
                    If e.Label.IndexOfAny(New Char() {"@"c, "."c, ","c, "!"c}) = -1 Then
                        ' Stop editing without canceling the label change. 
                        e.Node.Text = e.Label
                        e.Node.Name = e.Label
                        e.Node.EndEdit(False)
                        bTreeChanged = True
                    Else
                        ' Cancel the label edit action, inform the user, and 
                        ' place the node in edit mode again. 

                        e.CancelEdit = True
                        e.Node.BeginEdit()
                    End If
                Else
                    If e.Node.Text.Length = 0 Then
                        e.Node.Remove()
                    Else
                        e.CancelEdit = True
                    End If
                End If
            Else
                e.CancelEdit = True
            End If
        End Sub

        ''' <summary> 
        ''' Enables/Disables the Goto button 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_AfterSelect(ByVal sender As Object, ByVal e As TreeViewEventArgs) Handles tvwNamedViews.AfterSelect
            UpdateButtons()
        End Sub

        ''' <summary> 
        ''' Set the image of tree node 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_BeforeExpand(ByVal sender As Object, ByVal e As TreeViewCancelEventArgs) Handles tvwNamedViews.BeforeExpand
            Dim tNode As TreeNode = e.Node
            If Not TreeNodeUtil.IsViewNode(tNode) Then
                tNode.ImageIndex = 0
                tNode.SelectedImageIndex = 0
            End If
        End Sub

        ''' <summary> 
        ''' Set the image of tree node. 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_BeforeCollapse(ByVal sender As Object, ByVal e As TreeViewCancelEventArgs) Handles tvwNamedViews.BeforeCollapse
            Dim tNode As TreeNode = e.Node
            If Not TreeNodeUtil.IsViewNode(tNode) Then
                tNode.ImageIndex = 1
                tNode.SelectedImageIndex = 1
            End If
        End Sub

        ''' <summary> 
        ''' Same as Goto button handler. 
        ''' It sets the current view based on selected node. 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub tvwNamedViews_NodeMouseDoubleClick(ByVal sender As Object, ByVal e As TreeNodeMouseClickEventArgs) Handles tvwNamedViews.NodeMouseDoubleClick
            Dim tNode As TreeNode = e.Node
            If TreeNodeUtil.IsViewNode(tNode) Then
                ' get window id 
                Dim windowId As Integer = InteropHelper.GetMapWindowId()
                If windowId = 0 Then
                    Return
                End If

                Dim tNodeInfo As TreeNodeUtil.t_NodeInfo = DirectCast(tNode.Tag, TreeNodeUtil.t_NodeInfo)
                InteropHelper.SetView(windowId, tNodeInfo.m_x, tNodeInfo.m_y, tNodeInfo.m_zoom, tNodeInfo.m_unit, tNodeInfo.m_csys)
            End If
        End Sub

#End Region


#Region "[BUTTON HANDLERS]"
        ''' <summary> 
        ''' Add View handler. Gets the view information 
        ''' from running instance of MapInfo Professional App 
        ''' and prompts a user for the name of view. 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub btnAdd_Click(ByVal sender As Object, ByVal e As EventArgs) Handles btnAdd.Click
            ' get window id 
            Dim windowId As Integer = InteropHelper.GetMapWindowId()
            If windowId = 0 Then
                Return
            End If

            ' Get current view information from Mapper Window 
            Dim zoomValue As String, centerX As String, centerY As String
            Dim mapCSys, oldSessionCSys As String
            Dim mapUnit, oldSessionDistanceUnit As String

            ' Before we do any work involving the map's X/Y coordinates, we
            ' will set the current coordinate system; setting the coordsys 
            ' basically sets the units that will apply to the x/y coordinates. 
            ' Before we set the coorindate system, make note of the current 
            ' coordinate system, so that we can restore it later.  This way, in
            ' the unlikely event that the user typed a Set CoordSys statement into 
            ' the MapBasic window, we will preserve the coordsys typed in by the user. 

            ' Set the session coordinate system to match the coordsys of the map window 
            oldSessionCSys = InteropHelper.GetSessionCoordSys()   ' Get session coordsys string 
            mapCSys = InteropHelper.GetMapperCoordSys(windowId)   ' Get the map window's coordsys string
            InteropHelper.SetSessionCoordSys(mapCSys)

            centerX = InteropHelper.GetMapperCenterX(windowId)    ' Get CenterX 
            centerY = InteropHelper.GetMapperCenterY(windowId)    ' Get CenterY 

            InteropHelper.SetSessionCoordSys(oldSessionCSys)      ' restore original coordsys 

            ' Before we do any work involving distances (such as the zoom distance),
            ' we will want to set the session distance unit; we will set it to match 
            ' the distance unit in use by the map window. That way, we can record a 
            ' zoom distance in units that are unique to each map, e.g. 
            ' 5 "mi" 
            ' 1200 "m" 
            ' etc. 
            ' Before we set the session distance unit to match the map's unit, 
            ' make note of the original session distance unit, so we can restore it later. 
            oldSessionDistanceUnit = InteropHelper.GetSessionDistanceUnit()
            mapUnit = InteropHelper.GetMapperDistanceUnit(windowId)
            InteropHelper.SetSessionDistanceUnit(mapUnit)

            zoomValue = InteropHelper.GetMapperZoom(windowId)     ' Get the zoom value 

            InteropHelper.SetSessionDistanceUnit(oldSessionDistanceUnit)

            Dim addViewDlg As New AddNViewDlg()
            addViewDlg.m_currentZoom = InteropHelper.GetFormattedString(zoomValue)
            Dim dlgResult As DialogResult = addViewDlg.ShowDialog(Me)

            If dlgResult = Windows.Forms.DialogResult.OK Then
                Dim nodeName As String = addViewDlg.m_viewName
                AddNewNodeToTree(nodeName, centerX, centerY, zoomValue, mapUnit, mapCSys)
                UpdateButtons()
                bTreeChanged = True
            End If

            addViewDlg.Dispose()
        End Sub

        ''' <summary> 
        ''' Rename button handler. 
        ''' This function facilitates renaming of a folder name or a view name. 
        ''' Starts label editing on selected node. 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub btnRename_Click(ByVal sender As Object, ByVal e As EventArgs) Handles btnRename.Click
            If tvwNamedViews.SelectedNode IsNot Nothing Then
                tvwNamedViews.SelectedNode.BeginEdit()
            End If
        End Sub


        ''' <summary> 
        ''' New Folder button handler. 
        ''' This function adds a new folder to the treeview. 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub btnNewFolder_Click(ByVal sender As Object, ByVal e As EventArgs) Handles btnNewFolder.Click
            Dim tNode As TreeNode = tvwNamedViews.SelectedNode
            If tNode IsNot Nothing Then
                ' if selected node is a view node use its parent 
                If Not tNode.IsExpanded Then
                    tNode = tNode.Parent
                End If
            End If

            'TODO: Need to write a logic to generate some initial name for folder 
            Dim folderName As String = My.Resources.STR_DEF_FOLDER_NAME
            Dim newNode As TreeNode = Nothing

            ' add the node add appropriate location in the tree 
            If tNode IsNot Nothing Then
                folderName = GenerateNewFolderNameNoDuplicate(tNode.Nodes, folderName, 0)
                newNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tNode.Nodes, folderName)
                tNode.Expand()
            Else
                folderName = GenerateNewFolderNameNoDuplicate(tvwNamedViews.Nodes, folderName, 0)
                newNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tvwNamedViews.Nodes, folderName)
            End If

            bTreeChanged = True

            ' start the editing on the folder node so that 
            ' the user can change the folder name if required 
            newNode.BeginEdit()
        End Sub

        ''' <summary> 
        ''' Moves a node (view of folder node) to a folder node 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub btnMove_Click(ByVal sender As Object, ByVal e As EventArgs) Handles btnMove.Click
            ' Write any changes to XML file. 
            WriteTreeToFile(sXMLFile)

            ' Get the node that will be moved 
            Dim srcNode As TreeNode = tvwNamedViews.SelectedNode

            If srcNode Is Nothing Then
                Return
            End If

            ' Show the folders dialog to select the destination folder 
            Dim moveSelDlg As New MoveSelNodeDlg()
            moveSelDlg.m_sXMLFile = sXMLFile
            Dim dlgResult As DialogResult = moveSelDlg.ShowDialog(Me)

            ' If user clicked on OK button 
            If dlgResult = Windows.Forms.DialogResult.Yes Then
                Dim nodeFullPath As String = moveSelDlg.m_sSelectedNodeFullPath
                ' Locate the destination folder in the local tree view 
                Dim destNode As TreeNode = Nothing

                If Not TreeNodeUtil.IsViewNode(srcNode) Then
                    srcNode.Collapse()
                    srcNode.ImageIndex = 1
                End If

                If nodeFullPath.Length > 0 Then

                    destNode = TreeNodeUtil.GetNodeFromPath(tvwNamedViews.Nodes, nodeFullPath, tvwNamedViews.PathSeparator)

                    If Not destNode.Equals(srcNode) Then
                        ' Do not allow a node to be dropped on a child/grand child 
                        If TreeNodeUtil.ContainsNode(srcNode, destNode) Then
                            MessageBox.Show(My.Resources.ERR_INVALID_DROP, My.Resources.ERR_INVALID_DROP_MSG_TITLE, MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
                            Return
                        End If

                        ' Move the node 
                        destNode.Nodes.Add(DirectCast(srcNode.Clone(), TreeNode))
                        destNode.Expand()
                        destNode.ImageIndex = 0
                        destNode.SelectedImageIndex = 0
                    End If
                Else
                    tvwNamedViews.Nodes.Add(DirectCast(srcNode.Clone(), TreeNode))
                End If

                Dim srcNodeParent As TreeNode = srcNode.Parent
                srcNode.Remove()
                If srcNodeParent IsNot Nothing Then
                    If srcNodeParent.Nodes.Count = 0 Then

                        srcNodeParent.Collapse()
                        srcNodeParent.ImageIndex = 1
                        srcNodeParent.SelectedImageIndex = 1

                    End If
                End If

                bTreeChanged = True
            End If

            moveSelDlg.Dispose()

        End Sub


        ''' <summary> 
        ''' Delete button handler. 
        ''' This function confirms the deletion and deletes a selected node. 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub btnDelete_Click(ByVal sender As Object, ByVal e As EventArgs) Handles btnDelete.Click
            ' If there is a selected node display a confirmation message 
            If tvwNamedViews.SelectedNode IsNot Nothing Then
                Dim dlgResult As DialogResult = MessageBox.Show(My.Resources.CONFIRM_NODE_DELETE, My.Resources.CONFIRM_NODE_DELETE_MSG_TITLE, MessageBoxButtons.YesNo, MessageBoxIcon.Warning, MessageBoxDefaultButton.Button2)
                ' If user confirms deletion delete the selected node 
                If dlgResult = Windows.Forms.DialogResult.Yes Then
                    tvwNamedViews.SelectedNode.Remove()
                    UpdateButtons()
                    bTreeChanged = True
                End If
            End If
        End Sub

        ''' <summary>
        ''' On closing the dock window we will also like to update the Xml file
        ''' </summary>
        Public Sub CloseDockWindow()
            ''Write out the XML file that stores the Named Views info
            WriteTreeToFile(sXMLFile)
            _controller.DockWindowClose()
        End Sub
        ''' <summary>
        ''' Set the dialog position and docking state 
        ''' </summary>
        Public Sub SetDockPosition()
            _controller.SetDockWindowPositionFromFile()
        End Sub



        ''' <summary> 
        ''' Goto button handler. 
        ''' This function gets the top mapper window. 
        ''' It then reads the View node information from 
        ''' the selected TreeNode and sets the current view 
        ''' of Mapper window. 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub btnGoto_Click(ByVal sender As Object, ByVal e As EventArgs) Handles btnGoto.Click
            ' Get the selected node in the tree 
            ' Note: if there is no selected node in the tree 
            Dim tNode As TreeNode = tvwNamedViews.SelectedNode

            If tNode Is Nothing Then
                Return
            End If

            If Not TreeNodeUtil.IsViewNode(tNode) Then
                Return
            End If

            ' get window id 
            Dim windowId As Integer = InteropHelper.GetMapWindowId()
            If windowId = 0 Then
                Return
            End If

            Dim tNodeInfo As TreeNodeUtil.t_NodeInfo = DirectCast(tNode.Tag, TreeNodeUtil.t_NodeInfo)
            InteropHelper.SetView(windowId, tNodeInfo.m_x, tNodeInfo.m_y, tNodeInfo.m_zoom, tNodeInfo.m_unit, tNodeInfo.m_csys)

        End Sub

#End Region


#Region "[HELPER FUNCTIONS]"
        ' This function accepts and initial name and counter and 
        ' generates a name unique to a collection of nodes which 
        ' is passed to this function as first parameter 
        ''' <summary> 
        ''' This function accepts and initial name and counter and 
        ''' generates a name unique to a collection of nodes which 
        ''' is passed to this function as first parameter. 
        ''' </summary> 
        ''' <param name="checkNodes">Collection of tree nodes to check for duplicate names</param> 
        ''' <param name="initialName">Initial name</param> 
        ''' <param name="iCtr">A counter that will be used as suffix to initial name 
        ''' when a duplicate name is found. This counter is incremented 
        ''' until a unique name is reached.</param> 
        ''' <returns></returns> 
        Private Function GenerateNewFolderNameNoDuplicate(ByVal checkNodes As TreeNodeCollection, ByVal initialName As String, ByVal iCtr As Integer) As String

            Dim folderName As String = initialName
            If iCtr > 0 Then
                If System.Threading.Thread.CurrentThread.CurrentUICulture.TextInfo.IsRightToLeft Then
                    folderName = "(" + Convert.ToString(iCtr) + ")" + folderName
                Else
                    folderName = folderName + "(" + Convert.ToString(iCtr) + ")"
                End If
            End If

            For Each tn As TreeNode In checkNodes
                If String.Compare(tn.Text, folderName) = 0 Then
                    iCtr += 1
                    folderName = GenerateNewFolderNameNoDuplicate(checkNodes, initialName, iCtr)
                    Exit For
                End If
            Next
            Return folderName
        End Function

        ''' <summary> 
        ''' This function uses the input from Add New View dialog and 
        ''' add a new node to the treeview control which represents a view 
        ''' </summary> 
        ''' <param name="nodeName"></param> 
        ''' <param name="x"></param> 
        ''' <param name="y"></param> 
        ''' <param name="zoom"></param> 
        Private Sub AddNewNodeToTree(ByVal nodeName As String, ByVal x As String, ByVal y As String, ByVal zoom As String, ByVal unit As String, ByVal csys As String)
            ' Get the selected node 
            Dim tNode As TreeNode = tvwNamedViews.SelectedNode
            If tNode IsNot Nothing Then
                ' if selected node is a view node use its parent 
                If Not tNode.IsExpanded Then
                    tNode = tNode.Parent
                End If
            End If

            ' add the node add appropriate location in the tree 
            If tNode IsNot Nothing Then
                TreeNodeUtil.AddViewNodeToNodeCollection(tNode.Nodes, nodeName, x, y, zoom, unit, csys)
                tNode.Expand()
            Else
                TreeNodeUtil.AddViewNodeToNodeCollection(tvwNamedViews.Nodes, nodeName, x, y, zoom, unit, csys)
            End If
        End Sub

        ''' <summary> 
        ''' This function accepts the name of xml file 
        ''' and fill the content of xml file in the 
        ''' treeview control 
        ''' </summary> 
        ''' <param name="fName"></param> 
        Private Sub LoadTreeFromFile(ByVal fName As String)
            Dim sErr As String = String.Empty

            Dim rootNode As XmlNode = Nothing

            ' Wait until safe to read from file 
            mut.WaitOne()

            ' Try to read the xml file 
            Dim xmlDoc As New XmlDocument()
            Try
                'if (!System.IO.File.Exists(fName)) 
                ' throw new XmlException("XML file doesnot exist"); 

                ' Load the xml file 
                xmlDoc.Load(fName)

                ' Jump to the dialog node 
                Dim xmlNodeList As XmlNodeList = xmlDoc.SelectNodes(STR_PATH_DIALOG)

                If xmlNodeList Is Nothing Then
                    Throw New XmlException(My.Resources.ERR_INVALID_XML)
                End If

                Dim dialogNode As XmlNode = xmlNodeList(0)
                If dialogNode Is Nothing Then
                    Throw New XmlException(My.Resources.ERR_INVALID_XML)
                End If

                ' Preserve the dialog dimensions 
                dialogLeft = Convert.ToInt32(dialogNode.Attributes(STR_LEFT).Value)
                dialogTop = Convert.ToInt32(dialogNode.Attributes(STR_TOP).Value)
                dialogWidth = Convert.ToInt32(dialogNode.Attributes(STR_WIDTH).Value)
                dialogHeight = Convert.ToInt32(dialogNode.Attributes(STR_HEIGHT).Value)

                ' Jump to the root node (it contains all the top level nodes) 
                ' This node is not displayed in TreeView. It represent the 
                ' TreeView itself. 
                xmlNodeList = xmlDoc.SelectNodes(STR_PATH_ROOT_FOLDER)

                If xmlNodeList Is Nothing Then
                    Throw New XmlException(My.Resources.ERR_INVALID_XML)
                End If

                rootNode = xmlNodeList(0)
                If rootNode Is Nothing Then
                    Throw New XmlException(My.Resources.ERR_INVALID_XML)
                End If


                ' traverse all the folder and view nodes in XML file 
                For Each xmlNode As XmlNode In rootNode.ChildNodes
                    Dim tNode As TreeNode = Nothing
                    If String.Compare(xmlNode.Name, STR_VIEWS, True) = 0 Then
                        tNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tvwNamedViews.Nodes, xmlNode.Attributes("Name").Value)
                        TreeNodeUtil.FillTreeNode(tNode, xmlNode)
                    Else
                        tNode = TreeNodeUtil.AddViewNodeToNodeCollection(tvwNamedViews.Nodes, xmlNode.InnerText, xmlNode.Attributes("X").Value, xmlNode.Attributes("Y").Value, xmlNode.Attributes("Zoom").Value, xmlNode.Attributes("Unit").Value, xmlNode.Attributes("CoordSys").Value)
                    End If
                Next
            Catch ex As System.Xml.XPath.XPathException
                sErr = ex.Message
            Catch ex As XmlException
                sErr = ex.Message
            Catch ex As ArgumentException
                sErr = ex.Message
            Catch generatedExceptionName As FileNotFoundException
                sErr = String.Empty
            End Try

            If sErr <> String.Empty Then
                MessageBox.Show(sErr)
            End If

            bTreeChanged = False

            'release the mutex 
            mut.ReleaseMutex()
        End Sub

        ' This function writes the treeview to the xml file. 
        ' It uses mutexes to synchronize the threads accessing 
        ' the xml file 
        Private Sub WriteTreeToFile(ByVal fName As String)
            Dim sErr As String = String.Empty

            If Not bTreeChanged Then
                Return
            End If

            'wait until safe to read from file 
            mut.WaitOne()

            Try
                Dim xw As New XmlTextWriter(fName, System.Text.Encoding.Unicode)

                ' Use indenting for readability. 
                xw.Formatting = Formatting.Indented

                ' write the XML declaration 
                xw.WriteStartDocument()

                ' write the root element (represents the tool itself) 
                xw.WriteStartElement(STR_NAMEDVIEWS)

                ' write the dimensions of dialog 
                xw.WriteStartElement(STR_DIALOG)
                xw.WriteAttributeString(STR_LEFT, Convert.ToString(Me.Left))
                xw.WriteAttributeString(STR_TOP, Convert.ToString(Me.Top))
                xw.WriteAttributeString(STR_WIDTH, Convert.ToString(Me.Width))
                xw.WriteAttributeString(STR_HEIGHT, Convert.ToString(Me.Height))
                xw.WriteEndElement()


                ' Write the root node which contains all the other nodes 
                ' This node is never displayed in the tree view it simply 
                ' contains all the other nodes 
                xw.WriteStartElement(STR_VIEWS)
                xw.WriteAttributeString(STR_NAME, STR_ROOT)

                ' start writing the nodes in the tree 
                For Each tn As TreeNode In tvwNamedViews.Nodes
                    If TreeNodeUtil.IsViewNode(tn) Then
                        TreeNodeUtil.WriteViewNodeToFile(xw, tn)
                    Else
                        TreeNodeUtil.WriteFolderNodeToFile(xw, tn)
                    End If
                Next

                ' end the root node element (the container of all nodes) 
                xw.WriteEndElement()

                ' end the root element (represent the tool) 
                xw.WriteEndElement()

                ' finish the write operation 
                xw.Flush()

                xw.Close()
            Catch ex As DirectoryNotFoundException
                sErr = ex.Message
            Catch ex As IOException
                sErr = ex.Message
            Catch ex As UnauthorizedAccessException
                sErr = ex.Message
            Catch ex As InvalidOperationException
                sErr = ex.Message
            Catch ex As ArgumentException
                sErr = ex.Message
            End Try

            If sErr <> String.Empty Then
                MessageBox.Show(sErr)
            End If

            bTreeChanged = False

            'release the mutex 
            mut.ReleaseMutex()
        End Sub


        ''' <summary> 
        ''' Enables and disables command buttons based on the treeview state 
        ''' </summary> 
        Private Sub UpdateButtons() 
            btnGoto.Enabled = (tvwNamedViews.Nodes.Count > 0 AndAlso tvwNamedViews.SelectedNode IsNot Nothing AndAlso TreeNodeUtil.IsViewNode(tvwNamedViews.SelectedNode)) 
            btnMove.Enabled = (tvwNamedViews.Nodes.Count > 0 AndAlso tvwNamedViews.SelectedNode IsNot Nothing) 
            btnRename.Enabled = (tvwNamedViews.Nodes.Count > 0 AndAlso tvwNamedViews.SelectedNode IsNot Nothing) 
            btnDelete.Enabled = (tvwNamedViews.Nodes.Count > 0 AndAlso tvwNamedViews.SelectedNode IsNot Nothing) 
            
        End Sub 
        
#End Region

    End Class
End Namespace