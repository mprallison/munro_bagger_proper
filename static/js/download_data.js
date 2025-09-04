export async function download() {

    console.log("jj")
    try {
        const response = await fetch('/download', {
            method: 'POST',
        });

        const result = await response.json();  // properly await

        if (response.ok) {
              // ensure user is a string or id
        }
    } catch (err) {
        console.error(err);
    }
}