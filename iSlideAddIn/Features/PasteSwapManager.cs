namespace iSlideAddIn;
public static class PasteSwapManager
{
    public static void PasteInPlace() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; try { a.CommandBars.ExecuteMso("PasteSourceFormatting"); } catch { } }
    public static void SwapPositions() { var a = AddInModule.PowerPointApp; if (a?.ActivePresentation == null) return; try { var sel = a.ActiveWindow.Selection; if (sel.Type != 2 || sel.ShapeRange.Count != 2) { W("Select 2 shapes."); return; } float l1 = sel.ShapeRange[1].Left, t1 = sel.ShapeRange[1].Top; sel.ShapeRange[1].Left = sel.ShapeRange[2].Left; sel.ShapeRange[1].Top = sel.ShapeRange[2].Top; sel.ShapeRange[2].Left = l1; sel.ShapeRange[2].Top = t1; } catch { } }
    static void W(string m) => System.Windows.Forms.MessageBox.Show(m, "iSlide", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
}
