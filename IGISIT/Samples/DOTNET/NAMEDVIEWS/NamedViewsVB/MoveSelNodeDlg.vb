Imports System
Imports System.Windows.Forms
Imports System.Xml

Namespace MISamples
    Public Partial Class MoveSelNodeDlg 
        Inherits Form
        Private Const STR_VIEWS As String = "Views"
        Private Const STR_NAME As String = "Name"

        Private Const STR_PATH_ROOT_FOLDER As String = "/NamedViews/Views"

        Public m_sXMLFile As String
        Public m_sSelectedNodeFullPath As String


        Public Sub New()
            InitializeComponent()
        End Sub

#Region "[DIALOG EVENT HANDLERS]"

        Private Sub MoveSelNodeDlg_Load(ByVal sender As Object, ByVal e As EventArgs) Handles MyBase.Load
            LoadTreeFromFile(m_sXMLFile)
            If tvwFolders.Nodes.Count > 0 Then
                tvwFolders.Nodes(0).Expand()
            End If
        End Sub

        Private Sub MoveSelNodeDlg_FormClosing(ByVal sender As Object, ByVal e As FormClosingEventArgs) Handles MyBase.FormClosing
            If e.CloseReason = CloseReason.UserClosing Then
                e.Cancel = True
                Me.Hide()
            End If
        End Sub

#End Region

#Region "[TREEVIEW EVENT HANDLERS]"

        Private Sub tvwFolders_BeforeExpand(ByVal sender As Object, ByVal e As TreeViewCancelEventArgs) Handles tvwFolders.BeforeExpand
            Dim tNode As TreeNode = e.Node
            tNode.ImageIndex = 0
            tNode.SelectedImageIndex = 0
        End Sub

        Private Sub tvwFolders_BeforeCollapse(ByVal sender As Object, ByVal e As TreeViewCancelEventArgs) Handles tvwFolders.BeforeCollapse
            Dim tNode As TreeNode = e.Node
            tNode.ImageIndex = 1
            tNode.SelectedImageIndex = 1
        End Sub

#End Region
        
#Region "[BUTTON HANDLERS]"

        Private Sub cmdOK_Click(ByVal sender As Object, ByVal e As EventArgs) Handles cmdOK.Click
            If tvwFolders.SelectedNode IsNot Nothing Then
                If tvwFolders.Nodes(0).Equals(tvwFolders.SelectedNode) Then
                    m_sSelectedNodeFullPath = String.Empty
                Else
                    m_sSelectedNodeFullPath = tvwFolders.SelectedNode.FullPath.Substring(tvwFolders.SelectedNode.FullPath.IndexOf(tvwFolders.PathSeparator) + 1)
                End If
            End If
            Me.Hide()
        End Sub

#End Region

#Region "[HELPER FUNCTIONS]"

        ''' <summary> 
        ''' This function accepts the name of xml file 
        ''' and fill the content of xml file in the 
        ''' treeview control 
        ''' </summary> 
        ''' <param name="fName"></param> 
        Private Sub LoadTreeFromFile(ByVal fName As String)
            Dim sErr As String = String.Empty

            Dim rootNode As XmlNode = Nothing

            ' Try to read the xml file 
            Dim xmlDoc As New XmlDocument()
            Try
                ' Load the xml file 
                xmlDoc.Load(fName)

                ' Jump to the root node (it contains all the top level nodes) 
                ' This node is not displayed in TreeView. It represent the 
                ' TreeView itself. 
                Dim xmlNodeList As XmlNodeList = xmlDoc.SelectNodes(STR_PATH_ROOT_FOLDER)

                If xmlNodeList Is Nothing Then
                    Throw New XmlException(My.Resources.ERR_INVALID_XML)
                End If

                rootNode = xmlNodeList(0)
                If rootNode Is Nothing Then
                    Throw New XmlException(My.Resources.ERR_INVALID_XML)
                End If

                Dim topNode As TreeNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tvwFolders.Nodes, My.Resources.STR_MB_APP_DESC)

                ' traverse all the folder and view nodes in XML file 
                For Each xmlNode As XmlNode In rootNode.ChildNodes
                    Dim tNode As TreeNode = Nothing
                    If String.Compare(xmlNode.Name, STR_VIEWS, True) = 0 Then
                        tNode = TreeNodeUtil.AddFolderNodeToNodeCollection(topNode.Nodes, xmlNode.Attributes(STR_NAME).Value)
                        TreeNodeUtil.FillTreeNodeOnlyFolders(tNode, xmlNode)

                    End If
                Next
            Catch ex As System.Xml.XPath.XPathException
                sErr = ex.Message
            Catch ex As XmlException
                sErr = ex.Message
            Catch ex As ArgumentException
                sErr = ex.Message
            End Try

            If sErr <> String.Empty Then
                MessageBox.Show(sErr)
            End If

        End Sub

#End Region

    End Class
End Namespace