using iSlideAddIn.Dialogs;
namespace iSlideAddIn;
public static class WatermarkManager
{
    const string P = "_islide_wm_";
    public static void ShowDialog() { if (AddInModule.PowerPointApp?.ActivePresentation == null) return; using var d = new WatermarkDialog(); if (d.ShowDialog() != System.Windows.Forms.DialogResult.OK) return; Add(d.WatermarkText, d.FontSize, d.WatermarkOpacity, d.Rotation, d.ColorHex); }
    public static void Add(string t, float fs, int op, float rot, string ch) { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; int r = Convert.ToInt32(ch.Substring(0, 2), 16), g = Convert.ToInt32(ch.Substring(2, 2), 16), b = Convert.ToInt32(ch.Substring(4, 2), 16), n = 0; dynamic pres = a.ActivePresentation; float pw = pres.PageSetup.SlideWidth, ph = pres.PageSetup.SlideHeight; foreach (dynamic s in pres.Slides) { try { dynamic sh = s.Shapes.AddTextbox(1, pw * 0.1f, ph * 0.4f, pw * 0.8f, ph * 0.2f); sh.Name = P + s.SlideIndex; sh.Rotation = rot; sh.Fill.Transparency = 1f - (op / 100f); dynamic tf = sh.TextFrame; tf.TextRange.Text = t; tf.TextRange.Font.Name = "Microsoft YaHei"; tf.TextRange.Font.Size = fs; tf.TextRange.Font.Color.RGB = (b << 16) | (g << 8) | r; tf.TextRange.ParagraphFormat.Alignment = 2; n++; } catch { } } M($"Added watermark to {n} slides."); }
    public static void RemoveAll() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; int n = 0; foreach (dynamic s in a.ActivePresentation.Slides) { var td = new List<dynamic>(); foreach (dynamic sh in s.Shapes) { try { if (((string)sh.Name).StartsWith(P)) td.Add(sh); } catch { } } foreach (var sh in td) { try { sh.Delete(); n++; } catch { } } } M($"Removed {n} watermarks."); }
    static void M(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
}
