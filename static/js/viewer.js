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
			const textLayer = document.getElementById("textLayer");
			var spanCopy = textLayer.children[indexOfSpan];
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
				document.getElementById('testComment').textContent = listOfComments[element.dataset.value]
			});
		})
	}
}

markButton.addEventListener("click", highlightSelectedText);
var elementsSelected = []; 
var currentStartingElement;
document.addEventListener('selectionchange', function(event){
	if(window.getSelection().toString().length>0){
		var selection = window.getSelection();
		selectionList = selection.getRangeAt(0).cloneRange();
		currentStartingElement = selection.getRangeAt(0).startContainer;
		if(elementsSelected.length >0){
			const rect = elementsSelected[0].span.getBoundingClientRect();
			markButton.hidden = false;
			// Set the position of the movable element to match the clicked element
			markButton.style.top = rect.top + 'px';
		}
	}
});

document.addEventListener('mousedown', function(event) {
	// Check if the mouse is being held down over elements with id "textLayer"
	const textLayer = document.getElementById('textLayer');
	if (event.target.nodeName==='SPAN' && event.target.nodeName==='SPAN' && textLayer.contains(event.target)) {
		markButton.hidden = true;
		// Add mousemove event listener to track mouse movement while mouse button is held down
		document.addEventListener('mousemove', mouseMoveHandler);
		if(!elementsSelected.some(obj => obj.span === event.target)){//!elementsSelected.includes(event.target)){
			var index = Array.prototype.indexOf.call(textLayer.children, event.target);
			elementsSelected.push({index:index, span:event.target});
		}
	}
	else{
		//if starting from blank space, don't allow selection
		textLayer.style.cssText +=';'+ "-webkit-touch-callout :none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none";
		window.getSelection().empty();
		if(event.target.nodeName!='BUTTON'){
			markButton.hidden = true;
		}
	}
	// Add mouseup event listener to detect when mouse button is released
	document.addEventListener('mouseup', mouseUpHandler);
});
var clearedElements = false;
var seenSpan = false;
var selectionList; 
function mouseMoveHandler(event) {
	const textLayer = document.getElementById('textLayer');
	if(event.target.nodeName==='SPAN' && event.target.nodeName==='SPAN' && textLayer.contains(event.target)){
		const rect = event.target.getBoundingClientRect();
		// Set the position of the movable element to match the clicked element
		markButton.style.top = rect.top + 'px';
		markButton.hidden = false;
		if(seenSpan){
			if(!elementsSelected.some(obj => obj.span === event.target)){//!elementsSelected.includes(event.target)){
				var index = Array.prototype.indexOf.call(textLayer.children, event.target);
				elementsSelected.push({index:index, span:event.target});
			}
			var selection = window.getSelection();
			if(selection.rangeCount>0){
				selectionList = selection.getRangeAt(0).cloneRange();
			}

			textLayer.style.cssText +=';'+  "-webkit-touch-callout :text; -webkit-user-select: text; -khtml-user-select: text; -moz-user-select: text; -ms-user-select: text; user-select: text";
		}
		else{
			seenSpan = true;
			if(!clearedElements){
				clearedElements = true;
				elementsSelected = [];
			}
		}

	}
	else{
		seenSpan = false;
		//keep selection as before
		textLayer.style.cssText +=';'+ "-webkit-touch-callout :none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none";
	}
	
	//Turn off selection when over a highlighted seciton (because can't select it again)
	if(event.target.id == "markedSection"){
		//clear selection
		window.getSelection().empty();
		markButton.hidden = true;
		seenSpan = false;
		console.log("hide");
		elementsSelected = [];
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
	clearedElements = false;
	textLayer.style.cssText +=';'+  "-webkit-touch-callout :text; -webkit-user-select: text; -khtml-user-select: text; -moz-user-select: text; -ms-user-select: text; user-select: text";
}

function highlightSelectedText(event){
	//clear selection
	window.getSelection().empty();
	markButton.hidden = true;
	var totalLength = selectionList.toString().length;
	var offset = selectionList.startOffset;
	var selectedParts = [];
	// Assume you have an array of objects containing information about the selected parts within each span
	elementsSelected.forEach((element)=>{
		console.log(element);
		var part = {span: element.span, start: offset, end: Math.min(offset + totalLength, element.span.textContent.length)};
		selectedParts.push(part);
		totalLength-= (part.end - part.start);
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
			// Handle click event (e.g., open a modal, execute a function, etc.)
			console.log('Id is ', highlightedSpan.dataset.value);
			document.getElementById('testComment').textContent = "This comment was made by mark " + highlightedSpan.dataset.value;
		});
		count+=1;
	});

	//add to list of spans
	elementsSelected.forEach((element)=>{
		if(!listOfMarkedSpans.includes(element)){
			//Add escape characters so that it can be parsed by JSON
			var str = element.span.innerHTML;
			str = str.replace(/"/g, '\\"');
			listOfMarkedSpans.push({index:element.index, html: str});
			console.log(element.index);
			console.log(str);
		}
	});

	//listOfMarks.push(newMark);
	listOfComments[newMark.getId()] =  "This comment is by mark " + newMark.getId()
	//save changes
	savePdfChanges();
	clearSelections();
}

