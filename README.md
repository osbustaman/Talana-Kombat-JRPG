## PASO 1: Instalar python, en el caso de ya tenerlo omitir el paso 1
## PASO 2: crear entorno virtual con virtualenv

Comandos basados en Linux

> Comando para instalar

      pip install viertualenv
      
> Crear entorno virtual

      virtualenv env

> Activar entorno virtual

      source env/bin/activate
      
## PASO 3: instalar requirements.txt en el entorno virtual
> Comando para instalar

      pip install -r requirements

## PASO 4: ejecutar la app
Para ejecutar la aplicación se debe abrir una terminal, navegar hasta la carpeta raiz y ejecutar:

      python3 run.py

Ya con eso la aplicación se inicia. La aplicación puede ser ejecutada de dos formas consumiendo una API o desde el front de la aplicación.

> Consumiendo API: Desde Postman se debe agregar la ruta http://127.0.0.1:5000/create-combat, puede ser POST o GET, y se envia desde el body un json como el siguiente:
{
  "player1": {
    "movimientos": [
      "D",
      "DSD",
      "S",
      "DSD",
      "SD"
    ],
    "golpes": [
      "K",
      "P",
      "",
      "K",
      "P"
    ]
  },
  "player2": {
    "movimientos": [
      "SA",
      "SA",
      "SA",
      "ASA",
      "SA"
    ],
    "golpes": [
      "K",
      "",
      "K",
      "P",
      "P"
    ]
  }
}
En donde retornara un json como este {
    "accion": "success",
    "fight": [
        "Tonyn Stallone avanza y le da una Patada al pobre",
        "Arnaldor Shuatseneguer  conecta un Remuyuken",
        "Tonyn Stallone  usa un Taladoken",
        "Arnaldor Shuatseneguer se mueve ",
        "Tonyn Stallone se mueve ",
        "Arnaldor Shuatseneguer  conecta un Remuyuken",
        "Arnaldor Shuatseneguer gana la pelea y aun le queda 2 de energía"
    ]
}
----------
> Desde la aplicación: se debe ejecutar la ruta http://127.0.0.1:5000/ y mostrará una pagina con instrucciones del juego, se debe agregar los movimientos y golpes y eso desplegara inputas para movimientos y golpes para cada jugador, al llenar los campos se obtendra el resultado al presionar el boton A pelear!!