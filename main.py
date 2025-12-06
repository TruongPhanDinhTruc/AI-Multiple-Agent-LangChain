import sys
from pathlib import Path

# Thêm thư mục hiện tại vào path
sys.path.insert(0, str(Path(__file__).parent))

# Import streamlit app
import streamlit.web.cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "frontend/interface.py"]
    sys.exit(stcli.main())