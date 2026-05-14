# Microsoft Developer Studio Generated NMAKE File, Format Version 4.10
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Application" 0x0101

!IF "$(CFG)" == ""
CFG=Mdimap - Win32 Debug
!MESSAGE No configuration specified.  Defaulting to Mdimap - Win32 Debug.
!ENDIF 

!IF "$(CFG)" != "Mdimap - Win32 Debug" && "$(CFG)" != "Mdimap - Win32 Release"
!MESSAGE Invalid configuration "$(CFG)" specified.
!MESSAGE You can specify a configuration when running NMAKE on this makefile
!MESSAGE by defining the macro CFG on the command line.  For example:
!MESSAGE 
!MESSAGE NMAKE /f "Mdimap.mak" CFG="Mdimap - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "Mdimap - Win32 Debug" (based on "Win32 (x86) Application")
!MESSAGE "Mdimap - Win32 Release" (based on "Win32 (x86) Application")
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

!IF  "$(CFG)" == "Mdimap - Win32 Debug"

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

ALL : "$(OUTDIR)\Mdimap.exe" "$(OUTDIR)\mdimap.tlb"

CLEAN : 
	-@erase "$(INTDIR)\mainfrm.obj"
	-@erase "$(INTDIR)\mapinfow.obj"
	-@erase "$(INTDIR)\mdimadoc.obj"
	-@erase "$(INTDIR)\mdimap.obj"
	-@erase "$(INTDIR)\Mdimap.pch"
	-@erase "$(INTDIR)\mdimap.res"
	-@erase "$(INTDIR)\mdimap.tlb"
	-@erase "$(INTDIR)\mdimavw.obj"
	-@erase "$(INTDIR)\ovvwdlg.obj"
	-@erase "$(INTDIR)\stdafx.obj"
	-@erase "$(INTDIR)\vc40.idb"
	-@erase "$(INTDIR)\vc40.pdb"
	-@erase "$(OUTDIR)\Mdimap.exe"
	-@erase "$(OUTDIR)\Mdimap.ilk"
	-@erase "$(OUTDIR)\Mdimap.pdb"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

# ADD BASE CPP /nologo /MD /W3 /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS" /D "_MBCS" /D "_AFXDLL" /FR /Yu"stdafx.h" /c
# ADD CPP /nologo /MDd /W3 /Gm /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS" /D "_AFXDLL" /D "_MBCS" /Yu"stdafx.h" /c
# SUBTRACT CPP /Fr
CPP_PROJ=/nologo /MDd /W3 /Gm /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS"\
 /D "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Mdimap.pch" /Yu"stdafx.h" /Fo"$(INTDIR)/"\
 /Fd"$(INTDIR)/" /c 
CPP_OBJS=.\WinDebug/
CPP_SBRS=.\.
# ADD BASE MTL /nologo /D "_DEBUG" /win32
# ADD MTL /nologo /D "_DEBUG" /win32
MTL_PROJ=/nologo /D "_DEBUG" /win32 
# ADD BASE RSC /l 0x409 /d "_DEBUG" /d "_AFXDLL"
# ADD RSC /l 0x409 /d "_DEBUG" /d "_AFXDLL"
RSC_PROJ=/l 0x409 /fo"$(INTDIR)/mdimap.res" /d "_DEBUG" /d "_AFXDLL" 
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
BSC32_FLAGS=/nologo /o"$(OUTDIR)/Mdimap.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
# ADD BASE LINK32 /nologo /subsystem:windows /debug /machine:I386
# SUBTRACT BASE LINK32 /pdb:none
# ADD LINK32 /nologo /subsystem:windows /debug /machine:I386
# SUBTRACT LINK32 /pdb:none
LINK32_FLAGS=/nologo /subsystem:windows /incremental:yes\
 /pdb:"$(OUTDIR)/Mdimap.pdb" /debug /machine:I386 /out:"$(OUTDIR)/Mdimap.exe" 
LINK32_OBJS= \
	"$(INTDIR)\mainfrm.obj" \
	"$(INTDIR)\mapinfow.obj" \
	"$(INTDIR)\mdimadoc.obj" \
	"$(INTDIR)\mdimap.obj" \
	"$(INTDIR)\mdimap.res" \
	"$(INTDIR)\mdimavw.obj" \
	"$(INTDIR)\ovvwdlg.obj" \
	"$(INTDIR)\stdafx.obj"

"$(OUTDIR)\Mdimap.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
    $(LINK32) @<<
  $(LINK32_FLAGS) $(LINK32_OBJS)
<<

!ELSEIF  "$(CFG)" == "Mdimap - Win32 Release"

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

ALL : "$(OUTDIR)\Mdimap.exe" "$(OUTDIR)\mdimap.tlb"

