const I18N = {
  zh: {
    title: "ShotTrackTools", version: "版本", batch_renamer: "批量替换", batch_sequential: "顺序递增",
    png_export: "PNG/XML 导出", remove_suffix: "去后缀", target_track: "目标轨道", search: "查找内容",
    replace: "替换为", prefix: "前缀", start_num: "起始编号", step: "步长", padding: "编号位数",
    output_dir: "输出目录", remove_suffix_label: "去掉文件后缀", execute: "执行", undo: "撤回",
    log: "日志", ready: "就绪", track_hint: "如 V10 / V1 / A1", browse: "浏览...",
    renamer_desc: "批量替换时间线 Clip Name", sequential_desc: "按固定前缀和步长递增命名",
    png_desc: "生成透明 PNG + FCP 7 XML v5", suffix_desc: "去掉媒体池 .png 后缀",
    executing: "执行中...", executed: "执行完成", undone: "已撤回", undo_disabled: "无可撤回操作",
    error: "错误", select_func: "请选择左侧功能"
  },
  en: {
    title: "ShotTrackTools", version: "Version", batch_renamer: "Batch Replace", batch_sequential: "Sequential",
    png_export: "PNG/XML Export", remove_suffix: "Remove Suffix", target_track: "Target Track", search: "Search",
    replace: "Replace", prefix: "Prefix", start_num: "Start Number", step: "Step", padding: "Padding",
    output_dir: "Output Directory", remove_suffix_label: "Remove File Suffix", execute: "Execute", undo: "Undo",
    log: "Log", ready: "Ready", track_hint: "e.g. V10 / V1 / A1", browse: "Browse...",
    renamer_desc: "Batch replace timeline Clip Name", sequential_desc: "Sequential naming with prefix",
    png_desc: "Generate transparent PNG + FCP 7 XML v5", suffix_desc: "Remove .png suffix from Media Pool",
    executing: "Executing...", executed: "Executed", undone: "Undone", undo_disabled: "No operation to undo",
    error: "Error", select_func: "Please select a function from the left"
  }
};

class App {
  constructor() {
    this.lang = 'zh';
    this.currentFunc = null;
    this.undoData = null;
    this.isExecuting = false;
    this.initElements();
    this.bindEvents();
    this.renderSidebar();
    this.updateLanguage();
  }

  initElements() {
    this.sidebar = document.getElementById('sidebar');
    this.content = document.getElementById('content');
    this.logBody = document.getElementById('logBody');
    this.statusText = document.getElementById('statusText');
    this.btnExecute = document.getElementById('btnExecute');
    this.btnUndo = document.getElementById('btnUndo');
  }

