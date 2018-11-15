import csv
import sys

year = sys.argv[1]
scores_string = "./nfllines/nfl" + str(year) + "lines.csv"
scores_file = open(scores_string, "r")
output_file = open("./2010_output.csv", "w")


class past_games:
	def __init__(self, last_score, team, counter):
		prev_scores = table[team][counter]
		if counter > 0:
			prev_scores = table[team][counter].arr
		self.arr = [prev_scores[1], prev_scores[2], last_score]
		self.counter = counter + 1


teams = ["Arizona Cardinals", 
"Atlanta Falcons",
"Baltimore Ravens",
"Buffalo Bills",
"Carolina Panthers", 
"Chicago Bears", 
"Cincinnati Bengals", 
"Cleveland Browns", 
"Dallas Cowboys", 
"Denver Broncos", 
"Detroit Lions", 
"Green Bay Packers", 
"Houston Texans", 
"Indianapolis Colts", 
"Jacksonville Jaguars", 
"Kansas City Chiefs", 
"San Diego Chargers", 
"St Louis Rams", 
"Miami Dolphins", 
"Minnesota Vikings", 
"New England Patriots", 
"New Orleans Saints", 
"New York Giants", 
"New York Jets", 
"Oakland Raiders", 
"Philadelphia Eagles", 
"Pittsburgh Steelers", 
"San Francisco 49ers", 
"Seattle Seahawks", 
"Tampa Bay Buccaneers", 
"Tennessee Titans", 
"Washington Redskins"]


for i in range(len(teams)):
	teams[i] = teams[i].lower()

counter_table = {} # maps teams to number of games they've played already
table = {} # maps teams to a list, where each entry is a vec3 containing their last 3 games
predictions_table_total = {} # maps teams to an array of predictions based on their previous games
 # maps team to an array of booleans indicating if prediction was correct or not
predictions_table = {} # 0 indicates wrong, 1 indicates push, 2 indicates correct
for team in teams:
	counter_table[team] = 0
	first_week = [0,0,0]
	table[team] = [0] * 17 # number of games
	table[team][0] = first_week 
	predictions_table[team] = [0] * 16
	predictions_table_total[team] = [0] * 16


scores_file.readline()

line_count = 0
for line in scores_file:
	data = line.split(",")
	visitor = data[1].lower()
	visitor_score = int(data[2])
	home = data[3].lower()
	home_score = int(data[4])
	vegas_total = float(data[6])
	true_total = float(visitor_score + home_score)
	visitor_game_number = counter_table[visitor]
	home_game_number = counter_table[home]
	# print('current row: {}', data)
	# print('visitor_game_number: {}', visitor_game_number)
	# print('table[visitor]: {}', table[visitor])
	table[visitor][visitor_game_number + 1] = past_games(visitor_score, visitor, visitor_game_number)
	table[home][home_game_number + 1] = past_games(home_score, home, home_game_number)
	visitor_past_games_average, home_past_games_average = 0, 0
	if visitor_game_number == 0:
		visitor_past_games_average = sum(table[visitor][visitor_game_number])/3.0
	else:
		visitor_past_games_average = sum(table[visitor][visitor_game_number].arr)/3.0

	if home_game_number == 0:
		home_past_games_average = sum(table[home][home_game_number])/3.0
	else:
		home_past_games_average = sum(table[home][home_game_number].arr)/3.0
			
	
	predicted_total = visitor_past_games_average + home_past_games_average
#	print('predicted_total: {}', predicted_total)

	predictions_table_total[visitor][visitor_game_number] = predicted_total
	predictions_table_total[home][home_game_number] = predicted_total

	game_result = 0
	if (predicted_total > vegas_total and true_total > vegas_total) or (predicted_total < vegas_total and true_total < vegas_total):
		game_result = 2
	elif true_total == vegas_total:
		game_result = 1
	predictions_table[visitor][visitor_game_number] = game_result
	predictions_table[home][home_game_number] = game_result


	counter_table[visitor] += 1
	counter_table[home] += 1	



print('in total, there were 256 games in the 2013 nfl season. the prediction accuracies were: ')
correct_count = 0
push_count = 0
incorrect_count = 0
for team in predictions_table.keys():
	results = predictions_table[team]
	for game_number in results:
		if game_number == 2:
			correct_count += 1
		elif game_number == 1:
			push_count += 1
		else:
			incorrect_count += 1

correct_count /= 2
push_count /= 2
incorrect_count /= 2

print('correct picks: ' + str(correct_count))
print('pushed picks: ' + str(push_count))
print('incorrect picks: ' + str(incorrect_count))

# print('predictions for dallas cowboys totals in 2013 were: ' + str(predictions_table_total['dallas cowboys']))


















