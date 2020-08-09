import os
import sys
import csv
import logging.config
import yaml
import argparse

log_config = yaml.load(open("logging.yml"), Loader=yaml.FullLoader)
logging.config.dictConfig(log_config)

from expense_lib.expense import Expense
from expense_lib.expense import EXPENSE_MAP_HEADER
from expense_lib.normalizer import get_expense_type
from expense_lib.normalizer import NormalizerBuilder
from expense_lib.normalizer import normalize
from expense_lib.utils import get_csv_header


parser = argparse.ArgumentParser(prog=sys.argv[0], add_help=True)
parser.add_argument("-m", "--mode", action="store", default="credit_card", type=str, help="Choose the mode")
args = parser.parse_args()

logger = logging.getLogger(__name__)
if args.mode == "checkin":
    src_path = os.path.abspath("./data/checkin")
    dst_path = os.path.abspath("./output-data/checkin/")
    builder = NormalizerBuilder("config/normalize_checkin.json")
elif args.mode == "credit_card":
    src_path = os.path.abspath("./data/credit_card")
    dst_path = os.path.abspath("./output-data/cc/")
    builder = NormalizerBuilder("config/normalize_credit_card.json")
else:
    print("Unknown mode - {0}".format(args.mode))
    sys.exit(98)

normalizer_map = builder.get_config()
if not os.path.exists(dst_path):
    os.makedirs(dst_path)
files = os.listdir(src_path)
master_data = []


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
