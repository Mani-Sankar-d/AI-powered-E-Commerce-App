import bcrypt from "bcrypt"
import { ApiError } from "../utils/ApiError.js"
import { User } from "../models/user.model.js"
import jwt from "jsonwebtoken"
import { asyncHandler } from "../utils/asyncHandler.js"
import { generateAccessToken, generateRefreshToken } from "../controllers/auth.controller.js"
const injectemail = asyncHandler(async (req, res, next) => {
  const accessToken = req.cookies.accessToken;
  const refreshToken = req.cookies.refreshToken;

  if (accessToken) {
    try {
      const decoded = jwt.verify(
        accessToken,
        process.env.ACCESS_TOKEN_SECRET
      );

      req.userId = decoded._id;
      req.userEmail = decoded.email;
      return next();
    } catch (err) {
    }
  }

  if (!refreshToken) {
    throw new ApiError(401, "Login first");
  }

  let decoded;
  try {
    decoded = jwt.verify(
      refreshToken,
      process.env.REFRESH_TOKEN_SECRET
    );
  } catch (err) {
    throw new ApiError(401, "Invalid refresh token");
  }

  const user = await User.findById(decoded._id);
  if (!user || user.refreshToken !== refreshToken) {
    throw new ApiError(401, "Refresh token revoked");
  }

  const newAccessToken = generateAccessToken(user);
  const newRefreshToken = generateRefreshToken(user);

  user.refreshToken = newRefreshToken;
  await user.save();

  res.cookie("accessToken", newAccessToken, {
    httpOnly: true,
    secure: true
  });

  res.cookie("refreshToken", newRefreshToken, {
    httpOnly: true,
    secure: true
  });

  req.userId = user._id;
  req.userEmail = user.email;

  next();
});


export { injectemail }