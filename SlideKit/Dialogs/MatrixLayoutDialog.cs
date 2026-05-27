using System.Windows.Forms;
namespace SlideKit.Dialogs;
public class MatrixLayoutDialog : Form
{
    public int Columns => (int)_c.Value;
    public float HorizontalGap => (float)_hg.Value;
    public float VerticalGap => (float)_vg.Value;
    private readonly NumericUpDown _c, _hg, _vg;
    public MatrixLayoutDialog()
    {
        Text = "Matrix Layout"; Width = 300; Height = 190; FormBorderStyle = FormBorderStyle.FixedDialog; MaximizeBox = false; MinimizeBox = false; StartPosition = FormStartPosition.CenterParent;
        var t = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 4, Padding = new Padding(12) };
        t.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50)); t.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
        t.Controls.Add(new Label { Text = "Columns:" }, 0, 0); _c = new NumericUpDown { Minimum = 1, Maximum = 20, Value = 3 }; t.Controls.Add(_c, 1, 0);
        t.Controls.Add(new Label { Text = "H-Gap (pt):" }, 0, 1); _hg = new NumericUpDown { Minimum = 0, Maximum = 500, Value = 20, DecimalPlaces = 1 }; t.Controls.Add(_hg, 1, 1);
        t.Controls.Add(new Label { Text = "V-Gap (pt):" }, 0, 2); _vg = new NumericUpDown { Minimum = 0, Maximum = 500, Value = 20, DecimalPlaces = 1 }; t.Controls.Add(_vg, 1, 2);
        var bp = new FlowLayoutPanel { Dock = DockStyle.Bottom, FlowDirection = FlowDirection.RightToLeft, Padding = new Padding(8), Height = 40 };
        bp.Controls.Add(new Button { Text = "OK", Width = 75, DialogResult = DialogResult.OK });
        bp.Controls.Add(new Button { Text = "Cancel", Width = 75, DialogResult = DialogResult.Cancel });
        Controls.Add(t); Controls.Add(bp); AcceptButton = bp.Controls[0] as Button; CancelButton = bp.Controls[1] as Button;
    }
}
