import json, random

def neighbors(country):
	if country in data['continental']['new-world']:
		return data['continental']['new-world'][country]
	else:
		return data['continental']['old-world'][country]

def grab_marbles_from_bag(bag, num_marbles):
	for i in range(num_marbles):
		r = random.randint(i, len(bag) - 1)
		bag[i], bag[r] = bag[r], bag[i]
	return bag[0:num_marbles]

# bfs stands for "breadth-first search". Google this if unfamiliar.
def bfs(country):
	bfs_queue = [country]
	# { country_name: (distance_from_start, path_predecessor) }
	visited = {country: (0,'')} 
	while bfs_queue != []:
		v = bfs_queue.pop(0)
		for neighbor in neighbors(v):
			if neighbor not in visited:
				visited[neighbor] = (visited[v][0] + 1, v)
				# Everything borders China and Russia, skewing quiz difficulty.
				keep_china_russia = ['Finland', 'Sweden', 'Norway', \
									 'Mongolia', 'North Korea', 'South Korea']
				if neighbor in ['China', 'Russia'] and country not in keep_china_russia:
					pass
				else:
					bfs_queue.append(neighbor)
	return visited

def path(start_country, end_country):
	path = [end_country]
	a = bfs(start_country)
	predecessor = a[end_country][1]
	while predecessor != '':
		path.insert(0, predecessor)
		predecessor = a[predecessor][1]
	return ', '.join(path)

def countries_x_countries_away(start_country, x):
	a = bfs(start_country)
	return list(filter(lambda c: a[c][0] == x, a))

def countries_x_or_more_countries_away(start_country, x):
	a = bfs(start_country)
	return list(filter(lambda c: a[c][0] >= x, a))

def question(country, difficulty):
	s = "\nWhich of these countries does not border {0}?\n\n".format(country)
	neighboring = neighbors(country)
	if difficulty == 'easy':
		not_neighbor = grab_marbles_from_bag(countries_x_or_more_countries_away(country, 4), 1)
	if difficulty == 'hard':
		not_neighbor = grab_marbles_from_bag(countries_x_countries_away(country, 2), 1)
	if (len(neighboring) > 3):
		neighboring = grab_marbles_from_bag(neighboring, 3)
	choices = neighboring + not_neighbor
	letter = 'A'
	for choice in choices:
		s += "\t{0}. {1}\n".format(letter, choice)
		letter = chr(ord(letter) + 1)
	print(s)

def random_country():
	countries = list(data['continental']['old-world']) + list(data['continental']['new-world'])
	return grab_marbles_from_bag(countries, 1)[0]

if __name__ == '__main__':
	with open('borders.json') as data_file:
		data = json.load(data_file)