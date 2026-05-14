Imports System
Imports System.Windows.Forms

Namespace MISamples
    Partial Public Class AddNViewDlg
        Inherits Form
        Public m_viewName As String = ""
        ' stores the name of the view 
        Public m_currentZoom As String = ""  ' stores the zoom value of the view 

        ''' <summary> 
        ''' Default constructor 
        ''' </summary> 
        Public Sub New()
            InitializeComponent()
        End Sub

#Region "[DIALOG EVENT HANDLERS]"

        ''' <summary> 
        ''' Dialog/Form load event handler 
        ''' </summary> 
        ''' <param name="sender"></param> 
        ''' <param name="e"></param> 
        Private Sub AddNViewDlg_Load(ByVal sender As Object, ByVal e As EventArgs) Handles MyBase.Load
            lblZoom.Text = lblZoom.Text + " " + m_currentZoom
        End Sub

        ''' <summary>
        ''' Handle this event to set the m_veiwName member variable when user clicks OK.
        ''' </summary>
        ''' <param name="sender"></param>
        ''' <param name="e"></param>
        ''' <remarks></remarks>
        Private Sub AddNViewDlg_FormClosed(ByVal sender As System.Object, ByVal e As System.Windows.Forms.FormClosedEventArgs) Handles MyBase.FormClosed
            If DialogResult = Windows.Forms.DialogResult.OK Then
                m_viewName = txtViewName.Text
            End If
        End Sub

#End Region

#Region "[CONTROL EVENT HANDLERS]"

        Private Sub txtViewName_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles txtViewName.TextChanged
            If Me.txtViewName.Text.Length > 0 Then
                Me.btnAdd.Enabled = True
            Else
                Me.btnAdd.Enabled = False
            End If
        End Sub

#End Region

    End Class
End Namespace