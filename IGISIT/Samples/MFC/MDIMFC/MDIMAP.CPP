// mdimap.cpp : Defines the class behaviors for the application.
//

#include "stdafx.h"
#include "mdimap.h"

#include "mainfrm.h"
#include "mdimadoc.h"
#include "mdimavw.h"
#include "ovvwdlg.h"
#include "mapinfow.h"       // ADDED FOR INTEGRATED MAPPING SUPPORT

#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CMdimapApp

BEGIN_MESSAGE_MAP(CMdimapApp, CWinApp)
	//{{AFX_MSG_MAP(CMdimapApp)
	ON_COMMAND(ID_APP_ABOUT, OnAppAbout)
	ON_COMMAND(ID_FILE_OPEN, OnFileOpen)
	//}}AFX_MSG_MAP
	// Standard file based document commands
	ON_COMMAND(ID_FILE_NEW, CWinApp::OnFileNew)
	ON_COMMAND(ID_FILE_OPEN, CWinApp::OnFileOpen)
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CMdimapApp construction

CMdimapApp::CMdimapApp()
{
	// Place all significant initialization in InitInstance
}

/////////////////////////////////////////////////////////////////////////////
// The one and only CMdimapApp object

CMdimapApp theApp;

// This identifier was generated to be statistically unique for your app.
// You may change it if you prefer to choose a specific identifier.
static const CLSID BASED_CODE clsid =
{ 0xae8b3fc0, 0xf801, 0x11ce, { 0xbd, 0x29, 0x0, 0xaa, 0x0, 0x59, 0x4a, 0xd7 } };

/////////////////////////////////////////////////////////////////////////////
// ADDED FOR INTEGRATED MAPPING SUPPORT: The one and only DMapInfo object

DMapInfo mapinfo;

/////////////////////////////////////////////////////////////////////////////
// CMdimapApp initialization

BOOL CMdimapApp::InitInstance()
{
	// Initialize OLE libraries
	if (!AfxOleInit())
	{
		AfxMessageBox(IDP_OLE_INIT_FAILED);
		return FALSE;
	}

    // ADDED FOR INTEGRATED MAPPING SUPPORT
    if (!mapinfo.CreateDispatch("MapInfo.Application")) {
        AfxMessageBox("Failed to create MapInfo dispatch class!");
        //::MessageBox(0, mapinfo.GetFullName(), "Amazing!", MB_OK);
        return FALSE;
    }
    // END OF ADDITION FOR INTEGRATED MAPPING SUPPORT

	// Standard initialization
	// If you are not using these features and wish to reduce the size
	//  of your final executable, you should remove from the following
	//  the specific initialization routines you do not need.

	Enable3dControls();

	LoadStdProfileSettings();  // Load standard INI file options (including MRU)

	// Register the application's document templates.  Document templates
	//  serve as the connection between documents, frame windows and views.

	CMultiDocTemplate* pDocTemplate;
	pDocTemplate = new CMultiDocTemplate(
		IDR_MDIMAPTYPE,
		RUNTIME_CLASS(CMdimapDoc),
		RUNTIME_CLASS(CMDIChildWnd),          // standard MDI child frame
		RUNTIME_CLASS(CMdimapView));
	AddDocTemplate(pDocTemplate);

	// Connect the COleTemplateServer to the document template.
	//  The COleTemplateServer creates new documents on behalf
	//  of requesting OLE containers by using information
	//  specified in the document template.
	m_server.ConnectTemplate(clsid, pDocTemplate, FALSE);

	// Register all OLE server factories as running.  This enables the
	//  OLE libraries to create objects from other applications.
	COleTemplateServer::RegisterAll();
		// Note: MDI applications register all server objects without regard
		//  to the /Embedding or /Automation on the command line.

	// create main MDI Frame window
	CMainFrame* pMainFrame = new CMainFrame;
	if (!pMainFrame->LoadFrame(IDR_MAINFRAME))
		return FALSE;
	m_pMainWnd = pMainFrame;

	// Parse the command line to see if launched as OLE server
	if (RunEmbedded() || RunAutomated())
	{
		// Application was run with /Embedding or /Automation.  Don't show the
		//  main window in this case.
		return TRUE;
	}

	// When a server application is launched stand-alone, it is a good idea
	//  to update the system registry in case it has been damaged.
	m_server.UpdateRegistry(OAT_DISPATCH_OBJECT);
	COleObjectFactory::UpdateRegistryAll();

	// create a new (empty) document
    // Next API call commented out FOR INTEGRATED MAPPING SUPPORT. Uncomment if your app
    // wishes to create an empty document.
	// OnFileNew();

	if (m_lpCmdLine[0] != '\0')
	{
		// TODO: add command line processing here
	}

	// The main window has been initialized, so show and update it.
	pMainFrame->ShowWindow(m_nCmdShow);
	pMainFrame->UpdateWindow();

	return TRUE;
}

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

