document.addEventListener("DOMContentLoaded", function() {
    var themes = {
        "themes": [
            "dark-mode",
            "default-mode",
            "fire-mode",
            "forest-mode",
            "pink-mode",
        ]
    };

    var themeOptions = document.getElementById('themeOptions');

    for (var i = 0; i < themes.themes.length; i++) {
        var theme = themes.themes[i];
        var label = document.createElement("label");
        label.htmlFor = theme;
        label.appendChild(document.createTextNode(theme));
        
        var input = document.createElement("input");
        input.type = 'radio'; // Assuming you want radio buttons for theme selection
        input.id = theme;
        input.name = 'themeSelection';
        input.value = theme;

        themeOptions.appendChild(input);
        themeOptions.appendChild(label);
        themeOptions.appendChild(document.createElement("br"));
    }
});
