let map, service, infowindow;
function initMap(){
  const defaultLoc = { lat: 12.9716, lng: 77.5946 }; // Bengaluru
  map = new google.maps.Map(document.getElementById("map"), { center: defaultLoc, zoom: 14 });
  service = new google.maps.places.PlacesService(map);
  infowindow = new google.maps.InfoWindow();

  const input = document.getElementById("place-input");
  const geoBtn = document.getElementById("geo-btn");

  if (input && input.placeholder){
    geocodeAndSearch(input.placeholder);
  }

  if (geoBtn){
    geoBtn.addEventListener("click", ()=>{
      if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(pos=>{
          const loc = { lat: pos.coords.latitude, lng: pos.coords.longitude };
          map.setCenter(loc);
          nearbyPharmacies(loc);
        });
      }
    });
  }

  if (input){
    input.addEventListener("keydown",(e)=>{
      if (e.key === "Enter"){
        e.preventDefault();
        geocodeAndSearch(input.value || input.placeholder);
      }
    });
  }
}

function geocodeAndSearch(place){
  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: place }, (results, status)=>{
    if (status === "OK" && results[0]){
      const loc = results[0].geometry.location;
      map.setCenter(loc);
      nearbyPharmacies({lat: loc.lat(), lng: loc.lng()});
    }
  });
}

function nearbyPharmacies(location){
  const request = { location, radius: 3000, type: ["pharmacy"] };
  service.nearbySearch(request, (results, status)=>{
    if (status === google.maps.places.PlacesServiceStatus.OK && results){
      results.forEach(place=>{
        const marker = new google.maps.Marker({ map, position: place.geometry.location });
        google.maps.event.addListener(marker, "click", ()=>{
          infowindow.setContent(`<strong>${place.name}</strong><br>${place.vicinity || ""}`);
          infowindow.open(map, marker);
        });
      });
    }
  });
}
