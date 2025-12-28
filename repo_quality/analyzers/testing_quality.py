import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any


def analyze_testing_quality(repo_path: str) -> Dict[str, Any]:
    """
    Analyze the quality of test suites and testing practices.
    """
    test_files = []
    test_metrics = {
        'total_test_files': 0,
        'total_test_functions': 0,
        'total_assertions': 0,
        'test_to_code_ratio': 0,
        'assertion_density': 0,
        'mock_usage': 0,
        'flaky_tests': [],
        'missing_assertions': [],
        'anti_patterns': [],
        'test_quality_score': 0
    }

    # Find test files
    test_patterns = [
        'test_*.py', '*_test.py', 'tests/**/*.py',
        '*.spec.js', '*.test.js', '__tests__/**/*.js',
        '*.spec.ts', '*.test.ts', '__tests__/**/*.ts'
    ]

    for pattern in test_patterns:
        matches = list(Path(repo_path).glob(f'**/{pattern}'))
        test_files.extend(matches)

    test_metrics['total_test_files'] = len(test_files)

    if not test_files:
        return {
            **test_metrics,
            'test_quality': 'No tests found',
            'recommendations': ['Add comprehensive test suite', 'Implement unit tests for critical functions']
        }

    # Analyze each test file
    total_lines_code = 0
    total_lines_test = 0

    for test_file in test_files:
        try:
            with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                total_lines_test += len(lines)

                # Count test functions
                if test_file.suffix == '.py':
                    test_functions = _analyze_python_tests(content)
                elif test_file.suffix in ['.js', '.ts']:
                    test_functions = _analyze_javascript_tests(content)
                else:
                    test_functions = []

                test_metrics['total_test_functions'] += len(test_functions)

                # Count assertions
                assertions = _count_assertions(content, test_file.suffix)
                test_metrics['total_assertions'] += assertions

                # Check for anti-patterns
                anti_patterns = _detect_test_anti_patterns(content, test_file)
                test_metrics['anti_patterns'].extend(anti_patterns)

                # Check for missing assertions
                missing_asserts = _detect_missing_assertions(content, test_functions, test_file)
                test_metrics['missing_assertions'].extend(missing_asserts)

        except Exception as e:
            continue

    # Calculate code-to-test ratio
    code_files = []
    for ext in ['.py', '.js', '.jsx', '.ts', '.tsx']:
        code_files.extend(Path(repo_path).glob(f'**/*{ext}'))

    # Exclude test files from code count
    code_files = [f for f in code_files if not any(p in str(f) for p in ['test', 'spec', '__tests__'])]

    for code_file in code_files[:10]:  # Sample first 10 files for efficiency
        try:
            with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                total_lines_code += len(f.readlines())
        except:
            continue

    if total_lines_code > 0:
        test_metrics['test_to_code_ratio'] = round((total_lines_test / total_lines_code) * 100, 1)

    # Calculate assertion density
    if test_metrics['total_test_functions'] > 0:
        test_metrics['assertion_density'] = round(test_metrics['total_assertions'] / test_metrics['total_test_functions'], 1)

    # Calculate test quality score
    score = 0
    if test_metrics['test_to_code_ratio'] >= 100:
        score += 30
    elif test_metrics['test_to_code_ratio'] >= 50:
        score += 20
    elif test_metrics['test_to_code_ratio'] >= 25:
        score += 10

    if test_metrics['assertion_density'] >= 3:
        score += 30
    elif test_metrics['assertion_density'] >= 2:
        score += 20
    elif test_metrics['assertion_density'] >= 1:
        score += 10

    if len(test_metrics['anti_patterns']) == 0:
        score += 20
    elif len(test_metrics['anti_patterns']) <= 2:
        score += 10

    if len(test_metrics['missing_assertions']) == 0:
        score += 20
    elif len(test_metrics['missing_assertions']) <= 2:
        score += 10

    test_metrics['test_quality_score'] = min(100, score)

    # Determine overall quality
    if score >= 80:
        quality = 'Excellent'
    elif score >= 60:
        quality = 'Good'
    elif score >= 40:
        quality = 'Fair'
    else:
        quality = 'Poor'

    # Generate recommendations
    recommendations = []
    if test_metrics['test_to_code_ratio'] < 50:
        recommendations.append('Increase test-to-code ratio to at least 50%')
    if test_metrics['assertion_density'] < 2:
        recommendations.append('Add more assertions per test function (aim for 2-3)')
    if test_metrics['anti_patterns']:
        recommendations.append('Fix test anti-patterns for better reliability')
    if test_metrics['missing_assertions']:
        recommendations.append('Add assertions to tests that lack them')

    return {
        **test_metrics,
        'test_quality': quality,
        'recommendations': recommendations
    }


def _analyze_python_tests(content: str) -> List[str]:
    """Analyze Python test functions."""
    test_functions = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_functions.append(node.name)
    except:
        # Fallback to regex
        test_functions = re.findall(r'def\s+(test_\w+)', content)
    return test_functions


def _analyze_javascript_tests(content: str) -> List[str]:
    """Analyze JavaScript/TypeScript test functions."""
    test_functions = []
    # Jest/Mocha patterns
    patterns = [
        r'(?:it|test|describe)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'function\s+(test\w+)',
        r'const\s+(test\w+)\s*=',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        test_functions.extend(matches)
    return list(set(test_functions))


def _count_assertions(content: str, file_ext: str) -> int:
    """Count assertion statements."""
    assertions = 0

    if file_ext == '.py':
        # unittest, pytest assertions
        assertion_patterns = [
            r'assert\s+',
            r'self\.assert',
            r'pytest\.raises',
            r'with\s+self\.assertRaises',
        ]
    else:
        # Jest/Jasmine assertions
        assertion_patterns = [
            r'expect\s*\(',
            r'assert\s*\(',
            r'should\s*\.',
        ]

    for pattern in assertion_patterns:
        assertions += len(re.findall(pattern, content))

    return assertions


def _detect_test_anti_patterns(content: str, file_path: Path) -> List[str]:
    """Detect common test anti-patterns."""
    anti_patterns = []

    # Sleep in tests
    if re.search(r'time\.sleep|setTimeout.*\d+', content):
        anti_patterns.append(f"Sleep/delay detected in {file_path.name}")

    # Empty test functions
    if re.search(r'def test_\w+\([^)]*\):\s*pass', content):
        anti_patterns.append(f"Empty test function in {file_path.name}")

    # Tests without assertions (already handled separately)

    # Hardcoded test data
    if re.search(r'assert.*==.*[0-9]{4,}', content):  # Magic numbers
        anti_patterns.append(f"Magic numbers in assertions in {file_path.name}")

    return anti_patterns


def _detect_missing_assertions(content: str, test_functions: List[str], file_path: Path) -> List[str]:
    """Detect test functions that might be missing assertions."""
    missing = []

    # Simple heuristic: test functions without assert/expect
    for func in test_functions:
        # Find the function definition and check if it has assertions
        func_pattern = rf'def {re.escape(func)}\s*\([^)]*\):(.*?)(?=\ndef|\nclass|\n@|\Z)'
        match = re.search(func_pattern, content, re.DOTALL)
        if match:
            func_body = match.group(1)
            if not re.search(r'assert|expect|self\.assert', func_body):
                missing.append(f"{func} in {file_path.name}")

    return missing