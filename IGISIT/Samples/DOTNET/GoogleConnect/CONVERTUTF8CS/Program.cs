using System;
using System.Text;
using System.Xml;
using System.IO;
using System.Globalization;

namespace MapInfo
{
    public class WriteUTF
    {
        public const int ERROR_SUCCESS = 0;

        //  Return ERROR_SUCCESS if no exception is thrown
        // 
        public static int WriteUTF8(string fnIn, string fnOut)
        {
            int rval = -1;
            try
			{
				System.Xml.XmlDocument doc = new XmlDocument();

                SanitizeXml xml = new SanitizeXml(fnIn, GetEncoding(fnIn));
                
                doc.Load(xml);

                xml.Close();
	
				System.Xml.XmlTextWriter writer = new System.Xml.XmlTextWriter(fnOut, Encoding.UTF8);
	
				doc.Save(writer);
	
                writer.Close();

                rval = ERROR_SUCCESS;
			} 
			catch (Exception ex)
			{
                rval = -1;
                m_errMsg = ex.Message;
                // throw ex;
			}
            return rval;
        }

        public static int GetErrorMessage(ref string str)
        {
            str = m_errMsg;
            return m_errMsg.Length;
        }

        private static Encoding GetEncoding(string fnIn)
        {
            XmlTextReader textReader = new XmlTextReader(fnIn);
            textReader.MoveToContent();
            Encoding encoding = textReader.Encoding;
            textReader.Close();
            return encoding;
        }
		
		public static void ConvertDecimalToString(double dValue, out string sValue)
		{
			sValue = dValue.ToString(CultureInfo.InvariantCulture);
		}
        static string m_errMsg;
    } //WriteUTF

    public class SanitizeXml : StreamReader
    {
        private const int EOF = -1;
        
        public SanitizeXml(string path)
               :base(path, true)
        { }

        public SanitizeXml(string path, Encoding encoding)
            : base(path, encoding)
        { }

        /*--------------------------------------------------------------------------------
         * As per xml specs (http://www.w3.org/TR/REC-xml/#dt-character)the range of
         * characters falling within (0x00-0x08),(0x0B-0x0C) and (0x0E-0x1F) are the
         * invalid characters. 
         *--------------------------------------------------------------------------------*/
        public static bool IsLegalXmlChar(int iChar)
        {
            return
            (
                 iChar == 0x9 /* == '\t' == 9   */        ||
                 iChar == 0xA /* == '\n' == 10  */        ||
                 iChar == 0xD /* == '\r' == 13  */        ||
                (iChar >= 0x20 && iChar <= 0xD7FF) ||
                (iChar >= 0xE000 && iChar <= 0xFFFD) ||
                (iChar >= 0x10000 && iChar <= 0x10FFFF)
           );

        }

        /*--------------------------------------------------------------------------------
        * Function to redirect the TextReader's call to SanitizeXML's Read() function.
        * The following overridden method is the exact copy of Read(char[] buffer, int index, int count)
        * in System.IO.TextReader, extracted by disassembling the mscorlib.lib in .net Refelctor.
        *--------------------------------------------------------------------------------*/
        public override int Read(char[] buffer, int index, int count)
        {
            if (buffer == null)
            {
                throw new ArgumentNullException("buffer");
            }
            if (index < 0)
            {
                throw new ArgumentOutOfRangeException("index");
            }
            if (count < 0)
            {
                throw new ArgumentOutOfRangeException("count");
            }
            if ((buffer.Length - index) < count)
            {
                throw new ArgumentException();
            }
            int num = 0;
            do
            {
                int num2 = this.Read();
                if (num2 == -1)
                {
                    return num;
                }
                buffer[index + num++] = (char)num2;
            }
            while (num < count);
            return num;
        }

        /*--------------------------------------------------------------------------------
        *Overridden function to add sanitizing functionality to StreamReader's Read() function.
        *--------------------------------------------------------------------------------*/
        public override int Read()
        {
            int iNext = base.Read();
            switch (iNext)
            {
                case EOF:
                    return EOF;

                default:
                    return SanitizeXml.IsLegalXmlChar(iNext) ? iNext : 32;
            }
        }
      
    } // SanitizeXML

}   //namespace
