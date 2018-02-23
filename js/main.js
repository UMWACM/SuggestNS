function getLocation() {
     if (navigator.geolocation) {
         navigator.geolocation.getCurrentPosition(showPosition);
     } else {
         console.log("no Geo");
     }
 }

var map;
var marker;
var loc;


function saveLoc(){
    loc = marker.getPosition();
    console.log("Latitude: " + loc.lat() +
                "Longitude: " + loc.lng());
}

function emptyLoc(){
    loc = false;
}

function showPosition(position){
map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
marker.setPosition({lat: position.coords.latitude, lng: position.coords.longitude});
}

 function initMap() {
   console.log("Map Loaded");
   // Create a map object and specify the DOM element for display.
   map = new google.maps.Map(document.getElementById('mapPicker'), {
     center: {lat: 59.327, lng: 18.067},
     zoom: 8
   });
   marker = new google.maps.Marker({
     map: map,
     draggable: true,
     animation: google.maps.Animation.DROP,
     position: {lat: 59.327, lng: 18.067}
   });
   marker.addListener('click', toggleBounce);

   console.log(map);
 }
 function toggleBounce() {
   if (marker.getAnimation() !== null) {
     marker.setAnimation(null);
   } else {
     marker.setAnimation(google.maps.Animation.BOUNCE);
   }
 }

$(function() {
	  $("[data-toggle]").click(function() {
		    var target = $(".my-text");
		    if($(this).prop('checked')) {
			      target.html('You are my life <span class="text-red"><3</span>');
		    } else {
			      target.html('My life is beautiful, because...');
		    }
	  })
})

function Get(yourUrl){
     var Httpreq = new XMLHttpRequest(); // a new request
     Httpreq.open("GET",yourUrl,false);
     Httpreq.send(null);
     return Httpreq.responseText;
}

var json_obj;

function Request(){
    if(loc == false) {
        console.log("https://474071e8-3302-4004-99d8-4ea7530bb4db.mock.pstmn.io/?customizer=" + document.getElementById("keywordInput").value + "&tlds=" + CompileTlds());
        json_obj = JSON.parse(Get("https://474071e8-3302-4004-99d8-4ea7530bb4db.mock.pstmn.io/?customizer=" + document.getElementById("keywordInput").value + "&tlds=" + CompileTlds()));
    } else {
        console.log("https://474071e8-3302-4004-99d8-4ea7530bb4db.mock.pstmn.io/?customizer=" + document.getElementById("keywordInput").value + "&tlds=" + CompileTlds() + "&location={lat:" + loc.lat() + ",long:" + loc.lng() + "}");
        json_obj = JSON.parse(Get("https://474071e8-3302-4004-99d8-4ea7530bb4db.mock.pstmn.io/?customizer=" + document.getElementById("keywordInput").value + "&tlds=" + CompileTlds() + "&location={lat:" + loc.lat() + ",long:" + loc.lng() + "}"));
    }
}

function CompileTlds() {
    return "{autos:" + document.getElementById("inlineCheckbox1").checked + ",boats:" +  document.getElementById("inlineCheckbox2").checked + ",homes:" +  document.getElementById("inlineCheckbox3").checked + ",motorcycles:" +  document.getElementById("inlineCheckbox4").checked + ",yachts:" +  document.getElementById("inlineCheckbox5").checked + "}";
}

