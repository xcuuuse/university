using System;
using System.Windows.Forms;

namespace MISamples
{
	public partial class AddNViewDlg : Form
	{
		public string m_viewName = "";     // stores the name of the view
		public string m_currentZoom = "0.0"; // stores the zoom value of the view

		/// <summary>
		/// Default constructor
		/// </summary>
		public AddNViewDlg()
		{
			InitializeComponent();
		}

		#region [DIALOG EVENT HANDLERS]

		/// <summary>
		/// Dialog/Form load event handler
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void AddNViewDlg_Load(object sender, EventArgs e)
		{
			lblZoom.Text = lblZoom.Text + " " + m_currentZoom; 
		}

		/// <summary>
		/// Handle this event to set the m_veiwName member variable when user clicks OK.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void AddNViewDlg_FormClosed(object sender, FormClosedEventArgs e)
		{
			if (DialogResult == DialogResult.OK)
			{
				m_viewName = txtViewName.Text;
			}
		}
		
		#endregion


		#region [CONTROL EVENT HANDLERS]

		/// <summary>
		/// Handle this event to make sure the Add button is disabled
		/// when the textbox is empty.
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void txtViewName_TextChanged(object sender, EventArgs e)
		{
			btnAdd.Enabled = txtViewName.Text.Length > 0;
		}

		#endregion

	}
}