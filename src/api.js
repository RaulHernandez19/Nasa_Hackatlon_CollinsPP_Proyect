async function obtenerDatosNEO() {
    const url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api?neo=true&fields=object_name,epoch,mean_anomaly,eccentricity,semi_major_axis,inclination,arg_of_periapsis,long_of_asc_node";
    const response = await fetch(url);
    const data = await response.json();
    return data.data; // La respuesta contiene los datos que nos interesan
}

