var google;
var $;
var GoogleMap = function (mediaURL,language) {
    var t_spaces, t_bikes,t_available;
    if (language=="es"){
           t_spaces = "Aparcamientos";
           t_bikes = "Bicis";
           t_available = "disponibles";
       }   
    if (language=="en"){
              t_spaces = "Spaces";
              t_bikes = "Bicycles";
              t_available = "available";
          }
    var that = this;
    var map;
    var geocoder;
    var lastWindow;
    var graphWidth = 260; //also defined in css
    var graphHeight = 170;
    var bikeMarkers = [];
    var spaceMarkers = [];
    var addedSpaceMarkers = false;
    this.initialize = function () {
        //assume all other libraries have loaded
        this.geocoder = new google.maps.Geocoder();
        var center = new google.maps.LatLng(37.3876493509, - 5.96565525205);
        var mapOptions = {
            zoom: 14,
            center: center,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        googleMap.loadMarkers(false);
    };

    //if showSpaces is true we color based on spaces instead of vehicles
    this.addMarker = function (kiosk,showSpaces) {
        var name = kiosk.name;
        var spaces = kiosk.spaces;
        var bikes = kiosk.bikes;
        var slots;
        var latlng = new google.maps.LatLng(kiosk.lat, kiosk.lng);
        if (showSpaces){
            slots = spaces;
        }
        else{
            slots = bikes;
        }
        var image = new google.maps.MarkerImage(
        mediaURL + "marker/marker_" + color(slots) + ".png", new google.maps.Size(12, 20),
        // The origin for this image is 0,0.
        new google.maps.Point(0, 0),
        // The anchor for this image is the base of the pin at 0,32.
        new google.maps.Point(0, 32));

        var shadow = new google.maps.MarkerImage(
        mediaURL + "marker/marker_shadow.png",
        //shadow is wider
        new google.maps.Size(22, 20),
        // The origin for this image is 0,0.
        new google.maps.Point(0, 0),
        // The anchor for this image is the base of the pin at 0,32.
        new google.maps.Point(0, 32));

        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            title: name,
            icon: image,
            shadow: shadow
        });
        
        if (showSpaces){
              spaceMarkers.push(marker);
          }
          else{
              bikeMarkers.push(marker);
         }

        var contentString = "</div>"+"<div id='graph_container' " + "style='width:260px;height:170px'" + ">" + "</div>" + "<div class='marker_content'>" + "<div class='label' style='text-align:center'>" + name.slice(4) + "</div><div class='infowin_bikes'><span class='label'>"+t_bikes +":</span> " + bikes + "</div><div class='infowin_spaces'><span class='label'>" + t_spaces + ":</span> " + spaces + "</div>";

        var infoWindow = new google.maps.InfoWindow({
            content: contentString
        });

        function color(slots) {
            if (slots < 1) {
                return "red";
            }
            else if (slots < 3) {
                return "orange";
            }
            else if (slots < 6) {
                return "yellow";
            }
            else {
                return "green";
            }
        }


        google.maps.event.addListener(marker, 'click', function () {
            try {
                lastWindow.close();
            } catch (err) {
                //no window was open yet
            }
            infoWindow.open(map, marker);
            that.makeGraph(kiosk,showSpaces);
            lastWindow = infoWindow;
        });
    };

    this.makeGraph = function (kiosk,showSpaces) {
        // showSpaces = true;
        $("#graph_container").html("<img id='throbber' src='" + mediaURL + "throbber.gif'><img id='graph' width='" + graphWidth + "' height='" + graphHeight + "'>");
        $("#graph").hide();
        $("#throbber").imgCenter({
            scaleToFit: false
        });
        // var maxBikes = kiosk.bikes+kiosk.spaces; //20 seems to be the global max, stick with that
        var maxSlots = 20;
        $.getJSON(("/today_recs/" + kiosk.number), function (rec_data) {
            $.getJSON(("/today_predictions/" + kiosk.number), function (pred_data) {
                var csvData = "";

                function parseToCSV(slots) {
                    var slotPercent = slots * 100 / maxSlots;
                    csvData = parseInt(slotPercent, 10) + ",";
                    return csvData;
                }
                var t_slots;
            if(showSpaces){
                t_slots = t_spaces;
            }
            else{
                t_slots = t_bikes;
            }
                var time = rec_data.length;
                $.each(rec_data, function (index, record) {
                    if(showSpaces){
                          csvData += parseToCSV(record.fields.spaces);
                    }
                    else{
                    csvData += parseToCSV(record.fields.bikes);
                }

                });
                //we update every 10 minutes, make sure that the current number matches up properly.
                csvData += parseToCSV(kiosk.bikes, csvData); // TODO: make sure this is right
                $.each(pred_data, function (index, record) {
                    if(showSpaces){
                          csvData += parseToCSV(record.fields.spaces);
                    }else{
                    csvData += parseToCSV(record.fields.bikes);
                }
                   
                });
                csvData = csvData.slice(0, - 1);
                //copy to http://code.google.com/apis/chart/docs/chart_playground.html to edit
                var chartURL = "http://chart.apis.google.com/chart?chs=" + graphWidth + "x" + graphHeight + "&chtt=+"+t_slots+" "+t_available+"&chts=000000,18&chf=c,lg,90,ffffff,1,ffffff,0&chls=2,1,0&chco=0066CC&chd=t:" + csvData + "&cht=lc&chxt=y,x&chxr=0,0," + parseInt(maxSlots, 10) + "&chxl=1:|00h00|04h00|08h00|12h00|16h00|20h00|24h00" + "&chm=V,FF0000,0," + time + ",1.0" + "|B,DDDDDD,0," + time + ":,0";

                $("#graph").one('load', function () { //Set something to run when it finishes loading
                    $("#throbber").hide();
                    $(this).fadeIn(); //Fade it in when loaded
                }).attr('src', chartURL) //Set the source so it begins fetching
                .each(function () {
                    //Cache fix for browsers that don't trigger .load()
                    if (this.complete) {
                        $(this).trigger('load');
                    }
                });
            });
        });

    };

    this.loadMarkers = function (showSpaces) {
        $.getJSON("/kiosk_data", function (data) {
            that.kiosks = data;
            $.each(that.kiosks, function (index, value) {
                var kiosk = value.fields;
                kiosk.number = value.pk; //for some reason number is stored as pk
                that.addMarker(kiosk,showSpaces);
            });
        });
    };

    this.showBikes = function(){
        try {
            lastWindow.close();
        } catch (err) {
            //no window was open yet
        }
        $.each(spaceMarkers,function(index, marker){
                marker.setVisible(false);
            });
        $.each(bikeMarkers,function(index, marker){
            marker.setVisible(true);
        });

    };
    
    this.showSpaces = function(){
        try {
            lastWindow.close();
        } catch (err) {
            //no window was open yet
        }
        $.each(bikeMarkers,function(index, marker){
            marker.setVisible(false);
        });
        if (!addedSpaceMarkers){
           googleMap.loadMarkers(true);
           addedSpaceMarkers = true;
        }
        $.each(spaceMarkers,function(index, marker){
                marker.setVisible(true);
            });
    };

    this.codeAddress = function () {
        var address = document.getElementById("address").value;
        this.geocoder.geocode({
            'address': address
        }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
            } else {
                alert("Geocode was not successful for the following reason: " + status);
            }
        });
    };
    return this;
};
