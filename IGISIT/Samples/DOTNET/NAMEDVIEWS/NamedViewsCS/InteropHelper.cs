using System;
using System.Windows.Forms;
using MapInfo.MiPro.Interop;

namespace MISamples
{
	static class InteropHelper
	{

		#region [GET APP VERSION]

		private const int SYS_INFO_APPVERSION = 2; // Used with SystemInfo to get appversion

		/// <summary>
		/// Gets the MapInfo Professional version number
		/// </summary>
		/// <returns>Version number (multiplied by 100) as string</returns>
		public static string GetAppVersion()
		{
			string expr = string.Format("SystemInfo({0})", SYS_INFO_APPVERSION);
			return InteropServices.MapInfoApplication.Eval(expr);
		}

		#endregion

		#region [GET FRONT WINDOW]

		/// <summary>
		/// Get front window (child window) from the running instance of MapInfo Professional
		/// </summary>
		/// <returns>Id of the front window</returns>
		private static int GetFrontWindow()
		{
			string evalResult = InteropServices.MapInfoApplication.Eval("FrontWindow()");
			return Int32.Parse(evalResult);
			
		}

		#endregion

		#region [GET WINDOW INFORMATION]

		private const int WIN_INFO_TYPE = 3; // Used with WindowInfo to get win type

		/// <summary>
		/// Returns window type for given window id.
		/// </summary>
		/// <param name="windowId"></param>
		/// <returns>Window type</returns>
		private static int GetWindowType(int windowId)
		{
			// make sure the front window is a mapper
			string expr = string.Format("WindowInfo({0}, {1})", windowId, WIN_INFO_TYPE);
			string evalResult = InteropServices.MapInfoApplication.Eval(expr);
			return Int32.Parse(evalResult);
		}



		#endregion

		#region [GET MAPPER INFORMATION]

		private const int MAPPER_INFO_ZOOM = 1;    // Used with MapperInfo to get zoom
		private const int MAPPER_INFO_CENTERX = 3; // Used with MapperInfo to get center X
		private const int MAPPER_INFO_CENTERY = 4; // Used with MapperInfo to get center Y
		private const int MAPPER_INFO_DISTUNITS = 12; // Used with MapperInfo to get distance units e.g. "mi" 
		private const int MAPPER_INFO_COORDSYS_CLAUSE_WITH_BOUNDS = 22; // Used with MapperInfo to get a CoordSys string


		/// <summary>
		/// Gets the view information from a mapper window in
		/// MapInfo Professional application
		/// </summary>
		/// <remarks>
		/// MapBasic's MapperInfo function can return numeric information
		/// such as Zoom width.  However, MapInfoApplication.Eval returns 
		/// results as strings, so if you request numeric information such
		/// as MAPPER_INFO_ZOOM, Eval will return a string such as "1234.5"
		/// (with a period as the decimal separator, regardless of 
		/// the user's regional settings).  
		/// 
		/// Instead of parsing such String results into Double values, we 
		/// will return the String results.  The string representation
		/// of numeric values is ideal for this application, because the 
		/// string formatting returned by the Eval method (i.e. always using 
		/// the period as the decimal separator) is appropriate for use  
		/// in the Set Map statement we will be constructing later on. 
		/// </remarks>
		/// <param name="windowId">identification number of mapper window</param>
		/// <param name="infoType">The type of information</param>
		/// <returns>The requested information</returns>
		private static string GetMapperInfo(int windowId, int infoType)
		{
			string expr, evalResult;

			expr = string.Format("MapperInfo({0}, {1})", windowId, infoType);
			evalResult = InteropServices.MapInfoApplication.Eval(expr);
			return evalResult;
		}

		/// <summary>
		/// Get a string representing the coordinate system of the map window
		/// </summary>
		/// <param name="windowId">identification number of mapper window</param>
		/// <returns>a CoordSys clause string</returns>
		public static string GetMapperCoordSys(int windowId)
		{
			string expr;

			expr = string.Format("MapperInfo({0}, {1})", windowId, MAPPER_INFO_COORDSYS_CLAUSE_WITH_BOUNDS);
			return InteropServices.MapInfoApplication.Eval(expr);
		}

		/// <summary>
		/// Get a string representing the distance unit in use in a specific map window
		/// </summary>
		/// <param name="windowId">identification number of mapper window</param>
		/// <returns></returns>
		public static string GetMapperDistanceUnit(int windowId)
		{
			string expr;

			expr = string.Format("MapperInfo({0}, {1})", windowId, MAPPER_INFO_DISTUNITS);
			return InteropServices.MapInfoApplication.Eval(expr);
		}

		/// <summary>
		/// Gets mapper window zoom value
		/// </summary>
		/// <param name="windowId">identification number of mapper window</param>
		/// <returns>Zoom value of mapper window's current view</returns>
		public static string GetMapperZoom(int windowId)
		{
			return GetMapperInfo(windowId, MAPPER_INFO_ZOOM);
		}

		/// <summary>
		/// Gets mapper window center X value
		/// </summary>
		/// <param name="windowId">window identification number of mapper window</param>
		/// <returns>Center Y of mapper window's current view</returns>
		public static string GetMapperCenterX(int windowId)
		{
			return GetMapperInfo(windowId, MAPPER_INFO_CENTERX);
		}

		/// <summary>
		/// Gets mapper window center Y value
		/// </summary>
		/// <param name="windowId">window identification number of mapper window</param>
		/// <returns>Center X of mapper window's current view</returns>
		public static string GetMapperCenterY(int windowId)
		{
			return GetMapperInfo(windowId, MAPPER_INFO_CENTERY);
		}

