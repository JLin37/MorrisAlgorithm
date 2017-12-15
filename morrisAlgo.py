#!/usr/bin/python
"""
============================================================================
	Morris Approximate Counting of Events

	Give a periodic approximation of the number of events in an input stream.
	Each event is represented by the amount of time (in seconds) since the 
	previous event.
	Our output displays the time elapsed at each periodic output of 
	exact count and approximation count

	Authors: Menghao Lin (Jason), Xinliang Zhong, Ziqi Wang
	Date: 10 Dec 2017
	
============================================================================
"""
import random, math, sys, statistics

#declare global counters for morris
counters = [[]]
#execute morris function by incrementing count with probability 1/2^X
#Then return morris value = 2^X - 1
def morris(a):
	#mlist is list of morris value
    mlist = []
    for i in range(len(counters[a])):
        if 1.0/(2**counters[a][i]) > random.uniform(0,1) :
            counters[a][i] = counters[a][i]+1
    for x in counters[a]:
        mlist.append(2**x-1)
    return mlist

#morris+ function runs morris t times, s = (1/2*epsilon^2*delta)
#where delta = 1/3
#returns the mean value of morris runs as output
def morrisPlus(b):
    value = statistics.mean(morris(b))
    return value

#morris++ function runs morris+ t times, t = log(1/delta)
#returns the median value of morris+
def morrisPlusPlus():
	#pp store the list of morris+ values
    pp = [0]*len(counters)
    for i in range(len(counters)):
        pp[i] = morrisPlus(i)
    value = statistics.median(pp)
    return int(value)

def main():
	#getting argument input in commandline from user
	streamFile= sys.argv[1]
	#user defined epsilon value
	allowableError = float(sys.argv[2])
	#user defined delta value
	failureProbability = float(sys.argv[3])
	#check if howOften argument was declared by user
	if len(sys.argv) == 5:
		# get rid of [] from argument value
		howOften = float(sys.argv[4].strip("[]"))
	else:
		howOften = 1

	numEvents = 0
	currentTime = 0
	nextReportTime = howOften
	#times variable determines number times for morris+ to run
	times = int(1/(2*(allowableError*allowableError)*(1/3)))
	#ttimes variable determines number times for morris+ to run
	ttimes = int(math.log2(1/failureProbability))
	global counters
	#matrix to store morris values
	#each element is a morris value
	#number of columns represent morris+ runs
	#number of rows represent morris++ runs
	counters = [[0]*times for _ in range(ttimes)]

	print("elapsed time 	exact count 	Morris++ count")
    #read events files and stream each event line into program
	with open("%s"%streamFile, 'r') as fp:
		for line in fp:
			numEvents += 1
			currentTime += float(line)
			morrisValue = morrisPlusPlus()
			if currentTime >= nextReportTime:
				print(str(int(currentTime)) + "		" +
					str(numEvents) +  "		" +
					str(morrisValue))
				nextReportTime += howOften

if __name__ == "__main__":
    main()