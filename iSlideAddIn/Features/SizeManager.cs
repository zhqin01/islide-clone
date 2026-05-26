namespace iSlideAddIn;
public static class SizeManager
{
    public static void Apply(string m) { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; try { var sel = a.ActiveWindow.Selection; if (sel.Type != 2 || sel.ShapeRange.Count < 2) { W("Select 2+ shapes."); return; } dynamic sr = sel.ShapeRange; int n = sr.Count; if (m == "width" || m == "both") { float mw = 0; for (int i = 1; i <= n; i++) mw = Math.Max(mw, sr[i].Width); for (int i = 1; i <= n; i++) sr[i].Width = mw; } if (m == "height" || m == "both") { float mh = 0; for (int i = 1; i <= n; i++) mh = Math.Max(mh, sr[i].Height); for (int i = 1; i <= n; i++) sr[i].Height = mh; } } catch { } }
    static void W(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
}
