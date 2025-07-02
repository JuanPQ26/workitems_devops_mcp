# WorkItems DevOps MCP Server

Un servidor **Model Context Protocol (MCP)** que proporciona herramientas para interactuar con **Azure DevOps Work Items** desde aplicaciones de IA/LLM.

## 🎯 Propósito

Este proyecto permite que modelos de lenguaje (LLMs) y aplicaciones de IA interactúen directamente con Azure DevOps para:
- Consultar work items asignados al usuario
- Filtrar work items por criterios específicos
- Obtener detalles completos de work items
- Gestionar tipos de work items y sus estados
- Actualizar estados de work items

## 🏗️ Arquitectura

```
workitems_devops_mcp/
├── server.py              # Servidor MCP con herramientas expuestas
├── main.py                # Punto de entrada principal
├── settings.py            # Configuración y variables de entorno
├── services/
│   └── workitems.py       # Lógica de negocio para Azure DevOps API
└── utils/
    ├── http_client.py     # Cliente HTTP para Azure DevOps
    └── formatters.py      # Formateadores de respuestas
```

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.13+
- Cuenta de Azure DevOps con acceso al proyecto
- Personal Access Token (PAT) de Azure DevOps

### 1. Instalación

```bash
# Clonar el repositorio
git clone <tu-repo>
cd workitems_devops_mcp

# Instalar dependencias
uv sync
```

### 2. Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
AZURE_DEVOPS_ACCESS_TOKEN=tu_personal_access_token
AZURE_DEVOPS_PROJECT=nombre_del_proyecto
AZURE_DEVOPS_ORGANIZATION=nombre_de_la_organizacion
```

### 3. Ejecución

```bash
# Ejecutar el servidor MCP
python server.py

# O ejecutar el main básico
python main.py
```

## 🛠️ Herramientas Disponibles

El servidor MCP expone las siguientes herramientas:

### 📋 Consulta de Work Items

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `get_workitems_ids_assigned_to_user` | Obtiene IDs de work items asignados al usuario | Ninguno |
| `get_workitems_ids_assigned_to_user_by` | Filtra work items por criterios personalizados | `columns_where: str` |
| `get_workitems_ids_assigned_to_user_by_planned_date` | Filtra por fecha de inicio planeada | `planned_date: str` |
| `get_workitems_details_by_ids` | Obtiene detalles completos de work items | `workitems_ids: str` |

### 📊 Gestión de Tipos y Estados

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `get_all_workitems_types` | Lista todos los tipos de work items | Ninguno |
| `get_workitem_type_by_name` | Obtiene un tipo específico por nombre | `name: str` |
| `get_workitem_type_states` | Lista estados de un tipo de work item | `workitem_type_name: str` |
| `get_workitem_transitions_allowed` | Obtiene transiciones permitidas | `workitem_type_name: str`, `workitem_state_name: str` |

### ✏️ Actualización

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `update_workitem_state` | Actualiza el estado de un work item | `workitem_id: str`, `workitem_state_name: str` |

## 💡 Ejemplos de Uso

### Ejemplo 1: Obtener work items del día
```python
# Usar la herramienta con fecha específica
get_workitems_ids_assigned_to_user_by_planned_date("2025-01-02")
# Resultado: "Workitems ids found: 12345,67890"
```

### Ejemplo 2: Filtrar por criterios personalizados
```python
# Filtrar por título y prioridad
get_workitems_ids_assigned_to_user_by("System.Title CONTAINS 'Backend' AND Microsoft.VSTS.Common.Priority = 1")
```

### Ejemplo 3: Obtener detalles completos
```python
# Obtener detalles de múltiples work items
get_workitems_details_by_ids("12345,67890")
```

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `AZURE_DEVOPS_ACCESS_TOKEN` | Token de acceso personal | `ghp_xxxxxxxxxxxxxxxxxxxx` |
| `AZURE_DEVOPS_PROJECT` | Nombre del proyecto | `MiProyecto` |
| `AZURE_DEVOPS_ORGANIZATION` | Nombre de la organización | `miempresa` |

### Configuración de API
- **Versión de API**: 7.0 (configurable en `settings.py`)
- **User-Agent**: `workitems-devops-mcp/1.0`
- **Autenticación**: Basic Auth con PAT

## 🏃‍♂️ Desarrollo

### Estructura del Código

#### `server.py`
- Define las herramientas MCP usando decoradores `@mcp.tool`
- Maneja la lógica de presentación y formateo de respuestas
- Punto de entrada para el servidor MCP

#### `services/workitems.py`
- Contiene toda la lógica de negocio para Azure DevOps API
- Funciones para consultas WIQL (Work Item Query Language)
- Gestión de tipos, estados y transiciones

#### `utils/http_client.py`
- Cliente HTTP asíncrono usando `httpx`
- Maneja autenticación y headers
- Métodos para GET, POST y PATCH

#### `utils/formatters.py`
- Formatea respuestas para presentación en español
- Convierte datos de API a formato legible
- Maneja fechas, esfuerzo y estados

### Agregar Nuevas Herramientas

1. **Definir función en `services/workitems.py`**:
```python
async def mi_nueva_funcion(parametro: str) -> dict:
    # Lógica de negocio
    return resultado
