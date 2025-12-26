import dotenv from 'dotenv';
dotenv.config({path: 'D:/repos/AI-powered-E-commerce/backend/src/.env'})

import connectDB from './db/index.js'
import { app }  from './app.js'

const PORT = process.env.PORT || 3000;
// console.log(process.env.CLOUDINARY_API_KEY)
connectDB()

try{
    app.listen(PORT, () => {
        console.log(`Server is running on port ${PORT}`);
    });
}catch(error){
    console.log('Error connecting to the database', error);
}