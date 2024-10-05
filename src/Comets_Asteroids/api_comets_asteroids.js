async function getsNEOdata() {
    const url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,epoch,e,a,i,om,w,ma,diameter,neo,kind&sb-class=IEO";
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`); 
        }
        const data = await response.json();
        console.log(data.data); // Verificar la respuesta
        return data.data; // Los datos que nos interesan
    } catch (error) {
        console.error('Error al obtener datos NEO:', error);
    }
}

export {getsNEOdata};