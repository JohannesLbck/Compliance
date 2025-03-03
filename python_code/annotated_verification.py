import logging
import re
import xml.etree.ElementTree as ET
from util import * 
## Check util which is an interface to all other methods if you want all method names

## This contains the verification using explicit, annotated verification, meaning the activities are identified by labels and resources
## are explicity annotated

namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
data_decision_tags= [ ".//ns0:loop", ".//ns0:alternative"]
logger = logging.getLogger(__name__)

# Control Flow
## Existence: Checks if an activity a exists in the xml tree and returns the element or None, identifes by label, to identify using resource/data see below
def exists(tree, a):#
    if isinstance(a, ET.Element):
        return a
    elif a == "End Activity" or a == "end activity":
        return tree.find(".//ns0:end_activity", namespace)
    elif a == "Start Activity" or a == "start activity":
        return tree.find(".//ns0:start_activity", namespace)
    elif a == "terminate":
        return tree.find(".//ns0:terminate", namespace)
    else:
        logger.add_activity(a)
        a_ele = exists_by_label(tree, a)
        if a_ele is None:
            logger.info(f'Activity "{a}" existence was checked but not found')
        return a_ele

## Absence: opposite of exists, returns a Boolean 
def absence(tree, a):
    return not Bool(exists(a, tree))

## loop(tree, a): checks if an activity is in a loop, returns None or said loop element
def loop(tree, a):
    loops = tree.findall(".//ns0:loop", namespace)
    for loop in loops:
        apath = exists(loop, a)
        if apath is not None:
            logger.info(f'Found Activity "{a}" in a loop {loop}')
            return loop 
    logger.info(f'Found no Loop with Activity {a} in it')
    return None


def directly_follows(tree, a, b):
    apath = exists(tree, a)
    bpath = exists(tree, b)
    if apath is not None:
        if bpath is not None:
            if a =="terminate":
                logger.info(f'terminate can never lead to another activity, "{b}" directly follows "{a}" is False')
            elif b == "terminate":
                bpaths = tree.findall(".//ns0:terminate", namespace)
                for bpath in bpaths:
                    ## For terminates only must directly follows is accepted, since can directly follows makes no sense
                    must = directly_follows_must(tree, apath, bpath)
                    if must:
                        logger.info(f'Found a terminate that directly follows "{a}"')
                        return True
                logger.info(f'Found no terminate that directly follows "{a}"')
                return False
            else:
                must = directly_follows_must(tree, apath, bpath)
                if must:
                    logger.info(f'Activity "{b}" directly follows Activity "{a}" is True')
                    return True
                else:
                    can = directly_follows_can(tree, apath, bpath)
                    if can:
                        logger.info(f'Activity "{b}" CAN directly follow "{a}": True, but does not have to')
                        return True
                    else:
                        logger.info(f'Activity "{b}" does not directly follow "{a}"')
                        return False
        else:
            logger.add_missing_activity(b)
            logger.info(f'Activity "{b}" is missing in the process')
            return False
    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" is missing in the process')
        return False

## Leads To: Checks if an activity a exists and if it does if the activity it leads to exists after
def leads_to(tree, a, b):
    apath = exists(tree, a)
    bpath = exists(tree, b)
    if apath:
        if bpath:
            compare = compare_ele(tree, apath, bpath)
            if compare == 0:
                logger.info(f'Activity "{a}" and Activity "{b}" are on different exclusive branches')
                return False
            elif compare == -1:
                logger.info(f'Activity "{a}" and Activity "{b}" are in parrallel')
                return False
            elif compare == 1:
                logger.info(f'Activity "{a}" is before Activity "{b}"')
                return True
            elif compare == 2:
                logger.info(f'Activity "{b}" is before Activity "{a}"')
                return False
        else:
            logger.info(f'Activity "{b}" is not found in the tree')
            return False 
    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" is not found in the tree')
        return True


