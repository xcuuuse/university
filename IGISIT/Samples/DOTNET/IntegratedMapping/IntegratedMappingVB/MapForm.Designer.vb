<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class MapForm
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.MenuStrip1 = New System.Windows.Forms.MenuStrip
        Me.FileToolStripMenuItem = New System.Windows.Forms.ToolStripMenuItem
        Me.OpenToolStripMenuItem = New System.Windows.Forms.ToolStripMenuItem
        Me.ExitToolStripMenuItem = New System.Windows.Forms.ToolStripMenuItem
        Me.HelpToolStripMenuItem = New System.Windows.Forms.ToolStripMenuItem
        Me.AboutToolStripMenuItem = New System.Windows.Forms.ToolStripMenuItem
        Me.StatusStrip1 = New System.Windows.Forms.StatusStrip
        Me.ToolStripStatusLabel1 = New System.Windows.Forms.ToolStripStatusLabel
        Me.Label1 = New System.Windows.Forms.Label
        Me.ComboBoxMapTool = New System.Windows.Forms.ComboBox
        Me.ButtonZoomIn = New System.Windows.Forms.Button
        Me.ButtonZoomOut = New System.Windows.Forms.Button
        Me.MapPanel = New System.Windows.Forms.Panel
        Me.MenuStrip1.SuspendLayout()
        Me.StatusStrip1.SuspendLayout()
        Me.SuspendLayout()
        '
        'MenuStrip1
        '
        Me.MenuStrip1.Items.AddRange(New System.Windows.Forms.ToolStripItem() {Me.FileToolStripMenuItem, Me.HelpToolStripMenuItem})
        Me.MenuStrip1.Location = New System.Drawing.Point(0, 0)
        Me.MenuStrip1.Name = "MenuStrip1"
        Me.MenuStrip1.Size = New System.Drawing.Size(442, 24)
        Me.MenuStrip1.TabIndex = 0
        Me.MenuStrip1.Text = "MenuStrip1"
        '
        'FileToolStripMenuItem
        '
        Me.FileToolStripMenuItem.DropDownItems.AddRange(New System.Windows.Forms.ToolStripItem() {Me.OpenToolStripMenuItem, Me.ExitToolStripMenuItem})
        Me.FileToolStripMenuItem.Name = "FileToolStripMenuItem"
        Me.FileToolStripMenuItem.Size = New System.Drawing.Size(35, 20)
        Me.FileToolStripMenuItem.Text = "&File"
        '
        'OpenToolStripMenuItem
        '
        Me.OpenToolStripMenuItem.Name = "OpenToolStripMenuItem"
        Me.OpenToolStripMenuItem.Size = New System.Drawing.Size(152, 22)
        Me.OpenToolStripMenuItem.Text = "&Open..."
        '
        'ExitToolStripMenuItem
        '
        Me.ExitToolStripMenuItem.Name = "ExitToolStripMenuItem"
        Me.ExitToolStripMenuItem.Size = New System.Drawing.Size(152, 22)
        Me.ExitToolStripMenuItem.Text = "E&xit"
        '
        'HelpToolStripMenuItem
        '
        Me.HelpToolStripMenuItem.DropDownItems.AddRange(New System.Windows.Forms.ToolStripItem() {Me.AboutToolStripMenuItem})
        Me.HelpToolStripMenuItem.Name = "HelpToolStripMenuItem"
        Me.HelpToolStripMenuItem.Size = New System.Drawing.Size(40, 20)
        Me.HelpToolStripMenuItem.Text = "&Help"
        '
        'AboutToolStripMenuItem
        '
        Me.AboutToolStripMenuItem.Name = "AboutToolStripMenuItem"
        Me.AboutToolStripMenuItem.Size = New System.Drawing.Size(126, 22)
        Me.AboutToolStripMenuItem.Text = "About..."
        '
        'StatusStrip1
        '
        Me.StatusStrip1.Items.AddRange(New System.Windows.Forms.ToolStripItem() {Me.ToolStripStatusLabel1})
        Me.StatusStrip1.Location = New System.Drawing.Point(0, 376)
        Me.StatusStrip1.Name = "StatusStrip1"
        Me.StatusStrip1.Size = New System.Drawing.Size(442, 22)
        Me.StatusStrip1.TabIndex = 1
        Me.StatusStrip1.Text = "StatusStrip1"
        '
        'ToolStripStatusLabel1
        '
        Me.ToolStripStatusLabel1.Name = "ToolStripStatusLabel1"
        Me.ToolStripStatusLabel1.Size = New System.Drawing.Size(0, 17)
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(12, 38)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(88, 13)
        Me.Label1.TabIndex = 2
        Me.Label1.Text = "Active Map Tool:"
        '
        'ComboBoxMapTool
        '
        Me.ComboBoxMapTool.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        Me.ComboBoxMapTool.Enabled = False
        Me.ComboBoxMapTool.FormattingEnabled = True
        Me.ComboBoxMapTool.Location = New System.Drawing.Point(106, 35)
        Me.ComboBoxMapTool.Name = "ComboBoxMapTool"
        Me.ComboBoxMapTool.Size = New System.Drawing.Size(123, 21)
        Me.ComboBoxMapTool.TabIndex = 3
        '
        'ButtonZoomIn
        '
        Me.ButtonZoomIn.Enabled = False
        Me.ButtonZoomIn.Location = New System.Drawing.Point(250, 33)
        Me.ButtonZoomIn.Name = "ButtonZoomIn"
        Me.ButtonZoomIn.Size = New System.Drawing.Size(88, 23)
        Me.ButtonZoomIn.TabIndex = 4
        Me.ButtonZoomIn.Text = "Zoom In"
        Me.ButtonZoomIn.UseVisualStyleBackColor = True
        '
        'ButtonZoomOut
        '
        Me.ButtonZoomOut.Enabled = False
        Me.ButtonZoomOut.Location = New System.Drawing.Point(342, 33)
        Me.ButtonZoomOut.Name = "ButtonZoomOut"
        Me.ButtonZoomOut.Size = New System.Drawing.Size(88, 23)
        Me.ButtonZoomOut.TabIndex = 5
        Me.ButtonZoomOut.Text = "Zoom Out"
        Me.ButtonZoomOut.UseVisualStyleBackColor = True
        '
        'MapPanel
        '
        Me.MapPanel.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) _
                    Or System.Windows.Forms.AnchorStyles.Left) _
                    Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.MapPanel.BackColor = System.Drawing.SystemColors.Window
        Me.MapPanel.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.MapPanel.Location = New System.Drawing.Point(12, 62)
        Me.MapPanel.Name = "MapPanel"
        Me.MapPanel.Size = New System.Drawing.Size(418, 311)
        Me.MapPanel.TabIndex = 6
        '
        'MapForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(442, 398)
        Me.Controls.Add(Me.MapPanel)
        Me.Controls.Add(Me.ButtonZoomOut)
        Me.Controls.Add(Me.ButtonZoomIn)
        Me.Controls.Add(Me.ComboBoxMapTool)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.StatusStrip1)
        Me.Controls.Add(Me.MenuStrip1)
        Me.MainMenuStrip = Me.MenuStrip1
        Me.MinimumSize = New System.Drawing.Size(450, 400)
        Me.Name = "MapForm"
        Me.Text = "Map Viewer"
        Me.MenuStrip1.ResumeLayout(False)
        Me.MenuStrip1.PerformLayout()
        Me.StatusStrip1.ResumeLayout(False)
        Me.StatusStrip1.PerformLayout()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents MenuStrip1 As System.Windows.Forms.MenuStrip
    Friend WithEvents FileToolStripMenuItem As System.Windows.Forms.ToolStripMenuItem
    Friend WithEvents OpenToolStripMenuItem As System.Windows.Forms.ToolStripMenuItem
    Friend WithEvents HelpToolStripMenuItem As System.Windows.Forms.ToolStripMenuItem
    Friend WithEvents AboutToolStripMenuItem As System.Windows.Forms.ToolStripMenuItem
    Friend WithEvents StatusStrip1 As System.Windows.Forms.StatusStrip
    Friend WithEvents ExitToolStripMenuItem As System.Windows.Forms.ToolStripMenuItem
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents ComboBoxMapTool As System.Windows.Forms.ComboBox
    Friend WithEvents ButtonZoomIn As System.Windows.Forms.Button
    Friend WithEvents ButtonZoomOut As System.Windows.Forms.Button
    Friend WithEvents MapPanel As System.Windows.Forms.Panel
    Friend WithEvents ToolStripStatusLabel1 As System.Windows.Forms.ToolStripStatusLabel

End Class
