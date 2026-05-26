using System.Windows.Forms;
namespace iSlideAddIn.Dialogs;
public class WatermarkDialog : Form
{
    public string WatermarkText => _txt.Text;
    public float FontSize => (float)_fs.Value;
    public int WatermarkOpacity => (int)_op.Value;
    public float Rotation => (float)_rot.Value;
    public string ColorHex => $"{_btn.BackColor.R:X2}{_btn.BackColor.G:X2}{_btn.BackColor.B:X2}";
    private readonly TextBox _txt; private readonly NumericUpDown _fs, _op, _rot; private readonly Button _btn;
    public WatermarkDialog()
    {
        Text = "Add Watermark"; Width = 380; Height = 260; FormBorderStyle = FormBorderStyle.FixedDialog; MaximizeBox = false; MinimizeBox = false; StartPosition = FormStartPosition.CenterParent;
        var t = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 6, Padding = new Padding(12) };
        t.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40)); t.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60));
        t.Controls.Add(new Label { Text = "Text:" }, 0, 0); _txt = new TextBox { Text = "Confidential" }; t.Controls.Add(_txt, 1, 0);
        t.Controls.Add(new Label { Text = "Font Size:" }, 0, 1); _fs = new NumericUpDown { Minimum = 8, Maximum = 144, Value = 36, DecimalPlaces = 1 }; t.Controls.Add(_fs, 1, 1);
        t.Controls.Add(new Label { Text = "Opacity %:" }, 0, 2); _op = new NumericUpDown { Minimum = 1, Maximum = 100, Value = 30 }; t.Controls.Add(_op, 1, 2);
        t.Controls.Add(new Label { Text = "Rotation:" }, 0, 3); _rot = new NumericUpDown { Minimum = -180, Maximum = 180, Value = -45, DecimalPlaces = 1 }; t.Controls.Add(_rot, 1, 3);
        t.Controls.Add(new Label { Text = "Color:" }, 0, 4); _btn = new Button { Text = "Pick", BackColor = System.Drawing.Color.FromArgb(153, 153, 153) };
        _btn.Click += (s, e) => { using var cd = new ColorDialog { Color = _btn.BackColor }; if (cd.ShowDialog() == DialogResult.OK) { _btn.BackColor = cd.Color; _btn.Text = $"#{cd.Color.R:X2}{cd.Color.G:X2}{cd.Color.B:X2}"; } };
        t.Controls.Add(_btn, 1, 4);
        var bp = new FlowLayoutPanel { Dock = DockStyle.Bottom, FlowDirection = FlowDirection.RightToLeft, Padding = new Padding(8), Height = 40 };
        bp.Controls.Add(new Button { Text = "Add Watermark", Width = 110, DialogResult = DialogResult.OK });
        bp.Controls.Add(new Button { Text = "Cancel", Width = 75, DialogResult = DialogResult.Cancel });
        Controls.Add(t); Controls.Add(bp); AcceptButton = bp.Controls[0] as Button; CancelButton = bp.Controls[1] as Button;
    }
}
