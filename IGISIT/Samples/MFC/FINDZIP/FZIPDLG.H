// fzipdlg.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CFindZipDlg dialog

class CFindZipDlg : public CDialog
{
// Construction
public:
	CFindZipDlg(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CFindZipDlg)
	enum { IDD = IDD_FINDZIP };
	CString	m_strZip;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CFindZipDlg)
    protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	void AFXAPI DDV_ValidateInput(CDataExchange* pDX, LPCTSTR lpctstrInput);

	// Generated message map functions
	//{{AFX_MSG(CFindZipDlg)
	virtual BOOL OnInitDialog();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};
