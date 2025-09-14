export function addMapMarkers(locations) {

    // icon if gap
    const gapIcon = L.icon({
        iconUrl: window.gapIconUrl,
        iconSize: [18, 18],
        iconAnchor: [10, 10],
        popupAnchor: [0, -10]
    });

    // icon if bag
    const bagIcon = L.icon({
        iconUrl: window.userIconUrl,
        iconSize: [18, 18],
        iconAnchor: [10, 10],
        popupAnchor: [0, -10]
    });

    // layer group as leaflet marker layer
    const layerGroup = window.layerGroup;

    // Clear previous markers
    layerGroup.clearLayers();

    // at each munro location    
    locations.forEach(loc => {
        // gap or bag icon by presence of date
        const peakIcon = loc.date === null ? gapIcon : bagIcon;

        const marker = L.marker([loc.latitude, loc.longitude], { icon: peakIcon })
            .addTo(layerGroup)
            .bindTooltip(loc.name, { permanent: false, direction: 'top', offset: [-1, -7] })
            .on('click', e => {
                const popupContent = `
                    <div class="pop-up">
                        <h3 style="margin: 0;">${loc.name}</h3>
                        <p style="margin: 0; font-size: 12px; text-align: center;">
                            <a href="${loc.whl_url}" target="_blank">walkhighlands</a>
                        </p>
                        <br>
                        <div style="display:grid; grid-template-columns:max-content 1fr; row-gap:4px; column-gap:8px; font-size:13px; color:#000;">
                        <strong>Height:</strong><span>${loc.height}</span>
                        <strong>Region:</strong><span>${loc.region}</span>
                        </div>
                    </div>
                `;
                L.popup()
                    .setLatLng(e.latlng)
                    .setContent(popupContent)
                    .openOn(map);
            });
    });
}
    
window.addMapMarkers = addMapMarkers;