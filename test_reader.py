from web_reader import read_webpage

url = "https://cricstats.in/player/virat-kohli/2026/stats"

content = read_webpage(url)

print(content)