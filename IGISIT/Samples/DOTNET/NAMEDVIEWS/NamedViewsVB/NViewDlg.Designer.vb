Namespace MISamples
    Partial Class NViewDlg
        ''' <summary> 
        ''' Required designer variable. 
        ''' </summary> 
        Private components As System.ComponentModel.IContainer = Nothing

        ''' <summary> 
        ''' Clean up any resources being used. 
        ''' </summary> 
        ''' <param name="disposing">true if managed resources should be disposed; otherwise, false.</param> 
        Protected Overloads Overrides Sub Dispose(ByVal disposing As Boolean)
            If disposing AndAlso (components IsNot Nothing) Then
                components.Dispose()
            End If
            MyBase.Dispose(disposing)
        End Sub

#Region "Windows Form Designer generated code"

        ''' <summary> 
        ''' Required method for Designer support - do not modify 
        ''' the contents of this method with the code editor. 
        ''' </summary> 
        Private Sub InitializeComponent()
            Me.components = New System.ComponentModel.Container
            Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(NViewDlg))
            Me.tvwNamedViews = New System.Windows.Forms.TreeView
            Me.imageList1 = New System.Windows.Forms.ImageList(Me.components)
            Me.btnDelete = New System.Windows.Forms.Button
            Me.btnRename = New System.Windows.Forms.Button
            Me.btnMove = New System.Windows.Forms.Button
            Me.btnNewFolder = New System.Windows.Forms.Button
            Me.btnGoto = New System.Windows.Forms.Button
            Me.btnAdd = New System.Windows.Forms.Button
            Me.SuspendLayout()
            '
            'tvwNamedViews
            '
            Me.tvwNamedViews.AllowDrop = True
            resources.ApplyResources(Me.tvwNamedViews, "tvwNamedViews")
            Me.tvwNamedViews.FullRowSelect = True
            Me.tvwNamedViews.HideSelection = False
            Me.tvwNamedViews.ImageList = Me.imageList1
            Me.tvwNamedViews.LabelEdit = True
            Me.tvwNamedViews.Name = "tvwNamedViews"
            Me.tvwNamedViews.ShowNodeToolTips = True
            '
            'imageList1
            '
            Me.imageList1.ImageStream = CType(resources.GetObject("imageList1.ImageStream"), System.Windows.Forms.ImageListStreamer)
            Me.imageList1.TransparentColor = System.Drawing.Color.Transparent
            Me.imageList1.Images.SetKeyName(0, "OPENFOLD.ICO")
            Me.imageList1.Images.SetKeyName(1, "CLSDFOLD.ICO")
            Me.imageList1.Images.SetKeyName(2, "Globe.ico")
            '
            'btnDelete
            '
            resources.ApplyResources(Me.btnDelete, "btnDelete")
            Me.btnDelete.Name = "btnDelete"
            Me.btnDelete.UseVisualStyleBackColor = True
            '
            'btnRename
            '
            resources.ApplyResources(Me.btnRename, "btnRename")
            Me.btnRename.Name = "btnRename"
            Me.btnRename.UseVisualStyleBackColor = True
            '
            'btnMove
            '
            resources.ApplyResources(Me.btnMove, "btnMove")
            Me.btnMove.Name = "btnMove"
            Me.btnMove.UseVisualStyleBackColor = True
            '
            'btnNewFolder
            '
            resources.ApplyResources(Me.btnNewFolder, "btnNewFolder")
            Me.btnNewFolder.Name = "btnNewFolder"
            Me.btnNewFolder.UseVisualStyleBackColor = True
            '
            'btnGoto
            '
            resources.ApplyResources(Me.btnGoto, "btnGoto")
            Me.btnGoto.Name = "btnGoto"
            Me.btnGoto.UseVisualStyleBackColor = True
            '
            'btnAdd
            '
            resources.ApplyResources(Me.btnAdd, "btnAdd")
            Me.btnAdd.Name = "btnAdd"
            Me.btnAdd.UseVisualStyleBackColor = True
            '
            'NViewDlg
            '
            resources.ApplyResources(Me, "$this")
            Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
            Me.Controls.Add(Me.btnGoto)
            Me.Controls.Add(Me.btnAdd)
            Me.Controls.Add(Me.btnDelete)
            Me.Controls.Add(Me.btnRename)
            Me.Controls.Add(Me.btnMove)
            Me.Controls.Add(Me.btnNewFolder)
            Me.Controls.Add(Me.tvwNamedViews)
            Me.MinimumSize = New System.Drawing.Size(300, 300)
            Me.Name = "NViewDlg"
            Me.ResumeLayout(False)

        End Sub

#End Region

        Friend WithEvents tvwNamedViews As System.Windows.Forms.TreeView
        Friend WithEvents btnDelete As System.Windows.Forms.Button
        Friend WithEvents btnRename As System.Windows.Forms.Button
        Friend WithEvents btnMove As System.Windows.Forms.Button
        Friend WithEvents btnNewFolder As System.Windows.Forms.Button
        Friend WithEvents btnGoto As System.Windows.Forms.Button
        Friend WithEvents btnAdd As System.Windows.Forms.Button
        Friend WithEvents imageList1 As System.Windows.Forms.ImageList

    End Class
End Namespace