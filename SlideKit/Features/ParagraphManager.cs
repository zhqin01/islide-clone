namespace SlideKit;
public static class ParagraphManager
{
    public static string LineSpacingText { get; set; } = "1.2";
    public static string SpaceBeforeText { get; set; } = "0";
    public static string SpaceAfterText { get; set; } = "6";
    public static void ApplyToAll() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; float.TryParse(LineSpacingText, out float ls); float.TryParse(SpaceBeforeText, out float sb); float.TryParse(SpaceAfterText, out float sa); int c = 0; foreach (dynamic s in a.ActivePresentation.Slides) foreach (dynamic sh in s.Shapes) c += A(sh, ls, sb, sa); M($"Applied to {c} paragraphs."); }
    public static void ApplyToSelection() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; try { var sel = a.ActiveWindow.Selection; if (sel.Type != 2) return; float.TryParse(LineSpacingText, out float ls); float.TryParse(SpaceBeforeText, out float sb); float.TryParse(SpaceAfterText, out float sa); int c = 0; foreach (dynamic sh in sel.ShapeRange) c += A(sh, ls, sb, sa); M($"Applied to {c} paragraphs."); } catch { } }
    static int A(dynamic sh, float ls, float sb, float sa) { try { if (sh.HasTextFrame != -1) return 0; if (sh.TextFrame.HasText != -1) return 0; int c = 0; foreach (dynamic p in sh.TextFrame.TextRange.Paragraphs(-1,-1)) { try { if (ls > 0) p.ParagraphFormat.SpaceWithin = ls; if (sb >= 0) p.ParagraphFormat.SpaceBefore = sb; if (sa >= 0) p.ParagraphFormat.SpaceAfter = sa; c++; } catch { } } return c; } catch { return 0; } }
    static void M(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
}
