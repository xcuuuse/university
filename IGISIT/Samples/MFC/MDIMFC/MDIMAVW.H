// mdimavw.h : interface of the CMdimapView class
//
/////////////////////////////////////////////////////////////////////////////
#if !defined MDIMAVW_H
#define MDIMAVW_H

class CMdimapDoc;

class CMdimapView : public CView
{
protected: // create from serialization only
	CMdimapView();
	DECLARE_DYNCREATE(CMdimapView)

// Attributes
public:
	CMdimapDoc* GetDocument();

// Operations
public:
// ADDED FOR INTEGRATED MAPPING SUPPORT
    BOOL ViewInitialized(void) { return m_bViewInitialized; }
    BOOL Mapper(void) { return m_bMapper; }
    BOOL Browser(void) { return m_bBrowser; }
    long WindowId(void) { return m_lWindowID; }
    void OnWindowContentsChanged(void);
// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMdimapView)
	public:
	virtual void OnDraw(CDC* pDC);  // overridden to draw this view
	virtual void OnInitialUpdate();
	protected:
	virtual void OnActivateView(BOOL bActivate, CView* pActivateView, CView* pDeactiveView);
	virtual void OnUpdate(CView* pSender, LPARAM lHint, CObject* pHint);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CMdimapView();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:
// ADDED FOR INTEGRATED MAPPING SUPPORT
    long  m_lWindowID;
    HWND  m_hwndWindow;
    BOOL  m_bViewInitialized;
    BOOL  m_bMapper;
    BOOL  m_bBrowser;
    long  m_lLegendID;
// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

// Generated message map functions
protected:
	//{{AFX_MSG(CMdimapView)
	afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	afx_msg void OnDestroy();
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	afx_msg void OnSize(UINT nType, int cx, int cy);
	afx_msg void OnUpdateMapLayercontrol(CCmdUI* pCmdUI);
	afx_msg void OnMapLayercontrol();
	afx_msg void OnUpdateMapCreatetheme(CCmdUI* pCmdUI);
	afx_msg void OnMapCreatetheme();
	afx_msg void OnUpdateMapViewentirelayer(CCmdUI* pCmdUI);
	afx_msg void OnMapViewentirelayer();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG  // debug version in mdimavw.cpp
inline CMdimapDoc* CMdimapView::GetDocument()
   { return (CMdimapDoc*)m_pDocument; }
#endif

/////////////////////////////////////////////////////////////////////////////
#endif /* !defined MDIMAVW_H */