## Precedence: Checks if an activity a exists, and if it does if the activity it requires as a precedence exists prior
def precedence(tree, a, b):
    a_ele= exists(tree, a)
    b_ele = exists(tree, b)
    if a_ele is not None:
        if b_ele is not None:
            compare = compare_ele(tree, a_ele, b_ele)
            if compare == 0:
                logger.info(f'Activities "{a}" and "{b}" are in different exclusive branches and accordingly cannot be compared using precedence')
                return False
            elif compare == -1:
                logger.info(f'Activities "{a}" and "{b}" are in parrallel and accordingly cannot be compared using precedence')
                return False
            elif compare == 1:
                logger.info(f'Activity "{a}" was found before "{b}", so precedence "{a}" requires "{b}" before is False')
                return False 
            elif compare == 2:
                logger.info(f'Activity "{b}" was found before "{a}", so precedence "{a}" requires "{b}" before is True')
                return True
        else:
            logger.add_missing_activity(b)
            logger.info(f'Activity "{a}" was found but Activity "{b}" was not found, so precedence "{a}" requires "{b}" before it is false')
            return False
    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" was not found in the process so precedence "{a}" requires "{b}" before it is true')
        return True


## Leads To Absence: if activity a exists, activity b does not exist after:
def leads_to_absence(tree, a, b):
    apath = exists(tree, a)
    bpath = exists(tree, b)
    if apath is not None:
        if bpath is None:
            return True
        else:
            compare = compare_ele(tree, apath, bpath)
            if compare == 0:
                return True
            elif compare == -1:
                return False
            elif compare == 1:
                return False
            elif compare == 2:
                return True
    else:
        return True
## Precdence Absence: if activity a exists, then activity b does not exist before
def precedence_absence(tree, a, b):
    apath = exists(tree, a)
    bpath = exists(tree, b)
    if apath is not None:
        if not bpath is not None:
            return True
        else:
            compare = compare_ele(tree, apath, bpath)
            if compare == 0: ## exclusive, different branch
                return True 
            elif compare == -1: ## parallel, different branch
                return False 
            elif compare == 1: ## apath is first
                return True
            elif compare == 2: ## bpath is first
                return False 
    else:
        return True

## parallel: checks if activities a and b are in parallel, if either does not exist return false
def parallel(tree, a, b):
    apath = exists(tree, a)
    bpath = exists(tree, b)
    if apath is not None:
        if bpath is not None:
            compare = compare_ele(tree, apath, bpath)
            if compare == -1:
                logger.info(f'Activities "{a}" and "{b}" are in parallel')
                return True
            else:
                logger.info(f'Activities "{a}" and "{b}" are not in parallel')
                return False
        else:
            logger.add_missing_activity(b)
            logger.info(f'Activity "{b}" is missing in the process')
            return False

    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" is missing in the process')
        return False


# Resource

## Returns whichever activity is executed a resource, if none does return value is None
def executed_by_identify(tree, resource):
    for call in tree.findall(".//ns0:call", namespace):
        target = call.find('.//ns0:annotations/ns0:_generic/ns0:Resource', namespace)
        if target is not None:
            resources_split = target.text.split(",")
            for target_resource in resources_split:
                if resource.strip() == target_resource.strip():
                    label = call.find('.//ns0:parameters/ns0:label', namespace).text
                    logger.info(f'Activity "{label}" was found which is executed by resource {resource}')
                    return label 
    logger.info(f'No Activity was found where resource "{resource}" is annotatet as Resource')
    return None
## Executed By Annotation: checks if an activity a exists, and if it does if it is executed by resource, by checking the annotation for Input Name: Resource
def executed_by(tree, a, resource,):
    apath = exists(tree, a)
    if apath is not None:
        for a_resource in executed_by_annotated(apath, tree):
            if a_resource.strip() == resource.strip():
                logger.info(f'Activity "{a}" is executed by Resource "{resource}"')
                return True
        logger.info(f'Activity "{a}" does not have an annotation Resource "{resource}"')
        return False
    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" is missing in the process')
        return False

