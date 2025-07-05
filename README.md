# Gmail Profile Fetcher - Composio Integration

Una aplicación Python que se conecta a Gmail usando OAuth2 y obtiene el perfil del usuario a través de Composio's toolset.

## Funcionalidad

Esta aplicación:
- ✅ Autentica con Gmail usando OAuth2
- ✅ Obtiene el perfil del usuario (email, total de mensajes, threads, etc.)
- ✅ Muestra información básica del perfil
- ✅ Escucha nuevos emails en tiempo real (opcional)
- ✅ Maneja errores de autenticación robustamente

## Estructura del Proyecto

```
src/
├── main.py                    # Punto de entrada principal
├── mail/
│   ├── email_handler.py       # Manejador de email
│   └── email_listener.py      # Listener de emails nuevos
└── config/
    └── settings.py            # Configuración y variables de entorno
```

## Configuración

### 1. Variables de Entorno

Crea un archivo `.env.local` en la raíz del proyecto con:

```bash
COMPOSIO_API_KEY=your_composio_api_key_here
GMAIL_INTEGRATION_ID=your_gmail_integration_id_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Dependencias

Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
```

### 3. Configuración de Composio

1. Regístrate en [Composio](https://composio.dev/)
2. Crea una integración de Gmail
3. Obtén tu Integration ID y API Key
4. Configura las variables de entorno

## Uso

### Ejecución

```bash
python src/main.py
```

### Lo que hace la aplicación

1. **Autenticación**: Inicia el flujo OAuth2 y abre automáticamente el navegador
2. **Autorización**: El usuario autoriza la aplicación en Gmail
3. **Obtención del Perfil**: Usa `GMAIL_GET_PROFILE` para obtener información del usuario
4. **Mostrar Resultados**: Muestra el perfil del usuario de forma limpia
5. **Opción de Escucha**: Permite activar la escucha de nuevos emails en tiempo real

## Archivos Principales

### `main.py`
- Punto de entrada principal de la aplicación
- Maneja la inicialización y presentación de resultados
- Incluye opción interactiva para activar el listener

### `email_handler.py`
- Clase `EmailHandler` que maneja la integración con Gmail
- Autentica con OAuth2 y obtiene el perfil del usuario
- Incluye método para habilitar triggers de Gmail

### `email_listener.py`
- Clase `EmailListener` que escucha nuevos emails
- Maneja eventos de triggers de Gmail
- Procesa emails entrantes de forma modular

### `settings.py`
- Carga variables de entorno desde `.env.local`
- Valida que todas las variables requeridas estén presentes

## Características Técnicas

- **OAuth2**: Autenticación segura con Gmail
- **Composio Integration**: Usa Composio's toolset para la integración
- **Email Listening**: Escucha emails en tiempo real usando triggers
- **Manejo de Errores**: Captura y maneja errores de autenticación
- **Apertura Automática del Navegador**: Facilita el flujo OAuth
- **Interfaz Interactiva**: Opción para activar/desactivar el listener

## Resolución de Problemas

### Error: "Invalid integration ID"
- Verifica que tu `GMAIL_INTEGRATION_ID` sea correcto

### Error: "Connection failed or timed out"
- Completa el flujo OAuth en el navegador
- Verifica tu conexión a internet

### Error: "API key not found"
- Verifica que tu archivo `.env.local` contenga `COMPOSIO_API_KEY`