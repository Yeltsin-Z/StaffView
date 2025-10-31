# ⚡ StaffView - Usage Guide

*Gandalf's tool for regression clarity*

## Quick Start

1. **Start the server**:
   ```bash
   ./start.sh
   ```

2. **Open your browser** to: `http://localhost:5001`

3. **Upload Your Artifacts**:
   - Drag & drop a ZIP file, or
   - Click to browse for a file, or
   - Use the sample artifacts button

4. **Start Comparing!** 🎉

---

## Understanding the Interface

### Left Sidebar
- **Tenant Groups**: Artifacts are organized by tenant ID (e.g., 508, 561, 580)
- **File Counts**: Each tenant shows how many file pairs it contains
- **File Items**: Click any file to view its comparison
- **Active Highlight**: The selected file is highlighted in purple

### Main Comparison Area

#### Legend (Top Bar)
- ⬜ **Unchanged**: Lines that are identical in both versions
- 🟨 **Modified**: Lines that exist in both but have different values  
- 🟦 **Added in Feat**: Lines only present in the feature branch
- 🟥 **Removed in Feat**: Lines only present in the main branch

#### Statistics Dashboard
Shows real-time comparison metrics:
- **Unchanged**: Number of identical lines
- **Modified**: Number of changed lines
- **Added**: Lines added in feature branch
- **Removed**: Lines removed in feature branch
- **Total Lines**: Total line count

#### Comparison View
Three-column layout:
1. **Line Numbers**: For easy reference
2. **Main Branch**: Baseline (production) data
3. **Feature Branch**: New changes being tested

---

## Common Workflows

### 1. Review All Changes in a Tenant

```
1. Click on a tenant header (e.g., "📁 Tenant 508")
2. Browse through each file in that tenant
3. Look for patterns in the differences
```

### 2. Spot Critical Changes

Look for rows highlighted in **yellow** (modified) - these show where values changed between branches. The tool highlights the specific cells that differ, making it easy to spot exactly what changed.

### 3. Identify Added/Removed Data

- **Blue rows**: New data in the feature branch
- **Red rows**: Data removed from main branch

---

## Understanding Your Artifact Files

### File Naming Convention
Files follow the pattern: `{ID}-{branch}`

Examples:
- `CHART-426-feat` → Feature branch version
- `CHART-426-main` → Main/production branch version

### File Structure
Your artifacts contain CSV-formatted data with metrics:
```
metrics.ARR_Bookings_ASP1,Actual,,R,r,,,1447.718
metrics.ARR_Bookings_ASP1,Actual,,R,r,,Product_Line=Performance Reporting,5408.564
```

The tool automatically:
- Parses CSV structure
- Compares line-by-line
- Highlights cell-level differences
- Calculates statistics

---

## Tips & Best Practices

### 🎯 Efficient Review Process
1. Start with folders that have the most files
2. Look at the statistics first - high modification counts need more attention
3. Use the visual highlighting to quickly scan for differences

### 🔍 Finding Specific Issues
- Modified lines (yellow) = Value changes to investigate
- Added lines (blue) = New data to validate
- Removed lines (red) = Missing data to check

### 📊 Interpreting Results

**All lines modified (10/10 modified)**:
- Systematic changes across all metrics
- May indicate calculation formula changes

**Mixed results (some unchanged, some modified)**:
- Selective changes to specific metrics
- More targeted impact

**No unchanged lines**:
- Complete data refresh or restructure
- Requires thorough validation

---

## Keyboard Shortcuts

- **PageDown / PageUp**: Scroll through comparisons
- **Home / End**: Jump to top/bottom of comparison
- **Tab**: Navigate through the interface

---

## Troubleshooting

### Server won't start
```bash
# Check if port 5001 is available
lsof -i :5001

# If busy, kill the process or change port in app.py
```

### No artifacts showing
1. Verify the `ARTIFACTS_DIR` path in `app.py`
2. Check that artifacts are unzipped
3. Ensure folder structure matches: `folder_id/FILE-feat` and `FILE-main`

### Comparison not loading
1. Check browser console for errors (F12)
2. Verify both `-feat` and `-main` files exist
3. Ensure files are readable (check permissions)

---

## Advanced Configuration

### Change Artifacts Directory

Edit `app.py` line 16:
```python
ARTIFACTS_DIR = Path("/your/custom/path/to/artifacts")
```

### Change Port

Edit `app.py` line 225:
```python
app.run(debug=True, port=YOUR_PORT)
```

### Upload New Artifacts

The tool supports ZIP file uploads (feature planned for future release):
```python
# Future: Upload via web interface
POST /api/upload
```

---

## Support & Feedback

If you encounter issues or have suggestions:
1. Check the main `README.md` for installation help
2. Review `server.log` for error messages
3. Verify your artifact file structure matches the expected format

---

## Next Steps

After comparing artifacts:
1. Document significant differences
2. Investigate unexpected changes
3. Validate feature branch behavior
4. Approve or request fixes based on findings

**Happy Comparing!** 🔍✨

