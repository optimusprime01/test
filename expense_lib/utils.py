import logging.config

logger = logging.getLogger(__name__)


def get_csv_header(file_path):
    logger.debug("Input file : {}".format(file_path))
    with open(file_path) as file_obj:
        header = file_obj.readline()
        header = header.strip()
    column_list = header.split(",")
    column_list = [name.strip() for name in column_list if name.strip() != ""]
    return column_list
