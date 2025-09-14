// need global listener (on submit) as form is generated dynamically

document.addEventListener('submit', async (event) => {
    // check event exists and matches target elem
    if (event.target && event.target.id === 'bag-form') {
        // stop default behaviour
        event.preventDefault();

        const formEl = event.target;

        const formData = {
            munro_id: formEl.querySelector('#munro-id')?.value,
            date: formEl.querySelector('#date')?.value,
            distance: formEl.querySelector('#distance')?.value || null,
            friends: formEl.querySelector('#friends')?.value || null,
            notes: formEl.querySelector('#notes')?.value || null,
            private: formEl.querySelector('#private')?.value || null
            };

        try {
            const response = await fetch('/addBag', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error('Server error');

            const result = await response.json();

            // Save to localStorage before reload
            localStorage.setItem('newBag', true);
            localStorage.setItem('prev_munro_coords', JSON.stringify(result.coords));

            window.location.reload(); 

        } catch (err) {
            console.error("Error submitting form:", err);
        }
    }
});

// Handle previous coordinates / fireworks on page load
document.addEventListener('DOMContentLoaded', () => {
    const coords = JSON.parse(localStorage.getItem('prev_munro_coords'));
    if (coords) {
        localStorage.removeItem('prev_munro_coords');
        if (window.map && typeof goToLocation === 'function') {
            goToLocation(coords[0], coords[1]);
        }
    }

    if (localStorage.getItem('newBag')) {
        startFireworksOnMap(window.map);
        localStorage.removeItem('newBag');
    }
});
