# Sistema Redeco - Plataforma de Gestión y Reporteo Trimestral (CONDUSEF)

Análisis, modelado e implementación de un sistema web integral de gestión y automatización de reportes trimestrales de consultas para la plataforma Redeco. El sistema centraliza la administración de socios, automatiza la validación de catálogos oficiales de SEPOMEX, gestiona esquemas dinámicos de autenticación por token y configura una pasarela de comunicación asíncrona con los endpoints de CONDUSEF, garantizando transacciones atómicas seguras y trazables.

---

## 📊 Arquitectura del Sistema

El sistema se diseñó bajo un enfoque desacoplado de tres capas, garantizando la separación de responsabilidades y la integridad transaccional:

- **Frontend (Presentación):** React.js 18 (TypeScript) + Vite + Tailwind CSS. Diseñado como una Single Page Application (SPA) responsiva y reactiva.
- **Backend (Lógica de Negocio):** Python 3.x + Django Framework + Django REST Framework (DRF). Implementa vistas de API estructuradas (APIViews), serializadores robustos, middlewares de seguridad globales y servicios asíncronos orientados a eventos utilizando `requests` o `httpx`.
- **Base de Datos (Persistencia):** MySQL 8.0 operando bajo el motor transaccional InnoDB con un nivel de aislamiento `SERIALIZABLE` gestionado mediante el ORM de Django (`select_for_update`) para evitar colisiones de folios.

---

## 🗄️ Modelo de Datos (Esquema Relacional)

El sistema cuenta con un motor relacional sólido que asegura la consistencia ACID. A continuación se detalla la estructura base de las tablas principales gestionadas por los modelos de Django:

- `socios`: Indexada mediante el RFC como clave unívoca. Vinculada obligatoriamente al catálogo SEPOMEX.
- `consultas`: Registra las reclamaciones utilizando un Folio Único Temporal (`YYMMXXXX`) calculado síncronamente.
- `productos` y `causas`: Catálogos maestros jerárquicos oficiales de la CONDUSEF.
- `tokens`: Almacenamiento seguro y temporal del ciclo de vida de los tokens JWT externos.
- `envios` y `detalle_envio`: Entidades históricas inmutables que registran los lotes aceptados por el regulador.
- `bitacora`: Registro transaccional inmutable en formato JSON para auditoría de acciones críticas (altas, modificaciones y cancelaciones lógicas).

---

## 🌐 API REST Endpoints

La comunicación entre el cliente y el servidor se realiza mediante una interfaz síncrona y semántica. Los endpoints principales son:

### Autenticación
- `POST /api/auth/token` -> Solicita/renueva el token JWT institucional de CONDUSEF.

### Módulo de Socios
- `GET /api/socios?busqueda={query}` -> Búsqueda predictiva de socios.
- `POST /api/socios` -> Alta de nuevo socio (Valida Código Postal contra SEPOMEX local).
- `PUT /api/socios/{rfc}` -> Modificación de datos domiciliarios (Bloqueado si tiene históricos).

### Módulo de Consultas
- `GET /api/consultas?trimestre={Q}&anio={YYYY}` -> Listado filtrado por periodo.
- `POST /api/consultas` -> Registra queja, calcula el trimestre y asigna folio `YYMMXXXX`.
- `PATCH /api/consultas/{id}/cancelar` -> Cancelación lógica (desestimación de folio).

### Módulo de Despacho (Pasarela Regular)
- `POST /api/envios` -> Transmite el lote JSON seleccionado bajo la política atómica de *Todo o Nada*.

---

## 📂 Estructura del Proyecto (Directory Tree)

```text
redeco-condusef/
├── NE_REDECO/                # Directorio raíz del proyecto Django Backend
│   ├── NE_REDECO/            # Configuración global del proyecto (settings, urls, wsgi)
│   │   ├── __init__.py
│   │   ├── settings.py       # Configuración de BD MySQL y Apps instaladas
│   │   └── urls.py           # Enrutador global de la API
│   ├── apps/                 # Aplicaciones modulares de Django
│   │   ├── auth_condusef/    # Gestión de seguridad y JWT externo
│   │   ├── socios/           # Módulo de administración de socios y SEPOMEX
│   │   ├── consultas/        # Lógica de folios únicos y temporalidad
│   │   └── envios/           # Serializadores y despacho HTTP a CONDUSEF
│   ├── data/                 # Catálogos maestros en bruto (Excel/CSV de profesores)
│   ├── manage.py             # Utilidad de comandos de Django
│   └── requirements.txt      # Dependencias del proyecto Python
├── frontend/                 # Código fuente del Cliente (React.js)
│   ├── src/
│   │   ├── components/       # Componentes UX/UI (Consola de Errores, Tablas)
│   │   ├── views/            # Pantallas (Login, Alta Socio, Despacho)
│   │   ├── services/         # Clientes de API (Axios Interceptors)
│   │   └── hooks/            # Hooks personalizados para estado global
│   └── vite.config.ts        # Configuración del empaquetador
└── README.md                 # El archivo que estás leyendo

## 📦 Instalación y Configuración

Sigue estos pasos para levantar el proyecto en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/EduardoPicazo/REDECO.git
cd REDECO-1
```

### 2. 🚀 Inicialización del Proyecto
Enciende el entorno virtual interno para cargar todas las dependencias (como Django y Pandas):
```bash
.\NE_REDECO\venv\Scripts\activate
```

### 3. 📦 Base de Datos y Migraciones
Posiciónate en el directorio de Django y estructura las tablas (MySQL/SQLite) mediante:
```bash
cd NE_REDECO
python manage.py migrate
```

### 4. ⚡ Carga Masiva de Catálogos (CONDUSEF y SEPOMEX)
Ejecuta nuestro comando personalizado de optimización para poblar la base de datos:
```bash
python manage.py cargar_catalogos
```
*Nota de rendimiento:* Este script procesa **más de 150,000 registros en segundos** trabajando directamente en la memoria RAM de manera atómica, logrando así evitar cualquier cuello de botella por escrituras excesivas en el disco.

### 5. 🖥️ Ver la Demo de Búsqueda (MVP)
Levanta el servidor local de desarrollo:
```bash
python manage.py runserver
```
Abre tu navegador y dirígete a:
**[http://127.0.0.1:8000/demo/](http://127.0.0.1:8000/demo/)**

Ahí podrás interactuar con el MVP funcional y rápido, con una interfaz basada en la identidad visual de UCISA.

---

## 🐳 Despliegue con Docker (Recomendado)

Para evitar configuraciones locales complejas de Python y garantizar la ejecucion de la misma versión del código y base de datos con las dependencias exactas, este proyecto cuenta con --
**Dockerización completa**.

### Requisitos Previos
- Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/) en tu máquina.

### Levantar el Proyecto con un Solo Comando
Abre tu terminal en la raíz del proyecto (`REDECO-1`) y ejecuta:
```bash
docker compose up --build
```
Este comando automáticamente:
1. Descargará un sistema optimizado ligero (`python:3.12-slim`).
2. Instalará internamente todas las dependencias exactas (Django, Pandas, Openpyxl, Gunicorn, etc.).
3. Ejecutará las migraciones.
4. Montará de forma inteligente tu archivo `db.sqlite3` local (vía volúmenes) para que los más de 150,000 registros y la base de datos persistan sin borrarse al apagar el contenedor.
5. Encenderá el servidor de producción **Gunicorn** en el puerto `8000`.

Una vez que la terminal indique que está escuchando conexiones, entra a **[http://127.0.0.1:8000/demo/](http://127.0.0.1:8000/demo/)** para interactuar de inmediato con el sistema.
