using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;
using System.IO;
using MapInfo;

namespace MapInfo.MiPro.Samples.IM
{

	//
	// A demonstration of how to do Integrated Mapping (the reparenting of a
	// MapInfo Professional map window into other applications) using .Net.
	// 
	public partial class MapForm : Form, ICallbackNotify
	{
		// Id of the map window being reparented
		private string _mapWindowId = "";

		// HWND of the window being reparented
		private System.IntPtr _hWnd;

		// Mapping of map tool names to tool command ids
		private Dictionary<string, int> _toolIdMap;

		// ID of the custom OLE menu item on the map window's context menu
		private const uint _customItemId = 10000;

		// Reference to the callback object
		private MapInfoCallBack _callbackObject;


		// Store a reference to MapInfo Professional's COM interface
		private MapInfoApplication _mapInfoApp;
		private MapInfoApplication MapInfoApp
		{
			get { return _mapInfoApp; }
		}

		// A File Open dialog that the user can use to open one or more .TAB files
		private OpenFileDialog _openFileDlg;
		private OpenFileDialog OpenDlg
		{
			get
			{
				if (_openFileDlg == null)
				{
					_openFileDlg = new OpenFileDialog();
					_openFileDlg.Filter = "MapInfo Tables (*.tab)|*.tab";
					_openFileDlg.Multiselect = true;
					_openFileDlg.RestoreDirectory = false;
					_openFileDlg.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);

				}
				return _openFileDlg;
			}
		}

		// Constructor
		public MapForm()
		{
			InitializeComponent();

			InitializeMapToolCombobox();
		}


		// Given a list of .TAB filenames, open the tables and display them in a map
		private void NewMap(string[] tableList)
		{
			string aliasList = "";

			// Open each TAB file
			foreach (string tablepath in tableList)
			{
				// Create alias string for the table
				string alias = Path.GetFileNameWithoutExtension(tablepath);
				alias = alias.Replace(" ", "_");

				// Open the table
				MapInfoApp.Do("Open table \"" + tablepath + "\" as " + alias);

				// Add new table's alias to the list
				if (aliasList == "")
				{
					aliasList += alias;
				}
				else
				{
					aliasList += ", " + alias;
				}
			}

			// Create map window, reparenting it to our map panel
			MapInfoApp.Do("Set Next Document Parent " + this.mapPanel.Handle + " Style 1");
			MapInfoApp.Do("Map From " + aliasList);

			// Save the ID of the newly created window
			_mapWindowId = MapInfoApp.Eval("WindowID(0)");

			// Call WindowInfo with 12 (WIN_INFO_WND) to get the Windows HWND.
			// If the user resizes the form, we need the HWND to update the map size.
			_hWnd = (System.IntPtr)long.Parse(_mapInfoApp.Eval("WindowInfo(FrontWindow(),12)"));

			// Now that there is a map, enable the Zoom In and Zoom Out buttons
			this.buttonZoomIn.Enabled = true;
			this.buttonZoomOut.Enabled = true;
		}


		private void CloseWindow(string windowId)
		{
			// Close the window
			MapInfoApp.Do("Close window " + windowId);
		}


		private void CloseAllTables()
		{
			MapInfoApp.Do("Close All");
		}


		private void Form1_Load(object sender, EventArgs e)
		{
			InitializeComObject();

			AddMapperShortcutMenuitem();
		}


		private void Form1_FormClosed(object sender, FormClosedEventArgs e)
		{
			// Unregister the callback object
			MapInfoApp.UnregisterCallback(_callbackObject);
		}


		private void Form1_ResizeEnd(object sender, EventArgs e)
		{
			// The form has been resized. 
			if (_mapWindowId != "")
			{
				// Update the map to match the current size of the panel. 
				MoveWindow(_hWnd, 0, 0, this.mapPanel.Width, this.mapPanel.Height, false);
			}
		}

