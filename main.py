# Import required libraries
import os
from random import choice
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (works in VS Code)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# Directory setup 
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")

for d in [OUTPUT_DIR, GRAPHS_DIR]:
    os.makedirs(d, exist_ok=True)

SEPARATOR = "=" * 65

#  STEP 1 – Load Dataset

def load_data(filepath: str) -> pd.DataFrame:
    print(f"\n{SEPARATOR}")
    print("  STEP 1 : Loading Dataset")
    print(SEPARATOR)
    df = pd.read_csv(filepath)
    print(f"  ✔  Loaded  {len(df)} records  |  {df.shape[1]} columns")
    print(f"  Columns : {list(df.columns)}")
    return df

#  STEP 2 – Data Cleaning

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n{SEPARATOR}")
    print("  STEP 2 : Data Cleaning")
    print(SEPARATOR)

    # Missing values
    missing = df.isnull().sum()
    print("\n  Missing values per column:")
    print(missing.to_string())
    df.dropna(inplace=True)
    print(f"\n  ✔  Rows after dropping missing values : {len(df)}")

    #  Duplicates
    dupes = df.duplicated().sum()
    print(f"  Duplicate rows found : {dupes}")
    df.drop_duplicates(inplace=True)
    print(f"  ✔  Rows after removing duplicates    : {len(df)}")

    # Validate marks (must be 0–100)
    mark_cols = ["Math_Marks", "Science_Marks", "English_Marks"]
    for col in mark_cols:
        invalid = df[(df[col] < 0) | (df[col] > 100)]
        if not invalid.empty:
            print(f"  ⚠  Invalid marks in '{col}': {len(invalid)} row(s) removed.")
            df = df[(df[col] >= 0) & (df[col] <= 100)]

    df.reset_index(drop=True, inplace=True)
    print(f"\n  ✔  Clean dataset : {len(df)} records ready for analysis.")
    return df

#  STEP 3 – Calculate Derived Columns

def calculate_results(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n{SEPARATOR}")
    print("  STEP 3 : Calculating Results")
    print(SEPARATOR)

    mark_cols = ["Math_Marks", "Science_Marks", "English_Marks"]
    max_marks  = len(mark_cols) * 100   # 300

    df["Total_Marks"] = df[mark_cols].sum(axis=1)
    df["Percentage"]  = (df["Total_Marks"] / max_marks * 100).round(2)

    def assign_grade(pct: float) -> str:
        if pct >= 90: return "A"
        if pct >= 75: return "B"
        if pct >= 60: return "C"
        if pct >= 40: return "D"
        return "F"

    df["Grade"]       = df["Percentage"].apply(assign_grade)
    df["Pass_Fail"]   = df["Percentage"].apply(lambda p: "Pass" if p >= 40 else "Fail")

    print("  ✔  Total_Marks, Percentage, Grade, Pass_Fail — computed.")
    return df


#  STEP 4 – Insights

def generate_insights(df: pd.DataFrame) -> None:
    print(f"\n{SEPARATOR}")
    print("  STEP 4 : Key Insights")
    print(SEPARATOR)

    avg_pct = df["Percentage"].mean()
    print(f"\n  Overall Average Percentage : {avg_pct:.2f}%")

    top_student = df.loc[df["Percentage"].idxmax()]
    print(f"\n  🏆  Highest Scorer : {top_student['Name']} "
          f"({top_student['Percentage']}% | Grade {top_student['Grade']})")

    low_student = df.loc[df["Percentage"].idxmin()]
    print(f"  ⬇   Lowest Scorer  : {low_student['Name']} "
          f"({low_student['Percentage']}% | Grade {low_student['Grade']})")

    subjects = {"Math": "Math_Marks", "Science": "Science_Marks", "English": "English_Marks"}
    print("\n  Subject-wise Toppers:")
    for subj, col in subjects.items():
        topper = df.loc[df[col].idxmax()]
        print(f"    {subj:>10} → {topper['Name']:25s} ({topper[col]} marks)")

    pass_pct = (df["Pass_Fail"] == "Pass").mean() * 100
    print(f"\n  Pass Percentage : {pass_pct:.2f}%")

    print("\n  Grade Distribution:")
    grade_counts = df["Grade"].value_counts().sort_index()
    for grade, count in grade_counts.items():
        bar = "█" * int(count)
        print(f"    Grade {grade} : {bar}  ({count} students)")


#  STEP 5 – Visualizations

PALETTE = {
    "bg":      "#0f1117",
    "panel":   "#1a1d27",
    "accent1": "#4f8ef7",
    "accent2": "#f7934f",
    "accent3": "#4ff7a1",
    "text":    "#e8eaf0",
    "subtext": "#8890a8",
}

def _apply_dark_style(ax, fig):
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["panel"])
    ax.tick_params(colors=PALETTE["subtext"])
    ax.xaxis.label.set_color(PALETTE["text"])
    ax.yaxis.label.set_color(PALETTE["text"])
    ax.title.set_color(PALETTE["text"])
    for spine in ax.spines.values():
        spine.set_edgecolor("#2e3347")


