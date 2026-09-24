/* jshint esversion: 11 */
// Rotates the caption under the homepage cooking animation.
// Does nothing on pages that don't have the element — safe to load everywhere.
document.addEventListener("DOMContentLoaded", () => {
  const caption = document.getElementById("cook-caption");
  if (!caption) return;

  const dishes = [
    "Sunday roast, simmering away…",
    "A big pot of veggie chilli…",
    "Butter chicken on the hob…",
    "Something warm for someone who needs it…",
  ];

  let index = 0;
  setInterval(() => {
    index = (index + 1) % dishes.length;
    caption.textContent = dishes[index];
  }, 4000);
});
