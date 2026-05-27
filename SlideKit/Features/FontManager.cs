namespace SlideKit;
public static class FontManager
{
    public static string TitleFont { get; set; } = "Microsoft YaHei";
    public static string BodyFont { get; set; } = "Microsoft YaHei";
    public static void ApplyToAll() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; int c = 0; foreach (dynamic s in a.ActivePresentation.Slides) foreach (dynamic sh in s.Shapes) c += A(sh); M($"Font applied: {c} runs."); }
    public static void ApplyToSelection() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; try { var sel = a.ActiveWindow.Selection; if (sel.Type != 2) return; int c = 0; foreach (dynamic sh in sel.ShapeRange) c += A(sh); M($"Font applied: {c} runs."); } catch { } }
    static int A(dynamic sh) { try { if (sh.HasTextFrame != -1) return 0; if (sh.TextFrame.HasText != -1) return 0; int c = 0; foreach (dynamic p in sh.TextFrame.TextRange.Paragraphs(-1,-1)) foreach (dynamic r in p.Runs(-1,-1)) { try { string? f = r.Font.Size >= 24 ? TitleFont : BodyFont; if (!string.IsNullOrEmpty(f)) { r.Font.Name = f; c++; } } catch { } } return c; } catch { return 0; } }
    static void M(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
}
