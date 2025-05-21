import csv
import random
from datetime import datetime
import time
from tableau.models import ContentMetaDataModel


def random_date(start_date, end_date):
    start_timestamp = time.mktime(start_date.timetuple())
    end_timestamp = time.mktime(end_date.timetuple())
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    return datetime.fromtimestamp(random_timestamp)


PATH = r"tableau_contentmetadatamodel_202504140854.csv"
OUT_PATH = r"items_w_dates.csv"

new_rows = []

with open(OUT_PATH, "w", newline="", encoding="utf-8") as out_csvfile:
    fieldnames = ["id", "modified_date"]
    writer = csv.DictWriter(out_csvfile, fieldnames=fieldnames, delimiter="|")

    with open(PATH, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter="|")

        for row in reader:
            new_dict = {}
            new_dict["id"] = row["id"]

            rand_int = random.randint(1, 10)

            # OLD STUFF
            if rand_int >= 9:
                start = datetime(2024, 1, 1)
                end = datetime(2024, 6, 30)
                random_date_between = random_date(start, end)

            else:
                start = datetime(2025, 1, 1)
                end = datetime(2025, 4, 15)
                random_date_between = random_date(start, end)

            qry = ContentMetaDataModel.objects.get(id=row["id"])
            qry.modified_date = random_date_between
            qry.save()
