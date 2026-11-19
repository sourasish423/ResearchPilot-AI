from web_tools import web_search

query = "Virat Kohli achievements"

print("Testing:", query)

results = web_search(query)

for result in results:
    print(result)