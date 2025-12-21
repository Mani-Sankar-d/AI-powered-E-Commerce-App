import mongoose from "mongoose"

const productSchema = new mongoose.Schema({
    name:{
        type:String,
        required:true
    },
    description:{
      type:String  
    }
},{timestamps:true})

export const Product = mongoose.model("Product",productSchema)
