// ovvwdlg.cpp : implementation file
// Entire File ADDED FOR INTEGRATED MAPPING SUPPORT sample app
//

#include "stdafx.h"
#include "mdimap.h"
#include "ovvwdlg.h"
#include "mapinfow.h"

#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// COverviewDlg dialog

COverviewDlg::COverviewDlg(CWnd* pParent /*=NULL*/)
	: CDialog(COverviewDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(COverviewDlg)
		// NOTE: the ClassWizard will add member initialization here
	//}}AFX_DATA_INIT
    m_strTableName = "";
    m_strWndTitle = "";
    m_lWindowID = 0L;
    m_hwndWindow = NULL;
    m_bInitialized = FALSE;
    m_lMapWindowID = 0L;
    m_dMapZoom = 0.0;
    m_dMapCx = 0.0;
    m_dMapCy = 0.0;
}

COverviewDlg::COverviewDlg(CString strTableName, CString strWndTitle, long lMapWindowID, CWnd* pParent /*=NULL*/)
	: CDialog(COverviewDlg::IDD, pParent)
{
    m_strTableName = strTableName;
    m_strWndTitle = strWndTitle;
    m_lWindowID = 0L;
    m_hwndWindow = NULL;
    m_bInitialized = FALSE;
    m_lMapWindowID = lMapWindowID;
    m_dMapZoom = 0.0;
    m_dMapCx = 0.0;
    m_dMapCy = 0.0;
}

void COverviewDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(COverviewDlg)
		// NOTE: the ClassWizard will add DDX and DDV calls here
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(COverviewDlg, CDialog)
	//{{AFX_MSG_MAP(COverviewDlg)
   	ON_MESSAGE(WM_CREATE_OVERVIEW, OnCreateOverview)
	ON_WM_PAINT()
	ON_WM_SIZE()
	ON_WM_CLOSE()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()


/////////////////////////////////////////////////////////////////////////////
// COverviewDlg message handlers

BOOL COverviewDlg::OnInitDialog() 
{
	CDialog::OnInitDialog();
	
    SetCaption();

	return TRUE;  // return TRUE unless you set the focus to a control
	              // EXCEPTION: OCX Property Pages should return FALSE
}

BOOL COverviewDlg::Update(CString strTableName, CString strWndTitle, long lMapWindowID)
{
    TRACE("COverviewDlg::Update\n");

    // Updates by creating new mapper window and object frame
    if (m_lMapWindowID != lMapWindowID) {
        m_strTableName = strTableName;
        m_strWndTitle = strWndTitle;
        m_lMapWindowID = lMapWindowID;
        SetCaption();
        // Force our own update event to occur
        m_bInitialized = FALSE;
        Invalidate();
    }
	return TRUE; 
}

BOOL COverviewDlg::Update(long lMapWindowID)
{
    TRACE("COverviewDlg::Update\n");

    // Updates existing mapper window with new object frame
    if (m_lMapWindowID != lMapWindowID) {
        return FALSE;
    }
    else {
        CString strCommand;
        strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MINX); 
        double dX1 = atof(mapinfo.Eval(strCommand));
        strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MINY); 
        double dY1 = atof(mapinfo.Eval(strCommand));
        strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MAXX); 
        double dX2 = atof(mapinfo.Eval(strCommand));
        strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MAXY); 
        double dY2 = atof(mapinfo.Eval(strCommand));
        NewFrame(dX1, dY1, dX2, dY2); 
    }
	return TRUE; 
}

void COverviewDlg::SetCaption()
{
    TRACE("COverviewDlg::SetCaption\n");

    // Modify caption title so it looks nice
    CString strNew;
    strNew.Format("Overview - %s", (LPCTSTR)m_strWndTitle);
	SetWindowText(strNew);
}

void COverviewDlg::OnPaint() 
{
    TRACE("COverviewDlg::OnPaint\n");

	CPaintDC dc(this); // device context for painting

    // We can't make external calls during syncronous message handlers,
    // so instead, we post our own update message. The message handler
    // for WM_CREATE_OVERVIEW takes care of making the necessary calls
    // to MapInfo in order to create the mapper window.
    if (!m_bInitialized) {
        PostMessage(WM_CREATE_OVERVIEW, 0, 0);
    }

	// Do not call CDialog::OnPaint() for painting messages
}

