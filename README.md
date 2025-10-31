# ⚡ StaffView

**Gandalf's tool for regression clarity**

A powerful web-based tool to compare regression test artifacts from GitHub Actions side by side. Compare, analyze, and illuminate test differences with wizard-like clarity.

## ✨ Features

- ⚡ **Artifact Upload**: Drag-and-drop or browse to upload GitHub Actions artifacts
- 📦 **Automatic Parsing**: Extracts and organizes artifact files by tenant
- 🔍 **Side-by-Side Comparison**: View differences between feature and main branches
- 🎨 **Visual Diff Highlighting**: Color-coded changes (added, removed, modified)
- 📊 **Statistics Dashboard**: Quick overview of changes
- 🎯 **Cell-Level Diff Detection**: Highlights specific cells that changed in CSV files
- 🪄 **Modern UI**: Beautiful, responsive interface with wizard-like clarity

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

**Quick Start** (Recommended):
```bash
./start.sh
```

**Or manually**:
```bash
source venv/bin/activate
python app.py
```

The server will start at `http://localhost:5001`

### Using the Tool

1. **Open your browser** and navigate to `http://localhost:5001`

2. **Upload or Select Artifacts:**
   - **Option 1**: Drag and drop your artifact ZIP file into the upload area
   - **Option 2**: Click the upload area to browse and select a ZIP file
   - **Option 3**: Click "🚀 Use Sample Artifacts" to load the example data

3. **Compare Files:**
   - After loading artifacts, you'll be redirected to the comparison interface
   - Browse the sidebar to see all available tenant folders
   - Click on any file to see the side-by-side comparison
   - Use the "← Dashboard" button to return and upload different artifacts

4. **View the differences**:
   - 🟢 **Green stats** = Unchanged lines
   - 🟡 **Yellow highlighting** = Modified lines
   - 🔵 **Blue highlighting** = Lines added in feature branch
   - 🔴 **Red highlighting** = Lines removed in feature branch

### Artifact Structure

The tool expects artifacts in the following structure:
```
regression-diffs/
├── 508/
│   ├── CHART-426-feat
│   ├── CHART-426-main
│   ├── CHART-481-feat
│   └── CHART-481-main
├── 561/
│   ├── CHART-2431-feat
│   └── CHART-2431-main
└── ...
```

Each folder contains pairs of files:
- `*-feat`: Results from the feature branch
- `*-main`: Results from the main/master branch

## Configuration

By default, the tool looks for artifacts in:
```
/Users/yeltsinz/Downloads/regression-diffs (1)
```

To change this, modify the `ARTIFACTS_DIR` variable in `app.py`:

```python
ARTIFACTS_DIR = Path("/path/to/your/artifacts")
```

## File Format Support

The tool supports CSV-like files with comma-separated values. Example:
```csv
metrics.ARR_Bookings_ASP1,Actual,,R,r,,,1447.718
metrics.ARR_Bookings_ASP1,Actual,,R,r,,Product_Line=Performance Reporting,5408.564
```

## Features Explained

### Statistics Dashboard
Shows at-a-glance metrics:
- **Total Lines**: Total number of lines across both files
- **Unchanged**: Lines that are identical in both versions
- **Modified**: Lines that exist in both but have different values
- **Added**: Lines only in the feature branch
- **Removed**: Lines only in the main branch

### Cell-Level Differences
For modified lines, individual cells that differ are highlighted in yellow, making it easy to spot exactly what changed.

### Tenant Organization
Artifacts are organized by tenant ID (e.g., 508, 561), making it easy to group related comparisons together.

## Troubleshooting

### No artifacts found
- Check that the `ARTIFACTS_DIR` path is correct
- Ensure the artifact has been unzipped
- Verify the folder structure matches the expected format

### Port already in use
If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Modern gradient design with smooth animations

## Future Enhancements

- [ ] Upload artifacts directly through the web interface
- [ ] Export comparison reports as PDF/HTML
- [ ] Support for other file formats (JSON, XML)
- [ ] Advanced filtering and search
- [ ] Comparison history

## 🚀 Production Deployment

StaffView is production-ready! Multiple deployment options available:

### Quick Production Start
```bash
# Using Gunicorn (recommended for production)
gunicorn --config gunicorn_config.py app:app
```

### AWS EC2 Deployment (Recommended ⭐)

**Automated Deployment:**
```bash
# On your EC2 instance, after cloning the repository:
./deploy-ec2.sh
```

**Update Existing Deployment:**
```bash
# Pull latest changes and restart
./update-ec2.sh
```

**See [AWS_EC2_DEPLOYMENT.md](AWS_EC2_DEPLOYMENT.md) for complete guide** including:
- Step-by-step EC2 setup
- Nginx configuration
- SSL/HTTPS with Let's Encrypt
- Systemd service management
- Security and monitoring
- Troubleshooting

### Other Deployment Options
- **Render** - Easy deployment with free HTTPS
- **Heroku** - Simple git push deployment
- **Google Cloud Run** - Serverless container deployment
- **DigitalOcean** - App Platform auto-deployment
- **Railway** - Git-based deployment

---

## License

MIT License - feel free to use and modify as needed.

