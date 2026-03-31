# Review Java Class

## Propósito
Analizar una clase Java en busca de problemas de diseño, bugs potenciales, 
violaciones de principios SOLID y oportunidades de mejora de rendimiento.

## Contexto del sistema (system prompt)
```
Eres un senior Java developer con 10+ años de experiencia en sistemas 
empresariales. Revisas código con enfoque en: correctitud, mantenibilidad, 
rendimiento y adherencia a principios SOLID. Tu respuesta es directa, técnica 
y accionable. Estructuras el feedback en secciones claras con severidad 
(CRÍTICO / ADVERTENCIA / SUGERENCIA).
```

## Template del mensaje (user message con variables)
```
Revisa la siguiente clase Java y proporciona feedback detallado:

**Clase:** {{class_name}}
**Contexto del proyecto:** {{project_context}}
**Stack/Framework:** {{framework}} (e.g., Spring Boot 3.x, Jakarta EE)

```java
{{java_code}}
```

Evalúa los siguientes aspectos:
1. Principios SOLID (identifica violaciones específicas)
2. Manejo de excepciones y casos borde
3. Thread-safety y concurrencia (si aplica)
4. Oportunidades de optimización
5. Cobertura de tests sugerida (casos unitarios clave)

Formato de respuesta: usa severidad [CRÍTICO], [ADVERTENCIA], [SUGERENCIA].
```

## Ejemplo de uso
```python
# scripts/run_prompt.py
prompt_vars = {
    "class_name": "UserService",
    "project_context": "API REST de e-commerce, ~50k usuarios activos",
    "framework": "Spring Boot 3.2",
    "java_code": open("UserService.java").read()
}
```

## Output esperado
```
## Revisión de UserService.java

### [CRÍTICO] Violación de Single Responsibility Principle
La clase maneja autenticación, lógica de negocio y acceso a datos...

### [ADVERTENCIA] Posible NullPointerException en línea 47
El método `findByEmail()` puede retornar null sin verificación...

### [SUGERENCIA] Extraer constantes de configuración
Los valores hardcodeados en líneas 23, 45 deberían moverse a...

### Tests sugeridos
- `shouldThrowExceptionWhenEmailNotFound()`
- `shouldReturnUserWhenValidCredentials()`
```
