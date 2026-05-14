using System;
using System.Windows.Forms;
using System.Threading;
using System.Xml;
using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;

namespace MISamples
{
	public partial class NViewDlg : UserControl
	{
		// some string in xml file
		private const string STR_NAME = "Name";
		private const string STR_ROOT = "root";
		private const string STR_DIALOG = "Dialog";
		private const string STR_NAMEDVIEWS = "NamedViews";
		private const string STR_VIEWS = "Views";
		private const string STR_PATH_DIALOG = "/NamedViews/Dialog";
		private const string STR_PATH_ROOT_FOLDER = "/NamedViews/Views";
		private const string STR_LEFT = "Left";
		private const string STR_TOP = "Top";
		private const string STR_WIDTH = "Width";
		private const string STR_HEIGHT = "Height";


		
		/* The controller class which uses this dialog class ensures
		 * a single instance of this dialog class. However different
		 * running instance of MapInfo Professional will have their
		 * own copy of dll. To make sure that read/write from/to xml
		 * file which is going to be a single file on the disk, is
		 * smooth and we have the synchronized access to the xml file,
		 * the Mutexes will be used.
		 */
		private Mutex mut = null;
		private const string mutexName = "MISamples.NamedView"; // Name of the mutex
		private string sXMLFile = Environment.GetFolderPath(
			Environment.SpecialFolder.ApplicationData) + "\\MapInfo\\MapInfo\\nviews.xml";
		private bool bTreeChanged = false;						// a flag indicating that tree contents have been changed
																// since last write to xml file

		private TreeNode dragPrevNode = null;					// previous drag over node
		//private TreeNode dragSelNode = null;					// current drag over node

		private int dialogLeft, dialogTop, dialogWidth, dialogHeight;

		private bool firstLoad = true;
		private Controller _controller;

		/// <summary>
		/// Construction
		/// </summary>
		public NViewDlg()
		{
			InitializeComponent();
			mut = new Mutex(false, mutexName);
		}
		/// <summary>
		/// Parameterised Construction
		/// <param name="controller"></param>
		/// </summary>
		public NViewDlg(Controller controller):this()
		{
			_controller = controller;
		}
		#region [DIALOG EVENT HANDLERS]
		/// <summary>
		/// Named View dialog Load event handler
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void NViewDlg_Load(object sender, EventArgs e)
		{
			if (firstLoad)
			{
				firstLoad = false;

				LoadTreeFromFile(sXMLFile);
				UpdateButtons();

				if (dialogWidth >= this.MinimumSize.Width && dialogWidth <= Screen.PrimaryScreen.WorkingArea.Width)
					this.Width = dialogWidth;
				if (dialogHeight >= this.MinimumSize.Height && dialogHeight <= Screen.PrimaryScreen.WorkingArea.Height)
					this.Height = dialogHeight;
				if (dialogLeft > -this.Width && dialogLeft < Screen.PrimaryScreen.WorkingArea.Width)
					this.Left = dialogLeft;
				if (dialogTop > -this.Top && dialogTop < Screen.PrimaryScreen.WorkingArea.Height)
					this.Top = dialogTop;
			}
		}


		// This call to the WIN32 API function SetFocus is used in NViewDlg_FormClosing below
		[DllImport("user32.dll")]
		private static extern IntPtr SetFocus(IntPtr hWnd);
		
		

		#endregion


		#region [TREEVIEW EVENT HANDLERS]
		
		/// <summary>
		/// Begins drag operation
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_ItemDrag(object sender, ItemDragEventArgs e)
		{
			tvwNamedViews.SelectedNode = (TreeNode)e.Item;
			DoDragDrop(e.Item, DragDropEffects.Move);
		}

		/// <summary>
		/// Displays the drop target during a drag operation
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_DragOver(object sender, DragEventArgs e)
		{
			// Change any previous node back 
			if (dragPrevNode != null)
			{
				dragPrevNode.BackColor = Color.Empty;
				dragPrevNode.ForeColor = Color.Empty;
			}

			// Get the node from the mouse position, colour it
			Point pt = ((TreeView)sender).PointToClient(new Point(e.X, e.Y));
			TreeNode tNode = ((TreeView)sender).GetNodeAt(pt);
			tNode.BackColor = SystemColors.Highlight;
			tNode.ForeColor = SystemColors.HighlightText;

			dragPrevNode = tNode;

		}

