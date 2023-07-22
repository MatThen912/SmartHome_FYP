function initMap() {
    var marker;

    const citymap = {
      KualaLumpur: {
        center: { lat: 3.9743, lng: 102.4381 },
        population: 2714856,
      },
    }
    // Create the map.
    // Grab the patient long and lat from the input field 
  
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 8,
      center: { lat: 3.1743, lng: 102.4381 },
  
  
    });
    
    function placeMarker(location) {
        if ( marker ) {
          marker.setPosition(location);
        } else {
         marker = new google.maps.Marker({
         position: location,
         map: map
         });
        }
       }

    google.maps.event.addListener(map, 'click', function( event ){
        placeMarker(event.latLng);
        latitude = event.latLng.lat()
        longt = event.latLng.lng()
        // latitude = event.latLng.lat().toFixed(6);
        // longt = event.latLng.lng().toFixed(6);
        console.log(latitude,longt)
        document.getElementById("id_house_latitude").value = latitude.toFixed(6)
        document.getElementById("id_house_longitude").value = longt.toFixed(6)
        
    });

}