// mdimavw.cpp : implementation of the CMdimapView class
//

#include "stdafx.h"
#include "mdimap.h"

#include "mdimadoc.h"
#include "mdimavw.h"
#include "mapinfow.h"   // ADDED FOR INTEGRATED MAPPING SUPPORT

#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CMdimapView

IMPLEMENT_DYNCREATE(CMdimapView, CView)

BEGIN_MESSAGE_MAP(CMdimapView, CView)
	//{{AFX_MSG_MAP(CMdimapView)
	ON_WM_CREATE()
    // ADDED FOR INTEGRATED MAPPING SUPPORT
	ON_WM_DESTROY()
	ON_WM_ERASEBKGND()
	ON_WM_SIZE()
	ON_UPDATE_COMMAND_UI(ID_MAP_LAYERCONTROL, OnUpdateMapLayercontrol)
	ON_COMMAND(ID_MAP_LAYERCONTROL, OnMapLayercontrol)
	ON_UPDATE_COMMAND_UI(ID_MAP_CREATETHEME, OnUpdateMapCreatetheme)
	ON_COMMAND(ID_MAP_CREATETHEME, OnMapCreatetheme)
	ON_UPDATE_COMMAND_UI(ID_MAP_VIEWENTIRELAYER, OnUpdateMapViewentirelayer)
	ON_COMMAND(ID_MAP_VIEWENTIRELAYER, OnMapViewentirelayer)
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CMdimapView construction/destruction

CMdimapView::CMdimapView()
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    m_lWindowID = 0L;
    m_hwndWindow = NULL;
    m_bViewInitialized = FALSE;
    m_bMapper = FALSE;
    m_bBrowser = FALSE;
    m_lLegendID = 0L;
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

CMdimapView::~CMdimapView()
{
}

/////////////////////////////////////////////////////////////////////////////
// CMdimapView drawing

void CMdimapView::OnDraw(CDC* pDC)
{
	CMdimapDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	// TODO: add draw code for native data here
}

/////////////////////////////////////////////////////////////////////////////
// CMdimapView diagnostics

#ifdef _DEBUG
void CMdimapView::AssertValid() const
{
	CView::AssertValid();
}

void CMdimapView::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

CMdimapDoc* CMdimapView::GetDocument() // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CMdimapDoc)));
	return (CMdimapDoc*)m_pDocument;
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CMdimapView message handlers

int CMdimapView::OnCreate(LPCREATESTRUCT lpCreateStruct) 
{
	if (CView::OnCreate(lpCreateStruct) == -1)
		return -1;

	return 0;
}

void CMdimapView::OnDestroy() 
{
	CView::OnDestroy();
	
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    GetOurApp()->ClearOverview(m_lWindowID);
    if (m_hwndWindow) {
        CString strCommand;
        strCommand.Format("Close Window %ld", m_lWindowID);
        mapinfo.Do(strCommand);
        m_hwndWindow = NULL;
        m_lWindowID = 0L;
        m_lLegendID = 0L;
    }
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

void CMdimapView::OnInitialUpdate() 
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    CString strCommand;

    // Tables are opened in the document and displayed in the view
    CMdimapDoc *pDoc = GetDocument();

    // Find out whether table is mappable
    strCommand.Format("TableInfo(%s,%d)", (LPCTSTR)pDoc->GetAlias(), TAB_INFO_MAPPABLE);
	CString strResult = mapinfo.Eval(strCommand);
	if (strResult[0] == 'T') {
        strCommand.Format("Set Next Document Parent %lu Style 1  Map From %s", (long)m_hWnd, (LPCTSTR)pDoc->GetAlias());
        m_bMapper=TRUE;
	}
    else {
        strCommand.Format("Set Next Document Parent %lu Style 1  Browse * From %s", (long)m_hWnd, (LPCTSTR)pDoc->GetAlias());
        m_bBrowser=TRUE;
    }
    mapinfo.Do(strCommand);

    m_lWindowID = atol(mapinfo.Eval("WindowID(0)"));
    strCommand.Format("WindowInfo(0, %u)", WIN_INFO_WND);
    m_hwndWindow = (HWND)atol(mapinfo.Eval(strCommand));
    m_bViewInitialized=TRUE;

    // Set mouse mode to current tool
	mapinfo.RunMenuCommand(GetOurApp()->MouseMode());

    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

	CView::OnInitialUpdate();
}

