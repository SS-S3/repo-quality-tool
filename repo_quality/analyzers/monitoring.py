import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any


def analyze_monitoring_logging(repo_path: str) -> Dict[str, Any]:
    """
    Analyze monitoring and logging practices in the codebase.
    """
    monitoring_metrics = {
        'has_logging': False,
        'logging_framework': None,
        'structured_logging': False,
        'error_tracking': False,
        'metrics_collection': False,
        'health_checks': False,
        'monitoring_integrations': [],
        'logging_levels_used': [],
        'logging_quality_score': 0,
        'issues': [],
        'recommendations': []
    }

    repo_path_obj = Path(repo_path)

    # Detect logging frameworks and practices
    logging_info = _detect_logging_frameworks(repo_path_obj)
    monitoring_metrics.update(logging_info)

    # Analyze logging quality
    logging_quality = _analyze_logging_quality(repo_path_obj)
    monitoring_metrics.update(logging_quality)

    # Check for monitoring integrations
    monitoring_integrations = _detect_monitoring_integrations(repo_path_obj)
    monitoring_metrics['monitoring_integrations'] = monitoring_integrations

    # Check for health checks and metrics
    health_metrics = _detect_health_and_metrics(repo_path_obj)
    monitoring_metrics.update(health_metrics)

    # Calculate logging quality score
    score = 0

    # Base score for having logging
    if monitoring_metrics['has_logging']:
        score += 20

    # Structured logging bonus
    if monitoring_metrics['structured_logging']:
        score += 15

    # Error tracking bonus
    if monitoring_metrics['error_tracking']:
        score += 15

    # Metrics collection bonus
    if monitoring_metrics['metrics_collection']:
        score += 15

    # Health checks bonus
    if monitoring_metrics['health_checks']:
        score += 15

    # Monitoring integrations bonus
    score += min(10, len(monitoring_integrations) * 3)

    # Logging levels usage bonus
    score += min(10, len(monitoring_metrics['logging_levels_used']) * 2)

    monitoring_metrics['logging_quality_score'] = min(100, score)

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
    if not monitoring_metrics['has_logging']:
        recommendations.append('Implement comprehensive logging throughout the application')
    if not monitoring_metrics['structured_logging']:
        recommendations.append('Use structured logging with consistent formats')
    if not monitoring_metrics['error_tracking']:
        recommendations.append('Add error tracking and exception monitoring')
    if not monitoring_metrics['metrics_collection']:
        recommendations.append('Implement application metrics and performance monitoring')
    if not monitoring_metrics['health_checks']:
        recommendations.append('Add health check endpoints for service monitoring')
    if not monitoring_integrations:
        recommendations.append('Integrate with monitoring platforms (Prometheus, ELK, etc.)')

    monitoring_metrics['recommendations'] = recommendations

    return {
        **monitoring_metrics,
        'monitoring_quality': quality
    }


