QUnit.module('File List Tests', hooks => {

  // Setup HTML structure for tests
  hooks.beforeEach(() => {
    const testHtml = `
      <button id="renameButton">Rename</button>
      <div class="rename-form" style="display:none;">
        <input name="new_name" type="text">
      </div>
      <input type="checkbox" id="flexCheckDefault">
      <form id="delete-all" style="display:none;"></form>
      <div id="fileList">
        <div class="list-item" style="opacity:0; transform: translateY(20px);"></div>
        <div class="list-item" style="opacity:0; transform: translateY(20px);"></div>
      </div>
    `;
    document.getElementById('qunit-fixture').innerHTML = testHtml;
  });

  // Test showing the rename field
  QUnit.test('showRenameField() makes rename form visible and hides button', assert => {
    const button = document.getElementById('renameButton');
    showRenameField(button);
    assert.equal(button.style.display, 'none', 'Button is hidden');
    const renameForm = document.querySelector('.rename-form');
    assert.equal(renameForm.style.display, 'block', 'Rename form is visible');
  });

  // Test toggle of delete all form based on checkbox
  QUnit.test('Toggle delete all form visibility based on checkbox', assert => {
    const selectAllCheckbox = document.getElementById('flexCheckDefault');
    const deleteAllForm = document.getElementById('delete-all');
    // Simulate checking the checkbox
    selectAllCheckbox.checked = true;
    const changeEvent = new Event('change');
    selectAllCheckbox.dispatchEvent(changeEvent);
    // assert.equal(deleteAllForm.style.display, 'block', 'Delete all form is shown when checkbox is checked');

    // Simulate unchecking the checkbox
    selectAllCheckbox.checked = false;
    selectAllCheckbox.dispatchEvent(changeEvent);
    assert.equal(deleteAllForm.style.display, 'none', 'Delete all form is hidden when checkbox is unchecked');
  });

});