## Returns the FIRST resource that is executing activity a, used to compare resources for segregation type requirements
def executed_by_return(tree, a):
    apath = exists(tree, a)
    if apath is not None:
        for resource in executed_by_annotated(apath, tree):
            logger.info(f'Activity "{a}" is executed by resource "{resource}"')
            return resource 
    else:
        logger.add_missing_activity(a)
        logger.info("Activity " + a + " does not exist.")
        return None 


## Time

# timed_alternative: checks if two activities are in a cancel branch relationship, with a timeout before the time_alternative b, if either is missing its false
def timed_alternative(tree, a, b, time):
    a_ele = exists(tree, a)
    if a_ele is not None:
        b_ele = exists(tree, b)
        if b_ele is not None:
            for timeout in timeouts_exists(tree):
                  parallel = parallel_cancel(tree, timeout[0], a_ele)
                  if parallel is not None:
                      if timeout[1] is not None:
                          if not timeout[1].isdigit():
                              logger.warning('timeout in the parallel cancel uses a dataobject timestamp or is not passed a digit, correct dataobject is assumed, but this is a dynamic data requirement')
                              return exists(timeout[0], a)
                          else:
                              logger.info(f'Identified a timeout in a parallal cancel with "{b}"')
                              if time == int(timeout[1]):
                                  logger.info(f'Verifying existence of "{a} in {parallel}')
                                  return exists(parallel, a)
                              else:
                                  logger.info(f'timeout: "{timeout[1]}", while time required is: "{time}"')
                                  return False
            logger.info('No timeout was found to enforce the timed_alternative requirement')
            return False
        else:
            logger.info(f'Activity {b} is missing so the timed_alternative relationship is False')
    else:
        logger.info(f'Activity "{a}" is missing so the timed_alternative relationship is False')
        return False

# Time, between two syncs, deprecated, after fighting with it for a while, I decided this is not a requirement pattern that actually happens, so it is left unfinished
def min_time_between(tree, a, b, time):
    a_sync = False
    if leads_to(tree, a, b):
        apath = exists(tree, a)
        bpath = exists(tree, b)
        for sync in sync_exists(tree):
            if directly_follows_must(tree, apath, sync[0]) or directly_follows_must(tree, sync[0], apath):
                logger.info(f'identified a sync directly before or after Activity "{a}"')
                a_sync = True
                a_time = sync[1]
            elif a_sync and directly_follows_must(tree, sync[0], bpath):
                logger.info(f"identified a second sync that leads to bpath)")
        logger.info(f'no syncs which are directly before or after "{a}" and "{b}" were identified in order to achieve the min_time_between requirement')
        return False
    else:
        logger.info(f'Activities "{a}" and "{b}" are not in a leads_to relationship, so the min_time_between requirement is False')
        return False 
## By Due Date: annotated, 
## This simply reads the annotation whether the due date is set correctly in the annotation, it does not check actual implementation, could be extended with voting later then it would even work during execution
def by_due_date_annotated(tree, a, timestamp):
    for call in tree.findall(".//ns0:call", namespace):
        label = call.find("ns0:parameters/ns0:label", namespace)
        if label is not None and label.text == a:
            annotation = call.find('.//ns0:annotations/ns0:_generic/ns0:DueDate', namespace)
            if annotation is not None:
                if int(annotation.text) <= int(timestamp):
                    logger.info(f'Annotation for Activity "{a}" which equals the timestamp or is smaller was found')
                    return True
                else:
                    logger.info(f'Activity "{a}" has a annotation for a due date but it is empty')
                    return False
            else:
                logger.info(f'Activity "{a}" does not have a annotation for a due date, add it using the generic annotations DueDate with a unix timestamp')
    logger.add_missing_activity(a)
    logger.info(f'Activity "{a}" does not exist in the tree, and can accordingly never be executed before its due data')
    return False 
