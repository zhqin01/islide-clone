using iSlideAddIn.Dialogs;
namespace iSlideAddIn;
public static class SlideManager
{
    public static void ShowDialog() { if (AddInModule.PowerPointApp?.ActivePresentation == null) return; using var d = new SlideSorterDialog(); d.ShowDialog(); }
    public static void DeleteSlides(List<int> idx) { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; idx.Sort((x, y) => y.CompareTo(x)); foreach (int i in idx) { try { a.ActivePresentation.Slides[i].Delete(); } catch { } } }
    public static void DuplicateSlides(List<int> idx) { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; foreach (int i in idx) { try { a.ActivePresentation.Slides[i].Duplicate(); } catch { } } }
    public static void MoveSlide(int f, int t) { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; try { a.ActivePresentation.Slides[f].MoveTo(t); } catch { } }
}
