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
var currentMarkId;
const setupEvent = new Event('afterSetup')
const saveChanges = new Event('saveChanges');
var originalState;

function setup(){
		
	//Load all the info and marks into the pdf
	if(savedMarks!=""){
		Mark.instanceCount = mark_id;//"{{marks.mark_id}}";
		var jsonString = decodeEntities(marksListOfSpans);//"{{marks.listOfSpans}}");
		var dict = JSON.parse(jsonString);
		listOfComments = JSON.parse(decodeEntities(marksListOfComments));//"{{marks.listOfComments}}"))
		//go through list now


		dict.forEach((entry)=>{

			var indexOfSpan = entry["index"];
			var html = entry["html"];
			//add dataWidth attribute
			var dataWidth = entry["dataWidth"];
			//console.log("original htkl is", html);
			var span = fromHTML(html);//JSON.parse(testList));
			//console.log(span);
			const textLayerContainer = document.getElementById("textLayerContainer");
			
			var spanToInsertInto = textLayerContainer.querySelectorAll('span[role="presentation"]')[indexOfSpan];//textLayerContainer.querySelectorAll('*')[indexOfSpan];

			spanToInsertInto.innerHTML = "";
			spanToInsertInto.appendChild(span);
			//add to marked spans
			var str = html;
			str = str.replace(/"/g, '\\"');
			listOfMarkedSpans.push({index:indexOfSpan, html: str,dataWidth: dataWidth});
		})
		//This adds a click event for all the highlighted spans. Do whatever is needed in the below function.
		//the code currently changes the text of a test element
		document.querySelectorAll('#markedSection').forEach(element =>{
			element.addEventListener('click', () => {
				currentMarkId = element.dataset.value;
				document.getElementById('testComment').textContent = listOfComments[currentMarkId];			
			});
		})
		
	}
	document.dispatchEvent(setupEvent);

}

function renderAfterZoom(){
	//Render the marks after zooming. This does not require loading the saved marks, but just using the local lists
	//Go through every mark saved, and add it
	if(listOfMarkedSpans.length>0){
		listOfMarkedSpans.forEach((entry)=>{
			var indexOfSpan = entry["index"];
			var html = entry["html"];
			var span = fromHTML(html.replace(/\\"/g, '"')); //remove the escape characters from the html (as it is not JSON)
			const textLayerContainer = document.getElementById("textLayerContainer");
			
			var spanToInsertInto = textLayerContainer.querySelectorAll('span[role="presentation"]')[indexOfSpan];
			spanToInsertInto.innerHTML = "";
			spanToInsertInto.appendChild(span);
		})
		//This adds a click event for all the highlighted spans. Do whatever is needed in the below function.
		//the code currently changes the text of a test element
		document.querySelectorAll('#markedSection').forEach(element =>{
			element.addEventListener('click', () => {
				currentMarkId = element.dataset.value;
				document.getElementById('testComment').textContent = listOfComments[currentMarkId];			
			});
		})
	}
}


markButton.addEventListener("click", highlightSelectedText);
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

function mouseUpHandler(event) {
	// Remove mousemove event listener when mouse button is released
	document.removeEventListener('mousemove', mouseMoveHandler);
	// Remove mouseup event listener when mouse button is released
	document.removeEventListener('mouseup', mouseUpHandler);
	seenSpan = false;
	textLayerContainer.style.cssText +=';'+  "-webkit-touch-callout :text; -webkit-user-select: text; -khtml-user-select: text; -moz-user-select: text; -ms-user-select: text; user-select: text";
}

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

    // Process each element in the selection
    elementsList.forEach((element) => {
        var partEnd = Math.min(offset + totalLength, element.textContent.length);
        var part = { span: element, start: offset, end: partEnd };
        selectedParts.push(part);
        totalLength -= (part.end - part.start);
        offset = 0; // Reset offset for the next span
    });

    // Create a new mark
    var newMark = new Mark();
    var count = 0;

    // Iterate over each selected part
    selectedParts.forEach(part => {
        var highlightedSpan = highlightSpan(part.start, part.end, part.span, count === 0);
        highlightedSpan.dataset.value = newMark.getId();

        // Add event listener
        highlightedSpan.addEventListener('click', () => {
            currentMarkId = highlightedSpan.dataset.value;
            document.getElementById('testComment').textContent = "This comment was made by mark " + currentMarkId;
        });

        count += 1;

        // Measure and record the width of the highlighted span
        const rect = highlightedSpan.getBoundingClientRect();
        console.log("Measured width:", rect.width);


		var highlightSpanRegex = /<span class=\\\"highlight text\\\">(.*?)<\/span>/g;

        // Store the highlighted span information, including the measured width
        var str = part.span.innerHTML;
        str = str.replace(/"/g, '\\"');
		// Replace highlight spans with just their inner text content
		str = str.replace(highlightSpanRegex, '$1');

		console.log("the span html after marking:");
		console.log(str);
        listOfMarkedSpans.push({
            index: textLayerSpans.indexOf(part.span),
            html: str,
            dataWidth: rect.width.toString() // Store the width
        });
		console.log("hi");
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
	spacesSpan.style.userSelect='none';

	if(highlightSpan.nextSibling==null){
		//insert the span, and then the text before it
		setSpan.appendChild(spacesSpan);
	}
	else{
		//insert the span, and then the text before it
		setSpan.insertBefore(spacesSpan, highlightSpan.nextSibling); 
	}

	//highlgith tect needs to be before spaces span
	setSpan.insertBefore(highlightText, highlightSpan.nextSibling);
	
	//This means the order is text node | highlight | text | span | text
	//This allows them to be selected separately. 
	return highlightSpan;
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

		//pass parameters through url + "&listOfMarks=" + listOfMarksJson 
		var parameters = "?upload_id=" + upload_id  + "&mark_id=" + Mark.instanceCount  + "&listOfComments=" + listOfCommentsJson + "&listOfSpans=" + listOfMarkedSpansJson;
		formData.append('mark_id', Mark.instanceCount);
		formData.append('listOfComments', listOfCommentsJson);
		formData.append('listOfSpans', listOfMarkedSpansJson);
		xhttp.open("POST", "/save_pdf_marks/", true); 
	} else {
		var listOfVoiceCommentsJson = {};
		// Convert audio into base64 to be compatible with JSON
		for (const markId in listOfVoiceComments) {
			if (listOfVoiceComments.hasOwnProperty(markId)) {
				const blobs = listOfVoiceComments[markId];
				const base64array = blobs.map(blob => {
					return new Promise ((resolve) => {
						const reader = new FileReader();
						reader.onload = () => {
							const b64string = reader.result.split(',')[1];
							resolve(addPadding(b64string));
						};
						reader.readAsDataURL(blob);
					});
				});
				listOfVoiceCommentsJson[markId] = await Promise.all(base64array);
			}
		}
		var listOfVoiceCommentsJsonString = JSON.stringify(listOfVoiceCommentsJson);
		formData.append('voice-comment-list', listOfVoiceCommentsJsonString);
		xhttp.open("POST", "/save_pdf_comments/", true);
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
					document.dispatchEvent(saveChanges); // dispatch event after save of comments is complete
				}
			}
		}
	};

	return true; //Show the request has been sent successfully
}


/* Old Save PDF Function 

//Send the data to the database
function savePdfChanges(){
	var listOfMarkedSpansJson = JSON.stringify(listOfMarkedSpans);//JSON.stringify([listOfMarkedSpans[0].innerHTML]);//listOfMarkedSpans);
	var listOfCommentsJson = JSON.stringify(listOfComments);//JSON.stringify([listOfMarkedSpans[0].innerHTML]);//listOfMarkedSpans);

	//pass parameters through url + "&listOfMarks=" + listOfMarksJson 
	var parameters = "?upload_id=" + upload_id  + "&mark_id=" + Mark.instanceCount  + "&listOfComments=" + listOfCommentsJson + "&listOfSpans=" + listOfMarkedSpansJson;
	const xhttp = new XMLHttpRequest();
	//When the request has been dealt with, get the response
	xhttp.onreadystatechange = function() {
		if (this.readyState == XMLHttpRequest.DONE) {
			var response = JSON.parse(xhttp.response);
			
		}
	};

	let formData = new FormData();
	formData.append('upload_id', upload_id);
	formData.append('mark_id', Mark.instanceCount);
	formData.append('listOfComments', listOfCommentsJson);
	formData.append('listOfSpans', listOfMarkedSpansJson);


	xhttp.open("POST", "/save_pdf_marks/", true); 
	// Get CSRF token from cookie
	let csrftoken = getCookie('csrftoken');

	// Set CSRF token in request header
	xhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xhttp.send(formData);

	return true; //Show the request has been sent successfully
}
*/

/* Search for Term Javascript */
function escapeHtml(text) {
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}


function adjustMarkedSections() {
    // Assume we already found the search term and have highlighted it
    // Now we want to ensure the dimensions of the marked sections are preserved

    document.querySelectorAll('.markedSection').forEach(markedSection => {
        const originalWidth = markedSection.dataset.originalWidth;
        const originalHeight = markedSection.dataset.originalHeight;

        // Apply the original dimensions back to the marked section
        markedSection.style.width = originalWidth + 'px';
        markedSection.style.height = originalHeight + 'px';
    });
}

function highlightTerms(content, term) {
    const safeTerm = escapeHtml(term.trim());
    const regex = new RegExp(`(?<!\\w)(${safeTerm})(?!\\w)`, 'gi');
    return content.replace(regex, `<span class="highlight text">$1</span>`);
}


/*
Restore the width of the markedSection after search to fix visual inconsistencies
*/
function restoreOriginalWidths(foundPositions, listOfMarkedSpans) {
    foundPositions.forEach(foundPosition => {
		//console.log(foundPosition);

		const container = foundPosition.span;
		const highlights = container.querySelectorAll('.highlight');
	
		/*
		push the markedSection to the right as wrapping found element with highlight span
		causes loss of dimension
		*/
		
		highlights.forEach(highlight => {
			const width = highlight.getBoundingClientRect().width;
			let nextElement = highlight.nextElementSibling; // Start with the next sibling of highlight
			
			// Loop over all next siblings
			while (nextElement) {
				if (nextElement.classList.contains('markedSection')) {
					// Apply marginLeft to every .markedSection found
					nextElement.style.marginLeft = width + 'px';
				}
				// Move to the next sibling
				nextElement = nextElement.nextElementSibling;
			}
		});

        const markedSections = foundPosition.span.querySelectorAll('.markedSection');
       
		/*
		need to update span.index , use data-value instead because index is 
		not unique for each markedSpan
		*/
		markedSections.forEach(markedSection => {
			const dataValue = markedSection.getAttribute('data-value');
			const markedSpan = listOfMarkedSpans.find(span => span.index === foundPosition.index);
		
			// Check if this markedSection contains a .highlight element
			const highlightInside = markedSection.querySelector('.highlight');
		
			if (markedSpan && highlightInside) { // Only proceed if markedSpan is found and no highlight is inside this markedSection
				markedSection.style.width = markedSpan.dataWidth + 'px'; // Assuming dataWidth is a string with pixel units
			}
		});
    });
}

let originalStateCloned = false;

/*
Find matching words
*/
function searchForTerm(term) {
    //console.log("listOfMarkedSpans:", listOfMarkedSpans);
    // Clone the original state only if it hasn't been done before
    if (!originalStateCloned) {
		const textLayer2 = document.getElementById("textLayerContainer");
		originalState = textLayer2.cloneNode(true); // Deep clone
		originalStateCloned=true;
        console.log("Original state cloned for the first time.");
    }

    const textLayer = document.getElementById("textLayerContainer");
    const spans = textLayer.querySelectorAll('span[role="presentation"]');
    const foundPositions = [];
	
    spans.forEach((span, index) => {
        if (span.parentNode && span.parentNode.getAttribute('role') === 'presentation') {
            return; // Skip nested spans
        }

        let contentToSearch =  span.innerHTML;
		// console.log("span dataset original html");
		// console.log(span.innerHTML);
		//console.log(span.dataset.originalHtml);
        const highlightedContent = highlightTerms(contentToSearch, term);
		
        
        if (highlightedContent !== contentToSearch) {
            span.dataset.originalHtml = span.innerHTML; // Store the original HTML
            span.innerHTML = highlightedContent;
            foundPositions.push({ span: span, index: index });
        }
    });

    restoreOriginalWidths(foundPositions, listOfMarkedSpans);

    // console.log("found positions:", foundPositions);
    // foundPositions.forEach(pos => {
    //     console.log(`Index: ${pos.index}, Text: ${pos.span.textContent}`);
    // });
    return foundPositions;
}


// let foundPositions = [];
// let currentPosition = -1; // Start before the first position

function clearSearchHighlights() {
	console.log("originalState after search:");
	console.log(originalState);
    const textLayer = document.getElementById("textLayerContainer");
    // Replace the current textLayer with the original clone
    textLayer.parentNode.replaceChild(originalState, textLayer);
    
    // Re-initialize any required state after restoring the original DOM
   
	originalStateCloned = false;
}


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

document.getElementById('searchTermInput').addEventListener('input', updateSearchResults);


/* -------------------------------------------------------------------------------- */
/* -------------------------- VOICE RECORDING JAVASCRIPT -------------------------- */
/* -------------------------------------------------------------------------------- */

const voiceCommentLabel = document.getElementById('voiceCommentLabel');
const collapseMenu = document.getElementById('collapseMenu');
const playButton = document.getElementById('playCircle');
const playIcon = document.getElementById('play');
const saveButton = document.getElementById('save');
const allRecordings = document.getElementById('recordings');
const savedRecordings = document.getElementById('savedRecordings');
const animationBlocks = document.querySelectorAll('.animation-block');
const savedCommentsJSON = savedRecordings.getAttribute('data-saved');
const decodedJSONString = savedCommentsJSON.replace(/\\u[\dA-Fa-f]{4}/g, match => 
  String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16)) // Convert unicode into quotation marks
);
var listOfSavedComments = {};
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
		playIcon.classList.remove('fa-stop');
		playIcon.classList.add('fa-play');
		playIcon.setAttribute('title', 'Start Recording');
		animationBlocks.forEach(block => {
			block.style.display = 'none';
		});
	} else {
		startRecording();
		playIcon.classList.remove('fa-play');
		playIcon.classList.add('fa-stop');
		playIcon.setAttribute('title', 'Stop Recording');
		animationBlocks.forEach(block => {
			block.style.display = 'inline-block';
		});
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

// Function to create and configure reply buttons (functionality of replying not implemented)
function createReplyButton() {
	const reply = document.createElement('button');
	const replyIcon = document.createElement('i');
	replyIcon.className = 'fas fa-reply';
	reply.appendChild(replyIcon);
	reply.classList.add('button-large');
	reply.title = 'Reply to voice comment';
	return reply;
}

// Function to create and configure delete buttons
function createDeleteButton(deleteFunction) {
    const deleteBtn = document.createElement('button');
    const trashIcon = document.createElement('i');
    trashIcon.className = 'fa solid fa-trash';
    deleteBtn.appendChild(trashIcon);
	deleteBtn.classList.add('button-large');
    deleteBtn.title = 'Delete voice comment';
    deleteBtn.addEventListener('click', deleteFunction);
    return deleteBtn;
}

// function to record user's voice
async function startRecording() {
	const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
	mediaRecorder = new MediaRecorder(stream);
	mediaRecorder.addEventListener('dataavailable', (e) => {
		chunks.push(e.data);
	});

	mediaRecorder.addEventListener('stop', () => {
		// Initialise file for recording
		const blob = new Blob(chunks, { type: 'audio/wav' });

		// Call functions for audio + delete button 
		const audio = createAudioElement(blob, true)
		const deleteBtn = createDeleteButton(() => {
			audio.remove();
			deleteBtn.remove();
			const index = listOfVoiceComments[currentMarkId].indexOf(blob);
			if (index !== -1) {
				listOfVoiceComments[currentMarkId].splice(index, 1)
			}
			chunks = [];
			updateSaveButton();
		});

		// Add audio + delete button to div
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
			listOfVoiceComments[currentMarkId].push(blob);
		}
	});

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

// Functions to create user label, button and menu to sort voice comments
function createUserLabel (user, markId, userBtn) {
	const userLabel = document.createElement('div');
	userLabel.id = 'userLabel_' + user + markId;
	userLabel.appendChild(userBtn);
	userLabel.appendChild(document.createTextNode(` ${user}`));
	return userLabel;
}

function createUserButton (user, markId) {
	const userButton = document.createElement('div');
	userButton.id = 'userButton_' + user + markId;
	userButton.classList.add('collapse-button');
	const chevron = document.createElement('i');
	chevron.className = 'fas fa-chevron-right';
	userButton.appendChild(chevron);

	// Embed event listener to toggle correct menu
	userButton.addEventListener('click', function() {
		const userMenu = document.getElementById('userMenu_' + user + markId);
        if (userMenu.style.display == "none" || collapseMenu.style.display == "") {
            userMenu.style.display = "block";
            userButton.classList.add("rotate-down");
        } else {
            userMenu.style.display = "none";
            userButton.classList.remove("rotate-down");
        }
	});

	return userButton;
}

function createUserMenu (user, markId) {
	const userMenu = document.createElement('div');
	userMenu.id = 'userMenu_' + user + markId;
	userMenu.style.display = 'none';
	return userMenu;
}

// Updates voice comments in current recordings and saved recordings dynamically
function updateVoiceComments() {
	allRecordings.innerHTML = '';
	savedRecordings.innerHTML = '';
	// Displays audio recently recorded by the user
	if (currentMarkId && listOfVoiceComments[currentMarkId]) {
		listOfVoiceComments[currentMarkId].forEach(blob => {

			// Call functions for audio + delete button 
			var audio = createAudioElement(blob, true);
			var deleteBtn = createDeleteButton(() => {
				audio.remove();
				deleteBtn.remove();
				const index = listOfVoiceComments[currentMarkId].indexOf(blob);
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
		for (const user in listOfSavedComments[currentMarkId]) {

			// Create collapsible button for each user
			const userButton = createUserButton(user, currentMarkId);

			// Create user menu for each user
			const userMenu = createUserMenu(user, currentMarkId);

			// Create user label to store user and button
			const userLabel = createUserLabel(user, currentMarkId, userButton);

			// Loop over each user's voice comments
			listOfSavedComments[currentMarkId][user].forEach(audio_url => {

				// Call functions for audio + reply button 
				var audio = createAudioElement(audio_url, false);
				var replyBtn = createReplyButton();
				var deleteBtn;

				// Delete button can only be seen by the user who uploaded the PDF (subject to change)
				if (currentUser === fileOwner) {
					deleteBtn = createDeleteButton(() => {

						// Warn user that deletion is permanent
						if (confirm("Are you sure you want to delete this voice comment? This action is irreversible.")) {
							var csrftoken = getCookie('csrftoken');
							var formData = new FormData();
							formData.append('audio-url', audio_url);

							// Send request to delete audio from backend
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
							// On successful deletion, remove audio from frontend
							.then(data => {
								audio.remove();
								deleteBtn.remove();
								const index = listOfSavedComments[currentMarkId][user].indexOf(audio_url);
								if (index !== -1) {
									listOfSavedComments[currentMarkId][user].splice(index, 1);
								}
								if (listOfSavedComments[currentMarkId][user].length == 0) {
									delete listOfSavedComments[currentMarkId][user];
								}
								updateVoiceComments();
							})
						}
					});
				}

				userMenu.appendChild(audio);
				userMenu.appendChild(replyBtn);

				if (deleteBtn) {
					userMenu.appendChild(deleteBtn);
				}

			});

			savedRecordings.appendChild(userLabel);
			savedRecordings.appendChild(userMenu);
		}
	}

	voiceCommentLabel.style.display = 'none';
	if (currentMarkId && listOfSavedComments[currentMarkId]) {
		for (const comments of Object.values(listOfSavedComments[currentMarkId])) {
			if (comments.length > 0) {
				voiceCommentLabel.style.display = 'flex';
				break;
			}
		}
	}

	// Check if save button needs to be visible
	updateSaveButton();
	checkCurrentMark();
}

// this code is only called after setup() function is completed
document.addEventListener('afterSetup', () => {
	checkCurrentMark();

	// Call update everytime a button / marked section is clicked
	document.addEventListener('click', e => {
		if (e.target.tagName === 'BUTTON' || e.target.classList.contains('markedSection')) {

			// Do not update the voice comments when clicking buttons located in the voice-comment menu
			if (!e.target.classList.contains('button-large')) {
				updateVoiceComments();
			}
		}
	});

});

// function to call save PDF changes with correct flag
saveButton.addEventListener('click' , () => {
	saveButton.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i>'
	savePdfChanges(true)
});

const refreshContainer = document.getElementById('refreshContainer');
const refreshButton = document.getElementById('refresh');

// Once save is complete, an event is dispatched, calling this function
document.addEventListener('saveChanges', () => {
	saveButton.innerHTML = 'Save Comments';
	updateVoiceComments();
	refreshContainer.style.display = 'block';
});

// Reload the page when the button is clicked
refreshButton.addEventListener('click', () => {
    location.reload();
});

// Clicking a marked section directs user to viewComments tab
document.addEventListener('click', e => {
	if (e.target.classList.contains('markedSection')) {
		const thumbnailsView = document.getElementById("thumbnailView");
		const outlineView = document.getElementById("outlineView");
		const commentView = document.getElementById("commentView");
		const bookmarksView = document.getElementById("bookmarksView");
		thumbnailsView.style.display = "none";
        outlineView.style.display = "none";
        commentView.style.display = "block";
        bookmarksView.style.display = "none";
	}
});


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

