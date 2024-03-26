// File: test_dashboard.js

QUnit.module('Checkbox and Row Selection', function(hooks) {
    hooks.beforeEach(function() {
        // Setup for each test goes here. This could involve appending necessary HTML elements to the QUnit fixture.
        $('#qunit-fixture').append(`
            <table id="dataTable">
                <tbody>
                    <tr><td><input type="checkbox" class="row-checkbox"> Row 1</td></tr>
                    <tr><td><input type="checkbox" class="row-checkbox"> Row 2</td></tr>
                </tbody>
            </table>
        `);

        // Manually bind the event handler to mimic dashboard.js functionality if needed
        $('.row-checkbox').on('click', function() {
            $(this).closest('tr').toggleClass('table-active');
        });
    });

    QUnit.test('Row selection toggles class', function(assert) {
        // Simulate a click on the first checkbox
        $('.row-checkbox').first().click();
        assert.ok($('.row-checkbox').first().closest('tr').hasClass('table-active'), 'First row should be active after click.');

        // Simulate another click on the first checkbox
        $('.row-checkbox').first().click();
        assert.notOk($('.row-checkbox').first().closest('tr').hasClass('table-active'), 'First row should not be active after second click.');
    });
});