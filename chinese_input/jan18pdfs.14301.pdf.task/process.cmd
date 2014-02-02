# Tell us the version of R or Matlab you are using. Place it
# in the JobAd. Choose one. Or comment both if it is some other
# kind of program.

# By default, your R or Matlab will go whereever we can take it.
# If it runs long it should only run in our dedicated pool
# granting up to 24 hours per job. Short jobs will get far
# more resources if Open Science Grid(OSG) option below is used.
# Optimal time for OSG is about one hour.
+WantGlidein = True
# If it can run anywhere but OSG use the following one instead(seldom)
+WantFlocking = true
# Comment BOTH to run in our dedicated pool(Long Jobs Only).
+WantRHEL6 = true

+group = "WID"
+WIDsTheme = "Optimization"

# Arguments to the wrapper script.  Of note is the last one, --, anything
# after this goes direct to your R, Matlab or Other code.
# This gets augmented for you by mkdag.pl. Choose R or Matlab
arguments =  --type=Other --cmdtorun=sh do.sh --unique=jan18pdfs.14301.pdf.task -- 

# YOU SHOULD NOT NEED TO CHANGE ANYTHING BELOW THIS LINE

# This is a "normal" job.
universe = vanilla

# This wrapper script automates setting R or Matlab up.
executable = /scratch/czhang/journal_wrapper/ChtcRun/chtcjobwrapper

# If anything is output to standard output or standard error, 
# where should it be saved?
output = process.out
error = process.err

# Where to write a log of your jobs statuses.
log = process.log

# if you wanted your jobs to go on hold because they are
# running longer then expected uncomment this line and
# change from 24 hours to desired limit
#periodic_hold = (JobStatus == 2) && ((CurrentTime - EnteredCurrentStatus) > (60 * 60 * 24))

# remember where you have run
# release any job that had an issue and got set to hold after 30 seconds
# neither run where you failed to complete, nor on too busy a server.
# match_list_length = 5
periodic_release = (JobStatus == 5) && ((CurrentTime - EnteredCurrentStatus) > 30)
# requirements = (TARGET.Name =!= LastMatchName1) 
#
# Tell Condor how many cpus and how much memory and storage we need
# (Memory in MBs, we'll ask for 1GB)
# (Storage in 1k bytes, we'll ask for 1 GB)
#
request_cpus = 1
request_memory = 2000
request_disk = 2000000


# We need to bring our file with us.
# If job saves state and can restart
# use this one
# when_to_transfer_output = ON_EXIT_OR_EVICT
should_transfer_files = YES
when_to_transfer_output = ON_EXIT

# We don't want email about our jobs. (If you do, let us know,
# there may be some additional configuration necessary.)
notification = never

# This line is completed for you
transfer_input_files = /scratch/czhang/journal_wrapper/ChtcRun/jan29_chinese/jan18pdfs.14301.pdf.task/,/scratch/czhang/journal_wrapper/ChtcRun/jan29_chinese/shared/

# if you are a group of users, we'll map you outside of your jobs
# so leave this commented out. Otherwise, uncomment and insert the
# group account we assigned you.
#+AccountingGroup = "CHTC"


queue
