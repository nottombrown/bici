var google;
var geocoder;
var googleMap = function () {

  var map;
  this.initialize = function () {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(37.390891, - 5.987549);
    var myOptions = {
      zoom: 14,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  }


  this.codeAddress = function () {
    var address = document.getElementById("
	address ").value;
    geocoder.geocode({
      'address': address
    }, function (results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
        });
      } else {
        alert("
	Geocode was not successful
	for the following reason: " + status);
      }
    });
  }
  return this;
}();
$(document).ready(function () {
  $("#geocode - button ").onClick(googleMap.codeAddress());
})
