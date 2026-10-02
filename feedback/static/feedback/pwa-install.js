(() => {
    const installArea = document.getElementById("pwa-install-area");
    const installButton = document.getElementById("pwa-install-button");
    const helpDialog = document.getElementById("pwa-install-help");
    const instructions = document.getElementById("pwa-install-instructions");
    const closeButton = document.getElementById("pwa-install-close");

    if (!installArea || !installButton || !helpDialog || !instructions || !closeButton) {
        return;
    }

    let deferredPrompt = null;
    const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent)
        || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    const isStandalone = window.matchMedia("(display-mode: standalone)").matches
        || navigator.standalone === true;

    if (isStandalone) {
        return;
    }

    instructions.textContent = isIOS
        ? "No Safari, toque em Compartilhar e escolha Adicionar à Tela de Início."
        : "No menu do navegador, escolha Instalar app ou Adicionar à tela inicial.";
    installArea.classList.remove("hidden");

    window.addEventListener("beforeinstallprompt", (event) => {
        event.preventDefault();
        deferredPrompt = event;
    });

    installButton.addEventListener("click", async () => {
        if (!deferredPrompt) {
            helpDialog.showModal();
            return;
        }

        deferredPrompt.prompt();
        await deferredPrompt.userChoice;
        deferredPrompt = null;
        installArea.classList.add("hidden");
    });

    closeButton.addEventListener("click", () => helpDialog.close());
    helpDialog.addEventListener("click", (event) => {
        if (event.target === helpDialog) {
            helpDialog.close();
        }
    });

    window.addEventListener("appinstalled", () => installArea.classList.add("hidden"));
})();