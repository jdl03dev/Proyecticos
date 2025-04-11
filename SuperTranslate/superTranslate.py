import os
import threading
import asyncio
import uuid
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import Translator
import edge_tts
import playsound

# -------------------- CONFIGURACIÓN DEL ICONO DE LA APLICACIÓN --------------------
# Establece el icono de la aplicación en sistemas Windows para mejorar integración visual
try:
    from ctypes import windll
    ventana_icon_path = os.path.join(os.path.dirname(__file__), "A_digital_vector_graphic_features_a_square_app_ico.png")
    if os.name == "nt" and os.path.exists(ventana_icon_path):
        import ctypes
        myappid = 'supertranslate.app.futuristic'  # ID personalizado para el icono en la barra de tareas
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception as e:
    print(f"No se pudo establecer el icono de la ventana: {e}")

# -------------------- DEFINICIÓN DE IDIOMAS Y VOCES --------------------
# Diccionario de idiomas disponibles
idiomas = {
    "Inglés": "en",
    "Español": "es",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it",
    "Portugués": "pt",
    "Chino": "zh-cn",
    "Japonés": "ja"
}

# Voces de Edge TTS asignadas a cada idioma para síntesis de voz
voces_edge = {
    "es": "es-MX-DaliaNeural",
    "en": "en-US-JennyNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "it": "it-IT-ElsaNeural",
    "pt": "pt-BR-FranciscaNeural",
    "zh-cn": "zh-CN-XiaoxiaoNeural",
    "ja": "ja-JP-NanamiNeural"
}

# -------------------- FUNCIÓN PARA REPRODUCIR TEXTO CON VOZ --------------------
# Función asincrónica que sintetiza voz a partir de texto y la reproduce usando Edge TTS
async def reproducir_voz(texto, idioma):
    voz = voces_edge.get(idioma, "es-MX-DaliaNeural")
    filename = f"voz_{uuid.uuid4()}.mp3"
    try:
        communicate = edge_tts.Communicate(texto, voice=voz)
        await communicate.save(filename)
        playsound.playsound(filename)
    finally:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Error al eliminar archivo: {e}")

# Crea un hilo para reproducir voz sin bloquear la interfaz
def hablar_con_voz(texto, idioma):
    threading.Thread(target=lambda: asyncio.run(reproducir_voz(texto, idioma))).start()

# -------------------- FUNCIÓN PRINCIPAL DE TRADUCCIÓN --------------------
# Escucha voz del usuario, la convierte a texto, la traduce y la reproduce en otro idioma
def iniciar_traduccion():
    recognizer = sr.Recognizer()
    translator = Translator()
    recognizer.pause_threshold = 1.5  # Define el tiempo de pausa antes de procesar
    recognizer.energy_threshold = 300  # Nivel mínimo de volumen para detectar voz

    idioma_origen = idiomas[idioma_entrada.get()]
    idioma_destino = idiomas[idioma_salida.get()]

    with sr.Microphone() as source:
        texto_resultado.set(f"🎤 Escuchando... habla en {idioma_entrada.get()}")
        while traduccion_activa[0]:
            try:
                audio = recognizer.listen(source, phrase_time_limit=10)
                texto_voz = recognizer.recognize_google(audio, language=idioma_origen)
                texto_resultado.set(f"📢 {idioma_entrada.get()}: {texto_voz}")

                traduccion = translator.translate(texto_voz, src=idioma_origen, dest=idioma_destino)
                texto_traducido = traduccion.text
                texto_resultado.set(f"{texto_resultado.get()}\n🗣 {idioma_salida.get()}: {texto_traducido}")

                hablar_con_voz(texto_traducido, idioma_destino)

            except sr.UnknownValueError:
                texto_resultado.set("🤔 No entendí, intenta de nuevo...")
            except sr.RequestError as e:
                texto_resultado.set(f"❌ Error con Google API: {e}")
            except Exception as e:
                texto_resultado.set(f"⚠️ Error: {e}")

# -------------------- CONTROL DE HILOS --------------------
# Inicia un hilo de traducción de voz si no hay uno en ejecución
def iniciar_hilo_traduccion():
    if not traduccion_activa[0]:
        traduccion_activa[0] = True
        threading.Thread(target=iniciar_traduccion).start()

# Detiene la traducción en curso
def detener_traduccion():
    traduccion_activa[0] = False
    texto_resultado.set("⏹ Traducción detenida.")

# -------------------- INTERFAZ GRÁFICA (GUI) --------------------
# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Asistente Traductor Multilingüe")
ventana.geometry("500x400")
ventana.configure(bg="#121212")  # Color de fondo oscuro (estilo futurista)
ventana.resizable(False, False)

# Carga de icono en la interfaz principal
try:
    icon_path = os.path.join(os.path.dirname(__file__), "A_digital_vector_graphic_features_a_square_app_ico.png")
    if os.path.exists(icon_path):
        ventana.iconphoto(False, tk.PhotoImage(file=icon_path))
except Exception as e:
    print(f"No se pudo cargar el icono: {e}")

# Variables de control
texto_resultado = tk.StringVar()
traduccion_activa = [False]

# Título futurista
titulo = tk.Label(ventana, text="🔊 Traductor de Voz Futurista", font=("Orbitron", 18, "bold"), fg="#00FFC6", bg="#121212")
titulo.pack(pady=10)

# Frame para selección de idiomas
frame_idiomas = tk.Frame(ventana, bg="#121212")
frame_idiomas.pack(pady=5)

# Combobox para idioma de entrada
tk.Label(frame_idiomas, text="Idioma de Entrada:", font=("Segoe UI", 11), fg="white", bg="#121212").grid(row=0, column=0, padx=5, sticky="e")
idioma_entrada = ttk.Combobox(frame_idiomas, values=list(idiomas.keys()), state="readonly", font=("Segoe UI", 10))
idioma_entrada.grid(row=0, column=1)
idioma_entrada.set("Inglés")

# Combobox para idioma de salida
tk.Label(frame_idiomas, text="Idioma de Salida:", font=("Segoe UI", 11), fg="white", bg="#121212").grid(row=1, column=0, padx=5, sticky="e")
idioma_salida = ttk.Combobox(frame_idiomas, values=list(idiomas.keys()), state="readonly", font=("Segoe UI", 10))
idioma_salida.grid(row=1, column=1)
idioma_salida.set("Español")

# Área de resultado de traducción
resultado = tk.Label(ventana, textvariable=texto_resultado, wraplength=450, justify="left", font=("Consolas", 11), fg="#00FFC6", bg="#1E1E1E", bd=2, relief="groove", padx=10, pady=10)
resultado.pack(padx=10, pady=15, fill="x")

# Botón para iniciar traducción
boton_iniciar = tk.Button(ventana, text="🚀 Iniciar Traducción", command=iniciar_hilo_traduccion, bg="#00C853", fg="white", font=("Segoe UI", 12), relief="flat")
boton_iniciar.pack(pady=6)

# Botón para detener traducción
boton_detener = tk.Button(ventana, text="🛑 Detener", command=detener_traduccion, bg="#D32F2F", fg="white", font=("Segoe UI", 12), relief="flat")
boton_detener.pack(pady=6)

# Inicia la aplicación
ventana.mainloop()
