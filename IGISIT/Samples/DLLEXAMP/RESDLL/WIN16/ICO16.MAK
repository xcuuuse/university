# Microsoft Visual C++ generated build script - Do not modify

PROJ = ICO16
DEBUG = 1
PROGTYPE = 1
CALLER = 
ARGS = 
DLLS = 
D_RCDEFINES = /d_DEBUG 
R_RCDEFINES = /dNDEBUG 
ORIGIN = MSVC
ORIGIN_VER = 1.00
PROJPATH = D:\MALTA\PARTNER\SAMPLES\ICONS\WIN16\
USEMFC = 1
CC = cl
CPP = cl
CXX = cl
CCREATEPCHFLAG = 
CPPCREATEPCHFLAG = 
CUSEPCHFLAG = 
CPPUSEPCHFLAG = 
FIRSTC =             
FIRSTCPP = ICO16.CPP   
RC = rc
CFLAGS_D_WDLL = /nologo /W3 /FR /G2 /Zi /D_DEBUG /Od /GD /ALw /Fd"ICO16.PDB"
CFLAGS_R_WDLL = /nologo /W3 /FR /O1 /DNDEBUG /GD /ALw
LFLAGS_D_WDLL = /NOLOGO /ONERROR:NOEXE /NOD /PACKC:61440 /CO /NOE /ALIGN:16 /MAP:FULL
LFLAGS_R_WDLL = /NOLOGO /ONERROR:NOEXE /NOD /PACKC:61440 /NOE /ALIGN:16 /MAP:FULL
LIBS_D_WDLL = lafxdwd oldnames libw commdlg shell olecli olesvr ldllcew
LIBS_R_WDLL = lafxdw oldnames libw commdlg shell olecli olesvr ldllcew
RCFLAGS = /nologo 
RESFLAGS = /nologo 
RUNFLAGS = 
DEFFILE = ICO16.DEF
OBJS_EXT = 
LIBS_EXT = 
!if "$(DEBUG)" == "1"
CFLAGS = $(CFLAGS_D_WDLL)
LFLAGS = $(LFLAGS_D_WDLL)
LIBS = $(LIBS_D_WDLL)
MAPFILE = nul
RCDEFINES = $(D_RCDEFINES)
!else
CFLAGS = $(CFLAGS_R_WDLL)
LFLAGS = $(LFLAGS_R_WDLL)
LIBS = $(LIBS_R_WDLL)
MAPFILE = nul
RCDEFINES = $(R_RCDEFINES)
!endif
!if [if exist MSVC.BND del MSVC.BND]
!endif
SBRS = ICO16.SBR


ICO16_DEP = 

ICO16_RCDEP = d:\malta\partner\samples\icons\win16\ico1.bmp \
	d:\malta\partner\samples\icons\win16\bitmap2.bmp \
	d:\malta\partner\samples\icons\win16\cursor1.cur


all:	$(PROJ).DLL $(PROJ).BSC

ICO16.OBJ:	ICO16.CPP $(ICO16_DEP)
	$(CPP) $(CFLAGS) $(CPPCREATEPCHFLAG) /c ICO16.CPP

ICO16.RES:	ICO16.RC $(ICO16_RCDEP)
	$(RC) $(RCFLAGS) $(RCDEFINES) -r ICO16.RC


$(PROJ).DLL::	ICO16.RES

$(PROJ).DLL::	ICO16.OBJ $(OBJS_EXT) $(DEFFILE)
	echo >NUL @<<$(PROJ).CRF
ICO16.OBJ +
$(OBJS_EXT)
$(PROJ).DLL
$(MAPFILE)
U:\LIB\+
U:\MFC\LIB\+
$(LIBS)
$(DEFFILE);
<<
	link $(LFLAGS) @$(PROJ).CRF
	$(RC) $(RESFLAGS) ICO16.RES $@
	@copy $(PROJ).CRF MSVC.BND
	implib /nowep $(PROJ).LIB $(PROJ).DLL

$(PROJ).DLL::	ICO16.RES
	if not exist MSVC.BND 	$(RC) $(RESFLAGS) ICO16.RES $@

run: $(PROJ).DLL
	$(PROJ) $(RUNFLAGS)


$(PROJ).BSC: $(SBRS)
	bscmake @<<
/o$@ $(SBRS)
<<
