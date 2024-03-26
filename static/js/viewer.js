//Class
class Mark {
	static instanceCount = 0;


	constructor() {
		this.id = Mark.instanceCount++;
		this.spanList = [];
	}

	addToList(span){
		this.spanList.push(span);
	}

	getId(){
		return this.id;
	}

	getList(){
		return this.spanList;
	}

	// Other methods and properties...
}
function fromHTML(html, trim = true) {
	 // Process the HTML string (optional trimming)
	html = trim ? html.trim() : html;
	if (!html) return null; // Return null if the HTML string is empty

	// Set up a new template element
	const template = document.createElement('template');
	
	// Set the HTML content of the template element
	template.innerHTML = html;
	
	// Clone the content of the template
	const content = template.content.cloneNode(true);

	// Return the cloned content
	return content;
}


function decodeEntities(encodedString) {
	var textarea = document.createElement('textarea');
	textarea.innerHTML = encodedString;
	return textarea.value;
}
//Other stuff

var listOfMarkedSpans = []; //list of all the spans that are marked. 
var listOfComments = {} //this should be passed in from outside.
var listOfVoiceComments = {};
var listOfSavedComments = {};
var currentMarkId;
var currentCommentId;
var originalState;
let isMark = false;

const setupEvent = new Event('afterSetup')
const saveChanges = new Event('saveChanges');

