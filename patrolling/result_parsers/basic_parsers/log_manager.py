def get_log_content(log_path):
    """

    :param log_path:
    :return: return the content of a given log file
    """
    with open(log_path,'r') as log_file:
        content=log_file.readlines()

    return content

