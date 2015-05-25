__author__ = 'khalidu'

# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.

import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {"simple": {},
              "atr": {"inc": "aliases+tags+ratings"},
              "aliases": {"inc": "aliases"},
              "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print("requesting", r.url)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)


def main():
    # results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    # pretty_print(results)

    # artist_id = results["artists"][1]["id"]
    # print("\nARTIST:")
    # pretty_print(results["artists"][1])

    # artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    # releases = artist_data["releases"]
    # print("\nONE RELEASE:")
    # pretty_print(releases[0], indent=2)
    # release_titles = [r["title"] for r in releases]

    # print("\nALL TITLES:")
    # for t in release_titles:
    #     print(t)

    # How many bands Named "First Aid Kit"?
    results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit");
    fak_count = 0
    for artist in results['artists']:
        if artist['sort-name'] == 'First Aid Kit':
            # print(artist['sort-name'])
            fak_count += 1
        else:
            break
    print("Bands Named 'First Aid Kit' : " + str(fak_count))

    # BEGIN_AREA name for Queen?
    results = query_by_name(ARTIST_URL, query_type['simple'], "Queen")
    print("BEGIN_AREA name for Queen? : " + results['artists'][0]['begin-area']['name'])

    # Spanish Alias for Beatles?
    results = query_by_name(ARTIST_URL, query_type['simple'], "Beatles")

    for alias in results['artists'][0]['aliases']:
        if alias['locale'] == 'es':
            b_alias = alias['name']
            break
    print("Spanish Alias for Beatles :" + b_alias)


    # Nirvana Disambiguation?
    results = query_by_name(ARTIST_URL, query_type['simple'], "Nirvana")
    print("Nirvana Disambiguation : " + results['artists'][0]['disambiguation'])

    # When was One Direction formed?
    results = query_by_name(ARTIST_URL, query_type['simple'], "One Direction")
    print("When was One Direction formed? : " + results['artists'][0]['life-span']['begin'])


if __name__ == '__main__':
    main()
