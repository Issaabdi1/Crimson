QUnit.module('Viewer-sidebar', {
    beforeEach: function () {
        // Setup
        viewThumbnails = document.getElementById('viewThumbnails');
        viewOutline = document.getElementById('viewOutline');
        viewComments = document.getElementById('viewComments');

        thumbnailView = document.getElementById('thumbnailView');
        outlineView = document.getElementById('outlineView');
        commentView = document.getElementById('commentView');

        viewThumbnails.addEventListener("click", function () {
            thumbnailView.style.display = "block";
            outlineView.style.display = "none";
            commentView.style.display = "none";
        });

        viewOutline.addEventListener("click", function () {
            thumbnailView.style.display = "none";
            outlineView.style.display = "block";
            commentView.style.display = "none";
        });

        viewComments.addEventListener("click", function () {
            thumbnailView.style.display = "none";
            outlineView.style.display = "none";
            commentView.style.display = "block";
        });

        thumbnailsContainer = document.getElementById('thumbnailsContainer');

        thumbnailsContainer.addEventListener("click", function (event) {
            const clickedThumbnail = event.target.closest(".thumbnailContainer");
            if (clickedThumbnail) {
                const allThumbnails = document.querySelectorAll(".thumbnailContainer");
                allThumbnails.forEach(thumbnail => {
                    thumbnail.setAttribute("aria-selected", "false");
                });
                clickedThumbnail.setAttribute("aria-selected", "true");
            }
        });
    }
});

QUnit.test('test view default display', function (assert) {
    assert.equal(thumbnailView.style.display, 'block');
    assert.equal(outlineView.style.display, 'none');
    assert.equal(commentView.style.display, 'none');
});

QUnit.test('test side bar buttons', function (assert) {
    viewOutline.click();
    assert.equal(thumbnailView.style.display, 'none');
    assert.equal(outlineView.style.display, 'block');
    assert.equal(commentView.style.display, 'none');
    viewThumbnails.click();
    assert.equal(thumbnailView.style.display, 'block');
    assert.equal(outlineView.style.display, 'none');
    assert.equal(commentView.style.display, 'none');
    viewComments.click();
    assert.equal(thumbnailView.style.display, 'none');
    assert.equal(outlineView.style.display, 'none');
    assert.equal(commentView.style.display, 'block');
});

QUnit.test('test thumbnail default display', function (assert) {
    const allThumbnails = document.querySelectorAll(".thumbnailContainer");
    assert.equal(allThumbnails[0].getAttribute("aria-selected"), "true");
    assert.equal(allThumbnails[1].getAttribute("aria-selected"), "false");
});

QUnit.test('test thumbnail click', function (assert) {
    const allThumbnails = document.querySelectorAll(".thumbnailContainer");
    allThumbnails[1].click();
    assert.equal(allThumbnails[0].getAttribute("aria-selected"), "false");
    assert.equal(allThumbnails[1].getAttribute("aria-selected"), "true");
    allThumbnails[0].click();
    assert.equal(allThumbnails[0].getAttribute("aria-selected"), "true");
    assert.equal(allThumbnails[1].getAttribute("aria-selected"), "false");
});