# Bar chart — average marks by subject 
def plot_average_marks(df: pd.DataFrame, path: str) -> None:
    subjects   = ["Math_Marks", "Science_Marks", "English_Marks"]
    labels     = ["Mathematics", "Science", "English"]
    averages   = [df[s].mean() for s in subjects]
    colors     = [PALETTE["accent1"], PALETTE["accent2"], PALETTE["accent3"]]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    _apply_dark_style(ax, fig)

    bars = ax.bar(labels, averages, color=colors, width=0.5,
                  edgecolor="#2e3347", linewidth=0.8, zorder=3)

    for bar, val in zip(bars, averages):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.8,
                f"{val:.1f}", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color=PALETTE["text"])

    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
    ax.set_ylabel("Average Marks (out of 100)", fontsize=11)
    ax.set_title("Average Marks by Subject", fontsize=14, fontweight="bold", pad=16)
    ax.grid(axis="y", color="#2e3347", linestyle="--", linewidth=0.7, zorder=0)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✔  Saved → {path}")


#  Pie chart — grade distribution 
def plot_grade_distribution(df: pd.DataFrame, path: str) -> None:
    grade_order  = ["A", "B", "C", "D", "F"]
    grade_counts = df["Grade"].value_counts()
    grades       = [g for g in grade_order if g in grade_counts.index]
    counts       = [grade_counts[g] for g in grades]
    colors       = ["#4f8ef7", "#4ff7a1", "#f7e74f", "#f7934f", "#f74f6e"]

    fig, ax = plt.subplots(figsize=(7.5, 7))
    fig.patch.set_facecolor(PALETTE["bg"])

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=grades,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors[:len(grades)],
        pctdistance=0.78,
        wedgeprops=dict(edgecolor=PALETTE["bg"], linewidth=2),
    )
    for t in texts:
        t.set_color(PALETTE["text"]); t.set_fontsize(13); t.set_fontweight("bold")
    for a in autotexts:
        a.set_color(PALETTE["bg"]); a.set_fontsize(10); a.set_fontweight("bold")

    ax.set_title("Grade Distribution", fontsize=14, fontweight="bold",
                 color=PALETTE["text"], pad=20)

    legend_labels = [f"Grade {g}  ({c} students)" for g, c in zip(grades, counts)]
    ax.legend(wedges, legend_labels, loc="lower center",
              bbox_to_anchor=(0.5, -0.12), ncol=3,
              fontsize=9, framealpha=0.2,
              labelcolor=PALETTE["text"])

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✔  Saved → {path}")


