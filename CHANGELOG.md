# ⚡ StaffView Changelog

**Gandalf's tool for regression clarity**

All notable changes to the StaffView project.

---

## [Version 2.0] - 2025-10-31

### 🎉 Major Features Added

#### Dashboard Landing Page
- **New landing page** at root URL (`/`)
- Beautiful welcome interface with gradient design
- Clear instructions for first-time users
- Feature highlights showcase

#### Artifact Upload System
- **Drag-and-drop upload** for ZIP files
- **Click-to-browse** file selection
- **Real-time progress indicators** during upload/extraction
- **Automatic artifact extraction** and organization
- **Success/error feedback** with clear messaging
- Support for files up to 100MB

#### API Enhancements
- **POST `/api/upload`**: Handle artifact ZIP uploads
- **GET `/api/use-sample`**: Quick access to sample data
- **Enhanced responses**: Include artifact counts and structure
- **Better error handling**: Descriptive error messages

#### Navigation Improvements
- **Dashboard button** (← Dashboard) in comparison view
- **Automatic redirects** after successful uploads
- **Seamless flow** between upload and comparison

### 🎨 UI/UX Improvements

#### Dashboard Design
- Modern gradient background
- Large, friendly upload area
- Hover effects and animations
- Progress bar with shimmer effect
- Feature cards with icons
- Responsive layout

#### Upload Area States
- Default (dashed border)
- Drag-over (green highlight)
- Processing (disabled with progress)
- Success (checkmark confirmation)
- Error (red alert)

### 🔧 Technical Changes

#### Backend (`app.py`)
- Added `shutil` import for directory cleanup
- New route structure:
  - `/` → Dashboard (dashboard.html)
  - `/compare` → Comparison interface (index.html)
- Enhanced upload handler with cleanup
- Sample data quick-load endpoint
- Better session management for artifacts

#### Frontend
- Created `dashboard.html` with full upload interface
- Added back navigation button to `index.html`
- JavaScript for drag-and-drop functionality
- Progress tracking and status updates
- Form data handling for uploads

### 📚 Documentation Updates

#### New Guides
- **DASHBOARD_GUIDE.md**: Complete dashboard documentation
  - Upload methods
  - Workflow examples
  - Troubleshooting
  - Best practices

#### Updated Guides
- **README.md**: Added upload workflow instructions
- **USAGE_GUIDE.md**: Updated quick start section
- **PROJECT_SUMMARY.md**: Documented new features

#### New Files
- **.gitignore**: Ignore uploads, logs, and virtual environment
- **CHANGELOG.md**: This file

### 🐛 Bug Fixes
- Fixed import issue with `shutil`
- Improved artifact directory cleanup
- Better error handling for invalid ZIP files

---

## [Version 1.0] - 2025-10-31

### Initial Release

#### Core Features
- Side-by-side comparison of regression test artifacts
- Visual diff highlighting (modified/added/removed/unchanged)
- Cell-level difference detection for CSV files
- Real-time statistics dashboard
- Tenant-based organization
- Beautiful purple gradient UI

#### Components
- Flask backend server
- Single-page web interface
- REST API for data access
- CSV parsing and comparison engine

#### Documentation
- README with installation guide
- Usage guide with workflows
- Project summary
- Start script for easy setup

---

## Migration Guide: v1.0 → v2.0

### For Existing Users

If you were using version 1.0, here's what changed:

#### URL Changes
- **Old**: `http://localhost:5001` → Comparison interface
- **New**: `http://localhost:5001` → Dashboard
- **Comparison**: `http://localhost:5001/compare` → Comparison interface

#### Workflow Changes
**Old workflow:**
1. Start server
2. Ensure artifacts in configured directory
3. Open browser to comparison view

**New workflow:**
1. Start server
2. Open browser to dashboard
3. Upload artifacts OR use sample data
4. Automatic redirect to comparison view

#### No Breaking Changes
- All existing comparison features work the same
- Sample artifacts still accessible via button
- Configuration options remain unchanged
- No changes to file format or structure

### Getting Started with v2.0

```bash
# 1. Pull latest changes (if using git)
git pull

# 2. Restart server
./start.sh

# 3. Open browser
# Now opens to dashboard instead of comparison view
open http://localhost:5001
```

---

## Upcoming Features

### Planned for v2.1
- [ ] Multiple artifact comparison (A/B/C)
- [ ] Artifact upload history
- [ ] Download comparison reports (PDF/HTML)

### Planned for v2.2
- [ ] User authentication
- [ ] Team collaboration features
- [ ] Saved comparison bookmarks
- [ ] GitHub Actions webhook integration

### Planned for v3.0
- [ ] Real-time collaboration
- [ ] Comments and annotations
- [ ] Advanced filtering and search
- [ ] Custom diff algorithms
- [ ] API for programmatic access

---

## Technical Requirements

### System Requirements
- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 100MB+ disk space for artifacts
- 512MB+ RAM

### Dependencies
```
Flask==3.0.0
Werkzeug==3.0.1
```

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Contributors

Built with ❤️ for efficient regression testing workflows.

---

## License

MIT License - See LICENSE file for details

---

## Support

For issues, questions, or feature requests:
1. Check the documentation in the README
2. Review the USAGE_GUIDE for common workflows
3. See DASHBOARD_GUIDE for upload issues
4. Check the troubleshooting sections

---

## Acknowledgments

Special thanks to all users who provided feedback that helped shape v2.0!

---

*Last updated: October 31, 2025*

