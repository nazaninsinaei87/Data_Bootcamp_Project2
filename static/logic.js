//link for  data
var url = "/region"


d3.json(url, createMarkers);

function createMarkers(response){
    
    // pull the winery coordinates from the response
    var coords = response[0].coordinates;
    
    //initialize an array to hold the quake markers
    var wineryMarkers = [];
    
    
    //loop thru the features array
    for (var i=0; i < coords.length; i++){
        if(coords[i]){
        
        var wineryLocation = JSON.parse(coords[i]);
        console.log(wineryLocation);
        var markerOptions = {
        fillColor: "red",
        color: "white",
        weight:1,
        opacity: 1,
        fillOpacity: 0.8,
        radius: 2
        };
         
        // for each winery location, create a marker and bind a pop with properties
        
        var wineryMarker = L.circle([wineryLocation[0], wineryLocation[1]], markerOptions);
        
        // add the winery marker to the wineryMarkers array
        wineryMarkers.push(wineryMarker);
    }
    }
    
    //create a layer group made from the wineryMarkers array, pass it into createMap function
    createMap(L.layerGroup(wineryMarkers));
    
}

function createMap(wineries){
    // create a tile layer that will be the background of our map.
    var mapbox = 'https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?' + 'access_token=pk.eyJ1IjoiamRrb3JhIiwiYSI6ImNqaWc4ZDc0djBpajczb3QxMm91NmNnY28ifQ.FgOYmoVC85ZTAaeViPiTDQ';

   /* styles = [
    'streets-v9',
    'satellite-streets-v9',
    'light-v9',
    'dark-v9',
    'outdoors-v9'
    ]
    
    var mapbox = 'https://api.mapbox.com/styles/v1/mapbox/' + styles[0] + '/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWF0dGFseXRpY3MiLCJhIjoiY2podjEzNnltMHVnMDN1cGE1OWczMW5kdiJ9.p4Joc3qGh0zN6szhM9Mn9Q'
*/
    //create a tile layer
    var baseLayer = L.tileLayer(mapbox);
    
    // create a baseMaps object to hold the lightmap layer
      var baseMaps = {
        "Map": baseLayer
      };

    
    //create and overlayMaps object to hold the wineryLayer
    var overlayMaps = {
        "Wineries": wineries
    };
    
    //create the map object with options
    var myMap = L.map('map', {
        center: [37.0902, -95.7129],
        zoom: 5,
        layers: [baseLayer, wineries]
    });
    
     // create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
      L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
      }).addTo(myMap);
    
}

