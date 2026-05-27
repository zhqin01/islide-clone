using System.Windows.Forms;
namespace SlideKit.Dialogs;
public class CompressDialog : Form
{
    public int TargetDpi => _cmb.SelectedIndex switch { 0 => 220, 1 => 150, 2 => 96, _ => 150 };
    private readonly ComboBox _cmb;
    public CompressDialog()
    {
        Text = "Compress Presentation"; Width = 330; Height = 150; FormBorderStyle = FormBorderStyle.FixedDialog; MaximizeBox = false; MinimizeBox = false; StartPosition = FormStartPosition.CenterParent;
        var t = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 3, Padding = new Padding(12) };
        t.Controls.Add(new Label { Text = "Level:" }, 0, 0);
        _cmb = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList, Width = 160 };
        _cmb.Items.AddRange(new[] { "Light (220 DPI)", "Normal (150 DPI)", "Aggressive (96 DPI)" }); _cmb.SelectedIndex = 1;
        t.Controls.Add(_cmb, 1, 0);
        t.Controls.Add(new Label { Text = "Reduces image resolution\nin the presentation." }, 0, 1); t.SetColumnSpan(t.Controls[t.Controls.Count - 1], 2);
        var bp = new FlowLayoutPanel { Dock = DockStyle.Bottom, FlowDirection = FlowDirection.RightToLeft, Padding = new Padding(8), Height = 40 };
        var btnOk = new Button { Text = "Compress", Width = 90, DialogResult = DialogResult.OK };
        btnOk.Click += (s, e) => CompressManager.Compress(TargetDpi);
        bp.Controls.Add(btnOk); bp.Controls.Add(new Button { Text = "Cancel", Width = 75, DialogResult = DialogResult.Cancel });
        Controls.Add(t); Controls.Add(bp); AcceptButton = btnOk; CancelButton = bp.Controls[1] as Button;
    }
}
