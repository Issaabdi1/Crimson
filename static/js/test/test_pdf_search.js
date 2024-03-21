QUnit.module('Utilities', {
    beforeEach: function() {
      console.log('Setting up Utilities tests');
      // Setup for escapeHtml tests doesn't require DOM manipulation
  
      // Setup for searchForTerm tests
      document.body.innerHTML = `
        <div id="textLayerContainer">
          <span role="presentation">Test text</span>
          <span role="presentation">Another test</span>
        </div>
        <input id="searchTermInput" value=""/>
      `;
    }
  });
  
  // Tests for escapeHtml
  QUnit.test('escapeHtml converts special characters to HTML entities', function(assert) {
    console.log('Testing: escapeHtml converts special characters');
    const input = '&<>"\'';
    const expected = '&amp;&lt;&gt;&quot;&#039;';
    const result = escapeHtml(input);
    assert.equal(result, expected, 'Special characters are correctly escaped.');
  });
  
  QUnit.test('escapeHtml returns an empty string if given an empty string', function(assert) {
    console.log('Testing: escapeHtml with an empty string');
    const input = '';
    const expected = '';
    const result = escapeHtml(input);
    assert.equal(result, expected, 'Given an empty string, returns an empty string.');
  });
  
  QUnit.test('escapeHtml does not modify strings without special characters', function(assert) {
    console.log('Testing: escapeHtml with a string without special characters');
    const input = 'Hello, world!';
    const expected = 'Hello, world!';
    const result = escapeHtml(input);
    assert.equal(result, expected, 'String without special characters is not modified.');
  });
  
  // Tests for searchForTerm
  QUnit.module('Search', {
    beforeEach: function() {
      console.log('Setting up Search tests');
      // Setup for searchForTerm similar to Utilities but may include additional setup specific for search functionalities
      document.body.innerHTML = `
        <div id="textLayerContainer">
          <span role="presentation">Test text</span>
          <span role="presentation">Another test</span>
        </div>
      `;
    }
  });
  
  QUnit.test('searchForTerm highlights search terms correctly', function(assert) {
    console.log('Testing: searchForTerm highlights terms');
    const term = 'test';
    const foundPositions = searchForTerm(term);
    assert.equal(foundPositions.length, 1, 'One term is found and highlighted.');
    assert.ok(document.querySelector('span[style="background-color: lightblue;"]'), 'The term is highlighted with lightblue background.');
  });
  
  QUnit.test('searchForTerm handles case-insensitive search', function(assert) {
    console.log('Testing: searchForTerm with case-insensitive search');
    const term = 'TEST';
    const foundPositions = searchForTerm(term);
    assert.equal(foundPositions.length, 1, 'Case-insensitive search finds the term.');
  });
  
  QUnit.test('searchForTerm does not find non-existent terms', function(assert) {
    console.log('Testing: searchForTerm with a non-existent term');
    const term = 'nonexistent';
    const foundPositions = searchForTerm(term);
    assert.equal(foundPositions.length, 0, 'No terms are found when they do not exist in the text.');
  });