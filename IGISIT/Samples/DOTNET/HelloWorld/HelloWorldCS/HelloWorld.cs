
using System;
using System.Windows.Forms;

namespace MapInfo.MiPro.Samples
{
    /// <summary>
    /// Sample code demonstrating how to call .Net from MapBasic
    /// </summary>
    public class HelloWorld
    {
        public static void SayHello(String strName)
        {
            // Display a greeting in a standard .Net dialog box 
            MessageBox.Show("Hello, " + strName);
        }
    }
}
