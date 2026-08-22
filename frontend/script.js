const menuButton = document.querySelector(".menu-button");
const navLinks = document.querySelector(".nav-links");

const modal = document.querySelector("#infoModal");
const modalTitle = document.querySelector("#modalTitle");
const modalText = document.querySelector("#modalText");
const closeModalButton = document.querySelector(".close-modal");
const closeActionButton = document.querySelector(".close-action");

function openModal(title, text) {
  modalTitle.textContent = title;
  modalText.textContent = text;
  modal.hidden = false;
  document.body.style.overflow = "hidden";
  closeModalButton.focus();
}

function closeModal() {
  modal.hidden = true;
  document.body.style.overflow = "";
}

function scrollToSection(selector) {
  const section = document.querySelector(selector);

  if (section) {
    section.scrollIntoView({
      behavior: "smooth"
    });
  }
}

menuButton.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");

  menuButton.setAttribute("aria-expanded", isOpen);
  menuButton.setAttribute(
    "aria-label",
    isOpen ? "Close menu" : "Open menu"
  );
});

document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
  });
});

document.querySelectorAll(".learn-btn").forEach((button) => {
  button.addEventListener("click", () => {
    if (button.classList.contains("scroll-help")) {
      scrollToSection("#help");
      return;
    }

    openModal("NyayaSetu Guidance", button.dataset.message);
  });
});

document.querySelectorAll(".problem-card").forEach((card) => {
  card.addEventListener("click", () => {
    openModal(card.dataset.title, card.dataset.text);
  });
});

document.querySelector(".scroll-help").addEventListener("click", () => {
  scrollToSection("#help");
});

document.querySelector(".scroll-guidance").addEventListener("click", () => {
  scrollToSection("#guidance");
});

closeModalButton.addEventListener("click", closeModal);

closeActionButton.addEventListener("click", closeModal);

modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !modal.hidden) {
    closeModal();
  }
});