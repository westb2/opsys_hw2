
import PROCESS
import CPUS
import IOwait

from Queue import PriorityQueue

import PROCESS
import CPUS
import IOwait
from Queue import PriorityQueue

def simulatePP(Processes, num_cpus, dead_condition):
	#get the cpus up and running
	cpus = CPUS.CPUS(num_cpus)
	waiting_on_IO=IOwait.IOwait()
	dead_processes=[]
	time=0
	#put the processes in the cpu
	while True:
		if Processes and not cpus.full():
			job=cpus.addJob(Processes.pop(0))
			if job!=None:
				Processes.append(job)
				Processes.sort()
				break
		else:
			break
	#now we start running the simulation
	while True:
		if (len(Processes)+len(dead_processes)+len(waiting_on_IO.jobs)+len(cpus.jobs))!=12:
			print "WE LOST A PROCESS"
			
			print "there are %d jobs in process and %d jobs in the CPU and %d processes waiting on IO and %d dead processes"%(len(Processes), len(cpus.jobs), len(waiting_on_IO.jobs), len(dead_processes))
			print "printing items in processes"
			for item in Processes:
				print item.ID()
			print "printing items in dead_processes"
			for item in dead_processes:
				print item.ID()
			print "printing items in waiting_on_IO"
			for item in waiting_on_IO.jobs:
				print item.ID()
			print "printing items in cpus"
			for item in cpus.jobs:
				print item.ID()
			
			break
		time+=1
		#age all the processes that just had to wait
		for i in range(0, len(Processes)):
			Processes[i].age(time)
		#make all the processes wait on IO then put all the ones that are finished waiting back into the Q
		ready_processes=waiting_on_IO.wait_one(time)
		for i in range(0,len(ready_processes)):
			ready_processes[i].setAge(0)
			ready_processes[i].setPriority(ready_processes[i].TruePriority)
			Processes.append(ready_processes[i])
			#deal with printing that we are entering the ready Queue
			if ready_processes[i].isIOBound():
				print "[time %dms] Interacive process ID"%time, ready_processes[i].ID(), "entered the ready queue (requires","%dms CPU time; priority %d)"%(ready_processes[i].burstTime(), ready_processes[i].priority())
			else:
				print "[time %dms] CPU-bound process ID"%time, ready_processes[i].ID(), "entered the ready queue (requires","%dms CPU time; priority %d)"%(ready_processes[i].burstTime(), ready_processes[i].priority())
			#deal with preemption
		
		Processes.sort()
		#now we do preemption
		potential_victim= -1
		for j in range(0, len(cpus.jobs)):
			if potential_victim==-1:
				potential_victim=j
			else:
				if cpus.jobs[j].priority()<cpus.jobs[potential_victim].priority():
					potential_victim=j
		#if we have found a process we need to preempt then we do some stuff
		
		if Processes  and potential_victim>=0 and Processes[0].priority() < cpus.jobs[potential_victim].priority():
			print "[time %dms] Context switch (swapping out process ID %d for process ID %d)"%(time, cpus.jobs[potential_victim].ID(), Processes[i].ID())
			if cpus.jobs[potential_victim].isIOBound():
				print "[time %dms] Interacive process ID"%time, cpus.jobs[potential_victim].ID(), "entered the ready queue (requires","%dms CPU time; priority %d)"%(cpus.jobs[potential_victim].burstTime(), cpus.jobs[potential_victim].priority())
			else:
				print "[time %dms] CPU-bound process ID"%time, cpus.jobs[potential_victim].ID(), "entered the ready queue (requires","%dms CPU time; priority %d)"%(cpus.jobs[potential_victim].burstTime(), cpus.jobs[potential_victim].priority())
			#handle some stuff that 
			Processes[0].context_switch()
			cpus.jobs[potential_victim].setAge(0);
			cpus.jobs[potential_victim].setPriority(cpus.jobs[potential_victim].TruePriority)
			Processes.append(cpus.jobs.pop(potential_victim))
			cpus.addJob(Processes.pop(0))
			Processes.sort()

		#run all the processes for one second, then any that are finished we will remove from the CPU and have
		#them wait on IO. While we do this for each process that came off the CPU we will put a new one on
		finished_processes=cpus.runCPUS()		
		for i in range(0, len(finished_processes)):

			#if the process is finshed kill it
			if finished_processes[i].finished():
				dead_processes.append(finished_processes[i])
				#notify that we have killed the process

				#we must find the average turn time and wait time before this is done
				print "[time %dms] CPU-bound process ID"%time, finished_processes[i].ID(), "terminated (avg turnaround time %dms, avg total wait time %d ms)"%(finished_processes[i].avgTurnaroundTime(), finished_processes[i].avgWaitTime())
			#otherwise have it go wait on IO
			else:
				if finished_processes[i].isIOBound():
					print "[time %dms] IO-bound process ID"%time, finished_processes[i].ID(), "CPU-burst done (turnaround time %dms, total wait time %dms)"%(finished_processes[i].turnaroundTime(time), finished_processes[i].waitTime(time))
				else:
					print "[time %dms] CPU-bound process ID"%time, finished_processes[i].ID(), "CPU-burst done (turnaround time %dms, total wait time %dms)"%(finished_processes[i].turnaroundTime(time), finished_processes[i].waitTime(time))
				waiting_on_IO.addJob(finished_processes[i])
				#put a new job on the CPU
		#now fill the CPU with jobs for the next cycle
		while True:
			if Processes:
				job=cpus.addJob(Processes.pop(0))
				if job!=None:
					Processes.append(job)
					Processes.sort()
					break
			else:
				break
		if len(dead_processes)>=dead_condition:
			#here we need to calculate the avg tt time, wait time, and avg cpu utilization
			#collcect all the  times
			turnaroundTimes=[]
			waitTimes=[]
			process_jobs=0
			all_processes=[]
			for process in Processes:
				process_jobs+=1
				turnaroundTimes.extend(process.turnaroundTimes)
				waitTimes.extend(process.waitTimes)
				all_processes.append((process.ID(),process))
			for process in cpus.jobs:
				turnaroundTimes.extend(process.turnaroundTimes)
				waitTimes.extend(process.waitTimes)
				all_processes.append((process.ID(),process))
			for process in waiting_on_IO.jobs:
				turnaroundTimes.extend(process.turnaroundTimes)
				waitTimes.extend(process.waitTimes)
				all_processes.append((process.ID(),process))
			for process in dead_processes:
				turnaroundTimes.extend(process.turnaroundTimes)
				waitTimes.extend(process.waitTimes)
				all_processes.append((process.ID(),process))
			#print "there are %d jobs in process and %d jobs in the CPU and %d processes waiting on IO and %d dead processes"%(process_jobs, len(cpus.jobs), len(waiting_on_IO.jobs), len(dead_processes))

			print "Turnaround time: min %d ms; avg %.3f ms; max %d ms"%(min(turnaroundTimes), sum(turnaroundTimes)/float(len(turnaroundTimes)), max(turnaroundTimes))
			print "Wait time: min %d ms; avg %.3f ms; max %d ms"%(min(waitTimes), sum(waitTimes)/float(len(waitTimes)), max(waitTimes))
			print "Average CPU Utilization: %.3f%%"%(100*(sum(turnaroundTimes)-sum(waitTimes))/(float(time)*num_cpus))	
			all_processes.sort()
			#print the average cpu utilization per process
			print "Average CPU utilization per process:"
			for tup in all_processes:
				process=tup[1]
				print "process ID %d: %.3f%%" %(process.ID(), (sum(process.turnaroundTimes)-sum(process.waitTimes))/(float(time)*num_cpus*.01))
			break

