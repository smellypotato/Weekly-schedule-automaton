var counter = 1;
function addInput(divName){
  var table = document.getElementById(divName);
  var row = table.insertRow(-1);
  row.setAttribute("class", "row");
  row.innerHTML ='\
  <td class="inputID"><input type="text" name="id" value="'+(counter+1)+'" size="2" readonly></td>\
  <td class="inputtext"><input type="text" name="courseName" required></td>\
  <td class="inputtext"><input type="text" name="venue" autocomplete="on" class="venueinput" size="30" required></td>\
  <td class="inputtext"><select name="dow">\
                          <option value="sunday">Sun</option>\
                          <option value="monday">Mon</option>\
                          <option value="tuesday">Tue</option>\
                          <option value="wednesday">Wed</option>\
                          <option value="thursday">Thur</option>\
                          <option value="friday">Fri</option>\
                          <option value="saturday">Sat</option>\
                        </select></td>\
  <td class="inputtext"><input type="time" name="starttime" required></td>\
  <td class="inputtext"><input type="time" name="endtime" required></td>\
  <td class="inputtext"><input type="text" name="duration" size="4" required></td>\
  <td class="inputtext"><input type="text" name="income" size="4" required></td>\
  <td class="inputtext"><input type="text" name="venueExpenditure" value="0" required></td>\
  <td class="deletebtn"><input type="button" value="Delete" onclick="deleteRow(this)"></td>\
  ';
  counter = counter + 1;
  var options = {
      componentRestrictions: {country: 'HK'}
  };
  var venueinput = row.querySelectorAll(".venueinput")[0];
  new google.maps.places.Autocomplete(venueinput, options);
}
function deleteRow(r) {
  if (counter>1){
    var i = r.parentNode.parentNode.rowIndex;
    document.querySelector("#inputfield").deleteRow(i);
    counter--;
    var table = document.querySelector("#inputfield");
    var rows = table.querySelector(".row");
    i=i-1;
    for (; i < rows.length;i++){
      var id = rows[i].firstElementChild.firstElementChild.value
      rows[i].firstElementChild.firstElementChild.value= parseInt(id)-1;
    }
  }
  else alert("At least one record is required!");
}
