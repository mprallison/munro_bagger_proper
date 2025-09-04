// Listen to all submit events on the document
document.addEventListener('submit', async function(event) {
    event.preventDefault();

    // event.target is the form that was submitted
    const formEl = event.target;

    // Make sure the target is a form (safety check)
    if (formEl.tagName.toLowerCase() !== 'form') return;

    const buttonId = event.submitter.id;

    if (buttonId === 'del-profile') {

        try {
            const response = await fetch('/delUser', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                });

            const result = await response.json();
            if (response.ok) {
                window.location.href = `/${user}/view`
                }
            } catch (err) {
                console.error(err);
                    }
        
        } else {
        console.log("error")
        }
    });
