from urllib.parse import urlparse, parse_qs

url_data = urlparse("http://www.youtube.com/watch?v=z_AbfPXTKms&NR=1")
query = parse_qs(url_data.query)
video = query["v"][0]
print(video)