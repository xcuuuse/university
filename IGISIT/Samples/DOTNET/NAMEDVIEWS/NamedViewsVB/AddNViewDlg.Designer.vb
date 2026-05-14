Namespace MISamples
    Partial Class AddNViewDlg
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
            Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(AddNViewDlg))
            Me.lblZoom = New System.Windows.Forms.Label
            Me.lblDescCurView = New System.Windows.Forms.Label
            Me.txtViewName = New System.Windows.Forms.TextBox
            Me.btnAdd = New System.Windows.Forms.Button
            Me.cmdCancel = New System.Windows.Forms.Button
            Me.SuspendLayout()
            '
            'lblZoom
            '
            resources.ApplyResources(Me.lblZoom, "lblZoom")
            Me.lblZoom.Name = "lblZoom"
            '
            'lblDescCurView
            '
            resources.ApplyResources(Me.lblDescCurView, "lblDescCurView")
            Me.lblDescCurView.Name = "lblDescCurView"
            '
            'txtViewName
            '
            resources.ApplyResources(Me.txtViewName, "txtViewName")
            Me.txtViewName.Name = "txtViewName"
            '
            'btnAdd
            '
            Me.btnAdd.DialogResult = System.Windows.Forms.DialogResult.OK
            resources.ApplyResources(Me.btnAdd, "btnAdd")
            Me.btnAdd.Name = "btnAdd"
            Me.btnAdd.UseVisualStyleBackColor = True
            '
            'cmdCancel
            '
            Me.cmdCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
            resources.ApplyResources(Me.cmdCancel, "cmdCancel")
            Me.cmdCancel.Name = "cmdCancel"
            Me.cmdCancel.UseVisualStyleBackColor = True
            '
            'AddNViewDlg
            '
            Me.AcceptButton = Me.btnAdd
            resources.ApplyResources(Me, "$this")
            Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
            Me.CancelButton = Me.cmdCancel
            Me.Controls.Add(Me.cmdCancel)
            Me.Controls.Add(Me.btnAdd)
            Me.Controls.Add(Me.txtViewName)
            Me.Controls.Add(Me.lblDescCurView)
            Me.Controls.Add(Me.lblZoom)
            Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
            Me.MaximizeBox = False
            Me.MinimizeBox = False
            Me.Name = "AddNViewDlg"
            Me.ShowInTaskbar = False
            Me.ResumeLayout(False)
            Me.PerformLayout()

        End Sub

#End Region

        Private lblZoom As System.Windows.Forms.Label
        Private lblDescCurView As System.Windows.Forms.Label
        Private WithEvents txtViewName As System.Windows.Forms.TextBox
        Private btnAdd As System.Windows.Forms.Button
        Private cmdCancel As System.Windows.Forms.Button
    End Class
End Namespace