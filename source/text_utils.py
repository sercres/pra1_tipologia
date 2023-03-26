import re

class TextUtils:
    def get_numbers_from_string(self, text):
        separated_elements = re.search('[0-9]+(,[0-9]+)+', text)
        numbers = re.search('\\d+(?:\\.\\d+)?%', text)
        return [numbers.group(0), separated_elements.group(0)]
