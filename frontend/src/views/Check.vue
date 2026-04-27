<script lang="ts" setup>
import {nextTick, onMounted, onUnmounted, ref, watch} from 'vue';
import Main from "@/components/mainPage/mainContainer.vue";
import GuidePage from "@/components/mainPage/guidePage.vue";
import axios from "axios";
import { useStateStore } from '@/stores/stateStore';

const store = useStateStore();
const showGuide = ref(true);
const guidePageRef = ref(null);
const activeItem = ref<string | null | number>(null);
const mainPageRef = ref(null);
const items = ref([]);
const newItemLabel = ref('');
let itemIdCounter = 10000000;
const sidebarCollapsed = ref(false);

// 响应式窗口宽度（修复白页根因：不能在模板中直接使用 window）
const isMobile = ref(window.innerWidth < 768);

const updateMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

onMounted(() => {
  window.addEventListener('resize', updateMobile);
});

onUnmounted(() => {
  window.removeEventListener('resize', updateMobile);
});

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value;
};

const handleItemClick = async (id: string | number) => {
  showGuide.value = false;
  await nextTick();
  console.log(`选中项: ${id}`);
  const tempTip = items.value.find(item => item.id === id).temp
  if (tempTip) {
    console.log("临时页面")
    mainPageRef.value.resetPage();
    activeItem.value = id;
    mainPageRef.value.setTempName(items.value.find(item => item.id === activeItem.value).label)
    return
  }
  axios.get("/api/model/record/" + id, {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }, timeout: 20000
  }).then(res => {
    console.log("选中页面的数据", res.data.data.records)
    const data = res.data.data.records
    mainPageRef.value.inputData(data.map(item => {
          return {
            text: item.content,
            isUser: item.role == 1,
            loading: false,
            isPicture: false,
            time: new Date(item.create_at).toLocaleString('default', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit'
            }),
          }
        }), id
    )
    activeItem.value = id;
    // 移动端点击后自动收起侧边栏
    if (isMobile.value) {
      sidebarCollapsed.value = true;
    }
  }).catch(error => {
    console.log(error);
  })
};

watch(activeItem, () => {});

const addItem = () => {
  if (!newItemLabel.value.trim()) return;
  const newItemId = ++itemIdCounter;
  items.value.push({
    id: newItemId,
    label: newItemLabel.value.trim(),
    temp: true
  });
  handleItemClick(newItemId);
  newItemLabel.value = '';
};

const removeItem = (targetId: string) => {
  items.value = items.value.filter(item => item.id !== targetId);
  if (activeItem.value === targetId) {
    activeItem.value = items.value.length ? items.value[0].id : null;
  }
};

const formatData = (data: any) => {
  return data.map(item => {
    return {
      id: item.session_id,
      label: item.name,
      temp: false
    }
  })
}

onMounted(() => {
  axios.get("/api/model/session", {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }, timeout: 40000
  }).then(res => {
    console.log("初始化数据", res.data.data)
    items.value = formatData(res.data.data)
    if (items.value.length) {
      guidePageRef.value.changeGuideText(store.t('guideActionView'))
    } else guidePageRef.value.changeGuideText(store.t('guideActionNew'))
  }).catch(error => {
    console.log(error);
  })
});

const handleBackId = (id: string) => {
  items.value[items.value.length - 1].id = id
  activeItem.value = id
  items.value[items.value.length - 1].temp = false
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') addItem();
};
</script>

