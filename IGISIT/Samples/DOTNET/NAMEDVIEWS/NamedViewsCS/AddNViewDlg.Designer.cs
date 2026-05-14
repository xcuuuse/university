namespace MISamples
{
	partial class AddNViewDlg
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
			System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(AddNViewDlg));
			this.lblZoom = new System.Windows.Forms.Label();
			this.lblDescCurView = new System.Windows.Forms.Label();
			this.txtViewName = new System.Windows.Forms.TextBox();
			this.btnAdd = new System.Windows.Forms.Button();
			this.cmdCancel = new System.Windows.Forms.Button();
			this.SuspendLayout();
			// 
			// lblZoom
			// 
			resources.ApplyResources(this.lblZoom, "lblZoom");
			this.lblZoom.Name = "lblZoom";
			// 
			// lblDescCurView
			// 
			resources.ApplyResources(this.lblDescCurView, "lblDescCurView");
			this.lblDescCurView.Name = "lblDescCurView";
			// 
			// txtViewName
			// 
			resources.ApplyResources(this.txtViewName, "txtViewName");
			this.txtViewName.Name = "txtViewName";
			this.txtViewName.TextChanged += new System.EventHandler(this.txtViewName_TextChanged);
			// 
			// btnAdd
			// 
			this.btnAdd.DialogResult = System.Windows.Forms.DialogResult.OK;
			resources.ApplyResources(this.btnAdd, "btnAdd");
			this.btnAdd.Name = "btnAdd";
			this.btnAdd.UseVisualStyleBackColor = true;
			// 
			// cmdCancel
			// 
			this.cmdCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
			resources.ApplyResources(this.cmdCancel, "cmdCancel");
			this.cmdCancel.Name = "cmdCancel";
			this.cmdCancel.UseVisualStyleBackColor = true;
			// 
			// AddNViewDlg
			// 
			this.AcceptButton = this.btnAdd;
			resources.ApplyResources(this, "$this");
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.CancelButton = this.cmdCancel;
			this.Controls.Add(this.cmdCancel);
			this.Controls.Add(this.btnAdd);
			this.Controls.Add(this.txtViewName);
			this.Controls.Add(this.lblDescCurView);
			this.Controls.Add(this.lblZoom);
			this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
			this.MaximizeBox = false;
			this.MinimizeBox = false;
			this.Name = "AddNViewDlg";
			this.ShowInTaskbar = false;
			this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.AddNViewDlg_FormClosed);
			this.Load += new System.EventHandler(this.AddNViewDlg_Load);
			this.ResumeLayout(false);
			this.PerformLayout();

		}

		#endregion

		private System.Windows.Forms.Label lblZoom;
		private System.Windows.Forms.Label lblDescCurView;
		private System.Windows.Forms.TextBox txtViewName;
		private System.Windows.Forms.Button btnAdd;
		private System.Windows.Forms.Button cmdCancel;
	}
}