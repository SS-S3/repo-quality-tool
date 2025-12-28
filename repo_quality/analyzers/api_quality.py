import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any


def analyze_api_quality(repo_path: str) -> Dict[str, Any]:
    """
    Analyze API quality and design patterns.
    """
    api_metrics = {
        'has_api': False,
        'api_type': None,
        'endpoints_count': 0,
        'authenticated_endpoints': 0,
        'rate_limited_endpoints': 0,
        'documented_endpoints': 0,
        'restful_compliance': 0,
        'security_features': [],
        'api_quality_score': 0,
        'issues': [],
        'recommendations': []
    }

    repo_path_obj = Path(repo_path)

    # Detect API frameworks and specifications
    api_frameworks = _detect_api_frameworks(repo_path_obj)
    api_specs = _detect_api_specifications(repo_path_obj)

    if not api_frameworks and not api_specs:
        return {
            **api_metrics,
            'api_quality': 'No API detected',
            'recommendations': ['Consider adding API documentation if this is an API service']
        }

    api_metrics['has_api'] = True

    # Analyze API specifications (OpenAPI/Swagger)
    if api_specs:
        api_metrics['api_type'] = 'REST API with specification'
        for spec_file in api_specs:
            try:
                spec_data = _parse_api_spec(spec_file)
                _analyze_openapi_spec(spec_data, api_metrics)
            except Exception as e:
                api_metrics['issues'].append(f"Failed to parse API spec {spec_file.name}: {str(e)}")

    # Analyze API framework code
    if api_frameworks:
        api_metrics['api_type'] = list(api_frameworks.keys())[0]

        for framework, files in api_frameworks.items():
            for api_file in files[:5]:  # Limit analysis for efficiency
                try:
                    with open(api_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        _analyze_api_code(content, framework, api_metrics, api_file.name)
                except Exception as e:
                    continue

    # Calculate API quality score
    score = 0

    # Base score for having API
    score += 20

    # Documentation score
    if api_metrics['documented_endpoints'] > 0:
        doc_ratio = api_metrics['documented_endpoints'] / max(1, api_metrics['endpoints_count'])
        score += min(25, doc_ratio * 25)

    # Security score
    security_score = len(api_metrics['security_features']) * 8
    score += min(25, security_score)

    # REST compliance score
    score += min(15, api_metrics['restful_compliance'] * 3)

    # Authentication score
    if api_metrics['authenticated_endpoints'] > 0:
        auth_ratio = api_metrics['authenticated_endpoints'] / max(1, api_metrics['endpoints_count'])
        score += min(15, auth_ratio * 15)

    api_metrics['api_quality_score'] = min(100, score)

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
    if api_metrics['documented_endpoints'] == 0:
        recommendations.append('Add API documentation (OpenAPI/Swagger)')
    if api_metrics['authenticated_endpoints'] == 0:
        recommendations.append('Implement authentication for API endpoints')
    if not api_metrics['security_features']:
        recommendations.append('Add security features (CORS, input validation, etc.)')
    if api_metrics['restful_compliance'] < 5:
        recommendations.append('Follow RESTful API design principles')

    api_metrics['recommendations'] = recommendations

    return {
        **api_metrics,
        'api_quality': quality
    }


def _detect_api_frameworks(repo_path: Path) -> Dict[str, List[Path]]:
    """Detect API frameworks used in the codebase."""
    frameworks = {}

    # Python frameworks
    python_frameworks = {
        'FastAPI': ['fastapi', 'FastAPI'],
        'Flask': ['flask', 'Flask'],
        'Django REST': ['rest_framework', 'djangorestframework'],
        'Starlette': ['starlette', 'Starlette']
    }

    # JavaScript/TypeScript frameworks
    js_frameworks = {
        'Express.js': ['express', 'Express'],
        'NestJS': ['@nestjs', 'nest'],
        'Next.js API': ['next', 'NextApiRequest'],
        'Koa.js': ['koa', 'Koa']
    }

    # Check package.json for JS frameworks
    package_json = repo_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                dependencies = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                for framework, keywords in js_frameworks.items():
                    if any(keyword in ' '.join(dependencies.keys()) for keyword in keywords):
                        # Find API route files
                        api_files = list(repo_path.glob('**/routes/*.js')) + \
                                   list(repo_path.glob('**/api/*.js')) + \
                                   list(repo_path.glob('**/controllers/*.js'))
                        if api_files:
                            frameworks[framework] = api_files
        except:
            pass

    # Check Python files for frameworks
    python_files = list(repo_path.glob('**/*.py'))
    for py_file in python_files[:10]:  # Sample check
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                for framework, keywords in python_frameworks.items():
                    if any(keyword in content for keyword in keywords):
                        api_files = [f for f in python_files if any(term in str(f) for term in ['api', 'routes', 'views'])]
                        if api_files:
                            frameworks[framework] = api_files[:5]
                        break
        except:
            continue

    return frameworks


def _detect_api_specifications(repo_path: Path) -> List[Path]:
    """Detect API specification files."""
    spec_files = []
    spec_patterns = [
        'swagger.json', 'swagger.yaml', 'swagger.yml',
        'openapi.json', 'openapi.yaml', 'openapi.yml',
        'api.json', 'api.yaml', 'api.yml'
    ]

    for pattern in spec_patterns:
        matches = list(repo_path.glob(f'**/{pattern}'))
        spec_files.extend(matches)

    return spec_files


def _parse_api_spec(spec_file: Path) -> Dict[str, Any]:
    """Parse OpenAPI/Swagger specification."""
    with open(spec_file, 'r', encoding='utf-8') as f:
        if spec_file.suffix == '.json':
            return json.load(f)
        else:
            return yaml.safe_load(f)


def _analyze_openapi_spec(spec_data: Dict[str, Any], api_metrics: Dict[str, Any]):
    """Analyze OpenAPI specification for quality metrics."""
    paths = spec_data.get('paths', {})
    components = spec_data.get('components', {})
    security_schemes = components.get('securitySchemes', {})

    api_metrics['endpoints_count'] = len(paths)

    authenticated_endpoints = 0
    documented_endpoints = 0
    rate_limited_endpoints = 0
    restful_score = 0

    for path, methods in paths.items():
        for method, details in methods.items():
            # Check documentation
            if details.get('summary') or details.get('description'):
                documented_endpoints += 1

            # Check authentication
            if details.get('security') or spec_data.get('security'):
                authenticated_endpoints += 1

            # Check rate limiting (basic check for common patterns)
            if 'rate' in str(details).lower() or 'limit' in str(details).lower():
                rate_limited_endpoints += 1

            # RESTful compliance check
            if _is_restful_endpoint(path, method):
                restful_score += 1

    api_metrics['authenticated_endpoints'] = authenticated_endpoints
    api_metrics['documented_endpoints'] = documented_endpoints
    api_metrics['rate_limited_endpoints'] = rate_limited_endpoints
    api_metrics['restful_compliance'] = restful_score

    # Security features
    security_features = []
    if security_schemes:
        security_features.append('Authentication schemes defined')
    if any('cors' in str(spec_data).lower() for key in ['info', 'servers']):
        security_features.append('CORS configuration')
    if any('version' in str(spec_data).lower() for key in ['info']):
        security_features.append('API versioning')

    api_metrics['security_features'] = security_features


def _analyze_api_code(content: str, framework: str, api_metrics: Dict[str, Any], filename: str):
    """Analyze API framework code for quality patterns."""

    if framework == 'FastAPI':
        # FastAPI patterns
        routes = len(re.findall(r'@app\.(get|post|put|delete|patch)', content))
        api_metrics['endpoints_count'] += routes

        # Authentication
        if re.search(r'depends|Depends', content):
            api_metrics['authenticated_endpoints'] += routes

        # Documentation
        if re.search(r'doc|description', content):
            api_metrics['documented_endpoints'] += routes

    elif framework == 'Flask':
        # Flask patterns
        routes = len(re.findall(r'@app\.route', content))
        api_metrics['endpoints_count'] += routes

        # Authentication
        if re.search(r'login_required|@login', content):
            api_metrics['authenticated_endpoints'] += routes

    elif framework == 'Express.js':
        # Express patterns
        routes = len(re.findall(r'app\.(get|post|put|delete|patch)', content))
        api_metrics['endpoints_count'] += routes

        # Middleware (security)
        if re.search(r'app\.use.*cors|helmet|auth', content, re.IGNORECASE):
            api_metrics['security_features'].append('Security middleware detected')

    # Common security checks
    if re.search(r'jwt|token|auth', content, re.IGNORECASE):
        if 'Authentication implemented' not in api_metrics['security_features']:
            api_metrics['security_features'].append('Authentication implemented')

    if re.search(r'validate|joi|yup', content, re.IGNORECASE):
        if 'Input validation' not in api_metrics['security_features']:
            api_metrics['security_features'].append('Input validation')

    # Error handling
    if re.search(r'try|catch|error.*handler', content, re.IGNORECASE):
        if 'Error handling' not in api_metrics['security_features']:
            api_metrics['security_features'].append('Error handling')


def _is_restful_endpoint(path: str, method: str) -> bool:
    """Check if endpoint follows RESTful conventions."""
    score = 0

    # Resource naming (plural nouns)
    if re.search(r'/[a-z]+s(/|$)', path):
        score += 1

    # HTTP method appropriateness
    method_map = {
        'get': ['list', 'retrieve'],
        'post': ['create'],
        'put': ['update', 'replace'],
        'patch': ['partial_update'],
        'delete': ['delete']
    }

    method_lower = method.lower()
    if method_lower in method_map:
        # Check if path suggests the operation
        path_lower = path.lower()
        if any(op in path_lower for op in method_map[method_lower]):
            score += 1

    # Nested resources
    if re.search(r'/[a-z]+/\d+(/[a-z]+)?', path):
        score += 1

    return score >= 2