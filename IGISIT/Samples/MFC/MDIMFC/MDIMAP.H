// mdimap.h : main header file for the MDIMAP application
//
#if !defined MDIMAP_H
#define MDIMAP_H

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"       // main symbols

/////////////////////////////////////////////////////////////////////////////
// CMdimapApp:
// See mdimap.cpp for the implementation of this class
//

class CMdimapApp : public CWinApp
{
public:
	CMdimapApp();

// Operations
public:
    int MouseMode(void);
    void ClearOverview(long lMapperId);
    void UpdateOverview(long lMapperId);
    void PostOverviewUpdate(long lMapperId);
    void CheckDestroyOverview(void);
    long OverviewMapId(void);

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMdimapApp)
	public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();
	//}}AFX_VIRTUAL

// Implementation
	COleTemplateServer m_server;
		// Server object for document creation

	//{{AFX_MSG(CMdimapApp)
	afx_msg void OnAppAbout();
	afx_msg void OnFileOpen();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////
//  Global functions
CMdimapApp *GetOurApp(void);     // Gets the CMdimapApp app

#endif /* !defined MDIMAP_H */