int COverviewDlg::CreateMapOverview()
{
    TRACE("COverviewDlg::CreateMapOverview\n");

    CString strCommand;

    if (m_strTableName.IsEmpty() || m_bInitialized) {
        return 0;
    }

    // Close existing mapper window, if any
    if (m_hwndWindow) {
        strCommand.Format("Close Window %lu", m_lWindowID); 
        mapinfo.Do(strCommand);
        m_hwndWindow = NULL;
        m_lWindowID = 0L;
    }

    // Create new one, reparented to this dialog
    strCommand.Format("Set Next Document Parent %lu Style 1 Map From %s", (long)m_hWnd, (LPCTSTR)m_strTableName);
    mapinfo.Do(strCommand);
    m_lWindowID = atol(mapinfo.Eval("WindowID(0)"));
    strCommand.Format("WindowInfo(0, %u)", WIN_INFO_WND);
    m_hwndWindow = (HWND)atol(mapinfo.Eval(strCommand));
    m_bInitialized = TRUE;

    // For the sake of making it act as an "overview", we'll set up the zoom
    // of the overview map to fit its window, and center it at the same spot as 
    // the original mapper. Original mapper's saved zoom for future reference.
    GetMDIChildMapperInfo();
     
    strCommand.Format("Set Map Window %ld Zoom Entire Center(%lf, %lf)", m_lWindowID, m_dMapCx, m_dMapCy);
    mapinfo.Do(strCommand);

    // Now draw a rectangle on the OverView mapper showing the extents of  
    // the original mapper.  We'll use the MapperInfo function  
    // to determine the extents of the mapper.  Then we'll call 
    // the procedure NewFrame to actually draw the red rectangle.

    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MINX); 
    double dX1 = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MINY); 
    double dY1 = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MAXX); 
    double dX2 = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_MAXY); 
    double dY2 = atof(mapinfo.Eval(strCommand));
    NewFrame(dX1, dY1, dX2, dY2);

    return 1;
}

void COverviewDlg::OnSize(UINT nType, int cx, int cy) 
{
    TRACE("COverviewDlg::OnSize %d %d\n", cx, cy);

	CDialog::OnSize(nType, cx, cy);
	
    if (m_bInitialized && cx > 0 && cy > 0) {
        ::MoveWindow(m_hwndWindow, 0, 0, cx, cy, TRUE); 
    }
}

LONG COverviewDlg::OnCreateOverview(WPARAM wParam, LPARAM /* lParam */) 
{
    TRACE("COverviewDlg::OnCreateOverview\n");
    return (long) CreateMapOverview();
}

void COverviewDlg::OnClose() 
{
    // This message is sent to the parent so it may update the menu item
    // and update the parent's Overview dialog member pointer.
    GetParent()->PostMessage(WM_OVERVIEW_MESSAGE, 0, 0);
    DestroyWindow();	
}

void COverviewDlg::PostNcDestroy() 
{
    delete this;
}

BOOL COverviewDlg::ClearContents(long lMapperId)
{
    if (m_lMapWindowID != lMapperId) {
        return FALSE;
    }

    TRACE("COverviewDlg::ClearContents\n");
    m_strTableName.Empty();
    m_strWndTitle.Empty();
    SetWindowText("Overview");

    CString strCommand;
    strCommand.Format("Close Window %ld", m_lWindowID);
    mapinfo.Do(strCommand);
     
    m_hwndWindow = NULL;
    m_lWindowID = 0L;
    m_lMapWindowID = 0L;
    m_dMapZoom = 0.0;
    m_dMapCx = 0.0;
    m_dMapCy = 0.0;
    m_bInitialized = FALSE;
    Invalidate();
    return TRUE;
}

void COverviewDlg::GetMDIChildMapperInfo(void)
{
    TRACE("COverviewDlg::GetMDIChildMapperInfo\n");

    CString strCommand;

    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_ZOOM);
    m_dMapZoom = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_CENTERX);
    m_dMapCx = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_CENTERY);
    m_dMapCy = atof(mapinfo.Eval(strCommand));
}

