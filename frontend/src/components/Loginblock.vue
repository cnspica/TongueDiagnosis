<template>
  <div class="login-container">
    <el-form ref="Email_Password_login" style="max-width: 280px" :model="user" status-icon :rules="rules"
             label-width="auto" class="Email_Password_form" v-loading="loading"
             element-loading-background="rgba(10, 14, 26, 0.8)" size="large">
      <el-form-item label="" prop="Email">
        <el-input v-model="user.Email" placeholder="请输入邮箱" id="l_email" size="large"
                  class="dark-input" />
      </el-form-item>
      <el-form-item label="" prop="Password">
        <el-input v-model="user.Password" placeholder="请输入密码" id="l_password" type="password"
                  show-password size="large" class="dark-input" />
      </el-form-item>
      <el-form-item>
        <el-button class="login-btn" @click="login(Email_Password_login)" size="large">登 录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import {reactive, ref} from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
import router from '@/router';
import axios from 'axios';

const Email_Password_login = ref<FormInstance>()
let loading = ref(false)
let token = ''
let not_register = ref<boolean>(false)
let timeout = 50000

const validatePassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else if (value.length < 6) {
    callback(new Error('密码太短'))
  } else if (value.length > 20) {
    callback(new Error('密码太长'))
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

let user = reactive({
  Email: '',
  Password: '',
})

const rules = reactive<FormRules<typeof user>>({
  Email: [{validator: validateEmail, trigger: ['blur']}],
  Password: [{validator: validatePassword, trigger: ['blur']}],
})


const login = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      loading.value = true
      set_Login_post()
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

const generate_form = () => {
  const params = new URLSearchParams()
  params.append('email', user.Email.trim())
  params.append('password', user.Password.trim())
  return params
}

const set_Login_post = () => {
  axios({
    method: 'post',
    data: generate_form(),
    url: '/api/user/login',
    timeout: 20000,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
      .then(response => {
        loading.value = false
        analyze_response(response.data)
      })
      .catch(error => {
        loading.value = false
        if (error === 'ECONNABORTED') {
          loading.value = false
          fail_message('请求超时')
        } else {
          loading.value = false
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
    success_message("登录成功")
    token = data.data.token
    deliver_token(token)
    jump_home(1)
  } else {
    if (data.code === 101) {
      fail_message("用户不存在")
      not_register.value = true
    } else {
      if (data.code === 102) {
        fail_message("密码错误")
      } else {
        fail_message("遇到错误，请重试")
      }
    }
  }
}

const deliver_token = (t: string) => {
  localStorage.setItem('token', t);
}

function jump_home(seconds: any) {
  setTimeout(function () {
    router.push('./home')
  }, seconds * 1000);
}
</script>

<style scoped>
.login-container {
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

/* 密码显示按钮 */
:deep(.dark-input .el-input__suffix .el-icon) {
  color: rgba(224, 230, 240, 0.4);
}

:deep(.dark-input .el-input__suffix .el-icon:hover) {
  color: #00d4ff;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  margin-top: 16px;
  height: 42px;
  border-radius: 8px;
  font-size: 15px;
  letter-spacing: 4px;
  font-weight: 600;
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  border: none;
  color: #fff;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.25);
}

.login-btn:hover {
  background: linear-gradient(135deg, #00e5ff, #00b3e6);
  box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4);
  transform: translateY(-1px);
}

.login-btn:active {
  transform: translateY(0);
}

/* 表单验证错误文字 */
:deep(.el-form-item__error) {
  color: #ff6b6b;
}

/* ElMessage 在深色模式下 - 全局处理 */
</style>
