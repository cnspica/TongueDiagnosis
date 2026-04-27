// 简易国际化方案 - 不依赖 vue-i18n，轻量实现
export const locales = {
  'zh-CN': {
    // Header
    appTitle: '舌诊助手',
    appSubtitle: 'AI智能舌诊',
    navHome: '首页',
    navCheck: '舌诊检测',
    login: '登录',
    logout: '退出登录',
    profile: '个人资料',
    registeredUser: '注册用户',
    langSwitch: 'EN',

    // Home
    heroBadge: 'AI驱动的中医舌诊',
    heroTitle1: '智能',
    heroTitle2: '舌诊革命',
    heroTitle3: '新时代',
    heroSubtitle: '体验前沿AI技术带来的中医舌诊革新。基于深度学习，即时获取精准舌象分析与个性化健康建议。',
    tagAI: 'AI智能分析',
    tagInstant: '即时出结果',
    tagTCM: '中医辨证',
    ctaStart: '开始诊断',
    ctaMore: '了解更多',
    featureBadge: '特色功能',
    featureTitle1: 'AI舌象分析',
    featureDesc1: '先进的深度学习算法分析舌象特征，准确率达80%以上，秒级完成中医舌诊综合分析。',
    accuracy: '准确率',
    analysisTime: '分析用时',
    featureTitle2: '健康追踪',
    featureDesc2: '通过详细报告、历史对比和个性化建议，持续追踪您的健康状态。',
    visualReport: '可视化报告',
    progressTrack: '进度追踪',
    featureTitle3: '专家咨询',
    featureDesc3: '与认证中医师在线交流，获取详细的诊疗建议和调理方案。',
    certifiedExpert: '认证专家',
    liveChat: '实时对话',

    // Check page
    sidebarTitle: '诊断记录',
    sidebarPlaceholder: '输入记录名称',
    sidebarAdd: '新增',
    sidebarEmpty: '暂无记录',
    sidebarExpand: '展开侧边栏',
    sidebarCollapse: '收起侧边栏',

    // Guide page
    guideWelcome: '欢迎开启AI舌诊之旅 👋',
    guideSubtitle: '点击左侧{action}\n获取中医舌象分析',
    guideActionView: '查看记录详情',
    guideActionNew: '新增',
    guidePrompt: '点击此处添加或查看对话',

    // Chat
    welcomeTitle: '👋 欢迎使用 **AI中医舌诊**！',
    welcomeUpload: '📸 **请先上传您的舌象图片**，AI将根据中医理论进行智能分析，并提供健康建议。',
    welcomeHowTitle: '🔍 **如何拍摄舌象？**',
    welcomeHow1: '1. 在自然光下拍摄，避免过暗或过亮。',
    welcomeHow2: '2. 放松舌头，尽量伸出，不要用力。',
    welcomeHow3: '3. 保持口腔清洁，避免食物残渣影响判断。',
    welcomeDisclaimer: '💡 **免责声明**',
    welcomeDisclaimerText: '本系统提供的分析结果仅供参考，不能替代专业医生的诊断。如有健康问题，请咨询中医师或专业医疗专家。',
    welcomeStart: '➡ **请上传您的舌象图片，让我们开始吧！**',
    thinking: '思考中...',
    voicePlay: '语音播放',
    inputPlaceholder: '请在此输入...',
    uploadHint: '上传舌象图片',

    // Dialog
    errorTimeout: '请求超时，请重试',
    errorGeneral: '遇到错误，请重试',
    errorNoSpeech: '您的浏览器不支持语音识别',
    errorSpeech: '语音识别出错，请重试',

    // AI Prompt language directive
    aiLangDirective: '请使用简体中文回答。',
  },

  'en': {
    // Header
    appTitle: 'TongueAI',
    appSubtitle: 'AI TCM Diagnosis',
    navHome: 'Home',
    navCheck: 'Diagnosis',
    login: 'Login',
    logout: 'Logout',
    profile: 'Profile',
    registeredUser: 'User',
    langSwitch: '中文',

    // Home
    heroBadge: 'AI-Powered TCM Tongue Diagnosis',
    heroTitle1: 'Smart',
    heroTitle2: 'Tongue Diagnosis',
    heroTitle3: 'Revolution',
    heroSubtitle: 'Experience the innovation of AI-powered TCM tongue diagnosis. Based on deep learning, get instant precise tongue analysis and personalized health advice.',
    tagAI: 'AI Analysis',
    tagInstant: 'Instant Results',
    tagTCM: 'TCM Diagnosis',
    ctaStart: 'Start Diagnosis',
    ctaMore: 'Learn More',
    featureBadge: 'Featured',
    featureTitle1: 'AI Tongue Analysis',
    featureDesc1: 'Advanced deep learning algorithms analyze tongue features with 80%+ accuracy, completing TCM comprehensive analysis in seconds.',
    accuracy: 'Accuracy',
    analysisTime: 'Analysis Time',
    featureTitle2: 'Health Tracking',
    featureDesc2: 'Track your health status continuously with detailed reports, historical comparisons, and personalized advice.',
    visualReport: 'Visual Reports',
    progressTrack: 'Progress Tracking',
    featureTitle3: 'Expert Consultation',
    featureDesc3: 'Communicate online with certified TCM practitioners for detailed diagnosis and treatment advice.',
    certifiedExpert: 'Certified Experts',
    liveChat: 'Live Chat',

    // Check page
    sidebarTitle: 'Records',
    sidebarPlaceholder: 'New record name',
    sidebarAdd: 'Add',
    sidebarEmpty: 'No records yet',
    sidebarExpand: 'Expand sidebar',
    sidebarCollapse: 'Collapse sidebar',

    // Guide page
    guideWelcome: 'Welcome to AI Tongue Diagnosis 👋',
    guideSubtitle: 'Click {action} on the left\nfor TCM tongue analysis',
    guideActionView: 'View Records',
    guideActionNew: 'Add New',
    guidePrompt: 'Click here to add or view conversations',

    // Chat
    welcomeTitle: '👋 Welcome to **AI TCM Tongue Diagnosis**!',
    welcomeUpload: '📸 **Please upload your tongue image first**, and AI will analyze it based on TCM theory and provide health advice.',
    welcomeHowTitle: '🔍 **How to photograph your tongue?**',
    welcomeHow1: '1. Take photos in natural light, avoid too dark or too bright.',
    welcomeHow2: '2. Relax your tongue, extend it naturally without force.',
    welcomeHow3: '3. Keep your mouth clean, avoid food residue affecting judgment.',
    welcomeDisclaimer: '💡 **Disclaimer**',
    welcomeDisclaimerText: 'The analysis results provided by this system are for reference only and cannot replace professional medical diagnosis. If you have health concerns, please consult a TCM practitioner or medical expert.',
    welcomeStart: '➡ **Please upload your tongue image to get started!**',
    thinking: 'Thinking...',
    voicePlay: 'Voice',
    inputPlaceholder: 'Type here...',
    uploadHint: 'Upload tongue image',

    // Dialog
    errorTimeout: 'Request timeout, please retry',
    errorGeneral: 'Error occurred, please retry',
    errorNoSpeech: 'Speech recognition not supported',
    errorSpeech: 'Speech recognition error, please retry',

    // AI Prompt language directive
    aiLangDirective: 'Please respond in English.',
  }
};

// 获取存储的语言或默认中文
export function getStoredLang() {
  return localStorage.getItem('tongueAiLang') || 'zh-CN';
}

export function setStoredLang(lang) {
  localStorage.setItem('tongueAiLang', lang);
}
