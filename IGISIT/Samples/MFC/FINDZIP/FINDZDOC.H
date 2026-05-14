// findzdoc.h : interface of the CFindzipDoc class
//
/////////////////////////////////////////////////////////////////////////////
class CFindzipView;
class CFindzipDoc : public CDocument
{
protected: // create from serialization only
	CFindzipDoc();
	DECLARE_DYNCREATE(CFindzipDoc)

// Attributes
public:

// Operations
public:
	void SetCallback(void);
	CFindzipView *GetView();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CFindzipDoc)
	public:
	virtual BOOL OnNewDocument();
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CFindzipDoc();
	virtual void Serialize(CArchive& ar);   // overridden for document i/o
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CFindzipDoc)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()

	// Generated OLE dispatch map functions
	//{{AFX_DISPATCH(CFindzipDoc)
	afx_msg SCODE WindowContentsChanged(long lWindowID);
	afx_msg void OnQueryPosition(LPCTSTR lpcstrArg);
	//}}AFX_DISPATCH
	DECLARE_DISPATCH_MAP()
};

/////////////////////////////////////////////////////////////////////////////
