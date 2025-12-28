from typing import Dict, Any


def coerce_section(metrics: Dict[str, Any], key: str) -> dict:
    """Coerce a metrics section to a dict."""
    v = metrics.get(key, {})
    return v if isinstance(v, dict) else {}


def format_number(v, fmt=':.1f'):
    """Format a number or return 'null' if None."""
    if v is None:
        return 'null'
    try:
        return format(v, fmt)
    except Exception:
        return str(v)