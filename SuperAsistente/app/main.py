import speech_recognition as sr
import asyncio
from edge_tts import Communicate

# Función para hablar
async def speak(text):
    print(f"Asistente: {text}")
    communicate = Communicate(text, voice="es-MX-DaliaNeural")
    await communicate.play()

# Función para escuchar
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Esperando tu voz...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="es-MX")
        print(f"👂 Escuchado: {text}")
        return text
    except sr.UnknownValueError:
        print("No entendí, intentá de nuevo.")
        return None
    except sr.RequestError as e:
        print(f"Error con el servicio de reconocimiento: {e}")
        return None

# Loop principal
async def main():
    while True:
        user_input = listen()
        if user_input:
            if "adiós" in user_input.lower():
                await speak("Hasta luego.")
                break
            await speak(f"Vos dijiste: {user_input}")

if __name__ == "__main__":
    asyncio.run(main())