def _detect_logging_frameworks(repo_path: Path) -> Dict[str, Any]:
    """Detect logging frameworks and basic logging presence."""
    logging_info = {
        'has_logging': False,
        'logging_framework': None,
        'structured_logging': False
    }

    # Check package files for logging libraries
    package_files = [repo_path / 'package.json', repo_path / 'requirements.txt',
                     repo_path / 'pyproject.toml', repo_path / 'Pipfile']

    logging_libs = {
        'winston': 'Winston (Node.js)',
        'bunyan': 'Bunyan (Node.js)',
        'pino': 'Pino (Node.js)',
        'logging': 'Python logging',
        'loguru': 'Loguru (Python)',
        'structlog': 'Structlog (Python)',
        'sentry': 'Sentry',
        'rollbar': 'Rollbar',
        'bugsnag': 'Bugsnag'
    }

    detected_frameworks = []

    for package_file in package_files:
        if package_file.exists():
            try:
                with open(package_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    for lib, name in logging_libs.items():
                        if lib in content.lower():
                            detected_frameworks.append(name)
                            logging_info['has_logging'] = True

                            # Check for structured logging
                            if lib in ['structlog', 'pino', 'winston']:
                                logging_info['structured_logging'] = True

            except:
                continue

    if detected_frameworks:
        logging_info['logging_framework'] = ', '.join(detected_frameworks)

    # If no framework detected, check code for logging usage
    if not logging_info['has_logging']:
        code_files = list(repo_path.glob('**/*.{py,js,ts}'))
        for code_file in code_files[:10]:  # Sample check
            try:
                with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Check for logging usage
                    logging_patterns = [
                        r'console\.log', r'console\.error', r'console\.warn',
                        r'logging\.', r'logger\.', r'log\.',
                        r'print\s*\(',  # Basic logging fallback
                    ]

                    if any(re.search(pattern, content) for pattern in logging_patterns):
                        logging_info['has_logging'] = True
                        logging_info['logging_framework'] = 'Basic logging'
                        break

            except:
                continue

    return logging_info


def _analyze_logging_quality(repo_path: Path) -> Dict[str, Any]:
    """Analyze the quality of logging implementation."""
    quality_metrics = {
        'logging_levels_used': [],
        'error_tracking': False,
        'issues': []
    }

    code_files = list(repo_path.glob('**/*.{py,js,ts}'))
    logging_levels = set()

    for code_file in code_files[:15]:  # Sample for efficiency
        try:
            with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Detect logging levels
                level_patterns = {
                    'DEBUG': r'\.debug\s*\(',
                    'INFO': r'\.info\s*\(',
                    'WARNING': r'\.warn(?:ing)?\s*\(',
                    'ERROR': r'\.error\s*\(',
                    'CRITICAL': r'\.critical\s*\('
                }

                for level, pattern in level_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        logging_levels.add(level)

                # Check for error tracking
                error_tracking_patterns = [
                    r'sentry', r'rollbar', r'bugsnag', r'raygun',
                    r'try\s*:\s*[\s\S]*?except\s*[\s\S]*?log',
                    r'catch\s*.*log'
                ]

                if any(re.search(pattern, content, re.IGNORECASE) for pattern in error_tracking_patterns):
                    quality_metrics['error_tracking'] = True

                # Check for logging anti-patterns
                anti_patterns = [
                    (r'print\s*\(', 'Using print() instead of proper logging'),
                    (r'except\s*.*:\s*pass', 'Silent exception handling without logging'),
                    (r'console\.log.*error', 'Using console.log for errors instead of proper error logging'),
                    (r'log\..*\+.*log', 'String concatenation in logging calls'),
                ]

                for pattern, issue in anti_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        quality_metrics['issues'].append(f"{issue} in {code_file.name}")

        except:
            continue

    quality_metrics['logging_levels_used'] = list(logging_levels)
    return quality_metrics


def _detect_monitoring_integrations(repo_path: Path) -> List[str]:
    """Detect monitoring and observability integrations."""
    integrations = []

    monitoring_tools = {
        'prometheus': ['prometheus', 'prom-client'],
        'grafana': ['grafana'],
        'datadog': ['datadog', 'dd-trace'],
        'newrelic': ['newrelic'],
        'appdynamics': ['appdynamics'],
        'elastic': ['elasticsearch', '@elastic', 'kibana'],
        'splunk': ['splunk'],
        'cloudwatch': ['aws-sdk', 'cloudwatch'],
        'opentelemetry': ['opentelemetry', '@opentelemetry'],
        'jaeger': ['jaeger'],
        'zipkin': ['zipkin']
    }

    # Check package files
    package_files = [repo_path / 'package.json', repo_path / 'requirements.txt',
                     repo_path / 'pyproject.toml', repo_path / 'Pipfile']

    for package_file in package_files:
        if package_file.exists():
            try:
                with open(package_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    for tool, keywords in monitoring_tools.items():
                        if any(keyword in content.lower() for keyword in keywords):
                            integrations.append(tool.title())
                            break

            except:
                continue

    # Check for monitoring configuration files
    config_files = [
        'prometheus.yml', 'prometheus.yaml',
        'docker-compose.yml', 'docker-compose.yaml',
        'kibana.yml', 'logstash.conf'
    ]

    for config_file in config_files:
        if (repo_path / config_file).exists():
            if 'prometheus' in config_file:
                integrations.append('Prometheus')
            elif 'docker-compose' in config_file:
                integrations.append('Docker Monitoring')
            elif 'kibana' in config_file or 'logstash' in config_file:
                integrations.append('ELK Stack')

    return list(set(integrations))


def _detect_health_and_metrics(repo_path: Path) -> Dict[str, Any]:
    """Detect health checks and metrics collection."""
    health_metrics = {
        'health_checks': False,
        'metrics_collection': False
    }

    code_files = list(repo_path.glob('**/*.{py,js,ts}'))

    for code_file in code_files[:10]:  # Sample check
        try:
            with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Check for health endpoints
                health_patterns = [
                    r'/health', r'/healthcheck', r'/status',
                    r'health.*endpoint', r'status.*endpoint'
                ]

                if any(re.search(pattern, content, re.IGNORECASE) for pattern in health_patterns):
                    health_metrics['health_checks'] = True

                # Check for metrics collection
                metrics_patterns = [
                    r'metrics', r'counter', r'histogram', r'gauge',
                    r'prometheus', r'statsd', r'metric',
                    r'performance.*monitor', r'usage.*stats'
                ]

                if any(re.search(pattern, content, re.IGNORECASE) for pattern in metrics_patterns):
                    health_metrics['metrics_collection'] = True

                # Early exit if both found
                if health_metrics['health_checks'] and health_metrics['metrics_collection']:
                    break

        except:
            continue

    return health_metrics