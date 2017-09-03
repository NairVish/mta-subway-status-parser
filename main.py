import requests
import re
from bs4 import BeautifulSoup
# also need lxml


class SubwayStatusHandler:
    """
    Handles retrieval, parsing, and return of subway data.
    """
    STATUS_URL = "http://web.mta.info/status/serviceStatus.txt" # the URL we're getting the data from
    # LINES = ["123", "456", "7", "ACE", "BDFM", "G", "JZ", "NQR", "S", "SIR"]

    def __init__(self):
        """
        New data is automatically retrieved upon initialization of the object.
        """
        self.load_new_data()

    def load_new_data(self):
        """
        Gets the new data, processes it, and assigns it to a member variable called "status_data".
        We're only concerned with the Subway status portion of the data here.
        (However, the program can easily be extended to include buses, bridges & tunnels, LIRR, etc.)
        :return: Nothing.
        """
        r = requests.get(self.STATUS_URL)
        raw_data = self._received_data_processor(r.text)
        soup = BeautifulSoup(raw_data, 'lxml')
        self.status_data = soup.find("service").find("subway").findAll("line")

    @staticmethod
    def _received_data_processor(inp_data):
        """
        [Private] Replaces HTML character entities and other references with their appropriate characters.
        :param inp_data: The input data we must sweep.
        :return: The swept/cleaned up data.
        """
        # replace html escape characters in first pass-through
        esc_reps = {"&amp;nbsp;": " ", "&lt;": "<", "&gt;": ">", "&nbsp;": " ", "&amp;": "&", "Â": ""}
        esc_reps = dict((re.escape(k), v) for k, v in esc_reps.items()) # escape everything except except ASCII letters, numbers and '_'.
        esc_pattern = re.compile("|".join(esc_reps.keys()))  # create a regex object from keys
        out_data = esc_pattern.sub(lambda m: esc_reps[re.escape(m.group(0))], inp_data)  # for each match, find the string to replace it with in our dict

        # replace line breaks in second pass-through (same process as above)
        more_reps = {"<br>": "\n"}
        more_reps = dict((re.escape(k), v) for k, v in more_reps.items())
        more_patterns = re.compile("|".join(more_reps.keys()))
        out_data = more_patterns.sub(lambda m: more_reps[re.escape(m.group(0))], out_data)

        # strip out any leading whitespace from all of the lines
        out_data = '\n'.join([line.lstrip() for line in out_data.split('\n')])

        return out_data

    def get_lines_with_text(self):
        """
        Gets all of the status data and packages it for return.
        :return: Dict of the form: {"LINE_GROUP_NAME": (STATUS, STATUS_DESCRIPTION), ...}
        """
        r = {}
        for line in self.status_data:
            line_name = line.find("name").getText()
            line_status = line.find("status").getText()
            status_description = line.find("text").getText()
            r[line_name] = (line_status, status_description)
        return r

# Some code to output the result.
subway_line_data = SubwayStatusHandler().get_lines_with_text()
# print(subway_line_data)
for l, s in subway_line_data.items():
    print(l + " - " + s[0])
    print(s[1])

