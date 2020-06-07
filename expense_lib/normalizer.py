from datetime import datetime
from .constants import BOFA
from .constants import AMEX
from .constants import AMEX_YTD
from.constants import DISCOVER
from.constants import APPLE


def get_expense_type(header_list):
    if set(header_list) == set(BOFA):
        expense_type = "bofa"
    elif set(header_list) == set(AMEX):
        expense_type = "amex"
    elif set(header_list) == set(DISCOVER):
        expense_type = "discover"
    elif set(header_list) == set(AMEX_YTD):
        expense_type = "amex_ytd"
    elif set(header_list) == set(APPLE):
        expense_type = "apple"
    else:
        expense_type = None
    return expense_type


def bofa_normalizer(input_map):
    output_map = dict()
    tmp_amount = float(input_map.get("Amount", 0))
    output_map["amount"] = abs(tmp_amount)
    date_time_obj = datetime.strptime(input_map.get("Posted Date"), "%m/%d/%Y")
    output_map["date"] = date_time_obj
    output_map["is_credit"] = tmp_amount > 0
    output_map["description"] = input_map.get("Payee")
    output_map["address"] = input_map.get("Address")
    output_map["ref_num"] = input_map.get("Reference Number")
    output_map["category"] = None
    return output_map


def amex_normalizer(input_map):
    output_map = dict()
    tmp_amount = float(input_map.get("Amount", 0))
    output_map["amount"] = abs(tmp_amount)
    date_time_obj = datetime.strptime(input_map.get("Date"), "%m/%d/%y")
    output_map["date"] = date_time_obj
    output_map["is_credit"] = tmp_amount < 0
    output_map["description"] = input_map.get("Description")
    output_map["ref_num"] = input_map.get("Reference", "")
    output_map["category"] = input_map.get("Category", "")
    return output_map


def amex_ytd_normalizer(input_map):
    output_map = dict()
    tmp_amount = float(input_map.get("Amount #", 0))
    output_map["amount"] = abs(tmp_amount)
    date_time_obj = datetime.strptime(input_map.get("Date"), "%m/%d/%y")
    output_map["date"] = date_time_obj
    output_map["is_credit"] = tmp_amount < 0
    output_map["description"] = input_map.get("Description")
    output_map["ref_num"] = input_map.get("Reference", "")
    output_map["category"] = input_map.get("Category", "")
    return output_map

def discover_normalizer(input_map):
    output_map = dict()
    tmp_amount = float(input_map.get("Amount", 0))
    output_map["amount"] = abs(tmp_amount)
    date_time_obj = datetime.strptime(input_map.get("Post Date"), "%m/%d/%Y")
    output_map["date"] = date_time_obj
    output_map["is_credit"] = tmp_amount < 0
    output_map["description"] = input_map.get("Description")
    output_map["category"] = input_map.get("Category")
    return output_map


def apple_normalizer(input_map):
    output_map = dict()
    tmp_amount = float(input_map.get("Amount (USD)", 0))
    output_map["amount"] = abs(tmp_amount)
    date_time_obj = datetime.strptime(input_map.get("Clearing Date"), "%m/%d/%Y")
    output_map["date"] = date_time_obj
    output_map["is_credit"] = tmp_amount < 0
    output_map["description"] = input_map.get("Description")
    output_map["category"] = input_map.get("Category")
    return output_map


normalizer_map = {
    "amex_ytd": amex_normalizer,
    "amex": amex_normalizer,
    "discover": discover_normalizer,
    "bofa": bofa_normalizer,
    "apple": apple_normalizer,
}