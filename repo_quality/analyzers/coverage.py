import os
import re
from pathlib import Path
from typing import Dict, List, Any
import xml.etree.ElementTree as ET
import json


def analyze_code_coverage(repo_path: str) -> Dict[str, Any]:
    """
    Analyze test coverage by parsing coverage reports and calculating metrics.
    """
    coverage_files = []
    coverage_data = {}

    # Look for common coverage report files
    coverage_patterns = [
        'coverage.xml', '.coverage', 'coverage.json', 'lcov.info',
        'coverage/coverage.xml', 'htmlcov/index.html'
    ]

    for pattern in coverage_patterns:
        matches = list(Path(repo_path).glob(f'**/{pattern}'))
        coverage_files.extend(matches)

    if not coverage_files:
        return {
            'coverage_found': False,
            'line_coverage_pct': 0,
            'branch_coverage_pct': 0,
            'function_coverage_pct': 0,
            'uncovered_lines': 0,
            'total_lines': 0,
            'coverage_quality': 'No coverage reports found',
            'recommendations': ['Add test coverage reporting to CI/CD pipeline']
        }

    # Parse coverage data
    total_lines = 0
    covered_lines = 0
    total_branches = 0
    covered_branches = 0
    total_functions = 0
    covered_functions = 0

    for coverage_file in coverage_files:
        try:
            if coverage_file.name == 'coverage.xml':
                # Parse Cobertura XML format
                tree = ET.parse(coverage_file)
                root = tree.getroot()

                for package in root.findall('.//package'):
                    for cls in package.findall('.//class'):
                        # Line coverage
                        lines = cls.findall('.//line')
                        for line in lines:
                            hits = int(line.get('hits', 0))
                            total_lines += 1
                            if hits > 0:
                                covered_lines += 1

                        # Branch coverage
                        for line in lines:
                            if line.get('branch') == 'true':
                                total_branches += 1
                                if int(line.get('hits', 0)) > 0:
                                    covered_branches += 1

            elif coverage_file.name == 'lcov.info':
                # Parse LCOV format
                with open(coverage_file, 'r') as f:
                    content = f.read()

                # Parse LCOV format (simplified)
                lines = content.split('\n')
                current_file = None
                for line in lines:
                    if line.startswith('SF:'):
                        current_file = line[3:]
                    elif line.startswith('DA:'):
                        # DA:<line>,<hits>
                        parts = line[3:].split(',')
                        if len(parts) == 2:
                            hits = int(parts[1])
                            total_lines += 1
                            if hits > 0:
                                covered_lines += 1
                    elif line.startswith('BRDA:'):
                        # BRDA:<line>,<block>,<branch>,<hits>
                        parts = line[5:].split(',')
                        if len(parts) >= 4:
                            hits = int(parts[3])
                            total_branches += 1
                            if hits > 0:
                                covered_branches += 1

        except Exception as e:
            continue

    # Calculate percentages
    line_coverage = (covered_lines / total_lines * 100) if total_lines > 0 else 0
    branch_coverage = (covered_branches / total_branches * 100) if total_branches > 0 else 0
    function_coverage = (covered_functions / total_functions * 100) if total_functions > 0 else 0

    # Determine coverage quality
    if line_coverage >= 80:
        quality = 'Excellent'
    elif line_coverage >= 70:
        quality = 'Good'
    elif line_coverage >= 60:
        quality = 'Fair'
    else:
        quality = 'Poor'

    # Generate recommendations
    recommendations = []
    if line_coverage < 80:
        recommendations.append('Increase line coverage to at least 80%')
    if branch_coverage < 75:
        recommendations.append('Improve branch coverage for conditional logic')
    if not coverage_files:
        recommendations.append('Set up automated test coverage reporting')

    return {
        'coverage_found': True,
        'line_coverage_pct': round(line_coverage, 1),
        'branch_coverage_pct': round(branch_coverage, 1),
        'function_coverage_pct': round(function_coverage, 1),
        'uncovered_lines': total_lines - covered_lines,
        'total_lines': total_lines,
        'coverage_quality': quality,
        'recommendations': recommendations
    }