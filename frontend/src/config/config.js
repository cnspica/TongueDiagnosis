export const settings = {
    // 优先使用环境变量，默认 localhost
    ServerUrl: import.meta.env.VITE_API_URL || 'http://localhost:5000'
};

export default settings;