// Implementation
protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//{{AFX_MSG(CAboutDlg)
		// No message handlers
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

// App command to run the dialog
void CMdimapApp::OnAppAbout()
{
	CAboutDlg aboutDlg;
	aboutDlg.DoModal();
}

/////////////////////////////////////////////////////////////////////////////
// Routines from here down ADDED FOR INTEGRATED MAPPING SUPPORT
int CMdimapApp::ExitInstance() 
{
	mapinfo.ReleaseDispatch();
	return CWinApp::ExitInstance();
}

/////////////////////////////////////////////////////////////////////////////
// CMdimapApp Global functions - make it easier to get our application 
// object.

CMdimapApp *GetOurApp(void)
{
	return((CMdimapApp *)AfxGetApp());
}

/////////////////////////////////////////////////////////////////////////////
// CMdimapApp commands

void CMdimapApp::OnFileOpen() 
{
	// prompt the user
	CFileDialog dlgFile(TRUE, "tab", NULL, OFN_FILEMUSTEXIST|OFN_HIDEREADONLY,
	                "MapInfo Tables (*.tab)|*.tab||", NULL);

    // fill in ofn structure
    CString strFile;
	dlgFile.m_ofn.lpstrTitle = "Open MapInfo Table";
	dlgFile.m_ofn.lpstrFile = strFile.GetBuffer(_MAX_PATH);
	dlgFile.m_ofn.nMaxFile = _MAX_PATH;

    // put up dialog and do post modal processing
	BOOL bResult = dlgFile.DoModal() == IDOK ? TRUE : FALSE;
	strFile.ReleaseBuffer();

    if (bResult) {
	    OpenDocumentFile(strFile);
    }
		// if returns NULL, the user has already been alerted
}

void CMdimapApp::ClearOverview(long lMapperId)
{
    if (m_pMainWnd != NULL) {
        ((CMainFrame *)m_pMainWnd)->ClearOverview(lMapperId);
    }
}

int CMdimapApp::MouseMode(void)
{
    if (m_pMainWnd != NULL) {
        return ((CMainFrame *)m_pMainWnd)->MouseMode();
    }
    return -1;
}

void CMdimapApp::UpdateOverview(long lMapperId)
{
    if (m_pMainWnd != NULL) {
        ((CMainFrame *)m_pMainWnd)->UpdateOverview(lMapperId);
    }
}

void CMdimapApp::PostOverviewUpdate(long lMapperId)
{
    if (m_pMainWnd != NULL) {
        ((CMainFrame *)m_pMainWnd)->PostMessage(WM_OVERVIEW_MESSAGE, 1, lMapperId);
    }
}

void CMdimapApp::CheckDestroyOverview(void)
{
    if (m_pMainWnd != NULL) {
        ((CMainFrame *)m_pMainWnd)->CheckDestroyOverview();
    }
}

long CMdimapApp::OverviewMapId(void)
{
    if (m_pMainWnd != NULL) {
        return ((CMainFrame *)m_pMainWnd)->OverviewMapId();
    }
    return 0L;
}

// END OF ADDITION FOR INTEGRATED MAPPING SUPPORT


