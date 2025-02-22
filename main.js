const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');

let win;
let games = []; // Lista para almacenar los juegos añadidos

async function createWindow() {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        fullscreen: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true,
        }
    });

    win.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Manejar eventos de configuración
ipcMain.on('toggle-fullscreen', () => {
    if (!win.isFullScreen()) {
        win.setFullScreen(true);
    } else {
        win.setFullScreen(false);
    }
});

ipcMain.on('toggle-windowed', () => {
    if (win.isFullScreen()) {
        win.setFullScreen(false);
        win.setSize(800, 600); // Tamaño de ventana en modo ventana
    }
});

// Función para agregar juegos desde la computadora
ipcMain.on('add-game', async (event) => {
    const result = await dialog.showOpenDialog(win, {
        properties: ['openFile'],
        filters: [{ name: 'Games', extensions: ['exe'] }]
    });

    if (!result.canceled) {
        const filePath = result.filePaths[0];
        const gameName = path.basename(filePath, '.exe');
        // Aquí no usamos file-icon, solo añadimos el juego con un ícono predeterminado o sin ícono.
        const gameIcon = 'default-game-icon.png'; // Puedes usar una imagen predeterminada si lo prefieres
        games.push({ name: gameName, icon: gameIcon }); // Añadir el juego a la lista
        event.sender.send('game-added', { name: gameName, icon: gameIcon });
    }
});

// Evento para salir de la aplicación
ipcMain.on('exit-app', () => {
    app.quit();
});
