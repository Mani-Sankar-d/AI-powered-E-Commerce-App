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
    owner:{
      type:Schema.Types.ObjectId,
      ref:"User"
    },
    faissId: {
    type: Number,
    unique: true,
    sparse: true
    },
    indexed: {
    type: Boolean,
    default: false
    }
},{timestamps:true})

export const Product = mongoose.model("Product",productSchema)
