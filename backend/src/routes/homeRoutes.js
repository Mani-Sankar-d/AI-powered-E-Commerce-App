import { Router } from "express";
import { getAllProducts } from "../controllers/product.controller.js"
import { injectemail } from "../middleware/auth.middleware.js";


const homeRouter = Router();

homeRouter.get('/',injectemail,getAllProducts)

export default homeRouter;