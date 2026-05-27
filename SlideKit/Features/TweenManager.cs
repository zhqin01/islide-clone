namespace SlideKit;
public static class TweenManager
{
    public static string StepsText { get; set; } = "5";
    public static void Generate() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; if (!int.TryParse(StepsText, out int st) || st < 1 || st > 20) { W("Steps: 1-20."); return; } try { var sel = a.ActiveWindow.Selection; if (sel.Type != 2 || sel.ShapeRange.Count != 2) { W("Select 2 shapes."); return; } dynamic s1 = sel.ShapeRange[1], s2 = sel.ShapeRange[2]; int si = a.ActiveWindow.Selection.SlideRange.SlideIndex; dynamic slide = a.ActivePresentation.Slides[si]; int c = 0; for (int i = 1; i <= st; i++) { float t = (float)i / (st + 1); s1.Copy(); dynamic p = slide.Shapes.Paste(); p.Left = s1.Left + (s2.Left - s1.Left) * t; p.Top = s1.Top + (s2.Top - s1.Top) * t; p.Width = s1.Width + (s2.Width - s1.Width) * t; p.Height = s1.Height + (s2.Height - s1.Height) * t; p.Rotation = s1.Rotation + (s2.Rotation - s1.Rotation) * t; c++; } M($"Generated {c} shapes."); } catch (Exception ex) { W($"Error: {ex.Message}"); } }
    static void W(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
    static void M(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
}
