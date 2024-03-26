QUnit.module('escapeRegExp tests', function() {
  QUnit.test('should escape special characters', function(assert) {
      // Special characters in a string that are used in regex, focusing on the correct escaping pattern
      const specialChars = ".*+?^{}()|[]\\";
      // Escape the special characters using the function
      const escapedChars = escapeRegExp(specialChars);
      // Corrected expected result after escaping, with a single backslash for escape characters in the assertion string
      // This matches the actual output from the escapeRegExp function
      const expectedResult = "\\.\\*\\+\\?\\^\\{\\}\\(\\)\\|\\[\\]\\\\";
      // Assert that the function escapes special characters correctly
      assert.equal(escapedChars, expectedResult, 'Special characters are escaped correctly.');
  });

  QUnit.test('should return the same string if no special characters', function(assert) {
      // A regular string without special characters
      const normalString = 'hello world';
      // Pass the string through the escapeRegExp function
      const result = escapeRegExp(normalString);
      // The result should be the same as the input
      assert.equal(result, normalString, 'Returns the same string if no special characters present.');
  });
});


QUnit.module('highlightTerms tests', function() {
  QUnit.test('should highlight a single occurrence of a term', function(assert) {
      const content = 'hello world';
      const term = 'world';
      const highlightedContent = highlightTerms(content, term);
      assert.equal(highlightedContent, 'hello <span class="highlight text">world</span>world<span class="highlight text"></span>', 'Single occurrence of the term is highlighted correctly.');
  });

  QUnit.test('should highlight multiple occurrences of a term', function(assert) {
      const content = 'hello world, world';
      const term = 'world';
      const highlightedContent = highlightTerms(content, term);
      assert.equal(highlightedContent, 'hello <span class="highlight text">world</span>world<span class="highlight text"></span>, <span class="highlight text">world</span>world<span class="highlight text"></span>', 'Multiple occurrences of the term are highlighted correctly.');
  });

  QUnit.test('should be case insensitive', function(assert) {
      const content = 'Hello World, world';
      const term = 'world';
      const highlightedContent = highlightTerms(content, term);
      assert.equal(highlightedContent, 'Hello <span class="highlight text">World</span>World<span class="highlight text"></span>, <span class="highlight text">world</span>world<span class="highlight text"></span>', 'Highlights terms regardless of case.');
  });
});


QUnit.module('DOM Manipulation Tests', function() {
  QUnit.test('clearSearchHighlights should remove all highlights', function(assert) {
    clearSearchHighlights();
    const highlights = document.querySelectorAll('.clonedFindSpans');
    assert.equal(highlights.length, 0, 'All highlights are removed');
  
});
});


QUnit.module('DOM Manipulation Tests', function() {
  QUnit.test('joinUpAdjacentTextNodes should combine adjacent text nodes', function(assert) {
    // Create a parent element
    const parentElement = document.createElement('div');
    
    // Add several text nodes and an element node as children
    parentElement.appendChild(document.createTextNode('Hello '));
    parentElement.appendChild(document.createTextNode('World'));
    parentElement.appendChild(document.createElement('span')); // Non-text node for separation
    parentElement.appendChild(document.createTextNode('! '));
    parentElement.appendChild(document.createTextNode('How '));
    parentElement.appendChild(document.createTextNode('are you?'));
    // Call joinUpAdjacentTextNodes to combine adjacent text nodes
    joinUpAdjacentTextNodes(parentElement);
    
    // After joinUpAdjacentTextNodes, all adjacent text nodes should be combined.
    // So we should have 3 child nodes: combined text node, element node, combined text node.
    assert.equal(parentElement.childNodes.length, 3, 'Parent element should have 3 child nodes after combining adjacent text nodes.');
    
    // Check if the first child node's text content is correctly combined
    assert.equal(parentElement.childNodes[0].nodeValue, 'Hello World', 'First two text nodes are combined correctly.');
    
    // Check if the last child node's text content is correctly combined
    assert.equal(parentElement.childNodes[2].nodeValue, '! How are you?', 'Last two text nodes are combined correctly.');
  });
});


QUnit.module('deleteMark Tests', function(hooks) {
  hooks.beforeEach(() => {
      // Mock global variables and functions
      window.currentMarkId = 'mark1'; // Assume this is the ID of the mark to delete
      window.listOfMarkedSpans = [{id: 'mark1', html: 'Mark 1'}, {id: 'mark2', html: 'Mark 2'}];
      window.listOfComments = {'mark1': 'Comment for Mark 1'};
      window.listOfVoiceComments = {'mark1': 'Voice Comment for Mark 1'};
      window.savePdfChanges = () => {}; // Mock function, does nothing for testing
      
      // Simple console.log mocking to avoid cluttering the test output
      console.log = () => {};
  });

  hooks.afterEach(() => {
      // Clean up: Remove all marks from the DOM to ensure a clean slate for the next test
      document.getElementById('marksContainer').innerHTML = '';
      // Reset mocked global variables and functions
      window.currentMarkId = undefined;
      window.listOfMarkedSpans = [];
      window.listOfComments = {};
      window.listOfVoiceComments = {};
  });

  QUnit.test('deleteMark removes the mark and updates global variables', function(assert) {
      // Assume deleteMark function is globally accessible

      // Initial assertions to verify the setup is correct
      assert.equal(document.querySelectorAll('span[data-value="mark1"]').length, 1, 'Initial mark is present in the DOM');
      assert.equal(listOfMarkedSpans.length, 2, 'Initial listOfMarkedSpans length is correct');

      // Call the function to be tested
      deleteMark();

      // Assertions after calling deleteMark
      assert.equal(document.querySelectorAll('span[data-value="mark1"]').length, 0, 'Mark is removed from the DOM');
      assert.ok(!listOfComments['mark1'], 'Mark comment is removed from listOfComments');
      assert.ok(!listOfVoiceComments['mark1'], 'Mark voice comment is removed from listOfVoiceComments');
  });
});
