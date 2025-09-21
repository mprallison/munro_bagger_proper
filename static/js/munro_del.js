// need global listener as form is generated dynamically
document.addEventListener('submit', async (event) => {
    if (event.target && event.target.id === 'del-form') {
        event.preventDefault();

        const formEl = event.target;

        const formData = {
                        munro_id: formEl.querySelector('#munro-id')?.value,
                        }

        try {
            const response = await fetch('/delBag', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error('Server error');

            const result = await response.json();

            // Save to localStorage before reload
            localStorage.setItem('prev_munro_coords', JSON.stringify(result.coords));

            window.location.reload(); 

        } catch (err) {
            console.error("Error submitting form:", err);
        }
    }
});

window.addEventListener('DOMContentLoaded', () => {
    const coords = JSON.parse(localStorage.getItem('prev_munro_coords'));
    if (coords) {
        localStorage.removeItem('prev_munro_coords');

        if (window.map && typeof goToLocation === 'function') {
            goToLocation(coords[0], coords[1]);
        }
    };
});
