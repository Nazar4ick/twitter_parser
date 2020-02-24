import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_js_dict(user_name):
    """
    gets a dictionary with data from a user's account
    :param user_name: str
    :return: dict
    """
    while True:
        print('')
        acct = user_name
        if len(acct) < 1:
            break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '50'})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()
        js = json.loads(data)
        return js


def get_options(data):
    """
    suggests options where to chose data from
    :param data: dict
    :return: list
    """
    friends_len = len(data['users'])
    question = 'Yes'
    while question == 'Yes':
        number = input(f'Choose a friend number in range 1 and {friends_len}: ')
        friend = data['users'][int(number)-1]
        options = list(friend.keys())
        print(options)
        cont = 'Yes'
        while cont == 'Yes':
            option = input('Choose what would you like to see about this user from the list above: ')
            try:
                output = friend[option]
                print(output)
                print()
            except KeyError:
                print('Sorry, your input was incorrect')
                break
            cont = input('Would you like to know something more about him? (Yes or No) ')
        question = input('Would you like to know info about another friend? (Yes or No) ')
    out_str = 'If you want something more, launch the program again'
    return out_str


if __name__ == "__main__":
    username = input('Enter a twitter account: ')
    print(get_options(get_js_dict(username)))
