import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
# get address from alexa at some point


@ask.launch
def launch():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent('KeywordIntent',
            default={'keyword': 'fishing'})
def keyword(keyword):
    key_msg = render_template('keyword')
    return question(key_msg)


@ask.intent('TldIntent',
            default={'choice': '.boats'})
def tld(choice):
    tld_msg = render_template('tld')
    return question(tld_msg)


@ask.intent('OriginalIntent')
def original():
    return 0


@ask.intent('SuggestionIntent')
def suggestion():
    return 0


@ask.intent('DoneIntent')
def done():
    return 0


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)
