## 🧪 Manual Testing Instructions

### 1. Upload PDF
```bash
curl -X POST http://localhost:8000/pdf/upload -F "file=@sample.pdf"
