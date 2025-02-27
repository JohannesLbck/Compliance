import openai
import argparse


# Space for OpenAI API key
openai.api_key = "Insert Your Own Key Here"

## Textual Descriptions
collection_text = "Before the Blood collection can begin the blood bag which serves as a container for collected blood needs to be inspected for defects using the blood bag system. If the blood bag is found to be damp, the bag needs to be replaced. After the inspection of the blood bag, the actual blood collection can begin. First, directly before the venepuncture the donors are re-identified. Before the actual venepuncture, the venepuncture site also needs to be disinfected. One the venepuncture has been completed. The blood is collected for no longer than 5 minutes. Afterwards, the donor is monitored for at least 15 minutes. If the donor is still bleeding after 15 minutes the donor's condition is reevaluated by a physician and the blood has to be marked as unusable for the preparation of platelets. The final activity is always the verification of the donation number on all records, blood bags and laboratory samples."
registration_text = "Upon arrival at the blood establishment, the identity of donors is verified. Afterwards information regarding the purpose and effects of blood donations must be provided to the donors, before obtaining explicit consent. If the consent is not given the process has to immediately stop. If consent is given, the eligibility of the donor should be assessed using an interview, a questionnaire and further direct questions, if necessary. Further questions are necessary if the interview and questionnaire require a physician's assessment or reveal results that are not covered by the guidelines and should be conducted by a physician. Depending on the results of the eligibility assessments, potential donors should be either accepted, rejected or deferred. In both the cases of rejection and deferral the individuals should be given a clear explanation of the reasons for deferral / rejection. "


# Documentation to send to ChatGPT
documentation = """
control methods:
parallel(a, b) <- returns True or False
	Checks if two Activities are in parallel, also works for terminates, timeout and syncs
Event_based_gateway(tree, a, b) <- returns True or False
    Checks if two Activities are in an event based gateway relationship, also works for terminates, timeouts and syncs
exists(a) <- returns the Object Itself which is evaluated to True/False if not inside another method
    Checks if a Activity exists in the tree, also works for Start, End, terminate, sync and timeout. Returns the element itself (which evaluates to True if it is by itself) but can accordingly also be used in other checks
absence(a) <- returns True/False
    Checks if a Activity is absent in the tree. Works as a not exists, so it does NOT return the object if it exists
directly_follows(a, b) <- returns True/False
    Checks if Activity a directly follows Activity b
leads_to(a, b) <- returns True/False
    Checks if a Activity a leads to a Activity b in the process, this also accounts for parallels and exclusive choices, meaning a potentially leads to (a before exclusive, b on the exclusive branch) is regarded as False, and a and b on different parallel branches are false. Meanwhile a and b on the same parallel or exclusive branch are checked for order normally
precedence(a, b) <- returns True/false
    Checks if an Activity a has a Activity b before it, just like leads_to it accounts for exclusives and parallels
absence_leads_to(a, b) <- returns True/False
    Checks if an Activity a is absent before an Activity b, essentially this means if a exists it has to be after b while accounting for parallels and exclusives
leads_to_absence(a, b) <- returns True/False
    Checks if a exists and if it exists that b is not after it, accounts for parallels and exclusives
precedence_absence(a, b) <- returns True/False
    Checks if a exists and if it exists, that b is not before it, accounts for parallels and exclusives
loop(tree, a) <- returns True / False
    Checks if a activity a exists on a loop, returns the loop if it does returns None if not, it is handled this way such that it can also be used to compare if various activities are on the same loop using loop(a) == loop(b) as well as other types of checks
resource methods:
executed_by(a, resources) <- returns True/False
	Checks whether a activity a is executed by resource resource, returns true or false, resources always refers to executing resources like humans or a specific robot.
executed_by_return(a) <- returns a string that represents the resource
    Returns the resource that is executing activity a, used to compare resources for requirements such as segregation of tasks
executed_by_identify(resource) <- returns a activity (can be passed just like activity labels to other methods)
    Returns the element (Activity) that is currently executed by a resource, can be used to check whether a activity executed by a resource is in other relationships (parallel, leads_to, etc)
receive/send methods:
send_exists(data) <- returns the activity or None, can be used as argument
    Checks if data data is sent to any activity (which also means to anyone/anywhere outside the process), returns the activity if it is, returns None if not.
receive_exists(data) <- returns the activity or None, can be used as argument
    Checks if data data is returned from any activity, returns the activity if it is, returns None if not.
activity_sends(a, data) <- returns True/False
	Checks if data data is sent to activity a. This means it is also used to check if data is sent to anywhere/anyone outside the process. 
activity_receives(a, data) <- returns True/False
	Checks if activity a receives data. This means it is used to get data from anywhere/anyone outside the process into the process.
data_alternative methods:
data_value_alternative_directly_follows(condition, activity) <- returns True/False
	Checks if a branch with condition directly leads to a activity, same limitation as above
data_value_alternative_eventually_follows(condition, activity, scope = “branch”) <- returns True/False
    Checks if a branch with condition eventually leads to an activity. There are two options for the scope here either on the same branch which is the default or at any point AFTER the data condition, which has to be manually set with scope = “global”
data_leads_to_absence(condition, label) <- returns True/False
	See above, same thing but just with a absence instead of a exist at the end
time methods:
recurring(rule, time) <- returns True/False
Checks whether any rule(s) is(are) recurring within a loop which executes after a wait for a specific time, could technically be modeled using some for a in list(activites): as well, but will add a specific version of it
by_due_date_explicit(a, timestamp) <- returns True/False
Checks if a due date requirement is explicitly ensured through the existence of a due_date activity, which is a custom endpoint that just enforces a due data with a exclusive check after. This is just one of many ways to enforce a due date so there is also the option to just annotate the due date and enforce it different, see below
by_due_date_annotated(a, timestamp) <- returns True/False
This also checks for a due date, but simply through checking in general annotation, accordingly, if just this check is used to enforce a due date the assurance is reduced
by_due_date(a, timestamp) <- returns True, False, use this method for the requirement
See above, This checks both explicitly and through annotation. If the requirement is enforced explicitly or both, then it gives strong assurance, if only through annotation it gives weak assurance
max_time_between(a, b, time) <- returns True/False
There are technically many ways to implement this and accordingly many ways this could be checked, we enforce here a very visually pleasing way of enforcing this, which is a event based gateway with a timeout. If said timeout finishes first it would mean that the max time between has passed. This is just one of many ways such as adding syncs before and after a and b, but this would be much less checkable and also have several. The enforced way also has the advantage that it uses only standard bpm objects (timeout, event based gateway) and not special symbols (syncs, etc)

"""

