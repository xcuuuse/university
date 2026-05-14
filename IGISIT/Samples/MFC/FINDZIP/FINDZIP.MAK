# Microsoft Developer Studio Generated NMAKE File, Format Version 4.10
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Application" 0x0101

!IF "$(CFG)" == ""
CFG=Findzip - Win32 Debug
!MESSAGE No configuration specified.  Defaulting to Findzip - Win32 Debug.
!ENDIF 

!IF "$(CFG)" != "Findzip - Win32 Debug" && "$(CFG)" !=\
 "Findzip - Win32 Release"
!MESSAGE Invalid configuration "$(CFG)" specified.
!MESSAGE You can specify a configuration when running NMAKE on this makefile
!MESSAGE by defining the macro CFG on the command line.  For example:
!MESSAGE 
!MESSAGE NMAKE /f "Findzip.mak" CFG="Findzip - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "Findzip - Win32 Debug" (based on "Win32 (x86) Application")
!MESSAGE "Findzip - Win32 Release" (based on "Win32 (x86) Application")
!MESSAGE 
!ERROR An invalid configuration is specified.
!ENDIF 

!IF "$(OS)" == "Windows_NT"
NULL=
!ELSE 
NULL=nul
!ENDIF 
################################################################################
# Begin Project
CPP=cl.exe
RSC=rc.exe
MTL=mktyplib.exe

!IF  "$(CFG)" == "Findzip - Win32 Debug"

# PROP BASE Use_MFC 6
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir "WinDebug"
# PROP BASE Intermediate_Dir "WinDebug"
# PROP Use_MFC 6
# PROP Use_Debug_Libraries 1
# PROP Output_Dir "WinDebug"
# PROP Intermediate_Dir "WinDebug"
OUTDIR=.\WinDebug
INTDIR=.\WinDebug

ALL : "$(OUTDIR)\Findzip.exe" "$(OUTDIR)\findzip.tlb"

CLEAN : 
	-@erase "$(INTDIR)\findzdoc.obj"
	-@erase "$(INTDIR)\findzip.obj"
	-@erase "$(INTDIR)\Findzip.pch"
	-@erase "$(INTDIR)\findzip.res"
	-@erase "$(INTDIR)\findzip.tlb"
	-@erase "$(INTDIR)\findzvw.obj"
	-@erase "$(INTDIR)\fzipdlg.obj"
	-@erase "$(INTDIR)\mainfrm.obj"
	-@erase "$(INTDIR)\mapinfow.obj"
	-@erase "$(INTDIR)\stdafx.obj"
	-@erase "$(INTDIR)\vc40.idb"
	-@erase "$(INTDIR)\vc40.pdb"
	-@erase "$(OUTDIR)\Findzip.exe"
	-@erase "$(OUTDIR)\Findzip.ilk"
	-@erase "$(OUTDIR)\Findzip.pdb"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

# ADD BASE CPP /nologo /MD /W3 /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS" /D "_MBCS" /D "_AFXDLL" /FR /Yu"stdafx.h" /c
# ADD CPP /nologo /MDd /W3 /Gm /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS" /D "_AFXDLL" /D "_MBCS" /Yu"stdafx.h" /c
# SUBTRACT CPP /Fr
CPP_PROJ=/nologo /MDd /W3 /Gm /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS"\
 /D "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Findzip.pch" /Yu"stdafx.h"\
 /Fo"$(INTDIR)/" /Fd"$(INTDIR)/" /c 
CPP_OBJS=.\WinDebug/
CPP_SBRS=.\.
# ADD BASE MTL /nologo /D "_DEBUG" /win32
# ADD MTL /nologo /D "_DEBUG" /win32
MTL_PROJ=/nologo /D "_DEBUG" /win32 
# ADD BASE RSC /l 0x409 /d "_DEBUG" /d "_AFXDLL"
# ADD RSC /l 0x409 /d "_DEBUG" /d "_AFXDLL"
RSC_PROJ=/l 0x409 /fo"$(INTDIR)/findzip.res" /d "_DEBUG" /d "_AFXDLL" 
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
BSC32_FLAGS=/nologo /o"$(OUTDIR)/Findzip.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
# ADD BASE LINK32 /nologo /subsystem:windows /debug /machine:I386
# SUBTRACT BASE LINK32 /pdb:none
# ADD LINK32 /nologo /subsystem:windows /debug /machine:I386
# SUBTRACT LINK32 /pdb:none
LINK32_FLAGS=/nologo /subsystem:windows /incremental:yes\
 /pdb:"$(OUTDIR)/Findzip.pdb" /debug /machine:I386 /out:"$(OUTDIR)/Findzip.exe" 
LINK32_OBJS= \
	"$(INTDIR)\findzdoc.obj" \
	"$(INTDIR)\findzip.obj" \
	"$(INTDIR)\findzip.res" \
	"$(INTDIR)\findzvw.obj" \
	"$(INTDIR)\fzipdlg.obj" \
	"$(INTDIR)\mainfrm.obj" \
	"$(INTDIR)\mapinfow.obj" \
	"$(INTDIR)\stdafx.obj"

