using System;
using System.Windows.Forms;
using System.Xml;

namespace MISamples
{
	public partial class MoveSelNodeDlg : Form
	{
		private const string STR_VIEWS = "Views";
		private const string STR_NAME = "Name";

		private const string STR_PATH_ROOT_FOLDER = "/NamedViews/Views";

		public string m_sXMLFile;
		public string m_sSelectedNodeFullPath;


		public MoveSelNodeDlg()
		{
			InitializeComponent();
		}

		#region [DIALOG EVENT HANDLERS]

		private void MoveSelNodeDlg_Load(object sender, EventArgs e)
		{
			LoadTreeFromFile(m_sXMLFile);
			if (tvwFolders.Nodes.Count > 0)
				tvwFolders.Nodes[0].Expand();
		}

		private void MoveSelNodeDlg_FormClosing(object sender, FormClosingEventArgs e)
		{
			if (e.CloseReason == CloseReason.UserClosing) {
				e.Cancel = true;
				this.Hide();
			}
		}

		#endregion

		#region [TREEVIEW EVENT HANDLERS]

		private void tvwFolders_BeforeExpand(object sender, TreeViewCancelEventArgs e)
		{
			TreeNode tNode = e.Node;
			tNode.ImageIndex = 0;
			tNode.SelectedImageIndex = 0;
		}

		private void tvwFolders_BeforeCollapse(object sender, TreeViewCancelEventArgs e)
		{
			TreeNode tNode = e.Node;
			tNode.ImageIndex = 1;
			tNode.SelectedImageIndex = 1;
		}

		#endregion

		#region [BUTTON HANDLERS]

		private void cmdOK_Click(object sender, EventArgs e)
		{
			if (tvwFolders.SelectedNode != null)
				if (tvwFolders.Nodes[0].Equals(tvwFolders.SelectedNode))
					m_sSelectedNodeFullPath = string.Empty;
				else
					m_sSelectedNodeFullPath = tvwFolders.SelectedNode.FullPath.Substring
						(tvwFolders.SelectedNode.FullPath.IndexOf(tvwFolders.PathSeparator) + 1);
			this.Hide();
		}

		#endregion

		#region [HELPER FUNCTIONS]

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

			// Try to read the xml file
			XmlDocument xmlDoc = new XmlDocument();
			try
			{
				// Load the xml file
				xmlDoc.Load(fName);

				// Jump to the root node (it contains all the top level nodes)
				// This node is not displayed in TreeView. It represent the 
				// TreeView itself.
				XmlNodeList xmlNodeList = xmlDoc.SelectNodes(STR_PATH_ROOT_FOLDER);

				if (xmlNodeList == null) {
					throw new XmlException(Properties.Resources.ERR_INVALID_XML);
				}

				rootNode = xmlNodeList[0];
				if (rootNode == null) {
					throw new XmlException(Properties.Resources.ERR_INVALID_XML);
				}

				TreeNode topNode = TreeNodeUtil.AddFolderNodeToNodeCollection(tvwFolders.Nodes, Properties.Resources.STR_MB_APP_DESC);

				// traverse all the folder and view nodes in XML file
				foreach (XmlNode xmlNode in rootNode.ChildNodes) {
					TreeNode tNode = null;
					if (string.Compare(xmlNode.Name, STR_VIEWS, true) == 0)
					{
						tNode = TreeNodeUtil.AddFolderNodeToNodeCollection(topNode.Nodes, xmlNode.Attributes[STR_NAME].Value);
						TreeNodeUtil.FillTreeNodeOnlyFolders(tNode, xmlNode);
					}

				}
			}
			catch (System.Xml.XPath.XPathException ex) {
				sErr = ex.Message;
			} catch (XmlException ex) {
				sErr = ex.Message;
			} catch (ArgumentException ex) {
				sErr = ex.Message;
			}

			if (sErr != string.Empty)
				MessageBox.Show(sErr);

		}

		#endregion
	}
}