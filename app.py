#!/usr/bin/env python3
"""
StaffView - Gandalf's tool for regression clarity
Compare regression test artifacts from GitHub Actions
Compare, analyze, and illuminate test differences
"""

import os
import zipfile
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import csv
from io import StringIO
from difflib import unified_diff, SequenceMatcher
import json

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Use environment variable or default to uploads/extracted
# This makes it work on both local and deployed environments
default_artifacts = UPLOAD_FOLDER / "extracted"
ARTIFACTS_DIR = Path(os.getenv('ARTIFACTS_DIR', str(default_artifacts)))

# If default local path exists, use it (for development)
local_dev_path = Path("/Users/yeltsinz/Downloads/regression-diffs (1)")
if local_dev_path.exists():
    ARTIFACTS_DIR = local_dev_path

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size


def extract_artifact(zip_path, extract_to):
    """Extract artifact zip file"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to


def get_artifact_structure(base_path):
    """
    Get the structure of the artifact directory
    Returns: {folder_id: [file_pairs]}
    """
    base_path = Path(base_path)
    structure = {}
    
    if not base_path.exists():
        return structure
    
    # Get all subdirectories (like 508, 561, etc.)
    for folder in sorted(base_path.iterdir()):
        if folder.is_dir():
            folder_id = folder.name
            files = sorted([f.name for f in folder.iterdir() if f.is_file()])
            
            # Group files by their base ID (e.g., CHART-426)
            file_groups = {}
            for file_name in files:
                # Extract base ID (everything before -feat or -main)
                if '-feat' in file_name:
                    base_id = file_name.replace('-feat', '')
                    if base_id not in file_groups:
                        file_groups[base_id] = {}
                    file_groups[base_id]['feat'] = file_name
                elif '-main' in file_name:
                    base_id = file_name.replace('-main', '')
                    if base_id not in file_groups:
                        file_groups[base_id] = {}
                    file_groups[base_id]['main'] = file_name
            
            structure[folder_id] = file_groups
    
    return structure


def read_csv_file(file_path):
    """Read CSV file and return as list of rows"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.splitlines()
    except Exception as e:
        return [f"Error reading file: {str(e)}"]


def parse_csv_row(row):
    """Parse CSV row into structured data"""
    parts = row.split(',')
    return {
        'raw': row,
        'parts': parts
    }


def compare_files(feat_path, main_path):
    """
    Compare two files and return differences
    """
    feat_lines = read_csv_file(feat_path)
    main_lines = read_csv_file(main_path)
    
    # Create line-by-line comparison
    comparison = []
    max_lines = max(len(feat_lines), len(main_lines))
    
    for i in range(max_lines):
        feat_line = feat_lines[i] if i < len(feat_lines) else None
        main_line = main_lines[i] if i < len(main_lines) else None
        
        if feat_line == main_line:
            status = 'same'
        elif feat_line is None:
            status = 'removed'
        elif main_line is None:
            status = 'added'
        else:
            status = 'modified'
        
        # Parse cell-level differences for modified rows
        cell_diffs = []
        if status == 'modified' and feat_line and main_line:
            feat_parts = feat_line.split(',')
            main_parts = main_line.split(',')
            max_parts = max(len(feat_parts), len(main_parts))
            
            for j in range(max_parts):
                feat_cell = feat_parts[j] if j < len(feat_parts) else ''
                main_cell = main_parts[j] if j < len(main_parts) else ''
                cell_diffs.append({
                    'feat': feat_cell,
                    'main': main_cell,
                    'different': feat_cell != main_cell
                })
        
        comparison.append({
            'line_num': i + 1,
            'feat': feat_line,
            'main': main_line,
            'status': status,
            'cell_diffs': cell_diffs
        })
    
    # Calculate statistics
    stats = {
        'total_lines': max_lines,
        'same': sum(1 for c in comparison if c['status'] == 'same'),
        'modified': sum(1 for c in comparison if c['status'] == 'modified'),
        'added': sum(1 for c in comparison if c['status'] == 'added'),
        'removed': sum(1 for c in comparison if c['status'] == 'removed')
    }
    
    return {
        'comparison': comparison,
        'stats': stats
    }


