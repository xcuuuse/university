// mdimadoc.cpp : implementation of the CMdimapDoc class
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
// CMdimapDoc

IMPLEMENT_DYNCREATE(CMdimapDoc, CDocument)

BEGIN_MESSAGE_MAP(CMdimapDoc, CDocument)
	//{{AFX_MSG_MAP(CMdimapDoc)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CMdimapDoc construction/destruction

CMdimapDoc::CMdimapDoc()
{
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    m_strAlias = "";
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

CMdimapDoc::~CMdimapDoc()
{
}

BOOL CMdimapDoc::OnNewDocument()
{
	if (!CDocument::OnNewDocument())
		return FALSE;

	// TODO: add reinitialization code here
	// (SDI documents will reuse this document)

	return TRUE;
}

/////////////////////////////////////////////////////////////////////////////
// CMdimapDoc serialization

void CMdimapDoc::Serialize(CArchive& ar)
{
	if (ar.IsStoring())
	{
		// TODO: add storing code here
	}
	else
	{
		// TODO: add loading code here
	}
}

/////////////////////////////////////////////////////////////////////////////
// CMdimapDoc diagnostics

#ifdef _DEBUG
void CMdimapDoc::AssertValid() const
{
	CDocument::AssertValid();
}

void CMdimapDoc::Dump(CDumpContext& dc) const
{
	CDocument::Dump(dc);
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CMdimapDoc commands

BOOL CMdimapDoc::OnOpenDocument(LPCTSTR lpszPathName) 
{
	if (!CDocument::OnOpenDocument(lpszPathName))
		return FALSE;
	
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    CString strCommand;

    m_strPathName = lpszPathName;
    strCommand.Format("Open Table \"%s\"", (LPCTSTR)m_strPathName);
    mapinfo.Do(strCommand);
	strCommand.Format("TableInfo(0,%d)", TAB_INFO_NAME);
	m_strAlias = mapinfo.Eval(strCommand);
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

	return TRUE;
}

void CMdimapDoc::OnCloseDocument() 
{
	CDocument::OnCloseDocument();
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    GetOurApp()->CheckDestroyOverview();
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
}

