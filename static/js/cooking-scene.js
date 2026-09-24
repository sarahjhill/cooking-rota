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

  // Respect a user's reduced-motion preference — the caption text change
  // is a small thing, but there's no reason to keep it cycling forever
  // for someone who's asked for less motion/animation on their system.
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  if (prefersReducedMotion) return;

  let index = 0;
  setInterval(() => {
    index = (index + 1) % dishes.length;
    caption.textContent = dishes[index];
  }, 4000);
});
