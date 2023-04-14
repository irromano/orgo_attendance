from orgo_consumer import consumer
import sys
import pandas as pd
import re
import io
from typing import Tuple
import numpy as np

FILENAME = "Weekly Attendance for Orgo 2 Recitation with Miga.xlsx"

ConsumerDict = dict()

def read_excel(file: str) -> Tuple[str, pd.DataFrame]:
    with open(file, "rb") as f:
        file_io_obj = io.BytesIO(f.read())
        excelDict = pd.read_excel(file_io_obj, sheet_name=None).copy()
        for sheet, data in excelDict.items():
            rec = re.search("rec", sheet, re.IGNORECASE)
            if rec:
                ConsumerDict[sheet[rec.start():].capitalize()] = consumer(sheet[rec.start():].capitalize())
                ConsumerDict[sheet[rec.start():].capitalize()].read_data(data)
            else:
                finalDf = data.copy(deep=True)
                finalSheet = sheet
        return finalSheet, finalDf


def take_attendance(finalSheet: str, finalDf: pd.DataFrame):
    for sheet, consumer in ConsumerDict.items():
        consumer_df = consumer.students()
        present = finalDf[['First', 'Last']].stack().isin(consumer_df.stack().values).unstack()
        conditions = [
            present["First"].eq(True) & present["Last"].eq(True)
        ]
        finalDf[sheet] = np.select(conditions, ['x'], default="")
        unknownStudents = consumer_df[['First', 'Last']].stack().isin(finalDf[['First', 'Last']].stack().values).unstack()
        consumer_df = consumer_df[(unknownStudents.First == False) | (unknownStudents.Last == False)]
        print("\n\nThe following students from {sheet} were not found in the Final attendance sheet.\nYou must check them manually.")
        print(consumer_df)
    finalDf.fillna(' ')
    return finalDf

def main():
    filename = sys.argv[1]
    if not filename:
        print("Please drag an attendance Excel file on this bat file.")
        return
    print(f"Reading file at {filename}")
    finalSheet, finalDf = read_excel(filename)
    finalDf = take_attendance(finalSheet, finalDf)
    print(f"Writing attendance to {filename}")
    with pd.ExcelWriter(filename, mode="a", engine="openpyxl", if_sheet_exists='replace') as writer:
        finalDf.to_excel(writer, sheet_name="FINAL ")  
    print(f"Attendance has been recorded in {filename}.")

if __name__ == "__main__":
    main()