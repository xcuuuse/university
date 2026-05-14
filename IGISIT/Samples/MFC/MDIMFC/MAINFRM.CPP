// mainfrm.cpp : implementation of the CMainFrame class
//

#include "stdafx.h"
#include "mdimap.h"

#include "mainfrm.h"
#include "mdimadoc.h"
#include "mdimavw.h"

#include "mapinfow.h"       // ADDED FOR INTEGRATED MAPPING SUPPORT
#include "ovvwdlg.h"        // ADDED FOR INTEGRATED MAPPING SUPPORT OverView dialog

#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CMainFrame

IMPLEMENT_DYNAMIC(CMainFrame, CMDIFrameWnd)

BEGIN_MESSAGE_MAP(CMainFrame, CMDIFrameWnd)
	//{{AFX_MSG_MAP(CMainFrame)
	ON_WM_CREATE()
    // ADDED FOR INTEGRATED MAPPING SUPPORT
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_GRABBER, OnUpdateGrabber)
	ON_COMMAND(ID_TOOLBAR_GRABBER, OnGrabber)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_ZOOMIN, OnUpdateZoomin)
	ON_COMMAND(ID_TOOLBAR_ZOOMIN, OnZoomin)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_ZOOMOUT, OnUpdateZoomout)
	ON_COMMAND(ID_TOOLBAR_ZOOMOUT, OnZoomout)
	ON_UPDATE_COMMAND_UI(ID_TOOLBAR_INFOTOOL, OnUpdateInfotool)
	ON_COMMAND(ID_TOOLBAR_INFOTOOL, OnInfotool)
	ON_COMMAND(ID_MAP_OVERVIEW, OnMapOverview)
    ON_MESSAGE(WM_OVERVIEW_MESSAGE, OnOverviewMessage)
	ON_UPDATE_COMMAND_UI(ID_MAP_OVERVIEW, OnUpdateMapOverview)
	ON_WM_CLOSE()
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

BEGIN_DISPATCH_MAP(CMainFrame, CMDIFrameWnd)
	//{{AFX_DISPATCH_MAP(CMainFrame)
    // ADDED FOR INTEGRATED MAPPING SUPPORT
	DISP_FUNCTION(CMainFrame, "WindowContentsChanged", WindowContentsChanged, VT_ERROR, VTS_I4)
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
	//}}AFX_DISPATCH_MAP
END_DISPATCH_MAP()


/////////////////////////////////////////////////////////////////////////////
// arrays of IDs used to initialize control bars
	
// toolbar buttons - IDs are command buttons
static UINT BASED_CODE buttons[] =
{
	// same order as in the bitmap 'toolbar.bmp'
	ID_FILE_OPEN,
    // ADDED FOR INTEGRATED MAPPING SUPPORT
		ID_SEPARATOR,
    ID_TOOLBAR_GRABBER,
    ID_TOOLBAR_ZOOMIN,
    ID_TOOLBAR_ZOOMOUT,
		ID_SEPARATOR,
    ID_TOOLBAR_INFOTOOL,
	ID_APP_ABOUT,
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
};

static UINT BASED_CODE indicators[] =
{
	ID_SEPARATOR,           // status line indicator
	ID_INDICATOR_CAPS,
	ID_INDICATOR_NUM,
	ID_INDICATOR_SCRL,
};

/////////////////////////////////////////////////////////////////////////////
// CMainFrame construction/destruction

CMainFrame::CMainFrame()
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
   	m_eMouseMode = MM_DEFAULT;
    m_pOvDlg = NULL;

	EnableAutomation();
	AfxOleLockApp();
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

CMainFrame::~CMainFrame()
{
}

void CMainFrame::OnClose() 
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    // Note: AfxOleUnlockApp must be called before destructor. This can be done in
    // OnClose.
	mapinfo.SetCallback(NULL);
	AfxOleUnlockApp();
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
	CMDIFrameWnd::OnClose();
}

