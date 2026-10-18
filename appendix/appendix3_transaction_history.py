"""Lab 4 Appendix - Exercise 3: Transaction History Analyzer
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

customers = [f"{LAST_NAME}_C{i}" for i in range(1, 6)]
prices = {"NOTEBOOK": 45.0, "PEN": 15.0, "USB": 350.0, "HEADPHONES": 899.0, "CALCULATOR": 650.0}
prods = list(prices)
rows = []
for i in range(10):
    c, p = customers[i % 5], prods[(i * 2 + i // 5) % 5]
    rows.append((f"TX{i+1:02d}", c, p, 1 + gen(i) % 9, prices[p]))
rows.append(("TX11", rows[0][1], rows[0][2], 1 + gen(10) % 9, rows[0][4]))   # repeated purchase
df3 = pd.DataFrame(rows, columns=["TxID", "Customer", "Product", "Qty", "Price"])
df3["Total"] = df3.Qty * df3.Price
show("Generated Transaction Records", df3)
show("Organized Transaction Data", df3.sort_values(["Customer", "Product"]))
show("Repeated Purchases", df3[df3.duplicated(["Customer", "Product"], keep=False)])
print("Distinct customers:", df3.Customer.nunique(), "| Distinct products:", df3.Product.nunique())
cust = df3.groupby("Customer").agg(Transactions=("TxID", "count"), Items=("Qty", "sum"), Spent=("Total", "sum"))
prod = df3.groupby("Product").agg(Transactions=("TxID", "count"), Units=("Qty", "sum"), Revenue=("Total", "sum"))
show("Customer Summary (by spending, desc)", cust.sort_values("Spent", ascending=False).reset_index())
show("Product Summary (by revenue, desc)", prod.sort_values("Revenue", ascending=False).reset_index())
print(f"\nOVERALL: {len(df3)} transactions | {df3.Qty.sum()} items | total value = PHP {df3.Total.sum():,.2f} "
      f"| top customer = {cust.Spent.idxmax()} | top product = {prod.Revenue.idxmax()}")
