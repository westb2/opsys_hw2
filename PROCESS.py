#This is the class file for the process class. 
import random

#My process superclass
class Process(object):
	def __init__(self, ID_):
		self.IDEE=ID_
		self.burstMin=0
		self.burstMax=0
		self.IOmin=0
		self.IOmax=0
		self.IOBOUND=False
		self.BIRTHDAY=0
		self.LIFETIME=0
		self.CPUBurst = 0
		self.turnaroundTimes=[]
		self.waitTimes=[]
		self.RRtime=0
		self.PRIORITY=0
		self.TruePriority=0
		self.AGE=0
		self.CONTEXT_SWITCH=0
		self.CONTEXT_SWITCHS=[]

	#here we overload all of the comparision operators
	def __lt__(self, other):
		return self.PRIORITY<other.PRIORITY

	def __le__(self, other):
		return self.PRIORITY<=other.PRIORITY

	def __gt__(self, other):
		return self.PRIORITY>other.PRIORITY

	def __ge__(self, other):
		return self.PRIORITY>=other.PRIORITY

	#this we will use to tell whether a process is IOBound or not
	def isIOBound(self):
		return self.IOBOUND

	#here are a handful of functions that handle priority and aging
	def setPriority(self, p):
		self.PRIORITY=p

	def priority(self):
		return self.PRIORITY

	def setAge(self, number):
		self.AGE=number

	def age(self, time):
		self.AGE+=1
		if self.AGE>=1200:
			self.AGE=0
			if self.PRIORITY>0:
				self.PRIORITY-=1
				if self.isIOBound():
					print "[time %dms] Increased priority of IO-bound process ID %d to %d due to aging"%(time, self.IDEE, self.PRIORITY)
				else:
					print "[time %dms] Increased priority of CPU-bound process ID %d to %d due to aging"%(time, self.IDEE, self.PRIORITY)
	
	#this function gives us access to the ID of the process
	def ID(self):
		return self.IDEE

	#we call this when we enter the CPU to set the burst time and return the burst time
	def set_burst_time(self, birthday):
		self.BIRTHDAY=birthday
		self.CPUBurst=random.randint(self.burstMin, self.burstMax)
		self.LIFETIME=self.CPUBurst

	def wait_on_IO(self):
		if not self.IOBOUND:
			self.bursts-=1
		self.CPUBurst=random.randint(self.IOmin, self.IOmax)

	def burstTime(self):		
		#if we are CPU bound, subtract 1 from the remainder of bursts we need
		return self.CPUBurst

	#this process takes care of running the process on the cpu. It returns whether the process finished or not
	def run(self):
		self.CPUBurst-=1
		self.RRtime+=1
		return self.CPUBurst<=0

	def setRRtime(self, time):
		self.RRtime=0

	def getRRtime(self):
		return self.RRtime

	def RRrun(self, time_slice):
		self.CPUBurst-=1
		self.RRtime+=1
		return self.RRtime>=time_slice

	#this is our function to calculate and return the turnaround time
	def turnaroundTime(self, time):
		self.turnaroundTimes.append(time-self.BIRTHDAY)
		return time-self.BIRTHDAY

	#handles context switching
	def context_switch(self):
		self.CPUBurst+=2
		self.CONTEXT_SWITCH+=2

	#this is our function to return the wait time
	def waitTime(self,time):
		self.waitTimes.append(time-self.BIRTHDAY-self.LIFETIME)
		self.CONTEXT_SWITCHS.append(self.CONTEXT_SWITCH)
		self.CONTEXT_SWITCH=0
		return time-self.BIRTHDAY-self.LIFETIME

	#returns the avg turnaround time
	def avgTurnaroundTime(self):
		if self.isIOBound():
			print "OH NO AN IO PROCESS IS DYING"
		else:
			return sum(self.turnaroundTimes)/len(self.turnaroundTimes)

	#returns the avg wait time time
	def avgWaitTime(self):
		if self.isIOBound():
			print "OH NO AN IO PROCESS IS DYING"
		else:
			return sum(self.waitTimes)/len(self.waitTimes)

#My subclass for IO bound processes
class IOProcess(Process):
	def __init__(self, ID_):
		super(IOProcess, self).__init__(ID_)
		self.burstMin=20
		self.burstMax=200
		self.IOmin=1000
		self.IOmax=4500
		self.IOBOUND=True
		self.CPUBurst = random.randint(self.burstMin,self.burstMax);
		self.LIFETIME=self.CPUBurst
		
	def finished(self):
		return False

#My subclass for CPU bound processes
class CPUProcess(Process):
	def __init__(self, ID_):
		super(CPUProcess, self).__init__(ID_)
		self.burstMin=200
		self.burstMax=3000
		self.IOmin=1200
		self.IOmax=3200
		self.bursts = 8
		self.CPUBurst = random.randint(self.burstMin,self.burstMax)
		self.LIFETIME=self.CPUBurst

	def finished(self):
		return self.bursts<=0




	