class CPUS():
	def __init__(self, num_cpus):
		self.max_jobs=num_cpus
		self.jobs=[]

	#if one of the CPUS is empty we add the job to it and return None. otherwise we return the job 
	def addJob(self, job):
		if len(self.jobs)<self.max_jobs:
			self.jobs.append(job)
			return None
		else:
			return job

	#subtract 1 from the time remaining on each job. If any of the jobs have zero time left return 
	#them in a list of all the jobs that terminated
	def runCPUS(self):
		finished_jobs=[]
		for i in range(0, len(self.jobs)):
			if self.jobs[i].run():
				finished_jobs.append(self.jobs[i])
				self.jobs.pop(i)
		return finished_jobs

	#this gives us access to jobs outside of the cpu
	def jobs(self):
		return self.jobs
