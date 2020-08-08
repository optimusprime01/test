import os
import csv
import logging.config
import yaml

log_config = yaml.load(open("logging.yml"), Loader=yaml.FullLoader)
logging.config.dictConfig(log_config)

from expense_lib.expense import Expense
from expense_lib.expense import EXPENSE_MAP_HEADER
from expense_lib.normalizer import get_expense_type
from expense_lib.normalizer import NormalizerBuilder
from expense_lib.normalizer import normalize
from expense_lib.utils import get_csv_header


logger = logging.getLogger(__name__)
src_path = os.path.abspath("./data")
dst_path = os.path.abspath("./output-data")
if not os.path.exists(dst_path):
    os.makedirs(dst_path)
files = os.listdir(src_path)
master_data = []

builder = NormalizerBuilder("./config/normalize.json")
normalizer_map = builder.get_config()

for file in files:
    file_path = os.path.join(src_path, file)
    column_list = get_csv_header(file_path)
    read_type = get_expense_type(column_list, normalizer_map)
    if not read_type:
        logger.error("Input type not found for - {}".format(column_list))
        continue
    normalizer_config = normalizer_map.get(read_type)
    logger.debug("Input type is - {}".format(read_type))
    csv_reader = csv.DictReader(open(file_path), delimiter=",")
    for row_dict in csv_reader:
        logger.debug(row_dict)
        tmp_norm_dict = normalize(row_dict, normalizer_config)
        logger.debug(tmp_norm_dict)
        tmp_expense = Expense.from_dict(tmp_norm_dict)
        master_data.append(tmp_expense)
master_data.sort()

expense_file = open(os.path.join(dst_path, "all-expenses.csv"), "w", newline="")
payment_file = open(os.path.join(dst_path, "all-payments.csv"), "w", newline="")
csv_writer1 = csv.DictWriter(expense_file, EXPENSE_MAP_HEADER, quotechar='"')
csv_writer2 = csv.DictWriter(payment_file, EXPENSE_MAP_HEADER, quotechar='"')
csv_writer1.writeheader()
csv_writer2.writeheader()
for exp in master_data:
    logger.debug(exp.map)
    if exp.iscredit:
        csv_writer2.writerow(exp.map)
    else:
        csv_writer1.writerow(exp.map)
