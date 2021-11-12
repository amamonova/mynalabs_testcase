# Mynalabs Testcase
This repo created for a Data Engineer test task. The task was to prepare 
a dataset of minimum 2000 text sentences attributed to Billie Eilish. 

## Description
The repo includes parsing data only from YouTube videos. 

## Usage
First of all, clone the repo and jump into a folder.
```bash
pip install -r requirements.txt
```
After requirements installation run the script:
```bash
python main.py
```

## Result
As a result, three files will be created: dialogues.json, 
monologues.json and documentary.json. The first file contains 
interviews with speaker label in it. monologue.json is transcript of
Billie Eilish' monologues. Place for improvement here: parse questions 
from a video. The last file is subtitles from documentary about 
the celebrity. Future work is developing approach to label speakers 
inside subtitles.

## Ideas
More data can be parsed from:
- Social media (Facebook, Twitter, Instagram)
- Interviews from magazines
- [Book](https://www.billieeilish.com/book)

## Note
What must be done (but I haven't coded it, because of lack of time):
- Text preprocessing (I think that, it depends on future usage, but 
  removing punctuation, converting to lower case, removing stop words 
  can be done)
  
- Filter final dicts in dialogues without speakers

