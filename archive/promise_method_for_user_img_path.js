//check for user image else use generic bag.png
/*const userIconUrl = `/static/images/{{ user }}.*`;

const defaultIconUrl = '/static/images/bag.png';

function loadBagIcon() {
    return new Promise(resolve => {
        const img = new Image();
        img.onload = () => resolve(
          L.icon({
            iconUrl: userIconUrl,
            iconSize: [18, 18],
            iconAnchor: [10, 10],
            popupAnchor: [0, -10]
        }));
        img.onerror = () => resolve(
          L.icon({
            iconUrl: defaultIconUrl,
            iconSize: [18, 18],
            iconAnchor: [10, 10],
            popupAnchor: [0, -10]
        }));
        img.src = userIconUrl;
    });
}

// check image path then build markers

loadBagIcon().then(bagIcon => {
  
locations.forEach(loc => {
    */