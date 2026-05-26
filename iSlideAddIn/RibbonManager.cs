using System.Reflection;

namespace iSlideAddIn;

public static class RibbonManager
{
    private static string? _cachedXml;

    public static string GetRibbonXml()
    {
        if (_cachedXml != null) return _cachedXml;
        try
        {
            using var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream("iSlideAddIn.Ribbon.xml");
            if (stream != null) { using var r = new StreamReader(stream); _cachedXml = r.ReadToEnd(); return _cachedXml; }
        }
        catch { }
        _cachedXml = @"<customUI xmlns=""http://schemas.microsoft.com/office/2009/07/customui""><ribbon><tabs><tab id=""iSlideTab"" label=""iSlide""><group id=""grpFont"" label=""Font""><button id=""btnTest"" label=""Apply Font"" onAction=""OnFontAll""/></group></tab></tabs></ribbon></customUI>";
        return _cachedXml;
    }
}