		private void tvwNamedViews_DragLeave(object sender, EventArgs e)
		{
			// Change any previous node back 
			if (dragPrevNode != null)
			{
				dragPrevNode.BackColor = SystemColors.Highlight;
				dragPrevNode.ForeColor = SystemColors.HighlightText;
			}

		}

		/// <summary>
		/// Continues the drag operation
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_DragEnter(object sender, DragEventArgs e)
		{
			e.Effect = DragDropEffects.Move;

			dragPrevNode = null;
			//dragSelNode = null;
		}

		/// <summary>
		/// This event is generated when user drops a node
		/// on another node. This handler completes the drag
		/// & drop operation.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_DragDrop(object sender, DragEventArgs e)
		{
			// Change any previous node back 
			if (dragPrevNode != null)
			{
				dragPrevNode.BackColor = Color.Empty;
				dragPrevNode.ForeColor = Color.Empty;
				dragPrevNode = null;
			}

			TreeNode dragNode;

			if (e.Data.GetDataPresent("System.Windows.Forms.TreeNode", false)) {

				int dropIndex = -1;
				TreeNode newNode = null; 
				
				// Get the node where the item has been dropped
				Point pt = ((TreeView)sender).PointToClient(new Point(e.X, e.Y));
				TreeNode dropNode = ((TreeView)sender).GetNodeAt(pt);

				// Get the node that is being dragged
				dragNode = (TreeNode)e.Data.GetData("System.Windows.Forms.TreeNode");
				if (!TreeNodeUtil.IsViewNode(dragNode)){
					dragNode.Collapse();
					dragNode.ImageIndex = 1;
				}

				if (dropNode != null) {
					// If a node has been dropped on a view node use its parent as drop target
					if (TreeNodeUtil.IsViewNode(dropNode))
					{
						// Dropped a node onto a View node.  Move the node-being-dropped 
						// into the spot occupied by the drop target node. 
						if (dropNode.Parent != null)
						{
							// User dropped onto a node that is inside a folder. 
							// Get the index number of the target node, 
							// indicating the position within the folder. 
							dropIndex = dropNode.Parent.Nodes.IndexOf(dropNode);
						}
						else
						{
							// The view node that we are dropping onto does not have a 
							// parent node, so it must be at the root level of the tree.
							dropIndex = tvwNamedViews.Nodes.IndexOf(dropNode);
						}
						dropNode = dropNode.Parent;
					}
					else
					{
						// Dropped a node onto a Folder node.  Move the node-being-dropped 
						// into the top of the folder.  
						dropIndex = 0; 
					}
				}

				// If the drop node is null add dragged node as the top level node
				if (dropNode == null) {
					newNode = (TreeNode)dragNode.Clone();
					if (dropIndex >= 0)
					{
						tvwNamedViews.Nodes.Insert(dropIndex, newNode);
					}
					else
					{
						tvwNamedViews.Nodes.Add(newNode);
					}
					bTreeChanged = true;
				}

				// else check if drag and drop nodes are different
				else if (!dropNode.Equals(dragNode)) {
					// Do not allow a node to be dropped on a child/grand child
					if (TreeNodeUtil.ContainsNode(dragNode, dropNode)) {
						MessageBox.Show(Properties.Resources.ERR_INVALID_DROP,
								Properties.Resources.ERR_INVALID_DROP_MSG_TITLE,
									MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
						return;
					}

					newNode = (TreeNode)dragNode.Clone();
					if (dropIndex >= 0)
					{ 
						dropNode.Nodes.Insert(dropIndex, newNode);
					}
					else
					{
						dropNode.Nodes.Add(newNode);
					}
					 
					dropNode.Expand();
					dropNode.ImageIndex = 0;
					dropNode.SelectedImageIndex = 0;
					bTreeChanged = true;

				} else {
					return;
				}

				//Remove the dragged node
				TreeNode dragNodeParent = dragNode.Parent;
				dragNode.Remove();
				if (dragNodeParent != null)
				{
					if (dragNodeParent.Nodes.Count == 0)
					{
						dragNodeParent.Collapse();
						dragNodeParent.ImageIndex = 1;
						dragNodeParent.SelectedImageIndex = 1;
					}
					
				}

				// Make sure the node that the user dragged is the selected node.
				tvwNamedViews.SelectedNode = newNode; 

			}
		}

		/// <summary>
		/// Handles renaming of a tree node
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_AfterLabelEdit(object sender, NodeLabelEditEventArgs e)
		{
			if (e.Label == null && e.Node.Text.Length == 0) {
				e.Node.Remove();
				return;
			}

			if (e.Label != null) {
				if (e.Label.Length > 0) {
					if (e.Label.IndexOfAny(new char[] { '@', '.', ',', '!' }) == -1) {
						// Stop editing without canceling the label change.
						e.Node.Text = e.Label;
						e.Node.Name = e.Label;
						e.Node.EndEdit(false);
						bTreeChanged = true;
					} else {
						/* Cancel the label edit action, inform the user, and 
						   place the node in edit mode again. */
						e.CancelEdit = true;
						e.Node.BeginEdit();
					}
				} else {
					if (e.Node.Text.Length == 0)
						e.Node.Remove();
					else
						e.CancelEdit = true;
				}
			} else {
				e.CancelEdit = true;
			}
		}

		/// <summary>
		/// Enables/Disables the Goto button
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_AfterSelect(object sender, TreeViewEventArgs e)
		{
			UpdateButtons();
		}

		/// <summary>
		/// Set the image of tree node
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_BeforeExpand(object sender, TreeViewCancelEventArgs e)
		{
			TreeNode tNode = e.Node;
			if (!TreeNodeUtil.IsViewNode(tNode))
			{
				tNode.ImageIndex = 0;
				tNode.SelectedImageIndex = 0;
			}
		}

		/// <summary>
		/// Set the image of tree node.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_BeforeCollapse(object sender, TreeViewCancelEventArgs e)
		{
			TreeNode tNode = e.Node;
			if (!TreeNodeUtil.IsViewNode(tNode))
			{
				tNode.ImageIndex = 1;
				tNode.SelectedImageIndex = 1;
			}
		}

		/// <summary>
		/// Same as Goto button handler. 
		/// It sets the current view based on selected node.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void tvwNamedViews_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
		{
			TreeNode tNode = e.Node;
			if (TreeNodeUtil.IsViewNode(tNode))
			{
				// get window id
				int windowId = InteropHelper.GetMapWindowId();
				if (windowId == 0)
				{
					return;
				}

				TreeNodeUtil.t_NodeInfo tNodeInfo = (TreeNodeUtil.t_NodeInfo)tNode.Tag;
				InteropHelper.SetView(windowId, tNodeInfo.m_x, tNodeInfo.m_y, tNodeInfo.m_zoom, tNodeInfo.m_unit, tNodeInfo.m_csys);
			}
		}

		#endregion


		#region [BUTTON HANDLERS]
		/// <summary>
		/// Add View handler. Gets the view information
		/// from running instance of MapInfo Professional App
		/// and prompts a user for the name of view.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void btnAdd_Click(object sender, EventArgs e)
		{
			// get window id
			int windowId = InteropHelper.GetMapWindowId();
			if (windowId == 0)
			{
				return;
			}

			// Get current view information from Mapper Window
			string zoomValue, centerX, centerY;
			string mapCSys, oldSessionCSys;
			string mapUnit, oldSessionDistanceUnit; 

			// Before we do any work involving the map's X/Y coordinates, we
			// will set the current coordinate system; setting the coordsys 
			// sets the units that will apply to the x/y coordinates. 
			// Before we set the coorindate system, make note of the current 
			// coordinate system, so that we can restore it later.  This way, in
			// the unlikely event that the user typed a Set CoordSys statement into 
			// the MapBasic window, we will preserve the coordsys typed in by the user. 

			// Set the session coordinate system to match the coordsys of the map window 
			oldSessionCSys = InteropHelper.GetSessionCoordSys();  // Get session coordsys string 
			mapCSys = InteropHelper.GetMapperCoordSys(windowId);  // Get the map window's coordsys string
			InteropHelper.SetSessionCoordSys(mapCSys);

			centerX = InteropHelper.GetMapperCenterX(windowId);   // Get CenterX 
			centerY = InteropHelper.GetMapperCenterY(windowId);   // Get CenterY 

			InteropHelper.SetSessionCoordSys(oldSessionCSys);     // restore original coordsys 

			// Before we do any work involving distances (such as the zoom distance),
			// we will want to set the session distance unit; we will set it to match 
			// the distance unit in use by the map window. That way, we can record a 
			// zoom distance in units that are unique to each map, e.g. 
			// 5 "mi" 
			// 1200 "m" 
			// etc. 
			// Before we set the session distance unit to match the map's unit, 
			// make note of the original session distance unit, so we can restore it later. 
			oldSessionDistanceUnit = InteropHelper.GetSessionDistanceUnit();
			mapUnit = InteropHelper.GetMapperDistanceUnit(windowId);
			InteropHelper.SetSessionDistanceUnit(mapUnit);

			zoomValue = InteropHelper.GetMapperZoom(windowId);  // Get the zoom value 

			InteropHelper.SetSessionDistanceUnit(oldSessionDistanceUnit); // restore original distance unit

			AddNViewDlg addViewDlg = new AddNViewDlg();
			addViewDlg.m_currentZoom = InteropHelper.GetFormattedString(zoomValue);
			DialogResult dlgResult = addViewDlg.ShowDialog(this);

			if (dlgResult == DialogResult.OK) {
				string nodeName = addViewDlg.m_viewName;
				AddNewNodeToTree(nodeName, centerX, centerY, zoomValue, mapUnit, mapCSys);
				UpdateButtons();
				bTreeChanged = true;
			}

			addViewDlg.Dispose();
		}

		/// <summary>
		/// Rename button handler.
		/// This function facilitates renaming of a folder name or a view name.
		/// Starts label editing on selected node.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void btnRename_Click(object sender, EventArgs e)
		{
			if (tvwNamedViews.SelectedNode != null)
				tvwNamedViews.SelectedNode.BeginEdit();
		}


		/// <summary>
		/// New Folder button handler.
		/// This function adds a new folder to the treeview.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void btnNewFolder_Click(object sender, EventArgs e)
		{
			TreeNode tNode = tvwNamedViews.SelectedNode;
			if (tNode != null) {
				// if selected node is a view node use its parent
				if (!tNode.IsExpanded)
					tNode = tNode.Parent;
			}

			//TODO: Need to write a logic to generate some initial name for folder
			string folderName = Properties.Resources.STR_DEF_FOLDER_NAME;
			TreeNode newNode = null;

			// add the node add appropriate location in the tree
			if (tNode != null) {
				folderName = GenerateNewFolderNameNoDuplicate(tNode.Nodes, folderName, 0);
				newNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tNode.Nodes, folderName);
				tNode.Expand();
			} else {
				folderName = GenerateNewFolderNameNoDuplicate(tvwNamedViews.Nodes, folderName, 0);
				newNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tvwNamedViews.Nodes, folderName);
			}

