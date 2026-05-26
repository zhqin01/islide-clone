using System.Runtime.InteropServices;

namespace iSlideAddIn;

// IDTExtensibility2 — dual interface, DISPID-annotated
[ComVisible(true)]
[Guid("B65AD801-ABAF-11D0-BB8A-00A0C90F2744")]
[InterfaceType(ComInterfaceType.InterfaceIsDual)]
public interface IDTExtensibility2
{
    [DispId(1)]
    void OnConnection([MarshalAs(UnmanagedType.IDispatch)] object Application, ext_ConnectMode ConnectMode,
                      [MarshalAs(UnmanagedType.IDispatch)] object AddInInst, ref Array custom);
    [DispId(2)]
    void OnDisconnection(ext_DisconnectMode RemoveMode, ref Array custom);
    [DispId(3)]
    void OnAddInsUpdate(ref Array custom);
    [DispId(4)]
    void OnStartupComplete(ref Array custom);
    [DispId(5)]
    void OnBeginShutdown(ref Array custom);
}

[ComVisible(true)]
public enum ext_ConnectMode { ext_cm_AfterStartup = 0, ext_cm_Startup = 1 }

[ComVisible(true)]
public enum ext_DisconnectMode { ext_dm_HostShutdown = 0, ext_dm_UserClosed = 1 }

// IRibbonExtensibility — IUnknown-based
[ComVisible(true)]
[Guid("000C0396-0000-0000-C000-000000000046")]
[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IRibbonExtensibility
{
    [return: MarshalAs(UnmanagedType.BStr)]
    string GetCustomUI([MarshalAs(UnmanagedType.BStr)] string RibbonID);
}

// IRibbonControl — IDispatch-based
[ComVisible(true)]
[Guid("000C0398-0000-0000-C000-000000000046")]
[InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
public interface IRibbonControl
{
    [DispId(1)]
    string Id { [return: MarshalAs(UnmanagedType.BStr)] get; }
    [DispId(2)]
    object Context { [return: MarshalAs(UnmanagedType.IDispatch)] get; }
    [DispId(3)]
    string Tag { [return: MarshalAs(UnmanagedType.BStr)] get; }
}

[ComVisible(true)]
[ClassInterface(ClassInterfaceType.None)]
[Guid("F1A2B3C4-D5E6-7890-ABCD-EF0123456789")]
[ProgId("iSlideAddIn.Connect")]
public class AddInModule : IDTExtensibility2, IRibbonExtensibility
{
    public static dynamic? PowerPointApp { get; private set; }

    public void OnConnection(object Application, ext_ConnectMode ConnectMode, object AddInInst, ref Array custom)
        => PowerPointApp = Application;
    public void OnDisconnection(ext_DisconnectMode RemoveMode, ref Array custom)
        => PowerPointApp = null;
    public void OnAddInsUpdate(ref Array custom) { }
    public void OnStartupComplete(ref Array custom) { }
    public void OnBeginShutdown(ref Array custom) { }

    public string GetCustomUI(string RibbonID) => RibbonManager.GetRibbonXml();

    public void OnFontAll(object _) => FontManager.ApplyToAll();
    public void OnFontSel(object _) => FontManager.ApplyToSelection();
    public string OnGetTitleFont(object _) => FontManager.TitleFont;
    public string OnGetBodyFont(object _) => FontManager.BodyFont;
    public void OnTitleFontChanged(object _, string t) => FontManager.TitleFont = t;
    public void OnBodyFontChanged(object _, string t) => FontManager.BodyFont = t;
    public void OnParaAll(object _) => ParagraphManager.ApplyToAll();
    public void OnParaSel(object _) => ParagraphManager.ApplyToSelection();
    public string OnGetLineSpacing(object _) => ParagraphManager.LineSpacingText;
    public string OnGetSpaceBefore(object _) => ParagraphManager.SpaceBeforeText;
    public string OnGetSpaceAfter(object _) => ParagraphManager.SpaceAfterText;
    public void OnLineSpacingChanged(object _, string t) => ParagraphManager.LineSpacingText = t;
    public void OnSpaceBeforeChanged(object _, string t) => ParagraphManager.SpaceBeforeText = t;
    public void OnSpaceAfterChanged(object _, string t) => ParagraphManager.SpaceAfterText = t;
    public void OnAlignLeft(object _) => AlignmentManager.Align("left");
    public void OnAlignCenter(object _) => AlignmentManager.Align("center");
    public void OnAlignRight(object _) => AlignmentManager.Align("right");
    public void OnAlignTop(object _) => AlignmentManager.Align("top");
    public void OnAlignMiddle(object _) => AlignmentManager.Align("middle");
    public void OnAlignBottom(object _) => AlignmentManager.Align("bottom");
    public void OnDistH(object _) => AlignmentManager.DistributeHorizontal();
    public void OnDistV(object _) => AlignmentManager.DistributeVertical();
    public void OnSameWidth(object _) => SizeManager.Apply("width");
    public void OnSameHeight(object _) => SizeManager.Apply("height");
    public void OnSameBoth(object _) => SizeManager.Apply("both");
    public void OnMatrixLayout(object _) => LayoutManager.MatrixLayout();
    public void OnCircularLayout(object _) => LayoutManager.CircularLayout();
    public void OnExtractColors(object _) => ColorManager.ExtractColors();
    public void OnSchemeBlue(object _) => ColorManager.ApplyScheme("Material Blue");
    public void OnSchemeGreen(object _) => ColorManager.ApplyScheme("Material Green");
    public void OnSchemeOrange(object _) => ColorManager.ApplyScheme("Material Orange");
    public void OnSchemeCorporate(object _) => ColorManager.ApplyScheme("Corporate Blue");
    public void OnSchemeGray(object _) => ColorManager.ApplyScheme("Corporate Gray");
    public void OnSchemeRed(object _) => ColorManager.ApplyScheme("Warm Red");
    public void OnPastePlace(object _) => PasteSwapManager.PasteInPlace();
    public void OnSwap(object _) => PasteSwapManager.SwapPositions();
    public void OnAddWatermark(object _) => WatermarkManager.ShowDialog();
    public void OnRemoveWatermark(object _) => WatermarkManager.RemoveAll();
    public void OnProtect(object _) => ProtectionManager.ConvertToImages();
    public void OnSlideMgr(object _) => SlideManager.ShowDialog();
    public string OnGetTweenSteps(object _) => TweenManager.StepsText;
    public void OnTweenStepsChanged(object _, string t) => TweenManager.StepsText = t;
    public void OnTween(object _) => TweenManager.Generate();
    public void OnExportImages(object _) => ImageExportManager.ShowExportDialog();
    public void OnExportLongImg(object _) => ImageExportManager.ShowLongImageDialog();
    public void OnCompress(object _) => CompressManager.ShowDialog();
}
