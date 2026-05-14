Imports System
Imports System.Windows.Forms
Imports System.Reflection
Imports System.Text

Namespace MISamples
    Partial Class AboutNViewDlg
        Inherits Form
        Public Sub New()
            InitializeComponent()

            ' Initialize the AboutBox to display the product information from the assembly information. 
            ' Change assembly information settings for your application through either: 
            ' - Project->My->Application->Assembly Information 
            ' - AssemblyInfo.cs 
            Me.Text = [String].Format(My.Resources.STR_ABOUT, AssemblyTitle)
            Me.labelProductName.Text = AssemblyProduct
            Me.labelVersion.Text = [String].Format(My.Resources.STR_VERSION, AssemblyVersion)
            Me.labelCopyright.Text = AssemblyCopyright
            Me.labelCompanyName.Text = AssemblyCompany

            Dim sb As New StringBuilder
            Call sb.Append(My.Resources.STR_ABT_DESC1)
            Call sb.Append(Environment.NewLine)
            Call sb.Append(Environment.NewLine)
            Call sb.Append(My.Resources.STR_ABT_DESC2)
            Me.textBoxDescription.Text = sb.ToString()

        End Sub

#Region "Assembly Attribute Accessors"

        Public ReadOnly Property AssemblyTitle() As String
            Get
                ' Get all Title attributes on this assembly 
                Dim attributes As Object() = Assembly.GetExecutingAssembly().GetCustomAttributes(GetType(AssemblyTitleAttribute), False)
                ' If there is at least one Title attribute 
                If attributes.Length > 0 Then
                    ' Select the first one 
                    Dim titleAttribute As AssemblyTitleAttribute = DirectCast(attributes(0), AssemblyTitleAttribute)
                    ' If it is not an empty string, return it 
                    If titleAttribute.Title <> "" Then
                        Return titleAttribute.Title
                    End If
                End If
                ' If there was no Title attribute, or if the Title attribute was the empty string, return the .exe name 
                Return System.IO.Path.GetFileNameWithoutExtension(Assembly.GetExecutingAssembly().CodeBase)
            End Get
        End Property

        Public ReadOnly Property AssemblyVersion() As String
            Get
                Return Assembly.GetExecutingAssembly().GetName().Version.ToString()
            End Get
        End Property

        Public ReadOnly Property AssemblyDescription() As String
            Get
                ' Get all Description attributes on this assembly 
                Dim attributes As Object() = Assembly.GetExecutingAssembly().GetCustomAttributes(GetType(AssemblyDescriptionAttribute), False)
                ' If there aren't any Description attributes, return an empty string 
                If attributes.Length = 0 Then
                    Return ""
                End If
                ' If there is a Description attribute, return its value 
                Return DirectCast(attributes(0), AssemblyDescriptionAttribute).Description
            End Get
        End Property

        Public ReadOnly Property AssemblyProduct() As String
            Get
                ' Get all Product attributes on this assembly 
                Dim attributes As Object() = Assembly.GetExecutingAssembly().GetCustomAttributes(GetType(AssemblyProductAttribute), False)
                ' If there aren't any Product attributes, return an empty string 
                If attributes.Length = 0 Then
                    Return ""
                End If
                ' If there is a Product attribute, return its value 
                Return DirectCast(attributes(0), AssemblyProductAttribute).Product
            End Get
        End Property

        Public ReadOnly Property AssemblyCopyright() As String
            Get
                ' Get all Copyright attributes on this assembly 
                Dim attributes As Object() = Assembly.GetExecutingAssembly().GetCustomAttributes(GetType(AssemblyCopyrightAttribute), False)
                ' If there aren't any Copyright attributes, return an empty string 
                If attributes.Length = 0 Then
                    Return ""
                End If
                ' If there is a Copyright attribute, return its value 
                Return DirectCast(attributes(0), AssemblyCopyrightAttribute).Copyright
            End Get
        End Property

        Public ReadOnly Property AssemblyCompany() As String
            Get
                ' Get all Company attributes on this assembly 
                Dim attributes As Object() = Assembly.GetExecutingAssembly().GetCustomAttributes(GetType(AssemblyCompanyAttribute), False)
                ' If there aren't any Company attributes, return an empty string 
                If attributes.Length = 0 Then
                    Return ""
                End If
                ' If there is a Company attribute, return its value 
                Return DirectCast(attributes(0), AssemblyCompanyAttribute).Company
            End Get
        End Property
#End Region

    End Class
End Namespace