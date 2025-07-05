# AI Email Agent

Sistema inteligente de respuesta automática de emails usando IA con memoria y supervisión humana.

## Características

- **Respuestas Inteligentes**: Usa tu perfil personal y contenido específico del mensaje
- **Memoria de Conversaciones**: Recuerda información sobre remitentes usando IA
- **Sin Duplicados**: No responde múltiples veces al mismo mensaje
- **Supervisión Humana**: Muestra cada respuesta para aprobación antes de enviar
- **Extracción IA**: Aprende automáticamente detalles clave usando inteligencia artificial

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Crear `.env.local` con:
```env
OPENAI_API_KEY=tu_clave_openai
COMPOSIO_API_KEY=tu_clave_composio
GMAIL_INTEGRATION_ID=tu_id_gmail
```

## Uso

```bash
python src/main.py
```

### Comandos Disponibles

- `prompt <texto>` - Pregunta directa a la IA
- `memory` - Ver estadísticas de memoria e información de remitentes
- `profile` - Ver perfil de Gmail
- `quit` - Salir

### Configuración Avanzada

El comportamiento se puede personalizar en `src/config/agent_config.py`:

- **Extracción IA**: Configuración del modelo y categorías de información
- **Configuración de memoria**: Cuántos emails recordar por remitente
- **Tono de respuesta**: Profesional, casual, etc.
- **Información del usuario**: Nombre, rol, etc.