CLEAN : 
	-@erase "$(INTDIR)\mainfrm.obj"
	-@erase "$(INTDIR)\mapinfow.obj"
	-@erase "$(INTDIR)\mdimadoc.obj"
	-@erase "$(INTDIR)\mdimap.obj"
	-@erase "$(INTDIR)\Mdimap.pch"
	-@erase "$(INTDIR)\mdimap.res"
	-@erase "$(INTDIR)\mdimap.tlb"
	-@erase "$(INTDIR)\mdimavw.obj"
	-@erase "$(INTDIR)\ovvwdlg.obj"
	-@erase "$(INTDIR)\stdafx.obj"
	-@erase "$(OUTDIR)\Mdimap.exe"

"$(OUTDIR)" :
    if not exist "$(OUTDIR)/$(NULL)" mkdir "$(OUTDIR)"

# ADD BASE CPP /nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D "_MBCS" /D "_AFXDLL" /FR /Yu"stdafx.h" /c
# ADD CPP /nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D "_AFXDLL" /D "_MBCS" /Yu"stdafx.h" /c
# SUBTRACT CPP /Fr
CPP_PROJ=/nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D\
 "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Mdimap.pch" /Yu"stdafx.h" /Fo"$(INTDIR)/" /c\
 
CPP_OBJS=.\WinRel/
CPP_SBRS=.\.
# ADD BASE MTL /nologo /D "NDEBUG" /win32
# ADD MTL /nologo /D "NDEBUG" /win32
MTL_PROJ=/nologo /D "NDEBUG" /win32 
# ADD BASE RSC /l 0x409 /d "NDEBUG" /d "_AFXDLL"
# ADD RSC /l 0x409 /d "NDEBUG" /d "_AFXDLL"
RSC_PROJ=/l 0x409 /fo"$(INTDIR)/mdimap.res" /d "NDEBUG" /d "_AFXDLL" 
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
BSC32_FLAGS=/nologo /o"$(OUTDIR)/Mdimap.bsc" 
BSC32_SBRS= \
	
LINK32=link.exe
# ADD BASE LINK32 /nologo /subsystem:windows /machine:I386
# SUBTRACT BASE LINK32 /pdb:none
# ADD LINK32 /nologo /subsystem:windows /machine:I386
# SUBTRACT LINK32 /pdb:none
LINK32_FLAGS=/nologo /subsystem:windows /incremental:no\
 /pdb:"$(OUTDIR)/Mdimap.pdb" /machine:I386 /out:"$(OUTDIR)/Mdimap.exe" 
LINK32_OBJS= \
	"$(INTDIR)\mainfrm.obj" \
	"$(INTDIR)\mapinfow.obj" \
	"$(INTDIR)\mdimadoc.obj" \
	"$(INTDIR)\mdimap.obj" \
	"$(INTDIR)\mdimap.res" \
	"$(INTDIR)\mdimavw.obj" \
	"$(INTDIR)\ovvwdlg.obj" \
	"$(INTDIR)\stdafx.obj"

"$(OUTDIR)\Mdimap.exe" : "$(OUTDIR)" $(DEF_FILE) $(LINK32_OBJS)
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

# Name "Mdimap - Win32 Debug"
# Name "Mdimap - Win32 Release"

!IF  "$(CFG)" == "Mdimap - Win32 Debug"

!ELSEIF  "$(CFG)" == "Mdimap - Win32 Release"

!ENDIF 

################################################################################
# Begin Source File

SOURCE=.\stdafx.cpp
DEP_CPP_STDAF=\
	".\stdafx.h"\
	

!IF  "$(CFG)" == "Mdimap - Win32 Debug"

# ADD BASE CPP /Yc"stdafx.h"
# ADD CPP /Yc"stdafx.h"

BuildCmds= \
	$(CPP) /nologo /MDd /W3 /Gm /GX /Zi /Od /D "_DEBUG" /D "WIN32" /D "_WINDOWS"\
 /D "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Mdimap.pch" /Yc"stdafx.h" /Fo"$(INTDIR)/"\
 /Fd"$(INTDIR)/" /c $(SOURCE) \
	

"$(INTDIR)\stdafx.obj" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

"$(INTDIR)\Mdimap.pch" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

!ELSEIF  "$(CFG)" == "Mdimap - Win32 Release"

# ADD BASE CPP /Yc"stdafx.h"
# ADD CPP /Yc"stdafx.h"

BuildCmds= \
	$(CPP) /nologo /MD /W3 /GX /O2 /D "NDEBUG" /D "WIN32" /D "_WINDOWS" /D\
 "_AFXDLL" /D "_MBCS" /Fp"$(INTDIR)/Mdimap.pch" /Yc"stdafx.h" /Fo"$(INTDIR)/" /c\
 $(SOURCE) \
	

