#This is the class file for the process class. 
import random

#My process superclass
class Process(object):
	def __init__(self, ID_):
		self.ID=ID_
		self.burstMin=0
		self.burstMax=0
		self.IOmin=0
		self.IOmax=0
		self.IOBOUND=False
		
		self.CPUBurst = 0

	#this function gives us access to the ID of the process
	def ID(self):
		return self.ID

	#this we will use to tell whether a process is IOBound or not
	def isIOBound(self):
		return self.IOBOUND
	#we call this when we enter the CPU to set the burst time and return the burst time

	def set_burst_time(self):
		self.CPUBurst=random.randint(self.burstMin, self.burstMax)

	def wait_on_IO(self):
		if not self.IOBOUND:
			self.bursts-=1
		self.CPUBurst=random.randint(self.IOmin, self.IOmax)

	def burstTime(self):		
		#if we are CPU bound, subtract 1 from the remainder of bursts we need
		return self.CPUBurst

	#this process takes care of running the process on the cpu. It returns whehter the process finished or not
	def run(self):
		self.CPUBurst-=1
		return self.CPUBurst<=0


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
	def finished(self):
		return self.bursts<=0




	