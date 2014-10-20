import PROCESS
import CPUS
import IOwait
from Queue import PriorityQueue

def simulateSJFpreemption(Processes, num_cpus, dead_condition):
	#get the cpus up and running
	cpus = CPUS.CPUS(num_cpus)
	waiting_on_IO=IOwait.IOwait()
	dead_processes=[]
	time=0
	#put the processes in the cpu
	while True:
		if not Processes.empty():
			job=cpus.addJob(Processes.get()[1])
			if job!=None:
				Processes.put((job.burstTime(), job))
				break
		else:
			break
	#now we start running the simulation
	while True:
		time+=1
		#make all the processes wait on IO then put all the ones that are finished waiting back into the Q
		ready_processes=waiting_on_IO.wait_one(time)
		for i in range(0,len(ready_processes)):
			Processes.put((ready_processes[i].burstTime(), ready_processes[i]))
			#deal with printing that we are entering the ready Queue
			if ready_processes[i].isIOBound():
				print "[time %dms] Interacive process ID"%time, ready_processes[i].ID(), "entered the ready queue (requires","%dms CPU time)"%ready_processes[i].burstTime()
			else:
				print "[time %dms] CPU-bound process ID"%time, ready_processes[i].ID(), "entered the ready queue (requires","%dms CPU time)"%ready_processes[i].burstTime()
			#deal with preemption
			potential_victim= -1
			for j in range(0, len(cpus.jobs)):
				if potential_victim==-1:
					potential_victim=j
				else:
					if cpus.jobs[i].burstTime()<cpu.jobs[potential_victim].burstTime():
						potential_victim=j
			#if we have found a process we need to preempt then we do some stuff
			if potential_victim>=0 and ready_processes[i].burstTime()< cpus.jobs[potential_victim].burstTime():
				print "[time %dms] Context switch (swapping out process ID %d for process ID %d)"%(time, cpus.jobs[potential_victim].ID(), ready_processes[i].ID())
				if cpus.jobs[potential_victim].isIOBound():
					print "[time %dms] Interacive process ID"%time, cpus.jobs[potential_victim].ID(), "entered the ready queue (requires","%dms CPU time)"%cpus.jobs[potential_victim].burstTime()
				else:
					print "[time %dms] CPU-bound process ID"%time, cpus.jobs[potential_victim].ID(), "entered the ready queue (requires","%dms CPU time)"%cpus.jobs[potential_victim].burstTime()
				#handle some stuff that 
				ready_processes[i].context_switch()
				Processes.put((cpus.jobs[potential_victim].burstTime(), cpus.jobs.pop(potential_victim)))


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
			if not Processes.empty():
				job=cpus.addJob(Processes.get()[1])
				if job!=None:
					Processes.put(( job.burstTime(),job))
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
			while True:
				if not Processes.empty():
					process_jobs+=1
					process=Processes.get()[1]
					turnaroundTimes.extend(process.turnaroundTimes)
					waitTimes.extend(process.waitTimes)
				else:
					break
			for process in cpus.jobs:
				turnaroundTimes.extend(process.turnaroundTimes)
				waitTimes.extend(process.waitTimes)
			for process in waiting_on_IO.jobs:
				turnaroundTimes.extend(process.turnaroundTimes)
				waitTimes.extend(process.waitTimes)
			for process in dead_processes:
				turnaroundTimes.extend(process.turnaroundTimes)
				waitTimes.extend(process.waitTimes)
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