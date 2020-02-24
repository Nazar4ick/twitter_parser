import googlemaps
import folium
import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
from flask import Flask, request, render_template

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


def get_locations(username):
    """
    returns locations of all friends
    :param username: str
    :return: list
    """
    data = get_js_dict(username)
    locations = []
    for i in range(len(data['users'])):
        locations.append((data['users'][i]['location'], data['users'][i]['name']))
    for loc in locations:
        if loc[0] == '':
            locations.remove(loc)
    return locations


def get_coordinates(locs):
    """
    gets coordinates from locations and creates a map
    :param locs: list
    :return: None
    """
    maps = googlemaps.Client(key='AIzaSyAd3skpeldG352OyzjvBwzj_7p0AzUFB-k')
    f_map = folium.Map()
    friend_map = folium.FeatureGroup(name='friends')
    for i in range(len(locs)):
        error = 0
        try:
            location = maps.geocode(locs[i][0])
        except googlemaps.exceptions.HTTPError:
            error = 1
        if error == 0:
            if location:
                coords = [location[0]['geometry']['location']['lat'],
                          location[0]['geometry']['location']['lng']]
                friend_map.add_child(folium.Marker(location=coords,
                                                   popup=str(locs[i][1]),
                                                   icon=folium.Icon()))
    f_map.add_child(friend_map)
    f_map.save('templates/friends.html')
    return None


def main(username):
    get_coordinates(get_locations(username))
    return None


app = Flask(__name__)


@app.route('/')
def template_renderer():
    return render_template('main_map.html')


@app.route('/map', methods=['GET', 'POST'])
def map_renderer():
    name = request.form['name']
    main(name)
    return render_template('friends.html')

if __name__ == "__main__":
    app.run(debug=True)