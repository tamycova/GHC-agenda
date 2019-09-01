from bs4 import BeautifulSoup
from collections import defaultdict
from json import dump


def get_title(event):
    return event.find_all('h3')[0].text.strip()


def get_description(description):
    return description.text.strip()


def parse_info_event(event):
    data = {'audience': '-', 'location': '-'}
    spans = event.find_all('span')
    info = []
    for i in range(len(spans)):
        if i % 2 == 0:
            info.append(spans[i].text)
    for l in info:
        if ":" not in l:
            continue
        x, y = l.split(": ")
        y.strip()
        if "Audience" in x:
            data["audience"] = y
        if "Start Date" in x:
            data["date"] = y
        if "Start Time" in x:
            data["start"] = y
        if "End Time" in x:
            data["end"] = y
        if "Location" in x:
            data["location"] = y
    return data


def parse_event(i, events, descriptions):
    info = parse_info_event(events[i])
    info['title'] = get_title(events[i])
    info['description'] = get_description(descriptions[i])
    return info


def get_events(path):
    soup = BeautifulSoup(open(path), "html.parser")
    events = soup.find_all(class_="reg-matrix-header-container")
    descriptions = soup.find_all(class_="session-description")
    return [parse_event(i, events, descriptions) for i in range(len(events))]


def generate_json_by_date(agenda_path, json_path):
    events = get_events(agenda_path)
    data = defaultdict(list)
    for e in events:
        data[e['date']].append(e)
    with open(json_path, "w") as f:
        dump(data, f)

AGENDA_PATH = "./agenda.html"
JSON_PATH = "./events.json"
generate_json_by_date(AGENDA_PATH, JSON_PATH)
