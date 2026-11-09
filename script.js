const currentPage = window.location.pathname.split("/").pop() || "index.html";
const navLinks = document.querySelectorAll(".nav-list a");

navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (href === currentPage) {
        link.classList.add("active");
    }
});

const cards = document.querySelectorAll(".card, .project");

if ("IntersectionObserver" in window && cards.length) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    cards.forEach((card) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";
        card.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        observer.observe(card);
    });
}

const form = document.getElementById("contact-form");

if (form) {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const status = document.getElementById("form-status");
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        status.textContent = "";

        try {
            const response = await fetch("/api/contact", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(Object.fromEntries(new FormData(form)))
            });
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Unable to send your message.");
            }

            status.textContent = result.message;
            form.reset();
        } catch (error) {
            status.textContent = error instanceof Error
                ? error.message
                : "Unable to send your message. Please try again.";
        } finally {
            submitButton.disabled = false;
        }
    });
}

const buttons = document.querySelectorAll(".btn, .buttons a");

buttons.forEach((button) => {
    button.addEventListener("mouseenter", () => {
        button.style.transform = "translateY(-2px)";
    });

    button.addEventListener("mouseleave", () => {
        button.style.transform = "translateY(0)";
    });
});

const topBtn = document.getElementById("topBtn") || document.createElement("button");
if (!document.getElementById("topBtn")) {
    topBtn.id = "topBtn";
    topBtn.textContent = "↑";
    Object.assign(topBtn.style, {
        position: "fixed",
        right: "20px",
        bottom: "20px",
        border: "none",
        borderRadius: "50%",
        width: "48px",
        height: "48px",
        background: "#22c55e",
        color: "#fff",
        fontSize: "1.3rem",
        cursor: "pointer",
        boxShadow: "0 12px 24px rgba(34, 197, 94, 0.3)",
        display: "none",
        zIndex: "999"
    });
    document.body.appendChild(topBtn);
}

window.addEventListener("scroll", () => {
    topBtn.style.display = window.scrollY > 300 ? "block" : "none";
});

topBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});