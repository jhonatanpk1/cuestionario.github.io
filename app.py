from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cuestionario.db'
app.config['SECRET_KEY'] = 'clave_secreta_para_sesiones'  # Cambiar en producción
db = SQLAlchemy(app)

# Modelos
class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apoyo_social = db.Column(db.Integer)
    motivacion_resultados = db.Column(db.Integer)
    variedad_rutinas = db.Column(db.Integer)
    influencia_musica = db.Column(db.Integer)
    metas_claras = db.Column(db.Integer)
    retroalimentacion = db.Column(db.Integer)
    ambiente_gimnasio = db.Column(db.Integer)
    frecuencia_motivacion = db.Column(db.Integer)
    progreso_fisico = db.Column(db.Integer)
    comunidad_gimnasio = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# Rutas
@app.route('/')
def index():
    return render_template('cuestionario.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    # Recibir datos del formulario y convertir a enteros
    apoyo_social = int(request.form.get('apoyo_social', 0)) if request.form.get('apoyo_social') else 0
    motivacion_resultados = int(request.form.get('motivacion_resultados', 0)) if request.form.get('motivacion_resultados') else 0
    variedad_rutinas = int(request.form.get('variedad_rutinas', 0)) if request.form.get('variedad_rutinas') else 0
    influencia_musica = int(request.form.get('influencia_musica', 0)) if request.form.get('influencia_musica') else 0
    metas_claras = int(request.form.get('metas_claras', 0)) if request.form.get('metas_claras') else 0
    retroalimentacion = int(request.form.get('retroalimentacion', 0)) if request.form.get('retroalimentacion') else 0
    ambiente_gimnasio = int(request.form.get('ambiente_gimnasio', 0)) if request.form.get('ambiente_gimnasio') else 0
    frecuencia_motivacion = int(request.form.get('frecuencia_motivacion', 0)) if request.form.get('frecuencia_motivacion') else 0
    progreso_fisico = int(request.form.get('progreso_fisico', 0)) if request.form.get('progreso_fisico') else 0
    comunidad_gimnasio = int(request.form.get('comunidad_gimnasio', 0)) if request.form.get('comunidad_gimnasio') else 0

    # Guardar en la base de datos
    nueva_respuesta = Respuesta(
        apoyo_social=apoyo_social,
        motivacion_resultados=motivacion_resultados,
        variedad_rutinas=variedad_rutinas,
        influencia_musica=influencia_musica,
        metas_claras=metas_claras,
        retroalimentacion=retroalimentacion,
        ambiente_gimnasio=ambiente_gimnasio,
        frecuencia_motivacion=frecuencia_motivacion,
        progreso_fisico=progreso_fisico,
        comunidad_gimnasio=comunidad_gimnasio
    )
    db.session.add(nueva_respuesta)
    db.session.commit()

    # Redirigir a la página de resultados
    return redirect(url_for('resultados'))

@app.route('/resultados')
def resultados():
    # Calcular promedios para mostrar
    respuestas = Respuesta.query.all()
    total = len(respuestas)
    if total > 0:
        prom_apoyo_social = sum(r.apoyo_social for r in respuestas) / total
        prom_motivacion_resultados = sum(r.motivacion_resultados for r in respuestas) / total
        prom_variedad_rutinas = sum(r.variedad_rutinas for r in respuestas) / total
        prom_influencia_musica = sum(r.influencia_musica for r in respuestas) / total
        prom_metas_claras = sum(r.metas_claras for r in respuestas) / total
        prom_retroalimentacion = sum(r.retroalimentacion for r in respuestas) / total
        prom_ambiente_gimnasio = sum(r.ambiente_gimnasio for r in respuestas) / total
        prom_frecuencia_motivacion = sum(r.frecuencia_motivacion for r in respuestas) / total
        prom_progreso_fisico = sum(r.progreso_fisico for r in respuestas) / total
        prom_comunidad_gimnasio = sum(r.comunidad_gimnasio for r in respuestas) / total
    else:
        prom_apoyo_social = prom_motivacion_resultados = prom_variedad_rutinas = 0
        prom_influencia_musica = prom_metas_claras = prom_retroalimentacion = 0
        prom_ambiente_gimnasio = prom_frecuencia_motivacion = prom_progreso_fisico = 0
        prom_comunidad_gimnasio = 0

    return render_template('resultados.html', 
                           prom_apoyo_social=prom_apoyo_social,
                           prom_motivacion_resultados=prom_motivacion_resultados,
                           prom_variedad_rutinas=prom_variedad_rutinas,
                           prom_influencia_musica=prom_influencia_musica,
                           prom_metas_claras=prom_metas_claras,
                           prom_retroalimentacion=prom_retroalimentacion,
                           prom_ambiente_gimnasio=prom_ambiente_gimnasio,
                           prom_frecuencia_motivacion=prom_frecuencia_motivacion,
                           prom_progreso_fisico=prom_progreso_fisico,
                           prom_comunidad_gimnasio=prom_comunidad_gimnasio)

if __name__ == '__main__':
    db.create_all()  # Crear la base de datos si no existe
    app.run(host='0.0.0.0', port=5000, debug=True)  # Escuchar en todas las interfaces