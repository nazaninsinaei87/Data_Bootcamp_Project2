Changes required for leaflet to be rendered thru flask.

** Changes to Index.html file from orginal one

    1. Add leaflet resources in <head> and <body>
    ---these are to added before closing the <body> tag-----
     <!-- D3 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.5.0/d3.min.js"></script>

    <!-- Leaflet JavaScript-->
    <script src="https://unpkg.com/leaflet@1.0.2/dist/leaflet.js"></script>
    
    <!-- Our JS -->
    <script type="text/javascript" src="../static/logic.js">
    </script>
    
    --- this is to be added in the header tag ----
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.0.2/dist/leaflet.css" />
  
    2. add style to div tag for map
    
    <div id="map"  style="height:400px;width:1000px"> </div>
    
    
** Changes to style.css file from original one

    1. #map,
        body,
        html
        {
            height: 100%;
        }
        
File combination that worked as of Saturday

        index.html, logic.js, app.py (old one)


                Last Updated : Sunday 12.36 AM
                git push to janaki-leaflet performed