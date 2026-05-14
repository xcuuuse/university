namespace MISamples
{
	partial class NViewDlg
	{
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.IContainer components = null;

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		/// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing && (components != null))
			{
				components.Dispose();
			}
			base.Dispose(disposing);
		}

		#region Windows Form Designer generated code

		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			this.components = new System.ComponentModel.Container();
			System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(NViewDlg));
			this.tvwNamedViews = new System.Windows.Forms.TreeView();
			this.imageList1 = new System.Windows.Forms.ImageList(this.components);
			this.btnDelete = new System.Windows.Forms.Button();
			this.btnRename = new System.Windows.Forms.Button();
			this.btnMove = new System.Windows.Forms.Button();
			this.btnNewFolder = new System.Windows.Forms.Button();
			this.btnGoto = new System.Windows.Forms.Button();
			this.btnAdd = new System.Windows.Forms.Button();
			this.SuspendLayout();
			// 
			// tvwNamedViews
			// 
			this.tvwNamedViews.AllowDrop = true;
			resources.ApplyResources(this.tvwNamedViews, "tvwNamedViews");
			this.tvwNamedViews.FullRowSelect = true;
			this.tvwNamedViews.HideSelection = false;
			this.tvwNamedViews.ImageList = this.imageList1;
			this.tvwNamedViews.LabelEdit = true;
			this.tvwNamedViews.Name = "tvwNamedViews";
			this.tvwNamedViews.ShowNodeToolTips = true;
			this.tvwNamedViews.NodeMouseDoubleClick += new System.Windows.Forms.TreeNodeMouseClickEventHandler(this.tvwNamedViews_NodeMouseDoubleClick);
			this.tvwNamedViews.DragLeave += new System.EventHandler(this.tvwNamedViews_DragLeave);
			this.tvwNamedViews.AfterLabelEdit += new System.Windows.Forms.NodeLabelEditEventHandler(this.tvwNamedViews_AfterLabelEdit);
			this.tvwNamedViews.BeforeExpand += new System.Windows.Forms.TreeViewCancelEventHandler(this.tvwNamedViews_BeforeExpand);
			this.tvwNamedViews.BeforeCollapse += new System.Windows.Forms.TreeViewCancelEventHandler(this.tvwNamedViews_BeforeCollapse);
			this.tvwNamedViews.DragDrop += new System.Windows.Forms.DragEventHandler(this.tvwNamedViews_DragDrop);
			this.tvwNamedViews.AfterSelect += new System.Windows.Forms.TreeViewEventHandler(this.tvwNamedViews_AfterSelect);
			this.tvwNamedViews.DragEnter += new System.Windows.Forms.DragEventHandler(this.tvwNamedViews_DragEnter);
			this.tvwNamedViews.ItemDrag += new System.Windows.Forms.ItemDragEventHandler(this.tvwNamedViews_ItemDrag);
			this.tvwNamedViews.DragOver += new System.Windows.Forms.DragEventHandler(this.tvwNamedViews_DragOver);
			// 
			// imageList1
			// 
			this.imageList1.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("imageList1.ImageStream")));
			this.imageList1.TransparentColor = System.Drawing.Color.Transparent;
			this.imageList1.Images.SetKeyName(0, "OPENFOLD.ICO");
			this.imageList1.Images.SetKeyName(1, "CLSDFOLD.ICO");
			this.imageList1.Images.SetKeyName(2, "Globe.ico");
			// 
			// btnDelete
			// 
			resources.ApplyResources(this.btnDelete, "btnDelete");
			this.btnDelete.Name = "btnDelete";
			this.btnDelete.UseVisualStyleBackColor = true;
			this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);
			// 
			// btnRename
			// 
			resources.ApplyResources(this.btnRename, "btnRename");
			this.btnRename.Name = "btnRename";
			this.btnRename.UseVisualStyleBackColor = true;
			this.btnRename.Click += new System.EventHandler(this.btnRename_Click);
			// 
			// btnMove
			// 
			resources.ApplyResources(this.btnMove, "btnMove");
			this.btnMove.Name = "btnMove";
			this.btnMove.UseVisualStyleBackColor = true;
			this.btnMove.Click += new System.EventHandler(this.btnMove_Click);
			// 
			// btnNewFolder
			// 
			resources.ApplyResources(this.btnNewFolder, "btnNewFolder");
			this.btnNewFolder.Name = "btnNewFolder";
			this.btnNewFolder.UseVisualStyleBackColor = true;
			this.btnNewFolder.Click += new System.EventHandler(this.btnNewFolder_Click);
			// 
			// btnGoto
			// 
			resources.ApplyResources(this.btnGoto, "btnGoto");
			this.btnGoto.Name = "btnGoto";
			this.btnGoto.UseVisualStyleBackColor = true;
			this.btnGoto.Click += new System.EventHandler(this.btnGoto_Click);
			// 
			// btnAdd
			// 
			resources.ApplyResources(this.btnAdd, "btnAdd");
			this.btnAdd.Name = "btnAdd";
			this.btnAdd.UseVisualStyleBackColor = true;
			this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);
			// 
			// NViewDlg
			// 
			resources.ApplyResources(this, "$this");
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.Controls.Add(this.btnGoto);
			this.Controls.Add(this.btnAdd);
			this.Controls.Add(this.btnDelete);
			this.Controls.Add(this.btnRename);
			this.Controls.Add(this.btnMove);
			this.Controls.Add(this.btnNewFolder);
			this.Controls.Add(this.tvwNamedViews);
			this.MinimumSize = new System.Drawing.Size(200, 200);
			this.Name = "NViewDlg";
			this.Load += new System.EventHandler(this.NViewDlg_Load);
			this.ResumeLayout(false);

		}
	 
		#endregion

		private System.Windows.Forms.TreeView tvwNamedViews;
		private System.Windows.Forms.Button btnDelete;
		private System.Windows.Forms.Button btnRename;
		private System.Windows.Forms.Button btnMove;
		private System.Windows.Forms.Button btnNewFolder;
		private System.Windows.Forms.Button btnGoto;
		private System.Windows.Forms.Button btnAdd;
		private System.Windows.Forms.ImageList imageList1;

	}
}
