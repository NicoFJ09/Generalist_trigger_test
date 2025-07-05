# AI Email Assistant

Sistema inteligente de respuesta automática de emails usando IA con memoria y supervisión humana.

## Configuración del Entorno

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
Crear archivo `.env.local` en la raíz del proyecto:
```env
OPENAI_API_KEY=tu_clave_openai
COMPOSIO_API_KEY=tu_clave_composio
GMAIL_INTEGRATION_ID=tu_id_gmail
```

## Ejecutar el Programa

### Iniciar el Sistema
```bash
python src/main.py
```

## Procedimiento de Autenticación

1. **Conexión OAuth**: El sistema iniciará automáticamente el proceso de autenticación
2. **Autorización del Browser**: Se abrirá una ventana del navegador para autorizar el acceso a Gmail
3. **Completar OAuth**: Seguir las instrucciones en el navegador para autorizar la aplicación
4. **Confirmación**: El sistema confirmará cuando la conexión esté activa
5. **Listener Activo**: El programa comenzará a escuchar emails automáticamente

## Funciones Accesibles

### Procesamiento Automático de Emails
- **Detección**: Detecta automáticamente nuevos emails
- **Extracción IA**: Extrae información del remitente usando inteligencia artificial
- **Generación de Respuesta**: Crea respuestas personalizadas usando tu perfil
- **Aprobación**: Muestra email original y respuesta propuesta para tu aprobación
- **Envío**: Envía la respuesta solo después de tu confirmación

### Comandos Interactivos

**`help`**
- Mostrar ayuda con todos los comandos disponibles
- Lista completa de funciones y ejemplos

**`prompt <texto>`**
- Hacer preguntas directas a la IA
- Ejemplo: `prompt ¿Cuál es el estado de mi sistema?`

**`memory`**
- Ver estadísticas de emails procesados
- Mostrar información aprendida sobre remitentes
- Revisar historial de conversaciones

**`profile`**
- Mostrar información de tu perfil de Gmail
- Ver datos de la cuenta conectada

**`quit`**
- Salir del programa de forma segura

## Configuración Personalizada

Editar `src/config/agent_config.py` para personalizar:

- **Modelo IA**: Cambiar modelo de OpenAI utilizado
- **Temperatura**: Ajustar creatividad de las respuestas
- **Tono**: Modificar el tono de las respuestas (profesional, casual, etc.)
- **Información Personal**: Actualizar nombre, rol, y datos del usuario
- **Categorías de Extracción**: Definir qué información extraer de los emails
- **Memoria**: Configurar cuántos emails recordar por remitente