		[DllImport("user32.dll")]
		static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);


		private void InitializeComObject()
		{
			// Create the MapInfo Professional object
			_mapInfoApp = new MapInfoApplication();

			// Set parent window for MapInfo Professional dialogs
			_mapInfoApp.Do("Set Application Window " + this.Handle);

			// Create the callback object
			_callbackObject = new MapInfoCallBack(this);

			// Register the callback object with Professional
			_mapInfoApp.RegisterCallback(_callbackObject);
		}


		// Set up the combo box that lets the user choose a map tool 
		private void InitializeMapToolCombobox()
		{
			// Create the dictionary collection
			_toolIdMap = new Dictionary<string, int>();

			// Add "Select" tool to combobox and dictionary
			this.comboBoxMapTool.Items.Add(Properties.Resources.MapTool_Select);
			_toolIdMap.Add(Properties.Resources.MapTool_Select, 1701);

			// Add "Pan" tool to combobox and dictionary
			this.comboBoxMapTool.Items.Add(Properties.Resources.MapTool_Pan);
			_toolIdMap.Add(Properties.Resources.MapTool_Pan, 1702);

			// Add "Zoom In" tool to combobox and dictionary
			this.comboBoxMapTool.Items.Add(Properties.Resources.MapTool_ZoomIn);
			_toolIdMap.Add(Properties.Resources.MapTool_ZoomIn, 1705);

			// Add "Zoom Out" tool to combobox and dictionary
			this.comboBoxMapTool.Items.Add(Properties.Resources.MapTool_ZoomOut);
			_toolIdMap.Add(Properties.Resources.MapTool_ZoomOut, 1706);

			// Set the combobox item to Select
			comboBoxMapTool.SelectedIndex = 0;
		}


		// Add a custom item to the Map window's context menu 
		private void AddMapperShortcutMenuitem()
		{
			// Issue Alter Menu command, adding an OLE menuitem. 
			// When the user chooses a custom OLE menuitem from the context menu,
			// MapInfo Professional calls MapInfoCallback.MenuItemHandler,
			// which in turn calls the OnMenuItemClick item below. 
			string cmd = string.Format(@"Alter Menu ""MapperShortcut"" Add ""Custom Item"" ID {0} calling OLE ""MenuItemHandler""", _customItemId);
			_mapInfoApp.Do(cmd);
		}


		// Display the File Open dialog to let the user choose table(s) to open.
		private void openToolStripMenuItem_Click(object sender, EventArgs e)
		{
			// Prompt the user to open one or more TAB files
			if (OpenDlg.ShowDialog(this) == DialogResult.OK)
			{
				// Close window and tables, if they exist
				if (_mapWindowId != "")
				{
					CloseWindow(_mapWindowId);
					CloseAllTables();
					_mapWindowId = "";
				}
				// Create a new map
				NewMap(OpenDlg.FileNames);
				// Enable the tool picker 
				comboBoxMapTool.Enabled = true;
			}
		}


		private void exitToolStripMenuItem_Click(object sender, EventArgs e)
		{
			// Close form to end the application
			this.Close();
		}


		private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
		{
			this.ShowMessage("Demonstration of integrated mapping, using Windows Forms.");
		}


		// Handle the selection of a different tool from the combo box. 
		private void comboBoxMapTool_SelectionChangeCommitted(object sender, EventArgs e)
		{
			// Get the current combobox selection
			string selectedText = comboBoxMapTool.SelectedItem.ToString();
			// Get the command id
			int commandId = _toolIdMap[selectedText];
			// Issue command to change the map tool
			_mapInfoApp.Do("Run Menu Command " + commandId);
		}


		public void ShowMessage(string msg)
		{
			MessageBox.Show(this, msg);
		}


		#region ICallbackNotify Members


		// The method called when the user chooses the custom OLE menuitem.  
		public void OnMenuItemClick(uint id)
		{
			if (id == _customItemId)
			{
				MessageBox.Show(this, "Custom menu item was clicked.");
			}
		}


		// The method called when the MapInfo Professional status bar text changes. 
		// This can happen due to changes in the map view (zoom level) or selection, 
		// or can happen because the user highlights an item on the map's context menu.
		public void OnStatusBarTextChanged(string text)
		{
			bool b = statusStrip1.InvokeRequired;

			// Replace any occurrences of "\t" (which can be included when the status bar
			// is displaying map zoom etc.) with spaces.  
			toolStripStatusLabel1.Text = text.Replace("\t", "        ");
		}


		// The method called when the map window changes, e.g. layers added.  
		public void OnWindowContentsChanged(uint windowId)
		{
			// TODO:  If your application needs to respond to changes in the map 
			// contents, add appropriate code here.   
		}

		#endregion

		private void buttonZoomIn_Click(object sender, EventArgs e)
		{
			zoomMap(0.5);   // zoom in (show an area half as wide)
		}


		private void buttonZoomOut_Click(object sender, EventArgs e)
		{
			zoomMap(2.0);  // zoom out (show an area twice as wide)
		}


		private void zoomMap(double zoomFactor)
		{
			if (_mapWindowId != "")
			{
				// Call:  MapperInfo(id, MAPPER_INFO_DISTUNITS) 
				// to get a units string such as "mi" or "km"
				string strUnit = MapInfoApp.Eval("MapperInfo( " + _mapWindowId + " , 12)");

				// Call:  MapperInfo(id, MAPPER_INFO_ZOOM) 
				double dZoom = Double.Parse(MapInfoApp.Eval("MapperInfo( " + _mapWindowId + " , 1)"));

				dZoom *= zoomFactor;
				dZoom = Math.Min(dZoom, 10000000);
				dZoom = Math.Max(dZoom, 0.0001);
				// Apply the new zoom level with a statement of this form: 
				//     Set Map Window 123456 Zoom 123.456  Units "mi"  
				string cmd = string.Format(@"Set Map Window {0} Zoom {1} Units ""{2}""", _mapWindowId, dZoom, strUnit);
				MapInfoApp.Do(cmd);
			}

		}


	}
}