function setup(){
		
	// Load all the info and marks into the pdf
	if (savedMarks != "") {
		Mark.instanceCount = mark_id;//"{{marks.mark_id}}";
		var jsonString = decodeEntities(marksListOfSpans);//"{{marks.listOfSpans}}");
		var dict = JSON.parse(jsonString).filter(entry => entry !== null);
		listOfComments = JSON.parse(decodeEntities(marksListOfComments));//"{{marks.listOfComments}}"))
		
		//Iterate through list 
		dict.forEach((entry)=>{

			var indexOfSpan = entry["index"];
			var html = entry["html"];
			//console.log("original html is", html);
			var span = fromHTML(html);//JSON.parse(testList));
			//console.log(span);
			const textLayerContainer = document.getElementById("textLayerContainer");
			
			var spanToInsertInto = textLayerContainer.querySelectorAll('span[role="presentation"]')[indexOfSpan];//textLayerContainer.querySelectorAll('*')[indexOfSpan];

			spanToInsertInto.innerHTML = "";
			spanToInsertInto.appendChild(span);
			// Add to marked spans
			var str = html;
			str = str.replace(/"/g, '\\"');
			listOfMarkedSpans.push({index:indexOfSpan, html: str});
		})

		// This adds a click event for all the highlighted spans.
		document.querySelectorAll('#markedSection').forEach(span => {
			setupSpanClickEvent(span);
		});
	}
	document.dispatchEvent(setupEvent);

}

function renderAfterZoom() {
	console.log("REEE");
    // Render the marks after zooming without needing to load saved marks again
    if (listOfMarkedSpans.length > 0) {
        listOfMarkedSpans.forEach((entry) => {
            var indexOfSpan = entry["index"];
            var html = entry["html"];
            // Convert the string to HTML elements, ensuring to decode any HTML entities
            var span = fromHTML(html.replace(/\\"/g, '"'));
            const textLayerContainer = document.getElementById("textLayerContainer");
            var spanToInsertInto = textLayerContainer.querySelectorAll('span[role="presentation"]')[indexOfSpan];

            spanToInsertInto.innerHTML = ""; // Clear existing content
            spanToInsertInto.appendChild(span); // Insert new content
        });

        // Add click event listener for all highlighted spans to handle comment updates
    	document.querySelectorAll('#markedSection').forEach(span => {
			setupSpanClickEvent(span);	
		});
    }
	document.dispatchEvent(setupEvent);
}

markButton.addEventListener("click", highlightSelectedText);
// newMarkButton.addEventListener("click", highlightSelectedText);


var currentStartingElement;
var endingElement;
document.addEventListener('selectionchange', function(event){
	if(window.getSelection().toString().length>0){
		var selection = window.getSelection();
		selectionList = selection.getRangeAt(0).cloneRange();
		currentStartingElement = selection.getRangeAt(0).startContainer;
		if(selection.getRangeAt(0).endContainer.nodeName != "#text"){
			endingElement = currentStartingElement;
		}
		else{
			endingElement = selection.getRangeAt(0).endContainer;
		}

		if(selectionList.toString().length > 0){
			//const rect = currentStartingElement.parentNode.getBoundingClientRect();
			markButton.hidden = false;
			// Set the position of the movable element to match the clicked element
			//markButton.style.top = rect.top + 'px';
		}
		//Check if the slection inlcuides a highlighted span. If so, remove it
		var pastEndElement = false;
		selectionList.cloneContents().querySelectorAll('*').forEach((element)=>{
			if(element == endingElement){
				pastEndElement = true;
			}
			if(element.id =="markedSection" && !pastEndElement){
				//clear selection
				window.getSelection().empty();
				markButton.hidden = true;
				seenSpan = false;
				// Remove mousemove event listener when mouse button is released
				document.removeEventListener('mousemove', mouseMoveHandler);
				// Remove mouseup event listener when mouse button is released
				document.removeEventListener('mouseup', mouseUpHandler);
			}
		})

	}
});

document.addEventListener('mousedown', function(event) {
	// Check if the mouse is being held down over elements with id "textLayerContainer"
	const textLayerContainer = document.getElementById('textLayerContainer');
	if (event.target.nodeName==='SPAN' && event.target.nodeName==='SPAN' && textLayerContainer.contains(event.target)) {
		markButton.hidden = true;
		// Add mousemove event listener to track mouse movement while mouse button is held down
		document.addEventListener('mousemove', mouseMoveHandler);
	}
	else{
		//if starting from blank space, don't allow selection
		textLayerContainer.style.cssText +=';'+ "-webkit-touch-callout :none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none";
		window.getSelection().empty();
		if(event.target.nodeName!='BUTTON'){
			markButton.hidden = true;
		}
	}
	// Add mouseup event listener to detect when mouse button is released
	document.addEventListener('mouseup', mouseUpHandler);
});

var seenSpan = false;
var selectionList; 

function mouseMoveHandler(event) {
	const textLayerContainer = document.getElementById('textLayerContainer');
	if(event.target.nodeName==='SPAN' && event.target.nodeName==='SPAN' && textLayerContainer.contains(event.target)){
		const rect = event.target.getBoundingClientRect();
		// Set the position of the movable element to match the clicked element
		//markButton.style.top = rect.top + 'px';
		markButton.hidden = false;
		if(seenSpan){
			var selection = window.getSelection();
			if(selection.rangeCount>0){
				selectionList = selection.getRangeAt(0).cloneRange();
			}

			textLayerContainer.style.cssText +=';'+  "-webkit-touch-callout :text; -webkit-user-select: text; -khtml-user-select: text; -moz-user-select: text; -ms-user-select: text; user-select: text";
		}
		else{
			seenSpan = true;
		}

	}
	else{
		seenSpan = false;
		//keep selection as before
		textLayerContainer.style.cssText +=';'+ "-webkit-touch-callout :none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none";
	}
	

	//Turn off selection when over a highlighted seciton (because can't select it again)
	if(event.target.id == "markedSection"){
		//clear selection
		window.getSelection().empty();
		markButton.hidden = true;
		seenSpan = false;
		// Remove mousemove event listener when mouse button is released
		document.removeEventListener('mousemove', mouseMoveHandler);
		// Remove mouseup event listener when mouse button is released
		document.removeEventListener('mouseup', mouseUpHandler);
	}

}

/**
 * button group
 * @param event
 */
function mouseUpHandler(event) {
	// Remove mousemove event listener when mouse button is released
	document.removeEventListener('mousemove', mouseMoveHandler);
	// Remove mouseup event listener when mouse button is released
	document.removeEventListener('mouseup', mouseUpHandler);
	seenSpan = false;
	textLayerContainer.style.cssText +=';'+  "-webkit-touch-callout :text; -webkit-user-select: text; -khtml-user-select: text; -moz-user-select: text; -ms-user-select: text; user-select: text";

	// popUpMark(event)
}

/**
 * pop up the window with the mark and delete button
 */
// function popUpMark(event){
// 	setTimeout(() => {
//         const selection = window.getSelection();
//         if (!selection.isCollapsed) {
//             	const selection = window.getSelection();
// 				if (!selection.isCollapsed) { // Check if there's a selection
// 					const range = selection.getRangeAt(0).getBoundingClientRect();
// 					const buttonGroup = document.getElementById('buttonGroup');
// 					buttonGroup.style.top = (event.clientY + window.scrollY) + 'px';
// 					buttonGroup.style.left = (event.clientX + window.scrollX) + 'px';
// 					buttonGroup.style.display = 'flex';
// 				}
// 				else {
// 					document.getElementById('buttonGroup').style.display = 'none';
// 				}
//         } else {
//             document.getElementById('buttonGroup').style.display = 'none';
//         }
//     }, 10);
// }

// function popUpMarkWhenClick(event) {
//     var buttonGroup = document.getElementById("buttonGroup");
//
//     var posX = event.clientX + 10;
//     var posY = event.clientY + 10;
//
//     buttonGroup.style.left = posX + 'px';
//     buttonGroup.style.top = posY + 'px';
//     buttonGroup.style.display = 'flex';
// }




function highlightSelectedText(event) {
    // Clear selection
    window.getSelection().empty();
    markButton.hidden = true;

    const textLayerContainer = document.getElementById('textLayerContainer');
    var textLayerSpans = Array.from(textLayerContainer.querySelectorAll('span[role="presentation"]'));
    var totalLength = selectionList.toString().length;
    var offset = selectionList.startOffset;
    var selectedParts = [];
    var startIndex = textLayerSpans.indexOf(currentStartingElement.parentNode);
    var endIndex = textLayerSpans.indexOf(endingElement.parentNode);
    var elementsList = textLayerSpans.slice(startIndex, endIndex + 1);

	//create a new mark
	var newMark = new Mark();
	var count = 0;

    // Process each element in the selection
    elementsList.forEach((element) => {
        var partEnd = Math.min(offset + totalLength, element.textContent.length);
        var part = { span: element, start: offset, end: partEnd };
        selectedParts.push(part);
        totalLength -= (part.end - part.start);
        offset = 0; // Reset offset for the next span
    });

	// Iterate over each selected part
	selectedParts.forEach(part => {
		var highlightedSpan = highlightSpan(part.start, part.end, part.span, count==0);
		highlightedSpan["highlightSpan"].dataset.value = newMark.getId();
		highlightedSpan["spacesSpan"].dataset.value = newMark.getId();
		
		// Add event listeners
		setupSpanClickEvent(highlightedSpan["highlightSpan"]);

		count += 1;

        // Measure and record the width of the highlighted span
        const rect = highlightedSpan["highlightSpan"].getBoundingClientRect();
        console.log("Measured width:", rect.width);

		var highlightSpanRegex = /<span class=\\\"highlight text\\\">(.*?)<\/span>/g;

        // Store the highlighted span information, including the measured width
        var str = part.span.innerHTML;
        str = str.replace(/"/g, '\\"');
		// Replace highlight spans with just their inner text content
		str = str.replace(highlightSpanRegex, '$1');

        listOfMarkedSpans.push({
            index: textLayerSpans.indexOf(part.span),
            html: str,
        });

		listOfMarkedSpans.forEach((entry)=> {
			console.log("marks list of spans");
			console.log(entry);
		})
    });

    // Associate the mark with a comment
    listOfComments[newMark.getId()] = "This comment is by mark " + newMark.getId();
    // Save changes
    savePdfChanges();
}

// Example function to highlight selected text within a span
function highlightSpan(startOffset, endOffset, setSpan, firstElement) {
	var textNode = setSpan.firstChild; //try to always make it the starting element
	if(firstElement==true){
		textNode = currentStartingElement;
	}
	const range = document.createRange();

	// Set the range to cover the selected text within the text node
	range.setStart(textNode, startOffset);
	range.setEnd(textNode, endOffset);

	// Create a highlight span element
	const highlightSpan = document.createElement('span');
	highlightSpan.id = "markedSection";

	// ISSA CODE
	highlightSpan.classList.add('markedSection');

	highlightSpan.style.backgroundColor = 'yellow'; // Set highlight color
	highlightSpan.style.cursor = 'pointer'; // Change cursor to pointer
	highlightSpan.style.userSelect= 'none';
	// Wrap the selected text with the highlight span
	range.surroundContents(highlightSpan);

	// Create a text node with the text of the highlight span after the highlight span (to mimic it being in the text)
	const highlightText = document.createTextNode(highlightSpan.textContent);
	
	//create an empty span to separate the highlight text and the next text
	const spacesSpan = document.createElement('span');
	spacesSpan.style.userSelect = 'none';

	if(highlightSpan.nextSibling==null){
		//insert the span, and then the text before it
		setSpan.appendChild(spacesSpan);
	}
	else{
		//insert the span, and then the text before it
		setSpan.insertBefore(spacesSpan, highlightSpan.nextSibling);
	}

	// Highlight text needs to be before spaces span
	setSpan.insertBefore(highlightText, highlightSpan.nextSibling);
	
	//This means the order is text node | highlight | text | span | text
	//This allows them to be selected separately.
	return {"highlightSpan": highlightSpan, "spacesSpan":spacesSpan};
}

// Adds all the relevant actions to the general click event of highlight spans
function setupSpanClickEvent(element)
{
	element.addEventListener('click', (event) => {
		isMark = true;
		// document.getElementById("delete-mark-button-container").style.display = 'block';

		// This changes the previous selected mark back to yellow
		if(currentMarkId && currentMarkId !== element.dataset.value){
			document.querySelectorAll(`span[data-value="${currentMarkId}"]`).forEach(e =>{
				e.style.backgroundColor = 'yellow';
			})
		}
		currentMarkId = element.dataset.value;
		document.querySelectorAll(`span[data-value="${currentMarkId}"]`).forEach(e =>{
			e.style.backgroundColor = 'orange';
		})

		$.ajax({
			url: '/get_comments/',
			type: 'GET',
			data: {
				'mark_id': currentMarkId,
				'upload_id': upload_id,
			},
			success: function(response) {
				document.getElementById('addCommentBtn').style.display = 'block';
				console.log("Received JSON:", response);
				const selectedText = element.parentElement.textContent;
				// const selectedText = element.textContent;
				// popUpMarkWhenClick(event)
				console.log(event.clientX, event.clientY);

				try {
					var comments = JSON.parse(response.comments);
					console.log("Parsed comments:", comments);
					const quotationHTML = `
						<blockquote>
							<strong><em>${selectedText}</em></strong>
						</blockquote>
					`;
					var commentsHTML = '';
						comments.forEach(comment => {
							var resolvedAttribute = comment.resolved ? 'disabled' : '';
							currentCommentId = comment.comment_id;
							commentsHTML += `
								<div id="textComment-${comment.comment_id}" class="textComment" data-comment-id="${comment.comment_id}">
									<div class="card" style="border-radius: 35px; width: 350px; margin: 10px; padding: 2px; box-shadow: rgba(0, 0, 0, 0.35) 0 5px 15px;">
										<div>
											<div class="button-container">
												<button type="button" class="btn-close" aria-label="Close" onclick="deleteComment(${comment.comment_id})"></button>
											</div>
											<div class="p-2" style="display: flex; margin-top: 10px">
												<img src="${comment.avatar_url}" class="card-img-top" alt="avatar" style="margin-right: 10px;margin-top: 12px;width: 30px; height: 30px; border-radius: 30px">
												<div style="margin-top: 10px">
													<strong>${comment.commenter}</strong>
												</div>
											</div>
											<div class="updateTime p-2">
												<strong style="color: #5c636a">${comment.date}</strong>
											</div>
										</div>
										<div class="card-body">
											<p class="card-text"><textarea id="commentInputBox-${comment.comment_id}"  ${resolvedAttribute}>${comment.text}</textarea></p>
										</div>
										<div class="card-footer text-body-secondary p-3 flex-column">
											<div class="flex-column">
												<button class="btn-primary saveBtn" data-comment-id="${comment.comment_id}">save</button>
												<button class="resolveBtn btn-primary btn-outline-success" data-comment-id="${comment.comment_id}" ${resolvedAttribute}>Mark Resolved</button>
											</div>
										</div>
									</div>
								</div>`;
						});
					document.getElementById("commentsContainer").innerHTML = commentsHTML;
					document.getElementById("quotationContainer").innerHTML = quotationHTML;
					document.querySelectorAll('.card-footer .btn-primary').forEach((button, index) => {
					button.addEventListener('click', function() {
						// Find the textarea associated with this button
						var cardBody = button.closest('.card').querySelector('.card-body');
						var textarea = cardBody.querySelector('textarea');
						var commentText = textarea.value; // Get the current text from the textarea
						currentMarkId = element.dataset.value;
						var commentId = this.getAttribute('data-comment-id');

						// Assuming each comment card has a data attribute 'data-comment-id' for unique identification

						// AJAX request to update the comment
						$.ajax({
							url: '/update_comment/',
							type: 'POST',
							contentType: 'application/json',
							data: JSON.stringify({
								comment_id: commentId,
								text: commentText,
								mark_id: currentMarkId,
								upload_id: upload_id
							}),
							beforeSend: function(xhr) {
								xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
							},
							success: function(response) {
								console.log('current comment id is:', currentCommentId)
								console.log('current mark id is:', currentMarkId)
								console.log("Comment updated successfully:", response);
								document.querySelector(`#textComment-${commentId} .saveBtn`).textContent = "✅ Successfully Saved!";
								setTimeout(() => {
									document.querySelector(`#textComment-${commentId} .saveBtn`).textContent = "save";
								}, 2000);


							},
							error: function(xhr, status, error) {
								console.error("Error updating comment:", error);
							}
						});
					});
				});
				document.querySelectorAll('.resolveBtn').forEach((button, index) => {
					button.addEventListener('click', function() {
						var commentId = this.getAttribute('data-comment-id');

						currentMarkId = element.dataset.value;
						// Assuming each comment card has a data attribute 'data-comment-id' for unique identification

						// AJAX request to update the comment
						$.ajax({
							url: '/update_comment_status/',
							type: 'POST',
							contentType: 'application/json',
							data: JSON.stringify({
								comment_id: commentId,
								resolved: true
							}),
							beforeSend: function(xhr) {
								xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
							},
							success: function(response) {
								console.log("Comment marked as resolved successfully:", response);
								document.querySelector(`#textComment-${commentId} .resolveBtn`).disabled = true;
								document.querySelector(`#textComment-${commentId} .resolveBtn`).style.backgroundColor = "#d3d3d3";
								document.querySelector(`#textComment-${commentId} .resolveBtn`).textContent = "Resolved  ✅";
								document.querySelector(`#commentInputBox-${commentId}`).disabled = true;


							},
							error: function(xhr, status, error) {
								console.error("Error marking comment as resolved:", error);
								// Re-enable the button if there's an error, or handle errors appropriately
								document.querySelector(`#textComment-${commentId} .resolveBtn`).disabled = false;
							}
						});
					});
				});
				} catch (error) {
					console.error("Error parsing JSON:", error);
				}
			},
			error: function(xhr, status, error) {
				console.error("Error saving current mark ID: " + xhr.status);
				// Handle error if needed
			},
			beforeSend: function(xhr, settings) {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		});
	});
}

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Check if this cookie name matches the name we're looking for
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				// Extract and decode the cookie value
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

// Adds padding to encoded audio to ensure correct length
function addPadding(base64) {
    const padding = '='.repeat((4 - base64.length % 4) % 4);
    return base64 + padding;
}

//Send the data to the database
async function savePdfChanges(saveCommentsFlag){
	const xhttp = new XMLHttpRequest();

	let formData = new FormData();
	formData.append('upload_id', upload_id);

	// Get CSRF token from cookie
	let csrftoken = getCookie('csrftoken');

	if (!saveCommentsFlag) {
		var listOfMarkedSpansJson = JSON.stringify(listOfMarkedSpans);//JSON.stringify([listOfMarkedSpans[0].innerHTML]);//listOfMarkedSpans);
		var listOfCommentsJson = JSON.stringify(listOfComments);//JSON.stringify([listOfMarkedSpans[0].innerHTML]);//listOfMarkedSpans);
		
		// Append data to form
		formData.append('mark_id', Mark.instanceCount);
		formData.append('listOfComments', listOfCommentsJson);
		formData.append('listOfSpans', listOfMarkedSpansJson);
		xhttp.open("POST", "/save_pdf_marks/", true); 
	} else {
		var listOfVoiceCommentsJson = {};
		// Convert audio into base64 to be compatible with JSON
		for (const markId in listOfVoiceComments) {
			if (listOfVoiceComments.hasOwnProperty(markId)) {
				const blobTuple = listOfVoiceComments[markId];
				const base64array = blobTuple.map(tuple => {
					const [blob, transcript] = tuple;
					return new Promise ((resolve) => {
						const reader = new FileReader();
						reader.onload = () => {
							const b64string = reader.result.split(',')[1];
							resolve({
								blob: addPadding(b64string),
								transcript: transcript
							});
						};
						reader.readAsDataURL(blob);
					});
				});
				listOfVoiceCommentsJson[markId] = await Promise.all(base64array);
			}
		}
		var listOfVoiceCommentsJsonString = JSON.stringify(listOfVoiceCommentsJson);
		formData.append('voice-comment-list', listOfVoiceCommentsJsonString);
		xhttp.open("POST", "/save_voice_comments/", true);
	}

	// Set CSRF token in request header
	xhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xhttp.send(formData);

	//When the request has been dealt with, clear the dictionary
	xhttp.onreadystatechange = function() {
		if (this.readyState == XMLHttpRequest.DONE) {
			if (this.status === 200) {
				listOfVoiceComments = {};
				if (saveCommentsFlag) {
					listOfVoiceComments = {};
					const response = JSON.parse(this.responseText);
					const recentlySavedComments = response.recentlySavedComments;
					for (const markId in recentlySavedComments) {
						for (const comment of recentlySavedComments[markId]) {
							if (!(markId in listOfSavedComments)) {
								listOfSavedComments[markId] = [];
							}
							listOfSavedComments[markId].push(comment);
						}
					}
					document.dispatchEvent(saveChanges); // dispatch event after save of comments is complete
				}
			}
		}
	};

	return true; //Show the request has been sent successfully
}

/* Search for Term Javascript */

// Function to escape special characters in a string
function escapeRegExp(string) {
	return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

//Highlights the selected term in the content (string) provided
function highlightTerms(content, term) {
    const safeTerm = escapeRegExp(term.trim());
    const regex =  new RegExp(`(${safeTerm})`, 'gi');
	//Replace with a span with the content as well as the text and another span to preserve width
	return content.replace(regex, `<span class="highlight text">$1</span>$1<span class="highlight text"></span>`);
}



/*
Find matching words
*/
function searchForTerm(term) {
	clearSearchHighlights(); //clear old highlights
	const textLayer = document.getElementById("textLayerContainer");
    const spans = textLayer.querySelectorAll('span[role="presentation"]');
    const foundPositions = [];
    spans.forEach((span, index) => {
		//create a copy without any marked sections
		var clonedNode = span.cloneNode(true);
		//remove marked stuff from cloned node before setting its content
		clonedNode.querySelectorAll(`span`).forEach(e =>{
			e.remove();
			joinUpAdjacentTextNodes(clonedNode);
		})

        let contentToSearch =  clonedNode.innerHTML;
        const highlightedContent = highlightTerms(contentToSearch, term); 
		
        //if there was replacement (so a change in the string)
        if (highlightedContent !== contentToSearch) {
			clonedNode.innerHTML = highlightedContent;
			clonedNode.classList.add("clonedFindSpans")
			clonedNode.style.pointerEvents = "none";
			span.parentElement.insertBefore(clonedNode, span.nextSibling); //put the cloned span right before the real span
            foundPositions.push({ span: span, index: index });
        }
    });
    return foundPositions;
}



//Clears all the highlights by deleting all the clonedFindSpans in the document
function clearSearchHighlights() {
	document.querySelectorAll(`span[class="clonedFindSpans"]`).forEach(e =>{
		e.remove();
	})
}

//This is a duplicate function of the code in delete mark. Delete this one when it is merged
function joinUpAdjacentTextNodes(parentElement){
	//join up adjacent text nodes together (so they aren't separate)
	var childNodes = parentElement.childNodes;
	for (var i = 0; i < childNodes.length - 1; i++) {
		if (childNodes[i].nodeType === Node.TEXT_NODE && childNodes[i + 1].nodeType === Node.TEXT_NODE) {
			// Combine the text of adjacent text nodes
			var combinedText = childNodes[i].nodeValue + childNodes[i + 1].nodeValue;
			// Replace the first text node with the combined text
			childNodes[i].nodeValue = combinedText;
			// Remove the next text node
			parentElement.removeChild(childNodes[i + 1]);
			// Decrement the index since we removed a node
			i--;
		}
	}
}

//Update the search results (highlights) based on what is typed in the bar
function updateSearchResults() {
    const searchTerm = document.getElementById('searchTermInput').value.trim();
    if (searchTerm === "") {
        // If the search term is empty, clear all highlights
        clearSearchHighlights();
        // Optionally, reset or clear any search-related states or variables here
        foundPositions = [];
        currentPosition = -1;
    } else {
        // Perform the search and update the display as before
        foundPositions = searchForTerm(searchTerm);
        currentPosition = 0; // Reset to the first result
        if (foundPositions.length > 0) {
            moveToPosition(currentPosition);
        } else {
            // Handle no results found, e.g., show a message
        }
    }
}

document.getElementById('searchTermInput').addEventListener('input', updateSearchResults);


//Below is all moving to position code, Needs to be changed to make it clearer
function moveToPosition(index) {
    // Ensure index is within bounds
    if (index >= 0 && index < foundPositions.length) {
        const position = foundPositions[index];
        
        // Logic to scroll to the position.span or highlight it

        // I put it false for now so it doesn't scroll past the main container, just the viewer
        position.span.scrollIntoView(false);

        //position.span.scrollIntoView({ behavior: 'smooth', block: "center"});
        
        // Optionally highlight or otherwise indicate the current span
    }
}

document.getElementById('nextSearchResult').addEventListener('click', () => {
    if (foundPositions.length > 0) {
        currentPosition = (currentPosition + 1) % foundPositions.length;
        moveToPosition(currentPosition);
    }
});

document.getElementById('prevSearchResult').addEventListener('click', () => {
    if (foundPositions.length > 0) {
        currentPosition = (currentPosition - 1 + foundPositions.length) % foundPositions.length;
        moveToPosition(currentPosition);
    }
});


/* Deleting Marks Javascript */
const deleteMarkButton = document.getElementById('deleteMarkButton');
deleteMarkButton.addEventListener('click', deleteMark);


/* CURRENTLY IT DOES NOT DELETE COMMENTS PROPERLY */
function deleteMark() {
    // Ensure that a mark is selected
    if (currentMarkId !== undefined && currentMarkId !== null) {
        // Remove the span from the DOM
        document.querySelectorAll(`span[data-value="${currentMarkId}"]`).forEach(e =>{
			var parentElement = e.parentElement;
			e.remove();
			joinUpAdjacentTextNodes(parentElement);
		})

        // Remove the mark's data from listOfMarkedSpans
		listOfMarkedSpans = listOfMarkedSpans.filter(mark => !mark.html.includes(`data-value=\\"${currentMarkId}\\"`));//1


        // Remove the mark's comment from listOfComments
        delete listOfComments[currentMarkId];

        // Optionally, remove the mark's voice comments from listOfVoiceComments
        delete listOfVoiceComments[currentMarkId];

		console.log('listOfMarkedSpans',listOfMarkedSpans);
		console.log('listOfComments',listOfComments);
		console.log('listOfVoiceComments',listOfVoiceComments);
        // Clear the current mark ID
        currentMarkId = null;
		savePdfChanges(false);
		reloadComments()
    }
}

// Search Bar
document.addEventListener('DOMContentLoaded', () => {
    const viewFindbarButton = document.getElementById('viewFindbar');
    const searchSection = document.getElementById('searchSection');

    viewFindbarButton.addEventListener('click', () => {
        // Check the current display state and toggle it
        if (searchSection.style.display === 'none') {
            searchSection.style.display = 'block'; // Show the search section
            viewFindbarButton.classList.add('toggled'); // Optional: Add a class to indicate the toggle state
        } else {
            searchSection.style.display = 'none'; // Hide the search section
            viewFindbarButton.classList.remove('toggled'); // Optional: Remove the toggle state class
        }
    });
});


/* -------------------------------------------------------------------------------- */
/* -------------------------- VOICE RECORDING JAVASCRIPT -------------------------- */
/* -------------------------------------------------------------------------------- */

const voiceCommentLabel = document.getElementById('voiceCommentLabel');
const collapseMenu = document.getElementById('collapseMenu');
const playButton = document.getElementById('recordButton');
const playIcon = document.getElementById('play');
const saveButton = document.getElementById('save');
const allRecordings = document.getElementById('recordings');
const savedRecordings = document.getElementById('savedRecordings');
const savedCommentsJSON = savedRecordings.getAttribute('data-saved');
const decodedJSONString = savedCommentsJSON.replace(/\\u[\dA-Fa-f]{4}/g, match =>
  String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16)) // Convert unicode into quotation marks
);
if (decodedJSONString) {
	listOfSavedComments= JSON.parse(decodedJSONString);
}


let mediaRecorder;
let chunks = [];

// function to display delete all button if there is audio
function updateSaveButton() {
	if (allRecordings.querySelectorAll('audio').length > 0) {
		saveButton.style.display = 'block';
	} else {
		saveButton.style.display = 'none';
	}
}

// Initial call for displaying delete all button
updateSaveButton();

// Play or stop recording when clicked
playButton.addEventListener('click', () => {
	if (mediaRecorder && mediaRecorder.state === 'recording') {
		stopRecording();
		playButton.innerHTML = '<i id="play" class="fas fa-microphone" title="Start Recording"></i>&nbspRecord'
	} else {
		startRecording();
		playButton.innerHTML = '<i id="play" class="fas fa-stop" title="Stop Recording"></i>&nbspStop Recording'
	}
});

// Function to create and configure audio
function createAudioElement(audio_object, isBlob) {
    const audio = document.createElement('audio');
    audio.controls = true;
	audio.controlsList.add('nodownload');
	audio.controlsList.add('noplaybackrate');
	if (isBlob) {
		audio.src = URL.createObjectURL(audio_object);
	} else {
		audio.src = audio_object;
	}
    return audio;
}

// Function to create and configure delete buttons
function createDeleteButton(deleteFunction) {
    const deleteBtn = document.createElement('button');
	deleteBtn.innerHTML = '<i class="fa-solid fa-trash"></i>'
	deleteBtn.className = 'btn btn-danger';
    deleteBtn.addEventListener('click', deleteFunction);
    return deleteBtn;
}

// function to record user's voice
async function startRecording() {

	// Create MediaRecorder object to record audio
	const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
	mediaRecorder = new MediaRecorder(stream);
	mediaRecorder.addEventListener('dataavailable', (e) => {
		chunks.push(e.data);
	});

	// Create speechRecognition object to transcribe audio
	const recognizer = new webkitSpeechRecognition();
	var finalTranscript;
	recognizer.lang = 'en-US';
	recognizer.interimResults = true;
	recognizer.onresult = (e) => {
		finalTranscript = '';
		for (let i = e.resultIndex; i < e.results.length; ++i) {
			finalTranscript += e.results[i][0].transcript + ' ';
		}
	};
	
	mediaRecorder.addEventListener('stop', () => {

		// Initialise file for recording
		const blob = new Blob(chunks, { type: 'audio/wav' });
		
		setTimeout(() => { // Timeout used so recognizer catches up to audio
			// Stop transcription
			recognizer.stop();

			// Call functions for audio + delete button
			const audio = createAudioElement(blob, true)
			const deleteBtn = createDeleteButton(() => {
				audio.remove();
				deleteBtn.remove();
				var index = -1;
				for (let i = 0; i < listOfVoiceComments[currentMarkId].length; i++) {
					const [blobItem, transcriptItem] = listOfVoiceComments[currentMarkId][i];
					if (blobItem == blob) {
						index = i;
						break;
					}
				}
				if (index !== -1) {
					listOfVoiceComments[currentMarkId].splice(index, 1)
				}
				chunks = [];
				updateSaveButton();
			});

			// Add audio + delete button + transcript to div
			allRecordings.appendChild(audio);
			allRecordings.appendChild(deleteBtn);

			// Check if save button needs to be visible
			updateSaveButton();

			// Reset audio for the next recording
			chunks = [];

			// Update voice comment dictionary with new recording
			if (currentMarkId) {
				if (!listOfVoiceComments[currentMarkId]) {
					listOfVoiceComments[currentMarkId] = [];
				}
				listOfVoiceComments[currentMarkId].push([blob, finalTranscript]);
			}
		}, 200);
	});

	recognizer.start();
	mediaRecorder.start();
}

// function to stop recording
function stopRecording() {
	mediaRecorder.stop();
}

// function to chcek if a mark has been selected, user cannot record voice comments otherwise
function checkCurrentMark() {
	const voiceRecordContainer = document.getElementById('voiceRecordContainer');
	if (!currentMarkId) {
		voiceRecordContainer.style.display = 'none';
	} else {
		voiceRecordContainer.style.display = 'block';
	}
}

// Updates voice comments in current recordings and saved recordings dynamically
function updateVoiceComments() {
	allRecordings.innerHTML = '';
	savedRecordings.innerHTML = '';
	// Displays audio recently recorded by the user
	if (currentMarkId && listOfVoiceComments[currentMarkId]) {
		listOfVoiceComments[currentMarkId].forEach(blobTuple => {

			const [blob, transcript] = blobTuple;

			// Call functions for audio + delete button
			var audio = createAudioElement(blob, true);
			var deleteBtn = createDeleteButton(() => {
				audio.remove();
				deleteBtn.remove();
				var index = -1;
				for (let i = 0; i < listOfVoiceComments[currentMarkId].length; i++) {
					const [blobItem, transcriptItem] = listOfVoiceComments[currentMarkId][i];
					if (blobItem == blob) {
						index = i;
						break;
					}
				}
				if (index !== -1) {
					listOfVoiceComments[currentMarkId].splice(index, 1)
				}
				chunks = [];
				updateSaveButton();
			});

			// Add audio + delete button to div
			allRecordings.appendChild(audio);
			allRecordings.appendChild(deleteBtn);

		});
	}
	// Displays audio saved in the database
	if (currentMarkId && listOfSavedComments[currentMarkId]) {
		listOfSavedComments[currentMarkId].forEach(vc => {
			var audio_url = vc.audio_url;
			var audio = createAudioElement(audio_url, false);
			var card;
	
			var deleteBtn;
			if (currentUser === fileOwner) {
				deleteBtn = createDeleteButton(() => {
					if (confirm("Are you sure you want to delete this voice comment? This action is irreversible.")) {
						const csrftoken = getCookie('csrftoken');
						const formData = new FormData();
						formData.append('audio-url', audio_url);
	
						fetch('/delete_voice_comment/', {
							method: 'POST',
							headers: {
								'X-CSRFToken': csrftoken
							},
							body: formData
						})
						.then(response => {
							if (!response.ok) {
								throw new Error('Error when returning response');
							}
							return response.json();
						})
						.then(data => {
							card.remove();
							const index = listOfSavedComments[currentMarkId].findIndex(comment => comment.audio_url === audio_url);
							if (index !== -1) {
								listOfSavedComments[currentMarkId].splice(index, 1);
							}
							if (listOfSavedComments[currentMarkId].length === 0) {
								delete listOfSavedComments[currentMarkId];
							}
							updateVoiceComments();
						})
						.catch(error => {
							console.error('Error:', error);
						});
					}
				});
			}
	
			card = createCard(vc, audio, deleteBtn);
			savedRecordings.appendChild(card);
		});
	}
	

	voiceCommentLabel.style.display = 'none';
	if (currentMarkId && listOfSavedComments[currentMarkId]) {
		if (listOfSavedComments[currentMarkId].length > 0) {
			voiceCommentLabel.style.display = 'flex';
		}
	}

	// Check if save button needs to be visible
	updateSaveButton();
	checkCurrentMark();
}

// Checks voice comment as resolved
async function markAsResolved(audio_url) {
	if (confirm("Are you sure you want to mark this voice comment as resolved? This action is irreversible.")) {
		const csrftoken = getCookie('csrftoken');
		const formData = new FormData();
		formData.append('audio_url', audio_url);
		const response = await fetch('/mark_as_resolved/', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken
			},
			body: formData
		});
		if (response.ok) {
			return true;
		} else {
			console.error('Request failed: ', response.status);
			return false;
		}
	}
	return false;
}

// Voice comment cards creation
function createCard(vc, audio, deleteBtn) {
    const user = vc.username;
    const avatar_url = vc.avatar_url;
    const transcript = vc.transcript;
    const time_ago = vc.time_ago;
	const is_resolved = vc.is_resolved;
	const audio_url = vc.audio_url;

    const card = document.createElement('div');
    const cardTitle = document.createElement('div');
	const cardSubTitle = document.createElement('div');
    const cardBody = document.createElement('div');
    const cardFooter = document.createElement('div');
    const avatar = document.createElement('img');
    const username = document.createElement('span');
    const timestampText = document.createElement('span');
    const transcriptText = document.createElement('span');
    const transcriptBtn = document.createElement('button');
	const resolveBtn = document.createElement('button');

    card.classList.add('card', 'mb-3');
    cardTitle.classList.add('card-title', 'd-flex', 'justify-content-between');
    cardBody.classList.add('card-body', 'centered-text');
    cardFooter.classList.add('card-footer');
    avatar.classList.add('card-img-top');
    timestampText.classList.add('text-muted', 'text-nowrap');

    avatar.src = avatar_url;
    username.textContent = user;
    timestampText.textContent = time_ago;
    cardSubTitle.appendChild(avatar);
    cardSubTitle.appendChild(username);
	cardTitle.appendChild(cardSubTitle);
    cardTitle.appendChild(timestampText);
    cardBody.appendChild(audio);
    cardBody.appendChild(transcriptText);
    card.appendChild(cardTitle);
    card.appendChild(cardBody);
    card.appendChild(cardFooter);
    
    if (transcript) {
		transcriptText.textContent = 'Transcript: ' + transcript;
	} else {
		transcriptText.textContent = 'No transcript available';
	}
    transcriptText.style.display = "none";
    transcriptBtn.innerHTML = '<i class="fa fa-comment"></i>'
    transcriptBtn.className = 'btn btn-info btn-custom';

	if (is_resolved) {
		resolveBtn.innerHTML = 'Resolved';
        resolveBtn.disabled = true;
        resolveBtn.className = 'btn btn-success btn-custom';
	} else {
		resolveBtn.innerHTML = '<i class="fa fa-check"></i> &nbsp;Resolve';
        resolveBtn.className = 'btn btn-outline-success btn-custom';
	}
    
	cardFooter.appendChild(resolveBtn);
    cardFooter.appendChild(transcriptBtn);
    if (deleteBtn) {
        cardFooter.appendChild(deleteBtn);
    }

    transcriptBtn.addEventListener('click', function() {
        if (transcriptText.style.display == "none") {    
            transcriptText.style.display = "block";
        } else {
            transcriptText.style.display = "none";
        }
    });

	resolveBtn.addEventListener('click', function() {
		markAsResolved(audio_url)
			.then(accepted => {
			if (accepted) {
				resolveBtn.innerHTML = 'Resolved';
				resolveBtn.disabled = true;
				resolveBtn.className = 'btn btn-success btn-custom';
				const commentToUpdate = listOfSavedComments[currentMarkId].find(comment => comment.audio_url == audio_url);
				if (commentToUpdate) {
					commentToUpdate.is_resolved = true;
				}
			}
			})
			.catch(error => {
				console.error('Error:', error);
			});
	});

    return card;
}


// this code is only called after setup() function is completed
document.addEventListener('afterSetup', () => {
	checkCurrentMark();

	// Call update everytime a button / marked section is clicked
	document.addEventListener('click', e => {
		if (e.target.tagName === 'BUTTON' || e.target.classList.contains('markedSection')) {

			// Do not update the voice comments when clicking buttons located in the voice-comment menu
			if (!e.target.classList.contains('btn-custom')) {
				updateVoiceComments();
			}
		}
	});

});

// function to call save PDF changes with correct flag
saveButton.addEventListener('click' , () => {
	saveButton.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i>';
	savePdfChanges(true);
});

// Once save is complete, an event is dispatched, calling this function
document.addEventListener('saveChanges', () => {
	saveButton.innerHTML = 'Save Comments';
	updateVoiceComments();
});

// Clicking a marked section directs user to viewComments tab
document.addEventListener('click', e => {
	if (e.target.classList.contains('markedSection')) {
		const thumbnailsView = document.getElementById("thumbnailView");
		const outlineView = document.getElementById("outlineView");
		const commentView = document.getElementById("commentView");
		// const bookmarksView = document.getElementById("bookmarksView");
		thumbnailsView.style.display = "none";
        outlineView.style.display = "none";
        commentView.style.display = "block";
        // bookmarksView.style.display = "none";
	}
});

/* -------------------------------------------------------------------------------- */
/* -------------------------- TEXT COMMENT JAVASCRIPT ----------------------------- */
/* -------------------------------------------------------------------------------- */
function addComment(){
    const inputText = document.getElementById("inputText");
	if (inputText.style.display === "none") {
        inputText.style.display = "block";

    } else {
        inputText.style.display = "none";

    }
}

function saveComment() {
	var commentInput = document.getElementById("textArea").value;
	var commentBox = document.getElementById('textArea');
	console.log("text is:", commentInput)
	console.log("mark_id is:",  currentMarkId)
    $.ajax({
        url: '/save_comment/',
        type: 'POST',
        data: {
            'upload_id': upload_id,
            'mark_id': currentMarkId,
            'text': commentInput,
        },
        success: function(response) {
			console.log("text is:", commentInput)
			console.log("mark_id is:",  currentMarkId)
			commentBox.value = '';
            document.getElementById("inputText").style.display = "none";
			loadComments(upload_id, mark_id)
			simulateMarkedSectionClick(currentCommentId)
        },
        error: function(xhr, status, error) {
            console.error("Error saving comment: " + xhr.status);
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
	savePdfChanges(true)
}


function deleteComment(commentId) {
    $.ajax({
        url: '/delete_text_comment/', // Endpoint to handle comment deletion
        type: 'POST',
        data: JSON.stringify({ id: commentId }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // Handling CSRF token
        },
        success: function(response) {
            console.log('Comment deleted successfully', response);
            // Remove only the deleted comment
            $(`#textComment-${commentId}`).remove();
			loadComments(upload_id, mark_id)
			simulateMarkedSectionClick(currentCommentId)

        },
        error: function(xhr, status, error) {
            console.error("Error deleting comment:", error);
        }
    });
}

function loadComments(uploadId, markId) {
    $.ajax({
        url: `/get_comments_json/${uploadId}/${markId}/`,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            const commentsContainer = document.getElementById("commentsContainer");
            commentsContainer.innerHTML = '';
            response.comments.forEach(comment => {
                const commentElement = document.createElement("div");
                commentElement.className = "comment";
                commentElement.id = `comment-${comment.comment_id}`;

                commentElement.innerHTML = `
                    <p>${comment.text}</p>
                    <p>Comment by: ${comment.commenter}</p>
                `;
                commentsContainer.appendChild(commentElement);
            });
        },
        error: function(xhr, status, error) {
            console.error("Failed to load comments:", error);
        }
    });
}


function simulateMarkedSectionClick(markId) {
    var markedSections = document.querySelectorAll('.markedSection');
	console.log('current mark id in simulate mark section',currentMarkId)
    var targetSection = Array.from(markedSections).find(section => section.dataset.value === currentMarkId);

    if (targetSection) {
        targetSection.click();
    }
}

/**
 * reload the comment pill
 */
function reloadComments() {
  fetch('/update_comment/')
    .then(response => response.text()) // Parse the response as text
    .then(data => {
      // Replace existing content
      document.getElementById('commentsContainer').innerHTML = data;
    })
	.catch(error => {
	  if (error.name === 'NetworkError') {
		document.getElementById('commentsContainer').innerHTML = 'Network Error. Check your connection and try again.';
	  } else {
		document.getElementById('commentsContainer').innerHTML = 'Error loading comments. Please try again later.';
	  }
	  console.error(error);
	});
}