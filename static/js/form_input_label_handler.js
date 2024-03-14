document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll('input');

    inputs.forEach(input => {
        const label = input.previousElementSibling;

        input.addEventListener('focus', () => {
            if (label) {
                console.log(label.textContent);
                label.style.transform = 'translateY(-1.25rem)';
                label.style.fontSize = '0.8125rem';
                label.style.color = 'var(--gray-base)';
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
});