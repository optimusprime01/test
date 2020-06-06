from datetime import datetime

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
            date_time_obj = datetime.strptime(input_map.get("Posted Date"), "%m/%d/%Y")
            expense.expense_date = date_time_obj
            expense.iscredit_bool = tmp_amount > 0
            expense.expense_description = input_map.get("Payee")
            expense.expense_address = input_map.get("Address")
            expense.reference_number = input_map.get("Reference Number")
        elif expense_type == "amex":
            tmp_amount = float(input_map.get("Amount", 0))
            expense.expense_amount = abs(tmp_amount)
            date_time_obj = datetime.strptime(input_map.get("Date"), "%m/%d/%y")
            expense.expense_date = date_time_obj
            expense.iscredit_bool = tmp_amount < 0
            expense.expense_description = input_map.get("Description")
            expense.reference_number = input_map.get("Reference")
            expense.expense_category = input_map.get("Category")
        elif expense_type == "discover":
            tmp_amount = float(input_map.get("Amount", 0))
            expense.expense_amount = abs(tmp_amount)
            date_time_obj = datetime.strptime(input_map.get("Post Date"), "%m/%d/%Y")
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