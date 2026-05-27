using System.Windows.Forms;
namespace SlideKit.Dialogs;
public class CircularLayoutDialog : Form
{
    public float Radius => (float)_r.Value;
    public float StartAngle => (float)_sa.Value;
    public bool Clockwise => _cw.Checked;
    private readonly NumericUpDown _r, _sa;
    private readonly CheckBox _cw;
    public CircularLayoutDialog()
    {
        Text = "Circular Layout"; Width = 300; Height = 190; FormBorderStyle = FormBorderStyle.FixedDialog; MaximizeBox = false; MinimizeBox = false; StartPosition = FormStartPosition.CenterParent;
        var t = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 3, Padding = new Padding(12) };
        t.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50)); t.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
        t.Controls.Add(new Label { Text = "Radius (pt):" }, 0, 0); _r = new NumericUpDown { Minimum = 10, Maximum = 1000, Value = 200, DecimalPlaces = 1 }; t.Controls.Add(_r, 1, 0);
        t.Controls.Add(new Label { Text = "Start Angle:" }, 0, 1); _sa = new NumericUpDown { Minimum = 0, Maximum = 360, Value = 0, DecimalPlaces = 1 }; t.Controls.Add(_sa, 1, 1);
        _cw = new CheckBox { Text = "Clockwise", Checked = true }; t.Controls.Add(_cw, 1, 2);
        var bp = new FlowLayoutPanel { Dock = DockStyle.Bottom, FlowDirection = FlowDirection.RightToLeft, Padding = new Padding(8), Height = 40 };
        bp.Controls.Add(new Button { Text = "OK", Width = 75, DialogResult = DialogResult.OK });
        bp.Controls.Add(new Button { Text = "Cancel", Width = 75, DialogResult = DialogResult.Cancel });
        Controls.Add(t); Controls.Add(bp); AcceptButton = bp.Controls[0] as Button; CancelButton = bp.Controls[1] as Button;
    }
}