<template>
  <div class="check-page">
    <div class="content">
      <!-- 可收起侧边栏 -->
      <div class="sidebar" :class="{ collapsed: sidebarCollapsed, 'mobile-open': isMobile && !sidebarCollapsed }">
        <div class="sidebar-inner">
          <div class="sidebar-head">
            <h3 class="sidebar-title" v-show="!sidebarCollapsed">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              {{ store.t('sidebarTitle') }}
            </h3>
            <button class="toggle-btn" @click="toggleSidebar" :title="sidebarCollapsed ? store.t('sidebarExpand') : store.t('sidebarCollapse')">
              <svg v-if="sidebarCollapsed" width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="sidebar-input" v-show="!sidebarCollapsed">
            <el-input v-model="newItemLabel" :placeholder="store.t('sidebarPlaceholder')" size="large" @keydown="handleKeyDown">
              <template #append>
                <el-button type="primary" @click="addItem">{{ store.t('sidebarAdd') }}</el-button>
              </template>
            </el-input>
          </div>
          <div class="sidebar-list" v-show="!sidebarCollapsed">
            <div
                v-for="item in items"
                :key="item.id"
                :class="['sidebar-item', { active: activeItem === item.id }]"
                @click="handleItemClick(item.id)"
            >
              <div class="item-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                  <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <span class="item-label">{{ item.label }}</span>
            </div>
            <div class="empty-list" v-if="items.length === 0">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" opacity="0.3">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <p>{{ store.t('sidebarEmpty') }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 移动端遮罩 -->
      <div class="sidebar-overlay" :class="{ visible: isMobile && !sidebarCollapsed }" @click="sidebarCollapsed = true"></div>

      <!-- 主内容区 -->
      <div class="main-area">
        <!-- 移动端浮动菜单按钮 -->
        <button class="mobile-menu-btn" @click="sidebarCollapsed = false" v-if="isMobile && sidebarCollapsed">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
        <GuidePage v-if="showGuide" ref="guidePageRef"/>
        <Main ref="mainPageRef" @back-id="handleBackId" v-else/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.check-page {
  background: #0d1117;
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* 侧边栏 */
.sidebar {
  width: 260px;
  height: 100%;
  background: rgba(13, 17, 23, 0.95);
  border-right: 1px solid rgba(99, 179, 237, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 10;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 48px;
}

.sidebar-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.sidebar-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 10px;
  border-bottom: 1px solid rgba(99, 179, 237, 0.08);
  min-height: 48px;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #63b3ed;
  white-space: nowrap;
  overflow: hidden;
}

.toggle-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: 1px solid rgba(99, 179, 237, 0.15);
  background: rgba(99, 179, 237, 0.05);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #63b3ed;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.toggle-btn:hover {
  background: rgba(99, 179, 237, 0.12);
  border-color: rgba(99, 179, 237, 0.3);
}

.sidebar-input {
  padding: 10px;
}

.sidebar-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
  padding: 8px 10px;
}

.sidebar-list::-webkit-scrollbar {
  width: 4px;
}

.sidebar-list::-webkit-scrollbar-thumb {
  background: rgba(99, 179, 237, 0.15);
  border-radius: 4px;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.85rem;
  color: rgba(224, 230, 240, 0.6);
  transition: all 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-item:hover {
  background: rgba(99, 179, 237, 0.08);
  color: #63b3ed;
}

.sidebar-item.active {
  background: linear-gradient(135deg, rgba(79, 142, 247, 0.2), rgba(108, 92, 231, 0.2));
  color: #63b3ed;
  border: 1px solid rgba(99, 179, 237, 0.2);
}

.item-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.item-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
  gap: 10px;
}

.empty-list p {
  font-size: 0.8rem;
  color: rgba(224, 230, 240, 0.3);
}

/* 主内容区 */
.main-area {
  flex: 1;
  padding: 0;
  min-width: 0;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.main-area > * {
  width: 100%;
}

/* 遮罩 */
.sidebar-overlay {
  display: none;
}

/* 移动端浮动按钮 */
.mobile-menu-btn {
  display: none;
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 90;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid rgba(99, 179, 237, 0.2);
  background: rgba(13, 17, 23, 0.9);
  cursor: pointer;
  color: #63b3ed;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.mobile-menu-btn:hover {
  background: rgba(99, 179, 237, 0.1);
}

/* 移动端 */
/* 侧边栏 Element Plus 深色覆盖 */
.sidebar-input :deep(.el-input__wrapper) {
  background: rgba(15, 20, 35, 0.8) !important;
  box-shadow: 0 0 0 1px rgba(99, 179, 237, 0.2) inset !important;
  border-radius: 8px 0 0 8px;
}

.sidebar-input :deep(.el-input-group__append) {
  background: rgba(0, 212, 255, 0.1) !important;
  border: 1px solid rgba(99, 179, 237, 0.2) !important;
  border-left: none !important;
  box-shadow: none !important;
  border-radius: 0 8px 8px 0;
}

.sidebar-input :deep(.el-input-group__append .el-button) {
  background: transparent !important;
  border: none !important;
  color: #00d4ff !important;
  font-weight: 600;
}

.sidebar-input :deep(.el-input-group__append .el-button:hover) {
  color: #4fe0ff !important;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 64px;
    bottom: 0;
    z-index: 100;
    width: 260px;
    transform: translateX(0);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: #0d1117;
  }

  .sidebar.collapsed {
    transform: translateX(-100%);
    width: 260px;
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .sidebar-overlay {
    display: block;
    position: fixed;
    top: 64px;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 99;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }

  .sidebar-overlay.visible {
    opacity: 1;
    visibility: visible;
  }

  .mobile-menu-btn {
    display: flex;
  }
}
</style>
