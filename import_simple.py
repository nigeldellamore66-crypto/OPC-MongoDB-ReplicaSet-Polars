import csv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
col = client["noscites"]["logements"]

def to_bool(v):
    v = ("" if v is None else str(v)).strip().lower()
    if v in ("true", "t", "1", "yes", "y"): return True
    if v in ("false", "f", "0", "no", "n"): return False
    return None

def to_int(v):
    v = ("" if v is None else str(v)).strip()
    if v == "": return None
    try: return int(float(v))
    except: return None

# 1) Tag Paris sur tout ce qui n'a pas encore de ville
col.update_many({"city_name": {"$exists": False}}, {"$set": {"city_name": "Paris"}})

# 2) Reset Lyon
col.delete_many({"city_name": "Lyon"})

# 3) Import Lyon (CSV -> Mongo) + tag city + conversions minimales
docs = []
with open("listings_Lyon.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        row["city_name"] = "Lyon"
        if "id" in row: row["id"] = to_int(row["id"])
        for b in ("host_is_superhost", "instant_bookable", "has_availability"):
            if b in row: row[b] = to_bool(row[b])
        docs.append(row)

col.insert_many(docs)
print(f" Lyon importé: {len(docs)} docs")
