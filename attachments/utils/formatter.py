class Formatter:
    """
    Classe de utilidade para formatação de dados.
    """
    def format_by_type(bytes_num):
        suffixes = ['B', 'KB', 'MB', 'GB']
        index = 0

        while bytes_num >= 1024 and index < len(suffixes) - 1:
            bytes_num /= 1024.0
            index += 1

        return "{:.3gf} {}".format(bytes_num, suffixes[index])