// mainfrm.h : interface of the CMainFrame class
//
/////////////////////////////////////////////////////////////////////////////
#if !defined MAINFRM_H
#define MAINFRM_H

#include "mapbasic.h"       // ADDED FOR INTEGRATED MAPPING SUPPORT (for Mouse Modes)

/////////////////////////////////////////////////////////////////////////////
// Forward declarations
class COverviewDlg;

class CMainFrame : public CMDIFrameWnd
{
	DECLARE_DYNAMIC(CMainFrame)
public:
	CMainFrame();

public:
	enum tagMouseModes {
		MM_TOOLBAR_NOMODE=(-1),
		MM_TOOLBAR_GRABBER=M_TOOLS_RECENTER,
		MM_TOOLBAR_ZOOMIN=M_TOOLS_EXPAND,
		MM_TOOLBAR_ZOOMOUT=M_TOOLS_SHRINK,
		MM_TOOLBAR_INFOTOOL=M_TOOLS_PNT_QUERY,
		MM_DEFAULT=MM_TOOLBAR_GRABBER,
	} m_eMouseMode;

// Attributes
public:
    COverviewDlg *m_pOvDlg;

// Operations
public:
    void ClearOverview(long lMapperId);
    void UpdateOverview(long lMapperId);
    int MouseMode(void) { return (int)m_eMouseMode; }
    void CheckDestroyOverview(void);
    long OverviewMapId(void);

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMainFrame)
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CMainFrame();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:  // control bar embedded members
	CStatusBar  m_wndStatusBar;
	CToolBar    m_wndToolBar;

// Generated message map functions
protected:
	//{{AFX_MSG(CMainFrame)
	afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	afx_msg void OnUpdateGrabber(CCmdUI* pCmdUI);
	afx_msg void OnGrabber();
	afx_msg void OnUpdateZoomin(CCmdUI* pCmdUI);
	afx_msg void OnZoomin();
	afx_msg void OnUpdateZoomout(CCmdUI* pCmdUI);
	afx_msg void OnZoomout();
	afx_msg void OnUpdateInfotool(CCmdUI* pCmdUI);
	afx_msg void OnInfotool();
	afx_msg void OnMapOverview();
    afx_msg LONG OnOverviewMessage(WPARAM wParam, LPARAM lParam);
	afx_msg void OnUpdateMapOverview(CCmdUI* pCmdUI);
	afx_msg void OnClose();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()

	// Generated OLE dispatch map functions
	//{{AFX_DISPATCH(CMainFrame)
	afx_msg SCODE WindowContentsChanged(long lWindowId);
	//}}AFX_DISPATCH
	DECLARE_DISPATCH_MAP()

};

/////////////////////////////////////////////////////////////////////////////
// Defines

#define M_TOOLS_DEFAULT M_TOOLS_RECENTER

#endif /* !defined MAINFRM_H */
