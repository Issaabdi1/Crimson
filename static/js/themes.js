document.addEventListener("DOMContentLoaded", function() {
    var themes = {
        "themes": {
          // "dark-mode": "Dark Mode",
          "default-mode": "Default Mode",
          "orange-mode": "Orange Mode",
          "forest-mode": "Forest Mode",
          "pink-mode": "Pink Mode"
        }
      };

    var themeOptions = document.getElementById('themeOptions');

    for (var key in themes.themes) {
        if (themes.themes.hasOwnProperty(key)) {
            var theme = themes.themes[key];
            var label = document.createElement("label");
            label.htmlFor = key;
            label.appendChild(document.createTextNode(theme));
    
            var input = document.createElement("input");
            input.type = 'radio';
            input.id = key;
            input.name = 'themeSelection';
            input.value = key;
    
            themeOptions.appendChild(input);
            themeOptions.appendChild(label);
            themeOptions.appendChild(document.createElement("br"));
        }
    }
    
});
