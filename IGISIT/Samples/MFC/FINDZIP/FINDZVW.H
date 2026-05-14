// findzvw.h : interface of the CFindzipView class
//
/////////////////////////////////////////////////////////////////////////////

class CFindzipView : public CView
{
protected: // create from serialization only
	CFindzipView();
	DECLARE_DYNCREATE(CFindzipView)

// ADDED FOR INTEGRATED MAPPING SUPPORT
public:
	enum tagMouseModes {
		MM_TOOLBAR_NOMODE=(-1),
		MM_TOOLBAR_GRABBER=0,
		MM_TOOLBAR_ZOOMIN=1,
		MM_TOOLBAR_ZOOMOUT=2,
		MM_TOOLBAR_INFOTOOL=3,
		MM_TOOLBAR_QUERY=4,
		MM_DEFAULT=MM_TOOLBAR_GRABBER
	} m_eMouseMode;
// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

// Attributes
public:
	CFindzipDoc* GetDocument();

// Operations
public:
    BOOL MapperInitialized(void) { return m_bMapperInitialized; }

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CFindzipView)
	public:
	virtual void OnDraw(CDC* pDC);  // overridden to draw this view
	virtual void OnInitialUpdate();
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CFindzipView();
    void OnWindowContentsChanged(void);

#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// ADDED FOR INTEGRATED MAPPING SUPPORT
private:
    long  m_lWindowID;
    HWND  m_hwndWindow;
    BOOL  m_bMapperInitialized;
// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

// Generated message map functions
protected:
	//{{AFX_MSG(CFindzipView)
	afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	afx_msg void OnDestroy();
	afx_msg void OnSize(UINT nType, int cx, int cy);
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	afx_msg void OnUpdateMapLayercontrol(CCmdUI* pCmdUI);
	afx_msg void OnMapLayercontrol();
	afx_msg void OnUpdateMapCreatetheme(CCmdUI* pCmdUI);
	afx_msg void OnMapCreatetheme();
	afx_msg void OnUpdateMapViewentirelayer(CCmdUI* pCmdUI);
	afx_msg void OnMapViewentirelayer();
	afx_msg void OnUpdateGrabber(CCmdUI* pCmdUI);
	afx_msg void OnGrabber();
	afx_msg void OnUpdateZoomin(CCmdUI* pCmdUI);
	afx_msg void OnZoomin();
	afx_msg void OnUpdateZoomout(CCmdUI* pCmdUI);
	afx_msg void OnZoomout();
	afx_msg void OnUpdateInfotool(CCmdUI* pCmdUI);
	afx_msg void OnInfotool();
	afx_msg void OnUpdateQuery(CCmdUI* pCmdUI);
	afx_msg void OnQuery();
	afx_msg void OnUpdateFindZip(CCmdUI* pCmdUI);
	afx_msg void OnFindZip();
	afx_msg void OnFilePrintmap();
	afx_msg void OnUpdateFilePrintmap(CCmdUI* pCmdUI);
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG  // debug version in findzvw.cpp
inline CFindzipDoc* CFindzipView::GetDocument()
   { return (CFindzipDoc*)m_pDocument; }
#endif

/////////////////////////////////////////////////////////////////////////////
