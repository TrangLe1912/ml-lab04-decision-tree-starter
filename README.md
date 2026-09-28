# LAB 04 — Decision Tree: từ dự đoán đến quy tắc hỗ trợ

**Học phần:** Nhập môn Học máy  
**Case study xuyên suốt:** DNU Learning Analytics Lab  
**Dataset:** Student Performance Factors  
**Thuật toán chính:** Decision Tree Classifier

## Câu hỏi trung tâm

> **Decision Tree đưa ra dự đoán bằng những câu hỏi nào, và làm thế nào để biến một cây quyết định thành các quy tắc có thể giải thích?**

Lab 04 tiếp tục **đúng bài toán, đúng target, đúng feature và đúng train/test split** của Lab 02–03. Điểm mới của Lab 04 là chuyển trọng tâm từ **chỉ dự đoán** sang **dự đoán + giải thích**.

- K-NN: khoảng cách → hàng xóm → bỏ phiếu;
- Naive Bayes: prior → likelihood → posterior;
- Decision Tree: câu hỏi → phân nhánh → leaf → dự đoán.

Nhãn giảng dạy vẫn là:

```python
Needs_Support = 1 nếu Exam_Score < 65
```

> `Needs_Support` chỉ là nhãn giả lập phục vụ học tập, **không phải quy định chính thức của DNU** và không được dùng để ra quyết định thật về sinh viên.

---

## Mục tiêu

Sau bài lab, sinh viên có thể:

1. Xây dựng `DecisionTreeClassifier` trên cùng bài toán của Lab 02–03.
2. Đánh giá mô hình bằng accuracy, precision, recall, F1 và confusion matrix.
3. Xác định **False Negative** trong bối cảnh sinh viên cần hỗ trợ.
4. Trực quan hóa cây và xác định Root Node, Decision Node, Leaf Node.
5. Chuyển một đường đi Root → Leaf thành quy tắc bằng ngôn ngữ tự nhiên.
6. Giải thích dự đoán của một sinh viên cụ thể bằng đường đi qua cây.
7. Phân tích ảnh hưởng của `max_depth` đến underfitting/overfitting và khả năng diễn giải.
8. So sánh `criterion="gini"` và `criterion="entropy"`.
9. Dùng `GridSearchCV` để tìm cấu hình phù hợp trong một không gian tham số nhỏ.
10. So sánh Decision Tree với K-NN và Gaussian Naive Bayes trên **cùng test set**.

---

## Thời lượng gợi ý

**Trên lớp (2 tiết):** Mission 1–6.  
**Sau lớp / mở rộng:** Mission 7–9 + Optional Challenge + Final Reflection.

---

## Cấu trúc repo

```text
ml-lab04-decision-tree-starter/
│
├── README.md
├── Lab04_DecisionTree.ipynb
├── requirements.txt
│
├── data/
│   └── .gitkeep
│
├── scripts/
│   └── download_data.py
│
├── tests/
│   └── check_lab04.py
│
└── .github/
    └── workflows/
        └── lab-check.yml
```

---

## Chuẩn bị môi trường

Khuyến nghị Python 3.12.

```bash
conda create --name machine_learning python=3.12
conda activate machine_learning
pip install -r requirements.txt
python scripts/download_data.py
jupyter notebook
```

Mở:

```text
Lab04_DecisionTree.ipynb
```

---

## Quy tắc quan trọng

### 1. Giữ nguyên bài toán của Lab 02–03

```python
Needs_Support = 1 nếu Exam_Score < 65
```

Feature chính:

```python
feature_cols = [
    "Hours_Studied",
    "Attendance",
    "Previous_Scores",
    "Sleep_Hours",
]
```

Dùng đúng:

```python
test_size=0.25
random_state=42
stratify=y
```

Mục đích là để K-NN, Naive Bayes và Decision Tree được so sánh trên cùng dữ liệu.

### 2. Không dùng `Exam_Score` làm feature

