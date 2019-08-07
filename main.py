
import sys
from prepy.gui.main import PrePy, app


def start_app():
    """Start PrePy."""
    prep_app = app(sys.argv)
    ex = PrePy()
    sys.exit(prep_app.exec_())

if __name__ == '__main__':
    start_app()
