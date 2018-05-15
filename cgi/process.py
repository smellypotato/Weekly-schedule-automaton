#! /Python27/python
import cgi
import cgitb
import googlemaps
import copy
from operator import itemgetter
from datetime import datetime
cgitb.enable()

form = cgi.FieldStorage()
id = form.getlist("id")
courseName = form.getlist("courseName")
venue = form.getlist("venue")
dow = form.getlist("dow")
starttime = form.getlist("starttime")
endtime = form.getlist("endtime")
duration = form.getlist("duration")
income = form.getlist("income")
venueExpenditure = form.getlist("venueExpenditure")



print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Schedule Automaton</title>"
print "<head>"
print "<body>"

courselist = [];

for i in xrange(len(id)):
    course = {"id":id[i],"courseName":courseName[i],"venue":venue[i],"dow":dow[i],"starttime":starttime[i],
    "endtime":endtime[i],"duration":duration[i],"income":int(income[i]),"venueExpenditure":int(venueExpenditure[i]),"nextlesson":[]}
    courselist.append(course)

avatimeslot = [];
#append sunday timeslot to list
dowstarttime = form.getlist("sunstarttime")
dowendtime = form.getlist("sunendtime")
for i in xrange(len(dowstarttime)):
    avatimeslot.append({"dow":"sunday","starttime":dowstarttime[i],"endtime":dowendtime[i]})

#append monday timeslot to list
dowstarttime = form.getlist("monstarttime")
dowendtime = form.getlist("monendtime")
for i in xrange(len(dowstarttime)):
    avatimeslot.append({"dow":"monday","starttime":dowstarttime[i],"endtime":dowendtime[i]})

#append tuesday timeslot to list
dowstarttime = form.getlist("tuesstarttime")
dowendtime = form.getlist("tuesendtime")
for i in xrange(len(dowstarttime)):
    avatimeslot.append({"dow":"tuesday","starttime":dowstarttime[i],"endtime":dowendtime[i]})

#append wednesday timeslot to list
dowstarttime = form.getlist("wedstarttime")
dowendtime = form.getlist("wedendtime")
for i in xrange(len(dowstarttime)):
    avatimeslot.append({"dow":"wednesday","starttime":dowstarttime[i],"endtime":dowendtime[i]})

#append thursday timeslot to list
dowstarttime = form.getlist("thursstarttime")
dowendtime = form.getlist("thursendtime")
for i in xrange(len(dowstarttime)):
    avatimeslot.append({"dow":"thursday","starttime":dowstarttime[i],"endtime":dowendtime[i]})

#append friday timeslot to list
dowstarttime = form.getlist("fristarttime")
dowendtime = form.getlist("friendtime")
for i in xrange(len(dowstarttime)):
    avatimeslot.append({"dow":"friday","starttime":dowstarttime[i],"endtime":dowendtime[i]})

#append saturday timeslot to list
dowstarttime = form.getlist("satstarttime")
dowendtime = form.getlist("satendtime")
for i in xrange(len(dowstarttime)):
    avatimeslot.append({"dow":"saturday","starttime":dowstarttime[i],"endtime":dowendtime[i]})

gmaps = googlemaps.Client("AIzaSyA4oqlUsj9DzX18Zy7CYdeQkj8GeOeLM_I")

#remove all courses not fit in timeslot
for item in reversed(courselist):
    fit = False;
    for slot in avatimeslot:
        if item["dow"] == slot["dow"]:
            if item["starttime"]<slot["starttime"]:
                item["starttime"]=slot["starttime"]
            if item["endtime"]>slot["endtime"]:
                item["endtime"]=slot["endtime"]
            avamins = (int(item["endtime"][:-3]) * 60 + int(item["endtime"][-2:])) - (int(item["starttime"][:-3]) * 60 + int(item["starttime"][-2:]))
            if int(item["duration"]) <= avamins:
                fit = True;
                break;
    if not fit:
        courselist.remove(item)

#sort the courselist by day of week then by starttime
sortorder={"sunday":0, "monday":1, "tuesday":2, "wednesday":3, "thursday":4, "friday":5, "saturday":6}
courselist.sort(key=lambda x: (sortorder[x["dow"]],x["starttime"]))


for item in courselist:
    item["id"] = str(courselist.index(item))

#main point
idgraph = {}
x = 0
for i in xrange(len(courselist)):
    for j in range(i+1,len(courselist)):
        fromcourse = courselist[i]
        tocourse = courselist[j]
        fromcourse["nextlesson"].append(tocourse["id"])
    idgraph[courselist[i]["id"]]=courselist[i]["nextlesson"]

def paths(graph, v):
    #>>> g = {1: [2, 3], 2: [3, 4], 3: [1], 4: []}
    #>>> sorted(paths(g, 1))
    #[[1, 2, 3], [1, 2, 4], [1, 3]]
    #>>> sorted(paths(g, 3))
    #[[3, 1, 2, 4]]
    path = [v]                  # path traversed so far
    seen = {v}                  # set of vertices in path
    def search():
        dead_end = True
        for neighbour in graph[path[-1]]:
            if neighbour not in seen:
                dead_end = False
                seen.add(neighbour)
                path.append(neighbour)
                for p in search():
                    yield p
                path.pop()
                seen.remove(neighbour)
        if dead_end:
            yield list(path)
    for p in search():
        yield p


