import warnings


def my_warningformat(message, category, filename, lineno, line=None):
    return f"{filename}:{lineno}: {category.__name__}: {message}\n"


warnings.formatwarning = my_warningformat


def print_warning(msg):
    warnings.warn(msg)