## By Due Date: checks if the due date requirement is explicitly defined through sync check 
def by_due_date_explicit(tree, a, timestamp):
    apath = exists(tree, a)
    if apath:
        for call in due_date_exists(tree):
            if int(call[1]) <= int(timestamp):
                condition = f"data.{call[2]}"
                logger.info(f'found a due date activity that enforces the date requirement, check for alternative branch with condition: "{condition}" that eventually leads to "{a}"')
                return data_value_alternative_eventually_follows(tree, condition, a)
        logger.info(f'no due date activity was found to enforce the due date requirement')
        return False
    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" does not exist in the tree, and can accordingly never be executed before its due data')
        return False

## checks both annotated and explicit, returns true if either
def by_due_date(tree, a, timestamp):
    annotated = by_due_date_annotated(tree, a, timestamp)
    explicit = by_due_date_explicit(tree, a, timestamp)
    logger.info(f'The due date is enforced through annotation: {annotated}. The due date is enforced explicitly: {explicit}. Overall this means the due date is {annotated or explicit}')
    if explicit:
        return True
    elif annotated:
        logger.warning('Assurance level is reduced, since the due date is only enforced through annotation')
        return True
    else:
        return False

## There are technically many ways to implement this and accordingly many ways this could be checked, we enforcce here a very visually pleasing way of enforcing this, which is a event based gateway with a timeout. If said timeout finishes first it would mean that the max time between has passed. This is just one of many ways such as adding syncs before and after a and b, but this would be much less checkable and also have several ways of implementing
def max_time_between(tree, a, b, time):
    apath = exists(tree, a)
    bpath = exists(tree, b)
    if apath is not None:
        if bpath is not None:
            for timeout in timeouts_exists(tree):
                print(timeout)
                if parallel_cancel(tree, timeout[0], bpath) is not None:
                    if timeout[1] is not None:
                        if not timeout[1].isdigit(): 
                            logger.warning('timeout in the parallel with cancel uses a dataobject timestamp or is not passed a digit')
                            return True 
                        else:
                            logger.info(f'Identified a timeout in a parrallel with cancel relationship with "{b}"')
                            return time == int(timeout[1])## only works as long as all times are parsed as seconds
                    else:
                        logger.info('timeout in the parallel with cancel is not passed a argument or 0')
                        return False
                    ## A timeout is in an event based gateway with the second one, can be explicitly checked
            logger.info('No timeout was found to enforce the max time between requirement')
            return False
        else:
            logger.add_missing_activity(b)
            logger.info(f'Activity "{b}" is missing in the process')
    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" is missing in the process')
        return False


## Data
## Send Exist: Checks if any activity in tree sends data data, returns said activity or None, currently returns only the first
def send_exist(tree, data):
    dataobjects = data_objects(tree)
    for call in dataobjects:
        for data_object in call[1]:
            if data_object == data:
                label = call[0].find("ns0:parameters/ns0:label", namespace)
                if label is not None:
                    label = label.text
                logger.info(f'found activity"{label}" which sends dataobject "{data}"')
                return call[0]
    logger.info(f'did not find any activity which sends dataobject "{data}"')
    return None
## Receive Exist: Checks if any activity in tree receives data data, returns said activity or None
def receive_exist(tree, data):
    dataobjects = data_objects(tree)
    for call in dataobjects:
        for data_object in call[2]:
            if data_object == data:
                label = call[0].find("ns0:parameters/ns0:label", namespace)
                if label is not None:
                    label = label.text
                logger.info(f'found activity at path "{call[0]}" with label "{label}" which receives dataobject {data}')
                return call[0]
    logger.info(f'did not find any activity which receives dataobject "{data}"')
    return None
def activity_sends(tree, a, data):
    apath = exists(tree, a)
    if apath is not None:
        a_dict = activity_data_checks(tree, apath)
        arguments = a_dict["arguments"]
        prepare = a_dict["prepare"]
        for occurance in arguments:
            if occurance == data:
                logger.info(f'data object "{data}" is sent in the arguments of activity "{a}"')
                return True
        for occurance in prepare:
            if occurance == data:
                logger.info(f'data object "{data}" is prepared for sending in prepare of activity "{a}"')
                return True
        logger.info(f'data object "{data}" is not found in neither prepare nor arguments of Activity "{a}"')
        return False
    else:
        logger.info(f'Activity "{a}" does not exist in the tree, accordingly the send is trivally true')
        return True
