import click
import requests
from instagram.client import InstagramAPI
import json
import shutil
import sys


@click.command()

# Options
@click.option('--client_id', default=None, help='your Instagram client ID')
@click.option('--tag', help="Tag to search for")
# @click.option('--count', help="How many to return")
# TODO set a global number of pictures to download and return after reaching that number
# TODO create a function that measures the overall speed and timing of the CLI

# @click.argument('password')

def instaPy(client_id, tag):
    # Set some initial values for our counters
    page = 0
    index = 0
    nextJSON = 1

    # Check to see if we are on the first page
    # todo check to see that iterations after the zeroeth run as they should
    if page == 0:
        url = "https://api.instagram.com/v1/tags/{0}/media/recent?client_id={1}".format(tag, client_id)
        response = requests.get(url, stream=True)
        JSONrespsonse = response.json()
        nextJSON = int(JSONrespsonse["pagination"]["min_tag_id"]) - 8000000000000
    # If the page doesn't equal = 0, change up the URL and paginate
    elif page != 0:
        url = "https://api.instagram.com/v1/tags/{0}/media/recent?client_id={1}?min_tag_id=".format(tag, client_id, nextJSON)
        response = requests.get(url, stream=True)
        JSONrespsonse = response.json()
        nextJSON = int(JSONrespsonse["pagination"]["min_tag_id"]) - 8000000000000

    # TODO: rm these before release
    print("Next MIN ID is", nextJSON)
    print(len(JSONrespsonse["data"]))

    for media_object in JSONrespsonse["data"]:
        # Set the link and ID so we can get the file and give it a decent name
        link = JSONrespsonse["data"][index]["images"]["standard_resolution"]["url"]
        id = JSONrespsonse["data"][index]["id"]

        # Utils for dev
        print("Link is:", link)
        print("ID is:", id)
        print("Index is currently",index)

        image = requests.get(link, stream=True)
        with open('{0}.jpg'.format(id), 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)
        if index <= len(JSONrespsonse["data"]):
            index += 1
        else:
            page +=1
    # Clear response after completion
    del response

# Run
if __name__ == '__main__':
    instaPy()



