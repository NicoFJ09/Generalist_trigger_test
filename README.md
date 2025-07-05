# AI Email Agent

Sistema de respuesta automática de emails usando IA.

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

## Funcionalidad

- Se conecta a Gmail automáticamente
- Responde a emails nuevos con IA
- Recuerda conversaciones
- Interfaz de comandos simple

## Comandos

- `prompt <texto>` - Pregunta directa a la IA
- `memory` - Ver estadísticas de memoria
- `profile` - Ver perfil de Gmail
- `quit` - Salir

El sistema responde automáticamente a emails sin intervención manual.

## Problema Resuelto

✅ **Respuestas Duplicadas**: Ahora verifica threads procesados
✅ **Salida Limpia**: Mensajes de consola simplificados
✅ **Respuestas Naturales**: IA genera respuestas sin placeholders
✅ **Funcionamiento Correcto**: Un email = una respuesta