int CMainFrame::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
	if (CMDIFrameWnd::OnCreate(lpCreateStruct) == -1)
		return -1;
	
	if (!m_wndToolBar.Create(this) ||
		!m_wndToolBar.LoadBitmap(IDR_MAINFRAME) ||
		!m_wndToolBar.SetButtons(buttons,
		  sizeof(buttons)/sizeof(UINT)))
	{
		TRACE0("Failed to create toolbar\n");
		return -1;      // fail to create
	}

	if (!m_wndStatusBar.Create(this) ||
		!m_wndStatusBar.SetIndicators(indicators,
		  sizeof(indicators)/sizeof(UINT)))
	{
		TRACE0("Failed to create status bar\n");
		return -1;      // fail to create
	}

	// TODO: Delete these three lines if you don't want the toolbar to
	//  be dockable
	m_wndToolBar.EnableDocking(CBRS_ALIGN_ANY);
	EnableDocking(CBRS_ALIGN_ANY);
	DockControlBar(&m_wndToolBar);

	// TODO: Remove this if you don't want tool tips
	m_wndToolBar.SetBarStyle(m_wndToolBar.GetBarStyle() |
		CBRS_TOOLTIPS | CBRS_FLYBY);

    // ADDED FOR INTEGRATED MAPPING SUPPORT
    // Do one-time-only initialization
    CString strCommand;

    strCommand.Format("Set Application Window %lu", (long)m_hWnd);
    mapinfo.Do(strCommand);

    // Reparent InfoTool window to be a child of the mainframe
    strCommand.Format("Set Window Info Parent %lu", (long)m_hWnd);
    mapinfo.Do(strCommand);
    // For this sample app, make sure InfoTool never allows editing
    mapinfo.Do("Set Window Info ReadOnly");

    // Disable the help subsystem - we don't support help in this application
    mapinfo.Do("Set Window Help Off");
    // Disable the <Add...> control in the Layer Control dialog box
    mapinfo.Do("Alter MapinfoDialog 1800 Control 12 Disable");
    // Reprogram the map's shortcut menu (right-click on map)
    mapinfo.Do("Create Menu \"MapshellShortcut\" ID 17 as \"&Layer Control...\" calling 801, \"Create &Thematic Map...\" calling 307, \"View &Entire Layer...\" calling 807");

    // Set up global object frame for overview
    mapinfo.Do("Dim frame as Object");

    // Sets the MapInfo callback dispatch pointer.
	mapinfo.SetCallback(this->GetIDispatch(FALSE));

    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

	return 0;
}

/////////////////////////////////////////////////////////////////////////////
// CMainFrame diagnostics

#ifdef _DEBUG
void CMainFrame::AssertValid() const
{
	CMDIFrameWnd::AssertValid();
}

void CMainFrame::Dump(CDumpContext& dc) const
{
	CMDIFrameWnd::Dump(dc);
}

#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CMainFrame message handlers
// All Message Handles from here down ADDED FOR INTEGRATED MAPPING SUPPORT

void CMainFrame::OnUpdateGrabber(CCmdUI* pCmdUI) 
{
    BOOL bMaximized = FALSE;
    CMDIChildWnd* pActiveWnd = MDIGetActive(&bMaximized);
    CMdimapView *pActiveView = NULL;

    if (pActiveWnd) {
        pActiveView = (CMdimapView *)pActiveWnd->GetActiveView();
    }
	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_GRABBER);
	pCmdUI->Enable(pActiveView != NULL && pActiveView->Mapper());
}

void CMainFrame::OnGrabber() 
{
	// User selected the "Grabber" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_GRABBER) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(M_TOOLS_DEFAULT);
	} else {
		m_eMouseMode=MM_TOOLBAR_GRABBER;
		mapinfo.RunMenuCommand(M_TOOLS_RECENTER);
	}
}

void CMainFrame::OnUpdateZoomin(CCmdUI* pCmdUI) 
{
    BOOL bMaximized = FALSE;
    CMDIChildWnd* pActiveWnd = MDIGetActive(&bMaximized);
    CMdimapView *pActiveView = NULL;

    if (pActiveWnd) {
        pActiveView = (CMdimapView *)pActiveWnd->GetActiveView();
    }

	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_ZOOMIN);
	pCmdUI->Enable(pActiveView != NULL && pActiveView->Mapper());
}

