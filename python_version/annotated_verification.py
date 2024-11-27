import bigtree
from util import exists_by_label, comapre_xpaths, executed_by_annotated


## This contains the verification using explicit, annotated verification, meaning the activities are identified by labels and resources
## are explicity annotated

# Control Flow
## Existence: Checks if an activity a exists in the xml tree and returns the xpath or None, this annotated version identifies by label
def exists(a, tree):#
    return exists_by_label(tree, a)
    
    

## Absence: opposite of exists
def absence(a, tree):
    return not exists(a, tree)

## Leads To: Checks if an activity a exists and if it does if the activity it leads to exists after
def leads_to(a, b, tree):
    apath = exists(a, tree)
    bpath = exists(b, tree)
    if apath:
        if bpath:
            compare = compare_xpaths(tree, apath, bpath)
            if compare == 0:
                return False
            elif compare == -1:
                return False
            elif compare == 1:
                return True
            elif compare == 2:
                return False
        else:
            return False 
    else:
        return True

## Precedence: Checks if an activity a exists, and if it does if the activity it requires as a precedence exists prior
def precedence(a, b, tree):
    apath = exists(a, tree)
    bpath = exists(b, tree)
    if apath:
        if bpath:
            compare = compare_xpaths(tree, apath, bpath)
            if compare == 0:
                return False
            elif compare == -1:
                return False
            elif compare == 1:
                return False 
            elif compare == 2:
                return True
        else:
            return False
    else:
        return True


## Leads To Absence: if activity a exists, activity b does not exist after:
def leads_to_absence(a, b, tree):
    apath = exists(a, tree)
    bpath = exists(b, tree)
    if apath:
        if not bpath:
            return True
        else:
            compare = compare_xpaths(tree, apath, bpath)
            if compare == 0:
                return True
            elif compare == -1:
                return False
            elif compare == 1:
                return False
            elif comapre == 2:
                return True
    else:
        return True
## Precdence Absence: if activity a exists, then activity b does not exist before
def precedence_absence(a, b, tree):
    apath = exists(a, tree)
    bpath = exists(b, tree)
    if apath:
        if not bpath:
            return True
        else:
            compare = compare_xpaths(tree, apath, bpath)
            if compare == 0:
                return True
            elif compare == -1:
                return False
            elif compare == 1:
                return True
            elif comapre == 2:
                return False 
    else:
        return True

# Resource
## Executed By data: checks if an activity a exists, and if it does if it is executed by resource, by interpreting data
def executed_by_data(a, resource, tree):
    pass

## Executed By Annotation: checks if an activity a exists, and if it does if it is executed by resource, by checking the annotation for Input Name: Resource
def executed_by_anno(a, resource, tree):
    apath = exists(a, tree)
    if apath:
        if executed_by_annotated(apath, tree) == resource:
            return True
        else:
            print(apath + " is currently not executed by " + resource)
            return False
    else:
        True

# Data (which are also implicit resource)
## Send Exist: Checks if any activity in tree sends data data, returns said activity or None
def send_exist(data, tree):
    pass
## Receive Exist: Checks if any activity in tree receives data data, returns said activity or None
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
## Min Time between: checks if activities a and b have a minimal time between them, very likely this is a bugged and maybe even a bit useless
def min_time_between(tree, a, b, time):
    if leads_to(a, b, tree):
        timeouts = timeouts_exists(tree)
        for path, t in timeouts:
            if leads_to(a, path, tree) and leads_to(path, b, tree):
                return t <= time
        return False
    else:
        return True
# Time (that require sync activities)
## By Due Date: explicit, 
## and a decision that reads the answer of sync after its execution
def by_due_date_explicit(tree, a, time):
    apath = exists(a, tree)
    if apath:
        for sync in sync_exists(tree):
            if directly_follows_must(tree, apath, sync[0]) or directly_follows_must(tree, sync[0], apath):
                if sync[1]:
                    if isinstance(sync[1], string):
                        print("uses a dataobject timestamp, can only be implicitly checked")
                        return True
                    else:
                        return time == sync[1] ## assumes the passed time is already parsed into a time object
                else: ## No timestamp or data object has been added to the sync yet
                    print("No timestamp or data.object is read in the sync activiy")
                    return False
        print("no sync activity was found in the tree to enforce the due date requirement")
        return False ## No matching sync object found
    else:
        return True
## By Due Data: implicit
def by_due_date_implicit(tree, a):
    apath = exists(a, tree)
    if apath:
        for sync in sync_exists(tree):
            if directly_follows_must(tree, apath, sync[0]) or directly_follows_must(tree, sync[0], apath):
                if sync[1]:
                    if isinstance(sync[1], string):
                        return True
                    else:
                        print("timestamp was found, could be explicitly checked")
                        return True
                else: # No timestamp or data object has been added to the sync yet
                    print("No timestamp or data.object is read in the sync activity")
                    return False
        print("no sync activity was found to enforce the due date requirement")
        return False
    else:
        return True
    pass

def max_time_between(tree, a, b, time):
    pass

## Obligations vs Permissions: These can be modeled on the requirements side, using ands, ors and by just included the rule or not
## Complex resource requirements: These can also be modeled on the requirements side usind ands, ors and by just including rule or not