def activity_receives(tree, a, data):
    apath = exists(tree, a)
    if "data." in data:
        data = data.split(".",1)
    if apath is not None:
        a_dict = activity_data_checks(tree, apath)
        finalize = a_dict["finalize"]
        for occurance in finalize:
            if occurance == data:
                logger.info(f'data object "{data}" is finalized from Activity "{a}"')
                return True
        logger.info(f'data object "{data}" is not found in finalize of Activity "{a}"')
        return False
    else:
        logger.add_missing_activity(a)
        logger.info(f'Activity "{a}" does not exist in the tree, accordingly the receive is trivally true')
        return True
    
def data_value_alternative(tree, condition):
    if condition_finder(tree, condition):
        return True
    else:
        return False
## One aspect to note, is that this function works trivially with terminates, because there can always only be a single terminate per branch
def data_value_alternative_directly_follows(tree, condition , a):
    branch = condition_finder(tree, condition)
    if branch is None:
        logger.info(f'No branch with condition: "{condition}" was found')
        return False
    apath = exists(branch, a)
    onbranch = False
    counter = 0
    if apath is None:
        logger.info(f'Activity "{a}" did not exist in the branch of condition: "{condition}"')
        return False
    ## This is highly inefficient (3 Iterations instead of 1) but it works and is easy to understand)
    elements = [elem for elem in branch.iter() if elem.tag.endswith('call') or elem.tag.endswith("terminate")]
    for ele in elements:
        if counter == 1:
            logger.info(f'Activity "{a}" did not directly follow the data condition "{condition}"')
            return False
        if ele == apath:
            logger.info(f'Activity "{a}" directly followed the data_condition "{condition}"')
            return True
        counter += 1
    logger.error(f"IF we got here something went wrong, in the data_value_alternative_directly_follows function")
    return False


## Eventually follows a data condition. The default here is to check in the same branch (see scope = "branch") if the scope is said to global it checks anywhere after the branch as well 
def data_value_alternative_eventually_follows(tree, condition, a, scope = "branch"):
    branch = condition_finder(tree, condition)
    if branch is not None:
        apath = exists(branch,a)
        if apath is not None:
            logger.info(f'Activity "{a}" was found on branch following condition "{condition}"')
            return True
        else:
            if scope == "branch":
                logger.info(f'While Branch following condition "{condition}" was found, the Activity "{a}" was not found on the branch')
                return False
            else: ## Scope is global or misspelled
                logger.info(f'Branch following condition"{condition} was found, however the Activity "{a}" was not found on the branch, since the scope is global, the two elements are compared')
                apath = exists(tree, a)
                if a is not None:
                    compare = compare_ele(tree, branch, apath)
                    if compare == 0: ## ele and branch are exclusive different branches
                        logger.info(f'branch and "{a}" are on different exclusive branches')
                        return False
                    elif compare == -1:
                        logger.info(f'branch and "{a}" are on different parallel branches')
                        return False
                    elif compare == 1:
                        logger.info(f'branch is before "{a}", True')
                        return True
                    elif compare == 2:
                        logger.info(f'branch is after "{a}", False')
                        return False
                else:
                    logger.info(f'Activity "{a}" does not exist in the process, eventually follows is False')
                    return False

    else:
        logger.info(f'No branch with condition: "{condition}" was found')
        return False
def data_leads_to_absence(tree, condition, a):
    return not data_value_alternative_eventually_follows(tree, condition, a)

## Obligations vs Permissions: These can be modeled on the requirements side, using ands, ors and by just included the rule or not
## Complex resource requirements: These can also be modeled on the requirements side usind ands, ors and by just including rule or not
