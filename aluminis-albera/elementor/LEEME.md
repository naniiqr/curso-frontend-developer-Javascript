# Plantillas de Elementor – Aluminis l'Albera

Una plantilla `.json` por página. Importar en WordPress: **Plantillas → Plantillas guardadas → Importar plantillas**
(o dentro de Elementor: icono de carpeta → *Importar*). Después, "Insertar" en una página nueva.

| Archivo | Página | Slug esperado |
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

- Crea las páginas con esos slugs para que los enlaces del menú y de los botones funcionen.
- Cada plantilla usa el lienzo de Elementor (sin cabecera/pie del tema) y lleva su propia cabecera y pie.
- Las imágenes se descargan a la biblioteca de medios al importar, desde `img/` de este repositorio
  (`https://raw.githubusercontent.com/naniiqr/curso-frontend-developer-Javascript/claude/cool-maxwell-eomrra/aluminis-albera/img/`).
  Si cambias la rama o el repositorio es privado, vuelve a generar con la variable `IMG_BASE`.
- Solo usa widgets gratuitos de Elementor (sin Pro). El formulario de contacto y el mapa son bloques HTML
  de relleno: sustitúyelos por tu plugin de formularios y tu mapa.
