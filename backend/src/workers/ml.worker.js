import mongoose from "mongoose"
import { Product } from "../models/product.model.js"
import axios from "axios"
import dotenv from "dotenv"

dotenv.config()

async function startWorker() {
    console.log("MONGO_URL =", process.env.MONGO_URL);
    console.log("MONGO_URI =", process.env.MONGO_URI);

  try {
    console.log("Connecting to DB...");
    await mongoose.connect(process.env.MONGO_URL);
    console.log("DB connected");

    await workerLoop();   // start only after DB is ready
  } catch (err) {
    console.error("Worker startup failed:", err);
    process.exit(1);
  }
}

async function processProduct(product) {
  try {
    const captionRes = await axios.post(
      `${process.env.ML_SERVER}/caption`,
      { image: product.img_url },
      { timeout: 15000 }
    );

    const embedRes = await axios.post(
      `${process.env.ML_SERVER}/enterEmbedding`,
      { url: product.img_url },
      { timeout: 15000 }
    );

    await Product.findByIdAndUpdate(product._id, {
      description: captionRes.data.caption,
      faissId: embedRes.data.faissId,
      indexed: true,
      status: "READY"
    });

  } catch (err) {
    await Product.findByIdAndUpdate(product._id, {
      status: "FAILED",
      mlError: err.message
    });
  }
}

async function workerLoop() {
  while (true) {
    console.log("Finding");

    const product = await Product.findOneAndUpdate(
      { status: "PENDING" },
      { status: "PROCESSING" },
      { new: true }
    );

    if (!product) {
      console.log("Not found")
      await new Promise(r => setTimeout(r, 3000));
      continue;
    }
    console.log("found")
    console.log("Found one");
    await processProduct(product);
  }
}

startWorker();
