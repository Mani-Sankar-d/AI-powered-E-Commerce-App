import { Router } from "express";
import { registerUser,login,logout,getProfile } from "../controllers/user.controller.js";
import { injectemail } from "../middleware/auth.middleware.js";

const userRouter = Router();
userRouter.get('/',(req,res)=>{
    console.log("User route accessed");
    res.send("User route is working");
})

userRouter.post('/register-user',registerUser)
userRouter.post('/login', login)
userRouter.post('/logout',injectemail,logout)
userRouter.get('/get-profile',injectemail,getProfile)


export default userRouter;