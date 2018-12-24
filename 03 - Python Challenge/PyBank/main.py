#!/usr/bin/env python
#!/anaconda2/envs/PythonData/bin/python

import os 
import csv
import operator

os.system("clear")

## Variables

# set by using a row_counter, equal to the number of records.
num_months = 0

# use for simple addition/subtraction of the P/L column
profit_loss = 0

# Hold the greatest increase and decrease
pl_increase = 0
pl_decrease = 0

## Working variables
p = 0
prev_p = 0
prev_m = ""
jump = 0
jumpl= []
change_list = []

# Dict for our calculations
# (This wasn't used)
pl = {}


## Functions


def calc(row_counter,month,p):
	global prev_m, prev_p, change_list
	#print(str(month), str(p), str(prev_m), str(prev_p))

	# p value is the current profit
	# prev_p is the previous month's profits
	# we need to see if the p value is greater or less than prev_p
	# we'll store the difference as jump, and feed that number into a list of changes (jump[])
	
	if p > prev_p:
		# we have an increase in change
		jump = (p - prev_p)	
	elif p < prev_p:
		# we have a decrease in change
		# add abs values and multiply by -1
		jump = (prev_p - p)*-1
	
	jumpl.append(jump)
	change_list.append((row_counter, prev_m, month, jump))
	#print(change_list)
	
	# shift our current values into 'previous' values for the next iteration
	prev_m = month
	prev_p = p
		

		
csvpath = "budget_data.csv"
with open(csvpath, newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',')
	next(csvreader)
	row_counter = 0
	prev_m = ""
	for row in csvreader: 

		# Handy simple output test
		#print(row)
	
		# month will be our dict key later
		month = str(row[0])

		# Net total amount of P/L over period.
		profit_loss = profit_loss + int(row[1])

		# Total Months
		row_counter+=1
	
		# p is the row[1], to operated on for calcuations		
		p = int(row[1])

		# add to dictionary of key/value pairs. Why? For the glory of Satan, I guess.
		# Maybe we'll need this later.
		# pl[month] = int(p)
		calc(row_counter,month,p)


#print(jump)


# Returns highest/lowest change, but doesn't get month. Sad.
#pl_inc_list = sorted(jumpl, reverse=True)
#pl_increase = pl_inc_list[0]
#pl_dec_list = sorted(jumpl)
#pl_decrease = pl_dec_list[0]




# We're probably supposed to save stuff as lists and zip them as tuples 
# and then do some list comprehensions to do more stuff.
# I plan to do that later, because I need to practice that. 
# For now, I'm using the operator.itemgetter to simplify my life.


from operator import itemgetter
	
#change_list.sort(key=operator.itemgetter(3))
#print(change_list)

pl_increase = [max(change_list, key=operator.itemgetter(3))[2], max(change_list, key=operator.itemgetter(3))[3]]
pl_decrease= [min(change_list, key=operator.itemgetter(3))[2], min(change_list, key=operator.itemgetter(3))[3]]



# I'd like some feedback on the Average Change, since my output didn't reflect the reference graphic in the readme.md
# I calculated the change from month to month and stored them into a list, and then averaged them 
# by dividing the sum of the integers by the length of the list (which should  be the number of elements in the array)
# But this returns 7803.476744186047, not -2315.12.

average_pl = sum(jumpl) / len(jumpl)

	
# Print data!
print("Financial Analysis")
print("------------------")
print("Total Months: " + str(row_counter))
print("Total: $" + str(profit_loss))
print("Average Change: " + "$" + str(average_pl))
print("Greatest Increase in Profits: " + str(pl_increase[0]) + " (" + str(pl_increase[1]) + ")" )
print("Greatest Decrease in Profits: " + str(pl_decrease[0]) + " (" + str(pl_decrease[1]) + ")" )


		