#sort back
courselist = sorted(courselist, key = itemgetter("id"))


#get all possible path
pathlist=[]
for id in idgraph:
    for path in sorted(paths(idgraph, id)):
        pathlist.append(path)
    if [id] not in pathlist:
        pathlist.append([id])

distancelist={}
pathlistdetails = {}

for path in pathlist:
    key = "("+",".join(path)+")"
    pathdetails = {}
    #profit of first item
    pathdetails["profit"] = courselist[int(path[0])]["income"] - courselist[int(path[0])]["venueExpenditure"]
    pathlistdetails[key]=pathdetails
    pathdetails["lessons"] = []
    #first course
    course = copy.deepcopy(courselist[int(path[0])])
    course["endtime"] = '{:02d}:{:02d}'.format(*divmod((int(course["starttime"][:-3]) * 60 + int(course["starttime"][-2:]) + int(course["duration"])), 60))

    course.pop("nextlesson")
    pathdetails["lessons"].append(course)
    for i in xrange(len(path)):
        if i+1 != len(path):
            key = ','.join((path[i],path[i+1]))
            fromcourseindex = int(path[i])
            tocourseindex = int(path[i+1])
            #calculate profit
            pathdetails["profit"] = pathdetails["profit"] + courselist[tocourseindex]["income"] - courselist[tocourseindex]["venueExpenditure"]
            #the following if is for reducing request call
            if key not in distancelist:
                distancelist[key]=int(gmaps.distance_matrix(courselist[fromcourseindex]["venue"],courselist[tocourseindex]["venue"],"transit")["rows"][0]["elements"][0]["duration"]["text"].split()[0])
                #very close
                if distancelist[key] < 5:
                    distancelist[key] = 0
                #add buffer time
                elif distancelist[key] >10:
                    distancelist[key] = distancelist[key] + 10
            course = copy.deepcopy(courselist[tocourseindex])
            #print courselist[fromcourseindex],"<br>",course
            if courselist[fromcourseindex]["dow"] == course["dow"]:
                #print pathdetails["lessons"]#[i]["endtime"]
                earlieststarttime = '{:02d}:{:02d}'.format(*divmod((int(courselist[fromcourseindex]["endtime"][:-3]) * 60 + int(courselist[fromcourseindex]["endtime"][-2:]) + distancelist[key]), 60))
                #earlieststarttime = "18:00"
                #choose the later starttime
                if earlieststarttime > course["starttime"]:
                    course["starttime"] = earlieststarttime
                #check end time is valid
                earliestendtime = '{:02d}:{:02d}'.format(*divmod((int(course["starttime"][:-3]) * 60 + int(course["starttime"][-2:]) + int(course["duration"])), 60))
                if earliestendtime <= course["endtime"]:
                    course["endtime"] = earliestendtime
                else: #not fit
                    pathdetails["profit"] = -99999
                    continue
            else :
                course["endtime"] = '{:02d}:{:02d}'.format(*divmod((int(course["starttime"][:-3]) * 60 + int(course["starttime"][-2:]) + int(course["duration"])), 60))
            course.pop("nextlesson")
            pathdetails["lessons"].append(course)
            #print key, pathdetails, "<br>"

#print distancelist
#print courselist
#for item in pathlistdetails:
#    print "<p>",item,"</p>"

#for item in avatimeslot:
#    print "<p>",item,"</p>"
#for key in pathlistdetails:
#    print key, pathlistdetails[key]
#    print "<br>"
#print "<br>"
#for item in sorted(pathlistdetails.items(), key=lambda x: x[1]['profit'], reverse = True):
#    print item, "<br>"
print "<h2>Calculated Result</h2>"
bestresult = sorted(pathlistdetails.items(), key=lambda x: x[1]['profit'], reverse = True)[0]
print "<p>Weely Net Income: $" + str(bestresult[1]["profit"]) + "</p>"
#print bestresult
print "<h3>Details:</h3>"
print "<table border = 'solid'>"
print "<tr><th>Day</th><th colspan>Suggested Timeslot</th><th>Course</th><th>Venue</th><th>Income</th><th>Venue Expenditure</th>"
for lesson in bestresult[1]["lessons"]:
    print "<tr>"
    print "<td>",lesson["dow"],"</td><td>", lesson["starttime"],"~", lesson["endtime"],"</td><td>",lesson["courseName"],"</td><td>", lesson["venue"],"</td><td>$", lesson["income"],"</td><td>$", lesson["venueExpenditure"],"</td>"
    print "</tr>"
print "</table>"
print "<h3>Your available timeslots:</h3>"
print "<table border = 'solid'>"
print "<tr><th>Day</th><th>Timeslot</th>"
for timeslot in avatimeslot:
    print "<tr>"
    print "<td>",timeslot["dow"], "</td><td>", timeslot["starttime"],"~", timeslot["endtime"],"</td>"
    print "</tr>"
print "</table>"
print "<br>"
print "<button onClick='location.href = \"../index.html\"'>Try a new schedule</button>"

print "</body>"
print "</html>"