"$(INTDIR)\stdafx.obj" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

"$(INTDIR)\Mdimap.pch" : $(SOURCE) $(DEP_CPP_STDAF) "$(INTDIR)"
   $(BuildCmds)

!ENDIF 

# End Source File
################################################################################
# Begin Source File

SOURCE=.\mdimap.cpp
DEP_CPP_MDIMA=\
	".\mainfrm.h"\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\mdimadoc.h"\
	".\mdimap.h"\
	".\mdimavw.h"\
	".\ovvwdlg.h"\
	".\stdafx.h"\
	

"$(INTDIR)\mdimap.obj" : $(SOURCE) $(DEP_CPP_MDIMA) "$(INTDIR)"\
 "$(INTDIR)\Mdimap.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\mainfrm.cpp
DEP_CPP_MAINF=\
	".\mainfrm.h"\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\mdimadoc.h"\
	".\mdimap.h"\
	".\mdimavw.h"\
	".\ovvwdlg.h"\
	".\stdafx.h"\
	

"$(INTDIR)\mainfrm.obj" : $(SOURCE) $(DEP_CPP_MAINF) "$(INTDIR)"\
 "$(INTDIR)\Mdimap.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\mdimadoc.cpp
DEP_CPP_MDIMAD=\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\mdimadoc.h"\
	".\mdimap.h"\
	".\mdimavw.h"\
	".\stdafx.h"\
	

"$(INTDIR)\mdimadoc.obj" : $(SOURCE) $(DEP_CPP_MDIMAD) "$(INTDIR)"\
 "$(INTDIR)\Mdimap.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\mdimavw.cpp
DEP_CPP_MDIMAV=\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\mdimadoc.h"\
	".\mdimap.h"\
	".\mdimavw.h"\
	".\stdafx.h"\
	

"$(INTDIR)\mdimavw.obj" : $(SOURCE) $(DEP_CPP_MDIMAV) "$(INTDIR)"\
 "$(INTDIR)\Mdimap.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\mdimap.rc
DEP_RSC_MDIMAP=\
	".\res\mdimadoc.ico"\
	".\res\mdimap.ico"\
	".\res\mdimap.rc2"\
	".\res\toolbar.bmp"\
	

!IF  "$(CFG)" == "Mdimap - Win32 Debug"


"$(INTDIR)\mdimap.res" : $(SOURCE) $(DEP_RSC_MDIMAP) "$(INTDIR)"
   $(RSC) /l 0x409 /fo"$(INTDIR)/mdimap.res" /i "WinDebug" /d "_DEBUG" /d\
 "_AFXDLL" $(SOURCE)


!ELSEIF  "$(CFG)" == "Mdimap - Win32 Release"


"$(INTDIR)\mdimap.res" : $(SOURCE) $(DEP_RSC_MDIMAP) "$(INTDIR)"
   $(RSC) /l 0x409 /fo"$(INTDIR)/mdimap.res" /i "WinRel" /d "NDEBUG" /d\
 "_AFXDLL" $(SOURCE)


!ENDIF 

# End Source File
################################################################################
# Begin Source File

SOURCE=.\readme.txt

!IF  "$(CFG)" == "Mdimap - Win32 Debug"

!ELSEIF  "$(CFG)" == "Mdimap - Win32 Release"

!ENDIF 

# End Source File
################################################################################
# Begin Source File

SOURCE=.\mdimap.odl

!IF  "$(CFG)" == "Mdimap - Win32 Debug"


"$(OUTDIR)\mdimap.tlb" : $(SOURCE) "$(OUTDIR)"
   $(MTL) /nologo /D "_DEBUG" /tlb "$(OUTDIR)/mdimap.tlb" /win32 $(SOURCE)


!ELSEIF  "$(CFG)" == "Mdimap - Win32 Release"


"$(OUTDIR)\mdimap.tlb" : $(SOURCE) "$(OUTDIR)"
   $(MTL) /nologo /D "NDEBUG" /tlb "$(OUTDIR)/mdimap.tlb" /win32 $(SOURCE)


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
 "$(INTDIR)\Mdimap.pch"


# End Source File
################################################################################
# Begin Source File

SOURCE=.\ovvwdlg.cpp
DEP_CPP_OVVWD=\
	".\mapbasic.h"\
	".\mapinfow.h"\
	".\mdimap.h"\
	".\ovvwdlg.h"\
	".\stdafx.h"\
	

"$(INTDIR)\ovvwdlg.obj" : $(SOURCE) $(DEP_CPP_OVVWD) "$(INTDIR)"\
 "$(INTDIR)\Mdimap.pch"


# End Source File
# End Target
# End Project
################################################################################