Nhãn `Needs_Support` được tạo trực tiếp từ `Exam_Score`. Nếu đưa `Exam_Score` vào `X`, mô hình sẽ nhìn thấy thông tin tạo ra chính target — đây là **target leakage**.

### 3. Decision Tree không cần StandardScaler

Không scale dữ liệu cho Decision Tree. Trong Mission so sánh mô hình, `StandardScaler` chỉ được dùng cho K-NN để giữ đúng pipeline của Lab 02.

### 4. Không chỉ nhìn Accuracy

Trong case study, đặc biệt chú ý:

> **False Negative = sinh viên thực tế cần hỗ trợ nhưng mô hình dự đoán không cần hỗ trợ.**

Sinh viên phải đọc confusion matrix và thảo luận trade-off giữa precision và recall.

### 5. Cây sâu hơn không mặc định là tốt hơn

Phải quan sát đồng thời:

- train accuracy;
- test accuracy;
- số node;
- số leaf;
- khả năng diễn giải.

### 6. GridSearchCV không thay cho phân tích

Sau khi tìm được `best_params_`, vẫn phải:

1. đánh giá mô hình;
2. trực quan hóa cây;
3. đọc decision rules;
4. giải thích một prediction cụ thể.

### 7. Mỗi Mission cần có code + nhận xét

Không chỉ chạy code và chép con số. Hãy giải thích kết quả bằng Markdown.

---

## Các Mission

- **Mission 1 — Back to DNU case study:** tái tạo đúng dữ liệu và train/test split của Lab 02–03.
- **Mission 2 — Baseline Decision Tree:** huấn luyện cây đầu tiên.
- **Mission 3 — Evaluate beyond Accuracy:** accuracy, precision, recall, F1, confusion matrix và False Negative.
- **Mission 4 — Read the Tree:** trực quan hóa cây sâu 3 tầng và đọc Root → Leaf thành quy tắc.
- **Mission 5 — Complexity matters:** thử `max_depth ∈ {2, 3, 5, None}`.
- **Mission 6 — Gini vs Entropy:** so sánh hiệu năng và cấu trúc cây.
- **Mission 7 — Small GridSearch:** tinh chỉnh một không gian tham số nhỏ.
- **Mission 8 — Explain one student:** dùng `decision_path()` để giải thích một dự đoán.
- **Mission 9 — Model Showdown:** so K-NN, GaussianNB và Decision Tree trên cùng test set.
- **Optional Challenge — Decision Tree Regression:** thử `DecisionTreeRegressor` trên California Housing.
- **Final — Model Reflection Card:** tổng kết prediction → explanation.

---

## Sản phẩm cần nộp

Bài được xem là hoàn thành khi:

- `Lab04_DecisionTree.ipynb` chạy được từ đầu đến cuối;
- Mission 1–9 có code và nhận xét;
- có ít nhất **2 decision rules** được viết lại bằng ngôn ngữ tự nhiên;
- có giải thích đường đi của **1 sinh viên** từ Root → Leaf;
- có bảng thí nghiệm `max_depth`;
- có so sánh Gini/Entropy;
- có bảng K-NN vs Naive Bayes vs Decision Tree;
- có Final Reflection;
- bài được push lên branch `main`.

Kiểm tra trước khi nộp:

```bash
python scripts/download_data.py
python tests/check_lab04.py
```

Push bài:

```bash
git add .
git commit -m "Complete Lab 04 Decision Tree"
git push
```

---

## GitHub Actions

Mỗi lần push lên `main`, Actions sẽ:

1. cài Python và dependencies;
2. tải Student Performance Factors dataset;
3. kiểm tra cấu trúc repo/notebook;
4. kiểm tra không có `Exam_Score` trong `feature_cols`;
5. kiểm tra các thành phần cốt lõi của Lab 04;
6. chạy notebook trong môi trường sạch.

GitHub Actions chỉ kiểm tra phần kỹ thuật. **Phần giải thích decision rules, phân tích trade-off và lập luận của sinh viên vẫn cần giảng viên đánh giá.**
