# Slack bot

```cmd
python -m venv env
```

```cmd
env/Scripts/Activate.ps1
```

```cmd
pip install -r requirements.txt
```

```cmd
python.exe -m pip install --upgrade pip
```

```cmd
python.exe app.py
```

## Extras

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
