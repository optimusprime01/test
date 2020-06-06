import os
import csv
import logging.config
import yaml
from expense_lib.expense import Expense
from expense_lib.normalizer import get_expense_type
from expense_lib.normalizer import normalizer_map


log_config = yaml.load(open("logging.yml"), Loader=yaml.FullLoader)
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

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
    read_type = get_expense_type(column_list)
    if not read_type:
        logger.error("Input type not found for - {}".format(column_list))
        continue
    normalizer_func = normalizer_map.get(read_type)
    logger.debug("Input type is - {}".format(read_type))
    csv_reader = csv.DictReader(open(file_path), delimiter=",")
    for row_dict in csv_reader:
        logger.debug(row_dict)
        tmp_norm_dict = normalizer_func(row_dict)
        tmp_expense = Expense.from_dict(tmp_norm_dict)
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
