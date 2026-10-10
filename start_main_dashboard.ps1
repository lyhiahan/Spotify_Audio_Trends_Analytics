# Khởi chạy Main Dashboard (1 trang no-scroll) của Gia Hân
$Host.UI.RawUI.WindowTitle = "Spotify Main Dashboard - Gia Han"
Write-Host "Dang khoi dong Spotify Main Dashboard tren cong 8503..." -ForegroundColor Green
python -m streamlit run dashboard/main_dashboard.py --server.port 8503 --server.headless true
