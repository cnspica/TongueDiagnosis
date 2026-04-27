<script setup>
import { ref, onMounted } from 'vue';
import { useStateStore } from '@/stores/stateStore';

const store = useStateStore();
const isLoaded = ref(false);

onMounted(() => {
  setTimeout(() => { isLoaded.value = true; }, 100);
});
</script>

<template>
  <div class="home-page">
    <!-- 粒子背景 -->
    <div class="particles">
      <div class="particle" v-for="i in 20" :key="i" :style="{
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 6 + 's',
        animationDuration: (4 + Math.random() * 4) + 's'
      }"></div>
    </div>

    <!-- 网格线背景 -->
    <div class="grid-bg"></div>

    <section class="hero-section">
      <div class="container">
        <el-row :gutter="48" align="middle">
          <el-col :xs="24" :lg="14">
            <div class="hero-content" :class="{ loaded: isLoaded }">
              <div class="tech-badge">
                <span class="badge-dot"></span>
                <span>{{ store.t('heroBadge') }}</span>
              </div>

              <h1 class="hero-title">
                <span class="line">{{ store.t('heroTitle1') }}</span>
                <span class="line highlight">{{ store.t('heroTitle2') }}</span>
                <span class="line">{{ store.t('heroTitle3') }}</span>
              </h1>

              <p class="hero-desc">{{ store.t('heroSubtitle') }}</p>

              <div class="feature-chips">
                <span class="chip">✨ {{ store.t('tagAI') }}</span>
                <span class="chip">⚡ {{ store.t('tagInstant') }}</span>
                <span class="chip">🏥 {{ store.t('tagTCM') }}</span>
              </div>

              <div class="cta-group">
                <router-link to="/check" class="btn-start">
                  <span class="btn-glow"></span>
                  <span class="btn-text">{{ store.t('ctaStart') }}</span>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" class="btn-arrow">
                    <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="currentColor" stroke-width="2.5"/>
                  </svg>
                </router-link>
                <router-link to="/check" class="btn-ghost">
                  {{ store.t('ctaMore') }}
                </router-link>
              </div>
            </div>
          </el-col>

          <el-col :xs="24" :lg="10">
            <div class="cards-area" :class="{ loaded: isLoaded }">
              <!-- 主特色卡 -->
              <div class="card-main">
                <div class="card-glow"></div>
                <div class="card-top">
                  <div class="card-icon-lg">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2L15.09 8.26L22 9L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9L8.91 8.26L12 2Z" fill="currentColor"/>
                    </svg>
                  </div>
                  <span class="card-badge">{{ store.t('featureBadge') }}</span>
                </div>
                <h3 class="card-title">{{ store.t('featureTitle1') }}</h3>
                <p class="card-desc">{{ store.t('featureDesc1') }}</p>
                <div class="stats-row">
                  <div class="stat-item">
                    <span class="stat-val">80%+</span>
                    <span class="stat-lbl">{{ store.t('accuracy') }}</span>
                  </div>
                  <div class="stat-divider"></div>
                  <div class="stat-item">
                    <span class="stat-val">&lt;40s</span>
                    <span class="stat-lbl">{{ store.t('analysisTime') }}</span>
                  </div>
                </div>
              </div>

              <!-- 小功能卡 -->
              <div class="card-sm-group">
                <div class="card-sm">
                  <div class="card-sm-icon icon-blue">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                  <h4>{{ store.t('featureTitle2') }}</h4>
                  <p>{{ store.t('featureDesc2') }}</p>
                  <div class="sm-tags">
                    <span>📊 {{ store.t('visualReport') }}</span>
                    <span>📈 {{ store.t('progressTrack') }}</span>
                  </div>
                </div>
                <div class="card-sm">
                  <div class="card-sm-icon icon-purple">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                      <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88M13 7C13 9.20914 11.2091 11 9 11C6.79086 11 5 9.20914 5 7C5 4.79086 6.79086 3 9 3C11.2091 3 13 4.79086 13 7Z" stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                  <h4>{{ store.t('featureTitle3') }}</h4>
                  <p>{{ store.t('featureDesc3') }}</p>
                  <div class="sm-tags">
                    <span>👨‍⚕️ {{ store.t('certifiedExpert') }}</span>
                    <span>💬 {{ store.t('liveChat') }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #0a0e1a;
  position: relative;
  overflow: hidden;
  color: #e0e6f0;
}

/* 粒子背景 */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(99, 179, 237, 0.5);
  border-radius: 50%;
  animation: drift linear infinite;
}

@keyframes drift {
  0% { transform: translateY(0) scale(1); opacity: 0.4; }
  50% { opacity: 1; }
  100% { transform: translateY(-120px) scale(0.3); opacity: 0; }
}

/* 网格背景 */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(99, 179, 237, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99, 179, 237, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  z-index: 0;
}

