# Generate Spring Service

## Propósito
Generar un servicio Spring Boot completo con su interfaz, implementación,
manejo de excepciones y tests unitarios, a partir de una descripción funcional.

## Contexto del sistema (system prompt)
```
Eres un arquitecto de software especializado en Spring Boot 3.x y Java 17+.
Generas código production-ready que sigue convenciones de Spring, usa inyección
de dependencias por constructor, manejo adecuado de excepciones personalizadas
y está listo para ser testeado con JUnit 5 + Mockito. Incluyes anotaciones
Javadoc en métodos públicos.
```

## Template del mensaje (user message con variables)
```
Genera un servicio Spring Boot completo para el siguiente caso de uso:

**Nombre del servicio:** {{service_name}}
**Dominio/entidad principal:** {{entity_name}}
**Descripción funcional:** {{functional_description}}

**Operaciones requeridas:**
{{operations_list}}

**Dependencias disponibles:**
- Spring Data JPA con repositorio: {{repository_name}}
- {{additional_dependencies}}

**Reglas de negocio:**
{{business_rules}}

Genera en este orden:
1. Interfaz {{service_name}} con Javadoc en cada método
2. Implementación {{service_name}}Impl con @Service
3. Excepción personalizada si aplica
4. Test unitario con JUnit 5 + Mockito (happy path y caso de error)
```

## Ejemplo de uso
```python
prompt_vars = {
    "service_name": "OrderService",
    "entity_name": "Order",
    "functional_description": "Gestión del ciclo de vida de órdenes de compra",
    "operations_list": "- createOrder(orderRequest)\n- cancelOrder(orderId)\n- getOrdersByUser(userId)",
    "repository_name": "OrderRepository",
    "additional_dependencies": "UserService, InventoryService",
    "business_rules": "- No cancelar ordenes con estado SHIPPED\n- Verificar stock antes de crear"
}
```

## Output esperado
```
// OrderService.java
public interface OrderService {
    /** Crea una orden. @throws InsufficientStockException si no hay stock */
    OrderResponse createOrder(OrderRequest request);
    void cancelOrder(Long orderId);
    List<OrderResponse> getOrdersByUser(Long userId);
}

// OrderServiceImpl.java
@Service
@RequiredArgsConstructor
public class OrderServiceImpl implements OrderService {
    private final OrderRepository orderRepository;
    private final UserService userService;
    private final InventoryService inventoryService;
    ...
}

// OrderServiceTest.java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock private OrderRepository orderRepository;
    @InjectMocks private OrderServiceImpl orderService;

    @Test void shouldCreateOrderWhenStockAvailable() { ... }
    @Test void shouldThrowWhenStockInsufficient() { ... }
}
```
