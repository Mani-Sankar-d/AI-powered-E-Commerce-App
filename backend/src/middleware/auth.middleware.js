import bcrypt from "bcrypt"
import { ApiError } from "../utils/ApiError.js"
import { User } from "../models/user.model.js"
import jwt from "jsonwebtoken"
import { asyncHandler } from "../utils/asyncHandler.js"
const injectemail = asyncHandler(async(req,res,next)=>{
    const accessToken = req.cookies.accessToken
    if(!accessToken) throw new ApiError(401,"Register yourself then login in inject")
    
    try{
        const user =  jwt.verify(accessToken,process.env.ACCESS_TOKEN_SECRET)
        req.body.email = user.email
        next()
    }catch(err){
        throw new ApiError(400,"Token expired")
    }
})

export { injectemail }