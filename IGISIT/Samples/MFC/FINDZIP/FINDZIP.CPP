// findzip.cpp : Defines the class behaviors for the application.
//

#include "stdafx.h"
#include "findzip.h"

#include "mainfrm.h"
#include "findzdoc.h"
#include "findzvw.h"
#include "mapinfow.h"        // ADDED FOR INTEGRATED MAPPING SUPPORT


#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CFindzipApp

BEGIN_MESSAGE_MAP(CFindzipApp, CWinApp)
	//{{AFX_MSG_MAP(CFindzipApp)
	ON_COMMAND(ID_APP_ABOUT, OnAppAbout)
		// NOTE - the ClassWizard will add and remove mapping macros here.
		//    DO NOT EDIT what you see in these blocks of generated code!
	//}}AFX_MSG_MAP
	// Standard file based document commands
	ON_COMMAND(ID_FILE_NEW, CWinApp::OnFileNew)
	ON_COMMAND(ID_FILE_OPEN, CWinApp::OnFileOpen)
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CFindzipApp construction

CFindzipApp::CFindzipApp()
{
	// TODO: add construction code here,
	// Place all significant initialization in InitInstance
}

/////////////////////////////////////////////////////////////////////////////
// The one and only CFindzipApp object

CFindzipApp theApp;

// This identifier was generated to be statistically unique for your app.
// You may change it if you prefer to choose a specific identifier.
static const CLSID BASED_CODE clsid =
{ 0x123ebba0, 0xf439, 0x11ce, { 0xbd, 0x29, 0x0, 0xaa, 0x0, 0x59, 0x4a, 0xd7 } };

/////////////////////////////////////////////////////////////////////////////
// ADDED FOR INTEGRATED MAPPING SUPPORT: The one and only DMapInfo object

DMapInfo mapinfo;

/////////////////////////////////////////////////////////////////////////////
// CFindzipApp initialization

BOOL CFindzipApp::InitInstance()
{
	// Initialize OLE libraries - added by class wizard when OLE Automation chosen
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

	CSingleDocTemplate* pDocTemplate;
	pDocTemplate = new CSingleDocTemplate(
		IDR_MAINFRAME,
		RUNTIME_CLASS(CFindzipDoc),
		RUNTIME_CLASS(CMainFrame),       // main SDI frame window
		RUNTIME_CLASS(CFindzipView));
	AddDocTemplate(pDocTemplate);

	// Connect the COleTemplateServer to the document template.
	//  The COleTemplateServer creates new documents on behalf
	//  of requesting OLE containers by using information
	//  specified in the document template.
	m_server.ConnectTemplate(clsid, pDocTemplate, TRUE);
		// Note: SDI applications register server objects only if /Embedding
		//   or /Automation is present on the command line.

	// Parse the command line to see if launched as OLE server
	if (RunEmbedded() || RunAutomated())
	{
		// Register all OLE server (factories) as running.  This enables the
		//  OLE libraries to create objects from other applications.
		COleTemplateServer::RegisterAll();

		// Application was run with /Embedding or /Automation.  Don't show the
		//  main window in this case.
		return TRUE;
	}

	// When a server application is launched stand-alone, it is a good idea
	//  to update the system registry in case it has been damaged.
	m_server.UpdateRegistry(OAT_DISPATCH_OBJECT);
	COleObjectFactory::UpdateRegistryAll();

	// create a new (empty) document
	OnFileNew();

	if (m_lpCmdLine[0] != '\0')
	{
		// TODO: add command line processing here
	}

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
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

// App command to run the dialog
void CFindzipApp::OnAppAbout()
{
	CAboutDlg aboutDlg;
	aboutDlg.DoModal();
}

/////////////////////////////////////////////////////////////////////////////
// CFindzipApp commands

int CFindzipApp::ExitInstance() 
{
	// TODO: Add your specialized code here and/or call the base class

  // ADDED FOR INTEGRATED MAPPING SUPPORT
  mapinfo.ReleaseDispatch();
  // END OF ADDITION FOR INTEGRATED MAPPING SUPPORT

	return CWinApp::ExitInstance();
}
