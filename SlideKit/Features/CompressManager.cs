using SlideKit.Dialogs;
namespace SlideKit;
public static class CompressManager
{
    public static void ShowDialog() { if (AddInModule.PowerPointApp?.ActivePresentation == null) return; using var d = new CompressDialog(); d.ShowDialog(); }
    public static void Compress(int dpi) { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; try { int p = 0; foreach (dynamic s in a.ActivePresentation.Slides) foreach (dynamic sh in s.Shapes) { try { if (sh.Type == 13) { sh.ScaleHeight(1f, -1); p++; } } catch { } } M($"Processed {p} images."); } catch { } }
    static void M(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
}
