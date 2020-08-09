EXPENSE_MAP_HEADER = ["Date", "Amount", "Category", "Description", "Address", "Reference", "Type", "Bank"]


class Expense:
    def __init__(self):
        self.bank = None
        self.expense_date = None
        self.expense_amount = 0
        self.iscredit_bool = None
        self.expense_description = ""
        self.expense_address = ""
        self.reference_number = ""
        self.expense_category = ""

    @classmethod
    def from_dict(cls, input_map):
        expense = cls()
        expense.bank = input_map.get("bank", "")
        expense.expense_amount = input_map.get("amount", 0)
        expense.expense_date = input_map.get("date")
        expense.iscredit_bool = input_map.get("is_credit")
        expense.expense_description = input_map.get("description", "")
        expense.expense_address = input_map.get("address", "")
        expense.reference_number = input_map.get("ref_num", "")
        expense.expense_category = input_map.get("category", "")
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
            amount = self.amount
            type = "CREDIT"
        else:
            amount = self.amount * -1
            type = "DEBIT"
        output_map = {
            "Date": self.date.strip(),
            "Amount": amount,
            "Reference": self.reference_number.strip(),
            "Category": self.expense_category.strip(),
            "Address": self.expense_address.strip(),
            "Description": self.expense_description.strip(),
            "Type": type,
            "Bank": self.bank,
        }
        return output_map

    def __eq__(self, other):
        return self.expense_date == other.expense_date

    def __lt__(self, other):
        return self.expense_date < other.expense_date