void CMainFrame::OnZoomin() 
{
	// User selected the "Zoomin" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_ZOOMIN) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(M_TOOLS_DEFAULT);
	} else {
		m_eMouseMode=MM_TOOLBAR_ZOOMIN;
		mapinfo.RunMenuCommand(M_TOOLS_EXPAND);
	}
}

void CMainFrame::OnUpdateZoomout(CCmdUI* pCmdUI) 
{
    BOOL bMaximized = FALSE;
    CMDIChildWnd* pActiveWnd = MDIGetActive(&bMaximized);
    CMdimapView *pActiveView = NULL;

    if (pActiveWnd) {
        pActiveView = (CMdimapView *)pActiveWnd->GetActiveView();
    }

	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_ZOOMOUT);
	pCmdUI->Enable(pActiveView != NULL && pActiveView->Mapper());
}

void CMainFrame::OnZoomout() 
{
	// User selected the "Zoomout" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_ZOOMOUT) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(M_TOOLS_DEFAULT);
	} else {
		m_eMouseMode=MM_TOOLBAR_ZOOMOUT;
		mapinfo.RunMenuCommand(M_TOOLS_SHRINK);
	}
}

void CMainFrame::OnUpdateInfotool(CCmdUI* pCmdUI) 
{
    BOOL bMaximized = FALSE;
    CMDIChildWnd* pActiveWnd = MDIGetActive(&bMaximized);
    CMdimapView *pActiveView = NULL;

    if (pActiveWnd) {
        pActiveView = (CMdimapView *)pActiveWnd->GetActiveView();
    }

	pCmdUI->SetRadio(m_eMouseMode==MM_TOOLBAR_INFOTOOL);
	pCmdUI->Enable(pActiveView != NULL && (pActiveView->Browser() || pActiveView->Mapper()) );
}

void CMainFrame::OnInfotool() 
{
	// User selected the "Infotool" button on the toolbar;
	// toggle the current mouse mode
	if(m_eMouseMode==MM_TOOLBAR_INFOTOOL) {
		m_eMouseMode=MM_DEFAULT;
		mapinfo.RunMenuCommand(M_TOOLS_DEFAULT);
	} else {
		m_eMouseMode=MM_TOOLBAR_INFOTOOL;
		mapinfo.RunMenuCommand(M_TOOLS_PNT_QUERY);
	}
}

void CMainFrame::OnUpdateMapOverview(CCmdUI* pCmdUI) 
{
    // This item is always enabled, but if there is no overview
    // dialog, make sure the item has the correct text.
    if (!m_pOvDlg) {
        GetMenu()->ModifyMenu(ID_MAP_OVERVIEW, MF_BYCOMMAND|MF_STRING, ID_MAP_OVERVIEW, "Overview...");
    }
}

void CMainFrame::OnMapOverview() 
{
    BOOL bMaximized = FALSE;
    CMDIChildWnd* pActiveWnd = NULL;
    CMdimapView *pActiveView = NULL;
    CMdimapDoc *pActiveDoc = NULL;

    pActiveWnd = MDIGetActive(&bMaximized);
    if (!pActiveWnd) {
        return;
    }
    pActiveView = (CMdimapView *)pActiveWnd->GetActiveView();
    pActiveDoc = (CMdimapDoc *)pActiveWnd->GetActiveDocument();
    if (!pActiveDoc || !pActiveView) {
        return;
    }

    // We want to make the overview mapper track the current mapper. 
    // If the current "front" window isn't a mapper, advise the user.
    CString strCommand;
    strCommand.Format("WindowInfo(FrontWindow(), %d)", WIN_INFO_TYPE);
    if (atoi(mapinfo.Eval(strCommand)) != WIN_MAPPER) {
        AfxMessageBox("You must make a Map window the active\nwindow before you choose OverView.");
        return;
    }

    CString strTitle;
    pActiveWnd->GetWindowText(strTitle);

    long lMapperId = pActiveView->WindowId();
    ASSERT(lMapperId > 0L); 

    GetMenu()->ModifyMenu(ID_MAP_OVERVIEW, MF_BYCOMMAND|MF_STRING, ID_MAP_OVERVIEW, "Update Overview");

    if (!m_pOvDlg) {

        // Initialize new dialog with doc name, view title, and active mapper ID. 
        // Note that dialog is created with WS_CLIPCHILDREN window style set.
        m_pOvDlg = new COverviewDlg(pActiveDoc->GetAlias(), strTitle, lMapperId);
        if (!m_pOvDlg) {
            AfxMessageBox("Unable to create Overview window!");
            return;
        }

        // Show modeless dialog
        m_pOvDlg->Create(IDD_OVERVIEW, this);
    }
    else {
        // Update existing dialog window.
        if (!m_pOvDlg->IsWindowVisible()) {
            m_pOvDlg->ShowWindow(SW_SHOW);
        }
        m_pOvDlg->Update(pActiveDoc->GetAlias(), strTitle, lMapperId);
    }

}

