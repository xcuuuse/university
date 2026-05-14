// findzvw.cpp : implementation of the CFindzipView class
//

#include "stdafx.h"
#include "findzip.h"

#include "findzdoc.h"
#include "findzvw.h"
#include "mapinfow.h"   // ADDED FOR INTEGRATED MAPPING SUPPORT
#include "fzipdlg.h"    // Find Zip dialog class

#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CFindzipView

IMPLEMENT_DYNCREATE(CFindzipView, CView)

BEGIN_MESSAGE_MAP(CFindzipView, CView)
	//{{AFX_MSG_MAP(CFindzipView)
	ON_WM_CREATE()
	ON_WM_DESTROY()
	ON_WM_SIZE()
	ON_WM_ERASEBKGND()
	ON_UPDATE_COMMAND_UI(ID_MAP_LAYERCONTROL, OnUpdateMapLayercontrol)
	ON_COMMAND(ID_MAP_LAYERCONTROL, OnMapLayercontrol)
	ON_UPDATE_COMMAND_UI(ID_MAP_CREATETHEME, OnUpdateMapCreatetheme)
	ON_COMMAND(ID_MAP_CREATETHEME, OnMapCreatetheme)
	ON_UPDATE_COMMAND_UI(ID_MAP_VIEWENTIRELAYER, OnUpdateMapViewentirelayer)
	ON_COMMAND(ID_MAP_VIEWENTIRELAYER, OnMapViewentirelayer)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_GRABBER, OnUpdateGrabber)
	ON_COMMAND(ID_TOOLBAR_GRABBER, OnGrabber)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_ZOOMIN, OnUpdateZoomin)
	ON_COMMAND(ID_TOOLBAR_ZOOMIN, OnZoomin)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_ZOOMOUT, OnUpdateZoomout)
	ON_COMMAND(ID_TOOLBAR_ZOOMOUT, OnZoomout)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_INFOTOOL, OnUpdateInfotool)
	ON_COMMAND(ID_TOOLBAR_INFOTOOL, OnInfotool)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_QUERY, OnUpdateQuery)
	ON_COMMAND(ID_TOOLBAR_QUERY, OnQuery)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_FINDZIP, OnUpdateFindZip)
	ON_COMMAND(ID_TOOLBAR_FINDZIP, OnFindZip)
	ON_COMMAND(ID_FILE_PRINTMAP, OnFilePrintmap)
	ON_UPDATE_COMMAND_UI(ID_FILE_PRINTMAP, OnUpdateFilePrintmap)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CFindzipView construction/destruction

CFindzipView::CFindzipView()
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    m_lWindowID=0L;
    m_hwndWindow=NULL;
   	m_eMouseMode=MM_DEFAULT;
    m_bMapperInitialized=FALSE;
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

CFindzipView::~CFindzipView()
{
}

/////////////////////////////////////////////////////////////////////////////
// CFindzipView drawing

void CFindzipView::OnDraw(CDC* pDC)
{
	CFindzipDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);

	// TODO: add draw code for native data here
}

/////////////////////////////////////////////////////////////////////////////
// CFindzipView diagnostics

#ifdef _DEBUG
void CFindzipView::AssertValid() const
{
	CView::AssertValid();
}

void CFindzipView::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

CFindzipDoc* CFindzipView::GetDocument() // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CFindzipDoc)));
	return (CFindzipDoc*)m_pDocument;
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CFindzipView message handlers

int CFindzipView::OnCreate(LPCREATESTRUCT lpCreateStruct) 
{
	if (CView::OnCreate(lpCreateStruct) == -1)
		return -1;
	
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    CString strCommand;

    mapinfo.Do("Open Table \"States.tab\" ReadOnly Interactive");
    mapinfo.Do("Open Table \"us_zips.tab\" ReadOnly Interactive");

    strCommand.Format("Set Next Document Parent %lu Style 1  Map From States", (long)m_hWnd);
    mapinfo.Do(strCommand);
    m_lWindowID = atol(mapinfo.Eval("WindowID(0)"));
    strCommand.Format("WindowInfo(0, %u)", WIN_INFO_WND);
    m_hwndWindow = (HWND)atol(mapinfo.Eval(strCommand));
    m_bMapperInitialized=TRUE;

    // Disable the help subsystem - we don't support help in this application
    mapinfo.Do("Set Window Help Off");
    // Disable the <Add...> control in the Layer Control dialog box
    mapinfo.Do("Alter MapinfoDialog 1800 Control 12 Disable");
    // Reprogram the map's shortcut menu (right-click on map)
    mapinfo.Do("Create Menu \"MapshellShortcut\" ID 17 as \"&Layer Control...\" calling 801, \"Create &Thematic Map...\" calling 307, \"View &Entire Layer...\" calling 807");

    // Create our custom "Query" tool
    mapinfo.Do("Alter ButtonPad ID 3 Add ToolButton Calling OLE \"OnQueryPosition\" Cursor 128 DrawMode 34 ID 101");

    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
	return 0;
}

