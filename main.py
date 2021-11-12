import json
import logging

from bs4 import BeautifulSoup

from youtube_functions import *


def write_data(data, path_name):
    with open(path_name, 'w') as fp:
        json.dump(data, fp)


if __name__ == '__main__':
    # downloading and writing a file with monologues
    monos_ids = ['_18xpepmbcE&t=327s', 'hS2x1zl4rn0&t=129s', 'YavL_IVSGV4', 'Mi5g74O-E5M']
    logging.info('Downloading monologues...')
    monologues = get_monologues(monos_ids)
    write_data(monologues, 'data/monologues.json')
    logging.info('Monologues was successfully saved into file.')

    # downloading and writing a file with dialogs
    with_speakers = ['cw5gCoIbUbg', 'DN26vJyZakg']
    without_speakers = ['hzmbCSHcSts']

    logging.info('Downloading dialogues...')
    interviews_data = get_interviews([*with_speakers, *without_speakers])
    data = {}

    for video_id, interview in interviews_data.items():
        if video_id in with_speakers:
            data[video_id] = process_interviews_with_speaker_name(interview)
        else:
            data[video_id] = process_interviews(interview)
    write_data(data, 'data/dialogs.json')
    logging.info('Dialogues was successfully saved into file.')

    # processing documentary subtitles
    # TODO: add speakers
    with open('data/subtitles.smi') as f:
        data = f.readlines()
    data = [BeautifulSoup(x, 'html.parser') for x in data if '♪' not in x]

    subtitles = []
    for item in data:
        p = item.find('p')
        if p:
            if len(re.sub(r"[\n\t\s]*", "", p.text)):
                subtitles.append(p.text.strip())
    write_data(subtitles, 'data/documantary.json')
    logging.info('Documentary was successfully saved into file.')
