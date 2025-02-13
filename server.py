from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from astroquery.jplhorizons import Horizons
from astropy.time import Time
import datetime
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Mapping of planet names to their Horizons IDs
PLANET_IDS = {
    'mercury': '199',
    'venus': '299',
    'earth': '399',
    'mars': '499',
    'jupiter': '599',
    'saturn': '699',
    'uranus': '799',
    'neptune': '899',
    'pluto': '999'  # Optional
}

# Mapping of moon names to their Horizons IDs
MOON_IDS = {
    'moon': '301',  # Earth's Moon
    # Add other moons as needed, e.g., 'phobos': '401', 'deimos': '402' for Mars' moons
}

# Mapping of asteroid names to their Horizons IDs
ASTEROID_IDS = {
    'ceres': '1',
    'pallas': '2',
    'juno': '3',
    'vesta': '4',
    # Add more asteroids as needed
}

# Mapping of comet names to their Horizons IDs
COMET_IDS = {
    'halley': '1P',
    'hyakutake': '109P',
    # Add more comets as needed
}

# Mapping of Potential Hazard Asteroid (PHA) names to their Horizons IDs
PHA_IDS = {
    'apophis': '99942',
    # Add more PHAs as needed
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solar_system')
def solar_system():
    return render_template('solar_system_view.html')

@app.route('/earth_close_items')
def earth_close_items():
    return render_template('earth_close_items.html')

@app.route('/api/object_positions', methods=['GET'])
def get_object_positions():
    """
    Endpoint to get positions of various celestial objects.
    Query Parameters:
    - fecha: Date in YYYY-MM-DD format (optional, defaults to current date)
    - type: Type of object ('planet', 'moon', 'asteroid', 'comet', 'pha') (optional, defaults to 'planet')
    - names: Comma-separated list of object names to retrieve (optional, defaults to all in the type)
    """
    fecha_str = request.args.get('fecha')
    obj_type = request.args.get('type', 'planet').lower()
    names_str = request.args.get('names')

    if fecha_str:
        try:
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    else:
        fecha = datetime.datetime.utcnow()

    # Convert date to Julian Day
    t = Time(fecha)
    jd = t.jd

    # Select the appropriate ID mapping based on object type
    if obj_type == 'planet':
        id_map = PLANET_IDS
    elif obj_type == 'moon':
        id_map = MOON_IDS
    elif obj_type == 'asteroid':
        id_map = ASTEROID_IDS
    elif obj_type == 'comet':
        id_map = COMET_IDS
    elif obj_type == 'pha':
        id_map = PHA_IDS
    else:
        return jsonify({'error': 'Invalid object type specified.'}), 400

    # If specific names are provided, filter the id_map
    if names_str:
        requested_names = [name.strip().lower() for name in names_str.split(',')]
        id_map = {name: id_horizons for name, id_horizons in id_map.items() if name in requested_names}

    if not id_map:
        return jsonify({'error': 'No valid object names provided.'}), 400

    object_positions = {}

    for nombre, id_horizons in id_map.items():
        try:
            obj = Horizons(id=id_horizons, location='@sun', epochs=jd, id_type='id')
            vec = obj.vectors()
            object_positions[nombre] = {
                'x': vec['x'][0],  # AU
                'y': vec['y'][0],
                'z': vec['z'][0]
            }
        except Exception as e:
            print(f"Error obtaining position for {nombre}: {e}")
            object_positions[nombre] = {'error': str(e)}

    return jsonify(object_positions)

@app.route("/header")
def header():
    return render_template("header.html") 

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto que Render asigna
    app.run(host="0.0.0.0", port=port, debug=True)