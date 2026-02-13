<div align="center">

# Módulo Registro Seguro

</div>


<div align="center">

**Sistema de Gestión de Usuarios**  
Desarrollado para la materia de Seguridad de Desarrollo de Aplicaciones

</div>

---

## Descripción del Proyecto

Este sistema de gestión de usuarios implementa un flujo de registro seguro utilizando **FastAPI** y **Python 3.14**, incorporando el algoritmo de hashing **bcrypt** para la protección robusta de credenciales de usuario.

---

## Colaboradores

<table>
  <tr>
    <td><strong>Fausto Javier Mendoza Pérez</strong></td>
  </tr>
  <tr>
    <td><strong>Edna Fabiola Cervantes Burgos</strong></td>
  </tr>
</table>

**Materia:** Seguridad de Desarrollo de Aplicaciones

---

## Instalación y Configuración

### Requisitos Previos

- Python 3.14 instalado en el sistema
- pip (gestor de paquetes de Python)

### Pasos de Instalación

**1. Crear el entorno virtual**

```bash
py -3.14 -m venv .venv
```

**2. Activar el entorno virtual**

- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

- **Unix/MacOS:**
  ```bash
  source .venv/bin/activate
  ```

**3. Instalar las dependencias necesarias**

```bash
pip install -r requirements.txt
```

---

## Esquema de la Base de Datos

El sistema utiliza **SQLite** para el almacenamiento de información. La estructura de la tabla de usuarios se define mediante la siguiente consulta SQL:

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email TEXT NOT NULL UNIQUE, 
    password TEXT NOT NULL, 
    role TEXT DEFAULT 'cliente'
);
```

### Descripción de Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | Identificador único autoincremental |
| `email` | TEXT | Correo electrónico del usuario (único) |
| `password` | TEXT | Contraseña hasheada con bcrypt |
| `role` | TEXT | Rol del usuario (valor por defecto: 'cliente') |

---

## Documentación de la API

### Registro de Usuario

<table>
  <tr>
    <td><strong>Endpoint</strong></td>
    <td><code>POST /api/v1/registro</code></td>
  </tr>
  <tr>
    <td><strong>Descripción</strong></td>
    <td>Registra un nuevo usuario en el sistema. La contraseña recibida es procesada mediante bcrypt antes de ser almacenada en la base de datos para garantizar que no se guarde en texto plano.</td>
  </tr>
</table>

#### Estructura del Request Body (JSON)

```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "rol": "string"
}
```

---

## Implementación de Seguridad

El sistema incorpora múltiples capas de seguridad para proteger la información de los usuarios:

<dl>
  <dt><strong>Hashing con Bcrypt</strong></dt>
  <dd>Se utiliza para transformar las contraseñas en hashes irreversibles, protegiendo la información ante posibles accesos no autorizados a la base de datos.</dd>
  
  <dt><strong>Validación de Datos</strong></dt>
  <dd>Uso de esquemas de Pydantic para asegurar la integridad de los datos de entrada y prevenir inyecciones maliciosas.</dd>
  
  <dt><strong>Restricciones de Base de Datos</strong></dt>
  <dd>Implementación de campos UNIQUE para evitar la duplicidad de registros de correo electrónico.</dd>
</dl>

---

## Ejecución

Para iniciar el servidor de desarrollo, ejecute el siguiente comando:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

### Documentación Interactiva

Una vez iniciado el servidor, puede acceder a la documentación interactiva de la API en:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

<div align="center">

**Proyecto Académico** | Seguridad de Desarrollo de Aplicaciones

</div>