void COverviewDlg::NewFrame(double dX1, double dY1, double dX2, double dY2) 
{
    TRACE("COverviewDlg::NewFrame\n");

    CString strCommand;

    // This procedure draws a hollow rectangle to the OverView mapper.
    // The rectangle indicates the current position and extents
    // of the other mapper window which we're overseeing. 
    //
    // But we need to do more than just create the rectangle object.
    // If the "current extents" rectangle doesn't fit within our 
    // OverView mapper, we'll recenter the overview mapper.
     
    double dOld_minx, dOld_miny, dOld_maxx, dOld_maxy;  
    double dMap_zoom, dOv_zoom;
    BOOL bShrink = FALSE;

    // Now decide whether the new extents rectangle will fit within the current 
    // overview mapper.  If not, we'll recenter and possibly re-zoom the  
    // overview mapper. 
    strCommand.Format("MapperInfo(%ld, %d)", m_lMapWindowID, MAPPER_INFO_ZOOM);  
    dMap_zoom = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lWindowID, MAPPER_INFO_ZOOM);
    dOv_zoom = atof(mapinfo.Eval(strCommand));
      
    if (dMap_zoom >= (dOv_zoom / 2.0)) {  
        dOv_zoom = 2.0 * dMap_zoom;     // Zoom overview out, if necessary
        bShrink = TRUE;
    }

    if ((dMap_zoom * 30.0) < dOv_zoom) {
        dOv_zoom = 10.0 * dMap_zoom;    // Zoom overview in, if necessary
        bShrink = TRUE;                    
    }

    strCommand.Format("MapperInfo(%ld, %d)", m_lWindowID, MAPPER_INFO_MINX);
    dOld_minx = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lWindowID, MAPPER_INFO_MINY);
    dOld_miny = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lWindowID, MAPPER_INFO_MAXX);
    dOld_maxx = atof(mapinfo.Eval(strCommand));
    strCommand.Format("MapperInfo(%ld, %d)", m_lWindowID, MAPPER_INFO_MAXY);
    dOld_maxy = atof(mapinfo.Eval(strCommand));
     
    if (dX1 < dOld_minx || dX1 > dOld_maxx || 
        dY1 < dOld_miny || dY1 > dOld_maxy ||      
        dX2 < dOld_minx || dX2 > dOld_maxx || 
        dY2 < dOld_miny || dY2 > dOld_maxy || bShrink) {
        strCommand.Format("Set Map Window %ld Center ((%lf+%lf)/2, (%lf+%lf)/2) Zoom %lf",
            m_lWindowID, dX1, dX2, dY1, dY2, dOv_zoom);
        mapinfo.Do(strCommand);
    }   

    // Create new extents rectangle; store it in a variable for now.
    // Variable "frame" was declared when the main App frame was created.

    strCommand.Format("Create Region Into Variable frame 1 5");
    CString strTmp;
    strTmp.Format(" (%lf, %lf) (%lf, %lf) (%lf, %lf) (%lf, %lf) (%lf, %lf)", 
                     dX1, dY1, dX1, dY2, dX2, dY2, dX2, dY1, dX1, dY1);
    strCommand += strTmp;
    strCommand += " Pen MakePen(1, 2, RGB(255, 0, 0)) Brush MakeBrush(1, 0, 0)";               
    mapinfo.Do(strCommand);

    // Insert the newly created extents rectangle. If the cosmetic layer
    // contains one object, that object must be the old extents rectangle; 
    // in this case, we can replace the old rectangle with the new rectangle  
    // through the Update statement.  (This is nice, because there's only one
    // screen redraw when you do a simple "UpDate").  

    // BUT, if the cosmetic layer has multiple objects, the user must have 
    // drawn a label or something, and we won't know which object is the 
    // old extents rectangle. In that case, we'll have to just erase the 
    // entire cosmetic layer, and then add the new extents rectangle through 
    // the Insert statement.  (This is not quite as nice, because there 
    // are 2 screen redraws when you do a "Delete" followed by an "Insert".)

    strCommand.Format("WindowInfo(%ld, %d)", m_lWindowID, WIN_INFO_TABLE);  
    CString strCosmetic = mapinfo.Eval(strCommand);

    strCommand.Format("TableInfo(%s, %d)", (LPCTSTR)strCosmetic, TAB_INFO_NROWS);
    if (atoi(mapinfo.Eval(strCommand)) == 1 ) {
        strCommand.Format("Update %s  Set obj = frame", (LPCTSTR)strCosmetic);
        mapinfo.Do(strCommand);
    }
    else {
        strCommand.Format("Delete From %s Insert Into %s (obj) Values (frame)", 
            (LPCTSTR)strCosmetic, (LPCTSTR)strCosmetic);
        mapinfo.Do(strCommand);
    }
        
}
