<template>
  <div class="logo">
    <img src="../assets/logo.png" alt="Wipro logo" />
  </div>
  <div class="details">
    <h1>Text Detection From Files</h1>
  </div>
  <div class="files">
    <input type="file" ref="fileInput" @change="handleFileSelect" multiple accept=".pdf, .doc, .jpeg, .jpg, .png, .docx" />
    <Spinner v-if="loading" />
    <div class="buttons">
      <button :disabled="!fileInput" @click="uploadFile">Generate</button>
      <button :disabled="!fileUploaded" @click="downloadFile">Download</button>
      <button
        :disabled="!fileUploaded"
        @click="clearFiles">
        Clear
      </button>
    </div>
  </div>
</template>

<script setup>
import Spinner from "./Spinner.vue";
import axios from "axios";
import { ref } from "vue";

const files = ref([])

const fileInput = ref(null);
const fileDownload = ref(null);
const fileUploaded = ref(false);
const loading = ref(false);

const handleFileSelect = (event) => {
  files.value = event.target.files
}

const uploadFile = async () => {
  const formData = new FormData()
  for (const file of files.value) {
    formData.append('files', file)
  }

  try {
    loading.value = true
    await axios.post('http://localhost:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    files.value = []
    console.log('Files uploaded successfully')
    fileUploaded.value = true;
    loading.value = false
  } catch (error) {
    console.error(error)
  }
};

const clearFiles = () => {
  files.value = [];
  fileInput.value.value = "";
  fileDownload.value = null;
  fileUploaded.value = false;
  removeDirectory();
};

const downloadFile = async () => {
  const downloadURL = `http://localhost:5000/download/`;
  const fileDownloadName ="result.xlsx"; 
  try {
    const response = await fetch(downloadURL, {
      method: "GET",
    });

    console.log("Server response:", response.status, response.statusText);

    if (response.ok) {
      fileDownload.value = await response.blob();
      const url = window.URL.createObjectURL(fileDownload.value);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileDownloadName);

      document.body.appendChild(link);
      link.click();

      document.body.removeChild(link);
      console.log("File downloaded");
    }
  } catch (error) {
    console.error("Error uploading file:", error);
  }
};

const removeDirectory = async () => {
  try {
    const response = await fetch("http://localhost:5000/cleardata", {
      method: "GET",
    });

    console.log("Server response:", response.status, response.statusText);

    if (response.ok) {
      console.log("Directory removed");
    }
  } catch (error) {
    console.error("Error removing files:", error);
  }
};

</script>

<style scoped>
img {
  position:absolute;
  left:0;
  top:0;
  padding-top: 20px;
  height: 150px;
  width: 280px;
}

h1{
  padding-top: 30px;
  position: absolute ;
  top: 0;
  left: 50%;
  transform: translate(-50%, 0%);
}

.files {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.files input {
  width: 200px;
  scale: 1.5;
  outline: 2px solid rgb(138, 138, 174);
  margin: 15px;
}

.buttons {
  width: 350px;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results {
  width: 100vw;
  display: flex;
  justify-content: space-around;
  align-items: center;
  flex-wrap: wrap;
}

.cards {
  max-width: 40%;
  max-height: 600px;
  overflow-y: scroll;
}

.cards::-webkit-scrollbar {
  display: none;
}
</style>
