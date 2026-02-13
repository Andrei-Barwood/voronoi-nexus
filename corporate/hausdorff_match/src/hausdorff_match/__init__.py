"""
hausdorff_match - Cybersecurity Module
Part of Snocomm Security Suite

Misión: My Last Boy
Rol: signature-matcher
"""

__version__ = "3.0.0"
__author__ = "Kirtan Teg Singh"
__license__ = "MIT"

from .core import HausdorffMatch

__all__ = ["HausdorffMatch", "__version__"]
