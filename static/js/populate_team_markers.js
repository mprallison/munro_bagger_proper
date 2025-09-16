export function addTeamMapMarkers(locations) {


    function createCircleIcon(color, count) {
    return L.divIcon({
        className: '',
        html: `
            <div style="
                background-color: ${color+"CC"};
                width: 15px;
                height: 15px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 12px;
                border: 1px solid white;
            ">
                ${count}
            </div>
        `,
        iconSize: [24, 24],
        iconAnchor: [9, 9],
        popupAnchor: [0, 5]
    });
}

    // icon if gap
    const gapIcon = L.icon({
        iconUrl: '/static/images/gap.png',
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
        const teamIcon = loc.count === 0
        ? gapIcon 
        : createCircleIcon(color_list[loc.count], loc.count)


        const marker = L.marker([loc.latitude, loc.longitude], { icon: teamIcon })
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
                        ${loc.count === 0
                        ? ''
                        : `<hr style="border: none; height: 0.5px; background-color: #333; margin: 10px 10px;">
                            <div style="display:grid; grid-template-columns:max-content 1fr; row-gap:4px; column-gap:8px; font-size:13px; color:#000;">
                                ${loc.user_name ? `<strong>Baggers:</strong><span>${loc.user_name}</span>` : ''}
 
                            </div>
                            `}
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
    
window.addTeamMapMarkers = addTeamMapMarkers;