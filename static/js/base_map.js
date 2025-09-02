const apiKey = window.API_KEY 

 var map = L.map('map', {
    center: [57.08, -4.02],
    zoom: 7,
    minZoom: 7,
    maxZoom: 13,
    zoomControl: false 
  });

// Base layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// on zoom layer
L.tileLayer(`https://api.os.uk/maps/raster/v1/zxy/Outdoor_3857/{z}/{x}/{y}.png?key=${apiKey}`, {
  attribution: '&copy; Ordnance Survey',
  maxZoom: 18,
  minZoom: 7,
  tileSize: 512,
  zoomOffset: -1,
  noWrap: true,
  continuousWorld: true,
  className: 'os-tiles'
}).addTo(map);

window.layerGroup = L.layerGroup().addTo(map);

window.map = map;