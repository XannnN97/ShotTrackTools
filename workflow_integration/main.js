const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    useContentSize: true,
    minWidth: 700,
    minHeight: 500,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  mainWindow.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => { app.quit(); });

function getPythonEnv() {
  const env = Object.assign({}, process.env);
  const resolveModules = path.join(
    process.env.PROGRAMDATA || 'C:\\ProgramData',
    'Blackmagic Design', 'DaVinci Resolve', 'Support', 'Developer', 'Scripting', 'Modules'
  );
  env.PYTHONPATH = env.PYTHONPATH ? resolveModules + ';' + env.PYTHONPATH : resolveModules;
  if (!env.RESOLVE_SCRIPT_LIB) {
    env.RESOLVE_SCRIPT_LIB = 'C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll';
  }
  return env;
}

function findPythonCommand() {
  const { execSync } = require('child_process');
  const commands = ['python', 'python3', 'py'];
  for (const cmd of commands) {
    try {
      execSync(`${cmd} -c "from PIL import Image"`, { stdio: 'pipe', env: getPythonEnv() });
      console.log('Found Python with Pillow:', cmd);
      return cmd;
    } catch (e) {
      // 该命令没有 Pillow，尝试下一个
    }
  }
  console.log('No Python with Pillow found, fallback to py -3');
  return 'py -3';
}

async function callPython(action, data) {
  return new Promise((resolve, reject) => {
    const pluginDir = __dirname;
    const pythonCmd = findPythonCommand();
    const scriptPath = path.join(pluginDir, 'backend.py');

    const proc = spawn(pythonCmd, ['-3', scriptPath], {
      cwd: pluginDir,
      env: getPythonEnv(),
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (d) => { stdout += d.toString(); });
    proc.stderr.on('data', (d) => { stderr += d.toString(); });

    proc.on('close', (code) => {
      if (stderr) console.error('[Python stderr]', stderr);
      try {
        const lines = stdout.trim().split('\n').filter(l => l);
        const result = JSON.parse(lines[lines.length - 1]);
        resolve(result);
      } catch (e) {
        reject(new Error('Parse error. stdout: ' + stdout + ' | stderr: ' + stderr));
      }
    });

    proc.on('error', (err) => reject(err));
    proc.stdin.write(JSON.stringify({ action, ...data }) + '\n');
    proc.stdin.end();
  });
}

ipcMain.handle('execute', async (e, data) => callPython('execute', data));
ipcMain.handle('undo', async (e, data) => callPython('undo', data));
ipcMain.handle('browse-output', async () => {
  const r = await dialog.showOpenDialog(mainWindow, { properties: ['openDirectory'] });
  return r.filePaths[0] || null;
});
