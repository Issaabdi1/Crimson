const url = 'loremipsum.pdf';

pdfjsLib.GlobalWorkerOption.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.worker.mjs';

const loadingTask = pdfjsLib.getDocument(url);
const pdf = loadingTask.promise;

const page = pdf.getPage(1);
const scale = 1.5;
const viewport = page.getViewport({ sclae });

const canvas = document.getElementById("pdf");
const context = canvas.getContext("2d");

canvas.width = Math.floor(viewport.width * outputScale);
canvas.height = Math.floor(viewport.height * outputScale);
canvas.style.width = Math.floor(viewport.width) + "px";
canvas.style.height = Math.floor(viewport.height) + "px";

const transform = outputScale !== 1
	? [outputScale, 0, 0, outputScale, 0, 0]
	: null;

const renderContext = {
	canvasContext: context,
	transform,
	viewport,
};

page.render(renderContext);
