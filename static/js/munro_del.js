// Listen to all submit events on the document
document.addEventListener('submit', async function(event) {
    event.preventDefault();

    // event.target is the form that was submitted
    const formEl = event.target;

    // Make sure the target is a form (safety check)
    if (formEl.tagName.toLowerCase() !== 'form') return;

    const buttonId = event.submitter.id;

    if (buttonId === 'del-munro') {

        const data = {
                    munro_id: formEl.querySelector('[id="munro-id"]')?.value
                    }
        try {
            const response = await fetch('/delBag', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
                });

            const result = await response.json();
            if (response.ok) {
                localStorage.setItem('prev_munro_coords', JSON.stringify(result.coords));
                window.location.reload();
                }
            } catch (err) {
                console.error('Error submitting form:', err);
                    }
        
        } else {
        console.log("error")
        };
    });


window.addEventListener('DOMContentLoaded', () => {
    const coords = JSON.parse(localStorage.getItem('prev_munro_coords'));
    if (coords) {

        localStorage.removeItem('prev_munro_coords');

        if (window.map && typeof goToLocation === 'function') {
            goToLocation(coords[0], coords[1]);
        }
    };
    if (localStorage.getItem('newBag')) {
      startFireworksOnMap(window.map);
      localStorage.removeItem('newBag');
    }
});