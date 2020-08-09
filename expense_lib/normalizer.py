import os
import json
from datetime import datetime


class NormalizeConfig:
    def __init__(self, bank_type, csv_header, source, data_format):
        self.bank_type = bank_type
        self.csv_header = csv_header
        self.source = source
        self.data_format = data_format

    @property
    def bank(self):
        return self.bank_type

    @property
    def header(self):
        return self.csv_header

    @property
    def date_format(self):
        return self.data_format.get("date", "%m/%d/%Y")

    @property
    def source_map(self):
        return self.source

    @property
    def is_credit_positive(self):
        return self.data_format.get("credit_amount", "negative") == "positive"


class NormalizerMapper:
    def __init__(self, config_dict):
        self.config = config_dict

    def get_config(self):
        normalizer_map = dict()
        for bank_type, bank_def in self.config.items():
            csv_header = bank_def.get("csv_header")
            source_map = bank_def.get("source")
            data_format = bank_def.get("format", {})
            if not csv_header:
                raise RuntimeError("csv_header not defined for {0}".format(bank_type))
            elif type(csv_header) is not list:
                raise RuntimeError('csv_header must be a list in "{0}" config'.format(bank_type))
            if not source_map:
                raise RuntimeError("source not defined for {0}".format(bank_type))
            elif type(source_map) is not dict:
                raise RuntimeError('source must be a dict in "{0}" config'.format(bank_type))
            if not source_map.get("amount"):
                raise RuntimeError('source must have mapping for amount in "{0}" config'.format(bank_type))
            if not source_map.get("date"):
                raise RuntimeError('source must have mapping for date in "{0}" config'.format(bank_type))
            normalizer_map[bank_type] = NormalizeConfig(bank_type, csv_header, source_map, data_format)
        return normalizer_map


class NormalizerBuilder:
    def __init__(self, json_file):
        self.file = json_file
        if not os.path.exists(self.file):
            raise RuntimeError("{0} doesn't exist".format(json_file))

    def get_config(self):
        json_confg = json.load(open(self.file))
        n_mapper = NormalizerMapper(json_confg)
        return n_mapper.get_config()


def get_expense_type(header_list, normalizer_map):
    expense_type = None
    for bank_type, normalize_config in normalizer_map.items():
        if set(header_list) == set(normalize_config.header):
            expense_type = bank_type
            break
    return expense_type


def normalize(input_map, normalize_config):
    output_map = dict()
    source_map = normalize_config.source_map
    tmp_amount = input_map.get(source_map.get("amount"), 0)
    try:
        tmp_amount = float(tmp_amount)
    except ValueError:
        tmp_amount = 0.0
    output_map["bank"] = normalize_config.bank
    output_map["amount"] = abs(tmp_amount)
    date_time_obj = datetime.strptime(input_map.get(source_map.get("date")), normalize_config.date_format)
    output_map["date"] = date_time_obj
    output_map["is_credit"] = tmp_amount > 0 if normalize_config.is_credit_positive else tmp_amount < 0
    if source_map.get("description"):
        output_map["description"] = input_map.get(source_map.get("description"))
    else:
        output_map["description"] = ""
    if source_map.get("address"):
        output_map["address"] = input_map.get(source_map.get("address"))
    if source_map.get("ref_num"):
        output_map["ref_num"] = input_map.get(source_map.get("ref_num"))
    if source_map.get("category"):
        output_map["category"] = input_map.get(source_map.get("category"))
    return output_map
