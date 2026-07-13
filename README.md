# 眾悅 Brand Guidelines｜內部互動版

悅聯集團內部使用的眾悅品牌規範網站。此專案為全新 GitHub 專案，不依賴也不修改既有網站。

## 專案目標

- 30 秒內找到規則。
- 快速判斷正確／錯誤。
- 直接下載正確 Logo 資產。
- 母法與子法分區，不混用。
- 規範內容可由 Markdown 維護並重新產生網站。

## 直接上線

本專案已包含預先產生的靜態網站，不需要 Node.js 或建置服務。

1. 建立新的 GitHub Repository。
2. 將本專案所有檔案推送到 Repository 根目錄。
3. GitHub Repository → **Settings → Pages**。
4. Source 選擇 **Deploy from a branch**。
5. Branch 選擇 `main`，Folder 選擇 `/(root)`。
6. 儲存後即可發布。

## 本機預覽

```bash
python -m http.server 8000
```

開啟 `http://localhost:8000`。

## 更新內容

1. 修改 `content/` 中的 Markdown。
2. 執行：

```bash
python tools/build.py
```

3. 檢查頁面後提交 Git。

建置腳本使用 Python 套件 `mistune`：

```bash
pip install -r requirements.txt
```

## 影像素材

影像素材不是上線必要條件。未上傳時，網站會顯示待補卡片。

預定位置：`assets/imagery/`

- `JY_img_identity_01.webp`
- `JY_img_identity_02.webp`
- `JY_img_evidence_01.webp`
- `JY_img_evidence_02.webp`

建議規格：1600 × 1200 px、WebP、sRGB、單檔 800 KB 以下。

## 字體

網站指定 `IBM Plex Sans TC` 為第一順位，並提供系統字體後備。專案不內嵌字體檔；內部電腦安裝 IBM Plex Sans TC 後即可正確顯示。

## 治理邊界

- `pages/constitution.html` 至 `pages/imagery.html`：品牌母法。
- `pages/resources.html`：資產與子法入口。
- 通路、工具、尺寸、模板等規則只進子法，不寫回母法。

## 內部使用

詳見 `INTERNAL_USE.md`。

## 發布安全提醒

此網站標示為內部使用。`robots.txt` 與 `noindex` 不等於權限保護。

- 使用 GitHub Enterprise Cloud 時，可評估 private Pages 存取控制。
- 一般公開 GitHub Pages 不適合放置敏感內部資料。
- 詳見 `SECURITY.md`。
