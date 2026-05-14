Namespace MISamples
    Partial Class MoveSelNodeDlg
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
            Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(MoveSelNodeDlg))
            Me.tvwFolders = New System.Windows.Forms.TreeView
            Me.imageList1 = New System.Windows.Forms.ImageList(Me.components)
            Me.cmdOK = New System.Windows.Forms.Button
            Me.cmdCancel = New System.Windows.Forms.Button
            Me.SuspendLayout()
            '
            'tvwFolders
            '
            resources.ApplyResources(Me.tvwFolders, "tvwFolders")
            Me.tvwFolders.FullRowSelect = True
            Me.tvwFolders.HideSelection = False
            Me.tvwFolders.ImageList = Me.imageList1
            Me.tvwFolders.Name = "tvwFolders"
            Me.tvwFolders.ShowLines = False
            Me.tvwFolders.ShowPlusMinus = False
            Me.tvwFolders.ShowRootLines = False
            '
            'imageList1
            '
            Me.imageList1.ImageStream = CType(resources.GetObject("imageList1.ImageStream"), System.Windows.Forms.ImageListStreamer)
            Me.imageList1.TransparentColor = System.Drawing.Color.Transparent
            Me.imageList1.Images.SetKeyName(0, "OPENFOLD.ICO")
            Me.imageList1.Images.SetKeyName(1, "CLSDFOLD.ICO")
            '
            'cmdOK
            '
            resources.ApplyResources(Me.cmdOK, "cmdOK")
            Me.cmdOK.DialogResult = System.Windows.Forms.DialogResult.Yes
            Me.cmdOK.Name = "cmdOK"
            Me.cmdOK.UseVisualStyleBackColor = True
            '
            'cmdCancel
            '
            resources.ApplyResources(Me.cmdCancel, "cmdCancel")
            Me.cmdCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
            Me.cmdCancel.Name = "cmdCancel"
            Me.cmdCancel.UseVisualStyleBackColor = True
            '
            'MoveSelNodeDlg
            '
            resources.ApplyResources(Me, "$this")
            Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
            Me.CancelButton = Me.cmdCancel
            Me.Controls.Add(Me.cmdCancel)
            Me.Controls.Add(Me.cmdOK)
            Me.Controls.Add(Me.tvwFolders)
            Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
            Me.MaximizeBox = False
            Me.MinimizeBox = False
            Me.Name = "MoveSelNodeDlg"
            Me.ShowInTaskbar = False
            Me.ResumeLayout(False)

        End Sub

#End Region

        Friend WithEvents tvwFolders As System.Windows.Forms.TreeView
        Friend WithEvents cmdOK As System.Windows.Forms.Button
        Friend WithEvents cmdCancel As System.Windows.Forms.Button
        Friend WithEvents imageList1 As System.Windows.Forms.ImageList
    End Class
End Namespace