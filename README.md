# ITB Meeting
<img title="tellurium logo" src="./docs/images/logos/itb_logo.png" height="50" />

Organisation of the Institute of Theoretical Biology (ITB) meeting
at the Humboldt University Berlin

The meeting homepage is available at
https://itb.biologie.hu-berlin.de/wiki/itbmeeting/

## Workflow
* Until Sunday: Get title from speaker till Sunday 
* Monday: Update & send emails (invitation & reminder for next speaker)
* Tuesday after talk: 
    * Update `speakers.yaml` & `talks.yaml` 
    * Update homepage
    * Send slide email 
* If slides: update slides


## Installation
```
mkvirtualenv itbmeeting --python=python3.6
(itbmeeting) pip install -r requirements.txt
```

## Open Issues
* crawl emails & web pages from ITB page

## Misc
* screen shots in firefox via `screenshot` in developer tools
* convert series of png to one pdf `convert *.png talk.pdf`