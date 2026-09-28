from pathlib import Path
import ast
import nbformat

required_files = [
    Path("README.md"),
    Path("requirements.txt"),
    Path("data/StudentPerformanceFactors.csv"),
    Path("Lab04_DecisionTree.ipynb"),
]

missing = [str(p) for p in required_files if not p.exists()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

nb = nbformat.read("Lab04_DecisionTree.ipynb", as_version=4)
markdown = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
code = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "code")

required_sections = [
    "Mission 1", "Mission 2", "Mission 3", "Mission 4",
    "Mission 5", "Mission 6", "Mission 7", "Mission 8", "Mission 9",
    "Optional Challenge", "Model Reflection Card",
]
missing_sections = [s for s in required_sections if s.lower() not in markdown.lower()]
if missing_sections:
    raise SystemExit("Notebook is missing sections: " + ", ".join(missing_sections))

prohibited_paths = ["/content/drive/", "C:/Users/", "C:\\Users\\", "/Users/"]
found_paths = [p for p in prohibited_paths if p in code]
if found_paths:
    raise SystemExit("Prohibited absolute path(s) found: " + ", ".join(found_paths))

for cell in nb.cells:
    if cell.cell_type != "code":
        continue
    try:
        tree = ast.parse(cell.source)
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "feature_cols":
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        value = None
                    if isinstance(value, list) and "Exam_Score" in value:
                        raise SystemExit("Target leakage: Exam_Score must not be in feature_cols")

required_code_tokens = [
    "DecisionTreeClassifier",
    "plot_tree",
    "confusion_matrix",
    "GridSearchCV",
    "decision_path",
    "KNeighborsClassifier",
    "GaussianNB",
]
missing_tokens = [t for t in required_code_tokens if t not in code]
if missing_tokens:
    raise SystemExit("Notebook is missing expected concepts: " + ", ".join(missing_tokens))

placeholders = ["[VIẾT", "[TRẢ LỜI", "Họ tên: ...", "MSSV: ...", "Lớp: ..."]
found = [p for p in placeholders if p.lower() in markdown.lower()]

print("✅ Required files found")
print("✅ Notebook structure is valid")
print("✅ No prohibited absolute paths found")
print("✅ feature_cols does not contain Exam_Score (when statically detectable)")
print("✅ Core Decision Tree / comparison concepts are present")

if found:
    print("⚠️ Notebook still contains answer placeholders:")
    for item in found:
        print("  -", item)
else:
    print("✅ No common answer placeholders detected")
