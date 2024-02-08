
function add(a, b) {
    return a + b;
}

QUnit.module('notifications', function() {
    //Notifications
    const btns = document.querySelectorAll('#remove-notification');
    //test delete-button
    const delete_all_button = document.querySelectorAll('button[type=submit]')
    const delete_button = document.querySelectorAll('button[type=button]')
    console.log(delete_all_button);
    console.log(delete_button);

    //test dismiss all button
    QUnit.test('delete-button', function(assert) {
        assert.equal(add(1, 2), 3);
    });
});

