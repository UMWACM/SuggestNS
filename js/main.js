



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
}

function emptyLoc(){
    loc = false;
}

function showPosition(position){
map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
marker.setPosition({lat: position.coords.latitude, lng: position.coords.longitude});
}

 function initMap() {
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

 function locateZip() {
     var zip = document.getElementById("zipInput").value;
   var geocoder = new google.maps.Geocoder();
   geocoder.geocode( { 'address': zip}, function(results, status) {
     if (status == google.maps.GeocoderStatus.OK) {
       map.setCenter(results[0].geometry.location);
       marker.setPosition(results[0].geometry.location);
     }
   });
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
    $('#spinner').html('<img src="images/ball-triangle.svg" id="spinner" style="margin-bottom:5px;" alt="" width="15"></img>&nbsp;');
    if(loc == false) {
        json_obj = JSON.parse(Get('https://dosdude1.com:2023/suggestions?customizer=' + document.getElementById("keywordInput").value + '&tlds=' + CompileTlds()));
    } else {
        console.log(Get('https://dosdude1.com:2023/suggestions?customizer=' + document.getElementById("keywordInput").value + '&tlds=' + CompileTlds() + "&location={lat:" + loc.lat() + ",long:" + loc.lng() + "}"));
        json_obj = JSON.parse(Get('https://dosdude1.com:2023/suggestions?customizer=' + document.getElementById("keywordInput").value + '&tlds=' + CompileTlds() + "&location={lat:" + loc.lat() + ",long:" + loc.lng() + "}"));
    }
    GenerateTable();
}

function CompileTlds() {
    return "{autos:" + document.getElementById("inlineCheckbox1").checked + ",boats:" +  document.getElementById("inlineCheckbox2").checked + ",homes:" +  document.getElementById("inlineCheckbox3").checked + ",motorcycles:" +  document.getElementById("inlineCheckbox4").checked + ",yachts:" +  document.getElementById("inlineCheckbox5").checked + "}";
}

function GenerateTable(){
    var originals = json_obj["originals"];
    var suggestions = json_obj["suggestions"];
    var table_str = '<table class="table table-striped"><thead><tr><th>URL</th><th>Availability</th></tr></thead><tbody>';
    for (var key_o in originals) {
        if (originals.hasOwnProperty(key_o)) {
            var insert;
            if (originals[key_o]) {
                insert = '&#x2714;';
            } else {
                insert = '&#x274C;';
            }
            table_str = table_str + '<tr>' + '<th scope="row">' + key_o + '</th><td>' + insert + '</td></tr>';
        }
    }
    table_str = table_str + '<tr><th scope="row"><hr></th><td><hr></td></tr>';
    for (var key_s in suggestions) {
        if (suggestions.hasOwnProperty(key_s)) {
            var insert;
            if (originals[key_s]) {
                insert = '&#x2714;';
            } else {
                insert = '&#x274C;';
            }
            table_str = table_str + '<tr>' + '<th scope="row">' + key_s + '</th><td>' + insert + '</td></tr>';
        }
    }
    table_str = table_str + '</tbody></table>';
    console.log(table_str);
    $('#fillHere').html(table_str);
    $('#spinner').html('');
}

// Get the input field
var input1 = document.getElementById("keywordInput");

// Execute a function when the user releases a key on the keyboard
input1.addEventListener("keyup", function(event) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        // Trigger the button element with a click
        document.getElementById("generate").click();
    }
});

// Get the input field
var input2 = document.getElementById("zipInput");

// Execute a function when the user releases a key on the keyboard
input2.addEventListener("keyup", function(event) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        // Trigger the button element with a click
        locateZip();
    }
}); 
