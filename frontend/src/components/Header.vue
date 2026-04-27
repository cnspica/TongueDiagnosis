<script setup>
import axios from "axios";
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStateStore } from '@/stores/stateStore'

const store = useStateStore()
const router = useRouter()
const route = useRoute()
const activeIndex = ref('')
const isAuthenticated = ref(false)
const userInfo = ref({
  name: '',
  avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
})
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

const setActiveIndex = () => {
  activeIndex.value = route.path === '/check' ? '3' : '2'
}

const fetchUserInfo = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    await router.push('/login')
    return
  }
  try {
    const res = await axios.get('/api/user/info', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.data.code === 0) {
      isAuthenticated.value = true
      if (res.data.data) {
        // 后端 UserBase 只有 ID + email，无 name 字段
        // 用 email 的 @ 前部分作为显示名
        const data = res.data.data
        const displayName = data.name || (data.email ? data.email.split('@')[0] : '用户')
        userInfo.value = { ...userInfo.value, ...data, name: displayName }
      }
    }
  } catch (error) {
    console.error('authentication failure:', error)
    localStorage.removeItem('token')
    await router.push('/login')
  }
}

const handleSelect = (key) => {
  const routes = { 1: '/home', 2: '/home', 3: '/check' }
  if (routes[key]) {
    router.push(routes[key])
    isMobileMenuOpen.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  isMobileMenuOpen.value = false
  router.push('/login')
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const toggleLang = () => {
  store.toggleLang()
}

onMounted(() => {
  setActiveIndex()
  fetchUserInfo()
  window.addEventListener('scroll', handleScroll)
})

watch(() => route.path, () => {
  setActiveIndex()
  isMobileMenuOpen.value = false
  fetchUserInfo()
})
</script>

<template>
  <header class="tech-header" :class="{ scrolled: isScrolled }">
    <div class="header-inner">
      <!-- Logo -->
      <div class="logo-area" @click="router.push('/home')">
        <div class="logo-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L15.09 8.26L22 9L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9L8.91 8.26L12 2Z" fill="currentColor"/>
          </svg>
        </div>
        <div class="logo-text">
          <span class="logo-name">{{ store.t('appTitle') }}</span>
          <span class="logo-sub">{{ store.t('appSubtitle') }}</span>
        </div>
      </div>

      <!-- Desktop Nav -->
      <nav class="desktop-nav">
        <router-link to="/home" class="nav-link" :class="{ active: activeIndex === '2' }">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2"/>
            <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>{{ store.t('navHome') }}</span>
        </router-link>
        <router-link to="/check" class="nav-link" :class="{ active: activeIndex === '3' }">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>{{ store.t('navCheck') }}</span>
        </router-link>
      </nav>

      <!-- 右侧：语言切换 + 用户 -->
      <div class="header-right">
        <button class="lang-btn" @click="toggleLang" :title="store.isZh ? 'Switch to English' : '切换为中文'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2"/>
            <path d="M2 12H22M12 2C14.5013 4.73835 15.9228 8.29203 16 12C15.9228 15.708 14.5013 19.2616 12 22C9.49872 19.2616 8.07725 15.708 8 12C8.07725 8.29203 9.49872 4.73835 12 2Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>{{ store.t('langSwitch') }}</span>
        </button>

        <div v-if="isAuthenticated" class="user-area">
          <el-dropdown trigger="click" popper-class="tech-dropdown">
            <div class="user-trigger">
              <img :src="userInfo.avatar" :alt="userInfo.name" class="user-avatar" />
              <span class="user-name">{{ userInfo.name }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item disabled>
                  <div class="dropdown-user-card">
                    <img :src="userInfo.avatar" :alt="userInfo.name" />
                    <div>
                      <div class="du-name">{{ userInfo.name }}</div>
                      <div class="du-role">{{ store.t('registeredUser') }}</div>
                    </div>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item divided @click="logout" class="logout-item">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9M16 17L21 12M21 12L16 7M21 12H9" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <span>{{ store.t('logout') }}</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <div v-else class="auth-area">
          <router-link to="/login" class="login-btn">{{ store.t('login') }}</router-link>
        </div>

        <button class="mobile-btn" @click="toggleMobileMenu">
          <svg v-if="!isMobileMenuOpen" width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2"/>
          </svg>
          <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <div class="mobile-menu" :class="{ open: isMobileMenuOpen }">
      <router-link to="/home" class="mobile-link" :class="{ active: activeIndex === '2' }" @click="isMobileMenuOpen = false">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2"/>
          <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2"/>
        </svg>
        <span>{{ store.t('navHome') }}</span>
      </router-link>
      <router-link to="/check" class="mobile-link" :class="{ active: activeIndex === '3' }" @click="isMobileMenuOpen = false">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
        </svg>
        <span>{{ store.t('navCheck') }}</span>
      </router-link>
      <button class="mobile-lang-btn" @click="toggleLang">
        🌐 {{ store.t('langSwitch') }}
      </button>
      <div v-if="isAuthenticated" class="mobile-user">
        <div class="mobile-user-info">
          <img :src="userInfo.avatar" />
          <span>{{ userInfo.name }}</span>
        </div>
        <button class="mobile-logout" @click="logout">{{ store.t('logout') }}</button>
      </div>
      <div v-else class="mobile-auth">
        <router-link to="/login" class="mobile-login" @click="isMobileMenuOpen = false">{{ store.t('login') }}</router-link>
      </div>
    </div>
  </header>
</template>

<style scoped>
.tech-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(10, 14, 26, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(99, 179, 237, 0.08);
  transition: all 0.3s ease;
  height: 64px;
}

.tech-header.scrolled {
  background: rgba(10, 14, 26, 0.95);
  border-bottom-color: rgba(99, 179, 237, 0.15);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo */
.logo-area {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #4f8ef7, #6c5ce7);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 12px rgba(79, 142, 247, 0.3);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #f0f4ff;
  line-height: 1;
}

.logo-sub {
  font-size: 0.7rem;
  color: #63b3ed;
  font-weight: 500;
}

/* Desktop Nav */
.desktop-nav {
  display: flex;
  gap: 6px;
  background: rgba(99, 179, 237, 0.06);
  border-radius: 12px;
  padding: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 10px;
  text-decoration: none;
  color: rgba(224, 230, 240, 0.6);
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #63b3ed;
  background: rgba(99, 179, 237, 0.08);
}

.nav-link.active {
  color: white;
  background: linear-gradient(135deg, #4f8ef7, #6c5ce7);
  box-shadow: 0 2px 12px rgba(79, 142, 247, 0.3);
}

/* Header Right */
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.lang-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid rgba(99, 179, 237, 0.2);
  background: rgba(99, 179, 237, 0.05);
  color: #63b3ed;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.lang-btn:hover {
  background: rgba(99, 179, 237, 0.12);
  border-color: rgba(99, 179, 237, 0.35);
}

/* User */
.user-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid rgba(99, 179, 237, 0.1);
}

.user-trigger:hover {
  background: rgba(99, 179, 237, 0.08);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(99, 179, 237, 0.3);
}

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e0e6f0;
}

.login-btn {
  padding: 8px 18px;
  background: linear-gradient(135deg, #4f8ef7, #6c5ce7);
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(79, 142, 247, 0.3);
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(79, 142, 247, 0.4);
}

/* Mobile */
.mobile-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid rgba(99, 179, 237, 0.15);
  background: transparent;
  color: #63b3ed;
  cursor: pointer;
}

.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(10, 14, 26, 0.98);
  backdrop-filter: blur(25px);
  border-bottom: 1px solid rgba(99, 179, 237, 0.1);
  padding: 20px;
  transform: translateY(-100%);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.mobile-menu.open {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  color: rgba(224, 230, 240, 0.7);
  text-decoration: none;
  font-weight: 500;
  border-radius: 10px;
  margin-bottom: 6px;
  transition: all 0.2s ease;
}

.mobile-link:hover, .mobile-link.active {
  background: linear-gradient(135deg, rgba(79, 142, 247, 0.15), rgba(108, 92, 231, 0.15));
  color: #63b3ed;
}

.mobile-lang-btn {
  width: 100%;
  padding: 12px;
  border: 1px solid rgba(99, 179, 237, 0.15);
  border-radius: 10px;
  background: rgba(99, 179, 237, 0.05);
  color: #63b3ed;
  font-size: 0.9rem;
  cursor: pointer;
  margin: 8px 0;
}

.mobile-user {
  padding-top: 12px;
  border-top: 1px solid rgba(99, 179, 237, 0.1);
  margin-top: 8px;
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.mobile-user-info img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.mobile-user-info span {
  color: #e0e6f0;
  font-weight: 600;
}

.mobile-logout {
  width: 100%;
  padding: 12px;
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 10px;
  background: rgba(239, 68, 68, 0.05);
  color: #ef4444;
  cursor: pointer;
}

.mobile-login {
  display: block;
  text-align: center;
  padding: 14px;
  background: linear-gradient(135deg, #4f8ef7, #6c5ce7);
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  margin-top: 10px;
}

@media (max-width: 1024px) {
  .desktop-nav { display: none; }
  .mobile-btn { display: flex; }
  .logo-text { display: none; }
  .user-name { display: none; }
}

@media (max-width: 768px) {
  .header-inner { padding: 0 16px; }
}
</style>

<style>
/* Dropdown (unscoped) */
.tech-dropdown {
  background: rgba(13, 17, 23, 0.98) !important;
  border: 1px solid rgba(99, 179, 237, 0.15) !important;
  border-radius: 14px !important;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5) !important;
  padding: 6px !important;
}

.tech-dropdown .el-dropdown-menu__item {
  border-radius: 10px !important;
  color: #e0e6f0 !important;
  padding: 0 !important;
  background: transparent !important;
}

.tech-dropdown .el-dropdown-menu__item:hover {
  background: rgba(99, 179, 237, 0.08) !important;
}

.tech-dropdown .el-dropdown-menu__item.is-disabled {
  opacity: 1 !important;
  cursor: default !important;
}

.dropdown-user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
}

.dropdown-user-card img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(99, 179, 237, 0.3);
}

.du-name {
  font-weight: 600;
  color: #f0f4ff;
  font-size: 0.95rem;
}

.du-role {
  font-size: 0.8rem;
  color: #63b3ed;
}

.logout-item {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 10px 12px !important;
  color: #ef4444 !important;
}

.logout-item:hover {
  background: rgba(239, 68, 68, 0.08) !important;
}
</style>
