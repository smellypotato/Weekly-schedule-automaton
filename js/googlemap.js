jQuery(function($) {
    // Asynchronously Load the map API
    var script = document.createElement('script');
    script.src = "//maps.googleapis.com/maps/api/js?libraries=places&key=AIzaSyA4oqlUsj9DzX18Zy7CYdeQkj8GeOeLM_I&language=en-UK&callback=initialize";
    document.body.appendChild(script);
});
var autocomplete;

function initialize() {
  var options = {
      componentRestrictions: {country: 'HK'}
  };
  var input_1 = document.getElementsByClassName("venueinput")[0];
  new google.maps.places.Autocomplete(input_1,options);
}

// Calculate our route between the markers & set/change the mode of travel
function calcRoute() {
    var selectedMode = document.getElementById('travelType').value;
    var request = {
        // London Eye
        origin: new google.maps.LatLng(markers[0][1], markers[0][2]),
        // Palace of Westminster
        destination: new google.maps.LatLng(markers[1][1], markers[1][2]),
        // Set our mode of travel - default: walking
        travelMode: google.maps.TravelMode[selectedMode]
    };
    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });
}
