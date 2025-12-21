import express, {urlencoded} from 'express';
import cookieParser from 'cookie-parser';
import cors from 'cors';
const app = express();

app.use(express.json());
app.use(urlencoded({extended: true}));
app.use(cookieParser());    
app.use(express.static('public'));
app.use(cors())

import userRouter from './routes/userRoutes.js';
app.use('/api/users', userRouter);
app.use((err, req, res, next) => {
  console.error(err);

  const statusCode = err.statusCode || 500;
  const message = err.message || "Internal Server Error";

  res.status(statusCode).json({
    success: false,
    message
  });
});
export { app };