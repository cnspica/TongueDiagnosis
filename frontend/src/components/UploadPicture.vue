<script setup lang="ts">
import {UploadFilled} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'

const emit = defineEmits(["success"])

function PicOnLoad(file) {
  const reader = new FileReader();
  reader.onload = function (event) {
    const base64String = event.target?.result as string;
    // FileReader 回调内数据已就绪，直接 emit，无需 setTimeout
    emit("success", {success: true, base64: base64String, fileData: file.raw});
  };
  reader.onerror = function () {
    ElMessage.error('文件读取失败，请重试');
  };
  reader.readAsDataURL(file.raw);
}

async function handleSuccess(event) {
  // 使用自定义 http-request 后由 PicOnLoad 处理
}
</script>

<template>
  <el-upload
      class="upload-demo"
      drag
      :on-change="PicOnLoad"
      :http-request="handleSuccess"
      accept=".jpg,.jpeg,.png,.bmp"
      :show-file-list="false"
      :limit="1"
  >
    <el-icon class="el-icon--upload">
      <upload-filled/>
    </el-icon>
    <div class="el-upload__text">
      将文件拖到此处，或<em>点击此处上传照片</em>
    </div>
  </el-upload>
</template>

<style scoped>
.upload-demo {
  width: 100%;
  max-width: 500px;
  height: 180px;
}

:deep(.el-upload-dragger) {
  background-color: rgba(15, 20, 35, 0.8) !important;
  border: 2px dashed rgba(0, 212, 255, 0.3) !important;
  border-radius: 8px;
  color: #e0e6f0;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: all 0.3s;
}

:deep(.el-upload-dragger:hover) {
  border-color: rgba(0, 212, 255, 0.6) !important;
  background-color: rgba(15, 20, 35, 0.95) !important;
}

:deep(.el-icon--upload) {
  font-size: 50px;
  color: #00d4ff;
}

:deep(.el-upload__text) {
  font-size: 16px;
  font-weight: bold;
  color: rgba(224, 230, 240, 0.6);
}

:deep(.el-upload__text em) {
  color: #00d4ff;
  font-style: normal;
}
</style>
