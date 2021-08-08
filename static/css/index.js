// // [START maps_map_simple]
// let map;

// // function initMap() {
// //   map = new google.maps.Map(document.getElementById("map"), {
// //     center: { lat: 30.274212, lng: -97.743519 },
// //     zoom: 8,
// //   });
// // }

// function initMap() {
//   const myLatLng = { lat: 30.274212, lng: -97.743519 };
//   const map = new google.maps.Map(document.getElementById("map"), {
//     zoom: 4,
//     center: myLatLng,
//   });
//   console.log(data)
//   new google.maps.Marker({
//     position: data,
//     map,
//     title: "Hello World!",
//   });
// }
// function test_func(data) {
//   console.log(data);
// }
// test_func({{ data|safe }})

// function initMap() {
//   const map = new google.maps.Map(document.getElementById("map"), {
//     zoom: 3,
//     center: { lat: 30.274212, lng: -97.743519 },
//   });
//   // Create an array of alphabetical characters used to label the markers.
//   const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
//   // Add some markers to the map.
//   // Note: The code uses the JavaScript Array.prototype.map() method to
//   // create an array of markers based on a given "locations" array.
//   // The map() method here has nothing to do with the Google Maps API.
//   const markers = locations.map((location, i) => {
//     return new google.maps.Marker({
//       position: location,
//       label: labels[i % labels.length],
//     });
//   });
//   // Add a marker clusterer to manage the markers.
//   new MarkerClusterer(map, markers, {
//     imagePath:
//       "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
//   });
// }
// const locations = data;

// // [END maps_map_simple]