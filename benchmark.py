import os
import json
import time
import pathlib
import traceback

# import PyNime
from pynimeapi import PyNime

# image status generator
from image import generate_image

ANIME_TITLE = "Eiyuuou, Bu wo Kiwameru Tame Tenseisu: Soshite, Sekai Saikyou no Minarai Kishi"

ASSETS_PATH = pathlib.Path(".")/"assets"
ASSETS_PATH.mkdir(exist_ok=True)

# Status
FAILED = (ASSETS_PATH / "fail.png", (218, 69, 83))
SUCCESS = (ASSETS_PATH / "success.png", (50, 198, 113))

try:
	api = PyNime()
	search_result = api.search_anime(anime_title = ANIME_TITLE)
	episode_urls = api.get_episode_urls(anime_category_url = search_result[0].category_url)

	latest_episode = len(episode_urls)

	t0 = time.time()
	stream_urls = api.get_stream_urls(anime_episode_url = episode_urls[latest_episode-1])
	t1 = time.time()
	total_time = t1-t0
	# print(stream_urls)

	if stream_urls == None:
		# failed to obtain stream url
		image = generate_image(*FAILED, "result empty")
	else:
		image = generate_image(*SUCCESS, f"url obtained, {total_time}s")

	image.save("bench_result.png")

except Exception as e:
	# print(traceback.format_exc())
	image = generate_image(*FAILED, "scraper error")
	image.save("bench_result.png")