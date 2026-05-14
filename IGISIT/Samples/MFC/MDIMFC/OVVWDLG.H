// ovvwdlg.h : header file
// Entire File ADDED FOR INTEGRATED MAPPING SUPPORT
//
#if !defined OVVWDLG_H
#define OVVWDLG_H

/////////////////////////////////////////////////////////////////////////////
// COverviewDlg dialog

class COverviewDlg : public CDialog
{
// Construction
public:
	COverviewDlg(CWnd* pParent = NULL);   // standard constructor
	COverviewDlg(CString strTableName, CString strWndTitle, long m_lOriginalWindowID, CWnd* pParent = NULL);

// Dialog Data
	//{{AFX_DATA(COverviewDlg)
	enum { IDD = IDD_OVERVIEW };
		// NOTE: the ClassWizard will add data members here
	//}}AFX_DATA 

// Operations
public:
    BOOL Update(CString strTableName, CString strWndTitle, long lMapperId);
    BOOL Update(long lMapperId);
    BOOL ClearContents(long lMapperId);
    long WindowId(void) { return m_lWindowID; }
    long MapperId(void) { return m_lMapWindowID; }

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(COverviewDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	virtual void PostNcDestroy();
	//}}AFX_VIRTUAL

// Implementation
protected:
    CString m_strTableName;
    CString m_strWndTitle;
    long    m_lWindowID;
    HWND    m_hwndWindow;
    BOOL    m_bInitialized;
    long    m_lMapWindowID;
    double  m_dMapZoom;
    double  m_dMapCx;
    double  m_dMapCy;

	// Generated message map functions
	//{{AFX_MSG(COverviewDlg)
    afx_msg LONG OnCreateOverview(WPARAM wParam, LPARAM lParam);
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg void OnSize(UINT nType, int cx, int cy);
	afx_msg void OnClose();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()

// Operations
protected:
    void SetCaption(void);
    int CreateMapOverview();
    void GetMDIChildMapperInfo(void);
    void NewFrame(double dX1, double dY1, double dX2, double dY2);

};

/*****************************************************************************
 * Messages used by the Overview dlg.
 */
#define WM_CREATE_OVERVIEW  WM_USER+10
#define WM_OVERVIEW_MESSAGE  WM_USER+11

#endif /* !defined OVVWDLG_H */
