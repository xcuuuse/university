unit Tabmap;

interface

uses
  ShellApi, SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, ExtCtrls, TabNotBk, StdCtrls, DdeMan, Buttons, ComCtrls,OLEAuto;

type
  TfrmMapInfo = class(TForm)
    tabViews: TTabbedNotebook;
    pnlMapper: TPanel;
    cmdAddTable: TButton;
    ddeMapInfo: TDdeClientConv;
    ddeMapInfoItem: TDdeClientItem;
    cmdExit: TButton;
    grpTools: TGroupBox;
    cmdZoomIn: TBitBtn;
    cmdZoomOut: TBitBtn;
    cmdGrabber: TBitBtn;
    lstBrowser: TListBox;
    pnlBrowser: TPanel;
    lblTableList: TLabel;
    pnlGrapher: TPanel;
    lblColumns: TLabel;
    lstColumns: TListBox;
    cmdGraph: TButton;
    procedure FormActivate(Sender: TObject);
    procedure cmdAddTableClick(Sender: TObject);
    procedure cmdExitClick(Sender: TObject);
    procedure cmdZoomInClick(Sender: TObject);
    procedure cmdZoomOutClick(Sender: TObject);
    procedure cmdGrabberClick(Sender: TObject);
    procedure lstBrowserClick(Sender: TObject);
    procedure tabViewsChange(Sender: TObject; NewTab: Integer;
      var AllowChange: Boolean);
    procedure cmdGraphClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frmMapInfo     : TfrmMapInfo;
  giMode         : Integer;
  oleMapInfo     : Variant;

implementation

{$R *.DFM}

procedure TfrmMapInfo.FormActivate(Sender: TObject);

Const
 SW_SHOWNORMAL = 1;

var
 MsgString : String;
 sWinHand : String;
 sApplicationPath : String[100];
 sApplicationName : PChar;
 sTemp            : PChar;
 pcEntry : PChar;
 pcSection  : PChar;
 MsgSent :PChar;
 rc : Boolean;
 rcw : Word;
 hRegKey : HKEY;
 cb : LongInt;
 iRc : Integer;

begin

  { Setting up some global Variables }

  giMode         := 1;

  {
    The following code will be used to run MapInfo as an OLE server.  Since Delphi 2.0
    now supports OLE automation, we can take advantage of OLE.  The following statement
    will run MapInfo in Server mode and assign the instance of MapInfo into the Variant
    variable oleMapInfo.  Throughout the rest of the application, if we need to
    communicate to MapInfo, we do this through the oleMapInfo object.
  }

  oleMapInfo := CreateOLEObject('MapInfo.Application');

  {
    Our next step is to set the Next Document parent to a window in the Delphi sample
    app.  The following lines of code will show you how to send commands to MapInfo using
    the oleMapInfo variable.
  }

  Str(pnlMapper.Handle, sWinHand);
  MsgString := 'Set Next Document Parent ' + sWinHand + ' Style 1';
  oleMapInfo.Do(MsgString);

  {
    Finally, since we want all MapInfo dialogs and messages to appear in our sample app,
    we will reparent all of the dialogs to the sample application again using our OLE
    variable oleMapInfo.
  }

  MsgString := 'Set Application Window ' + sWinHand;
  oleMapInfo.Do(MsgString);

end;

procedure TfrmMapInfo.cmdAddTableClick(Sender: TObject);

Var
 MsgString : String;
 MsgSent :PChar;
 rc : Boolean;
 sWinHand : String;

begin

 {
   Since this procedure will open a MapInfo map table, we will set the next window to be
   created to the mapper panel.
 }

 Str(pnlMapper.Handle, sWinHand);
 MsgString := 'Set Next Document Parent ' + sWinHand + ' Style 1';
 oleMapInfo.Do(MsgString);

 {
  This will prompt the user with the MapInfo Open Table Dialog Box. What ever table
  the user opens will be put into the panel Window.
 }

 oleMapInfo.RunMenuCommand(102);

end;

procedure TfrmMapInfo.cmdExitClick(Sender: TObject);

Var
 MsgSent :PChar;
 rc : Boolean;

begin

 {
   The line will shut down MapInfo by Unassigning the object variable.  
 }

 oleMapInfo := UnAssigned;

 {
   Terminate the app
 }
 
 Application.Terminate;

end;

procedure TfrmMapInfo.cmdZoomInClick(Sender: TObject);

begin

 {
  Send a message to run the Zoom-in tool
 }

  oleMapInfo.RunMenuCommand(1705);

end;

procedure TfrmMapInfo.cmdZoomOutClick(Sender: TObject);

begin

 {
  Send a message to run the Zoom-Out tool
 }

  oleMapInfo.RunMenuCommand(1706);

end;

procedure TfrmMapInfo.cmdGrabberClick(Sender: TObject);

begin

 {
  Send a message to run the Grabber tool
 }

  oleMapInfo.RunMenuCommand(1702);

end;


procedure TfrmMapInfo.lstBrowserClick(Sender: TObject);

Var
 sMsgString : String;
 sWinID     : String;
 sWinHand   : String;
 sResult    : String;
 sVal       : String;
 sInVal     : String;
 i          : Integer;
 Code       : Integer;
 iInLoop    : Integer;

