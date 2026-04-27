<template>
  <div class="register-container">
    <el-form ref="Email_Password_register" style="max-width: 280px; margin-top: 10px" :model="user" status-icon :rules="rules"
             label-width="auto" class="Email_Password_form" v-loading="loading"
             element-loading-background="rgba(10, 14, 26, 0.8)" size="large">
      <el-form-item label="" prop="Email">
        <el-input v-model="user.Email" placeholder="请输入邮箱" id="r_email" size="large"
                  class="dark-input" />
      </el-form-item>
      <el-form-item label="" prop="Password">
        <el-input v-model="user.Password" placeholder="设置密码" id="r_password" type="password"
                  show-password size="large" class="dark-input" />
      </el-form-item>
      <el-form-item label="" prop="checkPassword">
        <el-input v-model="user.checkPassword" placeholder="确认密码" id="r_cpassword" type="password"
                  show-password size="large" class="dark-input" />
      </el-form-item>
      <el-form-item>
        <el-button class="register-btn" @click="register(Email_Password_register)" size="large">注 册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import {reactive, ref} from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
const emit = defineEmits(["change"])

const Email_Password_register = ref<FormInstance>()
let loading = ref(false)
const timeout = 20000
let finish_register = ref<boolean>(false)

const validatePassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请设置密码'))
  } else if (value.length < 6) {
    callback(new Error('密码长度不能少于6位'))
  } else if (value.length > 20) {
    callback(new Error('密码长度不能超过20位'))
  } else {
    callback()
  }
}

const validateEmail = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入邮箱地址'));
  } else {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      callback(new Error('请输入有效的邮箱地址'));
    } else {
      callback();
    }
  }
};

const validatecheckPassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== user.Password) {
    callback(new Error("两次密码不一致"))
  } else {
    callback()
  }
}

const user = reactive({
  Email: '',
  Password: '',
  checkPassword: '',
})

const rules = reactive<FormRules<typeof user>>({
  Email: [{validator: validateEmail, trigger: ['blur']}],
  Password: [{validator: validatePassword, trigger: ['blur']}],
  checkPassword: [{validator: validatecheckPassword, trigger: 'change'}],
})

const register = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      set_Register_post()
      loading.value = true
    } else {
      fail_message("请按要求填写")
      return false
    }
  })
}

const reset = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

import axios from 'axios';

const set_Register_post = () => {
  axios.post('/api/user/register', {
    email: user.Email.trim(),
    password: user.Password.trim()
  }, {timeout: timeout})
      .then(response => {
        analyze_response(response.data)
        loading.value = false
      })
      .catch(error => {
        loading.value = false
        if (error === 'ECONNABORTED') {
          fail_message('请求超时')
        } else {
          fail_message("遇到错误，请重试")
          console.error(error);
        }
      });
}

const success_message = (message: string) => {
  ElMessage({
    showClose: true,
    message: message,
    type: 'success',
    duration: 1500
  })
}

const fail_message = (message: string) => {
  ElMessage({
    showClose: true,
    message: message,
    type: 'error',
    duration: 3000
  })
}

const analyze_response = (data: any) => {
  if (data.code === 0) {
    success_message("注册成功")
    finish_register.value = true
    jump_login(1)
  } else {
    if (data.code === 101) {
      fail_message("该账号已被注册")
    } else {
      fail_message("注册失败，请重试")
    }
  }
}

function jump_login(seconds) {
  setTimeout(function () {
    emit('change');
  }, seconds * 1000);
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.Email_Password_form {
  width: 100%;
}

/* 深色主题输入框 */
:deep(.dark-input .el-input__wrapper) {
  background: rgba(15, 20, 35, 0.8);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 8px;
  box-shadow: none;
  transition: all 0.3s;
}

:deep(.dark-input .el-input__wrapper:hover) {
  border-color: rgba(0, 212, 255, 0.4);
}

:deep(.dark-input .el-input__wrapper.is-focus) {
  border-color: #00d4ff;
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.15);
}

:deep(.dark-input .el-input__inner) {
  color: #e0e6f0;
  font-size: 14px;
}

:deep(.dark-input .el-input__inner::placeholder) {
  color: rgba(224, 230, 240, 0.3);
}

:deep(.dark-input .el-input__suffix .el-icon) {
  color: rgba(224, 230, 240, 0.4);
}

:deep(.dark-input .el-input__suffix .el-icon:hover) {
  color: #00d4ff;
}

/* 注册按钮 */
.register-btn {
  width: 100%;
  margin-top: 10px;
  height: 42px;
  border-radius: 8px;
  font-size: 15px;
  letter-spacing: 4px;
  font-weight: 600;
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
  border: none;
  color: #fff;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.25);
}

.register-btn:hover {
  background: linear-gradient(135deg, #a78bfa, #7c3aed);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
  transform: translateY(-1px);
}

.register-btn:active {
  transform: translateY(0);
}

/* 表单验证错误文字 */
:deep(.el-form-item__error) {
  color: #ff6b6b;
}
</style>
