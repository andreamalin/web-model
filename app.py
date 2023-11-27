
import cv2
from flask import Flask, render_template, Response, jsonify
from utilities import convert_avi_to_mp4

app = Flask(__name__)

# Si tienes varias cámaras puedes acceder a ellas en 1, 2, etcétera (en lugar de 0)
camara = cv2.VideoCapture(0)

"""
    Configuraciones de vídeo
"""
FRAMES_VIDEO = 20.0
RESOLUCION_VIDEO = (640, 480)
# El código de 4 dígitos. En windows me parece que se soporta el XVID
fourcc = cv2.VideoWriter_fourcc(*'XVID')
archivo_video = None
grabando = False

# Una función generadora para stremear la cámara
# https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/


def generador_frames():
    while True:
        ok, imagen = obtener_frame_camara()
        if not ok:
            break
        else:
            # Regresar la imagen en modo de respuesta HTTP
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + imagen + b"\r\n"


def obtener_frame_camara():
    ok, frame = camara.read()
    if not ok:
        return False, None
    # Escribir en el vídeo en caso de que se esté grabando
    if grabando and archivo_video is not None:
        archivo_video.write(frame)
    # Codificar la imagen como JPG
    _, bufer = cv2.imencode(".jpg", frame)
    imagen = bufer.tobytes()

    return True, imagen


# Cuando visiten la ruta
@app.route("/streaming_camara")
def streaming_camara():
    return Response(generador_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Cuando visiten /, servimos el index.html
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/comenzar_grabacion")
def comenzar_grabacion():
    global grabando
    global archivo_video
    if grabando and archivo_video:
        return jsonify(False)
    nombre = "output.avi"
    archivo_video = cv2.VideoWriter(
        nombre, fourcc, FRAMES_VIDEO, RESOLUCION_VIDEO)
    grabando = True
    return jsonify(True)


@app.route("/detener_grabacion")
def detener_grabacion():
    global grabando
    global archivo_video
    if not grabando or not archivo_video:
        return jsonify(False)
    grabando = False
    archivo_video.release()
    archivo_video = None

    convert_avi_to_mp4("D:\Documents\Trabajo\web_model\output.avi", "D:\Documents\Trabajo\web_model\output.mp4")
    return jsonify(True)


@app.route("/estado_grabacion")
def estado_grabacion():
    return jsonify(grabando)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