"$(OUTDIR)\Findzip.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ELSEIF  "$(CFG)" == "Findzip - Win32 Release"

# PROP BASE Use_MFC 6
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir "WinRel"
# PROP BASE Intermediate_Dir "WinRel"
# PROP Use_MFC 6
# PROP Use_Debug_Libraries 0
# PROP Output_Dir "WinRel"
# PROP Intermediate_Dir "WinRel"
OUTDIR=.\WinRel
INTDIR=.\WinRel

ALL : "$(OUTDIR)\Findzip.exe" "$(OUTDIR)\findzip.tlb"

CLEAN : 
	-@erase "$(INTDIR)\findzdoc.obj"
	-@erase "$(INTDIR)\findzip.obj"
	-@erase "$(INTDIR)\Findzip.pch"
	-@erase "$(INTDIR)\findzip.res"
	-@erase "$(INTDIR)\findzip.tlb"
	-@erase "$(INTDIR)\findzvw.obj"
	-@erase "$(INTDIR)\fzipdlg.obj"
	-@erase "$(INTDIR)\mainfrm.obj"
	-@erase "$(INTDIR)\mapinfow.obj"
	-@erase "$(INTDIR)\stdafx.obj"
	-@erase "$(OUTDIR)\Findzip.exe"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

# ADD BASE CPP /nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D "_MBCS" /D "_AFXDLL" /FR /Yu"stdafx.h" /c
# ADD CPP /nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D "_AFXDLL" /D "_MBCS" /Yu"stdafx.h" /c
# SUBTRACT CPP /Fr
CPP_PROJ=/nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D\
 "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Findzip.pch" /Yu"stdafx.h" /Fo"$(INTDIR)/"\
 /c 
CPP_OBJS=.\WinRel/
CPP_SBRS=.\.
# ADD BASE MTL /nologo /D "NDEBUG" /win32
# ADD MTL /nologo /D "NDEBUG" /win32
MTL_PROJ=/nologo /D "NDEBUG" /win32 
# ADD BASE RSC /l 0x409 /d "NDEBUG" /d "_AFXDLL"
# ADD RSC /l 0x409 /d "NDEBUG" /d "_AFXDLL"
RSC_PROJ=/l 0x409 /fo"$(INTDIR)/findzip.res" /d "NDEBUG" /d "_AFXDLL" 
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
BSC32_FLAGS=/nologo /o"$(OUTDIR)/Findzip.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
# ADD BASE LINK32 /nologo /subsystem:windows /machine:I386
# SUBTRACT BASE LINK32 /pdb:none
# ADD LINK32 /nologo /subsystem:windows /machine:I386
# SUBTRACT LINK32 /pdb:none
LINK32_FLAGS=/nologo /subsystem:windows /incremental:no\
 /pdb:"$(OUTDIR)/Findzip.pdb" /machine:I386 /out:"$(OUTDIR)/Findzip.exe" 
LINK32_OBJS= \
	"$(INTDIR)\findzdoc.obj" \
	"$(INTDIR)\findzip.obj" \
	"$(INTDIR)\findzip.res" \
	"$(INTDIR)\findzvw.obj" \
	"$(INTDIR)\fzipdlg.obj" \
	"$(INTDIR)\mainfrm.obj" \
	"$(INTDIR)\mapinfow.obj" \
	"$(INTDIR)\stdafx.obj"

"$(OUTDIR)\Findzip.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ENDIF 

.c{$(CPP_OBJS)}.obj:
   $(CPP) $(CPP_PROJ) $<  

.cpp{$(CPP_OBJS)}.obj:
   $(CPP) $(CPP_PROJ) $<  

.cxx{$(CPP_OBJS)}.obj:
   $(CPP) $(CPP_PROJ) $<  

.c{$(CPP_SBRS)}.sbr:
   $(CPP) $(CPP_PROJ) $<  

.cpp{$(CPP_SBRS)}.sbr:
   $(CPP) $(CPP_PROJ) $<  

.cxx{$(CPP_SBRS)}.sbr:
   $(CPP) $(CPP_PROJ) $<  

################################################################################
# Begin Target

# Name "Findzip - Win32 Debug"
# Name "Findzip - Win32 Release"

!IF  "$(CFG)" == "Findzip - Win32 Debug"

!ELSEIF  "$(CFG)" == "Findzip - Win32 Release"

!ENDIF 

################################################################################
# Begin Source File

SOURCE=.\stdafx.cpp
DEP_CPP_STDAF=\
	".\stdafx.h"\
	

!IF  "$(CFG)" == "Findzip - Win32 Debug"

# ADD BASE CPP /Yc"stdafx.h"
# ADD CPP /Yc"stdafx.h"

BuildCmds= \
	$(CPP) /nologo /MDd /W3 /Gm /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS"\
 /D "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Findzip.pch" /Yc"stdafx.h"\
 /Fo"$(INTDIR)/" /Fd"$(INTDIR)/" /c $(SOURCE) \
	

