Imports System
Imports System.ComponentModel
Imports System.Windows.Forms
Imports System.Runtime.InteropServices
Imports System.Collections.Generic
Imports System.Text

'
' Integrated Mapping sample code
'
Namespace MapInfo.MiPro.Samples.IM

    '====================================================================
    ' Interface defining methods used to notify client of events.
    ' Implement these methods in your Windows Forms application.  The
    ' MapInfoCallback class calls these methods at appropriate times. 
    '
    ' Note that Control classes (such as Form) implement the 
    ' ISynchronizeInvoke interface.
    '====================================================================
    Public Interface ICallbackNotify
        Inherits ISynchronizeInvoke
        ' Method called by MapInfoCallback class when user chooses custom OLE menuitem 
        Sub OnMenuItemClick(ByVal id As UInteger)

        ' Method called by MapInfoCallback class when the status bar text changes 
        Sub OnStatusBarTextChanged(ByVal text As String)

        ' Method called by MapInfoCallback class when window changes
        Sub OnWindowContentsChanged(ByVal windowId As UInteger)
    End Interface

    '====================================================================
    ' Interface that includes the callback methods. 
    ' Your application must provide a COM-visible class that implements 
    ' these methods.  MapInfo Professional will call these methods
    ' at appropriate times. 
    ' Implemented in MapInfoCallback class (see below). 
    '====================================================================
    Public Interface IMapInfoCallback
        ' Method called by MapInfo Professional when window changes
        Function WindowContentsChanged(ByVal windowID As UInt32) As Integer

        ' Method called by MapInfo Professional when the status bar text changes 
        Function SetStatusText(ByVal message As String) As Integer

        ' Method called by MapInfo Professional when user chooses custom OLE menuitem 
        Sub MenuItemHandler(ByVal commandInfo As String)
    End Interface

    '====================================================================
    ' Callback class.  Provides methods called by MapInfo Professional.
    '====================================================================
    <ClassInterface(ClassInterfaceType.None)> _
    <ComVisible(True)> _
    Public Class MapInfoCallBack
        Implements IMapInfoCallback

        ' Reference to object that gets notified when a callback occurs
        Private _callbackClient As ICallbackNotify

        ' Delegates used to call ICallbackNotify methods on the appropriate thread 
        Public Delegate Sub OnMenuItemClickDelegate(ByVal id As UInteger)
        Public _onMenuItemClickDelegate As OnMenuItemClickDelegate

        Public Delegate Sub OnStatusBarTextChangedDelegate(ByVal text As String)
        Public _onStatusBarTextChangedDelegate As OnStatusBarTextChangedDelegate

        Public Delegate Sub OnWindowContentsChangedDelegate(ByVal windowId As UInteger)
        Public _onWindowContentsChangedDelegate As OnWindowContentsChangedDelegate


        ' Constructor that takes a ref to an object that implements ICallbackNotify
        Public Sub New(ByVal callbackClient As ICallbackNotify)
            ' Save reference to callback client
            _callbackClient = callbackClient

            ' instantiate our delegates 
            _onMenuItemClickDelegate = New OnMenuItemClickDelegate(AddressOf _callbackClient.OnMenuItemClick)

            _onStatusBarTextChangedDelegate = New OnStatusBarTextChangedDelegate(AddressOf _callbackClient.OnStatusBarTextChanged)

            _onWindowContentsChangedDelegate = New OnWindowContentsChangedDelegate(AddressOf _callbackClient.OnWindowContentsChanged)
        End Sub

        ' Callback method invoked when contents of a map window change
        Public Function WindowContentsChanged(ByVal windowId As UInteger) As Integer Implements IMapInfoCallback.WindowContentsChanged

            If _callbackClient IsNot Nothing Then
                ' Notify client.  Use the client app's InvokeRequired property to 
                ' make sure the call is invoked on the appropriate thread.
                If _callbackClient.InvokeRequired Then
                    ' We are on the wrong thread; call Invoke to correct. 
                    _callbackClient.Invoke(Me._onWindowContentsChangedDelegate, New Object() {windowId})
                Else
                    _callbackClient.OnWindowContentsChanged(windowId)
                End If
            End If
            ' Return value does not matter
            Return 0
        End Function

        ' Callback method invoked when the status bar text changes
        Public Function SetStatusText(ByVal text As String) As Integer Implements IMapInfoCallback.SetStatusText

            If _callbackClient IsNot Nothing Then
                ' Notify client.  Use the client app's InvokeRequired property to 
                ' make sure the call is invoked on the appropriate thread.
                If _callbackClient.InvokeRequired Then
                    ' We are on the wrong thread; call Invoke to correct. 
                    _callbackClient.Invoke(Me._onStatusBarTextChangedDelegate, New Object() {text})
                Else
                    _callbackClient.OnStatusBarTextChanged(text)
                End If
            End If
            ' Return value does not matter
            Return 0
        End Function

        ' Callback method invoked when a OLE menuitem has been clicked 
        Public Sub MenuItemHandler(ByVal commandInfo As String) Implements IMapInfoCallback.MenuItemHandler

            If _callbackClient IsNot Nothing Then
                ' Parse out the menuitem id
                Dim args As String() = commandInfo.Split(","c)
                If args.Length >= 8 Then
                    Dim id As UInteger = UInteger.Parse(args(7))
                    ' Notify client.  Use the client app's InvokeRequired property to 
                    ' make sure the call is invoked on the appropriate thread.
                    If _callbackClient.InvokeRequired Then
                        ' We are on the wrong thread; call Invoke to correct. 
                        _callbackClient.Invoke(Me._onMenuItemClickDelegate, New Object() {id})
                    Else
                        _callbackClient.OnMenuItemClick(id)
                    End If
                End If
            End If
        End Sub
    End Class
End Namespace
