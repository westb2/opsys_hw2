'''class cpu():
	def __init__(self):

	def run(self):

k = cpu()
k.run()'''
import PROCESS
import CPUS
from Queue import PriorityQueue
#intializin ght eprocess
def initializeprocesses(num_processes):
	# set up the priority queue 
	process_queue = MyPriorityQueue()
	# creating the IO Processes and storing with priority  
	for item in range(0,(num_processes*.8)):
		k = PROCESS.IOProcess()
		process_queue.put(k, k.burstTime())
	# creating the CPU bound Processes and storing with priotiry
	for item in range(0,int((num_processes - int((num_processes *.8)) ))):
		k = PROCESS.CPUProcess()
		process_queue.put(k, k.burstTime())
	# returning the priority queue
	return process_queue

# Simulate the SJF algorithm without preemtion
def simulateSJF(Processes, num_cpus, dead_condition):
	#get the cpus up and running
	cpus = CPUS.CPUS(num_cpus)
	waiting_on_IO=IOwait.IOwait()
	dead_processes=[]
	#put the processes in the cpu
	while True:
		if !Processes.empty():
			job=cpus.addJob(Processes.get())
			if job!=None:
				Processes.put(job, job.burstTime())
				break
		else:
			break
	#now we start running the simulation
	while True:
		#make all the processes wait on IO then put all the ones that are finished waiting back into the Q
		ready_processes=waiting_on_IO.wait_one()
		for i in range(0,len(ready_processes)):
			Processes.put(ready_processes[i], ready_processes[i].burstTime())

		#run all the processes for one second, then any that are finished we will remove from the CPU and have
		#them wait on IO. While we do this for each process that came off the CPU we will put a new one on
		finished_processes=cpus.runCPUS()		
		for i in range(0, len(finished_processes)):
			#if the process is finshed kill it
			if finished_processes[i].finished():
				dead_processes.append(finished_processes[i])
			#otherwise have it go wait on IO
			else:
				waiting_on_IO.addJob(finished_processes[i])
				#put a new job on the CPU
			if !Processes.empty():
				cpus.addJob(Processes.get())
		if len(dead_processes)>=dead_condition:
			break
			



#This is our function that will run our program, easy way to change numreical parameters
def main(num_processes, num_cpus):
	#do some initialization
	Processes=initializeprocesses(num_processes)
	IOprocesses=int(num_processes*.8)
	#need to declare the CPU structure here

	#run simulations	
	simulateSJF(Processes, num_cpus, num_processes-IOprocesses)
	simulateSJFpreemption(Processes, num_cpus)
	simulateRR(Processes, num_cpus)
	simulatePP(Processes, num_cpus)

main(12,1)