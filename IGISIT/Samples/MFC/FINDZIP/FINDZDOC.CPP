// findzdoc.cpp : implementation of the CFindzipDoc class
//

#include "stdafx.h"
#include "findzip.h"

#include "findzdoc.h"
#include "findzvw.h"
#include "mapinfow.h"     // ADDED FOR INTEGRATED MAPPING SUPPORT

#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CFindzipDoc

IMPLEMENT_DYNCREATE(CFindzipDoc, CDocument)

BEGIN_MESSAGE_MAP(CFindzipDoc, CDocument)
	//{{AFX_MSG_MAP(CFindzipDoc)
		// NOTE - the ClassWizard will add and remove mapping macros here.
		//    DO NOT EDIT what you see in these blocks of generated code!
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

BEGIN_DISPATCH_MAP(CFindzipDoc, CDocument)
	//{{AFX_DISPATCH_MAP(CFindzipDoc)
    // ADDED BY CLASS WIZARD FOR INTEGRATED MAPPING SUPPORT
	DISP_FUNCTION(CFindzipDoc, "WindowContentsChanged", WindowContentsChanged, VT_ERROR, VTS_I4)
	DISP_FUNCTION(CFindzipDoc, "OnQueryPosition", OnQueryPosition, VT_EMPTY, VTS_BSTR)
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
	//}}AFX_DISPATCH_MAP
END_DISPATCH_MAP()

/////////////////////////////////////////////////////////////////////////////
// CFindzipDoc construction/destruction

CFindzipDoc::CFindzipDoc()
{
	// TODO: add one-time construction code here

	EnableAutomation();

	AfxOleLockApp();
}

CFindzipDoc::~CFindzipDoc()
{
	AfxOleUnlockApp();
}

BOOL CFindzipDoc::OnNewDocument()
{
	if (!CDocument::OnNewDocument())
		return FALSE;

	// TODO: add reinitialization code here
	// (SDI documents will reuse this document)

	return TRUE;
}

/////////////////////////////////////////////////////////////////////////////
// CFindzipDoc serialization

void CFindzipDoc::Serialize(CArchive& ar)
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
// CFindzipDoc diagnostics

#ifdef _DEBUG
void CFindzipDoc::AssertValid() const
{
	CDocument::AssertValid();
}

void CFindzipDoc::Dump(CDumpContext& dc) const
{
	CDocument::Dump(dc);
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CFindzipDoc commands

// ADDED FOR INTEGRATED MAPPING SUPPORT
void CFindzipDoc::SetCallback(void)
{
    // Sets the MapInfo callback dispatch pointer.
	mapinfo.SetCallback(this->GetIDispatch(FALSE));
}

CFindzipView *CFindzipDoc::GetView()
{
	POSITION rPos = GetFirstViewPosition( );
	return (CFindzipView*)GetNextView(rPos);
}

/////////////////////////////////////////////////////////////////////////////
// Automation methods - (callbacks from MapInfo) are attached to the 
// CFindzipDoc class

SCODE CFindzipDoc::WindowContentsChanged(long lWindowID) 
{
    TRACE("CFindzipDoc::WindowContentsChanged\n");
    CFindzipView *pView = GetView();
    if (pView != NULL) {
        if (pView->MapperInitialized()) {
            pView->OnWindowContentsChanged();
        }
	}
	return S_OK;
}

void CFindzipDoc::OnQueryPosition(LPCTSTR lpcstrArg) 
{
    CString str = lpcstrArg, strArg1 = "(null)", strArg2 = "(null)";

    // lpcstrArg is of the form: "MI:arg1,arg2,arg3,...,argn,plus some other stuff"
    // We only care about the first 2 args.

    str = str.Mid(3);           // "arg1,arg2,arg3,...,argn,plus some other stuff"
    int nStart = 0;
    int nIndex = str.Find(',');
    if (nIndex >= 0) {
        strArg1 = str.Mid(nStart, nIndex - nStart);
        str = str.Mid(nIndex + 1);      // "arg2,arg3,...,argn,plus some other stuff"
        nIndex = str.Find(',');
        if (nIndex >= 0) {
            strArg2 = str.Mid(nStart, nIndex - nStart);
        }
    }

    CString strFormat = "You clicked at (%s, %s)";
    str.Format(strFormat, (LPCTSTR)strArg1, (LPCTSTR)strArg2);
    AfxMessageBox(str, MB_OK|MB_ICONINFORMATION);
}
// END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT
