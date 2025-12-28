import os
import re
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Any


def analyze_documentation_quality(repo_path: str) -> Dict[str, Any]:
    """
    Analyze documentation completeness and quality.
    """
    docs_metrics = {
        'readme_present': False,
        'readme_quality': 'Not found',
        'changelog_present': False,
        'contributing_present': False,
        'license_present': False,
        'api_docs_present': False,
        'inline_comments_ratio': 0,
        'functions_with_docstrings': 0,
        'total_functions': 0,
        'docstring_quality_score': 0,
        'undocumented_functions': [],
        'documentation_gaps': []
    }

    # Check for standard documentation files
    repo_path_obj = Path(repo_path)

    # README files
    readme_files = ['README.md', 'README.rst', 'README.txt', 'readme.md']
    for readme in readme_files:
        if (repo_path_obj / readme).exists():
            docs_metrics['readme_present'] = True
            docs_metrics['readme_quality'] = _assess_readme_quality(repo_path_obj / readme)
            break

    # Other docs
    docs_metrics['changelog_present'] = any((repo_path_obj / f).exists()
                                           for f in ['CHANGELOG.md', 'CHANGES.md', 'HISTORY.md'])
    docs_metrics['contributing_present'] = any((repo_path_obj / f).exists()
                                              for f in ['CONTRIBUTING.md', 'CONTRIBUTING.rst'])
    docs_metrics['license_present'] = any((repo_path_obj / f).exists()
                                         for f in ['LICENSE', 'LICENSE.md', 'LICENSE.txt'])

    # API docs (OpenAPI, Swagger)
    api_docs = ['swagger.json', 'swagger.yaml', 'openapi.json', 'openapi.yaml']
    docs_metrics['api_docs_present'] = any((repo_path_obj / f).exists() for f in api_docs)

    # Analyze code documentation
    code_files = []
    for ext in ['.py', '.js', '.ts']:
        code_files.extend(repo_path_obj.glob(f'**/*{ext}'))

    total_lines = 0
    comment_lines = 0
    total_functions = 0
    documented_functions = 0

    for code_file in code_files[:20]:  # Sample for efficiency
        try:
            with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                total_lines += len(lines)

                # Count comments
                if code_file.suffix == '.py':
                    comment_lines += _count_python_comments(content)
                    func_metrics = _analyze_python_docstrings(content, code_file)
                elif code_file.suffix in ['.js', '.ts']:
                    comment_lines += _count_js_comments(content)
                    func_metrics = _analyze_js_docstrings(content, code_file)
                else:
                    func_metrics = {'functions': 0, 'documented': 0, 'undocumented': []}

                total_functions += func_metrics['functions']
                documented_functions += func_metrics['documented']
                docs_metrics['undocumented_functions'].extend(func_metrics['undocumented'])

        except Exception as e:
            continue

    # Calculate ratios
    if total_lines > 0:
        docs_metrics['inline_comments_ratio'] = round((comment_lines / total_lines) * 100, 1)

    docs_metrics['total_functions'] = total_functions
    docs_metrics['functions_with_docstrings'] = documented_functions

    # Calculate docstring quality score
    if total_functions > 0:
        docstring_ratio = (documented_functions / total_functions) * 100
        comment_ratio_score = min(100, docs_metrics['inline_comments_ratio'] * 2)

        docs_metrics['docstring_quality_score'] = round((docstring_ratio + comment_ratio_score) / 2, 1)

    # Identify documentation gaps
    gaps = []
    if not docs_metrics['readme_present']:
        gaps.append('Missing README file')
    if not docs_metrics['license_present']:
        gaps.append('Missing LICENSE file')
    if docs_metrics['docstring_quality_score'] < 50:
        gaps.append('Low docstring coverage (<50%)')
    if docs_metrics['inline_comments_ratio'] < 10:
        gaps.append('Low inline comment ratio (<10%)')

    docs_metrics['documentation_gaps'] = gaps

    # Overall documentation quality
    score = docs_metrics['docstring_quality_score']
    if docs_metrics['readme_present']:
        score += 20
    if docs_metrics['license_present']:
        score += 10
    if docs_metrics['contributing_present']:
        score += 10
    if docs_metrics['changelog_present']:
        score += 5

    if score >= 80:
        quality = 'Excellent'
    elif score >= 60:
        quality = 'Good'
    elif score >= 40:
        quality = 'Fair'
    else:
        quality = 'Poor'

    return {
        **docs_metrics,
        'documentation_quality': quality,
        'overall_docs_score': min(100, score)
    }


def _assess_readme_quality(readme_path: Path) -> str:
    """Assess README quality based on content."""
    try:
        with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()

        sections = ['installation', 'usage', 'contributing', 'license']
        found_sections = sum(1 for section in sections if section in content)

        if found_sections >= 3:
            return 'Comprehensive'
        elif found_sections >= 2:
            return 'Good'
        elif found_sections >= 1:
            return 'Basic'
        else:
            return 'Minimal'
    except:
        return 'Unreadable'


def _count_python_comments(content: str) -> int:
    """Count comment lines in Python code."""
    lines = content.split('\n')
    comment_lines = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or '"""' in line or "'''" in line:
            comment_lines += 1

    return comment_lines


def _count_js_comments(content: str) -> int:
    """Count comment lines in JavaScript/TypeScript code."""
    lines = content.split('\n')
    comment_lines = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or '*/' in stripped:
            comment_lines += 1

    return comment_lines


def _analyze_python_docstrings(content: str, file_path: Path) -> Dict[str, Any]:
    """Analyze Python docstrings."""
    functions = 0
    documented = 0
    undocumented = []

    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions += 1
                func_name = node.name

                # Check for docstring
                has_docstring = False
                if node.body and isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Str):
                        has_docstring = True
                    elif hasattr(ast, 'Constant') and isinstance(node.body[0].value, ast.Constant):
                        if isinstance(node.body[0].value.value, str):
                            has_docstring = True

                if has_docstring:
                    documented += 1
                else:
                    undocumented.append(f"{func_name} in {file_path.name}")

    except:
        # Fallback: count functions and docstrings with regex
        func_matches = re.findall(r'def\s+(\w+)\s*\(', content)
        functions = len(func_matches)

        # Count triple-quoted strings after function definitions
        docstring_pattern = r'def\s+\w+\s*\([^)]*\):\s*(?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"\s*[\s\S]*?")'
        docstring_matches = len(re.findall(docstring_pattern, content))
        documented = min(docstring_matches, functions)

        if documented < functions:
            undocumented = [f"Function in {file_path.name}"] * (functions - documented)

    return {
        'functions': functions,
        'documented': documented,
        'undocumented': undocumented
    }


def _analyze_js_docstrings(content: str, file_path: Path) -> Dict[str, Any]:
    """Analyze JavaScript/TypeScript docstrings (JSDoc comments)."""
    functions = 0
    documented = 0
    undocumented = []

    # Count functions
    func_patterns = [
        r'function\s+(\w+)',
        r'const\s+(\w+)\s*=.*=>',
        r'(\w+)\s*\([^)]*\)\s*{',
    ]

    for pattern in func_patterns:
        matches = re.findall(pattern, content)
        functions += len(matches)

    # Count JSDoc comments
    jsdoc_pattern = r'/\*\*\s*[\s\S]*?\*/\s*(?:function|const|let|var)?\s*\w+'
    jsdoc_matches = len(re.findall(jsdoc_pattern, content))
    documented = min(jsdoc_matches, functions)

    if documented < functions:
        undocumented = [f"Function in {file_path.name}"] * (functions - documented)

    return {
        'functions': functions,
        'documented': documented,
        'undocumented': undocumented
    }