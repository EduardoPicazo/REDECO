# Sistema Redeco - Plataforma de Gestión y Reporteo Trimestral (CONDUSEF)

Análisis, modelado e implementación de un sistema web integral de gestión y automatización de reportes trimestrales de consultas para la plataforma Redeco. El sistema centraliza la administración de socios, automatiza la validación de catálogos oficiales de SEPOMEX, gestiona esquemas dinámicos de autenticación por token y configura una pasarela de comunicación asíncrona con los endpoints de CONDUSEF, garantizando transacciones atómicas seguras y trazables.

---

## 📊 Arquitectura del Sistema

El sistema se diseñó bajo un enfoque desacoplado de tres capas, garantizando la separación de responsabilidades y la integridad transaccional:

- **Frontend (Presentación):** React.js 18 (TypeScript) + Vite + Tailwind CSS. Diseñado como una Single Page Application (SPA) responsiva y reactiva.
- **Backend (Lógica de Negocio):** Node.js + NestJS Framework. Implementa controladores REST estructurados, interceptores de seguridad globales y servicios asíncronos orientados a eventos.
- **Base de Datos (Persistencia):** MySQL 8.0 operando bajo el motor transaccional InnoDB con un nivel de aislamiento `SERIALIZABLE` para evitar colisiones de folios.

---

## 🗄️ Modelo de Datos (Esquema Relacional)

El sistema cuenta con un motor relacional sólido que asegura la consistencia ACID. A continuación se detalla la estructura base de las tablas principales:

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
├── backend/                  # Código fuente del Servidor (NestJS)
│   ├── src/
│   │   ├── auth/             # Gestión de seguridad y JWT externo
│   │   ├── socios/           # Módulo core de administración de socios
│   │   ├── consultas/        # Lógica de folios y temporalidad fiscal
│   │   ├── envios/           # Serializador y cliente HTTP para CONDUSEF
│   │   └── database/         # Migraciones, entities (TypeORM) y seeds
│   ├── test/                 # Pruebas unitarias y de integración (Jest)
│   └── .env.example          # Plantilla de configuración ambiental
├── frontend/                 # Código fuente del Cliente (React.js)
│   ├── src/
│   │   ├── components/       # Componentes UX/UI (Consola de Errores, Tablas)
│   │   ├── views/            # Pantallas (Login, Alta Socio, Despacho)
│   │   ├── services/         # Clientes de API (Axios Interceptors)
│   │   └── hooks/            # Hooks personalizados para estado global
│   └── vite.config.ts        # Configuración del empaquetador
└── README.md                 # El archivo que estás leyendo

## 📦 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO
