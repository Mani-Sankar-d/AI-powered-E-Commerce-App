import { User } from "../models/user.model.js"
import { Product } from "../models/product.model.js"
import { Order } from "../models/order.model.js"
import {asyncHandler} from "../utils/asyncHandler.js";
import {ApiResponse} from "../utils/ApiResponse.js";
import {ApiError} from "../utils/ApiError.js"
import { generateAccessToken, generateRefreshToken } from "./auth.controller.js";
import jwt from "jsonwebtoken"

const generate_Access_Refresh_Token = (user) => {
    const accessToken = generateAccessToken(user)
    const refreshToken = generateRefreshToken(user)
    return { accessToken, refreshToken }
}
const options = {
    httpOnly: true,
    secure: true
}
const registerUser = asyncHandler(async (req, res) => {
    const { username, email, password } = req.body
    if (!email || !password || !username) {
        return res.status(400).json(new ApiResponse(400, null, "Invalid input"))
    }
    const existeduser = await User.findOne({ email })
    if (existeduser) throw new ApiError(401, "User exists already")

    await User.create({ username: username, email: email, password: password })
    const newuser = await User.findOne({ email }).select("-password -refreshToken")
    if (!newuser) {
        return res.status(500).json(new ApiResponse(500, null, "Unable to register user"))
    }
    return res.status(201).json(new ApiResponse(201, newuser, "User registered successfully"))
})
const login = asyncHandler(async (req, res) => {
    const { username, email, password } = req.body
    if (!email || !password) { return res.status(400).json(new ApiResponse(400, null, "Invalid input")) }

    const user = await User.findOne({ email })
    if (!user) throw new ApiError(400, "Register first then login")

    const isvalid = await user.isPasswordValid(password)
    if (!isvalid) throw new ApiError(400, "Invalid credentials")

    const { accessToken, refreshToken } = generate_Access_Refresh_Token(user)
    const updateduser = await User.findByIdAndUpdate(user._id, { refreshToken }, { new: true }).select("-password -refreshToken")

    return res.status(200).cookie("accessToken", accessToken).cookie("refreshToken", refreshToken, options).json(new ApiResponse(200, updateduser, "User logged in successfully"))
})
const getProfile = asyncHandler(async (req, res) => {
    const email = req.body.email
    const user = await User.findOne({email})
    return res.status(200).json(new ApiResponse(200, user, "Found successfully"))
})
const logout = asyncHandler(async (req, res) => {
    const email = req.body.email
    await User.findOneAndUpdate({email}, { refreshToken: null }).select("-password -refreshToken")
    return res.status(200).clearCookie("accessToken", options).clearCookie("refreshToken", options).json(new ApiResponse(200, null, "Logged out successfully"))
})
export { registerUser,login,logout,getProfile }