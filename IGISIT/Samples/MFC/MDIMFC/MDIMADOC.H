// mdimadoc.h : interface of the CMdimapDoc class
//
/////////////////////////////////////////////////////////////////////////////
#if !defined MDIMADOC_H
#define MDIMADOC_H

/////////////////////////////////////////////////////////////////////////////
// Forward declarations
class CMdimapView;

class CMdimapDoc : public CDocument
{
protected: // create from serialization only
	CMdimapDoc();
	DECLARE_DYNCREATE(CMdimapDoc)

private:
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    CString m_strAlias;
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

// Attributes
public:

// Operations
public:
    // ADDED FOR INTEGRATED MAPPING SUPPORT
    CString GetAlias(void) { return m_strAlias; }
    // END OF ADDITIONS FOR INTEGRATED MAPPING SUPPORT

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMdimapDoc)
	public:
	virtual BOOL OnNewDocument();
	virtual BOOL OnOpenDocument(LPCTSTR lpszPathName);
	virtual void OnCloseDocument();
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CMdimapDoc();
	virtual void Serialize(CArchive& ar);   // overridden for document i/o
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CMdimapDoc)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()

};

/////////////////////////////////////////////////////////////////////////////
#endif /* !defined MDIMADOC_H */
