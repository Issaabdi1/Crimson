// Search function
document.getElementById('search').addEventListener('input', function () {
    const search = this.value.toLowerCase();
    const table = document.getElementById('filter');
    const rows = table.getElementsByTagName('tr');
    for (const row of rows) {
        const username = row.cells[0].textContent;
        if (search.length >= 3) {
            if (username.includes(search)) {
            row.style.display = 'table-row';
            } else {
            row.style.display = 'none';
            }
        } else {
            row.style.display = 'none';
        }
    }
  });

// Disables the Enter key which could cause unintentional sharing
document.getElementById('search').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
    }
})


// Each thumbnail selected updates the hidden 'select option' menu
const thumbnails = document.querySelectorAll('.thumbnail');
thumbnails.forEach(thumbnail => {

    // Filter the beginning of each file name
    const fileName = thumbnail.querySelector('.file-name').textContent;
    const filteredFileName = fileName.replace(/^user_@[\w\d]+\//, ''); 
    thumbnail.querySelector('.file-name').textContent = filteredFileName;

    thumbnail.addEventListener('click', function() {
        const isSelected = this.classList.contains('selected');
        thumbnails.forEach(thumb => {
            thumb.classList.remove('selected');
        });
        if (!isSelected) {
            this.classList.add('selected');
        }
        const fileId = isSelected ? null : this.getAttribute('file-id');
        document.getElementById('file-select').value = fileId;
    });
});
