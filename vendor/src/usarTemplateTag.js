import htmx from 'htmx.org';
/* 
permite pasar el contenido de un template tag a un elemnto target por medio de sus ids
usada como inline function por 'cotton/ui/td_showdetail.html'
*/
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
