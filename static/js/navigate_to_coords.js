export async function goToLocation(lat, lng) {
    const coords = [lat, lng - 0.002];

    window.map.setView(coords, 10);

    // small delay to ensure view updates
    await new Promise(resolve => setTimeout(resolve, 500));

    const circle = L.circle(coords, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0,
        radius: 1200
    }).addTo(window.map);

    // wait 1.5 seconds before removing
    await new Promise(resolve => setTimeout(resolve, 1500));

    window.map.removeLayer(circle);
}

window.goToLocation = goToLocation;
