import { asyncHandler } from "../utils/asyncHandler.js"
import { ApiError } from "../utils/ApiError.js"
import { ApiResponse } from "../utils/ApiResponse.js"
import { User } from "../models/user.model.js"
import { Product } from "../models/product.model.js"
import { Order } from "../models/order.model.js"
import uploadOnCloudinary from "../utils/cloudinary.js"
import axios from "axios";

const getProductsByName = asyncHandler(async(req,res)=>{
    const { name } = req.params
    const products = await Product.find({name})
    return res.status(200).json(new ApiResponse(200,`Got all products named ${name}`,products))
})

const getAllProducts = asyncHandler(async(req,res)=>{
    const products = await Product.find({}).sort({createdAt:-1}).select("-__v")
    return res.status(200).json(new ApiResponse(200,"Got all products",products))
})

const getProductById = asyncHandler(async(req,res)=>{
    const { id } = req.params
    const product = await Product.find({_id:id})
    if(product.length===0) throw new ApiError(400,"Not found")
    return res.status(200).json(new ApiResponse(200,"Got specified product",product))
})

const getProducts = asyncHandler(async (req, res) => {
    const product_name = req.body.product_name
    if (!product_name) throw new ApiError(400, "Product field empty")
    const products = await Product.find({ name: product_name })
    if (products.length === 0) throw new ApiError(400, "No such product")
    return res.status(200).json(new ApiResponse(200, "Found", products))
})

const addProduct = asyncHandler(async (req, res) => {
    if (!req.file) {
        throw new ApiError(400, "Image is required");
    }


    const fileBuffer = req.file.buffer;

    const result = await uploadOnCloudinary(fileBuffer);

    const imageUrl = result.secure_url;
    let finalCaption = req.body.description || null;
    let fId = null
    try {
        const captionResponse = await axios.post(
            `${process.env.CAPTION_SERVER}/caption`,
            {
                image: imageUrl,
                description: req.body.description || null
            },
            { timeout: 15000 } // prevent hanging forever
        );

        finalCaption = captionResponse.data.caption;
    } catch (err) {
        console.error("Caption service failed:", err.message);
        // fallback: keep user description or null
    }
    try{
        const embedResponse = await axios.post(
            `${process.env.CAPTION_SERVER}/enterEmbedding`,
            {
                url: imageUrl
            },
            { timeout: 15000 } // prevent hanging forever
        );

        fId = embedResponse.data.faissId;
    } catch (err) {
        console.error("Embed service failed:", err.message);
    }
    const product = await Product.create({
        name: req.body.name,
        price: req.body.price,
        description: finalCaption,
        owner: req.userId,
        img_url: imageUrl,
        faissId: fId,
        indexed:true
    });
    

    return res.status(201).json(
        new ApiResponse(201, product, "Product created successfully")
    );

});

export { getProducts, addProduct, getAllProducts,getProductById,getProductsByName }