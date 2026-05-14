Imports System
Imports System.Windows.Forms
Imports System.Xml

Namespace MISamples
    NotInheritable Class TreeNodeUtil 
        Private Sub New() 
        End Sub 
        Private Const STR_VIEWS As String = "Views"
        Private Const STR_NAME As String = "Name"
        Private Const STR_VIEW As String = "View"
        Private Const STR_X As String = "X"
        Private Const STR_Y As String = "Y"
        Private Const STR_ZOOM As String = "Zoom"
        Private Const STR_UNIT As String = "Unit"
        Private Const STR_CSYS As String = "CoordSys"

        ''' <summary>
        ''' This structure will be used
        ''' to store the information of 
        ''' each node.
        ''' </summary>
        Public Structure t_NodeInfo
            Public m_nodeTypeView As Boolean
            Public m_zoom As String
            Public m_unit As String
            Public m_x As String
            Public m_y As String
            Public m_csys As String

            Public Sub New(ByVal nodeTypeView As Boolean)
                m_nodeTypeView = nodeTypeView
                m_zoom = "0"
                m_x = "0"
                m_y = "0"
                m_unit = "mi"
                m_csys = "CoordSys Earth"
            End Sub
        End Structure

#Region "[ADD NODES TO TREE]"
        
        ''' <summary>
        ''' Reads child nodes from the XmlNode and adds them to recursively
        ''' to the TreeNode
        ''' </summary>
        ''' <param name="treeNode">The tree node to fill</param>
        ''' <param name="xmlNode">The xml node to read from</param>
        Public Shared Sub FillTreeNode(ByVal treeNode As TreeNode, ByVal xmlNode As XmlNode)
            If xmlNode.HasChildNodes Then
                For Each n As XmlNode In xmlNode.ChildNodes
                    Dim tNode As TreeNode = Nothing
                    If String.Compare(n.Name, STR_VIEWS, True) = 0 Then
                        tNode = AddFolderNodeToNodeCollection(treeNode.Nodes, n.Attributes(STR_NAME).Value)
                        FillTreeNode(tNode, n)
                    Else
                        tNode = AddViewNodeToNodeCollection(treeNode.Nodes, n.InnerText, n.Attributes("X").Value, n.Attributes("Y").Value, n.Attributes("Zoom").Value, n.Attributes("Unit").Value, n.Attributes("CoordSys").Value)
                    End If
                Next 
            End If
        End Sub

        ''' <summary>
        ''' Reads child nodes from the XmlNode and adds folders recursively
        ''' to the TreeNode
        ''' </summary>
        ''' <param name="treeNode">The tree node to fill</param>
        ''' <param name="xmlNode">The xml node to read from</param>
        Public Shared Sub FillTreeNodeOnlyFolders(ByVal treeNode As TreeNode, ByVal xmlNode As XmlNode)
            If xmlNode.HasChildNodes Then
                For Each n As XmlNode In xmlNode.ChildNodes
                    Dim tNode As TreeNode = Nothing
                    If String.Compare(n.Name, STR_VIEWS, True) = 0 Then
                        tNode = AddFolderNodeToNodeCollection(treeNode.Nodes, n.Attributes(STR_NAME).Value)
                        FillTreeNodeOnlyFolders(tNode, n) 
                    End If
                Next 
            End If
        End Sub

        ''' <summary>
        ''' Add node to the node collection as a folder node.
        ''' </summary>
        ''' <param name="nodCol">The node collection to add a folder node to.</param>
        ''' <param name="nodeName">Name of the folder</param>
        ''' <returns>The newly added tree node</returns>
        Public Shared Function AddFolderNodeToNodeCollection(ByVal nodCol As TreeNodeCollection, ByVal nodeName As String) As TreeNode
            ' create node information for a folder node
            Dim nodeInfo As New t_NodeInfo(False)

            ' setup the new View node with node information
            Dim newNode As New TreeNode()
            newNode.ImageIndex = 1
            newNode.SelectedImageIndex = 1
            newNode.Tag = nodeInfo
            newNode.Text = nodeName
            newNode.Name = nodeName

            nodCol.Add(newNode)
            
            newNode.ToolTipText = newNode.FullPath

            Return newNode

        End Function

        ''' <summary>
        ''' Add a view node with view information to the tree node collection.
        ''' </summary>
        ''' <param name="nodCol">The node collection to add a view node to.</param>
        ''' <param name="nodeName">Name of the view</param>
        ''' <param name="x">Center X of the view</param>
        ''' <param name="y">Center Y of the view</param>
        ''' <param name="zoom">Zoom of the view</param>
        ''' <returns>The newly added tree node</returns>
        Public Shared Function AddViewNodeToNodeCollection(ByVal nodCol As TreeNodeCollection, ByVal nodeName As String, ByVal x As String, ByVal y As String, ByVal zoom As String, ByVal unit As String, ByVal csys As String) As TreeNode
            ' setup the node information
            Dim nodeInfo As New t_NodeInfo(True)
            nodeInfo.m_x = x
            nodeInfo.m_y = y
            nodeInfo.m_zoom = zoom
            nodeInfo.m_unit = unit
            nodeInfo.m_csys = csys

            ' setup the new View node with node information
            Dim newNode As New TreeNode()

            newNode.ImageIndex = 2
            newNode.SelectedImageIndex = 2
            newNode.Tag = nodeInfo
            newNode.Text = nodeName
            newNode.Name = nodeName
            newNode.ToolTipText = String.Format(My.Resources.STR_TOOLTIP_VIEW, InteropHelper.GetFormattedString(nodeInfo.m_x), InteropHelper.GetFormattedString(nodeInfo.m_y), InteropHelper.GetFormattedString(nodeInfo.m_zoom), nodeInfo.m_unit)

            nodCol.Add(newNode)

            Return newNode

        End Function