// Example function to highlight selected text within a span
function highlightSpan(startOffset, endOffset, setSpan, firstElement) {
	var textNode = setSpan.firstChild; //try to always make it the starting element
	if(firstElement==true){
		textNode = currentStartingElement;
		console.log(currentStartingElement);
	}
	const range = document.createRange();

	console.log("Text node is ", textNode);
	// Set the range to cover the selected text within the text node
	range.setStart(textNode, startOffset);
	range.setEnd(textNode, endOffset);

	// Create a highlight span element
	const highlightSpan = document.createElement('span');
	highlightSpan.id = "markedSection";
	highlightSpan.style.backgroundColor = 'yellow'; // Set highlight color
	highlightSpan.style.cursor = 'pointer'; // Change cursor to pointer

	// Wrap the selected text with the highlight span
	range.surroundContents(highlightSpan);

	// Create a text node with the text of the highlight span after the highlight span (to mimic it being in the text)
	const highlightText = document.createTextNode(highlightSpan.textContent);
	
	//create an empty span to separate the highlight text and the next text
	const spacesSpan = document.createElement('span');
	spacesSpan.style.userSelect='none';

	//insert the span, and then the text before it
	setSpan.insertBefore(spacesSpan, highlightSpan.nextSibling); 
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

//Send the data to the database
function savePdfChanges(){
	//get the upload id
	//var upload_id = "{{ upload.id }}";
	console.log(listOfComments);
	//serialize the list of marks and the list of spans
	//var listOfMarksJson = JSON.stringify(listOfMarks);
	var listOfMarkedSpansJson = JSON.stringify(listOfMarkedSpans);//JSON.stringify([listOfMarkedSpans[0].innerHTML]);//listOfMarkedSpans);
	var listOfCommentsJson = JSON.stringify(listOfComments);//JSON.stringify([listOfMarkedSpans[0].innerHTML]);//listOfMarkedSpans);

	console.log(listOfCommentsJson)
	console.log("Mark instance count is ", Mark.instanceCount)
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

	// Add other variables as needed

	//xhr.send(formData);
	//xhttp.open("POST", "/save_pdf_marks/" + parameters, true); 
	xhttp.open("POST", "/save_pdf_marks/", true); 
	// Get CSRF token from cookie
	let csrftoken = getCookie('csrftoken');

	// Set CSRF token in request header
	xhttp.setRequestHeader("X-CSRFToken", csrftoken);
	//xhttp.send();
	xhttp.send(formData);

	return true; //Show the request has been sent successfully
}