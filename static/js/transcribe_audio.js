// transcribe_audio.js

let mediaStream, audioContext, audioSource
const fileUploadInput = document.getElementById("file-upload-input")
const fileUploadBtn = document.getElementById("file-upload-btn")
const transcriptEl = document.getElementById("transcript")
fileUploadBtn.addEventListener("click", handleFileUpload)


async function handleFileUpload() {
const file = fileUploadInput.files[0]
if (!file) return


// add audio file to FormData object
let data = new FormData()
data.append('audioFile', file)
data.append('fileName', file.name)


// send audio file to the `view` for transcription
transcriptEl.style.color = 'black'
transcriptEl.innerText = "Transcribing..."
const rawResponse = await fetch("", {
  method: 'POST',
  body: data,
  headers: { "X-CSRFToken": '{{csrf_token}}' },
})


// handle transcript in response
const { transcript, error } = await rawResponse.json()
if (error) {
  transcriptEl.style.color = 'red'
  transcriptEl.innerText = error
} else if (transcript?.trim() === "") {
  transcriptEl.innerText = "No audio detected."
} else if (transcript) {
  transcriptEl.innerText = transcript
}
}
