Imports System
Imports System.Text
Imports System.Xml
Imports System.IO
Imports System.Globalization



Namespace MapInfo
    Public Class WriteUTF
        Public Const ERROR_SUCCESS As Integer = 0

        ' Return ERROR_SUCCESS if no exception is thrown 
        ' 
        Public Shared Function WriteUTF8(ByVal fnIn As String, ByVal fnOut As String) As Integer
            Dim rval As Integer = -1
            Try
                Dim doc As New XmlDocument
                
                Dim xml As New SanitizeXml(fnIn, WriteUTF.GetEncoding(fnIn))
                
                doc.Load(xml)
                
                xml.Close()
                
                Dim writer As New XmlTextWriter(fnOut, Encoding.UTF8)
                doc.Save(writer)
                writer.Close()
                rval = ERROR_SUCCESS
            Catch ex As Exception
                rval = -1
                ' throw ex; 
                m_errMsg = ex.Message
            End Try
            Return rval
        End Function


        Public Shared Sub ConvertDecimalToString(ByVal dValue As Double, ByRef sValue As String)
            sValue = dValue.ToString(CultureInfo.InvariantCulture)
        End Sub


        Public Shared Function GetErrorMessage(ByRef str As String) As Integer
            str = m_errMsg
            Return m_errMsg.Length
        End Function

        Shared m_errMsg As String


        Private Shared Function GetEncoding(ByVal fnIn As String) As Encoding
            Dim textReader As New XmlTextReader(fnIn)
            textReader.MoveToContent()
            Dim encoding As Encoding = textReader.Encoding
            textReader.Close()
            Return encoding
        End Function

    End Class

    Public Class SanitizeXml
        Inherits StreamReader


        Private Const EOF As Integer = -1

        Public Sub New(ByVal path As String)
            MyBase.New(path, True)
        End Sub
        Public Sub New(ByVal path As String, ByVal encoding As Encoding)
            MyBase.New(path, encoding)
        End Sub


        '--------------------------------------------------------------------------------
        ' As per xml specs (http://www.w3.org/TR/REC-xml/#dt-character)the range of
        ' characters falling within (0x00-0x08),(0x0B-0x0C) and (0x0E-0x1F) are the
        ' invalid characters. 
        '--------------------------------------------------------------------------------/

        Public Shared Function IsLegalXmlChar(ByVal iChar As Integer) As Boolean
            Return (((((iChar = 9) OrElse (iChar = 10)) OrElse (iChar = 13)) OrElse (((iChar >= &H20) AndAlso (iChar <= &HD7FF)) OrElse ((iChar >= &HE000) AndAlso (iChar <= &HFFFD)))) OrElse ((iChar >= &H10000) AndAlso (iChar <= &H10FFFF)))
        End Function


        ''--------------------------------------------------------------------------------
        ' Function to redirect the TextReader's call to SanitizeXML's Read() function.
        ' The following overridden method is the exact copy of Read(char[] buffer, int index, int count)
        ' in System.IO.TextReader, extracted by disassembling the mscorlib.lib in .net Refelctor.
        '--------------------------------------------------------------------------------*/
         Public Overrides Function Read(ByVal buffer As Char(), ByVal index As Integer, ByVal count As Integer) As Integer
            If (buffer Is Nothing) Then
                Throw New ArgumentNullException("buffer")
            End If
            If (index < 0) Then
                Throw New ArgumentOutOfRangeException("index")
            End If
            If (count < 0) Then
                Throw New ArgumentOutOfRangeException("count")
            End If
            If ((buffer.Length - index) < count) Then
                Throw New ArgumentException
            End If
            Dim num As Integer = 0
            Do
                Dim num2 As Integer = Me.Read
                If (num2 = -1) Then
                    Return num
                End If
                buffer(index + num) = Convert.ToChar(num2)
                num = num + 1
            Loop While (num < count)
            Return num
        End Function



        '--------------------------------------------------------------------------------------
        'Overridden function to add sanitizing functionality to StreamReader's Read() function.
        '--------------------------------------------------------------------------------------
        Public Overrides Function Read() As Integer
            Dim iNext As Integer = MyBase.Read
            Select Case iNext
                Case -1
                    Return -1
            End Select
            Return IIf(SanitizeXml.IsLegalXmlChar(iNext), iNext, &H20)
        End Function



    End Class


End Namespace
