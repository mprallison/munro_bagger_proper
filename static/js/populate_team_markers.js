export function addTeamMapMarkers(locations, color_list, user_imgs) {


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
                    <div style="max-width: 180px;" class="pop-up">
                    
                        <h3 style="margin: 0;font-weight:bold;">${loc.name}</h3>
                        <p style="margin: 0; font-size: 12px; font-weight: bold; text-align: center;">
                            <a href="${loc.whl_url}" target="_blank">walkhighlands</a>
                        </p>
                        ${loc.count === 0
                        ? ''
                        : `<hr style="border: none; height: 0.5px; background-color: #333; margin: 10px 10px;">
                            <div style="text-align: center;">
                                        
                            ${loc.user_name
                                ?   
                                    loc.user_name
                                    .split(', ')
                                    .map(name => 
                                        `<div style="display: inline-block; text-align: center;">
                                        <img
                                            src="${user_imgs[name]}"
                                            alt="${name}"
                                            style="width: 30px; height: 30px; display: block;"
                                            onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';"
                                        />
                                        <span style="display: none;">${name}</span>
                                        </div>`)
                                    .join(' ')
                                : ''}

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