program Tabedmap;

uses
  Forms,
  Tabmap in 'TABMAP.PAS' {frmMapInfo};

{$R *.RES}

begin
  Application.CreateForm(TfrmMapInfo, frmMapInfo);
  Application.Run;
end.
