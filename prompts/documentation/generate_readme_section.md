# Generate README Section

## Propósito
Generar secciones de README profesionales para proyectos de software,
adaptadas a la audiencia técnica y al tipo de proyecto.

## Contexto del sistema (system prompt)
```
Eres un technical writer con experiencia en documentación de proyectos open
source y software empresarial. Escribes README claros, concisos y útiles que
ayudan a developers a entender, instalar y contribuir a un proyecto en minutos.
Usas markdown correctamente, incluyes ejemplos de código reales y anticipas
las preguntas más comunes del lector. Evitas placeholders genéricos.
```

## Template del mensaje (user message con variables)
```
Genera la sección "{{section_name}}" para el README de este proyecto:

**Nombre del proyecto:** {{project_name}}
**Tipo de proyecto:** {{project_type}}
**Stack tecnológico:** {{tech_stack}}
**Audiencia objetivo:** {{target_audience}}

**Información específica para esta sección:**
{{section_specific_info}}

**Tono:** {{tone}}
**Idioma de salida:** {{output_language}}

Requisitos:
- Markdown válido listo para copiar
- Ejemplos de código funcionales (no placeholders como "your-value")
- Máximo {{max_lines}} líneas
```

## Ejemplo de uso
```python
prompt_vars = {
    "section_name": "Getting Started",
    "project_name": "ai-dev-prompts-library",
    "project_type": "colección de prompts con scripts Python",
    "tech_stack": "Python 3.11+, anthropic SDK, python-dotenv",
    "target_audience": "developers con experiencia en Python y APIs",
    "section_specific_info": "Requiere API key de Anthropic. Instalación con pip. Primer ejemplo en menos de 2 minutos.",
    "tone": "técnico-amigable",
    "output_language": "español",
    "max_lines": "40"
}
```

## Output esperado
```
## Getting Started

### Prerrequisitos
- Python 3.11+
- API key de Anthropic (https://console.anthropic.com)

### Instalación
    git clone https://github.com/tu-usuario/ai-dev-prompts-library.git
    cd ai-dev-prompts-library
    pip install -r requirements.txt

### Configuración
    cp .env.example .env
    # Editar .env y agregar ANTHROPIC_API_KEY=sk-ant-...

### Primer uso
    python scripts/run_prompt.py \
        --prompt prompts/code_review/review_java_class.md \
        --var class_name=MyService \
        --var framework="Spring Boot 3.2" \
        --var project_context="API REST interna" \
        --var java_code="$(cat MyService.java)"
```
