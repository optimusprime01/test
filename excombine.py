import os
import sys
import datetime
import csv
import logging

FORMAT = "%(asctime)-15s %(levelname)s :: %(message)s"
Formatter = logging.Formatter(FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
clih = logging.StreamHandler(sys.stdout)
clih.setLevel(logging.DEBUG)
clih.setFormatter(Formatter)
logger.addHandler(clih)

BOFA = ["Posted Date", "Reference Number", "Payee", "Address", "Amount"]
AMEX = ["Date", "Reference", "Description", "Card Member", "Card Number", "Amount", "Category", "Type"]
DISCOVER = ["Trans. Date", "Post Date", "Description", "Amount", "Category"]


class Expense:
    def __init__(self):
        self.expense_date = None
        self.expense_amount = 0
        self.iscredit_bool = None
        self.expense_description = ""
        self.expense_address = ""
        self.reference_number = ""
        self.expense_category = ""

    @classmethod
    def from_dict(cls, input_map, expense_type):
        expense = cls()
        if expense_type == "bofa":
            tmp_amount = float(input_map.get("Amount", 0))
            expense.expense_amount = abs(tmp_amount)
            date_time_obj = datetime.datetime.strptime(input_map.get("Posted Date"), "%m/%d/%Y")
            expense.expense_date = date_time_obj
            expense.iscredit_bool = tmp_amount > 0
            expense.expense_description = input_map.get("Payee")
            expense.expense_address = input_map.get("Address")
            expense.reference_number = input_map.get("Reference Number")
        elif expense_type == "amex":
            tmp_amount = float(input_map.get("Amount", 0))
            expense.expense_amount = abs(tmp_amount)
            date_time_obj = datetime.datetime.strptime(input_map.get("Date"), "%m/%d/%y")
            expense.expense_date = date_time_obj
            expense.iscredit_bool = tmp_amount < 0
            expense.expense_description = input_map.get("Description")
            expense.reference_number = input_map.get("Reference")
            expense.expense_category = input_map.get("Category")
        elif expense_type == "discover":
            tmp_amount = float(input_map.get("Amount", 0))
            expense.expense_amount = abs(tmp_amount)
            date_time_obj = datetime.datetime.strptime(input_map.get("Post Date"), "%m/%d/%Y")
            expense.expense_date = date_time_obj
            expense.iscredit_bool = tmp_amount < 0
            expense.expense_description = input_map.get("Description")
            expense.expense_category = input_map.get("Category")
        return expense

    @property
    def date(self):
        return self.expense_date.strftime("%m/%d/%Y")

    @property
    def amount(self):
        return self.expense_amount

    @property
    def iscredit(self):
        return self.iscredit_bool

    @property
    def map(self):
        if self.iscredit_bool:
            amount = self.amount * -1
            type = "CREDIT"
        else:
            amount = self.amount
            type = "DEBIT"
        output_map = {
            "Date": self.date.strip(),
            "Amount": amount,
            "Reference": self.reference_number.strip(),
            "Category": self.expense_category.strip(),
            "Address": self.expense_address.strip(),
            "Description": self.expense_description.strip(),
            "Type": type,
        }
        return output_map

    def __eq__(self, other):
        return self.expense_date == other.expense_date

    def __lt__(self, other):
        return self.expense_date < other.expense_date


if __name__ == "__main__":
    src_path = os.path.abspath("./data")
    files = os.listdir(src_path)
    master_data = []
    for file in files:
        file_path = os.path.join(src_path, file)
        logger.debug("Input file : {}".format(file_path))
        with open(file_path) as file_obj:
            header = file_obj.readline()
            header = header.strip()
        column_list = header.split(",")
        column_list = [name.strip() for name in column_list if name.strip() != ""]
        if set(column_list) == set(BOFA):
            read_type = "bofa"
        elif set(column_list) == set(AMEX):
            read_type = "amex"
        elif set(column_list) == set(DISCOVER):
            read_type = "discover"
        logger.debug("Input type is - {}".format(read_type))
        csv_reader = csv.DictReader(open(file_path), delimiter=",")
        for row_dict in csv_reader:
            logger.debug(row_dict)
            tmp_expense = Expense.from_dict(row_dict, expense_type=read_type)
            master_data.append(tmp_expense)
    master_data.sort()
    op_fields = ["Date", "Amount", "Category", "Description", "Address", "Reference", "Type"]
    csv_writer1 = csv.DictWriter(open("all-expenses.csv", "w", newline=""), op_fields, quotechar='"')
    csv_writer2 = csv.DictWriter(open("all-payments.csv", "w", newline=""), op_fields, quotechar='"')
    csv_writer1.writeheader()
    csv_writer2.writeheader()
    for exp in master_data:
        logger.debug(exp.map)
        if exp.iscredit:
            csv_writer2.writerow(exp.map)
        else:
            csv_writer1.writerow(exp.map)
