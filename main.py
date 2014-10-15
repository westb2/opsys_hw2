'''class cpu():
	def __init__(self):

	def run(self):

k = cpu()
k.run()'''
import PROCESS
from Queue import PriorityQueue
#intializin ght eprocess
def initializeprocesses(num_processes):
	# set up the priority queue 
	process_queue = MyPriorityQueue()
	# creating the IO Processes and storing with priority  
	for item in range((num_processes*.8)):
		k = PROCESS.IOProcess()
		process_queue.put(k, k.getCPUBurst())
	# creating the CPU bound Processes and storing with priotiry
	for item in range(int ((num_processes - int((num_processes *.8)) ))):
		k = PROCESS.CPUProcess()
		process_queue.put(k, k.getCPUBurst())
	# returning the priority queue
	return process_queue

# Simulate the SJF algorithm without preemtion
def simulateSJF(Processes, CPUS):


#This is our function that will run our program, easy way to change numreical parameters
def main(num_processes, num_cpus):
	#do some initialization
	Processes=initializeprocesses(num_processes)
	IOprocesses=int(num_processes*.8)
	#need to declare the CPU structure here
	CPUS=initializeCPUS(num_cpus)

	#run simulations	
	simulateSJF(Processes, CPUS)
	simulateSJFpreemption(Processes, CPUS)
	simulateRR(Processes, CPUS)
	simulatePP(Processes, CPUS)

main(12,1)