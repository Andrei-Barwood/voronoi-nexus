"""
helly_rules - Cybersecurity Module
Part of Snocomm Security Suite

Misión: Charlotte Balfour
Rol: yara-rule-engine
"""

__version__ = "3.0.0"
__author__ = "Kirtan Teg Singh"
__license__ = "MIT"

from .core import HellyRules

__all__ = ["HellyRules", "__version__"]
