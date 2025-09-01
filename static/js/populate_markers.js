export function addMapMarkers(locations) {

    const gapIcon = L.icon({
        iconUrl: window.gapIconUrl,
        iconSize: [18, 18],
        iconAnchor: [10, 10],
        popupAnchor: [0, -10]
    });

    const userIconUrl = window.userIconUrl;
    const defaultIconUrl = window.defaultIconUrl;

    function loadBagIcon() {
        return new Promise(resolve => {
            const img = new Image();
            img.onload = () => resolve(L.icon({
                iconUrl: userIconUrl,
                iconSize: [18, 18],
                iconAnchor: [10, 10],
                popupAnchor: [0, -10]
            }));
            img.onerror = () => resolve(L.icon({
                iconUrl: defaultIconUrl,
                iconSize: [18, 18],
                iconAnchor: [10, 10],
                popupAnchor: [0, -10]
            }));
            img.src = userIconUrl;
        });
    }

    const layerGroup = window.layerGroup;

    // Clear previous markers
    layerGroup.clearLayers();

    loadBagIcon().then(bagIcon => {
        locations.forEach(loc => {
            const peakIcon = loc.date === null ? gapIcon : bagIcon;

            const marker = L.marker([loc.latitude, loc.longitude], { icon: peakIcon })
                .addTo(layerGroup)
                .bindTooltip(loc.name, { permanent: false, direction: 'top', offset: [-1, -7] })
                .on('click', e => {
                    const popupContent = `
                        <div class="pop-up">
                          <h3>${loc.date === null ? loc.name : `🏔️${loc.name}👜`}</h3>
                          <p style="font-size:12px;">${loc.description} <a href="${loc.whl_url}" target="_blank">More</a></p>
                          <div style="display:grid; grid-template-columns:max-content 1fr; row-gap:4px; column-gap:8px; font-size:13px; color:#000;">
                            <strong>Height:</strong><span>${loc.height}</span>
                            <strong>Region:</strong><span>${loc.region}</span>
                          </div>
                          ${loc.date === null
                            ? '<p style="text-align:right; font-size:10px;">©2006-2025 Walkhighlands</p>'
                            : `<hr style="border: none; height: 0.5px; background-color: #333; margin: 10px 10px;">
                               <div style="display:grid; grid-template-columns:max-content 1fr; row-gap:4px; column-gap:8px; font-size:13px; color:#000;">
                                  <strong>Date:</strong><span>${loc.date}</span>
                                  ${loc.distance ? `<strong>Distance:</strong><span>${loc.distance}</span>` : ''}
                                  ${loc.friends ? `<strong>Friends:</strong><span>${loc.friends}</span>` : ''}
                                  ${loc.notes ? `<strong>Notes:</strong><span>${loc.notes}</span>` : ''}
                               </div>
                               <p style="text-align:right; font-size:10px;">©2006-2025 Walkhighlands</p>`}
                        </div>
                    `;
                    L.popup()
                     .setLatLng(e.latlng)
                     .setContent(popupContent)
                     .openOn(map);
                });
        });
    });
}

window.addMapMarkers = addMapMarkers;
