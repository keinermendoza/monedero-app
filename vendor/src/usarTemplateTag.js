import htmx from 'htmx.org';

export default function usarTemplateTag(templateId, modalId, slotId) {
  const template = document.getElementById(templateId);
  const modal = document.getElementById(modalId);
  const content = document.getElementById(slotId);
  if (template && modal) {
    const clone = template.content.cloneNode(true);
    content.innerHTML = "";
    content.appendChild(clone);
    modal.showModal();
    htmx.process(content)
  } else {
    console.warn("Template o contenedor no encontrados.");
  }
}
