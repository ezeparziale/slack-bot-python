# :robot: Slack bot

Slack bot template con varias funciones.

## Funciones

- Mesanje en directo
- Mensaje en canal
- Reación
- Menciones
- Comandos
- Programación de mensajes
  
## Run

```shell
python -m venv env
```

```shell
env/Scripts/Activate.ps1
```

```shell
pip install -r requirements.txt
```

```shell
python.exe -m pip install --upgrade pip
```

```shell
python.exe app.py
```

## :test_tube: Extras

La configuración de los eventos necesita un "request_url".  
Es cualquier url que redireccione al server donde esta corriendo la app.
En este caso usamos ngrok

Para bajarlo:

```http
https://ngrok.com
```

Una vez descomprimido ejecutar:

```cmd
ngrok http 5000
```
