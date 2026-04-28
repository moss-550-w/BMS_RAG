const api = require('../../utils/request.js');
const app = getApp();

Page({
  data: {
    messages: [],
    inputValue: '',
    loading: false,
    backendStatus: 'offline',
    scrollToId: '',
    showModal: false,
    activeCite: null,
    isInputActive: false
  },

  onLoad() {
    this.checkBackendStatus();
    // 加载历史记录
    const history = wx.getStorageSync('chat_history') || [];
    this.setData({
      messages: history
    }, () => {
      this.scrollToBottom();
    });
  },

  checkBackendStatus() {
    api.get('/status')
      .then(res => {
        this.setData({ backendStatus: 'online' });
      })
      .catch(() => {
        this.setData({ backendStatus: 'offline' });
      });
  },

  onInput(e) {
    this.setData({ inputValue: e.detail.value });
  },

  onInputFocus() {
    this.setData({ isInputActive: true });
  },

  onInputBlur() {
    this.setData({ isInputActive: false });
  },

  scrollToBottom() {
    this.setData({
      scrollToId: 'bottom-anchor'
    });
  },

  clearHistory() {
    wx.showModal({
      title: '提示',
      content: '确定清空所有对话记录吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({ messages: [] });
          wx.removeStorageSync('chat_history');
        }
      }
    });
  },

  rewriteQuery() {
    if (!this.data.inputValue) return;
    
    wx.showLoading({ title: '正在优化...' });
    api.post('/rewrite', { query: this.data.inputValue })
      .then(res => {
        this.setData({ inputValue: res.rewritten_query });
      })
      .finally(() => {
        wx.hideLoading();
      });
  },

  sendMessage() {
    const query = this.data.inputValue.trim();
    if (!query || this.data.loading) return;

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: query,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    this.setData({
      messages: [...this.data.messages, userMsg],
      inputValue: '',
      loading: true
    }, () => {
      this.scrollToBottom();
    });

    // 调用后端 API
    api.post('/query', {
      query: query,
      top_k: app.globalData.settings.topK,
      embedding_provider: app.globalData.settings.provider
    }).then(res => {
      const assistantMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: this.formatContent(res.answer),
        citations: res.citations || [],
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      this.setData({
        messages: [...this.data.messages, assistantMsg],
        loading: false
      }, () => {
        this.scrollToBottom();
        // 保存到本地
        wx.setStorageSync('chat_history', this.data.messages);
      });
    }).catch(() => {
      this.setData({ loading: false });
    });
  },

  formatContent(text) {
    // 简单的术语高亮转换 (实际可以更复杂)
    const terms = ['SOC', 'SOH', 'BMS', '电池均衡', '故障诊断'];
    let formatted = text;
    terms.forEach(term => {
      const reg = new RegExp(term, 'g');
      formatted = formatted.replace(reg, `<span class="term-highlight">${term}</span>`);
    });
    return formatted;
  },

  showCitation(e) {
    const cite = e.currentTarget.dataset.cite;
    this.setData({
      activeCite: cite,
      showModal: true
    });
  },

  closeModal() {
    this.setData({ showModal: false });
  },

  stopBubble() {},

  copyCite() {
    if (!this.data.activeCite) return;
    wx.setClipboardData({
      data: this.data.activeCite.content,
      success: () => {
        wx.showToast({ title: '已复制到剪贴板' });
      }
    });
  },

  goToLiterature() {
    // 暂时跳转到文献列表页
    this.closeModal();
    wx.switchTab({
      url: '/pages/literature/literature'
    });
  },

  startVoice() {
    wx.showToast({ title: '正在录音...', icon: 'none' });
  },

  endVoice() {
    wx.showToast({ title: '语音识别中...', icon: 'none' });
    // 模拟语音识别结果
    setTimeout(() => {
      this.setData({ inputValue: '请分析锂离子电池SOC估计方法' });
    }, 1000);
  }
});
