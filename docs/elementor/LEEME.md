# Plantillas de Elementor Pro – Aluminis l'Albera

24 plantillas `.json`: 2 de Theme Builder (cabecera y pie) y 22 páginas.

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

### Páginas de producto (plantilla de la página 2 del PDF)
Cada producto del menú usa la misma plantilla, con el texto y las fotos de su página en aluminisalbera.com.

| Archivo | Producto | Slug nuevo | Slug en la web actual |
|---|---|---|---|
| `finestres-fulla-oculta.json` | Finestres fulla oculta C/16 | `/finestres-fulla-oculta/` | `/finestres-fulla-oculta/` |
| `finestres-rpt-55.json` | Finestres RPT 55 | `/finestres-rpt-55/` | `/finestres-rpt-55/` |
| `portes-dentrada.json` | Portes d'entrada | `/portes-dentrada/` | `/portes-dentrada/` |
| `persianes.json` | Persianes | `/persianes/` | `/portes-de-garaig/` |
| `persianes-locals-comercials.json` | Persianes locals comercials | `/persianes-locals-comercials/` | `/persianes/` |
| `corredisses.json` | Corredisses | `/corredisses/` | `/correderes/` |
| `corredisses-grans-dimensions.json` | Corredisses grans dimensions | `/corredisses-grans-dimensions/` | `/correderes-grans-dimensions/` |
| `baranes.json` | Baranes | `/baranes/` | `/baranes/` |
| `pergoles-bioclimatiques.json` | Pèrgoles bioclimàtiques | `/pergoles-bioclimatiques/` | `/pergoles/` |
| `sostres-dalumini.json` | Sostres d'alumini | `/sostres-dalumini/` | `/sostres-dalumini/` |
| `tancaments-jardi.json` | Tancaments jardí | `/tancaments-jardi/` | `/tancaments-jardi/` |
| `mampares-de-bany.json` | Mampares de bany | `/mampares-de-bany/` | `/mampares/` |
| `muntatge.json` | Muntatge | `/muntatge/` | `/muntatges/` |
| `altres-feines.json` | Altres feines | `/altres-feines/` | `/altres-feines/` |

Si sustituyes la web actual, los slugs que cambian necesitan una redirección 301 desde el antiguo para no perder posicionamiento.
Ojo: en la web actual `/portes-de-garaig/` contiene en realidad las persianes y `/persianes/` las persianes de locals comercials.

Crea las páginas con esos slugs para que los enlaces funcionen.

## Notas
- Las imágenes se descargan a la biblioteca de medios al importar, desde `img/` de este repositorio
  (`https://raw.githubusercontent.com/naniiqr/curso-frontend-developer-Javascript/claude/cool-maxwell-eomrra/docs/img/`).
  Si cambias la rama, el repositorio pasa a privado o mueves las imágenes, pídeme regenerar las plantillas con la nueva URL.
- Espaciados y tamaños están definidos para escritorio, tablet y móvil en cada sección.
- El formulario de contacto y el mapa son bloques HTML de relleno: sustitúyelos por tu formulario (Elementor Pro → Formulario) y tu mapa.
- Las redes sociales del pie apuntan a `#`: pon las URL reales.
