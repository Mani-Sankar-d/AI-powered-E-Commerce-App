import jwt from "jsonwebtoken"
import bcrypt from "bcrypt"

const generateAccessToken = (user)=>{
    return jwt.sign({
        _id :  user._id,
        username : user.username,
        email : user.email},
        process.env.ACCESS_TOKEN_SECRET,
        {expiresIn:"1m"}
    )
}

const generateRefreshToken = (user)=>{
    return jwt.sign({_id :  user._id},
        process.env.REFRESH_TOKEN_SECRET,
        {expiresIn:"1d"}
    )
}

export {generateAccessToken,generateRefreshToken}