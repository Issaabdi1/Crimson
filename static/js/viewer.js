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
function setup(){
	//get them from the stuff
	if(savedMarks!=""){
		Mark.instanceCount = mark_id;//"{{marks.mark_id}}";
		var jsonString = decodeEntities(marksListOfSpans);//"{{marks.listOfSpans}}");
		var dict = JSON.parse(jsonString);
		listOfComments = JSON.parse(decodeEntities(marksListOfComments));//"{{marks.listOfComments}}"))
		//go through list now
		dict.forEach((entry)=>{
			var indexOfSpan = entry["index"];
			var html = entry["html"];
			var span = fromHTML(html);//JSON.parse(testList));
			const textLayerContainer = document.getElementById("textLayerContainer");
			
			var spanCopy = textLayerContainer.querySelectorAll('span[role="presentation"]')[indexOfSpan];//textLayerContainer.querySelectorAll('*')[indexOfSpan];

			spanCopy.innerHTML = "";
			spanCopy.appendChild(span);
			//add to marked spans
			var str = html;
			str = str.replace(/"/g, '\\"');
			listOfMarkedSpans.push({index:indexOfSpan, html: str});
		})
		//This adds a click event for all the highlighted spans. Do whatever is needed in the below function.
		//the code currently changes the text of a test element
		document.querySelectorAll('#markedSection').forEach(element =>{
			element.addEventListener('click', () => {
				currentMarkId = element.dataset.value;
				document.getElementById('testComment').textContent = listOfComments[currentMarkId]
			});
		})
	}
	document.dispatchEvent(setupEvent);
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

function highlightSelectedText(event){
	//clear selection
	window.getSelection().empty();
	markButton.hidden = true;
	const textLayerContainer =  document.getElementById('textLayerContainer');
	var textLayerSpans =  Array.from(textLayerContainer.querySelectorAll('span[role="presentation"]'));
	var totalLength = selectionList.toString().length;
	var offset = selectionList.startOffset;
	var selectedParts = [];
	var startIndex = textLayerSpans.indexOf(currentStartingElement.parentNode);
	var endIndex = textLayerSpans.indexOf(endingElement.parentNode);
	var elementsList = textLayerSpans.slice(startIndex, endIndex + 1);
	console.log(elementsList);
	// Assume you have an array of objects containing information about the selected parts within each span
	elementsList.forEach((element)=>{
		console.log(element);
		var part = {span: element, start: offset, end: Math.min(offset + totalLength, element.textContent.length)};//{span: element.span, start: offset, end: Math.min(offset + totalLength, element.span.textContent.length)};
		selectedParts.push(part);
		totalLength-= (part.end - part.start);
		console.log("part end is ", part.end);
		offset= 0;
	})

	//create a new mark
	var newMark = new Mark();
	var count = 0;
	// Iterate over each selected part
	selectedParts.forEach(part => {
		var highlightedSpan = highlightSpan(part.start, part.end, part.span, count==0);
		highlightedSpan.dataset.value = newMark.getId();
		//add event listener
		highlightedSpan.addEventListener('click', () => {
			currentMarkId = highlightedSpan.dataset.value;
			// Handle click event (e.g., open a modal, execute a function, etc.)
			document.getElementById('testComment').textContent = "This comment was made by mark " + highlightedSpan.dataset.value;
		});
		count+=1;
	});

	//add the span to the list of marked spans if it isn't already there
	elementsList.forEach((element)=>{
		if(!listOfMarkedSpans.includes(element)){
			//Add escape characters so that it can be parsed by JSON
			var str = element.innerHTML;
			str = str.replace(/"/g, '\\"');
			listOfMarkedSpans.push({index:textLayerSpans.indexOf(element), html: str});
		}
	});


	//Add a new entry in the dictionary, associating the mark with a comment. 
	listOfComments[newMark.getId()] =  "This comment is by mark " + newMark.getId()
	//save changes
	savePdfChanges(false);
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
	highlightSpan.classList.add('markedSection');
	highlightSpan.style.backgroundColor = 'yellow'; // Set highlight color
	highlightSpan.style.cursor = 'pointer'; // Change cursor to pointer

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


/* -------------------------------------------------------------------------------- */
/* -------------------------- VOICE RECORDING JAVASCRIPT -------------------------- */
/* -------------------------------------------------------------------------------- */

const voiceCommentLabel = document.getElementById('voiceCommentLabel');
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
    const trashIcon = document.createElement('i');
    trashIcon.className = 'fa solid fa-trash';
    deleteBtn.appendChild(trashIcon);
    deleteBtn.title = 'Delete recording';
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
		listOfSavedComments[currentMarkId].forEach(audio_url => {

			// Call functions for audio + delete button 
			var audio = createAudioElement(audio_url, false);
			var deleteBtn = createDeleteButton(() => {

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
					const index = listOfSavedComments[currentMarkId].indexOf(audio_url);
					if (index !== -1) {
						listOfSavedComments[currentMarkId].splice(index, 1);
					}
					updateVoiceComments();
				})
			});
			savedRecordings.appendChild(audio);
			savedRecordings.appendChild(deleteBtn);
		})
	}

	voiceCommentLabel.style.display = 'none';
	if (listOfSavedComments[currentMarkId]?.length > 0) {
		voiceCommentLabel.style.display = 'block';
	}
	

	// Check if save button needs to be visible
	updateSaveButton();
	checkCurrentMark();
}

// this code is only called after setup() function is completed
document.addEventListener('afterSetup', () => {
	console.log('Setup has occured.')
	checkCurrentMark();

	// Call update everytime a click occurs
	document.addEventListener('click', () => {
		updateVoiceComments();
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