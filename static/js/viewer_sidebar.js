// Handle the sidebar buttons function
document.addEventListener("DOMContentLoaded", function() {
    const thumbnailsView = document.getElementById("thumbnailView");
    const outlineView = document.getElementById("outlineView");
    const commentView = document.getElementById("commentView");

    // Hide all views except the thumbnails view by default
    thumbnailsView.style.display = "block";
    outlineView.style.display = "none";
    commentView.style.display = "none";

    document.getElementById("viewThumbnails").addEventListener("click", function() {
        thumbnailsView.style.display = "block";
        outlineView.style.display = "none";
        commentView.style.display = "none";
    });

    document.getElementById("viewOutline").addEventListener("click", function() {
        thumbnailsView.style.display = "none";
        outlineView.style.display = "block";
        commentView.style.display = "none";
    });

    document.getElementById("viewComments").addEventListener("click", function() {
        thumbnailsView.style.display = "none";
        outlineView.style.display = "none";
        commentView.style.display = "block";
    });
});

// Handle the thumbnails aria selected effect
document.getElementById("thumbnailsContainer").addEventListener("click", function(event) {
    const clickedThumbnail = event.target.closest(".thumbnailContainer");
    if (clickedThumbnail) {
        const allThumbnails = document.querySelectorAll(".thumbnailContainer");
        allThumbnails.forEach(thumbnail => {
            thumbnail.setAttribute("aria-selected", "false");
        });
        clickedThumbnail.setAttribute("aria-selected", "true");
    }
});

