

//link for earthquake data for past 7 days
var region_data = "/region"
var wine_data = "../winedata"

// perform api call to the wine-data JSON to get wine reviews information.
d3.json(wine_data, function(wineData){
    console.log(wineData);
    //call the region data
    d3.json(region_data, function(regData){
        console.log(regData);
        var wineMarkers = [];
        var region = regData[0].region;
        var coords = regData[0].coordinates;
        console.log(region);
        console.log(coords);
        for (var i =0; i < wineData.length; i++){
            for (var j =0; j< region.length; j++){
                if (wineData[i].region_1 == region[j]){
                    var wineryLoc = JSON.parse(coords[j]);
                    console.log(wineryLoc);
                }
            }
            
            var radius = wineData[i].points;
            var markerOptions = {
                color: "white",
                weight:1,
                opacity:1,
                fillOpacity: 0.8,
            };
            console.log(wineryLoc);
            console.log(wineryLoc[0]);
            console.log(wineryLoc[1]);
            var wineMarker = L.marker([wineryLoc[0], wineryLoc[1]], markerOptions)
        .bindPopup("<h4> Wine: "+wineData[i].title + "</h4> <hr> <h5> Wine Variety : " + wineData[i].variety + "</h5");
        
            wineMarkers.push(wineMarker);
        }
        
        createMap(L.layerGroup(wineMarkers));
    })
});

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

    
    //create and overlayMaps object to hold the quakeLayer
    var overlayMaps = {
        "Wine Data": wineries
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


    

