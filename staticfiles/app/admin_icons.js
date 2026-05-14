// Ensure Material Icons are loaded when the DOM is ready
(function() {
    if (window.MaterialSymbolsLoaded) return;
    
    // Reload Material Symbols if not already loaded
    const linkTag = document.querySelector('link[href*="Material+Symbols"]');
    if (!linkTag) {
        const link = document.createElement('link');
        link.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0';
        link.rel = 'stylesheet';
        document.head.appendChild(link);
    }
    
    window.MaterialSymbolsLoaded = true;
})();

function setIconPreview(iconName) {
    const readonlyContainer = document.querySelector('.field-icon_preview .readonly');
    if (!readonlyContainer) return;

    let symbol = readonlyContainer.querySelector('.material-symbols-outlined');
    let label = readonlyContainer.querySelector('.icon-preview-label');

    if (!symbol || !label) {
        readonlyContainer.innerHTML =
            '<span style="display:inline-flex;align-items:center;gap:8px;">' +
            '<span class="material-symbols-outlined" style="font-size:24px;line-height:1;"></span>' +
            '<span class="icon-preview-label"></span>' +
            '</span>';
        symbol = readonlyContainer.querySelector('.material-symbols-outlined');
        label = readonlyContainer.querySelector('.icon-preview-label');
    }

    if (symbol) {
        symbol.textContent = iconName;
    }
    if (label) {
        label.textContent = iconName;
    }
}

function bindIconPreviewSync() {
    const iconInputs = document.querySelectorAll('input[type="radio"][name="icon"], input[type="radio"][name="icon_name"]');
    if (!iconInputs.length) return;

    const getSelectedIcon = () => {
        const selected = document.querySelector('input[type="radio"][name="icon"]:checked, input[type="radio"][name="icon_name"]:checked');
        return selected ? selected.value : 'school';
    };

    const sync = () => setIconPreview(getSelectedIcon());

    iconInputs.forEach((input) => {
        if (input.dataset.previewBound === '1') return;
        input.addEventListener('change', sync);
        input.dataset.previewBound = '1';
    });

    sync();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindIconPreviewSync);
} else {
    bindIconPreviewSync();
}
