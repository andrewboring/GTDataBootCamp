#!/usr/bin/env python
#/anaconda2/envs/PythonData/bin/python

import os
import csv

os.system("clear")

rcounter = 0

candidates = []
votes = []
percent = []	

def tally(candidate):
	if candidate not in candidates:
		candidates.append(candidate)
		votes.append(candidates.index(candidate))
	else:
		votes[candidates.index(candidate)] +=1

	#for c in candidates:
	#	print(str(candidate) + str(candidates.index(c)) + ":" + str(votes[(candidates.index(c))]))
			
sourcepath = "election_data.csv"
with open(sourcepath, newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',')
	next(csvreader)
		
	for r in csvreader:
		# Simple counter for total votes
		rcounter+=1
		
		cand = r[2]

		tally(cand)
			


print("Election Results")
print("-------------------------------------")
print("Total Votes:" + " " + str(rcounter))
print("-------------------------------------")
#print[candidates]
for c in candidates:
	#print(str(c) + ":" + " " + str(votes[(candidates.index(c))] / rcounter * 100) + "%" + " " + "(" + str(votes[(candidates.index(c))]) + ")")
	print(str(c) + ":" + " " + str(round(votes[(candidates.index(c))] / rcounter * 100, 3)) + "%" + " " + "(" + str(votes[(candidates.index(c))]) + ")")
print("-------------------------------------")
print("Winner: " + str(candidates[votes.index(max(votes))]))

# SAVE TO FILE
# It would be more efficient to save the percentage calcuations as another list,
# and and then print the lists to file or screen, rather than calculting it each time.
# But this homework is already late, so I call this a Minimum Viable Product
# and will add "improve the efficiency" as a backlog item for the next sprint planning meeting :-)

outfile = "election_results.txt"
output = open(outfile, 'w')
output.write("Election Results\n")
output.write("-------------------------------------\n")
output.write("Total Votes:" + " " + str(rcounter) + "\n")
output.write("-------------------------------------\n")
for c in candidates:
	#print(str(c) + ":" + " " + str(votes[(candidates.index(c))] / rcounter * 100) + "%" + " " + "(" + str(votes[(candidates.index(c))]) + ")")
	output.write(str(c) + ":" + " " + str(round(votes[(candidates.index(c))] / rcounter * 100, 3)) + "%" + " " + "(" + str(votes[(candidates.index(c))]) + ")" + "\n")
output.write("Winner: " + str(candidates[votes.index(max(votes))]) + "\n")
output.close()

print("Results have been saved as " + str(outfile) + ".")





