const { app, BrowserWindow, Menu } = require("electron");
const { autoUpdater } = require("electron-updater");

let mainWindow;

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    fullscreen: false,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  mainWindow.loadFile("src/index.html");

  // Auto-Updater
  autoUpdater.checkForUpdatesAndNotify();
});

autoUpdater.on("update-available", () => {
  console.log("Nueva actualización disponible.");
});

autoUpdater.on("update-downloaded", () => {
  console.log("Actualización lista. Reiniciando...");
  autoUpdater.quitAndInstall();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