  bindEvents() {
    this.btnExecute.addEventListener('click', () => this.execute());
    this.btnUndo.addEventListener('click', () => this.undo());
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', (e) => { this.lang = e.target.dataset.lang; this.updateLanguage(); });
    });
  }

  t(key) { return I18N[this.lang]?.[key] || key; }

  updateLanguage() {
    document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.lang === this.lang));
    document.getElementById('versionText').textContent = this.t('version') + ' 1.1.0';
    document.getElementById('logHeader').textContent = this.t('log');
    this.btnExecute.textContent = this.t('execute');
    this.btnUndo.textContent = this.t('undo');
    this.renderSidebar();
    if (this.currentFunc) this.selectFunction(this.currentFunc);
    else this.content.innerHTML = '<p style="color:#888;padding:40px 0;text-align:center;">' + this.t('select_func') + '</p>';
  }

  renderSidebar() {
    const funcs = [
      { key: 'batch_renamer', desc: 'renamer_desc' },
      { key: 'batch_sequential', desc: 'sequential_desc' },
      { key: 'png_export', desc: 'png_desc' },
      { key: 'remove_suffix', desc: 'suffix_desc' }
    ];
    this.sidebar.innerHTML = funcs.map(f => `
      <button class="func-btn ${this.currentFunc === f.key ? 'active' : ''}" data-func="${f.key}">
        <div>${this.t(f.key)}</div>
        <div class="func-desc">${this.t(f.desc)}</div>
      </button>
    `).join('');
    this.sidebar.querySelectorAll('.func-btn').forEach(btn => {
      btn.addEventListener('click', () => this.selectFunction(btn.dataset.func));
    });
  }

  selectFunction(funcKey) {
    this.currentFunc = funcKey;
    this.renderSidebar();
    const forms = {
      batch_renamer: `
        <div class="param-group"><label class="param-label">${this.t('target_track')}</label>
          <input type="text" class="param-input" id="p_track" value="V10" placeholder="V10"><div class="param-hint">${this.t('track_hint')}</div></div>
        <div class="param-group"><label class="param-label">${this.t('search')}</label><input type="text" class="param-input" id="p_search" value="sq1300"></div>
        <div class="param-group"><label class="param-label">${this.t('replace')}</label><input type="text" class="param-input" id="p_replace" value="sq1400"></div>
        <div class="checkbox-row"><input type="checkbox" id="p_remove_suffix" checked><label>${this.t('remove_suffix_label')}</label></div>`,
      batch_sequential: `
        <div class="param-group"><label class="param-label">${this.t('target_track')}</label>
          <input type="text" class="param-input" id="p_track" value="V10" placeholder="V10"><div class="param-hint">${this.t('track_hint')}</div></div>
        <div class="param-group"><label class="param-label">${this.t('prefix')}</label><input type="text" class="param-input" id="p_prefix" value="2Esq1400_"></div>
        <div class="param-group"><label class="param-label">${this.t('start_num')}</label><input type="text" class="param-input" id="p_start" value="10"></div>
        <div class="param-group"><label class="param-label">${this.t('step')}</label><input type="text" class="param-input" id="p_step" value="10"></div>
        <div class="param-group"><label class="param-label">${this.t('padding')}</label><input type="text" class="param-input" id="p_padding" value="4"></div>
        <div class="checkbox-row"><input type="checkbox" id="p_remove_suffix" checked><label>${this.t('remove_suffix_label')}</label></div>`,
      png_export: `
        <div class="param-group"><label class="param-label">${this.t('target_track')}</label>
          <input type="text" class="param-input" id="p_track" value="V10" placeholder="V10"><div class="param-hint">${this.t('track_hint')}</div></div>
        <div class="param-group"><label class="param-label">${this.t('output_dir')}</label>
          <div class="output-row"><input type="text" class="param-input" id="p_output_dir" value="" placeholder="Desktop">
            <button class="btn btn-secondary" id="btnBrowse">${this.t('browse')}</button></div></div>
        <div class="checkbox-row"><input type="checkbox" id="p_remove_suffix" checked><label>${this.t('remove_suffix_label')}</label></div>`,
      remove_suffix: `<div class="param-group" style="padding:20px 0;"><p style="color:#888;line-height:1.6;">${this.t('suffix_desc')}</p></div>`
    };
    this.content.innerHTML = forms[funcKey] || '';
    if (funcKey === 'png_export') {
      document.getElementById('btnBrowse').addEventListener('click', () => this.browseOutput());
    }
    this.log('[INFO] ' + this.t(funcKey) + ' selected');
  }

  getParams() {
    const p = {};
    const gt = id => document.getElementById(id)?.value;
    const gc = id => document.getElementById(id)?.checked;
    if (this.currentFunc === 'batch_renamer') {
      p.track = gt('p_track'); p.search = gt('p_search'); p.replace = gt('p_replace'); p.remove_suffix = gc('p_remove_suffix');
    } else if (this.currentFunc === 'batch_sequential') {
      p.track = gt('p_track'); p.prefix = gt('p_prefix'); p.start = parseInt(gt('p_start')) || 10;
      p.step = parseInt(gt('p_step')) || 10; p.padding = parseInt(gt('p_padding')) || 4; p.remove_suffix = gc('p_remove_suffix');
    } else if (this.currentFunc === 'png_export') {
      p.track = gt('p_track'); p.output_dir = gt('p_output_dir'); p.remove_suffix = gc('p_remove_suffix');
    }
    return p;
  }

  async execute() {
    if (!this.currentFunc || this.isExecuting) return;
    this.isExecuting = true; this.btnExecute.disabled = true; this.btnExecute.textContent = this.t('executing');
    this.statusText.textContent = this.t('executing');
    try {
      const result = await window.electronAPI.execute({ type: this.currentFunc, params: this.getParams() });
      result.logs.forEach(l => this.log(l));
      if (result.success && result.undoData) { this.undoData = result.undoData; this.updateUndoButton(); }
      this.statusText.textContent = this.t('executed');
    } catch (err) { this.log('[ERROR] ' + err.message); this.statusText.textContent = this.t('error'); }
    finally { this.isExecuting = false; this.btnExecute.disabled = false; this.btnExecute.textContent = this.t('execute'); }
  }

  async undo() {
    if (!this.undoData || this.isExecuting) return;
    this.isExecuting = true; this.btnUndo.disabled = true; this.statusText.textContent = this.t('undone');
    try {
      const result = await window.electronAPI.undo({ undoData: this.undoData });
      result.logs.forEach(l => this.log(l));
      this.undoData = null; this.updateUndoButton(); this.statusText.textContent = this.t('undone');
    } catch (err) { this.log('[ERROR] ' + err.message); this.statusText.textContent = this.t('error'); }
    finally { this.isExecuting = false; this.btnUndo.disabled = false; }
  }

  updateUndoButton() {
    if (this.undoData) {
      this.btnUndo.disabled = false; this.btnUndo.className = 'btn btn-danger';
    } else {
      this.btnUndo.disabled = true; this.btnUndo.className = 'btn btn-secondary';
    }
  }

  async browseOutput() {
    const path = await window.electronAPI.browseOutput();
    if (path) document.getElementById('p_output_dir').value = path;
  }

  log(msg) {
    const line = document.createElement('div'); line.className = 'log-line';
    if (msg.startsWith('[ERROR]')) line.classList.add('error');
    else if (msg.startsWith('[WARNING]')) line.classList.add('warning');
    else if (msg.startsWith('Done') || msg.includes('完成')) line.classList.add('success');
    line.textContent = msg; this.logBody.appendChild(line); this.logBody.scrollTop = this.logBody.scrollHeight;
  }
}

const app = new App();