		/// <summary>
		/// Gets a string representing MapInfo's current distance units, such as mi or km. 
		/// Defaults to "mi" but can be reset through the Set Distance Units statement. 
		/// </summary>
		/// <returns>A unit string such as mi or km</returns>
		public static string GetSessionDistanceUnit()
		{
			// Use SessionInfo(SESSION_INFO_DISTANCE_UNITS) to get the unit string
			return InteropServices.MapInfoApplication.Eval("SessionInfo(2)");
		}

		/// <summary>
		/// Sets MapInfo's current distance unit, such as mi or km.   Has the same effect
		/// as typing a Set Distance Units statement into the MapBasic window. 
		/// </summary>
		/// <param name="unit">a distance unit string, such as mi or km</param>
		public static void SetSessionDistanceUnit(string unit)
		{
			string expr;

			expr = string.Format("Set Distance Units \"{0}\"", unit);
			InteropServices.MapInfoApplication.Do(expr);
		}

		/// <summary>
		/// Get a string representing the CoordSys clause of the coordinate system 
		/// that is currently in effect. 
		/// </summary>
		/// <returns>string such as "CoordSys Earth" </returns>
		public static string GetSessionCoordSys()
		{
			// Make note of the current MapBasic Coordinate System SessionInfo(SESSION_INFO_COORDSYS_CLAUSE) 
			return InteropServices.MapInfoApplication.Eval("SessionInfo(1)"); 
		}

		/// <summary>
		/// Set the current coordinate system.  Has the same effect as typing 
		/// a Set CoordSys statement into the MapBasic window. 
		/// </summary>
		/// <param name="csys">string such as "CoordSys Earth"</param>
		public static void SetSessionCoordSys(string csys)
		{
			InteropServices.MapInfoApplication.Do(string.Format("Set {0}", csys));
		}

		/// <summary>
		/// Given a string representation of a number, in invariant formatting 
		/// (always using the period as the decimal separator), return a  
		/// string formatted according to the user's current system settings. 
		/// </summary>
		/// <remarks>
		/// The resulting number string is appropriate for displaying numbers 
		/// in the user interface, but not appropriate for constructing MapBasic 
		/// statements.  When you construct a MapBasic statement string (to 
		/// be executed through a call to the Do method), any numeric literals
		/// in the string must use period as the decimal separator, even if 
		/// the user's system's regional settings use some other character 
		/// as the decimal separator. 
		/// </remarks>
		/// <param name="numericString">A number string with period (.) as the decimal separator, if any</param>
		/// <returns>A number string with a decimal separator based on the user's system settings</returns>
		public static string GetFormattedString(string numericString)
		{
			return InteropServices.MapInfoApplication.Eval(string.Format("FormatNumber$({0})", numericString)); 
		}

		#endregion

		#region [SET CURRENT VIEW OF MAPPER WINDOW]

		/// <summary>
		/// Sets the current view of mapper window represented by windowId
		/// </summary>
		/// <param name="windowId">Window identification number of mapper window</param>
		/// <param name="centerX">New center X of the mapper window</param>
		/// <param name="centerY">New center Y of the mapper window</param>
		/// <param name="mapperZoom">New zoom of the mapper window</param>
		/// <param name="unit">Distance unit string that applies to mapperZoom, such as mi or km</param>
		/// <param name="csys">CoordSys string that specifies the coordinate system used by the X/Y arguments</param>
		public static void SetView(int windowId, string centerX, string centerY, string mapperZoom, string unit, string csys)
		{
			// Before we do any work involving the map's X/Y coordinates, we
			// will set the current coordinate system; that way, we will guarantee 
			// that the coordinates will be processed correctly, regardless of which
			// coordinate system is in use in the current map. 
			// But, before we set the coordinate system, make note of the current 
			// coordinate system, so that we can restore it later.  This way, in
			// the unlikely event that the user typed a Set CoordSys statement into 
			// the MapBasic window, we will preserve the coordsys typed in by the user. 

			// Make note of the current MapBasic Coordinate System, equivalent
			// to calling:  SessionInfo(SESSION_INFO_COORDSYS_CLAUSE) 
			string oldCoordSys = GetSessionCoordSys();  

			// Set the coordsys clause to the csys that was saved with the named view 
			SetSessionCoordSys(csys);  

			// Set the map view 
			string setMapStatement = string.Format(
				"Set Map Window {0} Center ( {1}, {2} ) Zoom {3} Units \"{4}\"", 
					windowId, centerX, centerY, mapperZoom, unit);

			InteropServices.MapInfoApplication.Do(setMapStatement); 

			// Restore the MapBasic Coordinate System to its previous state 
			SetSessionCoordSys(oldCoordSys); 
		}

		#endregion

		#region [GET MAPPER WINDOW IDENTIFICATION NUMBER]

		/// <summary>
		/// Get the ID of the front window.  Displays a message
		/// and returns 0 if there is no window open, or the 
		/// front window is not a mapper
		/// </summary>
		/// <returns></returns>
		public static int GetMapWindowId()
		{
			int windowId = GetFrontWindow();
			// Make sure we have a window
			if (windowId == 0)
			{
				MessageBox.Show(Properties.Resources.ERR_NO_WIN_OPEN);
				return 0;
			}

			int windowType = GetWindowType(windowId); ;
			// Make sure if front window is a mapper window
			if (windowType != 1)
			{
				MessageBox.Show(Properties.Resources.ERR_FRONT_WIN_NOT_MAPPER);
				return 0;
			}

			return windowId;
		}

		#endregion

	}
}
