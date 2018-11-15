output_file = open("2003-2013games_by_year.csv", "w")

FIRST_YEAR = 2003
LAST_YEAR = 2013

scores_files_arr = [0] * 11 # arr containing each file object

def main():
	initialize_files()
	teams = initialize_teams()
	organize_games(teams)

# simple method that takes in a mm/dd/yy date and returns the approx date in days
def parse_date(date): 
	total = 0
	data = date.split("/")
	month, day, year = int(data[0]), int(data[1]), int(data[2])
	if month == 9:
		total += 240
	elif month == 10:
		total += 270
	elif month == 11:
		total += 301
	elif month == 12:
		total += 331
	elif month == 1:
		total += 362

	return total + day

def initialize_files():
	file_strings = [0] * 11
	for i in range(0, 11):
		file_strings[i] = "nfllines/nfl" + str(i + 2003) + "lines.csv"

	counter = 0
	for i in range(0, 11):
		scores_files_arr[counter] = open(file_strings[i], "r")
		counter += 1

	columns_string = "Week,Date,Visitor,Visitor Score,Home Team,Home Score,Line,Total Line\n"
	output_file.write(columns_string)

def initialize_teams():
	teams = [0] * 32
	counter = 0
	with open("teams.txt") as teams_file:
		for line in teams_file:
			teams[counter] = line.strip().lower()
			counter += 1
	return teams
	
def organize_games(teams):
	game_counter = 0 # counter that verifies that each file has exactly 256 games in it
	for i in range(0, 11):
		curr_file = scores_files_arr[i]
		curr_file.readline()
		curr_year = i + 2003
		first_game = curr_file.readline()
		game_counter += 1
		data = first_game.split(",")
		first_date_of_curr_week = parse_date(data[0])
		for line in curr_file:
			data = line.split(",")
			curr_date = parse_date(data[0])
			
			new_arr = [0] * (len(data) + 1)
			new_arr[0] = str(curr_year)
			for i in range(len(data)):
				new_arr[i + 1] = data[i]
			output_string = ",".join(new_arr)
			output_file.write(output_string)
			game_counter += 1
		if game_counter != 256:
			print('the current file does not have 256 games. exiting')
			exit()
		game_counter = 0
		curr_file.close()

	output_file.close()



main()











