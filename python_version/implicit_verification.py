import bigtree

## This contains the verification using implicit verification, meaning the activities are identified by in/outputs and resources
## are identified through data values, reads/writes, and endpoints

# Control Flow
## Existence: Checks if an activity a exists in a tree
def exists(a, tree):
    pass

## Absence: opposite of exists
def absence(a, tree):
    return not exists(a, tree)

## Leads To: Checks if an activity a exists and if it does if the activity it leads to exists prior
def leads_to(a, b, tree):
    if exists(a, tree):
        ## check if b is after a in any branch
        pass
    else:
        return True

## Precedence: Checks if an activity a exists, and if it does if the activity it requires as a precedence exists prior
def precedence(a, b, tree):
    if exists(a, tree):
        ## check if b is before a in any branch or in a parrallel branch with a
        pass
    else:
        return True
    pass

## Leads To Absence: if activity a exists, activity b does not exist after:
def leads_to_absence(a, b, tree):    
    if exists(a, tree):
        return absence(b, tree)
    else:
        return True
## Precdence Absence: if activity a exists, then activity b does not exist before
def precedence_absence(a, b, tree):
    if exists(b, tree):
        return not leads_to(a, b, tree)
    else:
        return True


# Resource
## Executed By: checks if an activity a exists, and if it does if it is executed by resource
def executed_by(a, resource):
    pass

# Data (which are also implicit resource)
## Send Exist: Checks if any activity in tree sends data data, returns boolean and said activity
def send_exist(data, tree):
    pass
## Receive Exist: Checks if any activity in tree receives data data, returns boolean and said activity
def receive_exist(data, tree):
    pass
## Activity sends: Checks if activity a sends data data
def activity_sends(a, data):
    if exists(a, tree):
        ## check if a sends the data
        pass
    else:
        return True
## Activity receives: Checks if activity a receives data data
def activitiy_receives(a, data):
    if exists(a, tree):
        ## check if a receives the data
        pass
    else:
        return True
    pass


# Time (directly implementable without reliance on sync activities)
## Min Time between: checks if activities a and b have a minimal time between them
def min_time_between(a, b, time):
    pass

# Time (that require sync activities)
## By Due Date: checks if an activity a has a sync activity with a value of timestamp time
## and a decision that reads the answer of sync after its execution
def by_due_date(a, time):
    pass



## Obligations vs Permissions: These can be modeled on the requirements side, using ands, ors and by just included the rule or not
## Complex resource requirements: These can also be modeled on the requirements side usind ands, ors and by just including rule or not
