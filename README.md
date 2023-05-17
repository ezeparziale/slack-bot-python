# :robot: Slack bot

Slack bot template con varias funciones  

## :star: Funciones

- Mesanje en directo
- Mensaje en canal
- Reación
- Menciones
- Comandos
- Programación de mensajes
  
## :running_man: Run

```shell
python -m venv env
```

```shell
source env/bin/activate
```

```shell
python.exe -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

Para la base de datos+app:

```shell
docker-compose -f "docker-compose.yml" up -d
```

Para la app:

```shell
flask run --debug
```

## :right_anger_bubble: Slack

Hay que crear un bot en slack:

```http
https://slack.com/intl/es-ar/help/articles/115005265703-Cómo-crear-un-bot-para-tu-espacio-de-trabajo
```

```http
https://api.slack.com/apps?new_app=1
```

## :globe_with_meridians: Requests

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

## :bell: Comandos

Obtener el clima en una ciudad:

```text
/clima nombre_ciudad
```

Obtener la cotización de una crypto moneda:

```text
/crypto coin_name
```
