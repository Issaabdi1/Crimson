document.addEventListener('DOMContentLoaded', function() {   
    // Search function
    document.getElementById('search').addEventListener('input', function () {
        const search = this.value.toLowerCase();
        const items = document.querySelectorAll('.search-filter');
        for (const item of items) {
            const selected = item.classList.contains('selected');
            const username = item.querySelector('.username').textContent;
            if (search.length >= 3 && !selected) {
                if (username.includes(search)) {
                    item.classList.remove('d-none');
                } else {
                    item.classList.add('d-none');
                }
            } else if (!selected) {
                item.classList.add('d-none');
            }
        }
    });

    // Disables the Enter key which could cause unintentional sharing
    document.getElementById('search').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    });


    // Each thumbnail selected updates the hidden 'select option' menu
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumbnail => {

        // Filter the beginning of each file name
        const filename = thumbnail.querySelector('.file-name').textContent;
        const filter = filename.replace(/^user_@[\w\d]+\//, ''); 
        thumbnail.querySelector('.file-name').textContent = filter;

        thumbnail.addEventListener('click', function() {
            const isSelected = this.classList.contains('selected');
            thumbnails.forEach(thumb => {
                thumb.classList.remove('selected');
            });
            if (!isSelected) {
                this.classList.add('selected');
            }
            const fileid = isSelected ? null : this.getAttribute('file-id');
            document.getElementById('file-select').value = fileid;
        });
    });

    // Each user selected updates the button's userID
    let selectedUsers = [];
    const users = document.querySelectorAll('.search-filter');
    users.forEach(user => {
        user.addEventListener('click', function() {

            // Update selected class (visual update)
            const selected = this.classList.contains('selected');
            if (!selected) {
                this.classList.add('selected');
            } else {
                this.classList.remove('selected');
            }
            
            // Update selected array (data update)
            const userid = user.getAttribute('value');
            const index = selectedUsers.indexOf(userid);
            if (index === -1) {
                selectedUsers.push(userid);
            } else {
                selectedUsers.splice(index, 1);
            }
            
            // Update button with new array
            const sharebtn = document.querySelector('.share-btn');
            sharebtn.value = selectedUsers.join(',');
        });
    });

});
