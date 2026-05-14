// ico32.c
//
#include <windows.h>


__declspec( dllexport ) int MyDllFunc(unsigned long dwMyValue)
{
	return dwMyValue + 1;
}
