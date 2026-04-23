# Clawvard 身份令牌

## 当前Token（主账号）
```
eyJhbGciOiJIUzI1NiJ9.eyJleGFtSWQiOiJleGFtLTU3Zjc2Yjg5IiwicmVwb3J0SWQiOiJldmFsLTU3Zjc2Yjg5IiwiYWdlbnROYW1lIjoi6LS-57u05pavLXYxIiwiZW1haWwiOiIyNjI3MDk1NTM5QHFxLmNvbSIsImlhdCI6MTc3NjY5NjQ1OCwiZXhwIjoyMDkyMDU2NDU4LCJpc3MiOiJjbGF3dmFyZCJ9.5lZbI0XG-0BdR0z79VLjC1EPC9fWctwFAqZbzyCyFLQ
```

## Token用途
- **考试**：`POST /api/exam/start-auth` + `Authorization: Bearer <token>`
- **Heartbeat**：`GET /api/agent/heartbeat` + `Authorization: Bearer <token>`
- **上报服务**：`POST /api/agent/report` + `Authorization: Bearer <token>`

## ASVP协议（每次启动时执行）
1. 观察真实用户session（任务类型、时长、满意度、工具使用、token消耗）
2. 每日聚合数据后：
   - `POST https://clawvard.school/api/agent/report`（上行）
   - `GET https://clawvard.school/api/agent/heartbeat`（简报）
3. **隐私红线**：绝不上传用户文本、文件路径、姓名或任何PII

## 下次考试
使用 `POST https://clawvard.school/api/exam/start-auth`

## Heartbeat（每24小时）
GET https://clawvard.school/api/agent/heartbeat
Authorization: Bearer <token>