@app.route('/')
def index():
    """Dashboard landing page"""
    return render_template('dashboard.html')


@app.route('/compare')
def compare_view():
    """Comparison interface"""
    return render_template('index.html')


@app.route('/api/structure')
def get_structure():
    """Get artifact directory structure"""
    # Check if ARTIFACTS_DIR exists and has content
    if not ARTIFACTS_DIR.exists() or not any(ARTIFACTS_DIR.iterdir()):
        return jsonify({})
    
    structure = get_artifact_structure(ARTIFACTS_DIR)
    return jsonify(structure)


@app.route('/api/compare')
def compare():
    """Compare two files and return full contents for Monaco Editor"""
    folder = request.args.get('folder')
    file_id = request.args.get('file')
    
    if not folder or not file_id:
        return jsonify({'error': 'Missing parameters'}), 400
    
    feat_path = ARTIFACTS_DIR / folder / f"{file_id}-feat"
    main_path = ARTIFACTS_DIR / folder / f"{file_id}-main"
    
    if not feat_path.exists() or not main_path.exists():
        return jsonify({'error': 'Files not found'}), 404
    
    # Read full file contents
    try:
        with open(main_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        with open(feat_path, 'r', encoding='utf-8') as f:
            feat_content = f.read()
    except Exception as e:
        return jsonify({'error': f'Error reading files: {str(e)}'}), 500
    
    # Calculate statistics
    main_lines = main_content.splitlines()
    feat_lines = feat_content.splitlines()
    
    # Simple line-based diff statistics
    main_set = set(main_lines)
    feat_set = set(feat_lines)
    
    unchanged = len(main_set & feat_set)
    added = len(feat_set - main_set)
    removed = len(main_set - feat_set)
    
    # Modified lines are harder to determine without proper diff
    # Using SequenceMatcher for better accuracy
    from difflib import SequenceMatcher
    matcher = SequenceMatcher(None, main_lines, feat_lines)
    
    modified = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            modified += max(i2 - i1, j2 - j1)
        elif tag == 'delete':
            removed = max(removed, i2 - i1)
        elif tag == 'insert':
            added = max(added, j2 - j1)
    
    stats = {
        'unchanged': unchanged,
        'modified': modified,
        'added': added,
        'removed': removed,
        'total': max(len(main_lines), len(feat_lines))
    }
    
    return jsonify({
        'folder_id': folder,
        'file_id': file_id,
        'main_content': main_content,
        'feat_content': feat_content,
        'stats': stats
    })


@app.route('/api/upload', methods=['POST'])
def upload_artifact():
    """Upload and extract artifact zip file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'Only ZIP files are allowed'}), 400
    
    try:
        # Save uploaded file
        zip_path = UPLOAD_FOLDER / file.filename
        file.save(zip_path)
        
        # Extract to artifacts directory
        extract_to = UPLOAD_FOLDER / 'extracted'
        # Clear previous extraction
        if extract_to.exists():
            shutil.rmtree(extract_to)
        extract_to.mkdir(exist_ok=True)
        
        extract_artifact(zip_path, extract_to)
        
        # Update global artifacts directory (for this session)
        global ARTIFACTS_DIR
        ARTIFACTS_DIR = extract_to
        
        # Get structure to return
        structure = get_artifact_structure(ARTIFACTS_DIR)
        
        return jsonify({
            'success': True,
            'message': 'Artifact uploaded and extracted successfully',
            'artifact_count': len(structure),
            'structure': structure
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/use-sample')
def use_sample():
    """Use the sample artifact directory"""
    global ARTIFACTS_DIR
    ARTIFACTS_DIR = Path("/Users/yeltsinz/Downloads/regression-diffs (1)")
    
    structure = get_artifact_structure(ARTIFACTS_DIR)
    
    return jsonify({
        'success': True,
        'message': 'Using sample artifact directory',
        'artifact_count': len(structure),
        'structure': structure
    })


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    static_dir = Path(__file__).parent / 'static'
    return send_from_directory(static_dir, filename)


if __name__ == '__main__':
    print("⚡ Starting StaffView...")
    print("   Gandalf's tool for regression clarity")
    print(f"   Using artifacts from: {ARTIFACTS_DIR}")
    app.run(debug=True, port=5001)

