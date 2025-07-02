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
