#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper scripts to create updated email & homepage
for ITB Meeting
"""

from __future__ import print_function, division, absolute_import
from six import iteritems
import yaml
import warnings

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import datetime
import holidays

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('meeting', 'templates'),
                  trim_blocks=True, lstrip_blocks=True)


def create_homepage(talks, speakers, alumnis, debug=False):
    """ Create the updated homepage from given talks and upcoming speakers.

    :param talks:
    :param speakers:
    :return:
    """
    tname = 'itbmeeting.html'
    template = env.get_template(tname)

    text = template.render(talks=talks, speakers=speakers, alumnis=alumnis)
    if debug:
        print('*' * 80)
        print(text)
        print('*' * 80)
    with open("results/{}".format(tname), "w") as f:
        f.write(text)


def create_mail(speakers, alumnis):
    """ Create updated mail.

    :param speakers:
    :return:
    """
    template = env.get_template('mail.txt')

    text = template.render(speakers=speakers, alumnis=alumnis)
    print('*' * 80)
    print(text)
    print('*' * 80)
    with open("results/mail.txt", "w") as f:
        f.write(text)


def read_yaml(name):
    """ Read yaml data.

        'speakers' : ordered list of upcoming speakers (next to last)
        'talks' : ordered list of past talks (last to first)
        'alumnis': list of alumnis

    :param path:
    :return:
    """
    if name not in ['speakers', 'talks', 'alumnis']:
        raise ValueError
    path = 'database/{}.yaml'.format(name)
    stram = open(path, "r")
    data = yaml.load(stram)
    return data[name]


def get_next_dayofweek(d, weekday=1, skip_holidays=True):
    """ Returns date of next tuesday after the given
    date, if the date is not a holiday.
        0 = Monday
        1 = Tuesday
        ...

    :param date:
    :return:
    """
    days_ahead = weekday - d.weekday()
    if days_ahead < 1:  # Target day already happened this week (or monday)
        days_ahead += 7
    # this is the next possible date

    next_d = d + datetime.timedelta(days_ahead)
    #next_d = next_d - datetime.timedelta(7)

    # skip all the German holidays
    if skip_holidays:
        itb_holidays = [datetime.date(2016, 12, 20),
                        datetime.date(2016, 12, 27),
                        datetime.date(2017,  1,  3),
                        datetime.date(2017,  1, 24),
                        datetime.date(2017, 7, 25),
                        datetime.date(2017, 8, 1),
                        datetime.date(2017, 8, 8),
                        datetime.date(2017, 8, 15),
                        datetime.date(2017, 8, 22),
                        datetime.date(2017, 8, 29),
                        datetime.date(2017, 9, 12),
                        datetime.date(2017, 10, 31),
                        ]
        de_holidays = holidays.Germany(years=[2016, 2017])
        while next_d in de_holidays or next_d in itb_holidays:
            next_d = next_d + datetime.timedelta(7)

    return next_d


def update_outreach():
    """ Update homepage and mail.

    :return:
    """
    talks = read_yaml('talks')
    speakers = read_yaml('speakers')
    alumnis = read_yaml('alumnis')

    people_dict = {}

    def set_webaddress(person):
        if person['web']:
            web = person['web']
            if not web.startswith('http'):
                person['web'] = "https://itb.biologie.hu-berlin.de/" + web
        return person

    date = datetime.date.today()
    tuesday = 1
    for k, speaker in enumerate(speakers):
        speaker = set_webaddress(speaker)

        # get expected date of the talk (k+1 Tuesdays from now)
        date = get_next_dayofweek(date, weekday=tuesday)

        speaker['pdate'] = date

        # add to people dict
        people_dict[speaker['name']] = speaker

    for alumni in alumnis:
        speaker = set_webaddress(speaker)
        people_dict[alumni['name']] = alumni

    for talk in talks:
        # add slide link
        if talk['slides']:
            slides = talk['slides']
            if slides.startswith("http"):
                url = '<a href="{}" target="_blank">{}</a>'.format(slides, slides)
            else:
                # link to uploaded media
                url = '<a href="/wiki/_media/itbmeeting/{}" class="media mediafile mf_pdf" title="itbmeeting:{}">{}</a>'.format(
                    slides, slides, slides
                )
            talk['slides'] = url

        # Add speaker info to talk
        name = talk['name']
        if name not in people_dict:
            warnings.warn("Person does not exist: '{}'".format(name))
        person = people_dict.get(name, None)
        if person:
            for key, value in iteritems(person):
                talk[key] = value

    create_homepage(talks=talks, speakers=speakers, alumnis=alumnis)
    create_mail(speakers=speakers, alumnis=alumnis)


##########################################################################################
if __name__ == "__main__":
    print('-' * 80)
    print('Updating ITBmeeting information')
    print('-' * 80)
    update_outreach()