"$(INTDIR)\stdafx.obj" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

"$(INTDIR)\Findzip.pch" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

!ELSEIF  "$(CFG)" == "Findzip - Win32 Release"

# ADD BASE CPP /Yc"stdafx.h"
# ADD CPP /Yc"stdafx.h"

BuildCmds= \
	$(CPP) /nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D\
 "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Findzip.pch" /Yc"stdafx.h" /Fo"$(INTDIR)/"\
 /c $(SOURCE) \
	

"$(INTDIR)\stdafx.obj" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

"$(INTDIR)\Findzip.pch" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

!ENDIF 

# End Source File
################################################################################
# Begin Source File

SOURCE=.\findzip.cpp
DEP_CPP_FINDZ=\
	".\findzdoc.h"\
	".\findzip.h"\
	".\findzvw.h"\
	".\mainfrm.h"\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\stdafx.h"\
	

"$(INTDIR)\findzip.obj" : $(SOURCE) $(DEP_CPP_FINDZ) "$(INTDIR)"\
 "$(INTDIR)\Findzip.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\mainfrm.cpp
DEP_CPP_MAINF=\
	".\findzip.h"\
	".\mainfrm.h"\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\stdafx.h"\
	

"$(INTDIR)\mainfrm.obj" : $(SOURCE) $(DEP_CPP_MAINF) "$(INTDIR)"\
 "$(INTDIR)\Findzip.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\findzdoc.cpp
DEP_CPP_FINDZD=\
	".\findzdoc.h"\
	".\findzip.h"\
	".\findzvw.h"\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\stdafx.h"\
	

"$(INTDIR)\findzdoc.obj" : $(SOURCE) $(DEP_CPP_FINDZD) "$(INTDIR)"\
 "$(INTDIR)\Findzip.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\findzvw.cpp
DEP_CPP_FINDZV=\
	".\findzdoc.h"\
	".\findzip.h"\
	".\findzvw.h"\
	".\fzipdlg.h"\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\stdafx.h"\
	

"$(INTDIR)\findzvw.obj" : $(SOURCE) $(DEP_CPP_FINDZV) "$(INTDIR)"\
 "$(INTDIR)\Findzip.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\findzip.rc
DEP_RSC_FINDZI=\
	".\res\findzdoc.ico"\
	".\res\findzip.ico"\
	".\res\findzip.rc2"\
	".\res\toolbar.bmp"\
	

!IF  "$(CFG)" == "Findzip - Win32 Debug"


"$(INTDIR)\findzip.res" : $(SOURCE) $(DEP_RSC_FINDZI) "$(INTDIR)"
   $(RSC) /l 0x409 /fo"$(INTDIR)/findzip.res" /i "WinDebug" /d "_DEBUG" /d\
 "_AFXDLL" $(SOURCE)


!ELSEIF  "$(CFG)" == "Findzip - Win32 Release"


"$(INTDIR)\findzip.res" : $(SOURCE) $(DEP_RSC_FINDZI) "$(INTDIR)"
   $(RSC) /l 0x409 /fo"$(INTDIR)/findzip.res" /i "WinRel" /d "NDEBUG" /d\
 "_AFXDLL" $(SOURCE)


!ENDIF 

# End Source File
################################################################################
# Begin Source File

SOURCE=.\readme.txt

!IF  "$(CFG)" == "Findzip - Win32 Debug"

!ELSEIF  "$(CFG)" == "Findzip - Win32 Release"

!ENDIF 

# End Source File
################################################################################
# Begin Source File

SOURCE=.\findzip.odl

!IF  "$(CFG)" == "Findzip - Win32 Debug"


"$(OUTDIR)\findzip.tlb" : $(SOURCE) "$(OUTDIR)"
   $(MTL) /nologo /D "_DEBUG" /tlb "$(OUTDIR)/findzip.tlb" /win32 $(SOURCE)


!ELSEIF  "$(CFG)" == "Findzip - Win32 Release"


"$(OUTDIR)\findzip.tlb" : $(SOURCE) "$(OUTDIR)"
   $(MTL) /nologo /D "NDEBUG" /tlb "$(OUTDIR)/findzip.tlb" /win32 $(SOURCE)


!ENDIF 

# End Source File
################################################################################
# Begin Source File

SOURCE=.\mapinfow.cpp
DEP_CPP_MAPIN=\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\stdafx.h"\
	

"$(INTDIR)\mapinfow.obj" : $(SOURCE) $(DEP_CPP_MAPIN) "$(INTDIR)"\
 "$(INTDIR)\Findzip.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\fzipdlg.cpp
DEP_CPP_FZIPD=\
	".\findzip.h"\
	".\fzipdlg.h"\
	".\stdafx.h"\
	

"$(INTDIR)\fzipdlg.obj" : $(SOURCE) $(DEP_CPP_FZIPD) "$(INTDIR)"\
 "$(INTDIR)\Findzip.pch"


# End Source File
# End Target
# End Project
################################################################################
