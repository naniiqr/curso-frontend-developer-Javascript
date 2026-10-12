# Plantillas de Elementor Pro – Aluminis l'Albera

11 plantillas `.json`: 2 de Theme Builder (cabecera y pie) y 9 páginas.

## 1. Menú de WordPress (antes de importar)
Apariencia → Menús → crea un menú llamado **Menú principal** (slug `menu-principal`) con:
Inici (`/`), Productes, Projectes, Sobre nosaltres, Contacte. Las plantillas lo usan en la cabecera y en el pie.
Si tu menú tiene otro nombre, selecciónalo en el widget *Menú de navegación* de cada plantilla.

## 2. Cabecera y pie (Elementor Pro → Theme Builder)
1. Plantillas → Theme Builder → Cabecera → *Añadir nueva* → Importar `header.json`.
   Condiciones de visualización: **Todo el sitio**. Publicar.
2. Lo mismo con Pie de página → `footer.json`.
- La cabecera es fija (sticky), con menú hamburguesa en tablet y móvil. El botón "Demana pressupost" se oculta en tablet y móvil.
- El pie incluye el botón flotante de WhatsApp (600 83 19 36).

## 3. Páginas
Plantillas → Plantillas guardadas → Importar plantillas, y luego insertar cada una en una página nueva.
Las páginas usan la plantilla "Ancho completo de Elementor" (con la cabecera y el pie del Theme Builder).

| Archivo | Página | Slug |
|---|---|---|
| `inici.json` | Inici | `/` (página de inicio) |
| `productes.json` | Productes | `/productes/` |
| `projectes.json` | Projectes | `/projectes/` |
| `sobre-nosaltres.json` | Sobre nosaltres | `/sobre-nosaltres/` |
| `contacte.json` | Contacte | `/contacte/` |
| `finestres-rpt-55.json` | Finestres RPT 55 | `/finestres-rpt-55/` |
| `portes-entrada-particular.json` | Galería Particular | `/portes-entrada-particular/` |
| `portes-entrada-ocultec.json` | Galería OCULTEC | `/portes-entrada-ocultec/` |
| `portes-entrada-comercial.json` | Galería Comercial | `/portes-entrada-comercial/` |

Crea las páginas con esos slugs para que los enlaces funcionen.

## Notas
- Las imágenes se descargan a la biblioteca de medios al importar, desde `img/` de este repositorio
  (`https://raw.githubusercontent.com/naniiqr/curso-frontend-developer-Javascript/claude/cool-maxwell-eomrra/aluminis-albera/img/`).
  Si cambias la rama, el repositorio pasa a privado o mueves las imágenes, pídeme regenerar las plantillas con la nueva URL.
- Espaciados y tamaños están definidos para escritorio, tablet y móvil en cada sección.
- El formulario de contacto y el mapa son bloques HTML de relleno: sustitúyelos por tu formulario (Elementor Pro → Formulario) y tu mapa.
- Las redes sociales del pie apuntan a `#`: pon las URL reales.