			bTreeChanged = true;

			// start the editing on the folder node so that 
			// the user can change the folder name if required
			newNode.BeginEdit();
		}

		/// <summary>
		/// Moves a node (view of folder node) to a folder node
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void btnMove_Click(object sender, EventArgs e)
		{
			// Write any changes to XML file.
			WriteTreeToFile(sXMLFile);

			// Get the node that will be moved
			TreeNode srcNode = tvwNamedViews.SelectedNode;

			if (srcNode == null)
				return;
			
			// Show the folders dialog to select the destination folder
			MoveSelNodeDlg moveSelDlg = new MoveSelNodeDlg();
			moveSelDlg.m_sXMLFile = sXMLFile;
			DialogResult dlgResult = moveSelDlg.ShowDialog(this);

			// If user clicked on OK button
			if (dlgResult == DialogResult.Yes)
			{
				if (!TreeNodeUtil.IsViewNode(srcNode))
				{
					srcNode.Collapse();
					srcNode.ImageIndex = 1;
				}
				
				string nodeFullPath = moveSelDlg.m_sSelectedNodeFullPath;
				TreeNode destNode = null;
				if (nodeFullPath.Length > 0) {
					// Locate the destination folder in the local tree view
					destNode = TreeNodeUtil.GetNodeFromPath(
						tvwNamedViews.Nodes, nodeFullPath, tvwNamedViews.PathSeparator);

					if (!destNode.Equals(srcNode)) {
						// Do not allow a node to be dropped on a child/grand child
						if (TreeNodeUtil.ContainsNode(srcNode, destNode))
						{
							MessageBox.Show(Properties.Resources.ERR_INVALID_DROP,
									Properties.Resources.ERR_INVALID_DROP_MSG_TITLE,
										MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
							return;
						}
						
						// Move the node
						destNode.Nodes.Add((TreeNode)srcNode.Clone());
						destNode.Expand();
						destNode.ImageIndex = 0;
						destNode.SelectedImageIndex = 0;
					}
				}
 
				else {
					tvwNamedViews.Nodes.Add((TreeNode)srcNode.Clone());
				}

				TreeNode srcNodeParent = srcNode.Parent;
				srcNode.Remove();
				if (srcNodeParent != null)
				{
					if (srcNodeParent.Nodes.Count == 0)
					{
						srcNodeParent.Collapse();
						srcNodeParent.ImageIndex = 1;
						srcNodeParent.SelectedImageIndex = 1;
					}

				}

				bTreeChanged = true;
			}

			moveSelDlg.Dispose();

		}


		/// <summary>
		/// Delete button handler.
		/// This function confirms the deletion and deletes a selected node.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void btnDelete_Click(object sender, EventArgs e)
		{
			// If there is a selected node display a confirmation message
			if (tvwNamedViews.SelectedNode != null) {
				DialogResult dlgResult = MessageBox.Show(
					Properties.Resources.CONFIRM_NODE_DELETE,
						Properties.Resources.CONFIRM_NODE_DELETE_MSG_TITLE,
							MessageBoxButtons.YesNo, MessageBoxIcon.Warning, MessageBoxDefaultButton.Button2);
				// If user confirms deletion delete the selected node
				if (dlgResult == DialogResult.Yes) {
					tvwNamedViews.SelectedNode.Remove();
					UpdateButtons();
					bTreeChanged = true;
				}
			}
		}

		/// <summary>
		/// On closing the dock window we will also like to update the Xml file
		/// </summary>
		public void CloseDockWindow()
		{
			//Write out the XML file that stores the Named Views info
			WriteTreeToFile(sXMLFile);
			_controller.DockWindowClose();
		}
		
		/// <summary>
		/// Set the dialog position and docking state 
		/// </summary>
		public void SetDockPosition()
		{
			_controller.SetDockWindowPositionFromFile();
		}

  
		
		/// <summary>
		/// Goto button handler.
		/// This function gets the top mapper window. 
		/// It then reads the View node information from
		/// the selected TreeNode and sets the current view
		/// of Mapper window.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void btnGoto_Click(object sender, EventArgs e)
		{
			// Get the selected node in the tree
			// Note: if there is no selected node in the tree
			TreeNode tNode = tvwNamedViews.SelectedNode;

			if (tNode == null)
				return;

			if (!TreeNodeUtil.IsViewNode(tNode))
				return;


			// get window id
			int windowId = InteropHelper.GetMapWindowId();
			if (windowId == 0)
			{
				return;
			}

			TreeNodeUtil.t_NodeInfo tNodeInfo = (TreeNodeUtil.t_NodeInfo)tNode.Tag;
			InteropHelper.SetView(windowId, tNodeInfo.m_x, tNodeInfo.m_y, tNodeInfo.m_zoom, tNodeInfo.m_unit, tNodeInfo.m_csys);
		}

		#endregion


		#region [HELPER FUNCTIONS]
		// This function accepts and initial name and counter and 
		// generates a name unique to a collection of nodes which
		// is passed to this function as first parameter
		/// <summary>
		/// This function accepts and initial name and counter and
		/// generates a name unique to a collection of nodes which
		/// is passed to this function as first parameter.
		/// </summary>
		/// <param name="checkNodes">Collection of tree nodes to check for duplicate names</param>
		/// <param name="initialName">Initial name</param>
		/// <param name="iCtr">A counter that will be used as suffix to initial name
		/// when a duplicate name is found. This counter is incremented
		/// until a unique name is reached.</param>
		/// <returns></returns>
		private string GenerateNewFolderNameNoDuplicate(TreeNodeCollection checkNodes, string initialName, int iCtr)
		{
			
			string folderName = initialName;
			if (iCtr > 0)
				if (System.Threading.Thread.CurrentThread.CurrentUICulture.TextInfo.IsRightToLeft)
				{
					folderName = "(" + Convert.ToString(iCtr) + ")" + folderName;
				}
				else
					folderName = folderName + "(" + Convert.ToString(iCtr) + ")";
			
			foreach (TreeNode tn in checkNodes)
			{
				if (string.Compare(tn.Text, folderName) == 0)
				{
					iCtr++;
					folderName = GenerateNewFolderNameNoDuplicate(checkNodes, initialName, iCtr);
					break;
				}
			}
			return folderName;
		}

		/// <summary>
		/// This function uses the input from Add New View dialog and
		/// add a new node to the treeview control which represents a view
		/// </summary>
		/// <param name="nodeName"></param>
		/// <param name="x"></param>
		/// <param name="y"></param>
		/// <param name="zoom"></param>
		/// <param name="unit"></param>
		private void AddNewNodeToTree(string nodeName, string x, string y, string zoom, string unit, string csys)
		{
			// Get the selected node
			TreeNode tNode = tvwNamedViews.SelectedNode;
			if (tNode != null) {
				// if selected node is a view node use its parent
				if (!tNode.IsExpanded)
					tNode = tNode.Parent;
			}

			// add the node add appropriate location in the tree
			if (tNode != null) {
				TreeNodeUtil.AddViewNodeToNodeCollection(tNode.Nodes, nodeName, x, y, zoom, unit, csys);
				tNode.Expand();
			} else {
				TreeNodeUtil.AddViewNodeToNodeCollection(tvwNamedViews.Nodes, nodeName, x, y, zoom, unit, csys);
			}
		}

		/// <summary>
		/// This function accepts the name of xml file
		/// and fill the content of xml file in the 
		/// treeview control
		/// </summary>
		/// <param name="fName"></param>
		private void LoadTreeFromFile(string fName)
		{
			string sErr = string.Empty;
			
			XmlNode rootNode = null;
			
			// Wait until safe to read from file
			mut.WaitOne();

			// Try to read the xml file
			XmlDocument xmlDoc = new XmlDocument();
			try
			{
				//if (!System.IO.File.Exists(fName))
				//    throw new XmlException("XML file doesnot exist");
				
				// Load the xml file
				xmlDoc.Load(fName);

				// Jump to the dialog node
				XmlNodeList xmlNodeList = xmlDoc.SelectNodes(STR_PATH_DIALOG);

				if (xmlNodeList == null)
					throw new XmlException(Properties.Resources.ERR_INVALID_XML);

				XmlNode dialogNode = xmlNodeList[0];
				if (dialogNode == null)
					throw new XmlException(Properties.Resources.ERR_INVALID_XML);

				// Preserve the dialog dimensions
				dialogLeft = Convert.ToInt32(dialogNode.Attributes[STR_LEFT].Value);
				dialogTop = Convert.ToInt32(dialogNode.Attributes[STR_TOP].Value);
				dialogWidth = Convert.ToInt32(dialogNode.Attributes[STR_WIDTH].Value);
				dialogHeight = Convert.ToInt32(dialogNode.Attributes[STR_HEIGHT].Value);

				// Jump to the root node (it contains all the top level nodes)
				// This node is not displayed in TreeView. It represent the 
				// TreeView itself.
				xmlNodeList = xmlDoc.SelectNodes(STR_PATH_ROOT_FOLDER);

				if (xmlNodeList == null)
					throw new XmlException(Properties.Resources.ERR_INVALID_XML);

				rootNode = xmlNodeList[0];
				if (rootNode == null)
					throw new XmlException(Properties.Resources.ERR_INVALID_XML);


				// traverse all the folder and view nodes in XML file
				foreach (XmlNode xmlNode in rootNode.ChildNodes)
				{
					TreeNode tNode = null;
					if (string.Compare(xmlNode.Name, STR_VIEWS, true) == 0)
					{
						tNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tvwNamedViews.Nodes, xmlNode.Attributes["Name"].Value);
						TreeNodeUtil.FillTreeNode(tNode, xmlNode);
					}
					else
					{
						tNode = TreeNodeUtil.AddViewNodeToNodeCollection(tvwNamedViews.Nodes, xmlNode.InnerText, xmlNode.Attributes["X"].Value, xmlNode.Attributes["Y"].Value, xmlNode.Attributes["Zoom"].Value, xmlNode.Attributes["Unit"].Value, xmlNode.Attributes["CoordSys"].Value);
					}

				}
			}
			catch (System.Xml.XPath.XPathException ex) {
				sErr = ex.Message;
			} catch (XmlException ex) {
				sErr = ex.Message;
			} catch (ArgumentException ex) {
				sErr = ex.Message;
			} catch (FileNotFoundException) {
				sErr = string.Empty;
			}

			if (sErr != string.Empty)
				MessageBox.Show(sErr);

			bTreeChanged = false;

			//release the mutex
			mut.ReleaseMutex();
		}

