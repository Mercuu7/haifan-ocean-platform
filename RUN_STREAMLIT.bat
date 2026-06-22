@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Starting Haifan Streamlit platform...
echo Open http://localhost:8501 after startup.
python -m streamlit run streamlit_app.py
pause
