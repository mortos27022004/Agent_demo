# E-Web Backend

Backend API server cho dự án E-Web.

## Cấu trúc thư mục

```
backend/
├── config/                 # File cấu hình
│   └── database.js        # Cấu hình kết nối database
├── src/
│   ├── controllers/       # Controllers xử lý logic
│   ├── models/           # Models định nghĩa cấu trúc dữ liệu
│   ├── routes/           # Routes định nghĩa endpoints
│   ├── services/         # Business logic
│   ├── middleware/       # Middleware functions
│   ├── utils/            # Utility functions
│   └── app.js            # Express app configuration
├── tests/                # Test files
├── public/               # Static files
├── logs/                 # Log files
├── create.sql            # Database schema
├── insert.sql            # Sample data
├── server.js             # Entry point
├── package.json          # Dependencies
├── .env.example          # Environment variables template
└── README.md             # Documentation
```

## Cài đặt

1. Clone repository
2. Copy `.env.example` thành `.env` và cập nhật thông tin
3. Cài đặt dependencies:

```bash
npm install
```

1. Tạo database bằng file `create.sql` và `insert.sql`

## Chạy ứng dụng

### Development mode

```bash
npm run dev
```

### Production mode

```bash
npm start
```

## API Endpoints

Các API endpoints sẽ được định nghĩa tại `/api/v1/...`

## Technologies

- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **MySQL** - Database
- **dotenv** - Environment variables
- **cors** - CORS middleware

## License

ISC
