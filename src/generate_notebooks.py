import os
import json

base = r"d:\LAPTRINH\TUONGTACDATA\PROJECT"

def make_nb(filename, title, member, goals, steps, in_data, out_data):
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {title}\n\n",
                f"- **Người phụ trách:** {member}\n",
                f"- **Mục tiêu chính:** {goals}\n",
                f"- **Dữ liệu đầu vào (Input):** `{in_data}`\n",
                f"- **Dữ liệu đầu ra (Output):** `{out_data}`\n\n",
                "---\n",
                "### 📌 Danh sách công việc cần làm (Checklist)\n"
            ] + [f"- [ ] {s}\n" for s in steps]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Khởi tạo môi trường & thư viện\n",
                "import os\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n\n",
                "pd.set_option('display.max_columns', None)\n",
                "print('Môi trường làm việc đã sẵn sàng!')\n"
            ]
        }
    ]
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    with open(os.path.join(base, "notebooks", filename), "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)
    print(f"Created successfully: {filename}")

# Notebook 1
make_nb(
    "01_preprocess.ipynb",
    "PHẦN 1: TIỀN XỬ LÝ & KẾT NỐI 5 BẢNG DỮ LIỆU",
    "Thành viên 1 (Data Engineer / Pipeline)",
    "Làm sạch 5 bảng dữ liệu, chuẩn hóa mã định danh, xử lý missing value, join thành bảng tổng thể duy nhất.",
    [
        "Kiểm tra kích thước, kiểu dữ liệu và giá trị thiếu (Missing Values) của 5 file CSV",
        "Xử lý làm sạch tên nghệ sĩ, mã bài hát (uri -> track_id), tên quốc gia",
        "Xử lý cột doanh số của bảng best-selling-artists (chuyển về số định lượng)",
        "Thực hiện thuật toán JOIN 5 bảng (Spotify Charts + Tracks + GDP + Country Codes + Best Selling)",
        "Lưu kết quả hoàn chỉnh vào data/processed/merged_spotify_data.csv"
    ],
    "data/raw/*.csv (5 files)",
    "data/processed/merged_spotify_data.csv"
)

# Notebook 2
make_nb(
    "02_eda.ipynb",
    "PHẦN 2: KHÁM PHÁ DỮ LIỆU ĐA CHIỀU (EXPLORATORY DATA ANALYSIS - EDA)",
    "Thành viên 2 (Data Analyst)",
    "Trực quan hóa phân phối các đặc trưng âm học, xu hướng biến đổi qua thời gian, sự khác biệt giữa các quốc gia và thể loại nhạc.",
    [
        "Phân tích phân phối đơn biến (Univariate) của: Danceability, Energy, Valence, Tempo, Loudness",
        "Vẽ ma trận tương quan nhiệt (Heatmap correlation) giữa các audio features và lượt streams",
        "Phân tích xu hướng âm nhạc theo dòng thời gian (2020 - 2022): Mùa hè vs Mùa đông, Trước vs Sau đại dịch",
        "So sánh gu âm nhạc theo từng khu vực địa lý (Châu Âu, Châu Á, Mỹ Latin)",
        "Lưu các biểu đồ cốt lõi vào dashboard/assets/ phục vụ báo cáo và Dashboard"
    ],
    "data/processed/merged_spotify_data.csv (hoặc data/sample/)",
    "Báo cáo trực quan hóa, biểu đồ EDA & Insight ban đầu"
)

# Notebook 3
make_nb(
    "03_model.ipynb",
    "PHẦN 3: XÂY DỰNG MÔ HÌNH DỰ BÁO XU HƯỚNG (PREDICTIVE MODELING)",
    "Thành viên 3 (Machine Learning Engineer)",
    "Huấn luyện mô hình Hồi quy Tuyến tính dự đoán lượt Stream/Popularity và Hồi quy Logistic phân loại bài hát Top Trending.",
    [
        "Chuẩn bị tập Train / Test split (80/20) và chuẩn hóa đặc trưng (StandardScaler / MinMaxScaler)",
        "Xây dựng Mô hình 1: Hồi quy Tuyến tính (Linear Regression) dự đoán log(streams) hoặc popularity",
        "Xây dựng Mô hình 2: Hồi quy Logistic (Logistic Regression) dự đoán xác suất bài hát lọt Top 50 Trending",
        "Đánh giá hiệu năng mô hình: R2, RMSE, MAE (cho Linear) và Accuracy, Precision, Recall, ROC-AUC, Confusion Matrix (cho Logistic)",
        "Trích xuất hệ số đặc trưng (Feature Coefficients) để xem yếu tố âm học nào quyết định bài hát hit",
        "Lưu mô hình đã huấn luyện thành file models/trend_predictor.pkl để Dashboard sử dụng"
    ],
    "data/processed/merged_spotify_data.csv (hoặc data/sample/)",
    "models/trend_predictor.pkl, models/model_metrics.json"
)

# Notebook 4
make_nb(
    "04_story.ipynb",
    "PHẦN 4: KHAI PHÁ INSIGHT & KỂ CHUYỆN BẰNG DỮ LIỆU (DATA STORYTELLING)",
    "Thành viên 4 (Data Storyteller / Business Analyst)",
    "Xâu chuỗi các phát hiện từ EDA và Mô hình thành một câu chuyện hoàn chỉnh: Vĩ mô (Kinh tế thế giới) -> Trung mô (Thị trường streaming) -> Vi mô (Đặc trưng bài hát).",
    [
        "Insight 1: Tương quan giữa tiềm lực kinh tế (GDP, nhóm thu nhập) và sở thích nghe nhạc",
        "Insight 2: Sự chuyển dịch gu âm nhạc toàn cầu (Tâm trạng xã hội phản chiếu qua chỉ số Valence)",
        "Insight 3: Nghệ sĩ bán đĩa nhiều nhất lịch sử có còn giữ vị thế thống trị trên Spotify?",
        "Insight 4: Công thức tạo nên một bài hit Spotify theo đúc kết từ mô hình ML",
        "Viết kịch bản kể chuyện hoàn chỉnh để đưa lên trang Storytelling của Dashboard và Slide thuyết trình"
    ],
    "Kết quả tổng hợp từ Notebook 01, 02, 03",
    "Báo cáo Storytelling & Kịch bản thuyết trình"
)
