import requests
import re
from bs4 import BeautifulSoup
# need lxml

# retrieve service status XML
URL = "http://web.mta.info/status/serviceStatus.txt"
r = requests.get(URL)
data = r.text

# replace html escape characters in first pass-through
esc_reps = {"&amp;nbsp;": " ", "&lt;": "<", "&gt;": ">", "&nbsp;": " ", "&amp;": "&", "Â": ""}
esc_reps = dict((re.escape(k), v) for k, v in esc_reps.items())
esc_pattern = re.compile("|".join(esc_reps.keys()))
data = esc_pattern.sub(lambda m: esc_reps[re.escape(m.group(0))], data)

# replace line breaks in second pass-through
more_reps = {"<br>": "\n"}
more_reps = dict((re.escape(k), v) for k, v in more_reps.items())
more_patterns = re.compile("|".join(more_reps.keys()))
data = more_patterns.sub(lambda m: more_reps[re.escape(m.group(0))], data)

# have BeautifulSoup parse data using xml
soup = BeautifulSoup(data, 'lxml')
subway_line_data = soup.find("service").find("subway").findAll("line")
# print(str(subway_line_data))

for line in subway_line_data:
    line_name = line.find("name")
    line_status = line.find("status")
    print(str(line_name.text) + " - " + str(line_status.text))
    status_description = line.find("text")
    print(status_description.getText(separator=''))