#This is the class file for the process class. 
import random

#My process superclass
class Process(object):
	def __init__(self):
		self.burstMin=0
		self.burstMax=0
		self.IOBOUND=False
		self.burstTime=0

	#this we will use to tell whether a process is IOBound or not
	def isIOBound(self):
		return self.IOBOUND

	#we call this when we enter the CPU to set the burst time and return the burst time
	def burstTime(self):
		self.burstTime=random.randint(self.burstMin, self.burstMax)
		#if we are CPU bound, subtract 1 from the remainder of bursts we need
		if(!self.isIOBound()):
			bursts-=1
		return self.burstTime

	#this process takes care of running the process on the cpu. It returns how long it spent on the
	#cpu
	def runProcess(self, cpuTime):
		#if we have no burst time it means this process didnt get interupted last time
		if (self.burstTime==0):
			burstTime()
		#now we run the process until it is kicked out or kicks itself out
		if (self.burstTime > cpuTime):
			self.burstTime-=cpuTime
			return cpuTime
		else:
			tmp=self.burstTime
			self.burstTime=0
			return tmp



#My subclass for IO bound processes
class IOProcess(Process):
	def __init__(self):
		super(IOProcess, self).__init__()
		self.burstMin=20
		self.burstMax=200
		self.IOBOUND=True

#My subclass for CPU bound processes
class CPUProcess(Process):
	def __init__(self):
		super(CPUProcess, self).__init__()
		self.burstMin=200
		self.burstMax=3000
		self.bursts = 8




	