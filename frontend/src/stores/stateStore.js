import {defineStore} from 'pinia';
import settings from '../config/config.js';
import {locales, getStoredLang, setStoredLang} from '../i18n/index.js';

export const useStateStore = defineStore('state', {
    state: () => ({
        isOpenValue: 0,
        userImagePath: "./static/userDefault.jpg",
        aiImagePath: "./static/aiDefault.jpg",
        audioType: 'D',
        baseUrl: "/api/model/session",
        chatHistory: [],
        infoHistory: [],
        isPlayed: false,
        gender: "male",
        personalPrompt: "",
        isShow: true,
        // 国际化
        lang: getStoredLang(),
    }),
    getters: {
        t: (state) => (key) => {
            const messages = locales[state.lang] || locales['zh-CN'];
            return messages[key] || key;
        },
        currentLang: (state) => state.lang,
        isEn: (state) => state.lang === 'en',
        isZh: (state) => state.lang === 'zh-CN',
        aiLangDirective: (state) => {
            const messages = locales[state.lang] || locales['zh-CN'];
            return messages.aiLangDirective || '';
        },
    },
    actions: {
        setisOpenValue(newValue) {
            this.isOpenValue = newValue;
        },
        setuserImagePath(newValue) {
            this.userImagePath = newValue;
        },
        setaiImagePath(newValue) {
            this.aiImagePath = newValue;
        },
        setaudioType(newValue) {
            this.audioType = newValue;
        },
        setbaseUrl(newValue) {
            this.baseUrl = newValue;
        },
        setisPlayed(newValue) {
            this.isPlayed = newValue;
        },
        setGender(newValue) {
            this.gender = newValue;
        },
        setPersonalPrompt(newValue) {
            this.personalPrompt = newValue;
        },
        setIsShow(newValue) {
            this.isShow = newValue;
        },
        setChatHistory(newValue) {
            this.chatHistory = newValue;
        },
        setInfoHistory(newValue) {
            this.infoHistory = newValue;
        },
        setLang(lang) {
            this.lang = lang;
            setStoredLang(lang);
        },
        toggleLang() {
            const newLang = this.lang === 'zh-CN' ? 'en' : 'zh-CN';
            this.setLang(newLang);
        },
    },
});
