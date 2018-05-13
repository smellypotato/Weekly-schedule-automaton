#! /Python27/python
import cgi
import cgitb
import googlemaps
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
        #check if next course is in time - below is wrong solution!
        #correct solution:
        #   1.get travelling time between fromcourse and tocourse
        #   2.add travelling time to fromcourse earliest starttime
        #   3.check if arriving time + tocourse starttime <= endtime
        #   4.if ok, this is one possible edge (may not exist in the path as lessons before fromcourse affect the starttime and endtime of fromcourse)
        if fromcourse["dow"] == tocourse["dow"]:
            if fromcourse["endtime"] <= tocourse["starttime"]:
                fromcourse["nextlesson"].append(tocourse["id"])
        else:
            if sortorder[fromcourse["dow"]] < sortorder[tocourse["dow"]]:
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

distancelist={}
pathlistdetails = {}

for path in pathlist:
    key = "("+",".join(path)+")"
    pathdetails = {}
    pathdetails["profit"] = courselist[int(path[0])]["income"] - courselist[int(path[0])]["venueExpenditure"]
    pathlistdetails[key]=pathdetails
    for i in xrange(len(path)):
        if i+1 != len(path):
            key = ','.join((path[i],path[i+1]))
            fromcourseindex = int(path[i])
            tocourseindex = int(path[i])+1
            pathdetails["profit"] = pathdetails["profit"] + courselist[int(path[i+1])]["income"] - courselist[int(path[i+1])]["venueExpenditure"]
            #the following if is for reducing request call
            if key not in distancelist:
                distancelist[key]=gmaps.distance_matrix(courselist[fromcourseindex]["venue"],courselist[tocourseindex]["venue"],"transit")["rows"][0]["elements"][0]["duration"]["text"]



print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Schedule Automaton</title>"
print "<head>"
print "<body>"

print pathlist, "<br>"


for item in courselist:
    print "<p>",item,"</p>"

for item in avatimeslot:
    print "<p>",item,"</p>"

print pathlistdetails
print "<br>"

print distancelist,"<br>"


print "<br>"

#print gmaps.distance_matrix(courselist[0]["venue"],courselist[1]["venue"],"transit")["rows"][0]["elements"][0]["duration"]["text"]
print "</body>"
print "</html>"
