# 🎓 Student Result Analysis System (Python Data Analytics Project)
A beginner-friendly Python project that reads a student dataset, performs
data cleaning and analysis, generates grade/pass-fail statistics, and
produces three publication-ready charts — all in a single `main.py` run.

---

## 📁 Project Structure

## ⭐ Project Highlights

Student_Result_Analysis/
├── data/
│   └── students.csv          ← Raw input dataset (55 records)
├── output/
│   └── result_analysis.csv   ← Analysed results (auto-generated)
├── graphs/
│   ├── average_marks.png     ← Bar chart  (auto-generated)
│   ├── grade_distribution.png← Pie chart  (auto-generated)
│   └── percentage_histogram.png ← Histogram (auto-generated)
├── main.py                   ← Main analysis script
├── requirements.txt          ← Python dependencies
└── README.md                 ← This file

## ⭐ Project Highlights

- Automated student performance analysis
- Real-world data cleaning pipeline
- Grade classification system
- Interactive statistical insights
- Publication-ready visualizations
- Fully automated single-run execution


## 📋 Dataset Columns

| Column           | Description                        |
|------------------|------------------------------------|
| `Student_ID`     | Unique identifier (e.g. S001)      |
| `Name`           | Full name of the student           |
| `Gender`         | Male / Female                      |
| `Math_Marks`     | Marks out of 100                   |
| `Science_Marks`  | Marks out of 100                   |
| `English_Marks`  | Marks out of 100                   |

---

## ⚙️ Installation

git clone https://github.com/your-username/student-result-analysis.git
git clone <repo-url>

## 📂 Output Explanation

After running the project:

- `output/result_analysis.csv` → Cleaned + analyzed dataset
- `graphs/average_marks.png` → Subject-wise performance comparison
- `graphs/grade_distribution.png` → Grade distribution in class
- `graphs/percentage_histogram.png` → Student performance spread

## 🚀 Future Improvements

- Add GUI using Streamlit
- Store data in database (MySQL)
- Add login system for admin
- Export PDF report of results
- Deploy as web dashboard

### 3 — Install dependencies
pip install -r requirements.txt

## ▶️ Run
python main.py

## 👨‍💻 Author
Built by an Engineering student as a Data Analysis project using Python.

## 📊 What the Script Does
| Step | Task |
|------|------|
| 1 | Load `data/students.csv` with Pandas |
| 2 | Data cleaning — missing values, duplicates, mark validation |
| 3 | Calculate Total Marks, Percentage, Grade (A/B/C/D/F), Pass/Fail |
| 4 | Print key insights (toppers, pass %, grade distribution) |
| 5 | Generate 3 Matplotlib charts saved to `graphs/` |
| 6 | Export cleaned + analysed data to `output/result_analysis.csv` |
| 7 | Display Top 10, Bottom 10, and summary statistics |



## 🏅 Grading Scheme

| Grade | Percentage Range |
|-------|-----------------|
| A     | 90 % – 100 %    |
| B     | 75 % – 89 %     |
| C     | 60 % – 74 %     |
| D     | 40 % – 59 %     |
| F     | Below 40 %      |

> **Pass** = Percentage ≥ 40 %



## 📈 Expected Output (Screenshots)
> Place your screenshots here after running the project.
**average_marks.png** — Bar chart comparing the class average for each subject.
**grade_distribution.png** — Pie chart showing how many students fall in each grade band.
**percentage_histogram.png** — Histogram of the full percentage distribution with a mean reference line.



## 🛠️ Tech Stack
- **Python 3.8+**
- **Pandas** — data loading, cleaning, and manipulation
- **NumPy** — numerical operations
- **Matplotlib** — visualisation



## 📝 License
Free to use for learning and educational purposes.
