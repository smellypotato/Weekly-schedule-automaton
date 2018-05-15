function addTimeslot(divName, day){
    var row = divName.parentElement.parentElement;
    var timeslot = row.insertCell(row.cells.length-1);
    timeslot.setAttribute("class","inputtime");
    timeslot.innerHTML = '<input type="time" name="'+day+'starttime">~<input type="time" name="'+day+'endtime" required><input type="button" name="delSlot" value="X" onclick=deleteSlot(this)>';
}

function deleteSlot(td){
    var row = td.parentElement.parentElement;
    row.deleteCell(td.parentElement.cellIndex);
}
