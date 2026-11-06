"""Shared rendering components.  Registers HEIC/HEIF so iPhone photos open like any other image."""
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:  # optional: everything else still works
    pass