# Prompt to be sent to ChatGPT
prompt = f"""
Given the following list of functions and standard python functions, use the functions to write a expression that represents the requirement: {collection_text}. 

1. Procedure:
First identify activities, dataobjects and resources from the requirement. A resource is whatever or whoever is executing a activitiy. Whenever a requierment talks about the start / end then it means the "Start Activity" and the "End Activity". These can be passed to the methods as arguments where a, b are replaced by activities and data is replaced by dataobjects. Try to keep dataobjects short and concatenate them using data_object. Try to keep Activities short. If a process should terminate this is reflected through a "Terminate" Activity. Meanwhile timestamps are unix timestamps while time are seconds. 
Not every requirement will have resources and data objects. Resources represent humans/robots that conduct specific steps in the process.

2. Next identify the types of methods needed to create the expression:
Not every requirement will have every type of method.
The types are all found in the documentation and explained below:
control methods:
These are used to ensure that certain activities should exist, be executed before or after a certain activity or in parallel (at the same time) as another activity.

data_value_alternative methods:
These methods are used to represent conditions in requirements where a data object getting to a certain value should lead to something else like a activity or a terminate. A condition in any data_value_alternative type method will always contain a data object in some relation to either another data object or a string/int such as "dataobject =='string'" or just not dataobject or dataobject if the dataobject is a boolean. 
If a requirement talks about being the first or the last activity that means the activity direclty follows the "Start Activity" or the "End Activity" directly follows the activity.

time methods:
These are used to ensure any kind of timing requirements. Look for due dates or time descriptions like 5 minutes.

resource methods:
These are used to ensure any kind of resource requirements. Look for terms like "executed by", "done by", "conducted by" or more generally "'verb' by 'resource'.

send/receive methods:
These are used to ensure that activities send or receive data from outside the process. Can also be used to ensure that dataobjects that are used in conditions are actually sent to the process from activities. 


3. Finnaly create the resulting expression:
In the resulting expression data objects and activities should be in "". A resulting expression should always evaluate to either True/False or a Activity/None. Do not write methods. Avoid using "if" and "else". Instead model "if" and "else" using "and" and "or" or by searching for the fitting data_alternative method.

Documentation:
{documentation}
"""

# Send request to ChatGPT
stream = openai.chat.completions.create(
    #model="gpt-4",
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are business process expert, tasked with extracting requirements from a natural language process description to python expressions using the functions given by a documentation and the process description."},
        {"role": "user", "content": prompt}
    ],
    stream=True,
    max_tokens=1000,
    temperature=0.5
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
