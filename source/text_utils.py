import re
import locale
class TextUtils:
    def get_numbers_from_string(self, text):
        separated_elements = re.search('[0-9]+(,[0-9]+)+', text)
        numbers = re.search('\\d+(?:\\.\\d+)?%', text)
        if separated_elements is not None and numbers is not None:
            return [numbers.group(0), separated_elements.group(0)]
        else:
            return['','']

    '''
    Donada una llista de nombres i un patró regex, obtenim els elements coincidents
    '''
    def filter_number_from_array(self, array, pattern, first=False):
        p = re.compile(pattern)
        l = [s for s in array if p.match(s)]
        if len(l) > 0 and first:
            return l[0].strip()
        return l

    def remove_img_text(self, text):
        clean_text = []
        for t in text:
            clean_text.append(t.replace("platform_img ", ""))
        return(clean_text)


    def parse_to_number(self, number):
        return locale.atof(number)
