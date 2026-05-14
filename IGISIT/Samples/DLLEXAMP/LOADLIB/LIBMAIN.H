/****************************************************************************/
/* LibMain.H                                                                */
/*                                                                          */
/* Include file for building a DLL.  This file includes windows.h           */
/* and defines the macro DLLENTRYPOINT.  This file is compatible with both  */
/* Win16 and Win32.                                                         */
/****************************************************************************/
#if !defined(_LIBMAIN_H)

#include <windows.h>
#pragma warning(disable:4100)

#if !defined(DLLENTRYPOINT)
  #if defined(WIN32)
    #define DLLENTRYPOINT(returntype) __declspec(dllexport) returntype __cdecl
    /* CALLBACK is already defined as __stdcall */
  #else
    #define DLLENTRYPOINT(returntype) returntype __far __pascal __export
    #undef  CALLBACK
    #define CALLBACK                  __far __pascal __export
  #endif
#endif
     
#define _LIBMAIN_H
     
#endif

