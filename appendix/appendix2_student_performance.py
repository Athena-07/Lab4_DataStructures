"""Lab 4 Appendix - Exercise 2: Student Performance Data Analyzer
Athena R. Zozobrado | TUPM-26-1872
"""
import pandas as pd

LAST_NAME = "ZOZOBRADO"
SEED_NUM = 261872                      # digits of TUPM-26-1872
FAVORITE_ARTIST = "TAYLORSWIFT"        # Taylor Swift (letters only)

def gen(i):
    """Generate a number from SEED_NUM and the character position of FAVORITE_ARTIST."""
    pos = i % len(FAVORITE_ARTIST)
    return SEED_NUM + ord(FAVORITE_ARTIST[pos]) * (pos + 1) + i

def show(title, df):
    print(f"\n=== {title} ===")
    print(df.to_string(index=False))

print(f"STUDENT: Athena R. Zozobrado | ID: TUPM-26-1872 | SEED_NUM={SEED_NUM} | ARTIST={FAVORITE_ARTIST}")

students = [f"{LAST_NAME}_S{i}" for i in range(1, 6)]
subjects = ["PROGRAMMING", "MATHEMATICS", "ELECTRONICS", "PHYSICS", "ENGLISH"]

def category(sc):
    if sc is None: return "INCOMPLETE"
    return ("OUTSTANDING" if sc >= 90 else "VERY GOOD" if sc >= 85 else
            "SATISFACTORY" if sc >= 75 else "NEEDS IMPROVEMENT")

rows, n = [], 0
for st in students:
    for sb in subjects:
        rows.append([st, sb, 60 + gen(n) % 41]); n += 1     # scores 60-100
rows.append(list(rows[0]))                                   # repeated student-subject
rows[14][2] = None                                           # missing score (S3-ENGLISH)
df2 = pd.DataFrame(rows, columns=["Student", "Subject", "Score"])
df2["Category"] = df2.Score.apply(lambda x: category(None if pd.isna(x) else x))
show("Generated Performance Records", df2)
show("Organized Student/Subject Data", df2.sort_values(["Student", "Subject"]))
show("Repeated Records", df2[df2.duplicated(["Student", "Subject"], keep=False)])
show("Incomplete Records", df2[df2.Score.isna()])
valid2 = df2.drop_duplicates(["Student", "Subject"]).dropna(subset=["Score"])
stu = valid2.groupby("Student").Score.agg(Subjects="count", Average="mean", Highest="max").round(2)
sub = valid2.groupby("Subject").Score.agg(Students="count", Average="mean", Highest="max").round(2)
show("Student Summary (ordered by average, desc)", stu.sort_values("Average", ascending=False).reset_index())
show("Subject Summary (ordered by average, desc)", sub.sort_values("Average", ascending=False).reset_index())
print("\nFINAL REPORT: valid records =", len(valid2), "| class average =", round(valid2.Score.mean(), 2),
      "| top student =", stu.Average.idxmax(), "| top subject =", sub.Average.idxmax())
