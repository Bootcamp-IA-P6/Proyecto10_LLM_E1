# Frontend — Digital Content AI

Interfaz web del sistema de generación automática de contenido con IA, construida con Next.js 15, TypeScript y Tailwind CSS.

---

## Tecnologías

- **Next.js 15** — App Router
- **TypeScript 5**
- **Tailwind CSS v4**
- **react-markdown** — previsualización de contenido Markdown
- **@tailwindcss/typography** — estilos para contenido renderizado
- **axios** — llamadas HTTP al backend

---

## Requisitos previos

- Node.js 20 o superior
- npm 10 o superior
- Backend corriendo en `http://localhost:8000`

---

## Instalación y arranque

1. Entra en la carpeta frontend:
```bash
cd frontend
```

2. Instala las dependencias:
```bash
npm install
```

3. Crea el archivo de variables de entorno:
```bash
cp .env.example .env.local
```

El archivo `.env.example` contiene:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Arranca el servidor de desarrollo:
```bash
npm run dev
```

5. Abre la aplicación en:
```
http://localhost:3000
```

---

## Estructura

```
frontend/
├── Dockerfile                   # Build standalone con node:20-alpine
├── .dockerignore
├── next.config.ts               # output: standalone para Docker
├── src/
│   ├── app/
│   │   ├── globals.css          # Estilos globales + @plugin typography
│   │   ├── layout.tsx           # Layout raíz
│   │   └── page.tsx             # Página principal con tabs y estado global
│   ├── components/
│   │   ├── GenerateForm.tsx     # Formulario general con selector LLM
│   │   ├── ContentResult.tsx    # Resultado con imagen, tabs Raw/Preview
│   │   ├── ProfileForm.tsx      # Perfil de empresa con carga y guardado
│   │   ├── ScienceForm.tsx      # Formulario RAG científico
│   │   ├── NewsSection.tsx      # Titulares financieros + generación
│   │   └── HistoryPanel.tsx     # Historial de generaciones
│   ├── services/
│   │   └── api.ts               # Todas las llamadas HTTP al backend
│   └── types/
│       └── content.ts           # Tipos TypeScript compartidos
├── .env.example
├── package.json
└── tsconfig.json
```

---

## Funcionalidades

### Tab General
- Selección de plataforma: Blog, Twitter/X, LinkedIn, Instagram
- Inputs de tema, audiencia y tono
- Selector de idioma: Español, English, Français, Italiano
- Selector de LLM: Groq (online, rápido) / Ollama (local, sin límites)
- Aviso de latencia cuando se selecciona Ollama (30-60 segundos)

### Tab Científico 🔬
- Generación de contenido divulgativo con RAG sobre papers de arXiv
- Topics en inglés dan mejores resultados
- Aviso de lentitud durante la generación (2-3 minutos con Ollama)
- Contenido generado en el idioma seleccionado

### Tab Noticias 📰
- Titulares financieros en tiempo real via NewsAPI
- Caché de 5 minutos para respetar el límite de 100 req/día
- Botón de actualización forzada
- Cada titular con título, descripción y enlace a la noticia completa
- Generación de contenido financiero basado en noticias reales

### Perfil de empresa
- Sección colapsable con nombre, sector, tono y descripción
- Se persiste en el backend y se recupera al recargar
- Se inyecta como contexto en todas las generaciones
- Badges activos visibles cuando hay perfil guardado

### Resultado
- Imagen relevante de Unsplash encima del contenido
- Dos pestañas: **Raw** (texto plano) y **Preview** (Markdown renderizado)
- Botón copiar al portapapeles
- Skeleton loader durante la generación

### Historial 🕓
- Sección colapsable con todas las generaciones guardadas
- Cada registro expandible muestra imagen, metadatos y contenido completo
- Botón eliminar por registro
- Se actualiza automáticamente tras cada nueva generación

---

## Scripts disponibles

```bash
npm run dev      # Servidor de desarrollo
npm run build    # Build de producción
npm run start    # Servidor de producción
npm run lint     # Linter
```

---

## Docker

```bash
# Desde la raíz del proyecto
docker compose up --build
```

El frontend arranca en `http://localhost:3000` y se comunica con el
backend por nombre de servicio Docker (`http://backend:8000`).