begin

 {
   Depending on which tab the user chooses, we will either display a mapper, browser, or
   grapher.  The following code will determine which the user wants and display
   appropriately.
 }

 Case giMode of

    1: Begin

         {
           Sending the commands to MapInfo to display a Mapper.
         }

         Str(pnlMapper.Handle, sWinHand);
         sMsgString := 'Set Next Document Parent ' + sWinHand + ' Style 1';
         oleMapInfo.Do(sMsgString);
         sMsgString := 'Map from ' + lstBrowser.Items.Strings[lstBrowser.ItemIndex];
         oleMapInfo.Do(sMsgString);

       End;

    2: Begin

         {
           Sending the commands to MapInfo to display a Browser.
         }

         Str(pnlBrowser.Handle, sWinHand);
         sMsgString := 'Set Next Document Parent ' + sWinHand + ' Style 1';
         oleMapInfo.Do(sMsgString);
         sMsgString := 'Browse * from ' + lstBrowser.Items.Strings[lstBrowser.ItemIndex];
         oleMapInfo.Do(sMsgString);

       End;

    3: Begin

         {
           Sending the commands to MapInfo to display a Grapher.
         }

         lstColumns.Items.Clear;
         sVal := lstBrowser.Items.Strings[lstBrowser.ItemIndex];
         sMsgString := 'TableInfo(' + sVal + ', 4)';
         sResult := oleMapInfo.Eval(sMsgString);
         Val(sResult, i, Code);
         If i > 0 Then
           Begin
             For iInLoop := 1 to i Do
               Begin
                 Str(iInLoop,sInVal);
                 sMsgString := 'ColumnInfo(' + sVal + ',"' + 'COL' + sInVal + '"' + ', 1)';
                 lstColumns.Items.Add(oleMapInfo.Eval(sMsgString))
               End;
           End;
       End;
    End; {Case Statement}
end;

procedure TfrmMapInfo.tabViewsChange(Sender: TObject; NewTab: Integer;
  var AllowChange: Boolean);

Var
 sResult    : String;
 sMsgString : String;
 sVal       : String;
 sInVal     : String;
 rc         : Integer;
 i          : Integer;
 j          : Integer;
 Code       : Integer;
 iLoop      : Integer;
 iInLoop    : Integer;

begin

 {
   After a tab has been changed, we want to list all of the available tables.
 }

  lstBrowser.Items.Clear;
  lstColumns.Items.Clear;
  sResult := oleMapInfo.Eval('NumTables()');
  Val(sResult, I, Code);


  {
     Getting a list of available tables and populating the listbox on the interface.
  }

  If I > 0 Then
    Begin
      For iLoop := 1 to i Do
        Begin
          Str(iLoop,sVal);
          sMsgString := 'TableInfo(' + sVal + ', 1)';
          lstBrowser.Items.Add(oleMapinfo.Eval(sMsgString));
        End;
    End;

  {
    Depending on which tab the user clicks on, the following code will enable and disable
    controls.
  }

  Case NewTab of
    0: Begin
        cmdZoomIn.Enabled := True;
        cmdZoomOut.Enabled := True;
        cmdGrabber.Enabled := True;
        lstBrowser.Enabled := True;
        lstColumns.Enabled := False;
        giMode := 1;
       End;
    1: Begin
        cmdZoomIn.Enabled := False;
        cmdZoomOut.Enabled := False;
        cmdGrabber.Enabled := False;
        lstBrowser.Enabled := True;
        lstColumns.Enabled := False;
        giMode := 2;
       End;
    2: Begin
        cmdZoomIn.Enabled := False;
        cmdZoomOut.Enabled := False;
        cmdGrabber.Enabled := False;
        lstBrowser.Enabled := True;
        lstColumns.Enabled := True;
        giMode := 3;
       End;
  End; {Case Statement}
 end;

procedure TfrmMapInfo.cmdGraphClick(Sender: TObject);

Var
 sMsgString : String;
 sWinHand   : String;
 sResult    : String;
 sVal       : String;
 sInVal     : String;
 sCols      : String;
 i          : Integer;
 Code       : Integer;
 iInLoop    : Integer;
 iCtr       : Integer;

begin

 {
   This procedure will get the columns that the user will want to graph and
   attempt to create a graph.
 }

 If lstColumns.SelCount > 1 Then
   Begin
     sCols := '';
     iCtr  := 1;
     For i := 0 to lstColumns.Items.Count - 1 Do
       Begin
         If lstColumns.Selected[i] Then
           Begin
            If iCtr > 1 Then
              sCols := sCols + ',';
              sCols := sCols + lstColumns.Items.Strings[i];
              iCtr := iCtr + 1;
           End;
       End;
     Str(pnlGrapher.Handle, sWinHand);
     sMsgString := 'Set Next Document Parent ' + sWinHand + ' Style 1';
     oleMapInfo.Do(sMsgString);
     sMsgString := 'Graph ' + sCols + ' from ';
     sMsgString := sMsgString + lstBrowser.Items.Strings[lstBrowser.ItemIndex];
     oleMapInfo.Do(sMsgString);
   End;
end;

end.
