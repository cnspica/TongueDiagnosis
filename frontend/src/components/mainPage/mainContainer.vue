<script setup lang="ts">
import Bottom from "./dialogBox.vue";
import Main from "./main.vue";
import {ref} from 'vue'

let sharedInput = ref('');
const mainRef = ref(null)
const dialogRef = ref(null)
const tempName = ref('')

const handleSendToMain = (id: number, input: string) => {
  sharedInput.value = `${id},${input}`;
};

const handleSendPicture = (info) => {
  initPage(info, tempName.value);
};

const initPage = (basePic, sessionName) => {
  mainRef.value.initPage(basePic, sessionName);
}

const inputData = (data, id) => {
  dialogRef.value.startChat()
  mainRef.value.inputData(data, id);
}

const resetPage = () => {
  mainRef.value.resetPage();
  dialogRef.value.backUploading();
}

const setTempName = (name) => {
  console.log(name);
  tempName.value = name;
}

defineExpose({inputData, resetPage, setTempName})

const handleGetReturn = (data) => {
  dialogRef.value.getReturn(data);
}

const backIdToCheck = (id) => {
  emit("back-id", id);
}

const emit = defineEmits(["back-id"])
</script>

<template>
  <div class="container-wrapper">
    <Main :receivedInput="sharedInput" ref="mainRef" @get-return="handleGetReturn" @back-id="backIdToCheck"/>
    <Bottom @send-to-main="handleSendToMain" @send-picture="handleSendPicture" ref="dialogRef"/>
  </div>
</template>

<style scoped>
.container-wrapper {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px);
  background: #0d1117;
  overflow: hidden;
  max-width: 960px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 768px) {
  .container-wrapper {
    max-width: 100%;
    height: calc(100vh - 64px);
  }
}
</style>
