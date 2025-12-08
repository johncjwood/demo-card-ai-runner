#!/usr/bin/env python3
import os
from pathlib import Path
from collections import defaultdict

EXCLUDE_DIRS = {'node_modules', '.git', '__pycache__', 'dist', 'build', '.venv', 'venv'}
EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'JavaScript',
    '.tsx': 'TypeScript',
    '.md': 'Markdown',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.html': 'HTML',
    '.css': 'CSS',
    '.sql': 'SQL',
    '.sh': 'Shell',
}

def count_lines(directory='.'):
    counts = defaultdict(int)
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in EXTENSIONS:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                    counts[EXTENSIONS[ext]] += line_count
                except:
                    pass
    
    print("\nLines of Code by Language:")
    print("-" * 40)
    for lang in sorted(counts.keys()):
        print(f"{lang:20} {counts[lang]:>10,} lines")
    print("-" * 40)
    print(f"{'Total':20} {sum(counts.values()):>10,} lines")

if __name__ == '__main__':
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    count_lines(directory)
