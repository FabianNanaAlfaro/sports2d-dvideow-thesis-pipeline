const stages = [
  {
    id: "S00", label: "Framing", title: "Pregunta, ética y alcance",
    summary: "La investigación empieza con una pregunta operacional: si las rutas markerless pueden sostener un análisis de movimiento y asimetría en el intervalo pre-impacto → impacto.",
    input: "Pregunta + protocolo aprobado",
    output: "Plan de análisis versionado",
    gate: "Definir variables, límites y artefactos que nunca salen del paquete privado.",
    doc: "docs/pipeline.md#stage-0--research-question-ethics-and-scope"
  },
  {
    id: "S01", label: "Integrity map", title: "Inventario semántico, no por nombres accidentales",
    summary: "Cada unidad se identifica por trial, lado y rol de cámara. Los sufijos históricos se resuelven como alias documentados; no se usan para intercambiar CAM_1 y CAM_2.",
    input: "Fuentes y mapa de correspondencia",
    output: "Manifest versionado",
    gate: "Pareja de cámaras, plantilla de frames y origen trazables.",
    doc: "docs/pipeline.md#stage-1--source-inventory-and-integrity-map"
  },
  {
    id: "S02", label: "Synchronized views", title: "Anclar el tiempo antes de medir",
    summary: "Las vistas sincronizadas conservan su frecuencia y dimensión. El evento de impacto funciona como ancla; el desplazamiento entre convenciones de frame se declara, nunca se adivina.",
    input: "Par de vistas + ancla temporal",
    output: "Contrato de frame",
    gate: "Distinguir video row 0, DAT frame 1 y la relación con 3D.",
    doc: "docs/methods.md#temporal-contract"
  },
  {
    id: "S03", label: "Parallel 2D routes", title: "Cuatro rutas, una comparación honesta",
    summary: "DVIDEOW manual, Sports2D, MediaPipe Pose y DeepLabCut observan el movimiento de formas distintas. Cada una conserva su configuración y pasa por un adaptador explícito.",
    input: "Vistas ancladas",
    output: "Observaciones 2D por ruta",
    gate: "No copiar coordenadas manuales a un detector ni ocultar la curation detrás de un número.",
    doc: "docs/methods.md#routes"
  },
  {
    id: "S04", label: "Homologation", title: "Hablar el mismo idioma anatómico",
    summary: "Hip, rodilla, tobillo y pie se convierten en la interfaz funcional común. Se conservan likelihood, validez, missingness y transformaciones de ROI.",
    input: "Puntos 2D específicos de cada ruta",
    output: "Contrato común de puntos",
    gate: "Un valor ausente no se convierte en cero; toda transformación es reversible y versionada.",
    doc: "docs/methods.md#2d-observation-contract"
  },
  {
    id: "S05", label: "Common DLT", title: "Reconstruir con la misma geometría",
    summary: "Las dos observaciones homologadas entran al mismo contrato DLT. La calibración real permanece privada, pero su referencia, reproyección y controles forman parte del protocolo.",
    input: "Dos puntos 2D + referencia de calibración",
    output: "Contrato 3D con quality checks",
    gate: "Pareja correcta, valores finitos, reproyección y base de frames aprobadas.",
    doc: "docs/methods.md#reference-and-dlt-contract"
  },
  {
    id: "S06", label: "Temporal + biomechanics", title: "Filtrar sin borrar la pregunta",
    summary: "La ventana pre-impacto → impacto se normaliza a 101 posiciones y alimenta trayectorias, velocidades, ángulos, velocidades angulares y variables bilaterales.",
    input: "Trayectorias 3D válidas",
    output: "Variables derivadas normalizadas",
    gate: "Parámetros de filtro, orden, frecuencia y origen de cada punto viajan con el manifest.",
    doc: "docs/pipeline.md#stage-6--temporal-treatment-and-biomechanical-variables"
  },
  {
    id: "S07", label: "Validation + audit", title: "No reducir todo a un único score",
    summary: "La evaluación separa acuerdo 2D, reconstrucción 3D, preservación temporal, estructura de acuerdo, simetría y robustez. Las afirmaciones siguen el tipo de validación que realmente se ejecutó.",
    input: "Plan métrico + outputs válidos",
    output: "Registro de evaluación auditable",
    gate: "Distinguir selección 2D, validación 3D externa, exploratorio y confirmatorio.",
    doc: "docs/methods.md#metrics-contract"
  },
  {
    id: "S08", label: "Public release", title: "Publicar el proceso, no la base",
    summary: "La última etapa valida el manifiesto sintético, audita archivos y privacidad, comprueba enlaces y publica la guía interactiva con commits trazables.",
    input: "Árbol público revisado",
    output: "Repositorio + guía visual",
    gate: "Proof, database, videos, software, modelos y resultados deben estar ausentes.",
    doc: "docs/data-boundary.md"
  }
];

const list = document.querySelector("#stage-list");
const detail = document.querySelector("#stage-detail");

function renderDetail(stage) {
  detail.innerHTML = `
    <div class="detail-kicker">${stage.id} · ${stage.label.toUpperCase()}</div>
    <h3 class="detail-title">${stage.title}</h3>
    <p class="detail-summary">${stage.summary}</p>
    <div class="detail-grid">
      <div class="detail-cell"><span>Entra</span><p>${stage.input}</p></div>
      <div class="detail-cell"><span>Sale</span><p>${stage.output}</p></div>
      <div class="detail-cell"><span>Gate</span><p>${stage.gate}</p></div>
    </div>
    <a class="detail-link" href="https://github.com/FabianNanaAlfaro/sports2d-dvideow-thesis-pipeline/blob/main/${stage.doc}">Leer contrato completo ↗</a>
  `;
}

function setActive(index) {
  const stage = stages[index];
  document.querySelectorAll(".stage-button").forEach((button, buttonIndex) => {
    button.setAttribute("aria-pressed", String(buttonIndex === index));
  });
  renderDetail(stage);
}

stages.forEach((stage, index) => {
  const button = document.createElement("button");
  button.className = "stage-button";
  button.type = "button";
  button.setAttribute("aria-pressed", index === 0 ? "true" : "false");
  button.innerHTML = `<span class="stage-id">${stage.id}</span><span class="stage-name">${stage.label}</span><span class="stage-arrow" aria-hidden="true">›</span>`;
  button.addEventListener("click", () => setActive(index));
  list.appendChild(button);
});

renderDetail(stages[0]);

