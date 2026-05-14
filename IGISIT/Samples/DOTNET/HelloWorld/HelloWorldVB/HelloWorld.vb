Namespace MapInfo.MiPro.Samples

    ''' <summary>
    ''' Sample code demonstrating how to call .Net from MapBasic 
    ''' </summary>
    Public Class HelloWorld

        Public Shared Sub SayHello(ByVal s As String)
            ' Display a greeting in a standard .Net dialog box 
            System.Windows.Forms.MessageBox.Show("Hello, " + s)
        End Sub

    End Class

End Namespace

