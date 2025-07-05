# AI Email Agent

Sistema inteligente de respuesta automática de emails usando IA con memoria y supervisión humana.

## Características

✅ **Respuestas Inteligentes**: Responde usando tu perfil personal (nombre, email) y contenido específico del mensaje
✅ **Memoria de Conversaciones**: Recuerda información sobre remitentes usando IA inteligente
✅ **Sin Duplicados**: No responde múltiples veces al mismo mensaje
✅ **Supervisión Humana**: Muestra cada respuesta para aprobación antes de enviar
✅ **Extracción IA**: Aprende automáticamente detalles clave usando inteligencia artificial

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

### Flujo de Trabajo

1. **Inicio**: El sistema se conecta a Gmail automáticamente
2. **Nuevo Email**: Cuando llega un email nuevo:
   - Usa IA para extraer información clave del remitente
   - Genera respuesta usando tu perfil personal
   - Muestra el email original y la respuesta generada
   - Pregunta: "¿Enviar esta respuesta?" (Sí/No)
3. **Memoria**: Recuerda información entre conversaciones

### Comandos Disponibles

- `prompt <texto>` - Pregunta directa a la IA
- `memory` - Ver estadísticas de memoria y información de remitentes
- `profile` - Ver perfil de Gmail
- `quit` - Salir

### Ejemplo de Respuesta con Extracción IA

```
📧 Email from sarah@techcorp.com
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Hi! I'm Dr. Sarah Johnson, CTO at TechCorp. I'm based in Austin and have 7     │
│ years of experience in React development. I'm interested in collaborating on   │
│ your open source project. You can reach me at +1-512-555-0123.                │
└─────────────────────────────────────────────────────────────────────────────────┘

💡 Learned key details about sender: name: Dr. Sarah Johnson, job_title: CTO, company: TechCorp, location: Austin, experience: 7 years in React development, interest: collaborating on open source project, phone: +1-512-555-0123

🤖 Generated Response
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Hi Dr. Johnson,                                                                 │
│                                                                                 │
│ Thank you for reaching out about collaborating on our open source project!     │
│ It's great to connect with a CTO from Austin with React expertise.            │
│ [... respuesta personalizada usando contexto extraído ...]                     │
│                                                                                 │
│ Best regards,                                                                   │
│ Nicolas Florez                                                                  │
│ florezjnicolas@gmail.com                                                        │
└─────────────────────────────────────────────────────────────────────────────────┘

💡 Send this response? [y/n]: 
```

### Ejemplo de Comando Prompt

```
>: prompt What is your purpose?

🤖 Assistant Response:
Hello Nicolas,

As your AI Email Assistant, my purpose is to help you manage your email communications 
efficiently. I work specifically for you (Nicolas Florez) at florezjnicolas@gmail.com.

My capabilities include:
- Generate personalized email responses using your profile information
- Remember sender information across conversations (names, ages, preferences)
- Provide email management advice tailored to your needs
- Help with communication tasks and follow-ups
- Extract and use context from previous emails
- Maintain professional correspondence on your behalf

I'm here to make your email management seamless and professional. How can I assist you today?

Best regards,
Your AI Email Assistant
```

## Configuración Avanzada

El comportamiento se puede personalizar en `src/config/agent_config.py`:

- **Extracción IA**: Configuración del modelo y categorías de información
- **Configuración de memoria**: Cuántos emails recordar por remitente
- **Tono de respuesta**: Profesional, casual, etc.
- **Información del usuario**: Nombre, rol, etc.

## Funcionalidad Mejorada

- **Respuestas Contextuales**: Usa información de emails anteriores
- **Extracción Inteligente IA**: Detecta información compleja usando inteligencia artificial
- **Prevención de Duplicados**: Un email = una respuesta máximo
- **Flujo Simplificado**: Aprobación directa sin comandos complejos
- **12+ Categorías**: Extrae nombres, empresas, títulos, ubicaciones, proyectos, etc.
