import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import suggestions

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# get address from alexa at some point
@ask.launch
def launch():
    welcome_msg = render_template('greeting')
    return question(welcome_msg)


@ask.intent('KeywordIntent')
def keyword():
    key_msg = render_template('keyword')
    return question(key_msg)

# @ask.intent('TldIntent',
#             convert={'tld': str})
# def tld(tld):
#     tld_msg = render_template('tld')
#     return question(tld_msg)
@ask.intent('YesIntent')
def suggest():
    return question(render_template('suggest1'))

@ask.intent('NoIntent')
def no():
    return statement(render_template('done'))

@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)
#

if __name__ == '__main__':
    app.run(debug=True)