```

2. **Exponer como herramienta MCP en `server.py`**:
```python
@mcp.tool("mi_nueva_herramienta")
async def mi_nueva_herramienta(parametro: str):
    """Descripción de la herramienta"""
    resultado = await workitems.mi_nueva_funcion(parametro)
    return formato_resultado(resultado)
```

## 📦 Dependencias

```toml
dependencies = [
    "httpx>=0.28.1",        # Cliente HTTP asíncrono
    "mcp[cli]>=1.10.1",     # Model Context Protocol
    "pydantic-settings>=2.10.1",  # Gestión de configuración
    "python-dotenv>=1.1.1", # Variables de entorno
]
```

## 🤝 Integración con Aplicaciones IA

Este servidor MCP puede integrarse con:
- **Claude Desktop**: Agregar como servidor MCP en configuración
- **Aplicaciones personales**: Usar como cliente MCP
- **Pipelines CI/CD**: Automatización de work items
- **Chatbots**: Consulta y actualización de work items

### Ejemplo de configuración para Claude Desktop:
```json
{
  "mcpServers": {
    "workitems-devops": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "AZURE_DEVOPS_ACCESS_TOKEN": "tu_token"
      }
    }
  }
}
```

## 🚨 Consideraciones de Seguridad

- ⚠️ **Nunca commitear tokens**: Usar siempre variables de entorno
- 🔒 **Tokens con permisos mínimos**: Solo Work Items (lectura/escritura)
- 🕐 **Rotación de tokens**: Renovar PATs periódicamente
- 📝 **Logs**: No loggear información sensible

## 🐛 Solución de Problemas

### Error: "Workitems not found"
- Verificar IDs de work items válidos
- Confirmar permisos en Azure DevOps

### Error de autenticación
- Validar PAT en Azure DevOps
- Verificar variables de entorno

### Error de conexión
- Confirmar URL de organización/proyecto
- Verificar conectividad de red

---

**Desarrollado con ❤️ para integración Azure DevOps + IA**

## 📚 Guía Paso a Paso para Desarrolladores

### Paso 1: Configuración Inicial
```bash
# 1. Clonar y navegar al proyecto
git clone <tu-repositorio>
cd workitems_devops_mcp

# 2. Crear entorno virtual y activar
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
uv sync
# o si no tienes uv:
pip install -r requirements.txt
```

### Paso 2: Configuración Azure DevOps
```bash
# 1. Crear archivo .env
touch .env

# 2. Agregar configuración (editar con tu editor favorito)
echo "AZURE_DEVOPS_ACCESS_TOKEN=tu_token_aqui" >> .env
echo "AZURE_DEVOPS_PROJECT=tu_proyecto" >> .env
echo "AZURE_DEVOPS_ORGANIZATION=tu_organizacion" >> .env
```

### Paso 3: Verificar Conexión
```bash
# Ejecutar servidor para probar
python server.py
```

### Paso 4: Integración con Cliente IA

#### Para Claude Desktop:
```json
// Agregar a ~/.config/claude/claude_desktop_config.json
{
  "mcpServers": {
    "workitems-devops": {
      "command": "python",
      "args": ["/ruta/completa/al/servidor/server.py"],
      "env": {
        "AZURE_DEVOPS_ACCESS_TOKEN": "tu_token",
        "AZURE_DEVOPS_PROJECT": "tu_proyecto", 
        "AZURE_DEVOPS_ORGANIZATION": "tu_organizacion"
      }
    }
  }
}
```

#### Para Desarrollo Personalizado:
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env={
            "AZURE_DEVOPS_ACCESS_TOKEN": "tu_token",
            # ... más variables
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Usar herramientas MCP
            result = await session.call_tool(
                "get_workitems_ids_assigned_to_user", 
                {}
            )
            print(result)

asyncio.run(main())
```

