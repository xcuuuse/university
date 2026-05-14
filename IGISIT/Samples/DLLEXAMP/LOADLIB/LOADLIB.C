/****************************************************************************/
/* LoadLib.C                                                                */
/*                                                                          */
/* Sample DLL showing how to write a C language DLL that can be compiled    */
/* and used in both Win16 and Win32 environments.                           */
/****************************************************************************/

#include "libmain.h"
     
/****************************************************************************/
/* Function: TestLoadLibrary                                                */
/*                                                                          */
/* Purpose:  calls the WinAPI routine LoadLibrary and reports the success   */
/*           or failure of the call.  Can be used to diagnose problems      */
/*           in trying to load/call another DLL from MapBasic.              */
/*                                                                          */
/* Arguments: char * libraryname (in MapBasic, "libraryname As String")     */
/*                                                                          */
/* Return Value: long integer (in MapBasic, "Integer")                      */
/*               -1 if DLL was successfully loaded                          */
/*               operating system-specific error code if not                */
/****************************************************************************/

DLLENTRYPOINT(long) TestLoadLibrary(char * libraryname)
{
  char   msg[512];
  HANDLE hLib = LoadLibrary(libraryname);
  long   rc = -1;

#if defined(WIN32)
  wsprintf(msg, "LoadLibrary(%s) returned %lu", libraryname, (long)hLib);
  if (!hLib) {
    rc = GetLastError();
    wsprintf(msg+strlen(msg), " err=%lu", rc);
  }
  MessageBox(0, msg, "LoadLibrary Result", MB_OK);
  if (hLib)
    FreeLibrary(hLib);
#else
  wsprintf(msg, "LoadLibrary(%s) returned %lu", libraryname, (long)hLib);
  MessageBox(0, msg, "LoadLibrary Result", MB_OK);
  if (hLib >= 32) {  // free up library if loaded OK
    FreeLibrary(hLib);
  } else {
    rc = (long)hLib;
  }
#endif
  return rc;
}

