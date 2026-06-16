# Frontend — Digital Content AI

Interfaz web del sistema de generación automática de contenido con IA, construida con **React 19**, **TypeScript** y **Vite** sobre **TanStack Start**.

---

## Tecnologías

- **TanStack Start** — routing y estructura full-stack.
- **React 19**.
- **TypeScript 5**.
- **Vite 8**.
- **Tailwind CSS v4**.
- **TanStack Router** — navegación.
- **TanStack Query** — gestión de estado remoto.
- **react-markdown** — previsualización de contenido Markdown.
- **axios** — llamadas HTTP al backend.
- **@tailwindcss/typography** — estilos para contenido renderizado.

---

## Requisitos previos

- Node.js 20 o superior, o Bun si vas a usar el flujo actual del proyecto.
- Backend corriendo en `http://localhost:8000` en local.
- Si ejecutas todo con Docker, el frontend debe apuntar al backend por nombre de servicio.

---

## Variables de entorno

### Desarrollo local

Crea el archivo `.env.local` en `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

### Docker

Si el frontend se ejecuta dentro de Docker Compose, usa:

```env
VITE_API_URL=http://backend:8000
```

---

## Instalación y arranque

1. Entra en la carpeta frontend:

```bash
cd frontend
```

2. Instala dependencias:

```bash
bun install
```

Si prefieres npm y tu proyecto ya lo soporta, puedes usar `npm install`, pero ahora mismo el flujo principal del repo está preparado para Bun.

3. Crea el archivo de variables de entorno:

```bash
cp .env.example .env.local
```

4. Arranca el servidor de desarrollo:

```bash
bun run dev
```

5. Abre la aplicación en:

```bash
http://localhost:3000
```

---

## Estructura

```text
frontend/
├── Dockerfile
├── .dockerignore
├── bun.lock
├── bunfig.toml
├── vite.config.ts
├── tsconfig.json
├── package.json
├── .env.example
└── src/
    ├── start.ts
    ├── server.ts
    ├── styles.css
    ├── router.tsx
    ├── routes/
    │   ├── index.tsx
    │   ├── generate.tsx
    │   ├── science.tsx
    │   ├── news.tsx
    │   ├── history.tsx
    │   └── profile.tsx
    ├── components/
    │   ├── generate/GenerateForm.tsx
    │   ├── science/ScienceForm.tsx
    │   ├── news/NewsSection.tsx
    │   ├── profile/ProfileForm.tsx
    │   ├── history/HistoryPanel.tsx
    │   ├── shared/ContentResult.tsx
    │   ├── shared/ErrorBanner.tsx
    │   └── layout/{Header.tsx,Footer.tsx}
    ├── services/
    │   └── api.ts
    ├── hooks/
    │   └── useHistory.ts
    ├── types/
    │   └── content.ts
    └── constants/
        ├── navigation.ts
        └── site.ts
```

---

## Funcionalidades

### Tab General
- Selección de plataforma: Blog, Twitter/X, LinkedIn, Instagram.
- Inputs de tema, audiencia y tono.
- Selector de idioma: Español, English, Français, Italiano.
- Selector de modelo: Groq o Ollama.
- Aviso de latencia cuando se selecciona Ollama.

### Tab Científico 🔬
- Generación de contenido divulgativo con RAG sobre papers de arXiv.
- Topics en inglés dan mejores resultados.
- Aviso de lentitud durante la generación.
- Contenido generado en el idioma seleccionado.

### Tab Noticias 📰
- Titulares financieros en tiempo real vía NewsAPI.
- Caché temporal para evitar demasiadas peticiones.
- Botón de actualización manual.
- Cada titular muestra título, descripción y enlace completo.
- Generación de contenido financiero basada en noticias reales.

### Perfil de empresa
- Formulario con nombre, sector, tono y descripción.
- Se persiste en el backend y se recupera al recargar.
- Se usa como contexto en las generaciones.
- Muestra badges cuando hay perfil activo.

### Resultado
- Imagen relevante encima del contenido cuando existe.
- Dos vistas: **Raw** y **Preview**.
- Botón para copiar al portapapeles.
- Skeleton loader durante la generación.

### Historial 🕓
- Lista de generaciones guardadas.
- Cada registro es expandible y muestra metadatos y contenido.
- Botón para eliminar cada entrada.
- Actualización automática tras nuevas generaciones.

---

## Scripts disponibles

```bash
bun run dev      # Servidor de desarrollo
bun run build    # Build de producción
bun run preview  # Vista previa del build
bun run lint     # Linter
bun run format   # Formateo con Prettier
```

Si tu `package.json` tiene también scripts equivalentes en npm, puedes documentarlos, pero el proyecto que mostraste está claramente orientado a Bun.

---

## Docker

```bash
# Desde la raíz del proyecto
docker compose up --build
```

El frontend arranca en `http://localhost:3000` y se comunica con el backend por nombre de servicio Docker cuando se ejecuta dentro del compose.

---

## Notas de despliegue

- En local, `VITE_API_URL` debe apuntar a `http://localhost:8000`.
- En Docker Compose, el frontend debe usar `http://backend:8000`.
- Si el backend usa Ollama en local desde Docker, la URL del backend para Ollama debe apuntar correctamente al host.