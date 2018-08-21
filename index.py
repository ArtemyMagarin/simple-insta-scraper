import requests
import json


def get_instaplace_url(q):
	url = "https://www.instagram.com/web/search/topsearch/?context=blended&include_reel=false&query=" + q
	r = requests.get(url)
	places = r.json()['places']
	place_id = 0

	for place in places:
		if 'place' in place and place['position']==0:
			place_id = place['place']['location']['pk']
			break

	return 'https://www.instagram.com/explore/locations/{pk}/'.format(pk=place_id)


def get_insta_photos_by_place(url):
	r = requests.get(url)
	data = r.text
	lfStr = '<script type="text/javascript">window._sharedData = '
	rfStr = '</script>'

	data = data[data.find(lfStr)+len(lfStr):]
	data = data[:data.find(rfStr)-1] 

	x = json.loads(data)

	posts = {
		'top': [],
		'media': []
	}

	for post in x['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_top_posts']['edges']:
		print('https://www.instagram.com/p/'+post['node']['shortcode'])


if __name__ == '__main__':
	print('Type some place (nevsky prospekt): ', end="")
	place = input()
	if not place:
		place = 'nevsky prospekt'

	get_insta_photos_by_place(get_instaplace_url(place))