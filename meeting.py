#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper scripts to create updated email & homepage
for ITB Meeting
"""

from __future__ import print_function, division
import yaml
import warnings

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('meeting', 'templates'),
                  trim_blocks=True, lstrip_blocks=True)


def create_homepage(talks, speakers, debug=False):
    """ Create the updated homepage from given talks and upcoming speakers.

    :param talks:
    :param speakers:
    :return:
    """
    tname = 'itbmeeting.html'
    template = env.get_template(tname)

    text = template.render(talks=talks, speakers=speakers)
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

    for speaker in speakers:
        speaker = set_webaddress(speaker)
        people_dict[speaker['name']] = speaker

    for alumni in alumnis:
        speaker = set_webaddress(speaker)
        people_dict[alumni['name']] = alumni

    for talk in talks:
        # add slide link
        if talk['slides']:
            slides = talk['slides']
            url = '<a href="/wiki/_media/itbmeeting/{}" class="media mediafile mf_pdf" title="itbmeeting:{}">{}</a>'.format(
                slides, slides, slides
            )
            talk['slides'] = url

        # Add speaker info to talk
        name = talk['name']
        if name not in people_dict:
            warnings.warn("Person does not exist: '{}'".format(name))
        person = people_dict[name]
        for key, value in person.iteritems():
            talk[key] = value

    create_homepage(talks=talks, speakers=speakers)
    create_mail(speakers=speakers, alumnis=alumnis)


##########################################################################################
if __name__ == "__main__":
    update_outreach()



