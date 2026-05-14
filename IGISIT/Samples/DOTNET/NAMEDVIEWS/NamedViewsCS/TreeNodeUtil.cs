using System;
using System.Windows.Forms;
using System.Xml;

namespace MISamples
{
	static class TreeNodeUtil
	{
		private const string STR_VIEWS = "Views";
		private const string STR_NAME = "Name";
		private const string STR_VIEW = "View";
		private const string STR_X = "X";
		private const string STR_Y = "Y";
		private const string STR_ZOOM = "Zoom";
		private const string STR_UNIT = "Unit";
		private const string STR_CSYS = "CoordSys"; 
		
		/// <summary>
		/// This structure will be used
		/// to store the information of 
		/// each node.
		/// </summary>
		public struct t_NodeInfo
		{
			public bool m_nodeTypeView;
			public string m_zoom;
			public string m_unit; 
			public string m_x;
			public string m_y;
			public string m_csys; 


			public t_NodeInfo(bool nodeTypeView)
			{
				m_nodeTypeView = nodeTypeView;
				m_zoom = "0";
				m_x = "0";
				m_y = "0"; 
				m_unit = "mi";
				m_csys = "CoordSys Earth"; 
			}
		}

		#region [ADD NODES TO TREE]

		/// <summary>
		/// Reads child nodes from the XmlNode and adds them to recursively
		/// to the TreeNode
		/// </summary>
		/// <param name="treeNode">The tree node to fill</param>
		/// <param name="xmlNode">The xml node to read from</param>
		public static void FillTreeNode(TreeNode treeNode, XmlNode xmlNode)
		{
			if (xmlNode.HasChildNodes)
			{
				foreach (XmlNode n in xmlNode.ChildNodes)
				{
					TreeNode tNode = null;
					if (string.Compare(n.Name, STR_VIEWS, true) == 0)
					{
						tNode = AddFolderNodeToNodeCollection(treeNode.Nodes, n.Attributes[STR_NAME].Value);
						FillTreeNode(tNode, n);
					}
					else
					{
						tNode = AddViewNodeToNodeCollection(treeNode.Nodes, n.InnerText, n.Attributes["X"].Value, n.Attributes["Y"].Value, n.Attributes["Zoom"].Value, n.Attributes["Unit"].Value, n.Attributes["CoordSys"].Value); 
					}
				}
			}
		}

		/// <summary>
		/// Reads child nodes from the XmlNode and adds folders recursively
		/// to the TreeNode
		/// </summary>
		/// <param name="treeNode">The tree node to fill</param>
		/// <param name="xmlNode">The xml node to read from</param>
		public static void FillTreeNodeOnlyFolders(TreeNode treeNode, XmlNode xmlNode)
		{
			if (xmlNode.HasChildNodes)
			{
				foreach (XmlNode n in xmlNode.ChildNodes)
				{
					TreeNode tNode = null;
					if (string.Compare(n.Name, STR_VIEWS, true) == 0)
					{
						tNode = AddFolderNodeToNodeCollection(treeNode.Nodes, n.Attributes[STR_NAME].Value);
						FillTreeNodeOnlyFolders(tNode, n);
					}
				}
			}
		}

		/// <summary>
		/// Add node to the node collection as a folder node.
		/// </summary>
		/// <param name="nodCol">The node collection to add a folder node to.</param>
		/// <param name="nodeName">Name of the folder</param>
		/// <returns>The newly added tree node</returns>
		public static TreeNode AddFolderNodeToNodeCollection(TreeNodeCollection nodCol, string nodeName)
		{
			// create node information for a folder node
			t_NodeInfo nodeInfo = new t_NodeInfo(false);

			// setup the new View node with node information
			TreeNode newNode = new TreeNode();
			newNode.ImageIndex = 1;
			newNode.SelectedImageIndex = 1;
			newNode.Tag = nodeInfo;
			newNode.Text = nodeName;
			newNode.Name = nodeName;

			nodCol.Add(newNode);

			newNode.ToolTipText = newNode.FullPath;

			return newNode;

		}

