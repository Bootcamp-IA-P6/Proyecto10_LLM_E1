# Frontend — Digital Content AI

Interfaz web del sistema de generación automática de contenido con IA, construida con Next.js 15, TypeScript y Tailwind CSS.

---

## Tecnologías

- **Next.js 15** — App Router
- **TypeScript 5**
- **Tailwind CSS v4**
- **react-markdown** — previsualización de contenido Markdown
- **@tailwindcss/typography** — estilos para contenido renderizado

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
├── src/
│   ├── app/
│   │   ├── globals.css        # Estilos globales + plugins Tailwind
│   │   ├── layout.tsx         # Layout raíz
│   │   └── page.tsx           # Página principal
│   ├── components/
│   │   ├── GenerateForm.tsx   # Formulario de generación
│   │   └── ContentResult.tsx  # Visualización del resultado (Raw / Preview)
│   ├── services/
│   │   └── api.ts             # Llamadas HTTP al backend
│   └── types/
│       └── content.ts         # Tipos TypeScript compartidos
├── .env.example
├── package.json
└── tsconfig.json
```

---

## Funcionalidades actuales (Fase 1)

- Selección de plataforma: Blog, Twitter/X, LinkedIn, Instagram
- Inputs de tema, audiencia y tono
- Selector de idioma: Español, English, Français, Italiano
- Visualización del resultado en dos modos:
  - **Raw** — texto plano listo para copiar
  - **Preview** — Markdown renderizado
- Botón de copiar al portapapeles
- Skeleton loader mientras se genera el contenido
- Manejo de errores de conexión con el backend

---

## Scripts disponibles

```bash
npm run dev      # Servidor de desarrollo
npm run build    # Build de producción
npm run start    # Servidor de producción
npm run lint     # Linter
```