#  Histogram — percentage distribution 
def plot_percentage_histogram(df: pd.DataFrame, path: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    _apply_dark_style(ax, fig)

    n, bins, patches = ax.hist(df["Percentage"], bins=15,
                               edgecolor="#0f1117", linewidth=0.8, zorder=3)

    # Colour bins by grade zone
    zone_colors = {(90, 100): "#4f8ef7", (75, 90): "#4ff7a1",
                   (60, 75): "#f7e74f",  (40, 60): "#f7934f", (0, 40): "#f74f6e"}
    for patch, left in zip(patches, bins[:-1]):
        for (lo, hi), col in zone_colors.items():
            if lo <= left < hi:
                patch.set_facecolor(col); break

    ax.set_xlabel("Percentage (%)", fontsize=11)
    ax.set_ylabel("Number of Students", fontsize=11)
    ax.set_title("Distribution of Student Percentages", fontsize=14,
                 fontweight="bold", pad=16)
    ax.grid(axis="y", color="#2e3347", linestyle="--", linewidth=0.7, zorder=0)

    # Vertical mean line
    mean_pct = df["Percentage"].mean()
    ax.axvline(mean_pct, color="#ffffff", linewidth=1.4, linestyle="--", zorder=4)
    ax.text(mean_pct + 0.5, ax.get_ylim()[1] * 0.93,
            f"Mean: {mean_pct:.1f}%", color=PALETTE["text"], fontsize=10)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✔  Saved → {path}")


def create_visualizations(df: pd.DataFrame) -> None:
    print(f"\n{SEPARATOR}")
    print("  STEP 5 : Generating Visualizations")
    print(SEPARATOR)
    plot_average_marks(df,        os.path.join(GRAPHS_DIR, "average_marks.png"))
    plot_grade_distribution(df,   os.path.join(GRAPHS_DIR, "grade_distribution.png"))
    plot_percentage_histogram(df, os.path.join(GRAPHS_DIR, "percentage_histogram.png"))


#  STEP 6 – Save Results

def save_results(df: pd.DataFrame) -> None:
    print(f"\n{SEPARATOR}")
    print("  STEP 6 : Saving Results")
    print(SEPARATOR)
    out_path = os.path.join(OUTPUT_DIR, "result_analysis.csv")
    df.to_csv(out_path, index=False)
    print(f"  ✔  Result CSV saved → {out_path}")


#  STEP 7 – Display Tables

def display_tables(df: pd.DataFrame) -> None:
    display_cols = ["Student_ID", "Name", "Gender",
                    "Math_Marks", "Science_Marks", "English_Marks",
                    "Total_Marks", "Percentage", "Grade", "Pass_Fail"]

    print(f"\n{SEPARATOR}")
    print("  STEP 7a : Top 10 Students")
    print(SEPARATOR)
    top10 = df.nlargest(10, "Percentage")[display_cols].reset_index(drop=True)
    top10.index += 1
    print(top10.to_string())

    print(f"\n{SEPARATOR}")
    print("  STEP 7b : Bottom 10 Students")
    print(SEPARATOR)
    bot10 = df.nsmallest(10, "Percentage")[display_cols].reset_index(drop=True)
    bot10.index += 1
    print(bot10.to_string())

    print(f"\n{SEPARATOR}")
    print("  STEP 7c : Summary Statistics")
    print(SEPARATOR)
    stat_cols = ["Math_Marks", "Science_Marks", "English_Marks",
                 "Total_Marks", "Percentage"]
    print(df[stat_cols].describe().round(2).to_string())



#  MAIN
def main():
    print(f"\n{'*' * 65}")
    print("  🎓  Student Result Analysis System")
    print(f"{'*' * 65}")

    csv_path = os.path.join(DATA_DIR, "students.csv")
    df = load_data(csv_path)
    df = clean_data(df)

    # ================= ADD =================
    choice = "no"  # Automatically skip user input when running in GitHub Actions (CI)

    if choice.lower() == "yes":
        student_id = input("Enter Student ID: ")
        name = input("Enter Name: ")
        gender = input("Enter Gender: ")

        math = int(input("Enter Math Marks: "))
        science = int(input("Enter Science Marks: "))
        english = int(input("Enter English Marks: "))

        new_student = {
            "Student_ID": student_id,
            "Name": name,
            "Gender": gender,
            "Math_Marks": math,
            "Science_Marks": science,
            "English_Marks": english
        }

        df.loc[len(df)] = new_student
        df.to_csv(csv_path, index=False)

        print("✅ New record added successfully!")
    else:
        print("Nothing to do.")

    # ================= EDIT =================
    edit_choice = "no"  # Automatically skip user input when running in GitHub Actions (CI) 

    if edit_choice.lower() == "yes":
        student_id = input("Enter Student ID to edit: ")

        if student_id in df["Student_ID"].values:

            print("\nCurrent Record:")
            print(df[df["Student_ID"] == student_id])

            new_math = int(input("Enter new Math Marks: "))
            new_science = int(input("Enter new Science Marks: "))
            new_english = int(input("Enter new English Marks: "))

            df.loc[df["Student_ID"] == student_id, "Math_Marks"] = new_math
            df.loc[df["Student_ID"] == student_id, "Science_Marks"] = new_science
            df.loc[df["Student_ID"] == student_id, "English_Marks"] = new_english

            df.to_csv(csv_path, index=False)

            print("✅ Record updated successfully!")
        else:
            print("❌ Student ID not found!")
    else:
        print("Nothing to do.")

    # ================= SEARCH =================
    search_choice = "no"  # Automatically skip user input when running in GitHub Actions (CI) 

    if search_choice.lower() == "yes":
        student_id = input("Enter Student ID to search: ")

        if student_id in df["Student_ID"].values:
            result = df[df["Student_ID"] == student_id]

            print("\nStudent Found:")
            print(result.to_string(index=False))
        else:
            print("❌ Student ID not found!")
    else:
        print("Nothing to do.")

    # ================= DELETE =================
    delete_choice = "no"  # Automatically skip user input when running in GitHub Actions (CI) 

    if delete_choice.lower() == "yes":
        student_id = input("Enter Student ID to delete: ")

        if student_id in df["Student_ID"].values:
            df = df[df["Student_ID"] != student_id]
            df.to_csv(csv_path, index=False)
            print("✅ Record deleted successfully!")
        else:
            print("❌ Student ID not found!")
    else:
        print("Nothing to do.")
    df = calculate_results(df)
    generate_insights(df)
    create_visualizations(df)
    save_results(df)
    display_tables(df)


if __name__ == "__main__":
    main()
