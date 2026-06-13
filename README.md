# 🎯 UCISA - Plataforma Integral de Gestión y Reporteo Trimestral (REDECO/CONDUSEF)

Este sistema está diseñado para capturar reclamaciones y consultas financieras, validar contra catálogos oficiales y empaquetar de forma atómica y asíncrona lotes trimestrales en formato JSON listos para su envío al regulador.

## 🛠️ Stack Tecnológico Actualizado

* **Backend:** Python 3.12 + Django 6.0.x (Mapeo de base de datos relacional mediante Django ORM).
* **Base de Datos:** SQLite (`db.sqlite3`) cargada con datos de prueba estáticos para catálogos y socios.
* **Frontend:** Django Templates (SSR) + Bootstrap 5.3 (Componentes nativos y utilidades de diseño) + Bootstrap Icons.
* **Interactividad:** JavaScript nativo (Vanilla JS) para procesamiento dinámico en cliente y persistencia de datos.

## 🚀 Características Principales del MVP Actual (Core del Negocio)

* **Módulo de Captura de Quejas/Reclamaciones (Prioridad Alta):** Formulario dinámico para registrar consultas con validaciones estrictas en servidor y cliente (ej. la fecha de cierre es obligatoria si el estado es 'Concluido').
* **Lógica de Negocio - Folio Único Consecutivo:** Generación automática de identificadores irrepetibles con el formato regulatorio obligatorio `YYMMNN` (Año de 2 dígitos + Mes de 2 dígitos + Consecutivo mensual de 2 dígitos) para evitar colisiones con históricos.
* **Selector de Socios Interactivo:** Menú desplegable conectado a la base de datos de prueba que auto-completa la ubicación geográfica del socio (Estado, Municipio, Localidad) manteniendo los campos editables para correcciones en caliente.
* **Acuse de Recibo e Impresión de Tickets:** Pantalla de confirmación con vista de "Voucher Oficial" que integra un botón de impresión optimizado mediante CSS (`@media print`) para ocultar elementos de navegación y generar un PDF o ticket físico limpio.
* **Módulo de Cierre Trimestral y Generador JSON:** Panel de auditoría que lista y agrupa las quejas del trimestre (ej. Abril - Junio 2026), permitiendo una multi-selección mediante checkboxes para empaquetar y exportar los datos en un arreglo JSON estructurado para la CONDUSEF.
* **Soporte Global de Modo Oscuro:** Integración nativa mediante Bootstrap 5.3 con almacenamiento persistente en `localStorage` para mantener la preferencia del usuario en toda la sesión.

## 📂 Estructura del Proyecto

Archivos clave creados recientemente para soportar el flujo principal:

* `apps/consultas/forms.py` (Validación de capturas).
* `templates/consultas/captura_queja.html` (Formulario interactivo y modal de confirmación).
* `templates/consultas/ticket_queja.html` (Voucher imprimible estilizado).
* `templates/consultas/cierre_trimestral.html` (Tabla interactiva con multi-selector y exportador JSON).
* `seed_data.py` y `patch_causas.py` (Scripts de inicialización y parches de catálogos como el código 1211).

## 🏃‍♂️ Guía de Inicio Rápido (Cómo correr el proyecto)

Sigue estos comandos paso a paso para desplegar el entorno en otra máquina o revisar el avance:

1. **Clonar el repositorio y activar el entorno virtual:**
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Ejecutar las migraciones pendientes:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Poblar la base de datos con los datos genéricos de validación:**
   ```powershell
   python seed_data.py
   ```

4. **Iniciar el servidor local de desarrollo:**
   ```powershell
   python manage.py runserver
   ```
