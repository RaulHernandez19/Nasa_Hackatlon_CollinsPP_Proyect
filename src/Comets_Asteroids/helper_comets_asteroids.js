import { getsNEOdata } from './api_comets_asteroids'; 

async function keplerianToCartesian(params) {
    const semiMajorAxis = params.a; // Semieje mayor en AU
    const eccentricity = params.e;
    const inclination = params.i * (Math.PI / 180); // Convertir grados a radianes
    const longitudeOfAscendingNode = params.om * (Math.PI / 180); // Convertir grados a radianes
    const argumentOfPeriapsis = params.w * (Math.PI / 180); // Convertir grados a radianes
    const meanAnomaly = params.ma * (Math.PI / 180); // Convertir grados a radianes

    // Calcular la posición en coordenadas heliocéntricas
    const E = meanAnomaly + (eccentricity * Math.sin(meanAnomaly)); // Ecuación de Kepler
    const x = semiMajorAxis * (Math.cos(E) - eccentricity);
    const y = semiMajorAxis * Math.sqrt(1 - eccentricity * eccentricity) * Math.sin(E);

    // Rotación de los ejes según los elementos orbitales
    const xRot = (x * (Math.cos(argumentOfPeriapsis) * Math.cos(longitudeOfAscendingNode) - Math.sin(argumentOfPeriapsis) * Math.sin(longitudeOfAscendingNode) * Math.cos(inclination))) -
                 (y * (Math.sin(argumentOfPeriapsis) * Math.cos(longitudeOfAscendingNode) + Math.cos(argumentOfPeriapsis) * Math.sin(longitudeOfAscendingNode) * Math.cos(inclination)));

    const yRot = (x * (Math.cos(argumentOfPeriapsis) * Math.sin(longitudeOfAscendingNode) + Math.sin(argumentOfPeriapsis) * Math.cos(longitudeOfAscendingNode) * Math.cos(inclination))) +
                 (y * (Math.cos(argumentOfPeriapsis) * Math.cos(inclination)));

    const z = y * Math.sin(inclination);

    // Convertimos a coordenadas cartesianas
    return new Cesium.Cartesian3(xRot * 149597870.7, yRot * 149597870.7, z * 149597870.7); // Multiplicar por AU a km
}

export {keplerianToCartesian};