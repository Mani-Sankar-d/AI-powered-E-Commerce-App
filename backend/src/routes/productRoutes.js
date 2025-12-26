import { Router } from "express";
import { getProducts,addProduct,getProductById,getProductsByName } from "../controllers/product.controller.js"
import { injectemail } from "../middleware/auth.middleware.js";
import upload from "../middleware/multer.middleware.js"

const productRouter = Router();

productRouter.get('/product-name',injectemail,getProducts)
productRouter.post('/new-product',injectemail,upload.single("image"),addProduct)
productRouter.get('/id/:id',injectemail,getProductById)
productRouter.get('/name/:name',injectemail,getProductsByName)
export default productRouter;