"""
The file with function for scrapping and processing transcripts from youtube videos.
"""

import re

from youtube_transcript_api import YouTubeTranscriptApi


def get_monologues(video_ids: []) -> {}:
    """
    Create dict with video_id as a key and downloaded transcription as a value
    :param video_ids: list with youtube video ids
    :return: dict like {'video_id': [transcript]}
    """
    data = {}
    for video_id in video_ids:
        data[video_id] = (YouTubeTranscriptApi.get_transcript(video_id))
    return data


def get_interviews(video_ids: []) -> {}:
    """
    Create dict with video_id as a key and downloaded transcription as a value
    :param video_ids: list with youtube video ids
    :return: dict like {'video_id': [transcript]}
    """
    interviews_data = {}
    for video_id in video_ids:
        # TODO: automatically detect which transcript was added manually
        try:
            interviews_data[video_id] = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US'])
        except:
            interviews_data[video_id] = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return interviews_data


def extract_speaker(text: str) -> str:
    """
    Often, youtube transcript contains a speaker inside braces. This function extract text between '[' and ']' signs.
    :param text: phrase from youtube video
    :return: speaker name if exists, otherwise empty string
    """
    text_inside = re.search(r'\[(.*?)\]', text)
    if text_inside:
        return text_inside.group(1)
    else:
        return ''


def process_interviews_with_speaker_name(interview: []) -> []:
    """
    This function adds speaker name to each phrase. The logic is follow:
    when we have marker like '-' or '>>', it means that the speaker was changed.
    A lot of transcripts include interviewer name inside. Hence the next speaker is celebrity.

    POSSIBLE ISSUES: this approach is suitable only for dialogues. If there is, for example,
    third person, the function will not work.

    :param interview: list with phrase dicts
    :return: list with phrase dicts, that include speaker name
    """
    final_data = []
    last = ''
    interview = sorted(interview, key=lambda d: d['start'])
    for phrase_dict in interview:
        text = phrase_dict['text']
        text = text.replace('Jimmy:', '[interviewer]')
        # TODO: create list of all possible markers
        text = text.replace('>>', '-')
        text_in_braces = extract_speaker(text)

        # TODO: improve check if a string includes only braces without dialog phrases
        if len(text) == len(text_in_braces) + 2:
            continue

        if text_in_braces.lower() == 'interviewer':
            last = 'interviewer'
            phrase_dict['speaker'] = 'interviewer'
        elif text[0] != '-' and last == 'interviewer':
            phrase_dict['speaker'] = 'interviewer'
        elif text[0] != '-' and last == 'celeb':
            phrase_dict['speaker'] = 'celeb'
        elif text[0] == '-' and last == 'interviewer' and not text_in_braces:
            last = 'celeb'
            phrase_dict['speaker'] = 'celeb'
        elif not text_in_braces and last == 'celeb':
            phrase_dict['speaker'] = 'celeb'

        final_data.append(phrase_dict)
    return final_data


def process_interviews(interview: []) -> []:
    """
    Function for processing interviews without speaker name inside
    :param interview: list with phrase dicts
    :return: list with phrase dicts, that include speaker name
    """
    last = 'celeb'
    final_data = []
    for phrase_dict in interview:
        text = phrase_dict['text']
        if text[0] == '-':
            if last == 'celeb':
                phrase_dict['speaker'] = 'interviewer'
                last = 'interviewer'
            else:
                phrase_dict['speaker'] = 'celeb'
                last = 'celeb'
        else:
            if last == 'celeb':
                phrase_dict['speaker'] = 'celeb'
            else:
                phrase_dict['speaker'] = 'interviewer'
        final_data.append(phrase_dict)
    return final_data
