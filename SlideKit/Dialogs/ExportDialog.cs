using System.Windows.Forms;
namespace SlideKit.Dialogs;
public class ExportDialog : Form
{
    public string OutputPath => _txt.Text;
    public string Format => _fmt.SelectedItem?.ToString() ?? "PNG";
    public int Dpi => int.TryParse(_dpi.SelectedItem?.ToString(), out int d) ? d : 150;
    public List<int> SelectedSlides { get; } = new();
    private readonly TextBox _txt; private readonly ComboBox _fmt, _dpi; private readonly CheckedListBox _list; private readonly bool _li;
    public ExportDialog(bool longImageMode = false)
    {
        _li = longImageMode; Text = _li ? "Export Long Image" : "Export Slides to Images"; Width = 460; Height = 420; FormBorderStyle = FormBorderStyle.FixedDialog; MaximizeBox = false; MinimizeBox = false; StartPosition = FormStartPosition.CenterParent;
        var ml = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 1, RowCount = 4, Padding = new Padding(12) };
        ml.RowStyles.Add(new RowStyle(SizeType.Absolute, 55)); ml.RowStyles.Add(new RowStyle(SizeType.Absolute, 25)); ml.RowStyles.Add(new RowStyle(SizeType.Percent, 100)); ml.RowStyles.Add(new RowStyle(SizeType.Absolute, 40));
        var sp = new FlowLayoutPanel { FlowDirection = FlowDirection.TopDown, AutoSize = true };
        if (!_li) { var fp = new FlowLayoutPanel(); fp.Controls.Add(new Label { Text = "Format:", Width = 55 }); _fmt = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList, Width = 80 }; _fmt.Items.AddRange(new[] { "PNG", "JPG" }); _fmt.SelectedIndex = 0; fp.Controls.Add(_fmt); sp.Controls.Add(fp); }
        else { _fmt = new ComboBox(); _fmt.Items.Add("PNG"); _fmt.SelectedIndex = 0; }
        var dp = new FlowLayoutPanel(); dp.Controls.Add(new Label { Text = "DPI:", Width = 55 }); _dpi = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList, Width = 80 }; _dpi.Items.AddRange(new[] { "96", "150", "300" }); _dpi.SelectedIndex = 1; dp.Controls.Add(_dpi); sp.Controls.Add(dp);
        ml.Controls.Add(sp, 0, 0);
        ml.Controls.Add(new Label { Text = "Select slides:" }, 0, 1);
        _list = new CheckedListBox { Dock = DockStyle.Fill, CheckOnClick = true }; ml.Controls.Add(_list, 0, 2);
        var pp = new FlowLayoutPanel { Dock = DockStyle.Fill }; pp.Controls.Add(new Label { Text = "Output:", Width = 55 });
        _txt = new TextBox { Width = 230 }; pp.Controls.Add(_txt);
        var bb = new Button { Text = "Browse...", Width = 70 }; bb.Click += (s, e) => {
            if (_li) { using var sd = new SaveFileDialog { Filter = "PNG|*.png|JPG|*.jpg", DefaultExt = "png" }; if (sd.ShowDialog() == DialogResult.OK) _txt.Text = sd.FileName; }
            else { using var fd = new FolderBrowserDialog(); if (fd.ShowDialog() == DialogResult.OK) _txt.Text = fd.SelectedPath; }
        }; pp.Controls.Add(bb); ml.Controls.Add(pp, 0, 3);
        var bp = new FlowLayoutPanel { FlowDirection = FlowDirection.RightToLeft, Height = 40, Dock = DockStyle.Bottom, Padding = new Padding(8) };
        bp.Controls.Add(new Button { Text = "Export", Width = 80, DialogResult = DialogResult.OK });
        bp.Controls.Add(new Button { Text = "Cancel", Width = 75, DialogResult = DialogResult.Cancel });
        Controls.Add(bp); Controls.Add(ml);
        FormClosing += (s, ev) => { if (DialogResult == DialogResult.OK) { SelectedSlides.Clear(); for (int i = 0; i < _list.Items.Count; i++) if (_list.GetItemChecked(i)) SelectedSlides.Add(i + 1); } };
    }
    protected override void OnLoad(EventArgs e) { base.OnLoad(e); _list.Items.Clear(); var a = AddInModule.PowerPointApp; if (a?.ActivePresentation != null) { dynamic pres = a.ActivePresentation; for (int i = 1; i <= pres.Slides.Count; i++) _list.Items.Add($"Slide {i}", true); } }
}
