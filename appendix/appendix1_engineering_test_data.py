"""Lab 4 Appendix - Exercise 1: Engineering Test Data Organizer
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

sources = [f"{LAST_NAME}_T{i}" for i in range(1, 6)]
cats = ["TEMPERATURE", "VOLTAGE", "CURRENT", "PRESSURE", "SPEED"]
rows, n = [], 0
for s in sources:
    for c in cats:
        rows.append((s, c, round(gen(n) % 1000 / 10, 1))); n += 1
rows.append(rows[0])                                        # repeated record
rows += [(sources[1], "TEMPERATURE", round(gen(n) % 1000 / 10, 1)),   # additional data
         (sources[1], "TEMPERATURE", round(gen(n + 1) % 1000 / 10, 1)),
         (sources[2], "VOLTAGE", round(gen(n + 2) % 1000 / 10, 1)),
         (sources[2], "VOLTAGE", round(gen(n + 3) % 1000 / 10, 1))]
df1 = pd.DataFrame(rows, columns=["Source", "Category", "Value"])
show("Generated Test Data", df1)
show("Organized Test Data (by source, category)", df1.sort_values(["Source", "Category"]))
dup = df1[df1.duplicated(keep=False)]
show("Repeated Records", dup.drop_duplicates())
print("Distinct sources:", df1.Source.nunique(), "| Distinct categories:", df1.Category.nunique(),
      "| Distinct records:", len(df1.drop_duplicates()))
clean1 = df1.drop_duplicates()
cat_sum = clean1.groupby("Category").Value.agg(Count="count", Sum="sum", Mean="mean", Min="min", Max="max").round(2)
src_sum = clean1.groupby("Source").Value.agg(Count="count", Mean="mean").round(2)
show("Category Summary (Processed Results)", cat_sum.reset_index())
show("Source Summary", src_sum.reset_index())
show("Ordered Results (by mean, descending)", cat_sum.sort_values("Mean", ascending=False).reset_index())
print(f"\nFINAL SUMMARY: {len(df1)} records, {len(clean1)} distinct, "
      f"overall mean={clean1.Value.mean():.2f}, max={clean1.Value.max()}, min={clean1.Value.min()}")