		// This function writes the treeview to the xml file.
		// It uses mutexes to synchronize the threads accessing
		// the xml file
		private void WriteTreeToFile(string fName)
		{
			string sErr = string.Empty;

			if (!bTreeChanged)
				return;

			//wait until safe to read from file
			mut.WaitOne();

			try
			{
				XmlTextWriter xw = new XmlTextWriter(fName, System.Text.Encoding.Unicode);

				// Use indenting for readability.
				xw.Formatting = Formatting.Indented;

				// write the XML declaration
				xw.WriteStartDocument();

				// write the root element (represents the tool itself)
				xw.WriteStartElement(STR_NAMEDVIEWS);

				// write the dimensions of dialog
				xw.WriteStartElement(STR_DIALOG);
				xw.WriteAttributeString(STR_LEFT, Convert.ToString(this.Left));
				xw.WriteAttributeString(STR_TOP, Convert.ToString(this.Top));
				xw.WriteAttributeString(STR_WIDTH, Convert.ToString(this.Width));
				xw.WriteAttributeString(STR_HEIGHT, Convert.ToString(this.Height));
				xw.WriteEndElement();


				// Write the root node which contains all the other nodes
				// This node is never displayed in the tree view it simply
				// contains all the other nodes
				xw.WriteStartElement(STR_VIEWS);
				xw.WriteAttributeString(STR_NAME, STR_ROOT);

				// start writing the nodes in the tree
				foreach (TreeNode tn in tvwNamedViews.Nodes)
				{
					if (TreeNodeUtil.IsViewNode(tn))
					{
						TreeNodeUtil.WriteViewNodeToFile(xw, tn);
					}
					else
					{
						TreeNodeUtil.WriteFolderNodeToFile(xw, tn);
					}
				}

				// end the root node element (the container of all nodes)
				xw.WriteEndElement();

				// end the root element (represent the tool)
				xw.WriteEndElement();

				// finish the write operation
				xw.Flush(); xw.Close();

			} catch (DirectoryNotFoundException ex) {
				sErr = ex.Message;
			} catch (IOException ex) {
				sErr = ex.Message;
			} catch (UnauthorizedAccessException ex) {
				sErr = ex.Message;
			} catch (InvalidOperationException ex) {
				sErr = ex.Message;
			} catch (ArgumentException ex) {
				sErr = ex.Message;
			}

			if (sErr != string.Empty)
				MessageBox.Show(sErr);

			bTreeChanged = false;

			//release the mutex
			mut.ReleaseMutex();
		}

		
		/// <summary>
		/// Enables and disables command buttons based on the treeview state
		/// </summary>
		private void UpdateButtons()
		{
			btnGoto.Enabled = (tvwNamedViews.Nodes.Count > 0 &&
				tvwNamedViews.SelectedNode != null && TreeNodeUtil.IsViewNode(tvwNamedViews.SelectedNode));
			btnMove.Enabled = (tvwNamedViews.Nodes.Count > 0 &&
				tvwNamedViews.SelectedNode != null);
			btnRename.Enabled = (tvwNamedViews.Nodes.Count > 0 &&
				tvwNamedViews.SelectedNode != null);
			btnDelete.Enabled = (tvwNamedViews.Nodes.Count > 0 &&
				tvwNamedViews.SelectedNode != null);
				
		}

		#endregion


	}
}