void CFindzipView::OnDestroy() 
{
	CView::OnDestroy();
	
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    if (m_hwndWindow) {
        ::DestroyWindow(m_hwndWindow);
        m_hwndWindow = NULL;
        m_lWindowID = 0L;
    }
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

void CFindzipView::OnInitialUpdate() 
{
    CString strCommand;

	CView::OnInitialUpdate();

    // ADDED FOR INTEGRATED MAPPING SUPPORT
    // Set mouse mode to grabber tool
    OnGrabber();
    // Reparent InfoTool window to be a child of this view
    strCommand.Format("Set Window Info Parent %u", m_hWnd);
    mapinfo.Do(strCommand);
    // For this sample app, make sure InfoTool never allows editing
    mapinfo.Do("Set Window Info ReadOnly");

    // Set the IDispatch pointer for MapInfo OLE callbacks in the Document class
	CFindzipDoc *pDoc = GetDocument();
    if (pDoc!=NULL) {
        pDoc->SetCallback();
    }
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

void CFindzipView::OnSize(UINT nType, int cx, int cy) 
{
	CView::OnSize(nType, cx, cy);
	
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    if (m_bMapperInitialized && cx > 0 && cy > 0) {
        ::MoveWindow(m_hwndWindow, 0, 0, cx, cy, TRUE); 
    }
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

BOOL CFindzipView::OnEraseBkgnd(CDC* pDC) 
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    // Once MapInfo has drawn the mapper window, don't allow background erases
    // to occur. This allows you to drag the infotool (or other reparented windows)
    // over the view window without having Windows erase underneath.
    // Other option is to set window styles to CLIP_CHILDREN
	if (!m_bMapperInitialized) {
		return CView::OnEraseBkgnd(pDC);
	}
	return FALSE;
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

/////////////////////////////////////////////////////////////////////////////
// CFindzipView menu message handlers
//   (Find Zip-Code menu item is handled by toolbar msg handler)
// ADDED FOR INTEGRATED MAPPING SUPPORT

void CFindzipView::OnUpdateFilePrintmap(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
    	
}
void CFindzipView::OnFilePrintmap() 
{
    mapinfo.Do("PrintWin");
}

void CFindzipView::OnUpdateMapLayercontrol(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnMapLayercontrol() 
{
	mapinfo.RunMenuCommand(801);
}

void CFindzipView::OnUpdateMapCreatetheme(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnMapCreatetheme() 
{
	mapinfo.RunMenuCommand(307);
}

void CFindzipView::OnUpdateMapViewentirelayer(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnMapViewentirelayer() 
{
	mapinfo.RunMenuCommand(807);
}

/////////////////////////////////////////////////////////////////////////////
// CFindzipView toolbar message handlers

void CFindzipView::OnUpdateGrabber(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_GRABBER);
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnGrabber() 
{
	// User selected the "Grabber" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_GRABBER) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(1702);
	} else {
		m_eMouseMode=MM_TOOLBAR_GRABBER;
		mapinfo.RunMenuCommand(1702);
	}
}

void CFindzipView::OnUpdateZoomin(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_ZOOMIN);
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnZoomin() 
{
	// User selected the "Zoomin" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_ZOOMIN) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(1702);
	} else {
		m_eMouseMode=MM_TOOLBAR_ZOOMIN;
		mapinfo.RunMenuCommand(1705);
	}
}

void CFindzipView::OnUpdateZoomout(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_ZOOMOUT);
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnZoomout() 
{
	// User selected the "Zoomout" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_ZOOMOUT) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(1702);
	} else {
		m_eMouseMode=MM_TOOLBAR_ZOOMOUT;
		mapinfo.RunMenuCommand(1706);
	}
}

void CFindzipView::OnUpdateInfotool(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_INFOTOOL);
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnInfotool() 
{
	// User selected the "Infotool" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_INFOTOOL) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(1702);
	} else {
		m_eMouseMode=MM_TOOLBAR_INFOTOOL;
		mapinfo.RunMenuCommand(1707);
	}
}

void CFindzipView::OnUpdateQuery(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_QUERY);
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnQuery() 
{
	// User selected the "Query Tool" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_QUERY) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(1702);
	} else {
		m_eMouseMode=MM_TOOLBAR_QUERY;
		mapinfo.Do("Run Menu Command ID 101");
	}
}

void CFindzipView::OnUpdateFindZip(CCmdUI* pCmdUI) 
{
	CFindzipDoc *pDoc = GetDocument();
	pCmdUI->Enable(pDoc!=NULL && m_bMapperInitialized);
}

void CFindzipView::OnFindZip() 
{
    CString strCommand;
    CFindZipDlg dlgZip;

    if (dlgZip.DoModal() == IDOK) {
        CString strZip = dlgZip.m_strZip;
        if (!strZip.IsEmpty()) {
            mapinfo.Do("Find Using US_ZIPS(Zip_code)");
            strCommand.Format("Find \"%s\"",(LPCTSTR)strZip);
            mapinfo.Do(strCommand);
            if (atoi(mapinfo.Eval("CommandInfo(3)")) >= 1) {
                strCommand.Format("Set Map Window %lu Center(CommandInfo(1), CommandInfo(2)) Zoom 500", m_lWindowID);
                mapinfo.Do(strCommand);
            }
        }
    }
}

/////////////////////////////////////////////////////////////////////////////
// CFindzipView automation message handler(s)

void CFindzipView::OnWindowContentsChanged(void)
{
    static long lLegendID = 0L;

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
            
    if (bHasThematic && lLegendID == 0L) {
        // create legend
        strCommand.Format("Set Next Document Parent WindowInfo(%lu,%d) Style 1",m_lWindowID,WIN_INFO_WND);
        mapinfo.Do(strCommand);
        strCommand.Format("Create Legend From Window %lu",m_lWindowID);
        mapinfo.Do(strCommand);
    	lLegendID = atol(mapinfo.Eval("WindowID(0)"));
    }
    else if (!bHasThematic && lLegendID != 0L) {
    	// destroy legend
        strCommand.Format("Close Window %lu", lLegendID);
		mapinfo.Do(strCommand);
    	lLegendID = 0l;
    }
}
// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
