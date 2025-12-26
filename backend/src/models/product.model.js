import mongoose, { Schema } from "mongoose"

const productSchema = new mongoose.Schema({
    name:{
        type:String,
        required:true
    },
    price:{
      type:Number,
      required: true
    },
    userDescription:{
      type:String  
    },
    description:{
      type:String
    },
    img_url:{
      type:String
    },
    owner_email:{
      type:Schema.Types.ObjectId,
      ref:"User"
    },
    clipId: {
    type: Number,
    unique: true,
    index: true
  }
},{timestamps:true})

export const Product = mongoose.model("Product",productSchema)