LONG CMainFrame::OnOverviewMessage(WPARAM wParam, LPARAM lParam)
{

    switch(wParam) {
        case 0:
            // called after overview dialog destroyed
            m_pOvDlg = NULL;
            // Rename the menu item
            GetMenu()->ModifyMenu(ID_MAP_OVERVIEW, MF_BYCOMMAND|MF_STRING, ID_MAP_OVERVIEW, "Overview...");
            break;
        default:
            break;
    }
    return 0L;         
}

void CMainFrame::ClearOverview(long lMapperId)
{
    if (m_pOvDlg) {
        m_pOvDlg->ClearContents(lMapperId);
    }
}

void CMainFrame::UpdateOverview(long lMapperId)
{
    ASSERT(lMapperId > 0L);

    if (m_pOvDlg) {

        BOOL bMaximized = FALSE;
        CMDIChildWnd* pActiveWnd = MDIGetActive(&bMaximized);
        CMdimapView *pActiveView = NULL;
        CMdimapDoc *pActiveDoc = NULL;

        if (!pActiveWnd) {
            return;
        }
        pActiveView = (CMdimapView *)pActiveWnd->GetActiveView();
        pActiveDoc = (CMdimapDoc *)pActiveWnd->GetActiveDocument();
        if (!pActiveDoc || !pActiveView) {
            return;
        }
        // Update overview for active mapper only
        if (pActiveView->Mapper() && lMapperId == pActiveView->WindowId()) {
            CString strTitle;
            pActiveWnd->GetWindowText(strTitle);
         
            // Update existing dialog window.
            if (!m_pOvDlg->IsWindowVisible()) {
                m_pOvDlg->ShowWindow(SW_SHOW);
            }
            m_pOvDlg->Update(lMapperId);
        }
    }
}

void CMainFrame::CheckDestroyOverview(void)
{
    if (m_pOvDlg) {
        BOOL bMaximized = FALSE;
        CMDIChildWnd* pActiveWnd = MDIGetActive(&bMaximized);
        if (!pActiveWnd) {
            m_pOvDlg->DestroyWindow();
            m_pOvDlg = NULL;
        }
    }
}

long CMainFrame::OverviewMapId(void)
{
    if (m_pOvDlg) {
        return m_pOvDlg->MapperId();
    }
    return 0L;
}

/////////////////////////////////////////////////////////////////////////////
// Automation methods - (callbacks from MapInfo) are attached to the 
// CMainFrame class
SCODE CMainFrame::WindowContentsChanged(long lWindowId) 
{
    BOOL bMaximized = FALSE;
    CMDIChildWnd* pActiveWnd = MDIGetActive(&bMaximized);
    if (pActiveWnd) {

        CMdimapView *pActiveView = (CMdimapView *)pActiveWnd->GetActiveView();
        if (lWindowId == pActiveView->WindowId()) { 
            CMdimapDoc *pActiveDoc = (CMdimapDoc *)pActiveWnd->GetActiveDocument();
            if (pActiveDoc) {
                pActiveDoc->UpdateAllViews(NULL, lWindowId);
                UpdateOverview(lWindowId);
            }
        }
    }

	return S_OK;
}

// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