.hero-section {
  position: relative;
  z-index: 1;
  padding: 80px 0 100px;
  min-height: calc(100vh - 72px);
  display: flex;
  align-items: center;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Hero content */
.hero-content {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.hero-content.loaded {
  opacity: 1;
  transform: translateY(0);
}

.tech-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  background: rgba(99, 179, 237, 0.1);
  border: 1px solid rgba(99, 179, 237, 0.25);
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #63b3ed;
  margin-bottom: 28px;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: #63b3ed;
  border-radius: 50%;
  animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 24px;
  color: #f0f4ff;
}

.hero-title .line {
  display: block;
}

.hero-title .highlight {
  background: linear-gradient(135deg, #63b3ed, #a78bfa, #f093fb);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero-desc {
  font-size: 1.2rem;
  line-height: 1.8;
  color: rgba(224, 230, 240, 0.7);
  max-width: 580px;
  margin-bottom: 32px;
}

.feature-chips {
  display: flex;
  gap: 12px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.chip {
  padding: 8px 16px;
  background: rgba(99, 179, 237, 0.08);
  border: 1px solid rgba(99, 179, 237, 0.15);
  border-radius: 20px;
  font-size: 0.85rem;
  color: rgba(224, 230, 240, 0.8);
}

/* CTA buttons */
.cta-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-start {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 18px 36px;
  background: linear-gradient(135deg, #4f8ef7, #6c5ce7);
  border-radius: 16px;
  color: white;
  font-size: 1.15rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 24px rgba(79, 142, 247, 0.35);
}

.btn-start:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 40px rgba(79, 142, 247, 0.5);
}

.btn-glow {
  position: absolute;
  inset: -2px;
  border-radius: 18px;
  background: linear-gradient(135deg, #4f8ef7, #6c5ce7);
  filter: blur(16px);
  opacity: 0.4;
  animation: glow-pulse 2.5s ease-in-out infinite;
  z-index: -1;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

.btn-arrow {
  transition: transform 0.3s ease;
}

.btn-start:hover .btn-arrow {
  transform: translateX(4px);
}

.btn-ghost {
  display: inline-flex;
  align-items: center;
  padding: 18px 28px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  color: rgba(224, 230, 240, 0.8);
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* Cards area */
.cards-area {
  opacity: 0;
  transform: translateX(40px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.2s;
}

.cards-area.loaded {
  opacity: 1;
  transform: translateX(0);
}

.card-main {
  position: relative;
  background: rgba(16, 22, 42, 0.8);
  border: 1px solid rgba(99, 179, 237, 0.15);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.card-main:hover {
  border-color: rgba(99, 179, 237, 0.35);
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
}

.card-glow {
  position: absolute;
  top: -50%;
  right: -30%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(99, 179, 237, 0.12) 0%, transparent 70%);
  pointer-events: none;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.card-icon-lg {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #4f8ef7, #6c5ce7);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 16px rgba(79, 142, 247, 0.3);
}

.card-badge {
  padding: 4px 12px;
  background: linear-gradient(135deg, #4f8ef7, #a78bfa);
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.card-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #f0f4ff;
  margin-bottom: 12px;
}

.card-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(224, 230, 240, 0.6);
  margin-bottom: 24px;
}

.stats-row {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-val {
  font-size: 1.4rem;
  font-weight: 700;
  color: #63b3ed;
}

.stat-lbl {
  font-size: 0.8rem;
  color: rgba(224, 230, 240, 0.5);
}

.stat-divider {
  width: 1px;
  height: 32px;
  background: rgba(99, 179, 237, 0.2);
}

/* Small cards */
.card-sm-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.card-sm {
  background: rgba(16, 22, 42, 0.6);
  border: 1px solid rgba(99, 179, 237, 0.1);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.card-sm:hover {
  border-color: rgba(99, 179, 237, 0.25);
  transform: translateY(-3px);
}

.card-sm-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.icon-blue {
  background: rgba(99, 179, 237, 0.12);
  color: #63b3ed;
}

.icon-purple {
  background: rgba(167, 139, 250, 0.12);
  color: #a78bfa;
}

.card-sm h4 {
  font-size: 1.15rem;
  font-weight: 600;
  color: #f0f4ff;
  margin-bottom: 8px;
}

.card-sm p {
  font-size: 0.85rem;
  line-height: 1.5;
  color: rgba(224, 230, 240, 0.55);
  margin-bottom: 14px;
}

.sm-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.sm-tags span {
  padding: 4px 10px;
  background: rgba(99, 179, 237, 0.08);
  border-radius: 8px;
  font-size: 0.75rem;
  color: rgba(224, 230, 240, 0.6);
}

/* 响应式 */
@media (max-width: 1024px) {
  .hero-title { font-size: 3rem; }
  .hero-content { text-align: center; margin-bottom: 48px; }
  .feature-chips { justify-content: center; }
  .cta-group { justify-content: center; }
  .hero-desc { margin-left: auto; margin-right: auto; }
}

@media (max-width: 768px) {
  .hero-title { font-size: 2.5rem; }
  .hero-section { padding: 40px 0 60px; }
  .hero-content { text-align: center; }
  .cta-group { flex-direction: column; align-items: stretch; }
  .btn-start, .btn-ghost { justify-content: center; }
  .card-sm-group { grid-template-columns: 1fr; }
  .card-main h3 { font-size: 1.3rem; }
}

@media (max-width: 480px) {
  .hero-title { font-size: 2rem; }
  .hero-desc { font-size: 1rem; }
  .container { padding: 0 16px; }
  .btn-start { font-size: 1rem; padding: 16px 28px; }
  .card-main, .card-sm { padding: 20px; }
  .tech-badge { font-size: 0.8rem; }
  .chip { font-size: 0.8rem; padding: 6px 12px; }
}
</style>