		/// <summary>
		/// Add a view node with view information to the tree node collection.
		/// </summary>
		/// <param name="nodCol">The node collection to add a view node to.</param>
		/// <param name="nodeName">Name of the view</param>
		/// <param name="x">Center X of the view</param>
		/// <param name="y">Center Y of the view</param>
		/// <param name="zoom">Zoom of the view</param>
		/// <param name="unit">Distance unit describing the zoom, such as mi or km</param>
		/// <param name="csys">CoordSys string, which defines the units for the X/Y coordinates</param>
		/// <returns>The newly added tree node</returns>
		public static TreeNode AddViewNodeToNodeCollection(TreeNodeCollection nodCol, string nodeName, string x, string y, string zoom, string unit, string csys)
		{
			// setup the node information
			t_NodeInfo nodeInfo = new t_NodeInfo(true);
			nodeInfo.m_x = x;
			nodeInfo.m_y = y;
			nodeInfo.m_zoom = zoom;
			nodeInfo.m_unit = unit;
			nodeInfo.m_csys = csys; 

			// setup the new View node with node information
			TreeNode newNode = new TreeNode();
			
			newNode.ImageIndex = 2;
			newNode.SelectedImageIndex = 2;
			newNode.Tag = nodeInfo;
			newNode.Text = nodeName;
			newNode.Name = nodeName;
			newNode.ToolTipText = string.Format(Properties.Resources.STR_TOOLTIP_VIEW,
					InteropHelper.GetFormattedString(nodeInfo.m_x),
					InteropHelper.GetFormattedString(nodeInfo.m_y),
					InteropHelper.GetFormattedString(nodeInfo.m_zoom), nodeInfo.m_unit);

			nodCol.Add(newNode);

			return newNode;
		}

		#endregion

		#region [WRITE TREE NODES TO XML]

		/// <summary>
		/// Writes a view to xml file
		/// </summary>
		/// <param name="xw"></param>
		/// <param name="node"></param>
		public static void WriteViewNodeToFile(XmlTextWriter xw, TreeNode node)
		{
			if (node == null)
				return;

			t_NodeInfo nodeInfo = (t_NodeInfo)node.Tag;
			xw.WriteStartElement(STR_VIEW);
			xw.WriteAttributeString(STR_X, Convert.ToString(nodeInfo.m_x));
			xw.WriteAttributeString(STR_Y, Convert.ToString(nodeInfo.m_y));
			xw.WriteAttributeString(STR_ZOOM, Convert.ToString(nodeInfo.m_zoom));
			xw.WriteAttributeString(STR_UNIT, nodeInfo.m_unit);
			xw.WriteAttributeString(STR_CSYS, nodeInfo.m_csys); 
			xw.WriteValue(node.Text);
			xw.WriteEndElement();
		}

		/// <summary>
		/// Writes a folder to the xml file
		/// </summary>
		/// <param name="xw"></param>
		/// <param name="node"></param>
		public static void WriteFolderNodeToFile(XmlTextWriter xw, TreeNode node)
		{
			if (node == null)
				return;
			xw.WriteStartElement(STR_VIEWS);
			xw.WriteAttributeString(STR_NAME, node.Text);
			foreach (TreeNode tn in node.Nodes) {
				if (TreeNodeUtil.IsViewNode(tn)) {
					WriteViewNodeToFile(xw, tn);
				} else {
					WriteFolderNodeToFile(xw, tn);
				}
			}
			xw.WriteEndElement();

		}

		#endregion

		#region [VALIDATE CONDITIONS]

		/// <summary>
		/// This function tells if a tree node represents a View Node.
		/// </summary>
		/// <param name="node">The TreeNode to be checked.</param>
		/// <returns>true if tree node is a view node.</returns>
		public static bool IsViewNode(TreeNode node)
		{
			t_NodeInfo nodeInfo = (t_NodeInfo)node.Tag;
			return nodeInfo.m_nodeTypeView;
		}

		/// <summary>
		/// Searches the container node recursively to look check
		/// if the contained node is a child/grand child.
		/// </summary>
		/// <param name="container">The node to seach recursively</param>
		/// <param name="contained">The node to be checked as a child/grand child</param>
		/// <returns></returns>
		public static bool ContainsNode(TreeNode container, TreeNode contained)
		{
			bool ret = container.Nodes.Contains(contained);//false;
			foreach (TreeNode tn in container.Nodes)
			{
				if (tn.Equals(contained))
				{
					ret = true;
					break;
				}
				if (tn.Nodes.Count > 0)
				{
					if (ContainsNode(tn, contained))
					{
						ret = true;
						break;
					}
				}
			}
			return ret;
		}

		#endregion

		#region [TREEVIEW SEARCH]

		/// <summary>
		/// Retrieves a TreeNode based on its path.
		/// </summary>
		/// <param name="nodCol">The node collection where the search starts.</param>
		/// <param name="fullPath">The path to node relative to node collection.</param>
		/// <param name="pathSep">Path separator.</param>
		/// <returns></returns>
		public static TreeNode GetNodeFromPath(TreeNodeCollection nodCol, string fullPath, string pathSep)
		{
			TreeNode retNode = null;
			
			string[] sep = { pathSep };
			string[] nodes = fullPath.Split(sep, StringSplitOptions.None);
			TreeNodeCollection curCol = nodCol;
			for (int i = 0; i < nodes.Length; i++) {
				TreeNode[] nodesFound = curCol.Find(nodes[i], false);
				retNode = nodesFound[0];
				curCol = retNode.Nodes;
			}
			return retNode;
		}

		#endregion

	}
}
