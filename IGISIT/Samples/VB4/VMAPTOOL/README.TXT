Visual Map Tools Sample
-----------------------
10/26/95
-----------------------

Purpose:
--------
  The purpose of this sample is to demonstrate some of the more advanced
capabilities of the Integrated Mapping feature available in MapInfo 4.0,
and how to use them from Visual Basic 4.0. Some of these advanced features
include:
  *   Setting up an OLE automation object in the VB app for MapInfo
      to call back to when menu items and toolbuttons are used, as
      as well as when special events occur ( such as the contents of
      a window changing, or the MapInfo's status bar text changes ).

  *   Getting MapInfo to resize a reparented window when its parent
      ( in this case, a VB PictureBox control ) is resized. This requires
      a call to the Windows API function, MoveWindow().

  *   Using the new MapBasic Search functions ( SearchPoint(),
      SearchRect(), and SearchInfo() ) to simulate the capabilities of
      the info tool.

  For more details on these capabilities, look at the code and comments
in this project, and for further information, check out Chapter 13 in the
MapBasic User's Guide, "Integrated Mapping".

Requirements:
-------------
  Due to the use of Win95 custom controls and the creation of OLE
automation objects in VB, you must be running:
  *   32-bit Visual Basic 4.0 Professional ( or Enterprise )
  *   Windows 95 or Windows NT 3.5.1
