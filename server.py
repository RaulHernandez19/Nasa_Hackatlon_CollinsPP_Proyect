from flask import Flask, jsonify, request
from flask_cors import CORS
from astroquery.jplhorizons import Horizons
from astropy.time import Time
import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Mapeo de nombres de planetas a sus identificadores en Horizons
PLANET_IDS = {
    'mercury': 199,
    'venus': 299,
    'earth': 399,
    'mars': 499,
    'jupiter': 599,
    'saturn': 699,
    'uranus': 799,
    'neptune': 899,
    'pluto': 999  # Opcional
}

@app.route('/api/planet_positions', methods=['GET'])
def get_planet_positions():
    """
    Endpoint para obtener las posiciones de los planetas.
    Parámetros de consulta:
    - fecha: Fecha en formato YYYY-MM-DD (opcional, por defecto la fecha actual)
    """
    fecha_str = request.args.get('fecha')
    if fecha_str:
        try:
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD.'}), 400
    else:
        fecha = datetime.datetime.utcnow()

    # Convertir la fecha a Día Juliano
    t = Time(fecha)
    jd = t.jd

    planet_positions = {}

    for nombre, id_horizons in PLANET_IDS.items():
        try:
            # Solicitar los vectores heliocéntricos en formato ecuatorial (x, y, z en AU)
            obj = Horizons(id=id_horizons, location='@sun', epochs=jd, id_type='id')
            vec = obj.vectors()
            planet_positions[nombre] = {
                'x': vec['x'][0],  # AU
                'y': vec['y'][0],
                'z': vec['z'][0]
            }
        except Exception as e:
            print(f"Error obteniendo posición para {nombre}: {e}")
            planet_positions[nombre] = {'error': str(e)}

    return jsonify(planet_positions)

if __name__ == '__main__':
    app.run(debug=True)
