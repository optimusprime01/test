import pytest
from unittest.mock import Mock
from expense_lib.normalizer import get_expense_type
from expense_lib.normalizer import NormalizerMapper
from expense_lib.normalizer import NormalizeConfig
from expense_lib.normalizer import NormalizerBuilder


def test_get_expense_type():
    norm1 = Mock()
    norm1.header = ["Date", "Description", "Card Member", "Account #", "Amount"]

    norm2 = Mock()
    norm2.header = ["Posted Date", "Reference Number", "Payee", "Address", "Amount"]

    nmap = {"amex": norm1, "bofa": norm2}

    assert get_expense_type(["Card Member", "Account #", "Date", "Description", "Amount"], nmap) == "amex"
    assert get_expense_type(["Posted Date", "Payee", "Address", "Amount", "Reference Number"], nmap) == "bofa"
    assert get_expense_type(["Posted Date", "Payee", "Reference Number"], nmap) is None


def test_normalize_mapper():
    config_dict1 = {
        "bofa": {
            "csv_header": ["Posted Date", "Reference Number", "Payee", "Address", "Amount"],
            "source": {
                "amount": "Amount",
                "date": "Posted Date",
                "description": "Payee",
                "address": "Address",
                "ref_num": "Reference Number",
            },
            "format": {"date": "%m/%d/%Y", "credit_amount": "positive"},
        },
        "amex": {
            "csv_header": [
                "Date",
                "Reference",
                "Description",
                "Card Member",
                "Card Number",
                "Amount",
                "Category",
                "Type",
            ],
            "source": {
                "amount": "Amount",
                "date": "Date",
                "description": "Description",
                "ref_num": "Reference",
                "category": "Category",
            },
            "format": {"date": "%m/%d/%y", "credit_amount": "negative"},
        },
    }

    mapper = NormalizerMapper(config_dict1)
    nmap = mapper.get_config()
    assert list(nmap.keys()) == ["bofa", "amex"]
    for config in nmap.values():
        assert isinstance(config, NormalizeConfig)

    bofa_config = nmap.get("bofa")
    assert bofa_config.header == ["Posted Date", "Reference Number", "Payee", "Address", "Amount"]
    assert bofa_config.source_map == config_dict1["bofa"]["source"]
    assert bofa_config.is_credit_positive is True
    assert bofa_config.date_format == "%m/%d/%Y"
    assert bofa_config.bank == "bofa"

    amex_config = nmap.get("amex")
    assert amex_config.is_credit_positive is False
    assert amex_config.bank == "amex"


def test_normalize_mapper_negative():
    config_dict1 = {"bofa": {"format": {}}}
    with pytest.raises(RuntimeError) as runtime_error:
        mapper = NormalizerMapper(config_dict1)
        mapper.get_config()
        assert "csv_header not defined for bofa" == runtime_error.value

    config_dict2 = {"bofa": {"csv_header": {"x": "y"}, "format": {}}}
    with pytest.raises(RuntimeError) as runtime_error:
        mapper = NormalizerMapper(config_dict2)
        mapper.get_config()
        assert 'csv_header must be a list in "bofa" config' == runtime_error.value

    config_dict3 = {"bofa": {"csv_header": ["ab", "cd"], "format": {}}}
    with pytest.raises(RuntimeError) as runtime_error:
        mapper = NormalizerMapper(config_dict3)
        mapper.get_config()
        assert "source not defined for bofa" == runtime_error.value

    config_dict4 = {"bofa": {"csv_header": ["ab", "cd"], "source": ["a", "b"], "format": {}}}
    with pytest.raises(RuntimeError) as runtime_error:
        mapper = NormalizerMapper(config_dict4)
        mapper.get_config()
        assert 'source must be a dict in "bofa" config' == runtime_error.value

    config_dict5 = {"bofa": {"csv_header": ["ab", "cd"], "source": {"date": "data"}, "format": {}}}
    with pytest.raises(RuntimeError) as runtime_error:
        mapper = NormalizerMapper(config_dict5)
        mapper.get_config()
        assert 'source must have mapping for amount in "bofa" config' == runtime_error.value

    config_dict6 = {"bofa": {"csv_header": ["ab", "cd"], "source": {"amount": "data"}, "format": {}}}
    with pytest.raises(RuntimeError) as runtime_error:
        mapper = NormalizerMapper(config_dict6)
        mapper.get_config()
        assert 'source must have mapping for date in "bofa" config' == runtime_error.value

    config_dict7 = {"bofa": {"csv_header": ["ab", "cd"], "source": {"amount": "1", "date": "2"}, "format": {}}}
    mapper = NormalizerMapper(config_dict7)
    nmap = mapper.get_config()
    assert nmap.get("bofa").bank == "bofa"
