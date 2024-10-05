function keplerianToCartesian(params) {

    const semiMajorAxis = params.semi_major_axis; // En UA
    const eccentricity = params.eccentricity;
    const inclination = params.inclination;
    const meanAnomaly = params.mean_anomaly;
    const longOfAscNode = params.long_of_asc_node;
    const argOfPeriapsis = params.arg_of_periapsis;

    // Aquí puedes realizar los cálculos Keplerianos para obtener x, y, z
    // Retornar las coordenadas cartesianas basadas en los cálculos
    return Cesium.Cartesian3.fromDegrees(longOfAscNode, inclination, semiMajorAxis * 1e6);
}