### Paso 5: Casos de Uso Comunes

#### Caso 1: Consulta Matutina de Work Items
```python
# 1. Obtener work items del día
work_items = get_workitems_ids_assigned_to_user_by_planned_date("2025-01-02")

# 2. Obtener detalles
details = get_workitems_details_by_ids(work_items)
```

#### Caso 2: Gestión de Estados
```python
# 1. Verificar estados disponibles
states = get_workitem_type_states("Task")

# 2. Verificar transiciones permitidas  
transitions = get_workitem_transitions_allowed("Task", "To Do")

# 3. Actualizar estado
update_workitem_state("12345", "In Progress")
```

#### Caso 3: Filtros Avanzados
```python
# Filtrar por múltiples criterios
filtered = get_workitems_ids_assigned_to_user_by(
    "System.WorkItemType = 'Bug' AND Microsoft.VSTS.Common.Priority <= 2"
)
```

### Paso 6: Personalización y Extensión

#### Agregar Nueva Herramienta:

1. **Definir en `services/workitems.py`**:
```python
async def get_workitems_by_sprint(sprint_name: str) -> list[str]:
    """Nueva función para obtener work items por sprint"""
    # Implementación
    pass
```

2. **Exponer en `server.py`**:
```python
@mcp.tool("get_workitems_by_sprint")
async def get_workitems_by_sprint(sprint_name: str):
    """Obtiene work items de un sprint específico"""
    result = await workitems.get_workitems_by_sprint(sprint_name)
    return format_result(result)
```

#### Modificar Formateo:

Editar `utils/formatters.py` para cambiar cómo se presentan los datos:
```python
def format_workitem(workitem: dict) -> str:
    # Personalizar formato de salida
    return f"Mi formato personalizado: {workitem}"
```

### Paso 7: Testing y Debugging

#### Probar Herramientas Manualmente:
```python
# Crear script de prueba
import asyncio
from services.workitems import get_workitems_ids_assigned_to_user

async def test():
    result = await get_workitems_ids_assigned_to_user()
    print(f"Work items encontrados: {result}")

asyncio.run(test())
```

#### Debug con Logs:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Agregar logs en tus funciones
logger.debug(f"Calling Azure DevOps API: {url}")
```

### Paso 8: Despliegue

#### Para Uso Local:
```bash
# Ejecutar servidor en background
nohup python server.py &
```

#### Para Contenedor Docker:
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["python", "server.py"]
```

```bash
# Build y run
docker build -t workitems-mcp .
docker run -d --env-file .env workitems-mcp
```

#### Para Servidor:
```bash
# Usando systemd (Linux)
sudo tee /etc/systemd/system/workitems-mcp.service << EOF
[Unit]
Description=WorkItems MCP Server
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/al/proyecto
ExecStart=/ruta/al/venv/bin/python server.py
EnvironmentFile=/ruta/al/.env
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable workitems-mcp
sudo systemctl start workitems-mcp
```

### 🎯 Tips para Desarrolladores

1. **Usa el entorno correcto**: Siempre activa el venv antes de trabajar
2. **Variables de entorno**: Nunca hardcodees tokens en el código
3. **Manejo de errores**: Azure DevOps puede devolver diferentes códigos de error
4. **Rate limiting**: Considera implementar rate limiting para evitar excesos
5. **Caching**: Para consultas frecuentes, considera implementar cache
6. **Logging**: Usa logs para debugging, pero no loggees información sensible
7. **Testing**: Crea tests unitarios para tus nuevas funcionalidades

### 🔗 Recursos Útiles

- [Azure DevOps REST API](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- [Model Context Protocol Docs](https://modelcontextprotocol.io/)
- [WIQL Reference](https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax)
- [FastMCP Documentation](https://github.com/pydantic/fastmcp)