BOOL CMdimapView::OnEraseBkgnd(CDC* pDC) 
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    // Once MapInfo has drawn the mapper window, don't allow background erases
    // to occur. This allows you to drag the infotool (or other reparented windows)
    // over the view window without having Windows erase underneath.
    // Other option is to set view hwnd window styles to WS_CLIPCHILDREN
	if (!m_bViewInitialized) {
		return CView::OnEraseBkgnd(pDC);
	}
	return FALSE;
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

void CMdimapView::OnSize(UINT nType, int cx, int cy) 
{
	CView::OnSize(nType, cx, cy);
	
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    if (m_bViewInitialized && cx > 0 && cy > 0) {
        ::MoveWindow(m_hwndWindow, 0, 0, cx, cy, TRUE); 
    }
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

void CMdimapView::OnActivateView(BOOL bActivate, CView* pActivateView, CView* pDeactiveView) 
{
	CView::OnActivateView(bActivate, pActivateView, pDeactiveView);
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    if (bActivate) {
        if (m_hwndWindow != NULL) {
            ::SetFocus(m_hwndWindow);
            //GetOurApp()->PostOverviewUpdate(m_lWindowID);
        }
    }
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

/////////////////////////////////////////////////////////////////////////////
// Remaining functions ADDED FOR INTEGRATED MAPPING SUPPORT

void CMdimapView::OnUpdateMapLayercontrol(CCmdUI* pCmdUI) 
{
	CMdimapDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapper);
}

void CMdimapView::OnMapLayercontrol() 
{
	mapinfo.RunMenuCommand(M_MAP_LAYER_CONTROL);
}

void CMdimapView::OnUpdateMapCreatetheme(CCmdUI* pCmdUI) 
{
	CMdimapDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapper);
}

void CMdimapView::OnMapCreatetheme() 
{
	mapinfo.RunMenuCommand(M_MAP_THEMATIC);
}

void CMdimapView::OnUpdateMapViewentirelayer(CCmdUI* pCmdUI) 
{
	CMdimapDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapper);
}

void CMdimapView::OnMapViewentirelayer() 
{
	mapinfo.RunMenuCommand(M_MAP_ENTIRE_LAYER);
}

void CMdimapView::OnWindowContentsChanged(void)
{
    TRACE("CMdimapView::OnWindowContentsChanged\n");

    // Do LegendMaintence - this is responsible for showing/hiding 
    // the legend associated with the thematic map.
    BOOL bHasThematic = FALSE;
    int nNumThematic;
    CString strCommand;

	strCommand.Format("MapperInfo(%lu,%d)",m_lWindowID,MAPPER_INFO_NUM_THEMATIC);
    nNumThematic = atoi(mapinfo.Eval(strCommand));
    if (nNumThematic > 0) {
        bHasThematic = TRUE;
    }
            
    if (bHasThematic && m_lLegendID == 0L) {
        // create legend
        strCommand.Format("Set Next Document Parent WindowInfo(%lu,%d) Style 1",m_lWindowID,WIN_INFO_WND);
        mapinfo.Do(strCommand);
        strCommand.Format("Create Legend From Window %lu",m_lWindowID);
        mapinfo.Do(strCommand);
    	m_lLegendID = atol(mapinfo.Eval("WindowID(0)"));
    }
    else if (!bHasThematic && m_lLegendID != 0L) {
    	// destroy legend
        strCommand.Format("Close Window %lu", m_lLegendID);
		mapinfo.Do(strCommand);
    	m_lLegendID = 0l;
    }

}

void CMdimapView::OnUpdate(CView* pSender, LPARAM lHint, CObject* pHint) 
{
    if (lHint != m_lWindowID || !m_bMapper) {
        return;
    }
    OnWindowContentsChanged();
}

// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
