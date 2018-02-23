import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import suggestions

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# get address from alexa at some point
count = 0



@ask.launch
def launch():
    welcome_msg = render_template('greeting')
    return question(welcome_msg)


@ask.intent('KeywordIntent',
            convert={'keyword' : str})
def keyword(keyword):
    session.attributes['keyword'] = keyword
    key_msg = render_template('keyword', keyword=session.attributes['keyword'] )
    return question(key_msg)

@ask.intent('TldIntent',
            convert={'tld': str})
def tld(tld):
    # session.attributes['tld'] = choice
    keyword = session.attributes['keyword']
    url = keyword + " dot " + tld
    tld_msg = render_template('tld', url=url)
    session.attributes['original'] = url
    session.attributes['tld'] = "." + tld
    return question(tld_msg)


@ask.intent('SuggestFirstIntent')
def first():
    alexa_init(session.attributes['keyword'], session.attributes['tld'])
    suggestion = alexa_suggestion(0)
    global count
    count++
    url = session.attributes['url']
    if False is in suggestion.values():
        suggestion_msg = render_template(suggest_first_notavail, url=url)
    else:
        suggestion_msg = render_template(suggest_first_avail, url=url)
    return question(suggestion_msg)

#
# @ask.intent('SuggestionIntent')
# def suggestion():
#     return 0
#
#
# @ask.intent('DoneIntent')
# def done():
#     return 0


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
