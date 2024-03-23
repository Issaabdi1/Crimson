document.addEventListener("DOMContentLoaded", function () {
    // Change ErrorList Position
    const errorLists = document.querySelectorAll('.errorlist');

    errorLists.forEach(errorList => {
        const input = errorList.nextElementSibling;
        input.insertAdjacentElement('afterend', errorList);
    });

    // Handle the effect of label
    const mainContainers = document.querySelectorAll('.mainContainer');
    mainContainers.forEach(container => {
        const inputs = container.querySelectorAll('input');
        inputs.forEach(input => {
            const label = input.previousElementSibling;

            if (label && input.value) {
                label.style.transform = 'translateY(-1.25rem)';
                label.style.fontSize = '0.8125rem';
                if (document.body.classList.contains("dark-mode")) {
                    label.style.color = '#ACACAC';
                } else {
                    label.style.color = 'var(--gray-base)';
                }
            }

            input.addEventListener('focus', () => {
                if (label) {
                    console.log(label.textContent);
                    label.style.transform = 'translateY(-1.25rem)';
                    label.style.fontSize = '0.8125rem';
                    if (document.body.classList.contains("dark-mode")) {
                        label.style.color = '#ACACAC';
                    } else {
                        label.style.color = 'var(--gray-base)';
                    }
                }
            });

            input.addEventListener('blur', () => {
                if (label && input.value === '') {
                    label.style.transform = '';
                    label.style.fontSize = '';
                    label.style.color = '';
                }
            });
        });
    })
});