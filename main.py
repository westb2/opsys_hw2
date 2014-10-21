'''class cpu():
	def __init__(self):

	def run(self):

k = cpu()
k.run()'''
import SJFalg
import SJFpreemptionalg
import RRalg
import PPalg

import Queue
import PROCESS
import CPUS
import IOwait
import random
from random import shuffle
from Queue import PriorityQueue
#intializing the processes
def initializeprocesses(num_processes):
	# set up the priority queue 
	process_queue = PriorityQueue()
	process_num=0
	# creating the IO Processes and storing with priority  
	for item in range(0,int(num_processes*.8)):
		process_num+=1
		k = PROCESS.IOProcess(process_num)
		print "[time 0ms] Interacive process ID", process_num, "entered the ready queue (requires", "%dms CPU time)"%k.burstTime()
		process_queue.put((k.burstTime(), k))

	# creating the CPU bound Processes and storing with priority
	for item in range(0,int((num_processes - int((num_processes *.8)) ))):
		process_num+=1
		k = PROCESS.CPUProcess(process_num)
		print "[time 0ms] CPU-bound process ID", process_num, "entered the ready queue (requires", "%dms CPU time)"%k.burstTime()
		process_queue.put((k.burstTime(), k))
	# returning the priority queue
	return process_queue

def initializeRRprocesses(num_processes):
	process_list=[]
	process_num=0
	# creating the IO bound processes 
	for item in range(0,int(num_processes*.8)):
		process_num+=1
		k = PROCESS.IOProcess(process_num)
		process_list.append(k)

	# creating the CPU bound Processes and storing with priority
	for item in range(0,int((num_processes - int((num_processes *.8)) ))):
		process_num+=1
		k = PROCESS.CPUProcess(process_num)
		process_list.append(k)
	shuffle(process_list)
	processQ=Queue.Queue()
	for item in process_list:
		processQ.put(item)
		if item.isIOBound():
			print "[time 0ms] Interacive process ID", item.ID(), "entered the ready queue (requires", "%dms CPU time)"%item.burstTime()
		else:
			print "[time 0ms] CPU-bound process ID", process_num, "entered the ready queue (requires", "%dms CPU time)"%item.burstTime()

	return processQ

def initializePPprocesses(num_processes):
	process_list=[]
	process_num=0
	#creating the IO bound processes
	for item in range(0,int(num_processes*.8)):
		process_num+=1
		k = PROCESS.IOProcess(process_num)
		r=random.randint(0,4)
		k.setPriority(r)
		k.TruePriority=r
		print "[time 0ms] Interacive process ID", process_num, "entered the ready queue (requires", "%dms CPU time; priority %d)"%(k.burstTime(), k.priority())
		process_list.append(k)

	# creating the CPU bound Processes and storing with priotiry
	for item in range(0,int((num_processes - int((num_processes *.8)) ))):
		process_num+=1
		k = PROCESS.CPUProcess(process_num)
		r=random.randint(0,4)
		k.setPriority(r)
		k.TruePriority=r
		print "[time 0ms] CPU-bound process ID", process_num, "entered the ready queue (requires", "%dms CPU time; priority %d)"%(k.burstTime(), k.priority())
		process_list.append(k)
	process_list.sort()
	return process_list

#This is our function that will run our program, easy way to change numerical parameters
def main(num_processes, num_cpus):
	#do some initialization
	Processes=initializeprocesses(num_processes)
	IOprocesses=int(num_processes*.8)

	#run simulations	
	SJFalg.simulateSJF(Processes, num_cpus, num_processes-IOprocesses)
	Processes=initializeprocesses(num_processes)
	SJFpreemptionalg.simulateSJFpreemption(Processes, num_cpus, num_processes-IOprocesses)

	Processes=initializeRRprocesses(num_processes)
	RR_timeslice=100
	RRalg.simulateRR(Processes, num_cpus, num_processes-IOprocesses, RR_timeslice)

	Processes=initializePPprocesses(num_processes)
	PPalg.simulatePP(Processes, num_cpus, num_processes-IOprocesses)
#running the entire file
# the 12 is total number of processes, the 1 is the total number of cpus
main(12,1)