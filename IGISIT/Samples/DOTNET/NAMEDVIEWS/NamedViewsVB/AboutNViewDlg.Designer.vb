Namespace MISamples
    Partial Class AboutNViewDlg
        ''' <summary> 
        ''' Required designer variable. 
        ''' </summary> 
        Private components As System.ComponentModel.IContainer = Nothing

        ''' <summary> 
        ''' Clean up any resources being used. 
        ''' </summary> 
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
            Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(AboutNViewDlg))
            Me.tableLayoutPanel = New System.Windows.Forms.TableLayoutPanel
            Me.logoPictureBox = New System.Windows.Forms.PictureBox
            Me.labelProductName = New System.Windows.Forms.Label
            Me.labelVersion = New System.Windows.Forms.Label
            Me.labelCopyright = New System.Windows.Forms.Label
            Me.labelCompanyName = New System.Windows.Forms.Label
            Me.textBoxDescription = New System.Windows.Forms.TextBox
            Me.okButton = New System.Windows.Forms.Button
            Me.tableLayoutPanel.SuspendLayout()
            CType(Me.logoPictureBox, System.ComponentModel.ISupportInitialize).BeginInit()
            Me.SuspendLayout()
            '
            'tableLayoutPanel
            '
            resources.ApplyResources(Me.tableLayoutPanel, "tableLayoutPanel")
            Me.tableLayoutPanel.Controls.Add(Me.logoPictureBox, 0, 0)
            Me.tableLayoutPanel.Controls.Add(Me.labelProductName, 1, 0)
            Me.tableLayoutPanel.Controls.Add(Me.labelVersion, 1, 1)
            Me.tableLayoutPanel.Controls.Add(Me.labelCopyright, 1, 2)
            Me.tableLayoutPanel.Controls.Add(Me.labelCompanyName, 1, 3)
            Me.tableLayoutPanel.Controls.Add(Me.textBoxDescription, 1, 4)
            Me.tableLayoutPanel.Controls.Add(Me.okButton, 1, 5)
            Me.tableLayoutPanel.Name = "tableLayoutPanel"
            '
            'logoPictureBox
            '
            resources.ApplyResources(Me.logoPictureBox, "logoPictureBox")
            Me.logoPictureBox.Name = "logoPictureBox"
            Me.tableLayoutPanel.SetRowSpan(Me.logoPictureBox, 6)
            Me.logoPictureBox.TabStop = False
            '
            'labelProductName
            '
            resources.ApplyResources(Me.labelProductName, "labelProductName")
            Me.labelProductName.MaximumSize = New System.Drawing.Size(0, 17)
            Me.labelProductName.Name = "labelProductName"
            '
            'labelVersion
            '
            resources.ApplyResources(Me.labelVersion, "labelVersion")
            Me.labelVersion.MaximumSize = New System.Drawing.Size(0, 17)
            Me.labelVersion.Name = "labelVersion"
            '
            'labelCopyright
            '
            resources.ApplyResources(Me.labelCopyright, "labelCopyright")
            Me.labelCopyright.MaximumSize = New System.Drawing.Size(0, 17)
            Me.labelCopyright.Name = "labelCopyright"
            '
            'labelCompanyName
            '
            resources.ApplyResources(Me.labelCompanyName, "labelCompanyName")
            Me.labelCompanyName.MaximumSize = New System.Drawing.Size(0, 17)
            Me.labelCompanyName.Name = "labelCompanyName"
            '
            'textBoxDescription
            '
            resources.ApplyResources(Me.textBoxDescription, "textBoxDescription")
            Me.textBoxDescription.Name = "textBoxDescription"
            Me.textBoxDescription.ReadOnly = True
            Me.textBoxDescription.TabStop = False
            '
            'okButton
            '
            resources.ApplyResources(Me.okButton, "okButton")
            Me.okButton.DialogResult = System.Windows.Forms.DialogResult.Cancel
            Me.okButton.Name = "okButton"
            '
            'AboutNViewDlg
            '
            Me.AcceptButton = Me.okButton
            resources.ApplyResources(Me, "$this")
            Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
            Me.Controls.Add(Me.tableLayoutPanel)
            Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
            Me.MaximizeBox = False
            Me.MinimizeBox = False
            Me.Name = "AboutNViewDlg"
            Me.ShowIcon = False
            Me.ShowInTaskbar = False
            Me.tableLayoutPanel.ResumeLayout(False)
            Me.tableLayoutPanel.PerformLayout()
            CType(Me.logoPictureBox, System.ComponentModel.ISupportInitialize).EndInit()
            Me.ResumeLayout(False)

        End Sub

#End Region

        Private tableLayoutPanel As System.Windows.Forms.TableLayoutPanel
        Private logoPictureBox As System.Windows.Forms.PictureBox
        Private labelProductName As System.Windows.Forms.Label
        Private labelVersion As System.Windows.Forms.Label
        Private labelCopyright As System.Windows.Forms.Label
        Private labelCompanyName As System.Windows.Forms.Label
        Private textBoxDescription As System.Windows.Forms.TextBox
        Private okButton As System.Windows.Forms.Button
    End Class
End Namespace