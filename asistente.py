from flask import Flask
import pyttsx3
import speech_recognition as sr 
import pywhatkit
import yfinance as yf 
import pyjokes
import webbrowser
import datetime
import wikipedia

# Escuchar nuestro micrófono y devolverlo como texto
def transformar_audio_en_texto():
    # Almacenar recognizer en una variable
    r = sr.Recognizer()

    # Configurar el micrófono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó la grabación
        print('Ya puedes hablar')

        # Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en Google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-es")

            # Prueba de que pudo acceder
            print("Dijiste: " + pedido)

            # Devolver pedido
            return pedido
        
        # En caso de que no comprenda el audio
        except sr.UnknownValueError:

            # Prueba de que no comprendió el audio
            print('Ups... No lo entendí')

            # Devolver error
            return 'Sigo esperando'

        # En caso de no poder resolver el pedido
        except sr.RequestError:

            # Prueba de que no comprendió el audio
            print('Ups... No hay servicio')

            # Devolver error
            return 'Sigo esperando'

        # Error inesperado
        except:

            # Prueba de que no comprendió el audio
            print('Ups... Algo ha salido mal')

            # Devolver error
            return 'Sigo esperando'

# Función para que el asistente pueda ser escuchado
def hablar(mensaje):

    # Encender el motor de pyttsx3
    engine = pyttsx3.init()

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# Informar el dia de la semana
def pedir_dia():

    # Crear una variable con los datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear una variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Nombres de los días
    calendario = {0: 'Lunes',
                    1: 'Martes',
                    2: 'Miércoles',
                    3: 'Jueves',
                    4: 'Viernes',
                    5: 'Sábado',
                    6: 'Domingo'}

    # Pronunciar el día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}.')

# Informar de la hora
def pedir_hora():
    # Crea una variable con los datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} y {hora.minute}'

    # Decir la hora
    hablar(hora)

# Saludo inicial
def saludo_inicial():

    # Crear variables con datos de la hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour < 20:
        momento = 'Buenas noches'
    elif hora.hour >= 6 and hora.hour < 13:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    # Decir el saludo
    hablar(f'{momento}, soy ciber Neddy, tu asistente personal. Por favor, dime en qué te puedo ayudar')

# Función central del asistente
def pedir_cosas():

    # Activar el saludo inicial
    saludo_inicial()

    # Variable de corte
    comenzar = True

    # Loop central
    while comenzar:
        # Activa el micrófono y guarda el pedido en un string
        pedido = transformar_audio_en_texto(). lower()

        if 'abrir youtube' in pedido:
            hablar('De acuerdo, estoy abriendo youtube')
            webbrowser.open('htttps://www.youtube.es')
            continue
        elif 'abrir navegador' in pedido:
            hablar('De acuerdo, estoy abriendo el navegador')
            webbrowser.open('https://www.google.es')
            continue

        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        elif 'buscar en wikipedia' in pedido:
            hablar('Voy a buscarlo en wikipedia')
            pedido = pedido.replace('wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)

        elif 'busca en internet' in pedido:
            hablar('Voy a buscarlo')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue

        elif 'reproducir' in pedido:
            hablar('Buena idea, voy a buscarlo')
            pywhatkit.playonyt(pedido)
            continue

        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue

        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                        'amazon':'AMZN',
                        'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'Lo he encontrado, el precio de {accion_buscada} es de {precio_actual}')
                continue
            except:
                hablar('Perdón, pero no he encontrado lo que me has pedido')
                continue
        
        elif 'adiós' in pedido:
            hablar('Me voy a descansar los transistores, avisame si quieres algo más')
            break

pedir_cosas()