namespace MISamples
{
	partial class MoveSelNodeDlg
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
			System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MoveSelNodeDlg));
			this.tvwFolders = new System.Windows.Forms.TreeView();
			this.imageList1 = new System.Windows.Forms.ImageList(this.components);
			this.cmdOK = new System.Windows.Forms.Button();
			this.cmdCancel = new System.Windows.Forms.Button();
			this.SuspendLayout();
			// 
			// tvwFolders
			// 
			resources.ApplyResources(this.tvwFolders, "tvwFolders");
			this.tvwFolders.FullRowSelect = true;
			this.tvwFolders.HideSelection = false;
			this.tvwFolders.ImageList = this.imageList1;
			this.tvwFolders.Name = "tvwFolders";
			this.tvwFolders.ShowLines = false;
			this.tvwFolders.ShowPlusMinus = false;
			this.tvwFolders.ShowRootLines = false;
			this.tvwFolders.BeforeExpand += new System.Windows.Forms.TreeViewCancelEventHandler(this.tvwFolders_BeforeExpand);
			this.tvwFolders.BeforeCollapse += new System.Windows.Forms.TreeViewCancelEventHandler(this.tvwFolders_BeforeCollapse);
			// 
			// imageList1
			// 
			this.imageList1.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("imageList1.ImageStream")));
			this.imageList1.TransparentColor = System.Drawing.Color.Transparent;
			this.imageList1.Images.SetKeyName(0, "OPENFOLD.ICO");
			this.imageList1.Images.SetKeyName(1, "CLSDFOLD.ICO");
			// 
			// cmdOK
			// 
			resources.ApplyResources(this.cmdOK, "cmdOK");
			this.cmdOK.DialogResult = System.Windows.Forms.DialogResult.Yes;
			this.cmdOK.Name = "cmdOK";
			this.cmdOK.UseVisualStyleBackColor = true;
			this.cmdOK.Click += new System.EventHandler(this.cmdOK_Click);
			// 
			// cmdCancel
			// 
			resources.ApplyResources(this.cmdCancel, "cmdCancel");
			this.cmdCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
			this.cmdCancel.Name = "cmdCancel";
			this.cmdCancel.UseVisualStyleBackColor = true;
			// 
			// MoveSelNodeDlg
			// 
			resources.ApplyResources(this, "$this");
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.CancelButton = this.cmdCancel;
			this.Controls.Add(this.cmdCancel);
			this.Controls.Add(this.cmdOK);
			this.Controls.Add(this.tvwFolders);
			this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
			this.MaximizeBox = false;
			this.MinimizeBox = false;
			this.Name = "MoveSelNodeDlg";
			this.ShowInTaskbar = false;
			this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MoveSelNodeDlg_FormClosing);
			this.Load += new System.EventHandler(this.MoveSelNodeDlg_Load);
			this.ResumeLayout(false);

		}

		#endregion

		private System.Windows.Forms.TreeView tvwFolders;
		private System.Windows.Forms.Button cmdOK;
		private System.Windows.Forms.Button cmdCancel;
		private System.Windows.Forms.ImageList imageList1;
	}
}