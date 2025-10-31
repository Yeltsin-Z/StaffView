# ⚡ StaffView Dashboard Guide

**Gandalf's tool for regression clarity**

## Overview

StaffView features a beautiful dashboard landing page that allows you to easily upload and manage your GitHub Actions artifacts before comparing them with wizard-like clarity.

---

## Dashboard Features

### 🎯 Landing Page

When you navigate to `http://localhost:5001`, you'll see the dashboard with:

1. **Welcome Section**: Clear instructions on how to get started
2. **Upload Area**: Drag-and-drop zone for ZIP files
3. **Sample Artifacts Button**: Quick access to test data
4. **Feature Highlights**: Overview of tool capabilities

---

## How to Upload Artifacts

### Method 1: Drag and Drop 🎯

1. Download your artifact ZIP from GitHub Actions
2. Open `http://localhost:5001` in your browser
3. Drag the ZIP file to the dashed upload area
4. Drop it when you see the area highlight green
5. Wait for automatic extraction and processing
6. You'll be redirected to the comparison view automatically

### Method 2: Click to Browse 📁

1. Open `http://localhost:5001`
2. Click anywhere on the dashed upload area
3. Select your artifact ZIP file from the file browser
4. Wait for processing
5. Automatic redirect to comparison view

### Method 3: Use Sample Artifacts 🚀

1. Open `http://localhost:5001`
2. Click the "🚀 Use Sample Artifacts" button
3. Instantly loads pre-configured sample data
4. Perfect for testing and demonstration

---

## Upload Process

### What Happens During Upload?

1. **Validation**: Checks that the file is a valid ZIP
2. **Upload**: Transfers file to server
3. **Extraction**: Unzips artifact contents
4. **Organization**: Structures data by tenant ID
5. **Verification**: Counts and validates file pairs
6. **Redirect**: Automatically opens comparison interface

### Visual Feedback

- **Progress Bar**: Shows upload/extraction progress
- **Status Messages**: Clear feedback at each stage
- **Error Handling**: Helpful messages if something goes wrong
- **Success Notification**: Confirmation before redirect

---

## Expected Artifact Structure

Your uploaded ZIP should contain the following structure:

```
regression-diffs.zip
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

### File Naming Requirements

- Files must be paired: `{ID}-feat` and `{ID}-main`
- **-feat**: Feature branch version
- **-main**: Main/production branch version
- Folder names become tenant IDs (e.g., 508, 561)

---

## Navigation

### Dashboard to Comparison

- Upload artifact → Automatic redirect
- Use sample → Automatic redirect

### Comparison to Dashboard

- Click "← Dashboard" button in the top-left corner
- Upload different artifacts
- Switch between datasets

---

## Dashboard UI Elements

### Upload Area States

1. **Default (Blue Dashed Border)**
   - Hover: Slight color change and lift effect
   - Ready to receive files

2. **Drag Over (Green Solid Border)**
   - Indicates file is being dragged over
   - Safe to drop

3. **Processing (Disabled)**
   - Slightly faded
   - Progress bar visible
   - Cannot interact until complete

4. **Success (Green)**
   - Checkmark icon
   - Success message
   - Countdown to redirect

5. **Error (Red)**
   - Error icon
   - Descriptive error message
   - Upload area re-enabled

---

## Features Showcase

The dashboard highlights three key features:

### 🔄 Side-by-Side Comparison
Compare main vs feature branches in a dual-column layout

### 🎨 Visual Diffs
Color-coded highlighting for instant change recognition:
- Yellow: Modified
- Blue: Added
- Red: Removed
- Gray: Unchanged

### 📊 Statistics
Instant summary of changes with real-time counts

---

## Technical Details

### API Endpoints Used

**POST `/api/upload`**
- Accepts: `multipart/form-data` with ZIP file
- Returns: Success status and artifact count
- Handles: Extraction and organization

**GET `/api/use-sample`**
- Loads pre-configured sample directory
- Returns: Success status and artifact count
- No file upload required

### Session Management

- Uploaded artifacts persist for the server session
- Different uploads overwrite previous ones
- Each upload clears the previous extraction
- Server restart resets to default directory

---

## Best Practices

### Before Uploading

1. **Verify ZIP structure** matches expected format
2. **Check file sizes** (tool supports up to 100MB)
3. **Ensure file naming** follows `-feat` and `-main` convention

### During Upload

1. **Wait for completion** - don't navigate away
2. **Monitor progress bar** for status
3. **Read error messages** carefully if upload fails

### After Upload

1. **Review tenant list** in sidebar
2. **Verify file pairs** are correctly detected
3. **Start comparing** your regression tests
4. **Use Dashboard button** to upload new artifacts

---

## Troubleshooting

### Upload Fails

**"Only ZIP files are allowed"**
- Solution: Ensure file has `.zip` extension
- Check: File isn't corrupted

**"Failed to extract artifact"**
- Solution: Verify ZIP file structure
- Check: No password protection on ZIP

**"Upload error: Connection failed"**
- Solution: Verify server is running
- Check: Port 5001 is accessible

### No Tenants Found

**After successful upload, no tenants appear**
- Solution: Check ZIP structure matches expected format
- Verify: Folders contain properly named file pairs

### Slow Upload

**Upload takes a long time**
- Expected: Large files (50-100MB) may take 30-60 seconds
- Network: Check internet connection speed
- Server: Ensure adequate server resources

---

## Workflow Examples

### Example 1: First Time User

```
1. Start server: ./start.sh
2. Open: http://localhost:5001
3. Click: "🚀 Use Sample Artifacts"
4. Explore: Browse tenants and compare files
5. Return: Click "← Dashboard"
6. Upload: Your own artifact ZIP
7. Compare: Review your regression tests
```

### Example 2: Regular User

```
1. Download artifact from GitHub Actions
2. Open: http://localhost:5001 (server already running)
3. Drag & drop: Artifact ZIP to upload area
4. Wait: 5-10 seconds for processing
5. Automatic: Redirected to comparison view
6. Review: Check differences across tenants
```

### Example 3: Multiple Artifacts

```
1. Compare: First artifact
2. Return: Click "← Dashboard"
3. Upload: Second artifact
4. Compare: Side-by-side differences
5. Document: Note significant changes
6. Repeat: For additional artifacts
```

---

## Advanced Features

### Custom Artifact Directory

If you don't want to upload, you can configure a custom directory in `app.py`:

```python
ARTIFACTS_DIR = Path("/path/to/your/artifacts")
```

Then use the "🚀 Use Sample Artifacts" button to load from that location.

### Drag & Drop Tips

- **Multiple files**: Only accepts one ZIP at a time
- **Folder drag**: Must be zipped first
- **Browser support**: Works in Chrome, Firefox, Safari, Edge

---

## Security Notes

- Artifacts are stored temporarily in the `uploads/` folder
- Each upload overwrites previous extractions
- No permanent storage of uploaded files
- Server restart clears all uploads
- For production use, implement user authentication

---

## Future Enhancements

Planned features for the dashboard:

- [ ] Multiple artifact comparison (A/B/C testing)
- [ ] Artifact history tracking
- [ ] Saved comparisons
- [ ] Export comparison reports
- [ ] Team collaboration features
- [ ] Webhook integration with GitHub Actions

---

## Summary

The dashboard provides a user-friendly interface for:

✅ **Easy artifact uploads** via drag-and-drop  
✅ **Quick access** to sample data  
✅ **Automatic processing** and organization  
✅ **Seamless navigation** between uploads and comparisons  
✅ **Clear visual feedback** throughout the process  

**Start exploring your regression test results today!** 🚀

