import { keplerianToCartesian } from './helper_comets_asteroids'; 
import { getsNEOdata } from './api_comets_asteroids'; 

async function addNEOs() {
    neoData=await getsNEOdata()
    
    console.log("Agregando NEOs:", neoData); // Agrega esta línea para ver qué datos se están procesando
    neoData.forEach(neo => {
        const params = {
            a: neo[4],  // Semieje mayor
            e: neo[3],  // Excentricidad
            i: neo[5],  // Inclinación
            w: neo[6],  // Argumento del perihelio
            om: neo[7], // Longitud del nodo ascendente
            ma: neo[2], // Anomalía media
            diameter: neo[8] || 1 // Usar el diámetro si está disponible o 1 km como valor predeterminado
        };
        
        const position = keplerianToCartesian(params);
        
        // Escalar el tamaño del objeto basándose en el diámetro
        const radius = params.diameter / 2 * 1000; // Convertir a metros

        viewer.entities.add({
            position: position,
            ellipsoid: {
                radii: new Cesium.Cartesian3(radius, radius, radius), // Usar un elipsoide uniforme
                material: Cesium.Color.RED.withAlpha(0.6),
            },
            label: {
                text: neo[0],  // Nombre del objeto
                font: '12pt monospace',
                fillColor: Cesium.Color.WHITE,
            }
        });
    });
}

export {addNEOs};