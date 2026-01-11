import dotenv from 'dotenv'
dotenv.config()

import { v2 as cloudinary } from "cloudinary";
console.log(process.env.CLOUDINARY_API_KEY)
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

const uploadOnCloudinary = (buffer, folder = "products") => {
  return new Promise((resolve, reject) => {
    cloudinary.uploader.upload_stream(
      { folder },
      (error, result) => {
        if (error) {
          reject(error);
        } else {
          resolve(result);
        }
      }
    ).end(buffer);
  }); 
};

export default uploadOnCloudinary;