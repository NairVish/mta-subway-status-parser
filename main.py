import requests
import re
from bs4 import BeautifulSoup
# need lxml

class SubwayStatusHandler:
    STATUS_URL = "http://web.mta.info/status/serviceStatus.txt"
    LINES = ["123", "456", "7", "ACE", "BDFM", "G", "JZ", "NQR", "S", "SIR"]

    def __init__(self):
        self.load_new_data()

    def load_new_data(self):
        r = requests.get(self.STATUS_URL)
        raw_data = self._received_data_processor(r.text)
        soup = BeautifulSoup(raw_data, 'lxml')
        subway_line_data = soup.find("service").find("subway").findAll("line")
        self.status_data = subway_line_data

    @staticmethod
    def _received_data_processor(inp_data):
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

        return out_data

subway_line_data = SubwayStatusHandler().status_data
for line in subway_line_data:
    line_name = line.find("name")
    line_status = line.find("status")
    print(str(line_name.text) + " - " + str(line_status.text))
    status_description = line.find("text")
    print(status_description.getText())
