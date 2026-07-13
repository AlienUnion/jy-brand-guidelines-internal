# 發布與存取安全

本專案內容定位為公司內部使用。

## 重要限制

`robots.txt` 與 `noindex` 只能降低搜尋引擎收錄，不能提供存取控制。

- 若組織使用 **GitHub Enterprise Cloud**，可將組織擁有的 private/internal repository Pages 設為私密，只讓具 repository read 權限的人存取。
- 若沒有 GitHub Enterprise Cloud 的 private Pages 能力，不應把敏感內容直接發布成公開 GitHub Pages。
- 替代作法：保留 private GitHub repository 作版本來源，再部署到具有身分驗證的內部主機或 Cloudflare Access。

在確認存取方案前，請勿加入未公開的商業數據、客戶資訊、未發布產品或法律敏感內容。
