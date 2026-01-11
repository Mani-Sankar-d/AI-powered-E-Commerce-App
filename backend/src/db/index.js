import mongoose from "mongoose";
import { DB_NAME } from "../constants.js"
const connectDB = async()=>{
    try{
        const connectionInstance = await mongoose.connect(`${process.env.MONGO_URL}`)
    }catch(error){
        console.log("Error while connecting to DB",process.env.REFRESH_TOKEN_SECRET, error);
        process.exit(1)
    }
}
export default connectDB;