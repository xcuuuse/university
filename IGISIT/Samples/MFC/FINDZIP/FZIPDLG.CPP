// fzipdlg.cpp : implementation file
//

#include "stdafx.h"
#include "findzip.h"
#include "fzipdlg.h"

#ifdef _DEBUG
#undef THIS_FILE
static char BASED_CODE THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CFindZipDlg dialog

CFindZipDlg::CFindZipDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CFindZipDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CFindZipDlg)
	m_strZip = _T("");
	//}}AFX_DATA_INIT
}

void CFindZipDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CFindZipDlg)
	DDX_Text(pDX, IDC_ZIP, m_strZip);
	DDV_MaxChars(pDX, m_strZip, 5);
	//}}AFX_DATA_MAP
	DDV_ValidateInput(pDX, m_strZip);
}

BEGIN_MESSAGE_MAP(CFindZipDlg, CDialog)
	//{{AFX_MSG_MAP(CFindZipDlg)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// DDV_ValidateInput - makes sure user only types in numeric characters.

void AFXAPI CFindZipDlg::DDV_ValidateInput(CDataExchange* pDX, LPCTSTR lpctstrInput)
{
	if (pDX->m_bSaveAndValidate)
	{
		pDX->PrepareEditCtrl(IDC_ZIP);

        while (*lpctstrInput) {
            if (!isdigit(*lpctstrInput)) {
    			MessageBeep((UINT)-1);
    			AfxMessageBox("Please enter only numeric digits.",MB_ICONEXCLAMATION);
    			pDX->Fail();
            }
            lpctstrInput++;
        }
	}
}

/////////////////////////////////////////////////////////////////////////////
// CFindZipDlg message handlers

BOOL CFindZipDlg::OnInitDialog() 
{
	CDialog::OnInitDialog();
	
	// Set focus to edit control
    CWnd *pWnd = GetDlgItem(IDC_ZIP);
    if (pWnd) {
	    GotoDlgCtrl(pWnd);	
    }
	return FALSE; // return TRUE unless you set the focus to a control
	              // EXCEPTION: OCX Property Pages should return FALSE
}
