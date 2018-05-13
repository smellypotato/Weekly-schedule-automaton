jQuery(function($) {
    // Asynchronously Load the map API
    var script = document.createElement('script');
    script.src = "//maps.googleapis.com/maps/api/js?libraries=places&key=AIzaSyA4oqlUsj9DzX18Zy7CYdeQkj8GeOeLM_I&callback=initialize";
    document.body.appendChild(script);
});
var autocomplete;
/*function initialize() {
    // Change a few 'var variableName' to 'window.' This lets us set global variables from within our function
    window.directionsService = new google.maps.DirectionsService();
    window.directionsDisplay = new google.maps.DirectionsRenderer();
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'hybrid'//hybrid, roadmap, satellite, terrain
    };

    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    map.setTilt(45);

    // Multiple Markers (Start & end destination)
    window.markers = [
        ['London Eye, London', 51.503454,-0.119562],
        ['Palace of Westminster, London', 51.499633,-0.124755]
    ];

    // Render our directions on the map
    directionsDisplay.setMap(map);

    var options = {
        componentRestrictions: {country: 'HK'}
    };
    var input_1 = document.getElementsByClassName("venueinput")[0];
		new google.maps.places.Autocomplete(input_1,options);

    // Set the current route - default: walking
    calcRoute();

}*/

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
