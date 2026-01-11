import express, {urlencoded} from 'express';
import cookieParser from 'cookie-parser';
import cors from 'cors';
const app = express();

app.use(express.json());
app.use(urlencoded({extended: true}));
app.use(cookieParser());    
app.use(express.static('public'));
app.use(cors({
  origin: "http://localhost:5173",
  credentials: true,
}));


import userRouter from './routes/userRoutes.js';
import productRouter from './routes/productRoutes.js';
import homeRouter from './routes/homeRoutes.js';

app.use('/api/users', userRouter);
app.use('/api/products', productRouter);
app.use('/api',homeRouter)
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