#! /Python27/python
import cgi
import cgitb
from operator import itemgetter
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
    "endtime":endtime[i],"duration":duration[i],"income":income[i],"venueExpenditure":venueExpenditure[i],"nextlesson":[]}
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
            fromcourse["nextlesson"].append(tocourse["id"])
    idgraph[courselist[i]["id"]]=courselist[i]["nextlesson"]

#for course in courselist:
    #idgraph[course["id"]] = course["nextlesson"]

def dfs(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n, visited)
    return visited

pathlist = []
for id in idgraph:
    pathlist.append(dfs(idgraph, id, []))


print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Schedule Automaton</title>"
print "<head>"
print "<body>"
#for i in xrange(len(courselist)):
    #pathlist += getPathList(graph[i],graph2[i])
print pathlist
for item in courselist:
    print "<p>",item,"</p>"
#for item in avatimeslot:
#    print "<p>",item,"</p>"
print "<br>"
print "</body>"
print "</html>"
