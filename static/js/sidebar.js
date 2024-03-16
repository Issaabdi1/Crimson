document.addEventListener("DOMContentLoaded", function() {
    const switchInput = document.getElementById("flexSwitchCheckDefault");
    const switchLabel = document.querySelector('.form-check-label[for="flexSwitchCheckDefault"]');
    const modeIcon = document.getElementById("mode-icon");

    // Check local storage for user's preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';

    // Set initial state based on user's preference
    if (isDarkMode) {
        enableDarkMode();
        switchInput.checked = true;
    } else {
        disableDarkMode();
        switchInput.checked = false;
    }

    switchInput.addEventListener("change", function() {
        if (this.checked) {
            enableDarkMode();
        } else {
            disableDarkMode();
        }

        // Save user's preference to local storage
        localStorage.setItem('darkMode', this.checked);
    });

    function enableDarkMode() {
        document.body.classList.remove("default-mode");
        document.body.classList.add("dark-mode");
        modeIcon.classList.remove("bi-brightness-high");
        modeIcon.classList.add("bi-moon-stars-fill");
        switchLabel.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
    }

    function disableDarkMode() {
        document.body.classList.remove("dark-mode");
        document.body.classList.add("default-mode");
        modeIcon.classList.remove("bi-moon-stars-fill");
        modeIcon.classList.add("bi-brightness-high");
        switchLabel.innerHTML = '<svg t="1709392435303" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1967" width="25" height="25"><path d="M512 85.333333a42.666667 42.666667 0 0 1 42.666667 42.666667v42.666667a42.666667 42.666667 0 1 1-85.333334 0V128a42.666667 42.666667 0 0 1 42.666667-42.666667z m301.696 124.970667a42.666667 42.666667 0 0 1 0 60.330667l-30.165333 30.186666a42.666667 42.666667 0 0 1-60.330667-60.352l30.165333-30.165333a42.666667 42.666667 0 0 1 60.330667 0z m-603.392 0a42.666667 42.666667 0 0 1 60.330667 0l30.186666 30.165333a42.666667 42.666667 0 0 1-60.352 60.352l-30.165333-30.186666a42.666667 42.666667 0 0 1 0-60.330667zM512 341.333333a170.666667 170.666667 0 1 0 0 341.333334 170.666667 170.666667 0 0 0 0-341.333334z m-256 170.666667c0-141.376 114.624-256 256-256s256 114.624 256 256-114.624 256-256 256-256-114.624-256-256z m-170.666667 0a42.666667 42.666667 0 0 1 42.666667-42.666667h42.666667a42.666667 42.666667 0 1 1 0 85.333334H128a42.666667 42.666667 0 0 1-42.666667-42.666667z m725.333334 0a42.666667 42.666667 0 0 1 42.666666-42.666667h42.666667a42.666667 42.666667 0 1 1 0 85.333334h-42.666667a42.666667 42.666667 0 0 1-42.666666-42.666667z m-570.197334 211.2a42.666667 42.666667 0 1 1 60.352 60.330667l-30.186666 30.165333a42.666667 42.666667 0 1 1-60.330667-60.330667l30.165333-30.165333zM723.2 783.530667a42.666667 42.666667 0 0 1 60.330667-60.330667l30.165333 30.165333a42.666667 42.666667 0 1 1-60.330667 60.330667L723.2 783.530667zM512 810.666667a42.666667 42.666667 0 0 1 42.666667 42.666666v42.666667a42.666667 42.666667 0 1 1-85.333334 0v-42.666667a42.666667 42.666667 0 0 1 42.666667-42.666666z" fill="#000000" p-id="1968"></path></svg>';
    }
});