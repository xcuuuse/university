using System;
using System.ComponentModel;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Collections.Generic;
using System.Text;

namespace MapInfo.MiPro.Samples.IM
{
	//====================================================================
	// Interface that includes the callback methods. 
	// Your application must provide a COM-visible class that implements 
	// these methods.  MapInfo Professional will call these methods
	// at appropriate times. 
	// Implemented in MapInfoCallback class (see below).
	//====================================================================
	public interface IMapInfoCallback
	{
		// Method called by MapInfo Professional when window changes
		int WindowContentsChanged(UInt32 windowID);

		// Method called by MapInfo Professional when the status bar text changes 
		int SetStatusText(string message);

		// Method called by MapInfo Professional when user chooses custom OLE menuitem 
		void MenuItemHandler(string commandInfo);
	}


	//====================================================================
	// Interface defining methods used to notify client of events.
	// Implement these methods in your Windows Forms application.  The
	// MapInfoCallback class calls these methods at appropriate times. 
	// 
	// Note that Control classes (such as Form) implement the 
	// ISynchronizeInvoke interface. 
	//====================================================================
	public interface ICallbackNotify : ISynchronizeInvoke
	{
		// Method called by MapInfoCallback class when user chooses custom OLE menuitem 
		void OnMenuItemClick(uint id);

		// Method called by MapInfoCallback class when the status bar text changes 
		void OnStatusBarTextChanged(string text);

		// Method called by MapInfoCallback class when window changes
		void OnWindowContentsChanged(uint windowId);
	}


	//====================================================================
	// Callback class.  Provides methods called by MapInfo Professional.
	//====================================================================
	[ClassInterface(ClassInterfaceType.None)]
	[ComVisible(true)]
	public class MapInfoCallBack : IMapInfoCallback
	{
		// Reference to object that gets notified when a callback occurs
		private ICallbackNotify _callbackClient;

		// Delegates used to call ICallbackNotify methods on the appropriate thread 
		public delegate void OnMenuItemClickDelegate(uint id);
		public OnMenuItemClickDelegate _onMenuItemClickDelegate;

		public delegate void OnStatusBarTextChangedDelegate(string text);
		public OnStatusBarTextChangedDelegate _onStatusBarTextChangedDelegate;

		public delegate void OnWindowContentsChangedDelegate(uint windowId);
		public OnWindowContentsChangedDelegate _onWindowContentsChangedDelegate;


		// Constructor that takes a ref to an object that implements ICallbackNotify
		public MapInfoCallBack(ICallbackNotify callbackClient)
		{
			// Save reference to callback client
			_callbackClient = callbackClient;

			// instantiate our delegates 
			_onMenuItemClickDelegate = new OnMenuItemClickDelegate(_callbackClient.OnMenuItemClick);
			_onStatusBarTextChangedDelegate = new OnStatusBarTextChangedDelegate(_callbackClient.OnStatusBarTextChanged);
			_onWindowContentsChangedDelegate = new OnWindowContentsChangedDelegate(_callbackClient.OnWindowContentsChanged);
		}

		// Callback method invoked when contents of a map window change
		public int WindowContentsChanged(uint windowId)
		{
			if (_callbackClient != null)
			{
				// Notify client.  Use the client app's InvokeRequired property to 
				// make sure the call is invoked on the appropriate thread.
				if (_callbackClient.InvokeRequired)
				{
					_callbackClient.Invoke(this._onWindowContentsChangedDelegate, new Object[] { windowId });
				}
				else
				{
					_callbackClient.OnWindowContentsChanged(windowId);
				}
			}
			// Return value does not matter
			return 0;
		}

		// Callback method invoked when the status bar text changes
		public int SetStatusText(string text)
		{
			if (_callbackClient != null)
			{
				// Notify client.  Use the client app's InvokeRequired property to 
				// make sure the call is invoked on the appropriate thread. 
				if (_callbackClient.InvokeRequired)
				{
					_callbackClient.Invoke(this._onStatusBarTextChangedDelegate, new Object[] { text });
				}
				else
				{
					_callbackClient.OnStatusBarTextChanged(text);
				}
			}
			// Return value does not matter
			return 0;
		}

		// Callback method invoked when a OLE menuitem has been clicked 
		public void MenuItemHandler(string commandInfo)
		{
			if (_callbackClient != null)
			{
				// Parse out the menuitem id
				string[] args = commandInfo.Split(',');
				if (args.Length >= 8)
				{
					uint id = uint.Parse(args[7]);

					// Notify client.  Use the client app's InvokeRequired property to 
					// make sure the call is invoked on the appropriate thread.
					if (_callbackClient.InvokeRequired)
					{
						_callbackClient.Invoke(this._onMenuItemClickDelegate, new Object[] { id });
					}
					else
					{
						_callbackClient.OnMenuItemClick(id);
					}
				}
			}
		}
	}
}
