import time
import pathlib
import requests
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

	# print availabe resolution
	avail_res = ""
	for key, val in stream_urls.items():
		# print(key)
		avail_res += key
		avail_res += " "

	url_status = requests.get(stream_urls['360']).status_code

	if url_status == 200:
		image_bench_resut = generate_image(*SUCCESS, f"url obtained, {round(total_time, 3)}s")
		image_resolution_result = generate_image(*SUCCESS, avail_res, w=390)
		image_url_status = generate_image(*SUCCESS, f"OK {url_status}", w=220)
	else:
		# failed to obtain stream url
		# or stream url not available
		image_bench_resut = generate_image(*FAILED, "result empty", w=340)
		image_resolution_result = generate_image(*FAILED, "not available", w=340)
		image_url_status = generate_image(*FAILED, "url error", w=260)

	image_bench_resut.save("bench_result.png")
	image_resolution_result.save("resolution_result.png")
	image_url_status.save("url_status.png")

except Exception as e:
	print(traceback.format_exc())

	image_bench_resut = generate_image(*FAILED, "scraper error", w=340)
	image_resolution_result = generate_image(*FAILED, "not available", w=340)
	image_url_status = generate_image(*FAILED, "url error", w=260)

	image_bench_resut.save("bench_result.png")
	image_resolution_result.save("resolution_result.png")
	image_url_status.save("url_status.png")