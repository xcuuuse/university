#include <windows.h>

extern "C" int FAR PASCAL _WEP(int)
{
      /* Your WEP functionality goes here */
 return 1;
}

extern "C" long FAR PASCAL
MyDllFunc(DWORD dwMyValue)
{
  return dwMyValue + 1;
}
