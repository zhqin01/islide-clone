using System.Windows.Forms;
namespace SlideKit.Dialogs;
public class SlideSorterDialog : Form
{
    private readonly ListBox _lb;
    public SlideSorterDialog()
    {
        Text = "Slide Manager"; Width = 420; Height = 480; StartPosition = FormStartPosition.CenterParent;
        var ml = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 1, RowCount = 2, Padding = new Padding(8) };
        ml.RowStyles.Add(new RowStyle(SizeType.Percent, 100)); ml.RowStyles.Add(new RowStyle(SizeType.Absolute, 50));
        _lb = new ListBox { Dock = DockStyle.Fill, SelectionMode = SelectionMode.MultiExtended }; ml.Controls.Add(_lb, 0, 0);
        var bp = new FlowLayoutPanel { Dock = DockStyle.Fill };
        var bd = new Button { Text = "Delete", Width = 80, ForeColor = System.Drawing.Color.DarkRed }; bd.Click += (s, e) => Del(); bp.Controls.Add(bd);
        var bdup = new Button { Text = "Duplicate", Width = 80 }; bdup.Click += (s, e) => Dup(); bp.Controls.Add(bdup);
        var bu = new Button { Text = "Up", Width = 50 }; bu.Click += (s, e) => Move(-1); bp.Controls.Add(bu);
        var bd2 = new Button { Text = "Down", Width = 50 }; bd2.Click += (s, e) => Move(1); bp.Controls.Add(bd2);
        var bc = new Button { Text = "Close", Width = 60 }; bc.Click += (s, e) => Close(); bp.Controls.Add(bc);
        ml.Controls.Add(bp, 0, 1); Controls.Add(ml);
    }
    protected override void OnLoad(EventArgs e) { base.OnLoad(e); Refresh(); }
    private void R() { _lb.Items.Clear(); var a = AddInModule.PowerPointApp; if (a?.ActivePresentation != null) { dynamic pres = a.ActivePresentation; for (int i = 1; i <= pres.Slides.Count; i++) _lb.Items.Add($"Slide {i}"); } }
    private List<int> Sel() { var r = new List<int>(); foreach (int i in _lb.SelectedIndices) r.Add(i + 1); return r; }
    private void Del() { var idx = Sel(); if (idx.Count == 0) return; if (MessageBox.Show($"Delete {idx.Count} slide(s)?", "Confirm", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) == DialogResult.Yes) { SlideManager.DeleteSlides(idx); R(); } }
    private void Dup() { var idx = Sel(); if (idx.Count > 0) { SlideManager.DuplicateSlides(idx); R(); } }
    private void Move(int d) { var idx = Sel(); if (idx.Count != 1) return; int to = idx[0] + d; if (to < 1) return; var a = AddInModule.PowerPointApp; if (a?.ActivePresentation != null && to <= ((dynamic)a.ActivePresentation).Slides.Count) { SlideManager.MoveSlide(idx[0], to); R(); } }
}