#End Region

#Region "[WRITE TREE NODES TO XML]"

        ''' <summary>
        ''' Writes a view to xml file
        ''' </summary>
        ''' <param name="xw"></param>
        ''' <param name="node"></param>
        Public Shared Sub WriteViewNodeToFile(ByVal xw As XmlTextWriter, ByVal node As TreeNode)
            If node Is Nothing Then
                Return
            End If

            Dim nodeInfo As t_NodeInfo = DirectCast(node.Tag, t_NodeInfo) 
            xw.WriteStartElement(STR_VIEW)
            xw.WriteAttributeString(STR_X, Convert.ToString(nodeInfo.m_x))
            xw.WriteAttributeString(STR_Y, Convert.ToString(nodeInfo.m_y))
            xw.WriteAttributeString(STR_ZOOM, Convert.ToString(nodeInfo.m_zoom))
            xw.WriteAttributeString(STR_UNIT, Convert.ToString(nodeInfo.m_unit))
            xw.WriteAttributeString(STR_CSYS, Convert.ToString(nodeInfo.m_csys))
            xw.WriteValue(node.Text)
            xw.WriteEndElement()
        End Sub

        ''' <summary>
        ''' Writes a folder to the xml file
        ''' </summary>
        ''' <param name="xw"></param>
        ''' <param name="node"></param>
        Public Shared Sub WriteFolderNodeToFile(ByVal xw As XmlTextWriter, ByVal node As TreeNode)
            If node Is Nothing Then
                Return
            End If
            xw.WriteStartElement(STR_VIEWS)
            xw.WriteAttributeString(STR_NAME, node.Text)
            For Each tn As TreeNode In node.Nodes
                If TreeNodeUtil.IsViewNode(tn) Then
                    WriteViewNodeToFile(xw, tn)
                Else
                    WriteFolderNodeToFile(xw, tn)
                End If
            Next 
            xw.WriteEndElement()

        End Sub

#End Region

#Region "[VALIDATE CONDITIONS]"

        ''' <summary>
        ''' This function tells if a tree node represents a View Node.
        ''' </summary>
        ''' <param name="node">The TreeNode to be checked.</param>
        ''' <returns>true if tree node is a view node.</returns>
        Public Shared Function IsViewNode(ByVal node As TreeNode) As Boolean
            Dim nodeInfo As t_NodeInfo = DirectCast(node.Tag, t_NodeInfo) 
            Return nodeInfo.m_nodeTypeView
        End Function

        ''' <summary>
        ''' Searches the container node recursively to look check
        ''' if the contained node is a child/grand child.
        ''' </summary>
        ''' <param name="container">The node to seach recursively</param>
        ''' <param name="contained">The node to be checked as a child/grand child</param>
        ''' <returns></returns>
        Public Shared Function ContainsNode(ByVal container As TreeNode, ByVal contained As TreeNode) As Boolean
            Dim ret As Boolean = container.Nodes.Contains(contained) 
            'false; 
            For Each tn As TreeNode In container.Nodes
                If tn.Equals(contained) Then
                    ret = True
                    Exit For
                End If
                If tn.Nodes.Count > 0 Then
                    If ContainsNode(tn, contained) Then
                        ret = True
                        Exit For
                    End If
                End If
            Next 
            Return ret
        End Function

#End Region

#Region "[TREEVIEW SEARCH]"

        ''' <summary>
        ''' Retrieves a TreeNode based on its path.
        ''' </summary>
        ''' <param name="nodCol">The node collection where the search starts.</param>
        ''' <param name="fullPath">The path to node relative to node collection.</param>
        ''' <param name="pathSep">Path separator.</param>
        ''' <returns></returns>
        Public Shared Function GetNodeFromPath(ByVal nodCol As TreeNodeCollection, ByVal fullPath As String, ByVal pathSep As String) As TreeNode
            Dim retNode As TreeNode = Nothing
            
            Dim sep As String() = {pathSep} 
            Dim nodes As String() = fullPath.Split(sep, StringSplitOptions.None) 
            Dim curCol As TreeNodeCollection = nodCol
            For i As Integer = 0 To nodes.Length - 1
                Dim nodesFound As TreeNode() = curCol.Find(nodes(i), False) 
                retNode = nodesFound(0) 
                curCol = retNode.Nodes
            Next 
            Return retNode
        End Function

#End Region

    End Class
End Namespace