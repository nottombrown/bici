var google;
var $;
var GoogleMap = function (mediaURL) {
    var that = this;
    var map;
    var geocoder;
    var lastWindow;
    var graphWidth = 260; //also defined in css
    var graphHeight = 170;
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
        this.loadMarkers();
    };

    this.addMarker = function (kiosk) {
        var name = kiosk.name;
        var spaces = kiosk.spaces;
        var bikes = kiosk.bikes;
        var latlng = new google.maps.LatLng(kiosk.lat, kiosk.lng);
        var image = new google.maps.MarkerImage(
        mediaURL + "marker/marker_" + color(bikes) + ".png", new google.maps.Size(12, 20),
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

        var contentString = "<div id='graph_container' " + "style='width:260px;height:170px'" + ">" + "</div><div class='label'>" + name.slice(4) + "</div>" + "<div class='marker_content'>" + "<br>bikes available: " + bikes + "<br>" + "spaces available: " + spaces + "</p>";

        var infoWindow = new google.maps.InfoWindow({
            content: contentString
        });

        function color(bikes) {
            if (bikes < 1) {
                return "red";
            }
            else if (bikes < 3) {
                return "orange";
            }
            else if (bikes < 6) {
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
            that.makeGraph(kiosk);
            lastWindow = infoWindow;
        });
    };

    this.makeGraph = function (kiosk) {
        $("#graph_container").html("<img id='throbber' src='" + mediaURL + "throbber.gif'><img id='graph' width='" + graphWidth + "' height='" + graphHeight + "'>");
        $("#graph").hide();
        $("#throbber").imgCenter({
            scaleToFit: false
        });
        // var maxBikes = kiosk.bikes+kiosk.spaces; //20 seems to be the global max, stick with that
        var maxBikes = 20;
        $.getJSON(("/today_recs/" + kiosk.number), function (rec_data) {
            $.getJSON(("/today_predictions/" + kiosk.number), function (pred_data) {
                var csvData = "";

                function parseToCSV(bikes) {
                    var bikePercent = bikes * 100 / maxBikes;
                    csvData = parseInt(bikePercent, 10) + ",";
                    return csvData;
                }

                var time = rec_data.length;
                $.each(rec_data, function (index, record) {
                    csvData += parseToCSV(record.fields.bikes);

                });
                //we update every 10 minutes, make sure that the current number matches up properly.
                csvData += parseToCSV(kiosk.bikes, csvData) // TODO: make sure this is right
                $.each(pred_data, function (index, record) {
                    csvData += parseToCSV(record.fields.bikes);
                });
                csvData = csvData.slice(0, - 1);
                //copy to http://code.google.com/apis/chart/docs/chart_playground.html to edit
                var chartURL = "http://chart.apis.google.com/chart?chs=" + graphWidth + "x" + graphHeight + "&chtt=Available+Bikes&chts=000000,18&chf=c,lg,90,ffffff,1,ffffff,0&chls=2,1,0&chco=0066CC&chd=t:" + csvData + "&cht=lc&chxt=y,x&chxr=0,0," + parseInt(maxBikes, 10) + "&chxl=1:|00h00|04h00|08h00|12h00|16h00|20h00|24h00" + "&chm=V,FF0000,0," + time + ",1.0" + "|B,DDDDDD,0," + time + ":,0";

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

    this.loadMarkers = function () {
        $.getJSON("/kiosk_data", function (data) {
            that.kiosks = data;
            $.each(that.kiosks, function (index, value) {
                var kiosk = value.fields;
                kiosk.number = value.pk; //for some reason number is stored as pk
                that.addMarker(kiosk);
            });
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
