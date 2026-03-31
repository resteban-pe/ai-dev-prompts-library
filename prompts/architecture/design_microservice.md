# Design Microservice

## Propósito
Diseñar la arquitectura de un microservicio desde cero: responsabilidades,
APIs, modelo de datos, comunicación con otros servicios y decisiones clave (ADR).

## Contexto del sistema (system prompt)
```
Eres un arquitecto de soluciones con experiencia en sistemas distribuidos y
microservicios a escala. Diseñas servicios con bounded contexts claros (DDD),
contratos de API estables y resiliencia ante fallos. Produces decisiones
arquitectónicas justificadas (ADRs) y diagramas en formato Mermaid.
Cada decisión incluye alternativas descartadas y consecuencias.
```

## Template del mensaje (user message con variables)
```
Diseña la arquitectura del siguiente microservicio:

**Nombre del servicio:** {{service_name}}
**Sistema padre:** {{parent_system}}
**Responsabilidad principal:** {{responsibility}}

**Servicios con los que interactúa:**
{{service_interactions}}

**Requisitos no funcionales:**
- Throughput esperado: {{throughput}}
- SLA de disponibilidad: {{sla}}
- {{other_nfr}}

**Restricciones tecnológicas:** {{tech_constraints}}

Diseña e incluye:
1. Bounded context: qué hace y qué NO hace este servicio
2. API REST: endpoints principales con método, path y payload de ejemplo
3. Modelo de datos: entidades clave y relaciones
4. Comunicación: síncrona (REST) vs asíncrona (eventos) con justificación
5. Diagrama de componentes en Mermaid (formato texto)
6. Riesgos identificados y mitigaciones
7. ADR-001: decisión arquitectónica más importante con alternativas descartadas
```

## Ejemplo de uso
```python
prompt_vars = {
    "service_name": "notification-service",
    "parent_system": "plataforma e-commerce con 8 microservicios",
    "responsibility": "envío de notificaciones multicanal (email, SMS, push)",
    "service_interactions": "- order-service: consume eventos OrderCreated, OrderShipped\n- user-service: consulta preferencias del usuario",
    "throughput": "500 notificaciones/minuto en peak",
    "sla": "99.5%",
    "other_nfr": "Idempotencia garantizada ante reintentos",
    "tech_constraints": "AWS, Spring Boot 3.x, PostgreSQL disponible"
}
```

## Output esperado
```
## Arquitectura: notification-service

### Bounded Context
Responsable de: despacho de notificaciones y tracking de entrega.
NO responsable de: lógica de negocio de órdenes, templates de marketing.

### API REST
POST /api/v1/notifications        — envío directo (uso interno)
GET  /api/v1/notifications/{id}   — estado de una notificación
GET  /api/v1/notifications?userId — historial por usuario

### Diagrama Mermaid
graph LR
  order-service -->|OrderCreated| notification-service
  notification-service --> EmailProvider
  notification-service --> SMSProvider
  notification-service --> PushProvider

### ADR-001: Comunicación asíncrona via eventos Kafka
Decisión: consumir eventos en lugar de REST síncrono.
Alternativas descartadas: REST polling (acoplamiento), webhooks (complejidad).
Consecuencias: requiere idempotencia con event-id único en cada mensaje.
```
